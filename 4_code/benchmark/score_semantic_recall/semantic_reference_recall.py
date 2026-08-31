"""Compute semantic GT recall for Lab8 skill outputs.

This evaluator deliberately lives outside the skills. It does not change what a
skill may generate; it only judges whether generated augmentation columns
semantically cover the GT columns and whether generated values can be mapped to
GT value domains.
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
from typing import Any, Iterable

import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
LAB8_DIR = SCRIPT_DIR.parent
REPO_ROOT = LAB8_DIR.parent
NEWDATA_DIR = LAB8_DIR / "benchmark_data" / "newData"
DATASETS_DIR = NEWDATA_DIR / "datasets"
QUERIES_FILE = NEWDATA_DIR / "queries_v7.json"

DEFAULT_RUN_NAMES = {
    "v7": "opus47_direct_newgt_20260601",
    "v8": "opus47_direct_newgt_v8_20260601",
    "v9": "opus47_direct_newgt_v9_20260602",
}

NULL_STRINGS = {"", "none", "null", "nan", "na", "n/a", "not mentioned", "not_mentioned", "unknown"}


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
    raise ValueError(f"Unsupported table format: {path}")


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
    payload = _read_json(package_dir / "specs.json")
    return [spec for spec in payload.get("specs") or [] if spec.get("name")]


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


def _extract_vocab(description: str) -> list[str]:
    match = re.search(r"\{([^}]+)\}", description or "")
    if not match:
        return []
    return [token.strip() for token in match.group(1).split(",") if token.strip()]


def _domain_from_spec(spec: dict[str, Any]) -> list[str]:
    if isinstance(spec.get("domain"), list):
        return [str(value) for value in spec["domain"]]
    output_schema = spec.get("output_schema")
    if isinstance(output_schema, dict) and isinstance(output_schema.get("value_space"), list):
        return [str(value) for value in output_schema["value_space"]]
    description = str(spec.get("description") or spec.get("Description") or "")
    return _extract_vocab(description)


def _description_from_spec(spec: dict[str, Any]) -> str:
    return str(spec.get("description") or spec.get("Description") or spec.get("zh_description") or "")[:900]


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
    if isinstance(value, int):
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


def _semantic_key(value: Any) -> str | None:
    normalized = _normalize_value(value)
    if normalized is None:
        return None
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", str(normalized)).lower()
    text = re.sub(r"[^0-9a-z]+", "_", text).strip("_")
    return text or None


def _value_counts(values: Iterable[Any], limit: int = 20) -> dict[str, int]:
    counts: dict[str, int] = {}
    for raw in values:
        value = _normalize_value(raw)
        key = "<NULL>" if value is None else value
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit])


def _find_claude() -> str:
    exe = shutil.which("claude")
    if not exe:
        candidate = os.path.expandvars(r"%APPDATA%\npm\claude.CMD")
        if Path(candidate).exists():
            exe = candidate
    if not exe:
        raise RuntimeError("claude CLI not found")
    path = Path(exe)
    if os.name == "nt" and path.suffix.lower() in {".cmd", ".bat"}:
        native = path.parent / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe"
        if native.exists():
            return str(native)
    return exe


def _extract_json_object(text: str) -> dict[str, Any]:
    try:
        payload = json.loads(text)
        if isinstance(payload, dict):
            return payload
    except Exception:
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"Judge did not return JSON object: {text[:500]}")
    payload = json.loads(match.group(0))
    if not isinstance(payload, dict):
        raise ValueError("Judge JSON root is not an object")
    return payload


def _invoke_judge(prompt: str, *, model: str, timeout_s: int, attempts: int, log_path: Path) -> dict[str, Any]:
    cmd = [
        _find_claude(),
        "-p",
        "--bare",
        "--no-session-persistence",
        "--permission-mode",
        "bypassPermissions",
        "--output-format",
        "json",
        "--model",
        model,
    ]
    env = os.environ.copy()
    env["CLAUDE_CODE_SIMPLE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    last_error = ""
    for attempt in range(1, max(1, attempts) + 1):
        started = time.time()
        try:
            proc = subprocess.run(
                cmd,
                input=prompt,
                cwd=REPO_ROOT,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_s,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            last_error = f"timeout after {timeout_s}s"
            log_path.write_text(json.dumps({"attempt": attempt, "error": last_error}, indent=2), encoding="utf-8")
            continue

        stdout_raw = proc.stdout or ""
        stderr_text = proc.stderr or ""
        result_text = stdout_raw
        is_error = False
        try:
            outer = json.loads(stdout_raw)
            if isinstance(outer, dict):
                is_error = bool(outer.get("is_error"))
                result_text = str(outer.get("result") or outer.get("response") or "")
        except Exception:
            pass
        log_payload = {
            "attempt": attempt,
            "model": model,
            "returncode": proc.returncode,
            "is_error": is_error,
            "wall_seconds": round(time.time() - started, 2),
            "stderr_text": stderr_text[:4000],
            "stdout_text": result_text[:20000],
            "raw_stdout_head": stdout_raw[:4000],
        }
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(json.dumps(log_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        if proc.returncode == 0 and not is_error and result_text.strip():
            try:
                return _extract_json_object(result_text)
            except Exception as exc:
                last_error = str(exc)
        else:
            last_error = stderr_text or result_text[:1000]
        time.sleep(min(8, 2 * attempt))
    raise RuntimeError(f"semantic judge failed: {last_error}")


def _column_payload(
    *,
    name: str,
    spec: dict[str, Any],
    values: pd.Series | None,
    role: str,
) -> dict[str, Any]:
    domain = _domain_from_spec(spec)
    return {
        "name": name,
        "role": role,
        "description": _description_from_spec(spec),
        "domain": domain[:40],
        "observed_top_values": _value_counts([] if values is None else values.tolist(), limit=30),
    }


def _build_judge_prompt(
    *,
    package: ReferencePackage,
    source: pd.DataFrame,
    reference: pd.DataFrame,
    skill: pd.DataFrame,
    expected_specs: list[dict[str, Any]],
    skill_columns: list[str],
    skill_specs: dict[str, dict[str, Any]],
    version: str,
) -> str:
    expected_payload = []
    for spec in expected_specs:
        name = str(spec["name"])
        expected_payload.append(_column_payload(name=name, spec=spec, values=reference[name] if name in reference.columns else None, role="gt_expected"))
    skill_payload = []
    for name in skill_columns:
        skill_payload.append(_column_payload(name=name, spec=skill_specs.get(name, {}), values=skill[name] if name in skill.columns else None, role="skill_generated"))
    source_columns = [str(col) for col in source.columns]
    task = {
        "version": version,
        "query_id": package.query_id,
        "dataset": package.dataset_name,
        "query": package.query_text,
        "query_record": package.query_record,
        "source_columns": source_columns,
        "evidence_columns": package.evidence_cols,
        "expected_columns": expected_payload,
        "skill_columns": skill_payload,
    }
    return (
        "You are a fair semantic evaluator for a text-to-table augmentation benchmark.\n"
        "The skill is allowed to freely generate useful augmentation columns. The GT schema is one valid reference schema, not text that the skill saw.\n"
        "Your job is to judge whether each GT expected column is semantically covered by one generated skill column.\n\n"
        "Important rules:\n"
        "- Do not require exact column names, capitalization, casing, snake_case, or identical vocabulary.\n"
        "- Count a generated column as a match when it captures the same analytic slot, a clear synonym, or a useful parent/child version of the GT concept.\n"
        "- Do not count broad parent categories as full row-value matches when one skill value could map to several GT values.\n"
        "- A generated column may match at most one GT column. Prefer the most specific useful mapping.\n"
        "- Value aliases should map a skill value to a GT value only when the mapping is reliable globally. Case-only and naming-style differences should be mapped.\n"
        "- Also identify useful generated columns that do not match GT but are legitimate alternative schema choices for the query.\n\n"
        "Return strict JSON only, with this schema:\n"
        "{\n"
        "  \"column_matches\": [\n"
        "    {\"expected_column\": \"...\", \"skill_column\": \"... or null\", \"semantic_match\": \"full|partial|none\", \"score\": 0.0, \"relation\": \"same|synonym|parent_child|overlap|different|missing\", \"rationale\": \"...\", \"value_aliases\": [{\"skill_value\": \"...\", \"reference_value\": \"... or null\", \"confidence\": 0.0}]}\n"
        "  ],\n"
        "  \"useful_alternative_columns\": [\n"
        "    {\"skill_column\": \"...\", \"utility\": \"high|medium|low\", \"rationale\": \"...\"}\n"
        "  ]\n"
        "}\n\n"
        f"Evaluation input JSON:\n{json.dumps(task, ensure_ascii=False, indent=2)}"
    )


def _fallback_column_matches(expected_specs: list[dict[str, Any]], skill_columns: list[str], skill_specs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    remaining = set(skill_columns)
    matches: list[dict[str, Any]] = []
    for spec in expected_specs:
        expected = str(spec["name"])
        expected_key = _semantic_key(expected) or expected.lower()
        best: tuple[float, str] | None = None
        for candidate in sorted(remaining):
            score = SequenceMatcher(None, expected_key, _semantic_key(candidate) or candidate.lower()).ratio()
            if best is None or score > best[0]:
                best = (score, candidate)
        if best and best[0] >= 0.62:
            remaining.remove(best[1])
            matches.append(
                {
                    "expected_column": expected,
                    "skill_column": best[1],
                    "semantic_match": "partial" if best[0] < 0.9 else "full",
                    "score": round(best[0], 4),
                    "relation": "same" if best[0] >= 0.9 else "overlap",
                    "rationale": "fallback string similarity",
                    "value_aliases": [],
                }
            )
        else:
            matches.append(
                {
                    "expected_column": expected,
                    "skill_column": None,
                    "semantic_match": "none",
                    "score": 0.0,
                    "relation": "missing",
                    "rationale": "no fallback match",
                    "value_aliases": [],
                }
            )
    return {"column_matches": matches, "useful_alternative_columns": []}


def _dedupe_matches(judge: dict[str, Any], expected_specs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    expected_names = [str(spec["name"]) for spec in expected_specs]
    raw_by_expected: dict[str, dict[str, Any]] = {}
    for item in judge.get("column_matches") or []:
        expected = str(item.get("expected_column") or "")
        if expected in expected_names:
            raw_by_expected[expected] = item

    chosen: dict[str, dict[str, Any]] = {}
    used_skill: set[str] = set()
    for expected in expected_names:
        item = raw_by_expected.get(expected) or {"expected_column": expected, "skill_column": None, "semantic_match": "none", "score": 0.0, "relation": "missing", "rationale": "judge did not return this expected column", "value_aliases": []}
        skill_col = item.get("skill_column")
        if skill_col:
            skill_col = str(skill_col)
            if skill_col in used_skill:
                item = {**item, "skill_column": None, "semantic_match": "none", "score": 0.0, "relation": "duplicate_rejected", "rationale": "skill column already matched another GT column", "value_aliases": []}
            else:
                used_skill.add(skill_col)
        chosen[expected] = item
    return chosen


def _alias_map(match: dict[str, Any]) -> dict[str, str | None]:
    aliases: dict[str, str | None] = {}
    for item in match.get("value_aliases") or []:
        skill_value = _semantic_key(item.get("skill_value"))
        if skill_value is None:
            continue
        ref_value = item.get("reference_value")
        aliases[skill_value] = _semantic_key(ref_value) if ref_value is not None else None
    return aliases


def _compare_values(
    *,
    expected_col: str,
    skill_col: str | None,
    match: dict[str, Any],
    source: pd.DataFrame,
    reference: pd.DataFrame,
    skill: pd.DataFrame,
    evidence_cols: list[str],
    sample_limit: int,
) -> dict[str, Any]:
    base = {
        "expected_column": expected_col,
        "skill_column": skill_col,
        "semantic_match": match.get("semantic_match", "none"),
        "semantic_score": float(match.get("score") or 0.0),
        "semantic_relation": match.get("relation"),
        "semantic_rationale": match.get("rationale"),
        "value_aliases": match.get("value_aliases") or [],
    }
    if not skill_col or skill_col not in skill.columns or expected_col not in reference.columns:
        return {**base, "status": "missing", "semantic_value_accuracy": None, "canonical_value_accuracy": None, "mismatches_sample": []}

    aliases = _alias_map(match)
    ref_values = [_normalize_value(value) for value in reference[expected_col].tolist()]
    skill_values = [_normalize_value(value) for value in skill[skill_col].tolist()]
    canonical_matches = 0
    semantic_matches = 0
    mismatches: list[dict[str, Any]] = []
    for row_index, (ref_raw, got_raw) in enumerate(zip(ref_values, skill_values, strict=False)):
        ref_key = _semantic_key(ref_raw)
        got_key = _semantic_key(got_raw)
        canonical_ok = ref_key == got_key
        mapped_got = aliases.get(got_key, got_key)
        semantic_ok = canonical_ok or (ref_key is not None and mapped_got == ref_key)
        canonical_matches += 1 if canonical_ok else 0
        semantic_matches += 1 if semantic_ok else 0
        if not semantic_ok and len(mismatches) < sample_limit:
            mismatches.append(
                {
                    "row_index": row_index,
                    "reference": ref_raw,
                    "skill": got_raw,
                    "canonical_reference": ref_key,
                    "canonical_skill": got_key,
                    "alias_mapped_skill": mapped_got,
                    "evidence_excerpt": _evidence_excerpt(source, row_index, evidence_cols),
                }
            )
    row_count = len(reference)
    return {
        **base,
        "status": "compared",
        "row_count": row_count,
        "canonical_value_matches": canonical_matches,
        "semantic_value_matches": semantic_matches,
        "canonical_value_accuracy": round(canonical_matches / row_count, 4) if row_count else None,
        "semantic_value_accuracy": round(semantic_matches / row_count, 4) if row_count else None,
        "reference_distribution_top": _value_counts(ref_values),
        "skill_distribution_top": _value_counts(skill_values),
        "mismatches_sample": mismatches,
    }


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
    joined = " | ".join(parts)
    return joined[: limit - 3] + "..." if len(joined) > limit else joined


def _run_dir(package: ReferencePackage, version: str, run_name: str) -> Path:
    return package.package_dir / f"skill_{version}_runs" / run_name


def _semantic_report(package: ReferencePackage, version: str, args: argparse.Namespace) -> dict[str, Any]:
    run_name = args.run_name or DEFAULT_RUN_NAMES[version]
    workdir = _run_dir(package, version, run_name)
    output_path = workdir / f"augment.{args.output_format}"
    if not output_path.exists():
        raise FileNotFoundError(f"Missing skill output for {package.query_id}: {output_path}")
    source = _read_table(package.source_table).reset_index(drop=True)
    reference = _read_table(package.package_dir / "augmented.csv").reset_index(drop=True)
    skill = _read_table(output_path).reset_index(drop=True)
    expected_specs = _expected_specs(package.package_dir)
    skill_columns = _source_new_columns(source, skill)
    skill_specs = _skill_specs(workdir)
    semantic_path = workdir / "SEMANTIC_RECALL.json"
    judge_path = workdir / "semantic_judge.json"
    if judge_path.exists() and not args.force_judge:
        judge = _read_json(judge_path)
    elif args.no_llm_judge:
        judge = _fallback_column_matches(expected_specs, skill_columns, skill_specs)
        _write_json(judge_path, judge)
    else:
        prompt = _build_judge_prompt(
            package=package,
            source=source,
            reference=reference,
            skill=skill,
            expected_specs=expected_specs,
            skill_columns=skill_columns,
            skill_specs=skill_specs,
            version=version,
        )
        judge = _invoke_judge(prompt, model=args.judge_model, timeout_s=args.judge_timeout, attempts=args.attempts, log_path=workdir / "semantic_judge_call.json")
        _write_json(judge_path, judge)

    chosen = _dedupe_matches(judge, expected_specs)
    columns = []
    for spec in expected_specs:
        expected = str(spec["name"])
        item = chosen[expected]
        columns.append(
            _compare_values(
                expected_col=expected,
                skill_col=item.get("skill_column"),
                match=item,
                source=source,
                reference=reference,
                skill=skill,
                evidence_cols=package.evidence_cols,
                sample_limit=args.sample_limit,
            )
        )
    accepted = [item for item in columns if item.get("skill_column") and item.get("semantic_match") in {"full", "partial"} and float(item.get("semantic_score") or 0.0) >= args.match_threshold]
    full = [item for item in accepted if item.get("semantic_match") == "full"]
    expected_count = len(expected_specs)
    compared = [item for item in accepted if item.get("status") == "compared"]
    total_cells = sum(int(item.get("row_count") or 0) for item in compared)
    total_semantic_matches = sum(int(item.get("semantic_value_matches") or 0) for item in compared)
    total_canonical_matches = sum(int(item.get("canonical_value_matches") or 0) for item in compared)
    weighted_recall = sum(min(1.0, max(0.0, float(item.get("semantic_score") or 0.0))) for item in accepted) / expected_count if expected_count else None
    alternatives = [item for item in judge.get("useful_alternative_columns") or [] if str(item.get("utility") or "").lower() in {"high", "medium"}]
    summary = {
        "query_id": package.query_id,
        "dataset": package.dataset_name,
        "query": package.query_text,
        "version": version,
        "run_name": run_name,
        "reference_package": str(package.package_dir.relative_to(REPO_ROOT)),
        "skill_output": str(output_path.relative_to(REPO_ROOT)),
        "expected_column_count": expected_count,
        "skill_new_column_count": len(skill_columns),
        "skill_new_columns": skill_columns,
        "semantic_expected_column_count": len(accepted),
        "semantic_full_column_count": len(full),
        "semantic_missing_columns": [item["expected_column"] for item in columns if item not in accepted],
        "semantic_expected_column_recall": round(len(accepted) / expected_count, 4) if expected_count else None,
        "semantic_full_column_recall": round(len(full) / expected_count, 4) if expected_count else None,
        "semantic_expected_column_recall_weighted": round(weighted_recall, 4) if weighted_recall is not None else None,
        "cell_semantic_accuracy_on_semantic_columns": round(total_semantic_matches / total_cells, 4) if total_cells else None,
        "cell_canonical_accuracy_on_semantic_columns": round(total_canonical_matches / total_cells, 4) if total_cells else None,
        "useful_alternative_column_count": len(alternatives),
        "useful_alternative_columns": alternatives,
        "judge_model": None if args.no_llm_judge else args.judge_model,
        "match_threshold": args.match_threshold,
        "interpretation": "Semantic recall accepts close column semantics and reliable value aliases without changing the skill output or exposing GT schema to the skill.",
    }
    report = {"created_at": _now(), "summary": summary, "columns": columns, "judge": judge}
    _write_json(semantic_path, report)
    _write_semantic_markdown(report, workdir / "SEMANTIC_RECALL.md")
    return report


def _write_semantic_markdown(report: dict[str, Any], path: Path) -> None:
    summary = report["summary"]
    lines = [
        f"# Skill-{summary['version']} Semantic Reference Recall",
        "",
        f"- Query ID: `{summary['query_id']}`",
        f"- Query: {summary['query']}",
        f"- Semantic column recall: {summary['semantic_expected_column_recall']}",
        f"- Semantic full-column recall: {summary['semantic_full_column_recall']}",
        f"- Weighted semantic recall: {summary['semantic_expected_column_recall_weighted']}",
        f"- Cell semantic accuracy: {summary['cell_semantic_accuracy_on_semantic_columns']}",
        f"- Useful alternative columns: {summary['useful_alternative_column_count']}",
        "",
        "| GT column | Skill column | Match | Score | Relation | Semantic value acc | Rationale |",
        "| --- | --- | --- | ---: | --- | ---: | --- |",
    ]
    for item in report["columns"]:
        rationale = str(item.get("semantic_rationale") or "").replace("|", "\\|")[:220]
        lines.append(
            "| {expected} | {skill} | {match} | {score} | {relation} | {acc} | {rationale} |".format(
                expected=item.get("expected_column"),
                skill=item.get("skill_column") or "<missing>",
                match=item.get("semantic_match"),
                score=item.get("semantic_score"),
                relation=item.get("semantic_relation"),
                acc=item.get("semantic_value_accuracy"),
                rationale=rationale,
            )
        )
    if summary.get("useful_alternative_columns"):
        lines.extend(["", "## Useful Alternative Columns", ""])
        for item in summary["useful_alternative_columns"]:
            lines.append(f"- `{item.get('skill_column')}` ({item.get('utility')}): {item.get('rationale')}")
    path.write_text("\n".join(lines), encoding="utf-8")


def _update_summary(version: str, reports: list[dict[str, Any]]) -> None:
    summary_json = NEWDATA_DIR / f"skill_{version}_semantic_reference_recall_summary.json"
    summary_md = NEWDATA_DIR / f"skill_{version}_semantic_reference_recall_summary.md"
    existing: list[dict[str, Any]] = []
    if summary_json.exists():
        existing = list((_read_json(summary_json).get("reports") or []))
    by_key = {item["summary"]["query_id"]: item for item in existing if item.get("summary")}
    for report in reports:
        by_key[report["summary"]["query_id"]] = report
    merged = list(sorted(by_key.values(), key=lambda item: item["summary"]["query_id"]))
    _write_json(summary_json, {"updated_at": _now(), "reports": merged})

    lines = [
        f"# Skill-{version} Semantic Reference Recall Summary",
        "",
        "| Dataset | Query ID | Expected | Semantic matched | Full matched | Semantic recall | Weighted recall | Cell semantic acc | Useful alternatives |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for report in merged:
        s = report["summary"]
        lines.append(
            "| {dataset} | {qid} | {expected} | {matched} | {full} | {recall} | {weighted} | {cell} | {alts} |".format(
                dataset=s["dataset"],
                qid=s["query_id"],
                expected=s["expected_column_count"],
                matched=s["semantic_expected_column_count"],
                full=s["semantic_full_column_count"],
                recall=s["semantic_expected_column_recall"],
                weighted=s["semantic_expected_column_recall_weighted"],
                cell=s["cell_semantic_accuracy_on_semantic_columns"],
                alts=s["useful_alternative_column_count"],
            )
        )
    lines.append("")
    summary_md.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", choices=("v7", "v8"), required=True)
    parser.add_argument("--query-id", action="append", default=None, help="Reference query id to evaluate. Repeatable.")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--run-name", default=None, help="Run folder name. Defaults to current Lab8 direct run for the version.")
    parser.add_argument("--output-format", choices=("csv", "xlsx", "parquet"), default="csv")
    parser.add_argument("--judge-model", default="copilot/claude-opus-4.7-xhigh")
    parser.add_argument("--judge-timeout", type=int, default=900)
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument("--match-threshold", type=float, default=0.55)
    parser.add_argument("--sample-limit", type=int, default=8)
    parser.add_argument("--force-judge", action="store_true", help="Re-run LLM judge even if semantic_judge.json exists.")
    parser.add_argument("--no-llm-judge", action="store_true", help="Use deterministic name fallback only.")
    parser.add_argument("--continue-on-error", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packages = _discover_reference_packages(args.query_id)
    if args.limit:
        packages = packages[: max(0, args.limit)]
    reports: list[dict[str, Any]] = []
    for package in packages:
        try:
            print(f"[semantic-{args.version}] judging {package.query_id}", flush=True)
            report = _semantic_report(package, args.version, args)
            reports.append(report)
            s = report["summary"]
            print(
                f"[semantic-{args.version}] done {package.query_id}: recall={s['semantic_expected_column_recall']} weighted={s['semantic_expected_column_recall_weighted']} cell={s['cell_semantic_accuracy_on_semantic_columns']}",
                flush=True,
            )
        except Exception as exc:
            if not args.continue_on_error:
                raise
            print(f"[semantic-{args.version}] failed {package.query_id}: {exc}", flush=True)
    if reports:
        _update_summary(args.version, reports)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())