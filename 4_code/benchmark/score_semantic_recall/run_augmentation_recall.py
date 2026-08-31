"""Score skill augmentation tables against clean_annotations GT.

For every dataset/scenario produced by each substrate model in
``dataset_portion_1`` and ``dataset_portion_2`` this driver runs
``semantic_reference_recall`` for the three augmentation variants:

    - skill_off      : <scenario>/augment_skill_off/augment.csv
    - skill_on       : <scenario>/augment_skill_on/augment.csv
    - skill_on_e2e   : <scenario>/analyses/skill_on_e2e/tapp_workdir/augment.csv

The reference (ground truth) for a scenario is the matching package under
``clean_annotations/<dataset>/augmentations/<scenario>/`` (GT augmented table +
specs taken from ``GT.json``).

Results are written to::

    augmentation_result/<dataset>__<scenario>/<model>/
        <variant>_semantic_recall.json
        <variant>_semantic_judge.json
        comparison.json
        comparison.md

This script does not modify ``semantic_reference_recall.py``; it reuses its
low-level helpers and only adapts path resolution and the package layout.
"""
from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent  # .../4way_2model
sys.path.insert(0, str(SCRIPT_DIR))

import semantic_reference_recall as semrec  # noqa: E402

CLEAN_DIR = ROOT / "gt_annotations"
RESULT_DIR = ROOT / "augmentation_result"
PORTIONS = ("dataset_portion_1", "dataset_portion_2")
MODELS = ("substrate-claude-haiku-4-5", "substrate-claude-sonnet-4-6")

# variant -> (table relative path parts, specs dir relative path parts | None)
VARIANTS: dict[str, tuple[tuple[str, ...], tuple[str, ...] | None]] = {
    "skill_off": (("augment_skill_off", "augment.csv"), None),
    "skill_on": (("augment_skill_on", "augment.csv"), ("augment_skill_on",)),
    "skill_on_e2e": (
        ("analyses", "skill_on_e2e", "tapp_workdir", "augment.csv"),
        ("analyses", "skill_on_e2e", "tapp_workdir"),
    ),
}


def _resolve_gt_package(dataset_key: str, scenario: str) -> Path | None:
    candidates = [dataset_key, dataset_key.replace("_", "-")]
    for name in candidates:
        package = CLEAN_DIR / name / "augmentations" / scenario
        if (package / "GT.json").exists():
            return package
    return None


def _load_gt(package_dir: Path) -> dict[str, Any]:
    gt = semrec._read_json(package_dir / "GT.json")
    plan = gt.get("augmentation_plan") or {}
    query = gt.get("query") or {}
    meta = gt.get("meta") or {}
    specs = [spec for spec in plan.get("specs") or [] if spec.get("name")]
    evidence_cols = list(
        plan.get("evidence_cols")
        or query.get("expected_evidence_columns")
        or []
    )
    original_cols = [
        str(col.get("name"))
        for col in (gt.get("original_schema") or {}).get("columns") or []
        if col.get("name")
    ]
    reference_table = package_dir / str(meta.get("augmented_table") or "augmented.csv")
    dataset_dir = package_dir.parent.parent
    source_table = dataset_dir / str(meta.get("original_table") or "")
    return {
        "query_id": str(query.get("id") or meta.get("query_id") or package_dir.name),
        "dataset_name": dataset_dir.name,
        "query_text": str(query.get("text") or "").strip(),
        "expected_structure": query.get("expected_structure"),
        "specs": specs,
        "evidence_cols": evidence_cols,
        "original_cols": original_cols,
        "reference_table": reference_table,
        "source_table": source_table,
        "dataset_dir": dataset_dir,
        "package_dir": package_dir,
        "query_record": query,
    }


def _reference_package(gt: dict[str, Any]) -> semrec.ReferencePackage:
    return semrec.ReferencePackage(
        query_id=gt["query_id"],
        dataset_name=gt["dataset_name"],
        dataset_dir=gt["dataset_dir"],
        package_dir=gt["package_dir"],
        source_table=gt["source_table"],
        query_text=gt["query_text"],
        expected_structure=gt["expected_structure"],
        evidence_cols=gt["evidence_cols"],
        query_record=gt["query_record"],
    )


def _summarize(
    *,
    gt: dict[str, Any],
    variant: str,
    skill_columns: list[str],
    columns: list[dict[str, Any]],
    judge: dict[str, Any],
    match_threshold: float,
) -> dict[str, Any]:
    expected_specs = gt["specs"]
    expected_count = len(expected_specs)
    accepted = [
        item
        for item in columns
        if item.get("skill_column")
        and item.get("semantic_match") in {"full", "partial"}
        and float(item.get("semantic_score") or 0.0) >= match_threshold
    ]
    full = [item for item in accepted if item.get("semantic_match") == "full"]
    compared = [item for item in accepted if item.get("status") == "compared"]
    total_cells = sum(int(item.get("row_count") or 0) for item in compared)
    total_semantic = sum(int(item.get("semantic_value_matches") or 0) for item in compared)
    total_canonical = sum(int(item.get("canonical_value_matches") or 0) for item in compared)
    weighted = (
        sum(min(1.0, max(0.0, float(item.get("semantic_score") or 0.0))) for item in accepted)
        / expected_count
        if expected_count
        else None
    )
    alternatives = [
        item
        for item in judge.get("useful_alternative_columns") or []
        if str(item.get("utility") or "").lower() in {"high", "medium"}
    ]
    return {
        "variant": variant,
        "query_id": gt["query_id"],
        "dataset": gt["dataset_name"],
        "query": gt["query_text"],
        "expected_column_count": expected_count,
        "skill_new_column_count": len(skill_columns),
        "skill_new_columns": skill_columns,
        "semantic_expected_column_count": len(accepted),
        "semantic_full_column_count": len(full),
        "semantic_missing_columns": [
            item["expected_column"] for item in columns if item not in accepted
        ],
        "semantic_expected_column_recall": round(len(accepted) / expected_count, 4)
        if expected_count
        else None,
        "semantic_full_column_recall": round(len(full) / expected_count, 4)
        if expected_count
        else None,
        "semantic_expected_column_recall_weighted": round(weighted, 4)
        if weighted is not None
        else None,
        "cell_semantic_accuracy_on_semantic_columns": round(total_semantic / total_cells, 4)
        if total_cells
        else None,
        "cell_canonical_accuracy_on_semantic_columns": round(total_canonical / total_cells, 4)
        if total_cells
        else None,
        "useful_alternative_column_count": len(alternatives),
        "useful_alternative_columns": alternatives,
        "match_threshold": match_threshold,
    }


def _score_variant(
    *,
    gt: dict[str, Any],
    package: semrec.ReferencePackage,
    source_df: pd.DataFrame,
    reference_df: pd.DataFrame,
    scenario_dir: Path,
    variant: str,
    out_dir: Path,
    args: argparse.Namespace,
) -> dict[str, Any]:
    table_parts, specs_parts = VARIANTS[variant]
    if variant == "skill_off":
        table_parts = (getattr(args, "skill_off_subdir", "augment_skill_off"), "augment.csv")
    elif variant == "skill_on":
        parts = tuple(getattr(args, "skill_on_subdir", "augment_skill_on").split("/"))
        table_parts = (*parts, "augment.csv")
        specs_parts = parts
    elif variant == "skill_on_e2e":
        parts = tuple(getattr(args, "skill_on_e2e_subdir", "analyses/skill_on_e2e/tapp_workdir").split("/"))
        table_parts = (*parts, "augment.csv")
        specs_parts = parts
    skill_table = scenario_dir.joinpath(*table_parts)
    if not skill_table.exists():
        return {"variant": variant, "status": "missing_skill_output", "skill_output": str(skill_table)}

    skill = semrec._read_table(skill_table).reset_index(drop=True)
    original_cols = set(gt["original_cols"]) or set(map(str, source_df.columns))
    skill_columns = [str(col) for col in skill.columns if str(col) not in original_cols]
    skill_specs = (
        semrec._skill_specs(scenario_dir.joinpath(*specs_parts)) if specs_parts else {}
    )
    expected_specs = gt["specs"]

    judge_path = out_dir / f"{variant}_semantic_judge.json"
    if judge_path.exists() and not args.force_judge:
        judge = semrec._read_json(judge_path)
    elif args.no_llm_judge:
        judge = semrec._fallback_column_matches(expected_specs, skill_columns, skill_specs)
        semrec._write_json(judge_path, judge)
    else:
        prompt = semrec._build_judge_prompt(
            package=package,
            source=source_df,
            reference=reference_df,
            skill=skill,
            expected_specs=expected_specs,
            skill_columns=skill_columns,
            skill_specs=skill_specs,
            version=variant,
        )
        (out_dir / f"{variant}_judge_prompt.txt").write_text(prompt, encoding="utf-8")
        judge = semrec._invoke_judge(
            prompt,
            model=args.judge_model,
            timeout_s=args.judge_timeout,
            attempts=args.attempts,
            log_path=out_dir / f"{variant}_semantic_judge_call.json",
        )
        semrec._write_json(judge_path, judge)

    chosen = semrec._dedupe_matches(judge, expected_specs)
    columns = []
    for spec in expected_specs:
        expected = str(spec["name"])
        item = chosen[expected]
        columns.append(
            semrec._compare_values(
                expected_col=expected,
                skill_col=item.get("skill_column"),
                match=item,
                source=source_df,
                reference=reference_df,
                skill=skill,
                evidence_cols=gt["evidence_cols"],
                sample_limit=args.sample_limit,
            )
        )

    summary = _summarize(
        gt=gt,
        variant=variant,
        skill_columns=skill_columns,
        columns=columns,
        judge=judge,
        match_threshold=args.match_threshold,
    )
    summary["status"] = "ok"
    summary["skill_output"] = str(skill_table)
    report = {"created_at": semrec._now(), "summary": summary, "columns": columns, "judge": judge}
    semrec._write_json(out_dir / f"{variant}_semantic_recall.json", report)
    return summary


def _write_comparison_md(scenario: str, model: str, gt: dict[str, Any], results: dict[str, Any], path: Path) -> None:
    lines = [
        f"# Semantic Recall Comparison: {scenario}",
        "",
        f"- Model: `{model}`",
        f"- Dataset: `{gt['dataset_name']}`",
        f"- Query: {gt['query_text']}",
        f"- GT expected columns: `{len(gt['specs'])}`",
        "",
        "| Variant | Status | Sem. recall | Full recall | Weighted | Cell sem. acc | Matched/Expected |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for variant in VARIANTS:
        res = results.get(variant) or {}
        status = res.get("status", "n/a")
        lines.append(
            "| {v} | {st} | {rec} | {full} | {wt} | {cell} | {m}/{e} |".format(
                v=variant,
                st=status,
                rec=res.get("semantic_expected_column_recall"),
                full=res.get("semantic_full_column_recall"),
                wt=res.get("semantic_expected_column_recall_weighted"),
                cell=res.get("cell_semantic_accuracy_on_semantic_columns"),
                m=res.get("semantic_expected_column_count", "-"),
                e=res.get("expected_column_count", len(gt["specs"])),
            )
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _score_scenario(model: str, scenario_dir: Path, args: argparse.Namespace) -> dict[str, Any]:
    scenario_folder = scenario_dir.name
    dataset_key, _, scenario = scenario_folder.partition("__")
    package_dir = _resolve_gt_package(dataset_key, scenario)
    out_dir = RESULT_DIR / scenario_folder / model
    if package_dir is None:
        out_dir.mkdir(parents=True, exist_ok=True)
        record = {"status": "missing_gt_package", "scenario": scenario_folder, "model": model}
        semrec._write_json(out_dir / "comparison.json", record)
        return record

    gt = _load_gt(package_dir)
    if not gt["specs"]:
        out_dir.mkdir(parents=True, exist_ok=True)
        record = {"status": "no_gt_specs", "scenario": scenario_folder, "model": model}
        semrec._write_json(out_dir / "comparison.json", record)
        return record

    out_dir.mkdir(parents=True, exist_ok=True)
    reference_df = semrec._read_table(gt["reference_table"]).reset_index(drop=True)
    if gt["source_table"].exists():
        source_df = semrec._read_table(gt["source_table"]).reset_index(drop=True)
    else:
        source_df = reference_df
    package = _reference_package(gt)

    results: dict[str, Any] = {}
    selected = set(args.variants) if getattr(args, "variants", None) else set(VARIANTS)
    for variant in VARIANTS:
        if variant not in selected:
            # Reuse an existing result (e.g. copied from a prior run) so the
            # comparison/summary still cover this variant without re-judging it.
            prev_path = out_dir / f"{variant}_semantic_recall.json"
            if prev_path.exists():
                try:
                    results[variant] = semrec._read_json(prev_path).get("summary") or {"variant": variant, "status": "reused_missing_summary"}
                except Exception:
                    results[variant] = {"variant": variant, "status": "reused_unreadable"}
            continue
        try:
            results[variant] = _score_variant(
                gt=gt,
                package=package,
                source_df=source_df,
                reference_df=reference_df,
                scenario_dir=scenario_dir,
                variant=variant,
                out_dir=out_dir,
                args=args,
            )
        except Exception as exc:  # noqa: BLE001
            if not args.continue_on_error:
                raise
            results[variant] = {"variant": variant, "status": "failed", "error": repr(exc)}

    comparison = {
        "created_at": semrec._now(),
        "scenario": scenario_folder,
        "model": model,
        "dataset": gt["dataset_name"],
        "query_id": gt["query_id"],
        "query": gt["query_text"],
        "gt_package": str(package_dir.relative_to(ROOT)),
        "expected_column_count": len(gt["specs"]),
        "variants": results,
        "status": "ok",
    }
    semrec._write_json(out_dir / "comparison.json", comparison)
    _write_comparison_md(scenario_folder, model, gt, results, out_dir / "comparison.md")
    return comparison


def _discover_jobs(args: argparse.Namespace) -> list[tuple[str, Path]]:
    jobs: list[tuple[str, Path]] = []
    only = set(args.scenario or [])
    for portion in PORTIONS:
        for model in MODELS:
            base = ROOT / portion / model
            if not base.is_dir():
                continue
            for scenario_dir in sorted(p for p in base.iterdir() if p.is_dir()):
                if only and scenario_dir.name not in only:
                    continue
                jobs.append((model, scenario_dir))
    if args.limit:
        jobs = jobs[: max(0, args.limit)]
    return jobs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", action="append", default=None, help="Scenario folder name to score. Repeatable.")
    parser.add_argument("--out-dir", default="augmentation_result", help="Output folder (under 4way_2model) for results.")
    parser.add_argument("--skill-off-subdir", default="augment_skill_off", help="Subfolder holding the skill_off augment.csv.")
    parser.add_argument("--skill-on-subdir", default="augment_skill_on", help="Subfolder holding the skill_on augment.csv/specs.json (use augment_skill_on_v11 for the skill-v11 rerun).")
    parser.add_argument("--skill-on-e2e-subdir", default="analyses/skill_on_e2e/tapp_workdir", help="'/'-joined subfolder holding the skill_on_e2e augment.csv/specs.json (use analyses/skill_on_e2e_v11/tapp_workdir for the skill-v11 rerun).")
    parser.add_argument("--variants", nargs="*", default=None, help="Subset of variants to score (skill_off skill_on skill_on_e2e).")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--judge-model", default="claude-opus-4.8-xhigh")
    parser.add_argument("--judge-timeout", type=int, default=900)
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument("--match-threshold", type=float, default=0.55)
    parser.add_argument("--sample-limit", type=int, default=8)
    parser.add_argument("--force-judge", action="store_true", help="Re-run LLM judge even if cached.")
    parser.add_argument("--no-llm-judge", action="store_true", help="Use deterministic string fallback only.")
    parser.add_argument("--continue-on-error", action="store_true", default=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    global RESULT_DIR
    RESULT_DIR = (ROOT / args.out_dir) if not Path(args.out_dir).is_absolute() else Path(args.out_dir)
    jobs = _discover_jobs(args)
    print(f"[recall] discovered {len(jobs)} scenario jobs | out={RESULT_DIR.name}", flush=True)
    if args.dry_run:
        for model, scenario_dir in jobs:
            dataset_key, _, scenario = scenario_dir.name.partition("__")
            package = _resolve_gt_package(dataset_key, scenario)
            print(f"  {model} :: {scenario_dir.name} -> {'OK' if package else 'MISSING GT'}", flush=True)
        return 0

    workers = max(1, args.workers)
    done = 0
    total = len(jobs)
    if workers == 1:
        for model, scenario_dir in jobs:
            res = _score_scenario(model, scenario_dir, args)
            done += 1
            print(f"[recall] ({done}/{total}) {model} :: {scenario_dir.name} -> {res.get('status')}", flush=True)
    else:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_map = {
                executor.submit(_score_scenario, model, scenario_dir, args): (model, scenario_dir)
                for model, scenario_dir in jobs
            }
            for future in as_completed(future_map):
                model, scenario_dir = future_map[future]
                done += 1
                try:
                    res = future.result()
                    status = res.get("status")
                except Exception as exc:  # noqa: BLE001
                    status = f"error:{exc!r}"
                print(f"[recall] ({done}/{total}) {model} :: {scenario_dir.name} -> {status}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
