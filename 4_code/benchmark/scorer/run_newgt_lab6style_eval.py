"""Run Lab8 newData evaluation with Lab6-style analysis BT.

Pipeline stages:
1. Audit the GT package itself for structure, expected-column recall, value-domain
   validity, and optional LLM semantic sanity checks.
2. Run semantic reference recall for candidate skill outputs against the GT schema.
3. Generate one analysis report per available augmented table: GT and candidates.
4. Compare those reports with the Lab8/Lab6 pairwise grader in both A/B orders,
   then aggregate with swap-stabilized Bradley-Terry.

This script is intentionally additive. It does not replace the older direct
reference-comparison scripts; it orchestrates their strongest parts into one
Lab6-like evaluation path.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterable, Sequence

import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
LAB8_DIR = SCRIPT_DIR.parent
REPO_ROOT = LAB8_DIR.parent
NEWDATA_DIR = LAB8_DIR / "benchmark_data" / "newData"
SUMMARY_DIR = NEWDATA_DIR / "report_archive" / "lab6style_eval"

sys.path.insert(0, str(SCRIPT_DIR))
import semantic_reference_recall as semrec  # noqa: E402
from grader_v3 import (  # noqa: E402
    PKOutcome,
    _extract_text_from_claude_json,
    _invoke_claude,
    aggregate_dimension_scores,
    bradley_terry_mm,
    compute_bt_payload,
    find_claude,
    judge_pairwise,
)


ITEM_GT = "newData_GT"
DEFAULT_CANDIDATES = ("skill_v7", "skill_v8", "skill_v9")
DEFAULT_RUN_NAME = "lab6style_gt_semantic_analysis_bt"


@dataclass(frozen=True)
class VariantArtifact:
    name: str
    table_path: Path
    workdir: Path | None
    augmented_columns: list[str]
    status: str
    semantic_recall: dict[str, Any] | None = None
    direct_comparison: dict[str, Any] | None = None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT.resolve()))
    except Exception:
        return str(path)


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_") or "item"


def _safe_text(value: Any, max_len: int = 180) -> str:
    text = str(value if value is not None else "").replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text).replace("|", "\\|").strip()
    if len(text) > max_len:
        return text[: max_len - 3].rstrip() + "..."
    return text


def _query_id(package: semrec.ReferencePackage) -> str:
    return package.query_id


def _rank(scores: dict[str, float], items: Sequence[str]) -> list[str]:
    return sorted(items, key=lambda item: (-scores.get(item, 0.0), item))


def _winner_from_scores(scores: dict[str, float], items: Sequence[str]) -> str:
    if not scores or not items:
        return "unknown"
    best = max(scores.get(item, 0.0) for item in items)
    winners = [item for item in items if math.isclose(scores.get(item, 0.0), best, abs_tol=1e-6)]
    return "tie:" + ",".join(winners) if len(winners) > 1 else winners[0]


def _source_new_columns(source: pd.DataFrame, augmented: pd.DataFrame) -> list[str]:
    source_cols = set(map(str, source.columns))
    return [str(col) for col in augmented.columns if str(col) not in source_cols]


def _value_counts_list(series: pd.Series, limit: int = 12) -> list[dict[str, Any]]:
    counts = series.fillna("<null>").astype(str).value_counts(dropna=False).head(limit)
    total = max(1, len(series))
    return [
        {"value": _safe_text(value, 90), "count": int(count), "share": round(float(count) / total, 4)}
        for value, count in counts.items()
    ]


def _is_numeric(series: pd.Series) -> bool:
    return pd.api.types.is_numeric_dtype(series)


def _column_profile(frame: pd.DataFrame, column: str, spec: dict[str, Any] | None = None) -> dict[str, Any]:
    series = frame[column]
    profile: dict[str, Any] = {
        "column": column,
        "dtype": str(series.dtype),
        "coverage": round(float(series.notna().sum()) / max(1, len(series)), 4),
        "unique": int(series.nunique(dropna=True)),
    }
    if spec:
        profile["description"] = semrec._description_from_spec(spec)
        profile["domain"] = semrec._domain_from_spec(spec)[:30]
    if _is_numeric(series):
        numeric = pd.to_numeric(series, errors="coerce")
        profile["stats"] = {
            "mean": None if numeric.dropna().empty else round(float(numeric.mean()), 4),
            "median": None if numeric.dropna().empty else round(float(numeric.median()), 4),
            "min": None if numeric.dropna().empty else round(float(numeric.min()), 4),
            "max": None if numeric.dropna().empty else round(float(numeric.max()), 4),
        }
    else:
        profile["top_values"] = _value_counts_list(series, 12)
    return profile


def _focus_summary(frame: pd.DataFrame, focus: str | None) -> dict[str, Any]:
    if not focus or focus not in frame.columns:
        return {"available": False, "focus": focus}
    series = frame[focus]
    if _is_numeric(series):
        numeric = pd.to_numeric(series, errors="coerce")
        return {
            "available": True,
            "focus": focus,
            "type": "numeric",
            "mean": None if numeric.dropna().empty else round(float(numeric.mean()), 4),
            "median": None if numeric.dropna().empty else round(float(numeric.median()), 4),
            "min": None if numeric.dropna().empty else round(float(numeric.min()), 4),
            "max": None if numeric.dropna().empty else round(float(numeric.max()), 4),
        }
    return {"available": True, "focus": focus, "type": "categorical", "counts": _value_counts_list(series, 12)}


def _relationships_to_focus(frame: pd.DataFrame, augmented_columns: Sequence[str], focus: str | None, limit: int = 10) -> list[dict[str, Any]]:
    if not focus or focus not in frame.columns:
        return []
    relationships: list[dict[str, Any]] = []
    focus_series = frame[focus]
    for column in list(augmented_columns)[:limit]:
        if column not in frame.columns:
            continue
        labels = frame[column].fillna("<null>").astype(str)
        if _is_numeric(focus_series):
            numeric_frame = frame.assign(__label=labels)
            grouped = numeric_frame.groupby("__label")[focus].agg(["count", "mean", "median"]).reset_index()
            grouped = grouped.sort_values(["count", "mean"], ascending=[False, False]).head(10)
            relationships.append(
                {
                    "column": column,
                    "focus": focus,
                    "type": "numeric_focus_by_label",
                    "groups": [
                        {
                            "label": _safe_text(row["__label"], 80),
                            "count": int(row["count"]),
                            "mean": None if pd.isna(row["mean"]) else round(float(row["mean"]), 4),
                            "median": None if pd.isna(row["median"]) else round(float(row["median"]), 4),
                        }
                        for _, row in grouped.iterrows()
                    ],
                }
            )
        else:
            ctab = pd.crosstab(labels, focus_series.fillna("<null>").astype(str), normalize="index").round(4)
            counts = labels.value_counts().to_dict()
            groups = []
            for label in list(ctab.index)[:10]:
                top_focus = ctab.loc[label].sort_values(ascending=False).head(4).to_dict()
                groups.append(
                    {
                        "label": _safe_text(label, 80),
                        "count": int(counts.get(label, 0)),
                        "focus_distribution": {str(key): float(value) for key, value in top_focus.items()},
                    }
                )
            relationships.append({"column": column, "focus": focus, "type": "categorical_focus_by_label", "groups": groups})
    return relationships


def _sample_rows(
    frame: pd.DataFrame,
    augmented_columns: Sequence[str],
    evidence_cols: Sequence[str],
    focus: str | None,
    limit: int = 8,
) -> list[dict[str, Any]]:
    cols = list(dict.fromkeys([*evidence_cols, *([focus] if focus and focus in frame.columns else []), *augmented_columns[:8]]))
    cols = [col for col in cols if col in frame.columns]
    if not cols:
        cols = [str(col) for col in frame.columns[: min(8, len(frame.columns))]]
    rows = frame[cols].head(limit).to_dict(orient="records")
    return [{str(key): _safe_text(value, 140) for key, value in row.items()} for row in rows]


def _spec_by_name(specs: Sequence[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(spec.get("name")): spec for spec in specs if spec.get("name")}


def _domain_keys(spec: dict[str, Any]) -> set[str]:
    return {key for key in (semrec._semantic_key(value) for value in semrec._domain_from_spec(spec)) if key}


def _scalar_violation(value: Any) -> bool:
    text = semrec._normalize_value(value)
    if text is None:
        return False
    return any(sep in str(text) for sep in (";", "|"))


def _deterministic_gt_audit(package: semrec.ReferencePackage) -> dict[str, Any]:
    source = semrec._read_table(package.source_table).reset_index(drop=True)
    reference_path = package.package_dir / "augmented.csv"
    reference = semrec._read_table(reference_path).reset_index(drop=True)
    specs = semrec._expected_specs(package.package_dir)
    expected_names = [str(spec["name"]) for spec in specs if spec.get("name")]
    source_cols = set(map(str, source.columns))
    new_cols = [str(col) for col in reference.columns if str(col) not in source_cols]
    expected_present = [name for name in expected_names if name in reference.columns]
    missing_expected = [name for name in expected_names if name not in reference.columns]
    extra_new_cols = [name for name in new_cols if name not in set(expected_names)]
    evidence_cols_present = [col for col in package.evidence_cols if col in source.columns]
    evidence_cols_missing = [col for col in package.evidence_cols if col not in source.columns]

    column_audits: list[dict[str, Any]] = []
    total_domain_checked = 0
    total_domain_valid = 0
    critical_issues: list[str] = []
    warnings: list[str] = []
    if len(source) != len(reference):
        critical_issues.append("row_count_mismatch")
    if missing_expected:
        critical_issues.append("missing_expected_gt_columns")
    if evidence_cols_missing:
        warnings.append("missing_expected_evidence_columns")

    for spec in specs:
        name = str(spec.get("name"))
        if name not in reference.columns:
            column_audits.append({"column": name, "present": False, "status": "missing"})
            continue
        series = reference[name]
        domain_keys = _domain_keys(spec)
        non_null_values = [value for value in series.tolist() if semrec._normalize_value(value) is not None]
        invalid_samples: list[Any] = []
        in_domain = 0
        scalar_violations = 0
        for value in non_null_values:
            key = semrec._semantic_key(value)
            if not domain_keys or key in domain_keys:
                in_domain += 1
            elif len(invalid_samples) < 8:
                invalid_samples.append(value)
            if spec.get("domain_is_single_scalar") is True and not spec.get("multi_label_allowed") and _scalar_violation(value):
                scalar_violations += 1
        if domain_keys:
            total_domain_checked += len(non_null_values)
            total_domain_valid += in_domain
        domain_valid_rate = round(in_domain / len(non_null_values), 4) if non_null_values and domain_keys else None
        if domain_valid_rate is not None and domain_valid_rate < 0.98:
            warnings.append(f"low_domain_validity:{name}")
        if scalar_violations:
            warnings.append(f"scalar_violations:{name}")
        column_audits.append(
            {
                "column": name,
                "present": True,
                "coverage": round(float(series.notna().sum()) / max(1, len(series)), 4),
                "unique": int(series.nunique(dropna=True)),
                "domain_size": len(domain_keys),
                "domain_valid_rate": domain_valid_rate,
                "out_of_domain_sample": [_safe_text(value, 80) for value in invalid_samples],
                "scalar_violation_count": scalar_violations,
                "top_values": _value_counts_list(series, 10),
            }
        )

    expected_count = len(expected_names)
    new_count = len(new_cols)
    domain_valid_rate = round(total_domain_valid / total_domain_checked, 4) if total_domain_checked else None
    return {
        "query_id": package.query_id,
        "dataset": package.dataset_name,
        "query": package.query_text,
        "package": _rel(package.package_dir),
        "source_table": _rel(package.source_table),
        "reference_table": _rel(reference_path),
        "row_count_source": int(len(source)),
        "row_count_gt": int(len(reference)),
        "row_count_match": len(source) == len(reference),
        "expected_column_count": expected_count,
        "gt_new_column_count": new_count,
        "expected_columns_present": len(expected_present),
        "gt_expected_column_recall": round(len(expected_present) / expected_count, 4) if expected_count else None,
        "gt_expected_column_precision": round(len(expected_present) / new_count, 4) if new_count else None,
        "missing_expected_columns": missing_expected,
        "extra_new_columns": extra_new_cols,
        "evidence_columns_present": evidence_cols_present,
        "evidence_columns_missing": evidence_cols_missing,
        "domain_valid_cell_rate": domain_valid_rate,
        "critical_issues": sorted(set(critical_issues)),
        "warnings": sorted(set(warnings)),
        "column_audits": column_audits,
    }


def _gt_audit_samples(package: semrec.ReferencePackage, limit: int) -> list[dict[str, Any]]:
    source = semrec._read_table(package.source_table).reset_index(drop=True)
    reference = semrec._read_table(package.package_dir / "augmented.csv").reset_index(drop=True)
    expected_names = [str(spec["name"]) for spec in semrec._expected_specs(package.package_dir) if spec.get("name")]
    rows = []
    for idx in range(min(limit, len(source), len(reference))):
        evidence = {col: _safe_text(source.iloc[idx][col], 220) for col in package.evidence_cols if col in source.columns}
        labels = {col: _safe_text(reference.iloc[idx][col], 120) for col in expected_names if col in reference.columns}
        rows.append({"row_index": idx, "evidence": evidence, "gt_labels": labels})
    return rows


def _gt_llm_prompt(package: semrec.ReferencePackage, deterministic: dict[str, Any], sample_limit: int) -> str:
    specs = semrec._expected_specs(package.package_dir)
    task = {
        "query_id": package.query_id,
        "dataset": package.dataset_name,
        "query": package.query_text,
        "query_record": package.query_record,
        "deterministic_audit_summary": {key: value for key, value in deterministic.items() if key != "column_audits"},
        "expected_specs": [
            {
                "name": spec.get("name"),
                "description": semrec._description_from_spec(spec),
                "domain": semrec._domain_from_spec(spec)[:40],
            }
            for spec in specs
        ],
        "column_audit_head": deterministic.get("column_audits", [])[:20],
        "sample_rows": _gt_audit_samples(package, sample_limit),
    }
    return (
        "You are auditing a GT annotation package for a text-to-table augmentation benchmark.\n"
        "The GT was created for the current newData task. Old data must not be treated as label ground truth.\n"
        "Assess whether the GT schema and sampled row labels are semantically plausible for the query.\n"
        "Do not demand that the GT be the only possible schema; judge whether it is a valid, useful reference.\n\n"
        "Return strict JSON only with this schema:\n"
        "{\n"
        "  \"overall_semantic_ok\": true,\n"
        "  \"schema_relevance\": 0.0,\n"
        "  \"label_plausibility\": 0.0,\n"
        "  \"coverage_assessment\": \"complete|mostly_complete|partial|weak\",\n"
        "  \"critical_issues\": [\"...\"],\n"
        "  \"column_audits\": [\n"
        "    {\"column\": \"...\", \"semantic_fit\": \"high|medium|low\", \"value_domain_fit\": \"high|medium|low\", \"concerns\": [\"...\"], \"recommended_action\": \"keep|review|revise|drop\"}\n"
        "  ],\n"
        "  \"rationale\": \"short explanation\"\n"
        "}\n\n"
        f"Audit input JSON:\n{json.dumps(task, ensure_ascii=False, indent=2, default=str)}"
    )


def _write_gt_audit_md(audit: dict[str, Any], path: Path) -> None:
    deterministic = audit.get("deterministic") or {}
    llm = audit.get("llm_semantic_audit") or {}
    lines = [
        f"# GT Semantic Audit: {deterministic.get('query_id')}",
        "",
        f"- Dataset: `{deterministic.get('dataset')}`",
        f"- Query: {deterministic.get('query')}",
        f"- Expected-column recall: `{deterministic.get('gt_expected_column_recall')}`",
        f"- Expected-column precision: `{deterministic.get('gt_expected_column_precision')}`",
        f"- Domain-valid cell rate: `{deterministic.get('domain_valid_cell_rate')}`",
        f"- Row count match: `{deterministic.get('row_count_match')}`",
        f"- Critical issues: `{deterministic.get('critical_issues')}`",
        f"- Warnings: `{deterministic.get('warnings')}`",
        "",
    ]
    if llm and not llm.get("skipped"):
        lines.extend(
            [
                "## LLM Semantic Check",
                "",
                f"- Overall semantic OK: `{llm.get('overall_semantic_ok')}`",
                f"- Schema relevance: `{llm.get('schema_relevance')}`",
                f"- Label plausibility: `{llm.get('label_plausibility')}`",
                f"- Coverage assessment: `{llm.get('coverage_assessment')}`",
                f"- Critical issues: `{llm.get('critical_issues')}`",
                f"- Rationale: {llm.get('rationale')}",
                "",
            ]
        )
    lines.extend(["## Columns", "", "| Column | Present | Coverage | Domain valid | Issues |", "| --- | --- | ---: | ---: | --- |"])
    for item in deterministic.get("column_audits") or []:
        issues = []
        if item.get("out_of_domain_sample"):
            issues.append("out_of_domain")
        if item.get("scalar_violation_count"):
            issues.append("scalar_violation")
        lines.append(
            "| {col} | {present} | {coverage} | {domain} | {issues} |".format(
                col=item.get("column"),
                present=item.get("present"),
                coverage=item.get("coverage"),
                domain=item.get("domain_valid_rate"),
                issues=", ".join(issues),
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _run_gt_audit(package: semrec.ReferencePackage, outdir: Path, args: argparse.Namespace) -> dict[str, Any]:
    path = outdir / "GT_SEMANTIC_AUDIT.json"
    if path.exists() and not args.force_gt_audit:
        return _read_json(path)
    deterministic = _deterministic_gt_audit(package)
    audit: dict[str, Any] = {"created_at": _now(), "deterministic": deterministic, "llm_semantic_audit": {"skipped": True}}
    if not args.skip_gt_llm_audit:
        prompt = _gt_llm_prompt(package, deterministic, args.gt_sample_limit)
        (outdir / "GT_SEMANTIC_AUDIT_prompt.txt").write_text(prompt, encoding="utf-8")
        llm = semrec._invoke_judge(
            prompt,
            model=args.gt_judge_model,
            timeout_s=args.gt_judge_timeout,
            attempts=args.attempts,
            log_path=outdir / "GT_SEMANTIC_AUDIT_call.json",
        )
        audit["llm_semantic_audit"] = llm
    _write_json(path, audit)
    _write_gt_audit_md(audit, outdir / "GT_SEMANTIC_AUDIT.md")
    return audit


def _version_from_variant(variant: str) -> str:
    if variant == "skill_v7":
        return "v7"
    if variant == "skill_v8":
        return "v8"
    if variant == "skill_v9":
        return "v9"
    raise ValueError(f"unsupported candidate variant: {variant}")


def _candidate_run_name(args: argparse.Namespace, version: str) -> str:
    if version == "v7":
        return args.skill_v7_run_name
    if version == "v8":
        return args.skill_v8_run_name
    if version == "v9":
        return args.skill_v9_run_name
    raise ValueError(version)


def _variant_table(package: semrec.ReferencePackage, variant: str, args: argparse.Namespace) -> Path:
    if variant == ITEM_GT:
        return package.package_dir / "augmented.csv"
    version = _version_from_variant(variant)
    return package.package_dir / f"skill_{version}_runs" / _candidate_run_name(args, version) / f"augment.{args.output_format}"


def _variant_workdir(package: semrec.ReferencePackage, variant: str, args: argparse.Namespace) -> Path | None:
    if variant == ITEM_GT:
        return None
    version = _version_from_variant(variant)
    return package.package_dir / f"skill_{version}_runs" / _candidate_run_name(args, version)


def _load_direct_comparison(workdir: Path | None) -> dict[str, Any] | None:
    if workdir is None:
        return None
    path = workdir / "BT_COMPARISON.json"
    if not path.exists():
        return None
    try:
        payload = _read_json(path)
    except Exception:
        return {"status": "unreadable", "path": _rel(path)}
    summary = payload.get("summary") if isinstance(payload, dict) else None
    return summary if isinstance(summary, dict) else None


def _semantic_recall_for_variant(package: semrec.ReferencePackage, variant: str, args: argparse.Namespace) -> dict[str, Any] | None:
    if variant == ITEM_GT or args.skip_semantic_recall:
        return None
    version = _version_from_variant(variant)
    workdir = _variant_workdir(package, variant, args)
    assert workdir is not None
    table_path = _variant_table(package, variant, args)
    if not table_path.exists():
        return {"status": "missing_skill_output", "skill_output": _rel(table_path)}
    sem_args = SimpleNamespace(
        run_name=_candidate_run_name(args, version),
        output_format=args.output_format,
        force_judge=args.force_semantic_judge,
        no_llm_judge=args.no_llm_semantic_judge,
        judge_model=args.semantic_judge_model,
        judge_timeout=args.semantic_judge_timeout,
        attempts=args.attempts,
        match_threshold=args.match_threshold,
        sample_limit=args.semantic_sample_limit,
    )
    try:
        report = semrec._semantic_report(package, version, sem_args)
    except Exception as exc:
        if not args.continue_on_error:
            raise
        return {"status": "failed", "error": repr(exc), "skill_output": _rel(table_path)}
    return {"status": "ok", "summary": report.get("summary"), "path": _rel(workdir / "SEMANTIC_RECALL.json")}


def _variant_artifact(
    package: semrec.ReferencePackage,
    variant: str,
    source: pd.DataFrame,
    args: argparse.Namespace,
    semantic_recall: dict[str, Any] | None,
) -> VariantArtifact:
    table_path = _variant_table(package, variant, args)
    workdir = _variant_workdir(package, variant, args)
    if not table_path.exists():
        return VariantArtifact(variant, table_path, workdir, [], "missing", semantic_recall, _load_direct_comparison(workdir))
    frame = semrec._read_table(table_path).reset_index(drop=True)
    if variant == ITEM_GT:
        expected = [str(spec["name"]) for spec in semrec._expected_specs(package.package_dir) if spec.get("name")]
        new_cols = _source_new_columns(source, frame)
        augmented_columns = list(dict.fromkeys([*expected, *new_cols]))
        augmented_columns = [col for col in augmented_columns if col in frame.columns]
    else:
        augmented_columns = _source_new_columns(source, frame)
    return VariantArtifact(variant, table_path, workdir, augmented_columns, "ok", semantic_recall, _load_direct_comparison(workdir))


def _table_profile(
    package: semrec.ReferencePackage,
    variant: VariantArtifact,
    gt_audit: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    frame = semrec._read_table(variant.table_path).reset_index(drop=True)
    gt = _read_json(package.package_dir / "GT.json")
    query = gt.get("query") or {}
    focus = query.get("focus_variable") or package.query_record.get("focus_variable")
    expected_specs = semrec._expected_specs(package.package_dir)
    if variant.name == ITEM_GT:
        specs_by_name = _spec_by_name(expected_specs)
    else:
        specs_by_name = semrec._skill_specs(variant.workdir) if variant.workdir else {}
    column_profiles = [
        _column_profile(frame, col, specs_by_name.get(col))
        for col in variant.augmented_columns
        if col in frame.columns
    ]
    profile = {
        "profile_version": "lab8_newgt_lab6style_v1",
        "variant": variant.name,
        "table_path": _rel(variant.table_path),
        "query_id": package.query_id,
        "dataset": package.dataset_name,
        "query": package.query_text,
        "query_record": package.query_record,
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "source_table": _rel(package.source_table),
        "evidence_columns": package.evidence_cols,
        "focus_variable": focus,
        "focus_summary": _focus_summary(frame, focus),
        "augmented_columns": variant.augmented_columns,
        "augmented_column_profiles": column_profiles,
        "relationships_to_focus": _relationships_to_focus(frame, variant.augmented_columns, focus),
        "sample_rows": _sample_rows(frame, variant.augmented_columns, package.evidence_cols, focus, args.analysis_sample_limit),
    }
    return profile


def _analysis_prompt(profile: dict[str, Any]) -> str:
    return (
        "You are analyzing one augmented table for a Lab8 text-to-table benchmark query.\n"
        "Use only TABLE_PROFILE_JSON. Do not use external knowledge, do not invent row-level facts, "
        "and do not reward or punish a table merely because its variant name contains GT or skill.\n\n"
        "Evaluator metadata such as GT audit, semantic recall, and direct-reference scores is intentionally absent; "
        "base the analysis only on table evidence.\n\n"
        "Write concise Markdown that answers the query. Requirements:\n"
        "- Ground claims in concrete counts, shares, means, distributions, or visible column relationships from the profile.\n"
        "- Name augmented columns that materially support the analysis.\n"
        "- Combine augmented semantic facets with original structured columns where the profile supports it.\n"
        "- Identify useful segments, drivers, or causal/predictive signals matching the query family.\n"
        "- Include action-oriented recommendations or next diagnostics when the query asks why/how/what to improve.\n"
        "- Include limitations if focus variables, evidence columns, or row-level support are weak.\n\n"
        f"TABLE_PROFILE_JSON:\n{json.dumps(profile, ensure_ascii=False, indent=2, default=str)}\n"
    )


def _call_analysis_logged(
    prompt: str,
    *,
    outdir: Path,
    variant: str,
    claude_exe: str,
    model: str,
    fallback_model: str | None,
    timeout_s: int,
    attempts: int,
) -> str:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"{variant}_analysis_prompt.txt").write_text(prompt, encoding="utf-8")
    last_error = ""
    logs: list[dict[str, Any]] = []
    for attempt in range(1, max(1, attempts) + 1):
        attempt_prompt = prompt if attempt == 1 else prompt + "\n\nPrevious attempt failed or was empty. Return Markdown only."
        started = time.time()
        rc, stdout, stderr = _invoke_claude(claude_exe, attempt_prompt, timeout_s, model, fallback_model)
        text = _extract_text_from_claude_json(stdout).strip()
        log = {
            "attempt": attempt,
            "model": model,
            "fallback_model": fallback_model,
            "rc": rc,
            "wall_seconds": round(time.time() - started, 2),
            "stderr_head": stderr[:2000],
            "stdout_text_head": text[:4000],
            "raw_stdout_head": stdout[:2000],
        }
        logs.append(log)
        (outdir / f"{variant}_analysis_call.json").write_text(json.dumps(logs, ensure_ascii=False, indent=2), encoding="utf-8")
        if rc == 0 and text:
            return text
        last_error = stderr[-1200:] or stdout[-1200:] or f"rc={rc}"
        time.sleep(min(5, attempt))
    raise RuntimeError(f"analysis generation failed for {variant}: {last_error}")


def _load_or_generate_analysis(
    package: semrec.ReferencePackage,
    variant: VariantArtifact,
    gt_audit: dict[str, Any],
    outdir: Path,
    args: argparse.Namespace,
    claude_exe: str,
) -> str:
    analysis_dir = outdir / "analyses"
    report_path = analysis_dir / f"{variant.name}.md"
    profile_path = analysis_dir / f"{variant.name}_profile.json"
    if report_path.exists() and not args.regenerate_analysis:
        return report_path.read_text(encoding="utf-8", errors="replace")
    profile = _table_profile(package, variant, gt_audit, args)
    _write_json(profile_path, profile)
    report = _call_analysis_logged(
        _analysis_prompt(profile),
        outdir=analysis_dir,
        variant=variant.name,
        claude_exe=claude_exe,
        model=args.analysis_model,
        fallback_model=args.fallback_model or None,
        timeout_s=args.analysis_timeout,
        attempts=args.attempts,
    )
    report_path.write_text(report + ("\n" if not report.endswith("\n") else ""), encoding="utf-8")
    return report


def _mk_outcome(var_a: str, var_b: str, result: dict[str, Any], *, swap: bool) -> PKOutcome:
    return PKOutcome(
        var_a=var_a,
        var_b=var_b,
        raw_winner=str(result.get("winner", "TIE")).upper(),
        margin=str(result.get("margin", "small")).lower(),
        ok=bool(result.get("ok", False)),
        swap=swap,
        scores_a=result.get("scores_a"),
        scores_b=result.get("scores_b"),
        dimension_decisions=result.get("dimension_decisions") or {},
        evidence_refs=result.get("evidence_refs") or {"A": [], "B": []},
        augmented_column_refs=result.get("augmented_column_refs") or {"A": [], "B": []},
        confidence=result.get("confidence"),
        reason=result.get("reason"),
        validation_warnings=list(result.get("validation_warnings") or []),
    )


def _pairwise_path(outdir: Path, var_a: str, var_b: str, swap: bool) -> Path:
    return outdir / "pairwise" / f"{_safe_name(var_a)}__{_safe_name(var_b)}__swap{int(swap)}.json"


def _judge_or_load(
    outdir: Path,
    var_a: str,
    var_b: str,
    report_a: str,
    report_b: str,
    aug_cols_a: Sequence[str],
    aug_cols_b: Sequence[str],
    goal: str,
    swap: bool,
    args: argparse.Namespace,
    claude_exe: str,
) -> PKOutcome:
    path = _pairwise_path(outdir, var_a, var_b, swap)
    if path.exists() and not args.regenerate_judgments:
        return PKOutcome.from_dict(_read_json(path))
    result = judge_pairwise(
        claude_exe,
        goal,
        report_a,
        report_b,
        aug_cols_a=aug_cols_a,
        aug_cols_b=aug_cols_b,
        timeout_s=args.judge_timeout,
        model=args.judge_model,
        fallback_model=args.fallback_model or None,
        max_attempts=args.attempts,
    )
    outcome = _mk_outcome(var_a, var_b, result, swap=swap)
    record = outcome.to_dict(drop_empty=False)
    record["judge_model"] = args.judge_model
    record["judge_fallback_model"] = args.fallback_model or None
    _write_json(path, record)
    return outcome


def _run_analysis_bt(
    package: semrec.ReferencePackage,
    variants: list[VariantArtifact],
    gt_audit: dict[str, Any],
    outdir: Path,
    args: argparse.Namespace,
    claude_exe: str,
) -> dict[str, Any]:
    if args.skip_analysis_bt:
        return {"status": "skipped"}
    available = [variant for variant in variants if variant.status == "ok"]
    if len(available) < 2:
        return {"status": "insufficient_variants", "available": [variant.name for variant in available]}

    reports: dict[str, str] = {}
    for variant in available:
        reports[variant.name] = _load_or_generate_analysis(package, variant, gt_audit, outdir, args, claude_exe)
    by_name = {variant.name: variant for variant in available}
    goal = (
        f"Lab8 query: {package.query_text}\n"
        "Compare which augmented table enables a more specific, evidence-backed, actionable analysis. "
        "Do not use external ground truth; judge only the two reports and their cited evidence."
    )
    outcomes: list[PKOutcome] = []
    pairwise_jobs: list[tuple[str, str, bool]] = []
    for left, right in combinations([variant.name for variant in available], 2):
        pairwise_jobs.append((left, right, False))
        pairwise_jobs.append((right, left, True))

    def run_pairwise(job: tuple[str, str, bool]) -> PKOutcome:
        left, right, swap = job
        return _judge_or_load(
            outdir,
            left,
            right,
            reports[left],
            reports[right],
            by_name[left].augmented_columns,
            by_name[right].augmented_columns,
            goal,
            swap,
            args,
            claude_exe,
        )

    pairwise_workers = max(1, int(getattr(args, "pairwise_workers", 1)))
    if pairwise_workers == 1 or len(pairwise_jobs) <= 1:
        outcomes = [run_pairwise(job) for job in pairwise_jobs]
    else:
        with ThreadPoolExecutor(max_workers=min(pairwise_workers, len(pairwise_jobs))) as executor:
            future_to_index = {executor.submit(run_pairwise, job): index for index, job in enumerate(pairwise_jobs)}
            completed: dict[int, PKOutcome] = {}
            for future in as_completed(future_to_index):
                completed[future_to_index[future]] = future.result()
            outcomes = [completed[index] for index in sorted(completed)]
    items = [variant.name for variant in available]
    _write_json(outdir / "PAIRWISE_LAB6STYLE.json", [outcome.to_dict(drop_empty=False) for outcome in outcomes])
    bt = compute_bt_payload(package.query_id, outcomes, items=items)
    _write_json(outdir / "BT_LAB6STYLE.json", bt)
    return {"status": "ok", "items": items, "outcomes": [outcome.to_dict(drop_empty=False) for outcome in outcomes], "bt": bt}


def _write_package_md(report: dict[str, Any], path: Path) -> None:
    bt = (report.get("analysis_bt") or {}).get("bt") or {}
    scores = bt.get("bt_score") or {}
    gt_det = ((report.get("gt_audit") or {}).get("deterministic") or {})
    lines = [
        f"# Lab8 Lab6-Style Evaluation: {report.get('query_id')}",
        "",
        f"- Dataset: `{report.get('dataset')}`",
        f"- Query: {report.get('query')}",
        f"- Status: `{report.get('status')}`",
        f"- GT expected-column recall: `{gt_det.get('gt_expected_column_recall')}`",
        f"- GT domain-valid cell rate: `{gt_det.get('domain_valid_cell_rate')}`",
        f"- Available variants: `{', '.join((report.get('analysis_bt') or {}).get('items') or [])}`",
        f"- Analysis-BT winner: `{_winner_from_scores(scores, (report.get('analysis_bt') or {}).get('items') or []) if scores else 'unknown'}`",
        "",
        "## BT Scores",
        "",
    ]
    if scores:
        for item in _rank(scores, (report.get("analysis_bt") or {}).get("items") or list(scores)):
            lines.append(f"- `{item}`: `{scores.get(item)}`")
    else:
        lines.append("- No BT score available.")
    lines.extend(["", "## Semantic Recall", "", "| Variant | Status | Recall | Weighted | Cell semantic accuracy |", "| --- | --- | ---: | ---: | ---: |"])
    for variant in report.get("variants") or []:
        recall = variant.get("semantic_recall") or {}
        summary = recall.get("summary") or {}
        lines.append(
            "| {name} | {status} | {recall} | {weighted} | {cell} |".format(
                name=variant.get("name"),
                status=recall.get("status", "n/a"),
                recall=summary.get("semantic_expected_column_recall"),
                weighted=summary.get("semantic_expected_column_recall_weighted"),
                cell=summary.get("cell_semantic_accuracy_on_semantic_columns"),
            )
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _run_one(package: semrec.ReferencePackage, args: argparse.Namespace, claude_exe: str | None) -> dict[str, Any]:
    outdir = package.package_dir / "lab6style_eval" / args.run_name
    candidates = list(dict.fromkeys(args.candidate or DEFAULT_CANDIDATES))
    variant_names = [ITEM_GT, *candidates]

    if args.dry_run:
        variants = []
        for variant in variant_names:
            table = _variant_table(package, variant, args)
            variants.append({"name": variant, "table": _rel(table), "exists": table.exists()})
        return {
            "query_id": package.query_id,
            "dataset": package.dataset_name,
            "query": package.query_text,
            "status": "dry_run",
            "output_dir": _rel(outdir),
            "variants": variants,
        }

    outdir.mkdir(parents=True, exist_ok=True)
    source = semrec._read_table(package.source_table).reset_index(drop=True)
    gt_audit = _run_gt_audit(package, outdir, args)
    semantic_by_variant = {variant: _semantic_recall_for_variant(package, variant, args) for variant in candidates}
    variants = [_variant_artifact(package, ITEM_GT, source, args, None)]
    variants.extend(_variant_artifact(package, variant, source, args, semantic_by_variant.get(variant)) for variant in candidates)
    missing = [variant.name for variant in variants if variant.status != "ok"]
    analysis_bt = _run_analysis_bt(package, variants, gt_audit, outdir, args, claude_exe or find_claude())
    status = "ok" if analysis_bt.get("status") == "ok" else str(analysis_bt.get("status"))
    if missing and status == "ok":
        status = "partial_missing_variants"
    report = {
        "created_at": _now(),
        "query_id": package.query_id,
        "dataset": package.dataset_name,
        "query": package.query_text,
        "status": status,
        "output_dir": _rel(outdir),
        "package": _rel(package.package_dir),
        "gt_audit": gt_audit,
        "variants": [
            {
                "name": variant.name,
                "status": variant.status,
                "table": _rel(variant.table_path),
                "augmented_columns": variant.augmented_columns,
                "semantic_recall": variant.semantic_recall,
                "direct_comparison": variant.direct_comparison,
            }
            for variant in variants
        ],
        "missing_variants": missing,
        "analysis_bt": analysis_bt,
        "models": {
            "analysis_model": args.analysis_model,
            "judge_model": args.judge_model,
            "semantic_judge_model": None if args.no_llm_semantic_judge else args.semantic_judge_model,
            "gt_judge_model": None if args.skip_gt_llm_audit else args.gt_judge_model,
            "fallback_model": args.fallback_model or None,
        },
    }
    _write_json(outdir / "EVALUATION_LAB6STYLE.json", report)
    _write_package_md(report, outdir / "EVALUATION_LAB6STYLE.md")
    return report


def _aggregate_reports(reports: Sequence[dict[str, Any]], items: Sequence[str]) -> dict[str, Any]:
    stabilized: list[PKOutcome] = []
    raw: list[PKOutcome] = []
    for report in reports:
        bt = (report.get("analysis_bt") or {}).get("bt") or {}
        for item in bt.get("stabilized_outcomes") or []:
            stabilized.append(PKOutcome.from_dict(item))
        for item in bt.get("outcomes") or []:
            raw.append(PKOutcome.from_dict(item))
    if not stabilized:
        return {}
    present = {variant for outcome in stabilized for variant in (outcome.var_a, outcome.var_b)}
    active_items = [item for item in items if item in present]
    bt_score = bradley_terry_mm(stabilized, items=active_items)
    margin_bt = bradley_terry_mm(stabilized, items=active_items, use_margin_weight=True)
    raw_bt = bradley_terry_mm(raw, items=active_items)
    pair_counts: dict[str, dict[str, int]] = {}
    for outcome in stabilized:
        pair = "__vs__".join(sorted([outcome.var_a, outcome.var_b]))
        winner = outcome.winner_var() or "TIE"
        counts = pair_counts.setdefault(pair, {})
        counts[winner] = counts.get(winner, 0) + 1
    return {
        "dataset": "lab8_newData_lab6style",
        "aggregation_policy": "per_query_swap_stabilized_then_cross_query_bt",
        "requested_items": list(items),
        "items": active_items,
        "n_query_stabilized_outcomes": len(stabilized),
        "n_raw_ordered_outcomes": len(raw),
        "bt_score": bt_score,
        "bt_score_margin_weighted_secondary": margin_bt,
        "bt_score_raw_ordered": raw_bt,
        "primary_rank": _rank(bt_score, active_items),
        "secondary_rank": _rank(margin_bt, active_items),
        "winner": _winner_from_scores(bt_score, active_items),
        "pairwise_query_level_winner_counts": pair_counts,
        "dimension_summary": aggregate_dimension_scores(stabilized, items=active_items),
        "dimension_summary_raw_ordered": aggregate_dimension_scores(raw, items=active_items),
        "computed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }


def _mean(values: Iterable[Any]) -> float | None:
    numbers = [float(value) for value in values if value is not None]
    return round(statistics.mean(numbers), 4) if numbers else None


def _summary_payload(args: argparse.Namespace, reports: Sequence[dict[str, Any]]) -> dict[str, Any]:
    requested_items = [ITEM_GT, *list(dict.fromkeys(args.candidate or DEFAULT_CANDIDATES))]
    ok_reports = [report for report in reports if (report.get("analysis_bt") or {}).get("status") == "ok"]
    aggregate_bt = _aggregate_reports(ok_reports, requested_items)
    gt_audits = [(report.get("gt_audit") or {}).get("deterministic") or {} for report in reports]
    semantic_by_variant: dict[str, list[dict[str, Any]]] = {variant: [] for variant in requested_items if variant != ITEM_GT}
    for report in reports:
        for variant in report.get("variants") or []:
            name = variant.get("name")
            if name in semantic_by_variant:
                semantic_by_variant[name].append(((variant.get("semantic_recall") or {}).get("summary") or {}))
    return {
        "updated_at": _now(),
        "run_name": args.run_name,
        "requested_items": requested_items,
        "n_reports": len(reports),
        "n_analysis_bt_ok": len(ok_reports),
        "aggregate_bt": aggregate_bt,
        "gt_audit_summary": {
            "mean_gt_expected_column_recall": _mean(audit.get("gt_expected_column_recall") for audit in gt_audits),
            "mean_gt_expected_column_precision": _mean(audit.get("gt_expected_column_precision") for audit in gt_audits),
            "mean_domain_valid_cell_rate": _mean(audit.get("domain_valid_cell_rate") for audit in gt_audits),
            "critical_issue_queries": [audit.get("query_id") for audit in gt_audits if audit.get("critical_issues")],
        },
        "semantic_recall_summary": {
            variant: {
                "mean_semantic_column_recall": _mean(item.get("semantic_expected_column_recall") for item in summaries),
                "mean_weighted_semantic_recall": _mean(item.get("semantic_expected_column_recall_weighted") for item in summaries),
                "mean_cell_semantic_accuracy": _mean(item.get("cell_semantic_accuracy_on_semantic_columns") for item in summaries),
                "n_ok": sum(1 for item in summaries if item),
            }
            for variant, summaries in semantic_by_variant.items()
        },
        "reports": list(reports),
    }


def _write_summary_md(payload: dict[str, Any], path: Path) -> None:
    aggregate = payload.get("aggregate_bt") or {}
    scores = aggregate.get("bt_score") or {}
    lines = [
        "# Lab8 newData Lab6-Style Evaluation Summary",
        "",
        f"- Run: `{payload.get('run_name')}`",
        f"- Completed reports: `{payload.get('n_analysis_bt_ok')} / {payload.get('n_reports')}`",
        f"- Aggregate winner: `{aggregate.get('winner', 'unknown')}`",
        f"- Primary rank: `{aggregate.get('primary_rank')}`",
        "",
        "## Aggregate BT",
        "",
    ]
    if scores:
        for item in aggregate.get("primary_rank") or list(scores):
            lines.append(f"- `{item}`: `{scores.get(item)}`")
    else:
        lines.append("- No aggregate BT available.")
    gt = payload.get("gt_audit_summary") or {}
    lines.extend(
        [
            "",
            "## GT Audit",
            "",
            f"- Mean GT expected-column recall: `{gt.get('mean_gt_expected_column_recall')}`",
            f"- Mean GT expected-column precision: `{gt.get('mean_gt_expected_column_precision')}`",
            f"- Mean GT domain-valid cell rate: `{gt.get('mean_domain_valid_cell_rate')}`",
            f"- Critical-issue queries: `{gt.get('critical_issue_queries')}`",
            "",
            "## Candidate Semantic Recall",
            "",
            "| Variant | n ok | Mean recall | Mean weighted recall | Mean cell semantic accuracy |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for variant, summary in (payload.get("semantic_recall_summary") or {}).items():
        lines.append(
            "| {variant} | {n_ok} | {recall} | {weighted} | {cell} |".format(
                variant=variant,
                n_ok=summary.get("n_ok"),
                recall=summary.get("mean_semantic_column_recall"),
                weighted=summary.get("mean_weighted_semantic_recall"),
                cell=summary.get("mean_cell_semantic_accuracy"),
            )
        )
    per_query_variants = list((payload.get("semantic_recall_summary") or {}).keys())
    recall_headers = [f"{variant} recall" for variant in per_query_variants]
    lines.extend(["", "## Per Query", ""])
    lines.append("| Status | Query ID | Winner | GT recall | " + " | ".join(recall_headers) + " | Output |")
    lines.append("| --- | --- | --- | ---: | " + " | ".join("---:" for _ in recall_headers) + " | --- |")
    for report in payload.get("reports") or []:
        bt = (report.get("analysis_bt") or {}).get("bt") or {}
        winner = _winner_from_scores(bt.get("bt_score") or {}, (report.get("analysis_bt") or {}).get("items") or []) if bt else ""
        gt_det = ((report.get("gt_audit") or {}).get("deterministic") or {})
        recalls = {}
        for variant in report.get("variants") or []:
            summary = ((variant.get("semantic_recall") or {}).get("summary") or {})
            recalls[variant.get("name")] = summary.get("semantic_expected_column_recall")
        recall_cells = [str(recalls.get(variant)) for variant in per_query_variants]
        lines.append(
            "| {status} | {qid} | {winner} | {gt_recall} | {recalls} | `{outdir}` |".format(
                status=report.get("status"),
                qid=report.get("query_id"),
                winner=winner,
                gt_recall=gt_det.get("gt_expected_column_recall"),
                recalls=" | ".join(recall_cells),
                outdir=report.get("output_dir"),
            )
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_summary(args: argparse.Namespace, reports: Sequence[dict[str, Any]]) -> Path:
    payload = _summary_payload(args, reports)
    summary_base = SUMMARY_DIR / args.run_name
    json_path = summary_base.with_suffix(".json")
    md_path = summary_base.with_suffix(".md")
    _write_json(json_path, payload)
    _write_summary_md(payload, md_path)
    return json_path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query-id", action="append", default=None, help="Canonical query id. Repeatable.")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--candidate", action="append", choices=DEFAULT_CANDIDATES, default=None, help="Candidate variant to include. Defaults to skill_v7, skill_v8, and skill_v9.")
    parser.add_argument("--run-name", default=DEFAULT_RUN_NAME)
    parser.add_argument("--skill-v7-run-name", default=semrec.DEFAULT_RUN_NAMES["v7"])
    parser.add_argument("--skill-v8-run-name", default=semrec.DEFAULT_RUN_NAMES["v8"])
    parser.add_argument("--skill-v9-run-name", default=semrec.DEFAULT_RUN_NAMES["v9"])
    parser.add_argument("--output-format", choices=("csv", "xlsx", "parquet"), default="csv")
    parser.add_argument("--analysis-model", default="copilot/claude-opus-4.7-xhigh")
    parser.add_argument("--judge-model", default="copilot/claude-opus-4.7-xhigh")
    parser.add_argument("--semantic-judge-model", default="copilot/claude-opus-4.7-xhigh")
    parser.add_argument("--gt-judge-model", default="copilot/claude-opus-4.7-xhigh")
    parser.add_argument("--fallback-model", default="")
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument("--analysis-timeout", type=int, default=900)
    parser.add_argument("--judge-timeout", type=int, default=900)
    parser.add_argument("--semantic-judge-timeout", type=int, default=900)
    parser.add_argument("--gt-judge-timeout", type=int, default=900)
    parser.add_argument("--match-threshold", type=float, default=0.55)
    parser.add_argument("--semantic-sample-limit", type=int, default=8)
    parser.add_argument("--gt-sample-limit", type=int, default=8)
    parser.add_argument("--analysis-sample-limit", type=int, default=8)
    parser.add_argument("--force-gt-audit", action="store_true")
    parser.add_argument("--skip-gt-llm-audit", action="store_true")
    parser.add_argument("--skip-semantic-recall", action="store_true")
    parser.add_argument("--force-semantic-judge", action="store_true")
    parser.add_argument("--no-llm-semantic-judge", action="store_true")
    parser.add_argument("--skip-analysis-bt", action="store_true")
    parser.add_argument("--regenerate-analysis", action="store_true")
    parser.add_argument("--regenerate-judgments", action="store_true")
    parser.add_argument("--workers", type=int, default=1, help="Number of query packages to evaluate concurrently. Defaults to 1.")
    parser.add_argument("--pairwise-workers", type=int, default=1, help="Number of pairwise judge calls to run concurrently within each query. Defaults to 1.")
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Discover packages and variant tables without running LLM calls or writing package artifacts.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    packages = semrec._discover_reference_packages(args.query_id)
    if args.limit:
        packages = packages[: max(0, args.limit)]
    claude_exe = None if args.dry_run else find_claude()
    reports: list[dict[str, Any]] = []
    started = time.monotonic()

    def failure_report(package: semrec.ReferencePackage, exc: Exception) -> dict[str, Any]:
        return {
            "created_at": _now(),
            "query_id": package.query_id,
            "dataset": package.dataset_name,
            "query": package.query_text,
            "status": "failed",
            "error": repr(exc),
            "package": _rel(package.package_dir),
        }

    def run_indexed(index: int, package: semrec.ReferencePackage) -> dict[str, Any]:
        print(f"[lab6style] running {index}/{len(packages)} {package.query_id}", flush=True)
        return _run_one(package, args, claude_exe)

    workers = max(1, int(args.workers or 1))
    if workers == 1 or len(packages) <= 1:
        for index, package in enumerate(packages, start=1):
            try:
                report = run_indexed(index, package)
            except Exception as exc:
                report = failure_report(package, exc)
                print(f"[lab6style] failed {package.query_id}: {exc!r}", flush=True)
                if not args.continue_on_error:
                    raise
            reports.append(report)
            summary_path = _write_summary(args, reports)
            print(
                f"[lab6style] done {package.query_id}: status={report.get('status')} "
                f"elapsed={((time.monotonic() - started) / 60):.1f}m summary={_rel(summary_path)}",
                flush=True,
            )
    else:
        completed: dict[int, dict[str, Any]] = {}
        with ThreadPoolExecutor(max_workers=min(workers, len(packages))) as executor:
            future_to_item = {
                executor.submit(run_indexed, index, package): (index, package)
                for index, package in enumerate(packages, start=1)
            }
            for future in as_completed(future_to_item):
                index, package = future_to_item[future]
                try:
                    report = future.result()
                except Exception as exc:
                    report = failure_report(package, exc)
                    print(f"[lab6style] failed {package.query_id}: {exc!r}", flush=True)
                    if not args.continue_on_error:
                        raise
                completed[index] = report
                reports = [completed[item_index] for item_index in sorted(completed)]
                summary_path = _write_summary(args, reports)
                print(
                    f"[lab6style] done {package.query_id}: status={report.get('status')} "
                    f"elapsed={((time.monotonic() - started) / 60):.1f}m summary={_rel(summary_path)}",
                    flush=True,
                )
    summary_path = _write_summary(args, reports)
    print(f"[lab6style] summary={summary_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())