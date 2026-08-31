"""Drive the per-category *characteristic adherence* evaluation over the
4-way runs in ``dataset_portion_1`` and ``dataset_portion_2``.

This mirrors ``scorer/run_augmentation_recall.py`` but swaps the recall-based
grader for ``characteristic_adherence`` (advisor sync, 2026-06-25): instead of
asking "how many GT columns did we recover", it asks, per intent category,
whether the augmentation satisfies its characteristic --- e.g. for causal
scenarios, did we surface a treatment AND plausible confounders.

For each (portion, model, scenario) it evaluates three variants:

    skill_off     : <scenario>/augment_skill_off/augment.csv         (no specs.json)
    skill_on      : <scenario>/augment_skill_on/augment.csv          (+ specs.json)
    skill_on_e2e  : <scenario>/analyses/skill_on_e2e/tapp_workdir/augment.csv (+ specs.json)

Output::

    characteristic_result/<dataset>__<scenario>/<model>/<variant>_characteristic.json
    characteristic_result/SUMMARY.json     # per-category, per-variant aggregates
    characteristic_result/SUMMARY.md
"""
from __future__ import annotations

import argparse
import statistics as st
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent                      # .../4way_2model
SCORER_DIR = ROOT / "scorer"
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCORER_DIR))

import semantic_reference_recall as semrec     # noqa: E402
import characteristic_adherence as charadh      # noqa: E402

RESULT_DIR = ROOT / "characteristic_result"
GT_DIR = ROOT / "gt_annotations"
PORTIONS = ("dataset_portion_1", "dataset_portion_2")
MODELS = ("substrate-claude-haiku-4-5", "substrate-claude-sonnet-4-6")

# GT expected_structure -> FOI category. Used to assign ONE canonical category
# per scenario so all variants are judged under the same rubric (aligned n).
_STRUCT_TO_CAT = {
    "causal_graph": "causal_relation",
    "prediction_tree": "focus_relation",
    "flat_feature_set": "focus_relation",
    "concept_tree": "focus_internal_structure",
}


def _canonical_focus(scenario: str) -> str | None:
    """Scenario-level focus from the GT query, shared by all variants so the facet
    judge is given the same target concept regardless of variant specs."""
    dataset_key, _, sc = scenario.partition("__")
    for name in (dataset_key, dataset_key.replace("_", "-")):
        gt_path = GT_DIR / name / "augmentations" / sc / "GT.json"
        if gt_path.exists():
            query = (semrec._read_json(gt_path).get("query") or {})
            focus = query.get("focus_variable")
            return str(focus) if focus else None
    return None


def _canonical_category(scenario: str) -> str | None:
    """Scenario-level category from the GT package (expected_structure -> family),
    shared by all variants so skill_off/skill_on/skill_on_e2e are comparable."""
    dataset_key, _, sc = scenario.partition("__")
    for name in (dataset_key, dataset_key.replace("_", "-")):
        gt_path = GT_DIR / name / "augmentations" / sc / "GT.json"
        if gt_path.exists():
            query = (semrec._read_json(gt_path).get("query") or {})
            structure = str(query.get("expected_structure") or "").strip()
            if structure in _STRUCT_TO_CAT:
                return _STRUCT_TO_CAT[structure]
            family = str(query.get("family") or "").lower()
            if family == "causal":
                return "causal_relation"
            if family in {"concept", "concept_attribute", "faceted"}:
                return "focus_internal_structure"
            return "focus_relation"
    return None
# variant -> (augment.csv parts, specs dir parts | None)
# ``gt`` is a synthetic variant: it scores the ground-truth table itself, read from
# ``gt_annotations/``, as an upper-bound baseline. Any rubric the GT cannot pass is a
# broken rubric, not a failing system.
VARIANTS: dict[str, tuple[tuple[str, ...], tuple[str, ...] | None]] = {
    "skill_off": (("augment_skill_off", "augment.csv"), None),
    "skill_on": (("augment_skill_on", "augment.csv"), ("augment_skill_on",)),
    "skill_on_e2e": (
        ("analyses", "skill_on_e2e", "tapp_workdir", "augment.csv"),
        ("analyses", "skill_on_e2e", "tapp_workdir"),
    ),
    "gt": ((), None),
}


def _gt_package(scenario: str) -> tuple[Path | None, dict[str, Any]]:
    """Resolve the ground-truth table + plan for ``<dataset>__<scenario>``."""
    dataset_key, _, sc = scenario.partition("__")
    for name in (dataset_key, dataset_key.replace("_", "-")):
        base = GT_DIR / name / "augmentations" / sc
        gt_json = base / "GT.json"
        if not gt_json.exists():
            continue
        table = next(
            (base / n for n in ("augmented.csv", "augment_full.csv") if (base / n).exists()),
            None,
        )
        return table, semrec._read_json(gt_json)
    return None, {}


def _scenario_dirs(portion: str, model: str) -> list[Path]:
    base = ROOT / portion / model
    if not base.exists():
        return []
    return sorted(p for p in base.iterdir() if p.is_dir() and (p / "analyses").exists() or (p / "augment_skill_on").exists())


def _load_specs(scenario_dir: Path, specs_parts: tuple[str, ...] | None) -> dict[str, Any]:
    if not specs_parts:
        return {}
    path = scenario_dir.joinpath(*specs_parts, "specs.json")
    return semrec._read_json(path) if path.exists() else {}


def _query_and_source_columns(scenario_dir: Path) -> tuple[str, list[str]]:
    """Best-effort query text + original column names from summary_4way.json /
    materialized input. Source columns are only needed for skill_off (no specs)."""
    query, source_cols = "", []
    summary = scenario_dir.parent.parent / scenario_dir.name / "summary_4way.json"
    # summary_4way.json lives at <portion>/<scenario>/summary_4way.json in portion_1.
    portion_root = scenario_dir.parent.parent
    cand = portion_root / scenario_dir.name / "summary_4way.json"
    for path in (cand, scenario_dir / "summary_4way.json"):
        if path.exists():
            data = semrec._read_json(path)
            query = str(data.get("query") or "")
            src = data.get("source_data") or data.get("materialized_input")
            if src and Path(src).exists():
                try:
                    source_cols = [str(c) for c in semrec._read_table(Path(src)).columns]
                except Exception:
                    pass
            break
    return query, source_cols


def _eval_variant(
    *,
    scenario_dir: Path,
    scenario: str,
    variant: str,
    query: str,
    fallback_source_cols: list[str],
    out_dir: Path,
    args: argparse.Namespace,
) -> dict[str, Any]:
    table_parts, specs_parts = VARIANTS[variant]
    gt_doc: dict[str, Any] = {}
    if variant == "gt":
        gt_table, gt_doc = _gt_package(scenario)
        augment_path = gt_table if gt_table is not None else Path("/nonexistent")
    elif variant == "skill_off":
        table_parts = (getattr(args, "skill_off_subdir", "augment_skill_off"), "augment.csv")
    elif variant == "skill_on":
        sub = getattr(args, "skill_on_subdir", "augment_skill_on")
        parts = tuple(sub.split("/"))
        table_parts = (*parts, "augment.csv")
        specs_parts = parts
    elif variant == "skill_on_e2e":
        sub = getattr(args, "skill_on_e2e_subdir", "analyses/skill_on_e2e/tapp_workdir")
        parts = tuple(sub.split("/"))
        table_parts = (*parts, "augment.csv")
        specs_parts = parts
    if variant != "gt":
        augment_path = scenario_dir.joinpath(*table_parts)
    out_path = out_dir / f"{variant}_characteristic.json"
    # Resume: reuse an already-scored result unless forced.
    if out_path.exists() and not getattr(args, "force", False):
        try:
            prev = semrec._read_json(out_path)
            if prev.get("status") == "scored":
                return prev
        except Exception:
            pass
    if not augment_path.exists():
        return {"variant": variant, "status": "missing_output", "path": str(augment_path)}

    augment = semrec._read_table(augment_path).reset_index(drop=True)
    if variant == "gt":
        specs_payload = gt_doc.get("augmentation_plan") or {}
    else:
        specs_payload = _load_specs(scenario_dir, specs_parts)
    specs_by_name = {str(s.get("name")): s for s in (specs_payload.get("specs") or []) if s.get("name")}

    # Regenerated (query-only) skill_off tables record their exact added columns
    # in _schema.json; use it as the authoritative added-column list.
    schema_new_cols: list[str] | None = None
    if variant == "skill_off":
        schema_path = augment_path.parent / "_schema.json"
        if schema_path.exists():
            try:
                sch = semrec._read_json(schema_path)
                schema_new_cols = [str(c["name"]) for c in sch.get("columns", []) if c.get("name") and str(c["name"]) in augment.columns]
            except Exception:
                schema_new_cols = None

    # For skill_off (no specs.json) the original table is preserved as
    # augment_original_backup.csv once it has been directly augmented; use it to
    # isolate the ADDED columns instead of leaking the original schema.
    backup_path = augment_path.parent / "augment_original_backup.csv"
    backup_source_cols: list[str] = []
    if backup_path.exists():
        try:
            backup_source_cols = [str(c) for c in semrec._read_table(backup_path).columns]
        except Exception:
            backup_source_cols = []
    effective_fallback = backup_source_cols or fallback_source_cols

    if schema_new_cols:
        new_columns = schema_new_cols
        source_columns = [str(c) for c in augment.columns if str(c) not in set(schema_new_cols)]
    elif specs_by_name:
        new_columns = [c for c in specs_by_name if c in augment.columns]
        source_columns = [str(c) for c in augment.columns if c not in new_columns]
    elif effective_fallback:
        new_columns = [c for c in augment.columns if str(c) not in set(effective_fallback)]
        source_columns = effective_fallback
    else:
        # skill_off without a known source: treat every column as added (judge will
        # still find no treatment/confounder/facets -> low adherence, which is the point).
        new_columns = [str(c) for c in augment.columns]
        source_columns = []

    category = args.category or _canonical_category(scenario) or charadh.detect_category(scenario, specs_payload)
    focus = _canonical_focus(scenario) or charadh._focus_from_specs(specs_payload)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Optional: drop exact-synonym duplicate columns (e.g. FailureMode vs failure_mode)
    # before judging, and persist the deduped table as an artifact.
    dropped_dupes: list[str] = []
    if getattr(args, "dedup_exact", False):
        new_columns, dropped_dupes = charadh.dedup_exact([str(c) for c in new_columns])
        if dropped_dupes:
            keep_cols = [c for c in augment.columns if str(c) not in set(dropped_dupes)]
            try:
                augment[keep_cols].to_csv(out_dir / f"{variant}_augment_dedup.csv", index=False)
            except Exception:
                pass
    try:
        report = charadh.evaluate(
            augment_table=augment,
            new_columns=[str(c) for c in new_columns],
            specs_by_name=specs_by_name,
            category=category,
            query=query,
            focus=focus,
            source_columns=source_columns,
            judge_model=args.judge_model,
            judge_timeout=args.judge_timeout,
            attempts=args.attempts,
            log_path=out_dir / f"{variant}_judge_call.json",
            no_llm_judge=args.no_llm_judge,
        )
        report["variant"] = variant
        report["status"] = "scored"
        if dropped_dupes:
            report["dropped_duplicate_columns"] = dropped_dupes
    except Exception as exc:  # a refusal / parse / timeout must not kill the sweep
        report = {
            "variant": variant,
            "status": "judge_failed",
            "category": category,
            "error": str(exc)[:500],
            "n_added_columns": len(new_columns),
            "added_columns": [str(c) for c in new_columns],
        }
    semrec._write_json(out_path, report)
    return report


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """rows: list of {model, variant, category, metrics}. Aggregate per
    (category, variant)."""
    buckets: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("status") != "scored":
            continue
        buckets[(row["category"], row["variant"])].append(row["metrics"])

    def _mean(vals: list[float]) -> float | None:
        vals = [v for v in vals if v is not None]
        return round(st.mean(vals), 4) if vals else None

    summary: dict[str, dict[str, Any]] = {}
    for (category, variant), metrics in sorted(buckets.items()):
        n = len(metrics)
        agg: dict[str, Any] = {"n": n, "adherence": _mean([m.get("adherence") for m in metrics])}
        if category == "causal_relation":
            agg["treatment_present_rate"] = _mean([1.0 if m.get("treatment_present") else 0.0 for m in metrics])
            agg["confounder_present_rate"] = _mean([1.0 if m.get("confounder_present") else 0.0 for m in metrics])
            agg["mean_n_confounders"] = _mean([m.get("n_confounders") for m in metrics])
            agg["confounder_quality"] = _mean([m.get("confounder_quality") for m in metrics])
        elif category == "focus_relation":
            agg["predictor_fraction"] = _mean([m.get("predictor_fraction") for m in metrics])
        else:
            agg["facet_fraction"] = _mean([m.get("facet_fraction") for m in metrics])
            agg["coverage"] = _mean([m.get("coverage") for m in metrics])
            agg["redundancy"] = _mean([m.get("redundancy") for m in metrics])
        summary.setdefault(category, {})[variant] = agg
    return summary


def _write_summary_md(summary: dict[str, Any], path: Path) -> None:
    lines = ["# Characteristic Adherence Summary", ""]
    for category, variants in summary.items():
        lines.append(f"## {charadh.CATEGORY_LABEL.get(category, category)}")
        lines.append("")
        if category == "causal_relation":
            lines.append("| Variant | n | Adherence | Treatment-present | Confounder-present | Mean #conf | Conf. quality |")
            lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
            for variant in ("skill_off", "skill_on", "skill_on_e2e"):
                a = variants.get(variant)
                if not a:
                    continue
                lines.append(f"| {variant} | {a['n']} | {a['adherence']} | {a.get('treatment_present_rate')} | {a.get('confounder_present_rate')} | {a.get('mean_n_confounders')} | {a.get('confounder_quality')} |")
        elif category == "focus_relation":
            lines.append("| Variant | n | Adherence | Predictor fraction |")
            lines.append("| --- | ---: | ---: | ---: |")
            for variant in ("skill_off", "skill_on", "skill_on_e2e"):
                a = variants.get(variant)
                if not a:
                    continue
                lines.append(f"| {variant} | {a['n']} | {a['adherence']} | {a.get('predictor_fraction')} |")
        else:
            lines.append("| Variant | n | Adherence | Facet fraction | Coverage | Redundancy |")
            lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
            for variant in ("skill_off", "skill_on", "skill_on_e2e"):
                a = variants.get(variant)
                if not a:
                    continue
                lines.append(f"| {variant} | {a['n']} | {a['adherence']} | {a.get('facet_fraction')} | {a.get('coverage')} | {a.get('redundancy')} |")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Per-category characteristic adherence over 4-way runs.")
    parser.add_argument("--judge-model", default="claude-opus-4.8-xhigh")
    parser.add_argument("--out-dir", default="characteristic_result", help="Output folder (under 4way_2model) for per-dataset results and summary.")
    parser.add_argument("--skill-off-subdir", default="augment_skill_off", help="Subfolder under each scenario dir holding the skill_off augment.csv (use skill_off_regenerate for the mechanical query-only baseline).")
    parser.add_argument("--skill-on-subdir", default="augment_skill_on", help="Subfolder holding the skill_on augment.csv/specs.json (use augment_skill_on_v11 for the skill-v11 rerun).")
    parser.add_argument("--skill-on-e2e-subdir", default="analyses/skill_on_e2e/tapp_workdir", help="'/'-joined subfolder holding the skill_on_e2e augment.csv/specs.json (use analyses/skill_on_e2e_v11/tapp_workdir for the skill-v11 rerun).")
    parser.add_argument("--judge-timeout", type=int, default=240)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--variants", nargs="*", default=list(VARIANTS), choices=list(VARIANTS))
    parser.add_argument("--category", default=None, choices=list(charadh.CATEGORY_LABEL), help="Force a category (debug).")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--limit", type=int, default=0, help="Cap scenarios per model (debug).")
    parser.add_argument("--no-llm-judge", action="store_true")
    parser.add_argument("--force", action="store_true", help="Re-score even if a result file already exists.")
    parser.add_argument("--dedup-exact", action="store_true", help="Drop exact-synonym duplicate columns (e.g. FailureMode vs failure_mode) before judging.")
    parser.add_argument("--only-categories", nargs="*", default=None, choices=list(charadh.CATEGORY_LABEL), help="Only score scenarios whose canonical category is in this list.")
    args = parser.parse_args()

    global RESULT_DIR
    RESULT_DIR = (ROOT / args.out_dir) if not Path(args.out_dir).is_absolute() else Path(args.out_dir)

    tasks: list[tuple[str, str, str, Path]] = []  # (portion, model, scenario, scenario_dir)
    for portion in PORTIONS:
        for model in MODELS:
            dirs = _scenario_dirs(portion, model)
            if args.limit:
                dirs = dirs[: args.limit]
            for scenario_dir in dirs:
                if args.only_categories and (_canonical_category(scenario_dir.name) not in args.only_categories):
                    continue
                tasks.append((portion, model, scenario_dir.name, scenario_dir))

    rows: list[dict[str, Any]] = []

    def _run(task: tuple[str, str, str, Path]) -> list[dict[str, Any]]:
        portion, model, scenario, scenario_dir = task
        query, source_cols = _query_and_source_columns(scenario_dir)
        out_dir = RESULT_DIR / f"{portion}__{scenario}" / model
        out: list[dict[str, Any]] = []
        for variant in args.variants:
            rep = _eval_variant(
                scenario_dir=scenario_dir,
                scenario=scenario,
                variant=variant,
                query=query,
                fallback_source_cols=source_cols,
                out_dir=out_dir,
                args=args,
            )
            rep.update({"portion": portion, "model": model, "scenario": scenario})
            out.append(rep)
        return out

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = [pool.submit(_run, task) for task in tasks]
        for fut in as_completed(futures):
            rows.extend(fut.result())

    summary = _aggregate(rows)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    semrec._write_json(RESULT_DIR / "SUMMARY.json", {"updated_at": semrec._now(), "by_category": summary, "n_reports": len(rows)})
    _write_summary_md(summary, RESULT_DIR / "SUMMARY.md")
    print(f"Scored {len([r for r in rows if r.get('status') == 'scored'])} variant-runs; summary at {RESULT_DIR / 'SUMMARY.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
