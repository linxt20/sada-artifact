"""Run skill-v9 direct augmentation and compare it with reference labels.

The script is intentionally query-level: for each reference augmentation package,
it runs `skill-v9/scripts/run_tapp.py augment-e2e` on the same source table and
query, then writes a BT comparison report into that package's `skill_v9_runs/`
folder.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent


def _find_lab8_dir() -> Path:
    for parent in (SCRIPT_DIR, *SCRIPT_DIR.parents):
        if (parent / "benchmark_data").exists() and (parent / "skill-v9").exists():
            return parent
    raise RuntimeError("Could not locate lab8 root")


LAB8_DIR = _find_lab8_dir()
REPO_ROOT = LAB8_DIR.parent
NEWDATA_DIR = LAB8_DIR / "benchmark_data" / "newData"
DATASETS_DIR = NEWDATA_DIR / "datasets"
QUERIES_FILE = NEWDATA_DIR / "queries_v7.json"
SKILL_SCRIPT = LAB8_DIR / "skill-v9" / "scripts" / "run_tapp.py"
SUMMARY_JSON = NEWDATA_DIR / "skill_v9_reference_comparison_summary.json"
SUMMARY_MD = NEWDATA_DIR / "skill_v9_reference_comparison_summary.md"

NULL_STRINGS = {"", "none", "null", "nan", "na", "n/a", "not mentioned", "not_mentioned"}
BAD_MULTI_VALUE_RE = re.compile(
    r"(?:^|_)(?:or|and)(?:_|$)|\s+(?:or|and|and/or)\s+|[|,/&]",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ReferencePackage:
    query_id: str
    dataset_name: str
    dataset_dir: Path
    package_dir: Path
    source_table: Path
    query_text: str
    expected_structure: str | None
    evidence_cols: list[str]
    query_record: dict[str, Any]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def _read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if suffix == ".csv":
        for encoding in ("utf-8-sig", "utf-8", "latin1", "cp1252"):
            try:
                return pd.read_csv(path, encoding=encoding)
            except UnicodeDecodeError:
                continue
        return pd.read_csv(path, encoding="latin1")
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix in {".pkl", ".pickle"}:
        payload = pd.read_pickle(path)
        if isinstance(payload, pd.DataFrame):
            return payload
        if isinstance(payload, dict) and isinstance(payload.get("data"), pd.DataFrame):
            return payload["data"]
    raise ValueError(f"Unsupported table format: {path}")


def _safe_slug(value: str) -> str:
    slug = re.sub(r"[^0-9A-Za-z_.-]+", "_", str(value)).strip("_")
    return slug or "run"


def _model_slug(model: str) -> str:
    return _safe_slug(model.replace("/", "_"))


def _load_query_records() -> dict[str, dict[str, Any]]:
    payload = _read_json(QUERIES_FILE)
    return {str(item["id"]): item for item in payload.get("queries", [])}


def _discover_reference_packages(query_ids: list[str] | None = None) -> list[ReferencePackage]:
    query_records = _load_query_records()
    selected = set(query_ids or [])
    packages: list[ReferencePackage] = []

    for gt_path in sorted(DATASETS_DIR.glob("*/augmentations/*/GT.json")):
        package_dir = gt_path.parent
        dataset_dir = package_dir.parent.parent
        gt = _read_json(gt_path)
        query_id = str((gt.get("query") or {}).get("id") or gt.get("meta", {}).get("query_id") or package_dir.name)
        if selected and query_id not in selected:
            continue
        record = query_records.get(query_id, {})
        meta = gt.get("meta") or {}
        table_name = record.get("table") or meta.get("original_table")
        if not table_name:
            raise ValueError(f"Cannot locate source table for {package_dir}")
        source_table = dataset_dir / str(table_name)
        if not source_table.exists():
            raise FileNotFoundError(f"Missing source table for {query_id}: {source_table}")
        query_text = str(record.get("query") or (gt.get("query") or {}).get("text") or "").strip()
        if not query_text:
            raise ValueError(f"Missing query text for {query_id}")
        specs_payload = _read_json(package_dir / "specs.json")
        packages.append(
            ReferencePackage(
                query_id=query_id,
                dataset_name=dataset_dir.name,
                dataset_dir=dataset_dir,
                package_dir=package_dir,
                source_table=source_table,
                query_text=query_text,
                expected_structure=record.get("expected_structure") or (gt.get("query") or {}).get("expected_structure"),
                evidence_cols=list(specs_payload.get("evidence_cols") or record.get("text_evidence_columns") or []),
                query_record=record,
            )
        )

    missing = selected - {package.query_id for package in packages}
    if missing:
        raise ValueError(f"No reference packages found for: {sorted(missing)}")
    return packages


def _source_new_columns(source: pd.DataFrame, augmented: pd.DataFrame) -> list[str]:
    source_cols = set(map(str, source.columns))
    return [str(col) for col in augmented.columns if str(col) not in source_cols]


def _expected_specs(package_dir: Path) -> list[dict[str, Any]]:
    specs_payload = _read_json(package_dir / "specs.json")
    specs = specs_payload.get("specs") or []
    return [spec for spec in specs if spec.get("name")]


def _extract_vocab(description: str) -> list[str]:
    match = re.search(r"\{([^}]+)\}", description or "")
    if not match:
        return []
    return [token.strip() for token in match.group(1).split(",") if token.strip()]


def _skill_specs(workdir: Path) -> dict[str, dict[str, Any]]:
    path = workdir / "specs.json"
    if not path.exists():
        return {}
    payload = _read_json(path)
    result: dict[str, dict[str, Any]] = {}
    for spec in payload.get("specs") or []:
        name = spec.get("name") or spec.get("Name")
        if name:
            result[str(name)] = spec
    return result


def _merge_names(items: Any) -> list[str]:
    names: list[str] = []
    if not isinstance(items, list):
        return names
    for item in items:
        if isinstance(item, dict) and item.get("name"):
            names.append(str(item["name"]))
        elif isinstance(item, str):
            names.append(item)
    return names


def _skill_run_summary(workdir: Path) -> dict[str, Any]:
    specs_path = workdir / "specs.json"
    categorization_path = workdir / "categorization.json"
    merge_path = workdir / "merge_report.json"
    result: dict[str, Any] = {
        "actual_intent_class": None,
        "actual_intent_subtype": None,
        "actual_structure_type": None,
        "actual_spec_count": 0,
        "actual_spec_names": [],
        "merge_status": None,
        "merge_kept_count": None,
        "merge_kept_names": [],
        "merge_dropped_count": None,
        "merge_dropped_names": [],
    }
    if specs_path.exists():
        specs_payload = _read_json(specs_path)
        planning_structure = specs_payload.get("planning_structure") or specs_payload.get("PlanningStructure") or {}
        specs = specs_payload.get("specs") or []
        result.update(
            {
                "actual_intent_class": specs_payload.get("intent_class") or specs_payload.get("IntentClass"),
                "actual_intent_subtype": specs_payload.get("intent_subtype") or specs_payload.get("IntentSubtype"),
                "actual_structure_type": planning_structure.get("StructureType") or planning_structure.get("structure_type"),
                "actual_spec_count": len(specs),
                "actual_spec_names": [str(spec.get("name") or spec.get("Name")) for spec in specs if spec.get("name") or spec.get("Name")],
            }
        )
    elif categorization_path.exists():
        categorization_payload = _read_json(categorization_path)
        planning_structure = categorization_payload.get("PlanningStructure") or categorization_payload.get("planning_structure") or {}
        categories = categorization_payload.get("Categories") or categorization_payload.get("categories") or []
        result.update(
            {
                "actual_intent_class": categorization_payload.get("IntentClass") or categorization_payload.get("intent_class"),
                "actual_intent_subtype": categorization_payload.get("IntentSubtype") or categorization_payload.get("intent_subtype"),
                "actual_structure_type": planning_structure.get("StructureType") or planning_structure.get("structure_type"),
                "actual_spec_count": len(categories),
                "actual_spec_names": [str(spec.get("Name") or spec.get("name")) for spec in categories if spec.get("Name") or spec.get("name")],
            }
        )
    if merge_path.exists():
        merge_payload = _read_json(merge_path)
        kept = _merge_names(merge_payload.get("kept"))
        dropped = _merge_names(merge_payload.get("dropped"))
        result.update(
            {
                "merge_status": merge_payload.get("status"),
                "merge_kept_count": len(kept),
                "merge_kept_names": kept,
                "merge_dropped_count": len(dropped),
                "merge_dropped_names": dropped,
            }
        )
    return result


def _domain_from_spec(spec: dict[str, Any]) -> list[str]:
    if isinstance(spec.get("domain"), list):
        return [str(value) for value in spec["domain"]]
    output_schema = spec.get("output_schema")
    if isinstance(output_schema, dict) and isinstance(output_schema.get("value_space"), list):
        return [str(value) for value in output_schema["value_space"]]
    description = str(spec.get("description") or spec.get("Description") or "")
    return _extract_vocab(description)


def _norm_col_name(value: str) -> str:
    return re.sub(r"[^0-9a-z]+", "", str(value).lower())


def _domain_overlap(left: list[str], right: list[str]) -> float:
    left_set = {str(item) for item in left if str(item).strip()}
    right_set = {str(item) for item in right if str(item).strip()}
    if not left_set or not right_set:
        return 0.0
    return len(left_set & right_set) / len(left_set | right_set)


def _match_expected_columns(
    expected_specs: list[dict[str, Any]],
    skill_columns: list[str],
    skill_specs: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    remaining = set(skill_columns)
    matches: dict[str, dict[str, Any]] = {}
    for spec in expected_specs:
        expected = str(spec["name"])
        if expected in remaining:
            matches[expected] = {"skill_column": expected, "mode": "exact", "score": 1.0}
            remaining.remove(expected)

    for spec in expected_specs:
        expected = str(spec["name"])
        if expected in matches:
            continue
        expected_norm = _norm_col_name(expected)
        expected_domain = _domain_from_spec(spec)
        best: tuple[float, str, float, float] | None = None
        for candidate in sorted(remaining):
            name_score = SequenceMatcher(None, expected_norm, _norm_col_name(candidate)).ratio()
            candidate_domain = _domain_from_spec(skill_specs.get(candidate, {}))
            domain_score = _domain_overlap(expected_domain, candidate_domain)
            score = max(name_score, 0.45 * name_score + 0.55 * domain_score)
            if best is None or score > best[0]:
                best = (score, candidate, name_score, domain_score)
        if not best:
            continue
        domain_required = bool(expected_domain and _domain_from_spec(skill_specs.get(best[1], {})))
        if domain_required and best[3] < 0.50:
            continue
        if best[0] >= 0.62 or (best[2] >= 0.45 and best[3] >= 0.50):
            _, candidate, name_score, domain_score = best
            matches[expected] = {
                "skill_column": candidate,
                "mode": "fuzzy",
                "score": round(float(best[0]), 4),
                "name_score": round(float(name_score), 4),
                "domain_score": round(float(domain_score), 4),
            }
            remaining.remove(candidate)
    return matches


def _normalize_value(value: Any) -> str | None:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int,)):
        return str(value)
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return str(value).strip()
    text = str(value).strip()
    if text.lower() in NULL_STRINGS:
        return None
    if text.lower() in {"true", "false"}:
        return text.lower()
    if re.fullmatch(r"\d+\.0", text):
        return text[:-2]
    return text


def _is_scalar_ok(value: str | None) -> bool:
    if value is None:
        return True
    return BAD_MULTI_VALUE_RE.search(value) is None


def _value_counts(values: list[str | None], limit: int = 12) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = "<NULL>" if value is None else value
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit])


def _evidence_excerpt(source: pd.DataFrame, row_index: int, evidence_cols: list[str], limit: int = 220) -> str:
    parts: list[str] = []
    for col in evidence_cols:
        if col not in source.columns:
            continue
        value = source.iloc[row_index][col]
        if pd.isna(value):
            continue
        text = str(value).replace("\r", " ").replace("\n", " ").strip()
        if text:
            parts.append(f"{col}: {text}")
    if not parts:
        row = source.iloc[row_index]
        for col in source.columns[:5]:
            value = row[col]
            if pd.isna(value):
                continue
            text = str(value).replace("\r", " ").replace("\n", " ").strip()
            if text:
                parts.append(f"{col}: {text}")
    joined = " | ".join(parts)
    return joined[: limit - 3] + "..." if len(joined) > limit else joined


def _row_id(source: pd.DataFrame, row_index: int) -> Any:
    for col in source.columns:
        if str(col).lower().endswith("id") or str(col).lower() in {"id", "number"}:
            value = source.iloc[row_index][col]
            return None if pd.isna(value) else value
    return None


def _compare_column(
    *,
    expected_col: str,
    skill_col: str | None,
    match: dict[str, Any] | None,
    expected_spec: dict[str, Any],
    source: pd.DataFrame,
    reference: pd.DataFrame,
    skill: pd.DataFrame,
    evidence_cols: list[str],
    sample_limit: int,
) -> dict[str, Any]:
    domain = _domain_from_spec(expected_spec)
    domain_set = set(domain)
    row_count = len(reference)
    base = {
        "expected_column": expected_col,
        "skill_column": skill_col,
        "match_mode": (match or {}).get("mode", "missing"),
        "match_score": (match or {}).get("score"),
        "domain": domain,
        "row_count": row_count,
    }
    if not skill_col or skill_col not in skill.columns or expected_col not in reference.columns:
        return {
            **base,
            "status": "missing",
            "coverage": 0.0,
            "domain_valid_rate": None,
            "scalar_valid_rate": None,
            "exact_accuracy": None,
            "mismatches_sample": [],
        }

    ref_values = [_normalize_value(value) for value in reference[expected_col].tolist()]
    skill_values = [_normalize_value(value) for value in skill[skill_col].tolist()]
    non_null = [value for value in skill_values if value is not None]
    invalid_domain = [value for value in non_null if domain_set and value not in domain_set]
    scalar_bad = [value for value in skill_values if not _is_scalar_ok(value)]
    exact_matches = sum(1 for ref, got in zip(ref_values, skill_values, strict=False) if ref == got)
    mismatches: list[dict[str, Any]] = []
    for row_index, (ref, got) in enumerate(zip(ref_values, skill_values, strict=False)):
        if ref == got:
            continue
        if len(mismatches) >= sample_limit:
            break
        mismatches.append(
            {
                "row_index": row_index,
                "row_id": _row_id(source, row_index),
                "reference": ref,
                "skill_v9": got,
                "evidence_excerpt": _evidence_excerpt(source, row_index, evidence_cols),
            }
        )

    confusion: dict[str, int] = {}
    for ref, got in zip(ref_values, skill_values, strict=False):
        if ref == got:
            continue
        key = f"{ref if ref is not None else '<NULL>'} -> {got if got is not None else '<NULL>'}"
        confusion[key] = confusion.get(key, 0) + 1

    return {
        **base,
        "status": "compared",
        "coverage": round(len(non_null) / row_count, 4) if row_count else 0.0,
        "reference_coverage": round(sum(value is not None for value in ref_values) / row_count, 4) if row_count else 0.0,
        "domain_invalid_count": len(invalid_domain),
        "domain_valid_rate": round(1.0 - (len(invalid_domain) / max(1, len(non_null))), 4),
        "scalar_violation_count": len(scalar_bad),
        "scalar_valid_rate": round(1.0 - (len(scalar_bad) / max(1, row_count)), 4),
        "exact_matches": exact_matches,
        "exact_accuracy": round(exact_matches / row_count, 4) if row_count else None,
        "skill_distribution_top": _value_counts(skill_values),
        "reference_distribution_top": _value_counts(ref_values),
        "confusion_top": dict(sorted(confusion.items(), key=lambda item: (-item[1], item[0]))[:15]),
        "mismatches_sample": mismatches,
    }


def _compare_run(package: ReferencePackage, workdir: Path, output_path: Path, sample_limit: int) -> dict[str, Any]:
    source = _read_table(package.source_table).reset_index(drop=True)
    reference = _read_table(package.package_dir / "augmented.csv").reset_index(drop=True)
    skill = _read_table(output_path).reset_index(drop=True)
    expected_specs = _expected_specs(package.package_dir)
    skill_columns = _source_new_columns(source, skill)
    skill_specs = _skill_specs(workdir)
    skill_run = _skill_run_summary(workdir)
    matches = _match_expected_columns(expected_specs, skill_columns, skill_specs)

    row_count_match = len(source) == len(reference) == len(skill)
    columns = []
    for spec in expected_specs:
        expected_col = str(spec["name"])
        match = matches.get(expected_col)
        columns.append(
            _compare_column(
                expected_col=expected_col,
                skill_col=(match or {}).get("skill_column"),
                match=match,
                expected_spec=spec,
                source=source,
                reference=reference,
                skill=skill,
                evidence_cols=package.evidence_cols,
                sample_limit=sample_limit,
            )
        )

    compared = [item for item in columns if item.get("status") == "compared"]
    exact_columns = [item for item in columns if item.get("match_mode") == "exact"]
    mapped_columns = [item for item in columns if item.get("match_mode") in {"exact", "fuzzy"}]
    missing_columns = [item["expected_column"] for item in columns if item.get("status") == "missing"]
    total_cells = sum(int(item["row_count"]) for item in compared)
    total_exact = sum(int(item.get("exact_matches") or 0) for item in compared)
    total_non_null = sum(int(round((item.get("coverage") or 0) * int(item["row_count"]))) for item in compared)
    total_domain_invalid = sum(int(item.get("domain_invalid_count") or 0) for item in compared)
    total_scalar_bad = sum(int(item.get("scalar_violation_count") or 0) for item in compared)

    exact_agreement = round(total_exact / total_cells, 4) if total_cells else None
    domain_valid_rate = round(1.0 - total_domain_invalid / max(1, total_non_null), 4) if compared else None
    scalar_valid_rate = round(1.0 - total_scalar_bad / max(1, total_cells), 4) if compared else None
    expected_count = len(expected_specs)
    summary = {
        "query_id": package.query_id,
        "dataset": package.dataset_name,
        "query": package.query_text,
        "expected_structure": package.expected_structure,
        "actual_structure_type": skill_run["actual_structure_type"],
        "structure_match": package.expected_structure == skill_run["actual_structure_type"],
        "actual_intent_class": skill_run["actual_intent_class"],
        "actual_intent_subtype": skill_run["actual_intent_subtype"],
        "actual_spec_count": skill_run["actual_spec_count"],
        "actual_spec_names": skill_run["actual_spec_names"],
        "merge_status": skill_run["merge_status"],
        "merge_kept_count": skill_run["merge_kept_count"],
        "merge_kept_names": skill_run["merge_kept_names"],
        "merge_dropped_count": skill_run["merge_dropped_count"],
        "merge_dropped_names": skill_run["merge_dropped_names"],
        "source_table": str(package.source_table.relative_to(REPO_ROOT)),
        "reference_package": str(package.package_dir.relative_to(REPO_ROOT)),
        "skill_workdir": str(workdir.relative_to(REPO_ROOT)),
        "skill_output": str(output_path.relative_to(REPO_ROOT)),
        "row_count": len(source),
        "row_count_match": row_count_match,
        "expected_column_count": expected_count,
        "skill_new_column_count": len(skill_columns),
        "skill_new_columns": skill_columns,
        "exact_expected_column_count": len(exact_columns),
        "mapped_expected_column_count": len(mapped_columns),
        "missing_expected_columns": missing_columns,
        "expected_column_recall_exact": round(len(exact_columns) / expected_count, 4) if expected_count else None,
        "expected_column_recall_mapped": round(len(mapped_columns) / expected_count, 4) if expected_count else None,
        "cell_exact_accuracy_on_mapped_columns": exact_agreement,
        "domain_valid_rate_on_mapped_columns": domain_valid_rate,
        "scalar_valid_rate_on_mapped_columns": scalar_valid_rate,
        "interpretation": "Reference labels are treated as GT; direct skill-v9 can match them or surface rows for review, but exact-match scoring cannot prove it exceeds the GT labels.",
    }
    return {"created_at": _now(), "summary": summary, "columns": columns}


def _write_bt_markdown(report: dict[str, Any], path: Path) -> None:
    summary = report["summary"]
    lines = [
        "# skill-v9 Reference BT Comparison",
        "",
        f"- Dataset: `{summary['dataset']}`",
        f"- Query ID: `{summary['query_id']}`",
        f"- Query: {summary['query']}",
        f"- Source table: `{summary['source_table']}`",
        f"- Skill output: `{summary['skill_output']}`",
        "",
        "## Overall",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Row count match | {summary['row_count_match']} |",
        f"| Expected structure | {summary['expected_structure']} |",
        f"| Actual structure | {summary['actual_structure_type']} |",
        f"| Structure match | {summary['structure_match']} |",
        f"| Actual intent class | {summary['actual_intent_class']} |",
        f"| Expected columns | {summary['expected_column_count']} |",
        f"| Skill specs before merge | {summary['actual_spec_count']} |",
        f"| Merge kept columns | {summary['merge_kept_count']} |",
        f"| Merge dropped columns | {summary['merge_dropped_count']} |",
        f"| Skill new columns | {summary['skill_new_column_count']} |",
        f"| Exact expected column recall | {summary['expected_column_recall_exact']} |",
        f"| Mapped expected column recall | {summary['expected_column_recall_mapped']} |",
        f"| Cell exact accuracy on mapped columns | {summary['cell_exact_accuracy_on_mapped_columns']} |",
        f"| Domain valid rate on mapped columns | {summary['domain_valid_rate_on_mapped_columns']} |",
        f"| Scalar valid rate on mapped columns | {summary['scalar_valid_rate_on_mapped_columns']} |",
        "",
        "## Column Results",
        "",
        "| Expected column | Skill column | Match | Coverage | Accuracy | Domain invalid | Scalar bad |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for item in report["columns"]:
        lines.append(
            "| {expected} | {skill} | {mode} | {coverage} | {accuracy} | {domain_bad} | {scalar_bad} |".format(
                expected=item.get("expected_column"),
                skill=item.get("skill_column") or "<missing>",
                mode=item.get("match_mode"),
                coverage=item.get("coverage"),
                accuracy=item.get("exact_accuracy"),
                domain_bad=item.get("domain_invalid_count"),
                scalar_bad=item.get("scalar_violation_count"),
            )
        )
    lines.extend(["", "## Mismatch Samples", ""])
    for item in report["columns"]:
        samples = item.get("mismatches_sample") or []
        if not samples:
            continue
        lines.append(f"### {item.get('expected_column')}")
        lines.append("")
        lines.append("| Row | Row ID | Reference | skill-v9 | Evidence |")
        lines.append("| ---: | --- | --- | --- | --- |")
        for sample in samples[:8]:
            evidence = str(sample.get("evidence_excerpt") or "").replace("|", "\\|")
            lines.append(
                f"| {sample.get('row_index')} | {sample.get('row_id')} | {sample.get('reference')} | {sample.get('skill_v9')} | {evidence} |"
            )
        lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(summary["interpretation"])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _run_skill_v9(package: ReferencePackage, args: argparse.Namespace) -> tuple[Path, Path, dict[str, Any]]:
    run_name = args.run_name or _model_slug(args.model)
    workdir = package.package_dir / "skill_v9_runs" / run_name
    output_path = workdir / f"augment.{args.output_format}"
    if args.force and workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        str(SKILL_SCRIPT),
        "augment-e2e",
        "--input",
        str(package.source_table),
        "--workdir",
        str(workdir),
        "--query",
        package.query_text,
        "--query-contract-json",
        json.dumps(package.query_record, ensure_ascii=False),
        "--model",
        args.model,
        "--max-workers",
        str(args.max_workers),
        "--attempts",
        str(args.attempts),
        "--claude-timeout",
        str(args.claude_timeout),
        "--output",
        str(output_path),
        "--output-format",
        args.output_format,
        "--allow-low-coverage-fallback",
    ]
    if args.force:
        command.append("--force")

    run_meta = {
        "query_id": package.query_id,
        "dataset": package.dataset_name,
        "started_at": _now(),
        "command": command,
        "cwd": str(REPO_ROOT),
        "model": args.model,
    }

    if args.skip_run:
        if not output_path.exists():
            raise FileNotFoundError(f"--skip-run requested but output does not exist: {output_path}")
        existing_meta = _read_json(workdir / "run_command.json") if (workdir / "run_command.json").exists() else run_meta
        existing_meta["last_comparison_reused_at"] = _now()
        existing_meta.setdefault("status", "skipped_existing_output")
        existing_meta.setdefault("returncode", 0)
        _write_json(workdir / "run_command.json", existing_meta)
        return workdir, output_path, existing_meta

    if output_path.exists() and not args.force:
        existing_meta = _read_json(workdir / "run_command.json") if (workdir / "run_command.json").exists() else run_meta
        existing_meta["last_comparison_reused_at"] = _now()
        existing_meta.setdefault("status", "existing_output")
        existing_meta.setdefault("returncode", 0)
        _write_json(workdir / "run_command.json", existing_meta)
        return workdir, output_path, existing_meta

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    _write_json(workdir / "run_command.json", run_meta)
    started = time.time()
    proc = subprocess.run(
        command,
        cwd=REPO_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=args.run_timeout,
        check=False,
    )
    (workdir / "_skill_v9_stdout.txt").write_text(proc.stdout, encoding="utf-8")
    (workdir / "_skill_v9_stderr.txt").write_text(proc.stderr, encoding="utf-8")
    run_meta.update(
        {
            "finished_at": _now(),
            "wall_seconds": round(time.time() - started, 2),
            "returncode": proc.returncode,
            "stdout_tail": proc.stdout[-4000:],
            "stderr_tail": proc.stderr[-4000:],
            "status": "ok" if proc.returncode == 0 and output_path.exists() else "failed",
        }
    )
    _write_json(workdir / "run_command.json", run_meta)
    if proc.returncode != 0 or not output_path.exists():
        raise RuntimeError(f"skill-v9 run failed for {package.query_id}; see {workdir}")
    return workdir, output_path, run_meta


def _run_paths(package: ReferencePackage, args: argparse.Namespace) -> tuple[Path, Path]:
    run_name = args.run_name or _model_slug(args.model)
    workdir = package.package_dir / "skill_v9_runs" / run_name
    return workdir, workdir / f"augment.{args.output_format}"


def _failure_report(package: ReferencePackage, args: argparse.Namespace, error: Exception) -> dict[str, Any]:
    workdir, output_path = _run_paths(package, args)
    skill_run = _skill_run_summary(workdir)
    expected_specs = _expected_specs(package.package_dir)
    error_text = str(error)
    error_path = workdir / "augment_e2e_error.json"
    if error_path.exists():
        error_payload = _read_json(error_path)
        error_text = str(error_payload.get("error") or error_payload)
    summary = {
        "query_id": package.query_id,
        "dataset": package.dataset_name,
        "query": package.query_text,
        "run_status": "failed",
        "error": error_text,
        "expected_structure": package.expected_structure,
        "actual_structure_type": skill_run["actual_structure_type"],
        "structure_match": package.expected_structure == skill_run["actual_structure_type"] if skill_run["actual_structure_type"] else None,
        "actual_intent_class": skill_run["actual_intent_class"],
        "actual_intent_subtype": skill_run["actual_intent_subtype"],
        "actual_spec_count": skill_run["actual_spec_count"],
        "actual_spec_names": skill_run["actual_spec_names"],
        "merge_status": skill_run["merge_status"],
        "merge_kept_count": skill_run["merge_kept_count"],
        "merge_kept_names": skill_run["merge_kept_names"],
        "merge_dropped_count": skill_run["merge_dropped_count"],
        "merge_dropped_names": skill_run["merge_dropped_names"],
        "source_table": str(package.source_table.relative_to(REPO_ROOT)),
        "reference_package": str(package.package_dir.relative_to(REPO_ROOT)),
        "skill_workdir": str(workdir.relative_to(REPO_ROOT)),
        "skill_output": str(output_path.relative_to(REPO_ROOT)),
        "row_count": None,
        "row_count_match": False,
        "expected_column_count": len(expected_specs),
        "skill_new_column_count": 0,
        "skill_new_columns": [],
        "exact_expected_column_count": 0,
        "mapped_expected_column_count": 0,
        "missing_expected_columns": [str(spec.get("name")) for spec in expected_specs],
        "expected_column_recall_exact": 0.0 if expected_specs else None,
        "expected_column_recall_mapped": 0.0 if expected_specs else None,
        "cell_exact_accuracy_on_mapped_columns": None,
        "domain_valid_rate_on_mapped_columns": None,
        "scalar_valid_rate_on_mapped_columns": None,
        "interpretation": "skill-v9 did not produce an augmented table for this query; inspect the workdir failure artifacts before judging row-level quality.",
    }
    report = {"created_at": _now(), "summary": summary, "columns": [], "failure": {"error": error_text}}
    _write_json(workdir / "BT_COMPARISON.json", report)
    _write_failure_markdown(report, workdir / "BT_COMPARISON.md")
    return report


def _update_aggregate_summary(reports: list[dict[str, Any]]) -> None:
    existing: list[dict[str, Any]] = []
    if SUMMARY_JSON.exists():
        payload = _read_json(SUMMARY_JSON)
        existing = list(payload.get("reports") or [])
    by_key = {item["summary"]["query_id"]: item for item in existing if item.get("summary")}
    for report in reports:
        by_key[report["summary"]["query_id"]] = report
    merged = list(sorted(by_key.values(), key=lambda item: item["summary"]["query_id"]))
    _write_json(SUMMARY_JSON, {"updated_at": _now(), "reports": merged})

    lines = [
        "# skill-v9 Reference Comparison Summary",
        "",
        "| Status | Dataset | Query ID | Expected structure | Actual structure | Structure match | Specs | Kept | Dropped | Exact recall | Mapped recall | Cell accuracy | Output / workdir | Error |",
        "| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for report in merged:
        summary = report["summary"]
        error = str(summary.get("error") or "").replace("|", "\\|")[:180]
        lines.append(
            "| {status} | {dataset} | {query_id} | {expected_structure} | {actual_structure} | {structure_match} | {specs} | {kept} | {dropped} | {exact_recall} | {mapped_recall} | {accuracy} | `{output}` | {error} |".format(
                status=summary.get("run_status", "ok"),
                dataset=summary["dataset"],
                query_id=summary["query_id"],
                expected_structure=summary.get("expected_structure"),
                actual_structure=summary.get("actual_structure_type"),
                structure_match=summary.get("structure_match"),
                specs=summary.get("actual_spec_count"),
                kept=summary.get("merge_kept_count"),
                dropped=summary.get("merge_dropped_count"),
                exact_recall=summary["expected_column_recall_exact"],
                mapped_recall=summary["expected_column_recall_mapped"],
                accuracy=summary["cell_exact_accuracy_on_mapped_columns"],
                output=summary["skill_output"],
                error=error,
            )
        )
    lines.append("")
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")


def _write_failure_markdown(report: dict[str, Any], path: Path) -> None:
    summary = report["summary"]
    lines = [
        "# skill-v9 Reference BT Comparison",
        "",
        "## Failure",
        "",
        f"- Dataset: `{summary['dataset']}`",
        f"- Query ID: `{summary['query_id']}`",
        f"- Query: {summary['query']}",
        f"- Expected structure: `{summary.get('expected_structure')}`",
        f"- Actual structure before failure: `{summary.get('actual_structure_type')}`",
        f"- Actual intent class before failure: `{summary.get('actual_intent_class')}`",
        f"- Skill workdir: `{summary.get('skill_workdir')}`",
        "",
        "```text",
        str(summary.get("error") or ""),
        "```",
        "",
        "No augmented table was produced, so row-level BT scoring was not run.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def run_one(package: ReferencePackage, args: argparse.Namespace) -> dict[str, Any]:
    print(f"[skill-v9] running {package.query_id}", flush=True)
    workdir, output_path, run_meta = _run_skill_v9(package, args)
    print(f"[skill-v9] comparing {package.query_id}", flush=True)
    report = _compare_run(package, workdir, output_path, sample_limit=args.sample_limit)
    report["run"] = run_meta
    _write_json(workdir / "BT_COMPARISON.json", report)
    _write_bt_markdown(report, workdir / "BT_COMPARISON.md")
    if not args.no_summary_update:
        _update_aggregate_summary([report])
    summary = report["summary"]
    print(
        "[skill-v9] done {qid}: mapped_recall={recall} cell_accuracy={acc} output={out}".format(
            qid=package.query_id,
            recall=summary["expected_column_recall_mapped"],
            acc=summary["cell_exact_accuracy_on_mapped_columns"],
            out=summary["skill_output"],
        ),
        flush=True,
    )
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query-id", action="append", default=None, help="Reference query id to run. Repeatable.")
    parser.add_argument("--limit", type=int, default=0, help="Optional limit after query-id filtering.")
    parser.add_argument("--model", default="copilot/claude-opus-4.8-xhigh")
    parser.add_argument("--run-name", default=None, help="Subfolder under skill_v9_runs/. Defaults to a slug of --model.")
    parser.add_argument("--max-workers", type=int, default=2)
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument("--claude-timeout", type=int, default=900)
    parser.add_argument("--run-timeout", type=int, default=7200)
    parser.add_argument("--output-format", choices=("csv", "xlsx", "parquet"), default="csv")
    parser.add_argument("--sample-limit", type=int, default=12)
    parser.add_argument("--skip-run", action="store_true", help="Only compare an existing skill-v9 output.")
    parser.add_argument("--force", action="store_true", help="Delete the run workdir before running skill-v9.")
    parser.add_argument("--continue-on-error", action="store_true", help="Write failure reports and continue with later query ids.")
    parser.add_argument("--no-summary-update", action="store_true", help="Write per-run comparison files only; do not update aggregate summary files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packages = _discover_reference_packages(args.query_id)
    if args.limit:
        packages = packages[: max(0, args.limit)]
    if not packages:
        print("No reference packages selected.")
        return 0
    reports: list[dict[str, Any]] = []
    for package in packages:
        try:
            reports.append(run_one(package, args))
        except Exception as exc:
            if not args.continue_on_error:
                raise
            report = _failure_report(package, args, exc)
            reports.append(report)
            if not args.no_summary_update:
                _update_aggregate_summary([report])
            print(f"[skill-v9] failed {package.query_id}: {exc}", flush=True)
    if not args.no_summary_update:
        _update_aggregate_summary(reports)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
