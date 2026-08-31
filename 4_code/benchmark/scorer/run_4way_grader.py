"""Re-run the 4-way end-to-end analysis grading (pairwise + Bradley-Terry).

Two layouts are supported.

``--layout legacy`` (the original lab6 layout)
    Reports come from ``<portion>/<model>/<scenario>/analyses/<variant>/analysis.md``
    and results are written back into that scenario folder.

``--layout report`` (default; the consolidated corpus)
    Reports come from ``analysis_report/<dataset>/<scenario>/<prefix>__<kind>.md``
    and augmented tables from ``augment_table/<dataset>/<scenario>/``. Results are
    written to ``<out-dir>/<dataset>/<scenario>/<prefix>/``. The v11 tables are the
    scored ones, but the Bradley-Terry item labels stay canonical
    (``original / skill_off / skill_on / skill_on_e2e``) so scores remain
    comparable with the earlier runs.

For every scenario the four analysis reports

    original / skill_off / skill_on / skill_on_e2e

are graded against each other with the Lab8 pairwise grader (``grader_v3``), in
both A/B orders (12 ordered judgments), then aggregated with swap-stabilized
Bradley-Terry:

    <out>/_pk_<a>__<b>__swap<0|1>.json
    <out>/pairwise_4way.json
    <out>/bt_4way.json
    <out>/pairwise_4way_metadata.json

The grader model defaults to ``claude-opus-4.8-xhigh``. Analysis reports are never
modified.
"""
from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from typing import Any

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent  # .../4way_2model
sys.path.insert(0, str(SCRIPT_DIR))

import grader_v3 as grader  # noqa: E402
import semantic_reference_recall as semrec  # noqa: E402

CLEAN_DIR = ROOT / "clean_annotations"
GT_DIRS = (ROOT / "gt_annotations", ROOT / "gt_annotations_supplement", CLEAN_DIR)
REPORT_DIR = ROOT / "analysis_report"
AUGMENT_TABLE = ROOT / "augment_table"
PORTIONS = ("dataset_portion_1", "dataset_portion_2")
MODELS = ("substrate-claude-haiku-4-5", "substrate-claude-sonnet-4-6")

VARIANTS = ("original", "skill_off", "skill_on", "skill_on_e2e")
# variant -> augmented table relative path parts (None = no augmented table)
VARIANT_TABLE: dict[str, tuple[str, ...] | None] = {
    "original": None,
    "skill_off": ("augment_skill_off", "augment.csv"),
    "skill_on": ("augment_skill_on", "augment.csv"),
    "skill_on_e2e": ("analyses", "skill_on_e2e", "tapp_workdir", "augment.csv"),
}

# report layout: canonical variant -> file/table stem under analysis_report / augment_table
REPORT_KIND: dict[str, str] = {
    "original": "original",
    "skill_off": "skill_off",
    "skill_on": "skill_on-v11",
    "skill_on_e2e": "skill_on_e2e-v11",
}
# ``--skill-off-kind`` swaps which skill-off corpus fills the canonical
# ``skill_off`` slot (e.g. ``skill_off_update`` for the agentic baseline). The BT
# item label stays ``skill_off`` so scores line up with earlier runs.

MODEL_BY_PREFIX = {
    "haiku": "substrate-claude-haiku-4-5",
    "sonnet": "substrate-claude-sonnet-4-6",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_gt_package(dataset_key: str, scenario: str) -> Path | None:
    for gt_root in GT_DIRS:
        if not gt_root.is_dir():
            continue
        for name in (dataset_key, dataset_key.replace("_", "-"), dataset_key.replace("-", "_")):
            package = gt_root / name / "augmentations" / scenario
            if (package / "GT.json").exists():
                return package
    return None


def _gt_context(dataset_key: str, scenario: str) -> tuple[str, set[str]]:
    """Return (query_text, original_column_names) from the GT package if present."""
    package = _resolve_gt_package(dataset_key, scenario)
    if package is None:
        return "", set()
    try:
        gt = semrec._read_json(package / "GT.json")
    except Exception:
        return "", set()
    query = gt.get("query") or {}
    original_cols = {
        str(col.get("name"))
        for col in (gt.get("original_schema") or {}).get("columns") or []
        if col.get("name")
    }
    return str(query.get("text") or "").strip(), original_cols


def _augmented_columns(scenario_dir: Path, variant: str, original_cols: set[str]) -> list[str]:
    parts = VARIANT_TABLE[variant]
    if parts is None:
        return []
    table = scenario_dir.joinpath(*parts)
    if not table.exists():
        return []
    try:
        frame = semrec._read_table(table)
    except Exception:
        return []
    cols = [str(c) for c in frame.columns]
    if original_cols:
        return [c for c in cols if c not in original_cols]
    return cols


def _read_report(scenario_dir: Path, variant: str) -> str | None:
    path = scenario_dir / "analyses" / variant / "analysis.md"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    return text or None


def _strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            return text[end + 5 :].lstrip("\n")
    return text


def _read_report_v2(dataset: str, scenario: str, prefix: str, variant: str) -> str | None:
    """Read a report from the consolidated ``analysis_report`` corpus."""
    path = REPORT_DIR / dataset / scenario / f"{prefix}__{REPORT_KIND[variant]}.md"
    if not path.exists():
        return None
    text = _strip_front_matter(path.read_text(encoding="utf-8", errors="replace")).strip()
    return text or None


def _augmented_columns_v2(dataset: str, scenario: str, prefix: str, variant: str, original_cols: set[str]) -> list[str]:
    """Added columns of a variant's table under ``augment_table``.

    The scenario's own ``original.csv`` is the authoritative baseline; the GT
    ``original_schema`` is only a fallback.
    """
    if variant == "original":
        return []
    scen_dir = AUGMENT_TABLE / dataset / scenario
    table = scen_dir / f"{prefix}__{REPORT_KIND[variant]}.csv"
    if not table.exists():
        return []
    try:
        cols = [str(c) for c in semrec._read_table(table).columns]
    except Exception:
        return []
    base = set(original_cols)
    baseline = scen_dir / "original.csv"
    if baseline.exists():
        try:
            base |= {str(c) for c in semrec._read_table(baseline).columns}
        except Exception:
            pass
    return [c for c in cols if c not in base] if base else cols


def _pk_path(scenario_dir: Path, pair_a: str, pair_b: str, swap: bool) -> Path:
    return scenario_dir / f"_pk_{pair_a}__{pair_b}__swap{int(swap)}.json"


def _prepare_scenario_v2(
    dataset: str, scenario: str, prefix: str, out_root: Path
) -> dict[str, Any] | None:
    reports = {v: _read_report_v2(dataset, scenario, prefix, v) for v in VARIANTS}
    available = [v for v in VARIANTS if reports[v]]
    if len(available) < 2:
        return None
    query_text, original_cols = _gt_context(dataset, scenario)
    aug = {v: _augmented_columns_v2(dataset, scenario, prefix, v, original_cols) for v in available}
    return {
        "model": MODEL_BY_PREFIX[prefix],
        "scenario_dir": out_root / dataset / scenario / prefix,
        "scenario": f"{dataset}__{scenario}",
        "available": available,
        "reports": reports,
        "aug": aug,
        "goal": query_text or scenario.replace("_", " "),
    }


def _prepare_scenario(model: str, scenario_dir: Path) -> dict[str, Any] | None:
    dataset_key, _, scenario = scenario_dir.name.partition("__")
    reports = {variant: _read_report(scenario_dir, variant) for variant in VARIANTS}
    available = [variant for variant in VARIANTS if reports[variant]]
    if len(available) < 2:
        return None
    query_text, original_cols = _gt_context(dataset_key, scenario)
    aug = {variant: _augmented_columns(scenario_dir, variant, original_cols) for variant in available}
    goal = query_text or scenario.replace("_", " ")
    return {
        "model": model,
        "scenario_dir": scenario_dir,
        "scenario": scenario_dir.name,
        "available": available,
        "reports": reports,
        "aug": aug,
        "goal": goal,
    }


def _ordered_jobs(available: list[str]) -> list[tuple[str, str, bool]]:
    jobs: list[tuple[str, str, bool]] = []
    for pair_a, pair_b in combinations(available, 2):
        jobs.append((pair_a, pair_b, False))
        jobs.append((pair_a, pair_b, True))
    return jobs


def _run_pair(
    ctx: dict[str, Any],
    pair_a: str,
    pair_b: str,
    swap: bool,
    claude_exe: str,
    args: argparse.Namespace,
) -> None:
    scenario_dir: Path = ctx["scenario_dir"]
    scenario_dir.mkdir(parents=True, exist_ok=True)
    pk_path = _pk_path(scenario_dir, pair_a, pair_b, swap)
    if pk_path.exists() and args.resume:
        try:
            existing = semrec._read_json(pk_path)
            if existing.get("judge_model") == args.judge_model:
                return
        except Exception:
            pass

    var_a, var_b = (pair_b, pair_a) if swap else (pair_a, pair_b)
    result = grader.judge_pairwise(
        claude_exe,
        ctx["goal"],
        ctx["reports"][var_a],
        ctx["reports"][var_b],
        aug_cols_a=ctx["aug"].get(var_a, []),
        aug_cols_b=ctx["aug"].get(var_b, []),
        timeout_s=args.judge_timeout,
        model=args.judge_model,
        fallback_model=args.fallback_model or None,
        max_attempts=args.attempts,
    )
    outcome = grader.PKOutcome(
        var_a=var_a,
        var_b=var_b,
        swap=swap,
        raw_winner=result.get("winner", "TIE"),
        margin=result.get("margin", "small"),
        ok=bool(result.get("ok")),
        scores_a=result.get("scores_a"),
        scores_b=result.get("scores_b"),
        dimension_decisions=result.get("dimension_decisions") or {},
        evidence_refs=result.get("evidence_refs") or {"A": [], "B": []},
        augmented_column_refs=result.get("augmented_column_refs") or {"A": [], "B": []},
        confidence=result.get("confidence"),
        reason=result.get("reason"),
        validation_warnings=result.get("validation_warnings") or [],
    )
    payload = outcome.to_dict(drop_empty=False)
    payload["judge_rc"] = result.get("rc")
    payload["judge_model"] = args.judge_model
    grader.write_json(pk_path, payload)


def _assemble_scenario(ctx: dict[str, Any], args: argparse.Namespace) -> str:
    scenario_dir: Path = ctx["scenario_dir"]
    scenario_dir.mkdir(parents=True, exist_ok=True)
    available: list[str] = ctx["available"]
    outcomes: list[grader.PKOutcome] = []
    missing = 0
    for pair_a, pair_b in combinations(available, 2):
        for swap in (False, True):
            pk_path = _pk_path(scenario_dir, pair_a, pair_b, swap)
            if not pk_path.exists():
                missing += 1
                continue
            outcomes.append(grader.PKOutcome.from_dict(semrec._read_json(pk_path)))
    if not outcomes:
        return "no_outcomes"

    grader.write_json(scenario_dir / "pairwise_4way.json", [o.to_dict(drop_empty=False) for o in outcomes])
    bt = grader.compute_bt_payload(ctx["scenario"], outcomes, items=available)
    grader.write_json(scenario_dir / "bt_4way.json", bt)
    grader.write_json(
        scenario_dir / "pairwise_4way_metadata.json",
        {
            "dataset": ctx["scenario"],
            "evaluated_model": ctx["model"],
            "grader_model": args.judge_model,
            "grader_fallback_model": args.fallback_model or None,
            "grader_is_fixed": True,
            "outcome_count": len(outcomes),
            "created_at": _now(),
        },
    )
    return "ok" if not missing else f"partial_missing_{missing}"


def _discover_scenarios(args: argparse.Namespace) -> list[tuple[str, Path]]:
    only = set(args.scenario or [])
    found: list[tuple[str, Path]] = []
    for portion in PORTIONS:
        for model in MODELS:
            base = ROOT / portion / model
            if not base.is_dir():
                continue
            for scenario_dir in sorted(p for p in base.iterdir() if p.is_dir()):
                if only and scenario_dir.name not in only:
                    continue
                found.append((model, scenario_dir))
    if args.limit:
        found = found[: max(0, args.limit)]
    return found


def _build_contexts_v2(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[str]]:
    only_scen = set(args.scenario or [])
    only_ds = set(args.dataset or [])
    prefixes = tuple(args.prefix) if args.prefix else ("haiku", "sonnet")
    out_root = ROOT / args.out_dir

    contexts: list[dict[str, Any]] = []
    skipped: list[str] = []
    for ds_dir in sorted(p for p in AUGMENT_TABLE.iterdir() if p.is_dir()):
        if only_ds and ds_dir.name not in only_ds:
            continue
        for scen_dir in sorted(p for p in ds_dir.iterdir() if p.is_dir()):
            if only_scen and scen_dir.name not in only_scen:
                continue
            for prefix in prefixes:
                ctx = _prepare_scenario_v2(ds_dir.name, scen_dir.name, prefix, out_root)
                if ctx is None:
                    skipped.append(f"{ds_dir.name}/{scen_dir.name}/{prefix}")
                else:
                    contexts.append(ctx)
    if args.limit:
        contexts = contexts[: max(0, args.limit)]
    return contexts, skipped


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--layout",
        choices=("report", "legacy"),
        default="report",
        help="'report' reads analysis_report/ + augment_table/; 'legacy' reads <portion>/<model>/<scenario>/analyses/.",
    )
    parser.add_argument("--dataset", action="append", default=None, help="Dataset folder name (report layout). Repeatable.")
    parser.add_argument("--prefix", action="append", default=None, choices=["haiku", "sonnet"], help="Model prefix (report layout).")
    parser.add_argument("--out-dir", default="bt_result_v11", help="Output root for the report layout.")
    parser.add_argument(
        "--skill-off-kind",
        default="skill_off",
        help="Report/table stem filling the canonical skill_off slot "
             "(e.g. skill_off_update for the agentic baseline).",
    )
    parser.add_argument("--scenario", action="append", default=None, help="Scenario folder name. Repeatable.")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--judge-model", default="claude-opus-4.8-xhigh")
    parser.add_argument("--fallback-model", default=None)
    parser.add_argument("--judge-timeout", type=int, default=240)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--resume", action="store_true", help="Skip pair judgments already graded by the target model.")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if getattr(args, "skill_off_kind", "skill_off") != "skill_off":
        REPORT_KIND["skill_off"] = args.skill_off_kind
        print(f"[4way] skill_off slot <- {args.skill_off_kind}")
    if args.layout == "report":
        contexts, skipped = _build_contexts_v2(args)
    else:
        contexts, skipped = [], []
        for model, scenario_dir in _discover_scenarios(args):
            ctx = _prepare_scenario(model, scenario_dir)
            if ctx is None:
                skipped.append(f"{model}/{scenario_dir.name}")
            else:
                contexts.append(ctx)
    print(f"[4way] {len(contexts)} scenarios prepared, {len(skipped)} skipped (insufficient reports)", flush=True)
    for s in skipped[:10]:
        print(f"       skipped: {s}", flush=True)

    if args.dry_run:
        for ctx in contexts[:20]:
            print(
                f"  {ctx['model']} :: {ctx['scenario']} variants={ctx['available']} "
                f"aug={{{', '.join(f'{k}:{len(v)}' for k, v in ctx['aug'].items())}}} "
                f"goal={ctx['goal'][:60]!r}",
                flush=True,
            )
        if len(contexts) > 20:
            print(f"  ... and {len(contexts) - 20} more", flush=True)
        print(f"[4way] would queue {sum(len(_ordered_jobs(c['available'])) for c in contexts)} judgments", flush=True)
        return 0

    claude_exe = grader.find_claude()
    jobs: list[tuple[dict[str, Any], str, str, bool]] = []
    for ctx in contexts:
        for pair_a, pair_b, swap in _ordered_jobs(ctx["available"]):
            jobs.append((ctx, pair_a, pair_b, swap))
    total = len(jobs)
    print(f"[4way] {total} pairwise judgments queued (model={args.judge_model}, workers={args.workers})", flush=True)

    done = 0
    workers = max(1, args.workers)
    if workers == 1:
        for ctx, pair_a, pair_b, swap in jobs:
            _run_pair(ctx, pair_a, pair_b, swap, claude_exe, args)
            done += 1
            if done % 20 == 0 or done == total:
                print(f"[4way] judged {done}/{total}", flush=True)
    else:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(_run_pair, ctx, pair_a, pair_b, swap, claude_exe, args): (ctx, pair_a, pair_b, swap)
                for ctx, pair_a, pair_b, swap in jobs
            }
            for future in as_completed(futures):
                done += 1
                future.result()
                if done % 20 == 0 or done == total:
                    print(f"[4way] judged {done}/{total}", flush=True)

    for ctx in contexts:
        status = _assemble_scenario(ctx, args)
        print(f"[4way] aggregated {ctx['model']} :: {ctx['scenario']} -> {status}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
