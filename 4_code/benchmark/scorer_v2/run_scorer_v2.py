"""Drive the scorer_v2 sweep: B-1 (general quality) + B-2 (per-subtype adherence).

Runs over ``dataset_portion_1``/``dataset_portion_2`` x {haiku, sonnet} x
{skill_off, skill_on, skill_on_e2e}. Both scorers see exactly the same added-column
set for a given (scenario, model, variant), so B-1 and B-2 are directly comparable.

The intent subtype is resolved ONCE per scenario from the GT annotation and shared
by every model/variant, so all systems are graded under the same rubric.

Output (default ``characteristic_evaluation_v2``)::

    <out>/<portion>__<scenario>/<model>/<variant>_b1.json
    <out>/<portion>__<scenario>/<model>/<variant>_b2.json
    <out>/SUMMARY.json
    <out>/SUMMARY.md
"""
from __future__ import annotations

import argparse
import statistics as st
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
SCORER_DIR = ROOT / "scorer"
CHAR_DIR = ROOT / "scorer_characteristic"
for _p in (str(SCRIPT_DIR), str(SCORER_DIR), str(CHAR_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import semantic_reference_recall as semrec        # noqa: E402
import characteristic_adherence as charadh         # noqa: E402
import run_characteristic_adherence as rundrv      # noqa: E402
import b1_general_quality as b1                    # noqa: E402
import b2_characteristic_adherence as b2           # noqa: E402

GT_DIR = ROOT / "gt_annotations"
PORTIONS = rundrv.PORTIONS
MODELS = rundrv.MODELS
VARIANTS = rundrv.VARIANTS
VARIANT_ORDER = ("skill_off", "skill_on", "skill_on_e2e")


def _gt_query(scenario: str) -> dict[str, Any]:
    dataset_key, _, sc = scenario.partition("__")
    for name in (dataset_key, dataset_key.replace("_", "-")):
        gt_path = GT_DIR / name / "augmentations" / sc / "GT.json"
        if gt_path.exists():
            return semrec._read_json(gt_path).get("query") or {}
    return {}


def _variant_paths(args: argparse.Namespace, variant: str) -> tuple[tuple[str, ...], tuple[str, ...] | None]:
    """(table parts, specs dir parts) honouring the --*-subdir overrides."""
    if variant == "skill_off":
        parts = tuple(args.skill_off_subdir.split("/"))
        return (*parts, "augment.csv"), None
    sub = args.skill_on_subdir if variant == "skill_on" else args.skill_on_e2e_subdir
    parts = tuple(sub.split("/"))
    return (*parts, "augment.csv"), parts


def _resolve_columns(augment, augment_path: Path, variant: str, specs_by_name, fallback_source_cols):
    """Added columns + original columns, using the same precedence as v1:
    _schema.json (regenerated skill_off) > specs.json > backup source table > fallback."""
    if variant == "skill_off":
        schema_path = augment_path.parent / "_schema.json"
        if schema_path.exists():
            try:
                sch = semrec._read_json(schema_path)
                cols = [str(c["name"]) for c in sch.get("columns", [])
                        if c.get("name") and str(c["name"]) in augment.columns]
                if cols:
                    return cols, [str(c) for c in augment.columns if str(c) not in set(cols)]
            except Exception:
                pass

    if specs_by_name:
        new_cols = [c for c in specs_by_name if c in augment.columns]
        return new_cols, [str(c) for c in augment.columns if c not in new_cols]

    backup_path = augment_path.parent / "augment_original_backup.csv"
    backup_cols: list[str] = []
    if backup_path.exists():
        try:
            backup_cols = [str(c) for c in semrec._read_table(backup_path).columns]
        except Exception:
            backup_cols = []
    effective = backup_cols or fallback_source_cols
    if effective:
        return [c for c in augment.columns if str(c) not in set(effective)], list(effective)
    return [str(c) for c in augment.columns], []


def main() -> int:
    parser = argparse.ArgumentParser(description="scorer_v2 sweep: B-1 + B-2.")
    parser.add_argument("--judge-model", default="claude-opus-4.8-xhigh")
    parser.add_argument("--out-dir", default="characteristic_evaluation_v2")
    parser.add_argument("--skill-off-subdir", default="augment_skill_off")
    parser.add_argument("--skill-on-subdir", default="augment_skill_on_v11")
    parser.add_argument("--skill-on-e2e-subdir", default="analyses/skill_on_e2e_v11/tapp_workdir")
    parser.add_argument("--judge-timeout", type=int, default=300)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--variants", nargs="*", default=list(VARIANT_ORDER), choices=list(VARIANT_ORDER))
    parser.add_argument("--models", nargs="*", default=list(MODELS), choices=list(MODELS))
    parser.add_argument("--scorers", nargs="*", default=["b1", "b2"], choices=["b1", "b2"])
    parser.add_argument("--subtypes", nargs="*", default=None, choices=list(b2.SUBTYPES),
                        help="Only score scenarios of these subtypes.")
    parser.add_argument("--evidence-rows", type=int, default=5, help="Rows of cell evidence shown to the B-1 judge.")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--no-llm-judge", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dedup-exact", action="store_true")
    args = parser.parse_args()

    out_root = (ROOT / args.out_dir) if not Path(args.out_dir).is_absolute() else Path(args.out_dir)

    # (portion, model, scenario_dir) work items.
    tasks: list[tuple[str, str, Path, str]] = []
    for portion in PORTIONS:
        for model in args.models:
            dirs = rundrv._scenario_dirs(portion, model)
            if args.limit:
                dirs = dirs[: args.limit]
            for scenario_dir in dirs:
                subtype = b2.resolve_subtype(_gt_query(scenario_dir.name))
                if args.subtypes and subtype not in args.subtypes:
                    continue
                tasks.append((portion, model, scenario_dir, subtype))

    rows: list[dict[str, Any]] = []

    def _run(task: tuple[str, str, Path, str]) -> list[dict[str, Any]]:
        portion, model, scenario_dir, subtype = task
        scenario = scenario_dir.name
        gt_q = _gt_query(scenario)
        query, source_cols = rundrv._query_and_source_columns(scenario_dir)
        if not query:
            query = str(gt_q.get("text") or "")
        focus = str(gt_q.get("focus_variable") or "") or None
        concept = focus if subtype == "faceted_decomposition" else None

        out_dir = out_root / f"{portion}__{scenario}" / model
        out_dir.mkdir(parents=True, exist_ok=True)
        produced: list[dict[str, Any]] = []

        for variant in args.variants:
            table_parts, specs_parts = _variant_paths(args, variant)
            augment_path = scenario_dir.joinpath(*table_parts)
            meta = {"portion": portion, "model": model, "scenario": scenario,
                    "variant": variant, "subtype": subtype}

            if not augment_path.exists():
                produced.append({**meta, "status": "missing_output", "path": str(augment_path)})
                continue

            augment = semrec._read_table(augment_path).reset_index(drop=True)
            specs_payload = rundrv._load_specs(scenario_dir, specs_parts)
            specs_by_name = {str(s.get("name")): s for s in (specs_payload.get("specs") or []) if s.get("name")}
            new_columns, source_columns = _resolve_columns(
                augment, augment_path, variant, specs_by_name, source_cols
            )
            new_columns = [str(c) for c in new_columns]
            if args.dedup_exact:
                new_columns, _ = charadh.dedup_exact(new_columns)

            common = dict(
                augment_table=augment,
                new_columns=new_columns,
                specs_by_name=specs_by_name,
                query=query,
                judge_model=args.judge_model,
                judge_timeout=args.judge_timeout,
                attempts=args.attempts,
                no_llm_judge=args.no_llm_judge,
            )

            for scorer in args.scorers:
                out_path = out_dir / f"{variant}_{scorer}.json"
                if out_path.exists() and not args.force:
                    try:
                        prev = semrec._read_json(out_path)
                        if prev.get("status") == "scored":
                            produced.append({**meta, **prev, "scorer_kind": scorer})
                            continue
                    except Exception:
                        pass
                try:
                    if scorer == "b1":
                        rep = b1.evaluate(
                            **common,
                            source_columns=source_columns,
                            log_path=out_dir / f"{variant}_b1_judge_call.json",
                            n_evidence_rows=args.evidence_rows,
                        )
                    else:
                        rep = b2.evaluate(
                            **common,
                            subtype=subtype,
                            focus=focus,
                            concept=concept,
                            source_columns=source_columns,
                            log_path=out_dir / f"{variant}_b2_judge_call.json",
                        )
                    rep["status"] = "scored"
                except Exception as exc:
                    rep = {"status": "judge_failed", "error": str(exc)[:500],
                           "n_added_columns": len(new_columns), "added_columns": new_columns}
                rep.update(meta)
                semrec._write_json(out_path, rep)
                produced.append({**rep, "scorer_kind": scorer})
        return produced

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = [pool.submit(_run, t) for t in tasks]
        for fut in as_completed(futures):
            try:
                rows.extend(fut.result())
            except Exception as exc:  # never let one scenario kill the sweep
                print(f"[warn] task failed: {exc}", flush=True)

    out_root.mkdir(parents=True, exist_ok=True)
    summary = aggregate(rows)
    semrec._write_json(out_root / "SUMMARY.json",
                       {"updated_at": semrec._now(), "judge_model": args.judge_model,
                        "variants": {v: _variant_paths(args, v)[0] for v in args.variants},
                        **summary, "n_reports": len(rows)})
    write_summary_md(summary, out_root / "SUMMARY.md", judge_model=args.judge_model)
    scored = len([r for r in rows if r.get("status") == "scored"])
    print(f"Scored {scored}/{len(rows)} scorer-runs; summary at {out_root / 'SUMMARY.md'}")
    return 0


# --------------------------------------------------------------------------- #
# Aggregation
# --------------------------------------------------------------------------- #
def _mean(vals):
    vals = [v for v in vals if v is not None]
    return round(st.mean(vals), 4) if vals else None


_B2_FIELDS = {
    "predictive_feature_engineering": ("adherence", "predictor_fraction", "predictive_utility", "leakage_rate"),
    "exploratory_data_analysis": ("adherence", "predictor_fraction", "relationship_informativeness", "interpretable_fraction"),
    "causal_attribution": ("adherence", "treatment_present", "confounder_present", "unnamed_confounder_present",
                           "n_confounders", "n_unnamed_confounders", "unnamed_confounder_fraction", "confounder_quality"),
    "what_if": ("adherence", "treatment_present", "treatment_intervenable", "confounder_present",
                "unnamed_confounder_present", "n_confounders", "n_unnamed_confounders",
                "unnamed_confounder_fraction", "confounder_quality"),
    "faceted_decomposition": ("adherence", "facet_fraction", "mutual_exclusivity", "exhaustiveness", "mece", "redundancy"),
    "focus_inference": ("adherence", "focus_coherence", "structure_quality", "focus_actionability", "redundancy"),
}

_B1_FIELDS = ("b1_overall", "analytical_usefulness", "source_groundedness", "hallucination_rate")


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    b1_buckets: dict[tuple[str, str], list[dict]] = defaultdict(list)
    b2_buckets: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        if row.get("status") != "scored":
            continue
        m = row.get("metrics") or {}
        if row.get("scorer_kind") == "b1":
            b1_buckets[(row["model"], row["variant"])].append(m)
        else:
            b2_buckets[(row["subtype"], row["model"], row["variant"])].append(m)

    def _agg(metrics: list[dict], fields) -> dict[str, Any]:
        out: dict[str, Any] = {"n": len(metrics)}
        for f in fields:
            vals = [1.0 if v is True else 0.0 if v is False else v for v in (m.get(f) for m in metrics)]
            out[f] = _mean(vals)
        return out

    b1_summary: dict[str, dict[str, Any]] = {}
    for (model, variant), metrics in sorted(b1_buckets.items()):
        b1_summary.setdefault(model, {})[variant] = _agg(metrics, _B1_FIELDS)

    b2_summary: dict[str, dict[str, dict[str, Any]]] = {}
    for (subtype, model, variant), metrics in sorted(b2_buckets.items()):
        b2_summary.setdefault(subtype, {}).setdefault(model, {})[variant] = _agg(metrics, _B2_FIELDS[subtype])

    return {"b1_by_model_variant": b1_summary, "b2_by_subtype_model_variant": b2_summary}


def write_summary_md(summary: dict[str, Any], path: Path, *, judge_model: str) -> None:
    lines = [
        "# scorer_v2 — Experiment B Summary",
        "",
        f"Grader: `{judge_model}`. B-1 = general augmentation quality (necessary conditions, no completeness). "
        "B-2 = per-subtype instruction following.",
        "",
        "## B-1 General augmentation quality",
        "",
        "| Model | Variant | n | B-1 overall | Analytical usefulness | Source groundedness | Hallucination rate |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in MODELS:
        for variant in VARIANT_ORDER:
            a = (summary["b1_by_model_variant"].get(model) or {}).get(variant)
            if not a:
                continue
            lines.append(
                f"| {model} | {variant} | {a['n']} | {a.get('b1_overall')} | "
                f"{a.get('analytical_usefulness')} | {a.get('source_groundedness')} | {a.get('hallucination_rate')} |"
            )
    lines.append("")
    lines.append("## B-2 Characteristic adherence (instruction following)")
    lines.append("")

    for subtype in b2.SUBTYPES:
        by_model = summary["b2_by_subtype_model_variant"].get(subtype)
        if not by_model:
            continue
        fields = _B2_FIELDS[subtype]
        lines.append(f"### {b2.SUBTYPE_LABEL[subtype]}")
        lines.append("")
        header = "| Model | Variant | n | " + " | ".join(f.replace("_", " ") for f in fields) + " |"
        lines.append(header)
        lines.append("| --- | --- | ---: |" + " ---: |" * len(fields))
        for model in MODELS:
            for variant in VARIANT_ORDER:
                a = (by_model.get(model) or {}).get(variant)
                if not a:
                    continue
                cells = " | ".join(str(a.get(f)) for f in fields)
                lines.append(f"| {model} | {variant} | {a['n']} | {cells} |")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
