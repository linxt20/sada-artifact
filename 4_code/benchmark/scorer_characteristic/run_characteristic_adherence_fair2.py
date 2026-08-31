"""Drive the *fair2* focus-internal-structure evaluation.

Only scenarios whose GT canonical category is ``focus_internal_structure`` are
scored (the causal / correlational categories are unchanged from
``characteristic_evaluation_fair`` and are not touched here).

Per (portion, scenario) we infer the concept-to-decompose ONCE from the GT query
(variant-blind, model-blind, frozen) and cache it at
``<out>/<portion>__<scenario>/_concept.json``. Every model x variant is then
judged against that same concept (faceted) or, when the query names no focus,
against the focus-inference rubric.

Output (default ``characteristic_evaluation_fair2``)::

    <out>/<portion>__<scenario>/_concept.json
    <out>/<portion>__<scenario>/<model>/<variant>_characteristic.json
    <out>/SUMMARY.json
    <out>/SUMMARY.md
"""
from __future__ import annotations

import argparse
import statistics as st
import sys
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
SCORER_DIR = ROOT / "scorer"
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCORER_DIR))

import semantic_reference_recall as semrec          # noqa: E402
import characteristic_adherence as charadh           # noqa: E402
import characteristic_adherence_fair2 as fair2        # noqa: E402
import run_characteristic_adherence as rundrv         # noqa: E402

GT_DIR = ROOT / "gt_annotations"
PORTIONS = rundrv.PORTIONS
MODELS = rundrv.MODELS
VARIANTS = rundrv.VARIANTS


def _gt_query_obj(scenario: str) -> dict[str, Any]:
    dataset_key, _, sc = scenario.partition("__")
    for name in (dataset_key, dataset_key.replace("_", "-")):
        gt_path = GT_DIR / name / "augmentations" / sc / "GT.json"
        if gt_path.exists():
            return semrec._read_json(gt_path).get("query") or {}
    return {}


def _canonical_query_text(scenario: str) -> str:
    q = _gt_query_obj(scenario)
    return str(q.get("text") or "")


def _canonical_subtype(scenario: str) -> str:
    return str(_gt_query_obj(scenario).get("subtype") or "").lower()


def _gt_reference_facets(scenario: str) -> list[dict[str, Any]]:
    """Ground-truth reference facets for a scenario, from GT.json
    ``augmentation_plan.specs`` (annotator-authored answer key: name +
    description + value domain). Used to GT-ground the faceted judge.

    Only specs that were actually MATERIALISED into the GT table are used: the
    planner stage can propose columns that merge later drops, and counting those
    in the coverage denominator would systematically under-score every variant.
    """
    dataset_key, _, sc = scenario.partition("__")
    for name in (dataset_key, dataset_key.replace("_", "-")):
        base = GT_DIR / name / "augmentations" / sc
        gt_path = base / "GT.json"
        if not gt_path.exists():
            continue
        data = semrec._read_json(gt_path)
        specs = ((data.get("augmentation_plan") or {}).get("specs")) or []
        materialised: set[str] | None = None
        declared = (data.get("augmented_schema") or {}).get("new_columns")
        if declared:
            materialised = {str(c) for c in declared}
        else:
            table = next((base / n for n in ("augmented.csv", "augment_full.csv") if (base / n).exists()), None)
            if table is not None:
                try:
                    materialised = {str(c) for c in semrec._read_table(table).columns}
                except Exception:
                    materialised = None
        facets: list[dict[str, Any]] = []
        for s in specs:
            if not isinstance(s, dict) or not s.get("name"):
                continue
            if materialised is not None and str(s["name"]) not in materialised:
                continue
            facets.append({
                "name": str(s.get("name")),
                "description": str(s.get("description") or s.get("zh_description") or "")[:400],
            })
        return facets
    return []



def _domain_hint(scenario: str) -> str:
    dataset_key, _, _ = scenario.partition("__")
    return dataset_key.replace("_", " ")


def _added_columns(augment, scenario_dir: Path, table_parts, specs_by_name, fallback_source_cols):
    backup_path = scenario_dir.joinpath(*table_parts).parent / "augment_original_backup.csv"
    backup_cols: list[str] = []
    if backup_path.exists():
        try:
            backup_cols = [str(c) for c in semrec._read_table(backup_path).columns]
        except Exception:
            backup_cols = []
    effective_fallback = backup_cols or fallback_source_cols
    if specs_by_name:
        return [c for c in specs_by_name if c in augment.columns]
    if effective_fallback:
        return [c for c in augment.columns if str(c) not in set(effective_fallback)]
    return [str(c) for c in augment.columns]


def main() -> int:
    parser = argparse.ArgumentParser(description="Fair2 focus-internal-structure evaluation.")
    parser.add_argument("--judge-model", default="claude-opus-4.8-xhigh")
    parser.add_argument("--out-dir", default="characteristic_evaluation_fair2")
    parser.add_argument("--skill-off-subdir", default="augment_skill_off", help="Subfolder under each scenario dir holding the skill_off augment.csv (use skill_off_regenerate for the mechanical query-only baseline).")
    parser.add_argument("--skill-on-subdir", default="augment_skill_on", help="Subfolder holding the skill_on augment.csv/specs.json (use augment_skill_on_v11 for the skill-v11 rerun).")
    parser.add_argument("--skill-on-e2e-subdir", default="analyses/skill_on_e2e/tapp_workdir", help="'/'-joined subfolder holding the skill_on_e2e augment.csv/specs.json (use analyses/skill_on_e2e_v11/tapp_workdir for the skill-v11 rerun).")
    parser.add_argument("--judge-timeout", type=int, default=240)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--variants", nargs="*", default=list(VARIANTS), choices=list(VARIANTS))
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--no-llm-judge", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dedup-exact", action="store_true", help="Drop exact-synonym duplicate columns before judging.")
    args = parser.parse_args()

    out_root = (ROOT / args.out_dir) if not Path(args.out_dir).is_absolute() else Path(args.out_dir)

    # Collect (portion, scenario) that are focus_internal_structure, with the
    # per-model scenario dirs that actually exist.
    scenarios: dict[tuple[str, str], dict[str, Path]] = {}
    for portion in PORTIONS:
        for model in MODELS:
            for scenario_dir in rundrv._scenario_dirs(portion, model):
                scenario = scenario_dir.name
                if rundrv._canonical_category(scenario) != "focus_internal_structure":
                    continue
                scenarios.setdefault((portion, scenario), {})[model] = scenario_dir

    keys = sorted(scenarios)
    if args.limit:
        keys = keys[: args.limit]

    concept_locks: dict[tuple[str, str], threading.Lock] = {k: threading.Lock() for k in keys}
    rows: list[dict[str, Any]] = []

    def _concept_for(portion: str, scenario: str) -> dict[str, Any]:
        cache = out_root / f"{portion}__{scenario}" / "_concept.json"
        with concept_locks[(portion, scenario)]:
            if cache.exists() and not args.force:
                try:
                    return semrec._read_json(cache)
                except Exception:
                    pass
            query = _canonical_query_text(scenario)
            subtype = _canonical_subtype(scenario)
            cache.parent.mkdir(parents=True, exist_ok=True)
            if args.no_llm_judge:
                info = {"is_focus_named": subtype != "focus_inference", "concept_to_decompose": None, "expected_facets": [], "rationale": "no-llm"}
            elif subtype == "focus_inference":
                # GT already declares this as focus inference: no concept to fix.
                info = {"is_focus_named": False, "concept_to_decompose": None, "expected_facets": [], "rationale": "GT subtype=focus_inference"}
            else:
                info = fair2.infer_concept(
                    query=query,
                    domain_hint=_domain_hint(scenario),
                    judge_model=args.judge_model,
                    judge_timeout=args.judge_timeout,
                    attempts=args.attempts,
                    log_path=cache.parent / "_concept_call.json",
                )
            info["query"] = query
            info["gt_subtype"] = subtype
            semrec._write_json(cache, info)
            return info

    def _run(key: tuple[str, str]) -> list[dict[str, Any]]:
        portion, scenario = key
        concept_info = _concept_for(portion, scenario)
        gt_facets = _gt_reference_facets(scenario)
        out: list[dict[str, Any]] = []
        for model, scenario_dir in scenarios[key].items():
            query, source_cols = rundrv._query_and_source_columns(scenario_dir)
            if not query:
                query = concept_info.get("query") or ""
            out_dir = out_root / f"{portion}__{scenario}" / model
            out_dir.mkdir(parents=True, exist_ok=True)
            for variant in args.variants:
                table_parts, specs_parts = VARIANTS[variant]
                if variant == "skill_off":
                    table_parts = (args.skill_off_subdir, "augment.csv")
                elif variant == "skill_on":
                    parts = tuple(args.skill_on_subdir.split("/"))
                    table_parts = (*parts, "augment.csv")
                    specs_parts = parts
                elif variant == "skill_on_e2e":
                    parts = tuple(args.skill_on_e2e_subdir.split("/"))
                    table_parts = (*parts, "augment.csv")
                    specs_parts = parts
                gt_doc: dict[str, Any] = {}
                if variant == "gt":
                    gt_table, gt_doc = rundrv._gt_package(scenario)
                    augment_path = gt_table if gt_table is not None else Path("/nonexistent")
                else:
                    augment_path = scenario_dir.joinpath(*table_parts)
                out_path = out_dir / f"{variant}_characteristic.json"
                if out_path.exists() and not args.force:
                    try:
                        prev = semrec._read_json(out_path)
                        if prev.get("status") == "scored":
                            prev.update({"portion": portion, "model": model, "scenario": scenario})
                            out.append(prev)
                            continue
                    except Exception:
                        pass
                if not augment_path.exists():
                    rep = {"variant": variant, "status": "missing_output", "path": str(augment_path)}
                    rep.update({"portion": portion, "model": model, "scenario": scenario})
                    out.append(rep)
                    continue
                augment = semrec._read_table(augment_path).reset_index(drop=True)
                if variant == "gt":
                    specs_payload = gt_doc.get("augmentation_plan") or {}
                    specs_by_name = {str(s.get("name")): s for s in (specs_payload.get("specs") or []) if s.get("name")}
                    new_columns = [c for c in specs_by_name if c in augment.columns]
                else:
                    specs_payload = rundrv._load_specs(scenario_dir, specs_parts)
                    specs_by_name = {str(s.get("name")): s for s in (specs_payload.get("specs") or []) if s.get("name")}
                    new_columns = _added_columns(augment, scenario_dir, table_parts, specs_by_name, source_cols)
                # Regenerated (query-only) skill_off tables list their exact added
                # columns in _schema.json; prefer it as the authoritative list.
                if variant == "skill_off":
                    schema_path = augment_path.parent / "_schema.json"
                    if schema_path.exists():
                        try:
                            sch = semrec._read_json(schema_path)
                            sc_cols = [str(c["name"]) for c in sch.get("columns", []) if c.get("name") and str(c["name"]) in augment.columns]
                            if sc_cols:
                                new_columns = sc_cols
                        except Exception:
                            pass
                dropped_dupes: list[str] = []
                if args.dedup_exact:
                    new_columns, dropped_dupes = charadh.dedup_exact([str(c) for c in new_columns])
                    if dropped_dupes:
                        keep_cols = [c for c in augment.columns if str(c) not in set(dropped_dupes)]
                        try:
                            augment[keep_cols].to_csv(out_dir / f"{variant}_augment_dedup.csv", index=False)
                        except Exception:
                            pass
                try:
                    rep = fair2.evaluate(
                        augment_table=augment,
                        new_columns=[str(c) for c in new_columns],
                        specs_by_name=specs_by_name,
                        query=query,
                        concept_info=concept_info,
                        judge_model=args.judge_model,
                        judge_timeout=args.judge_timeout,
                        attempts=args.attempts,
                        log_path=out_dir / f"{variant}_judge_call.json",
                        no_llm_judge=args.no_llm_judge,
                        gt_facets=gt_facets,
                    )
                    rep["variant"] = variant
                    rep["status"] = "scored"
                    if dropped_dupes:
                        rep["dropped_duplicate_columns"] = dropped_dupes
                except Exception as exc:
                    rep = {
                        "variant": variant,
                        "status": "judge_failed",
                        "error": str(exc)[:500],
                        "n_added_columns": len(new_columns),
                        "added_columns": [str(c) for c in new_columns],
                    }
                semrec._write_json(out_path, rep)
                rep.update({"portion": portion, "model": model, "scenario": scenario})
                out.append(rep)
        return out

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = [pool.submit(_run, key) for key in keys]
        for fut in as_completed(futures):
            rows.extend(fut.result())

    summary = _aggregate(rows)
    out_root.mkdir(parents=True, exist_ok=True)
    semrec._write_json(out_root / "SUMMARY.json", {"updated_at": semrec._now(), "by_category_model": summary, "n_reports": len(rows)})
    _write_summary_md(summary, out_root / "SUMMARY.md")
    scored = len([r for r in rows if r.get("status") == "scored"])
    print(f"Scored {scored} variant-runs; summary at {out_root / 'SUMMARY.md'}")
    return 0


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate per (category, model, variant)."""
    buckets: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("status") != "scored":
            continue
        buckets[(row["category"], row["model"], row["variant"])].append(row["metrics"])

    def _mean(vals):
        vals = [v for v in vals if v is not None]
        return round(st.mean(vals), 4) if vals else None

    summary: dict[str, dict[str, dict[str, Any]]] = {}
    for (category, model, variant), metrics in sorted(buckets.items()):
        agg: dict[str, Any] = {"n": len(metrics), "adherence": _mean([m.get("adherence") for m in metrics])}
        if category == fair2.FACET_CATEGORY:
            agg["facet_fraction"] = _mean([m.get("facet_fraction") for m in metrics])
            agg["coverage"] = _mean([m.get("coverage") for m in metrics])
            agg["redundancy"] = _mean([m.get("redundancy") for m in metrics])
        else:
            agg["focus_coherence"] = _mean([m.get("focus_coherence") for m in metrics])
            agg["structure_quality"] = _mean([m.get("structure_quality") for m in metrics])
            agg["redundancy"] = _mean([m.get("redundancy") for m in metrics])
        summary.setdefault(category, {}).setdefault(model, {})[variant] = agg
    return summary


def _write_summary_md(summary: dict[str, Any], path: Path) -> None:
    lines = ["# Characteristic Adherence (fair2) Summary", ""]
    for category, by_model in summary.items():
        lines.append(f"## {fair2.CATEGORY_LABEL.get(category, category)}")
        lines.append("")
        if category == fair2.FACET_CATEGORY:
            header = "| Model | Variant | n | Adherence | Facet fraction | Coverage | Redundancy |"
            sep = "| --- | --- | ---: | ---: | ---: | ---: | ---: |"
        else:
            header = "| Model | Variant | n | Adherence | Focus coherence | Structure quality | Redundancy |"
            sep = "| --- | --- | ---: | ---: | ---: | ---: | ---: |"
        lines.append(header)
        lines.append(sep)
        for model in MODELS:
            for variant in ("skill_off", "skill_on", "skill_on_e2e"):
                a = (by_model.get(model) or {}).get(variant)
                if not a:
                    continue
                if category == fair2.FACET_CATEGORY:
                    lines.append(f"| {model} | {variant} | {a['n']} | {a['adherence']} | {a.get('facet_fraction')} | {a.get('coverage')} | {a.get('redundancy')} |")
                else:
                    lines.append(f"| {model} | {variant} | {a['n']} | {a['adherence']} | {a.get('focus_coherence')} | {a.get('structure_quality')} | {a.get('redundancy')} |")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
