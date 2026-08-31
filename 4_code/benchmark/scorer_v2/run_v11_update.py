"""薄驱动: 对 augment_table/<dataset>/<scenario>/<model>__<variant>_update.csv 跑 B-1 + B-2。

布局(与 run_scorer_v2 的假设不同, 故单独驱动):
    augment_table/<dataset>/<scenario>/
        original.csv                              源表
        <model>__skill_off_update.csv             variant=skill_off
        <model>__skill_on_v11_update.csv          variant=skill_on
        <model>__skill_on_e2e_v11_update.csv      variant=skill_on_e2e
    gt_annotations/<dataset*>/{augmentations,annotation_update}/<scenario>/GT.json
        -> query.text / query.subtype / query.focus_variable

无 specs.json: specs_by_name={} (b1/b2 对此安全, domain/description 退空)。
新列 = augment 表列 - original.csv 列。

输出: augment_table_evaluation/augment_result_v11_update/<dataset>/<model>/<scenario>__<variant>_{b1,b2}.json
断点续跑: 已有 status==scored 的 json 跳过 (除非 --force)。
"""
from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
for _p in (str(SCRIPT_DIR), str(ROOT / "scorer"), str(ROOT / "scorer_characteristic")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import semantic_reference_recall as semrec  # noqa: E402
import b1_general_quality as b1              # noqa: E402
import b2_characteristic_adherence as b2     # noqa: E402

AUG_ROOT = ROOT / "augment_table"
GT_ROOT = ROOT / "gt_annotations"
OUT_ROOT = ROOT / "augment_table_evaluation" / "augment_result_v11_update"

MODELS = ("haiku", "sonnet")
VARIANTS = {
    "skill_off": "skill_off_update",
    "skill_on": "skill_on_v11_update",
    "skill_on_e2e": "skill_on_e2e_v11_update",
}


def _gt_query(dataset: str, scenario: str) -> dict[str, Any]:
    """GT query, 兼容 flag_N<->flag-N 与 augmentations/annotation_update 两种父目录。"""
    for name in (dataset, dataset.replace("_", "-")):
        for parent in ("augmentations", "annotation_update"):
            p = GT_ROOT / name / parent / scenario / "GT.json"
            if p.exists():
                return semrec._read_json(p).get("query") or {}
    return {}


def _iter_tasks(only_dataset: str | None, limit: int) -> list[tuple[str, str, str, str, Path]]:
    tasks: list[tuple[str, str, str, str, Path]] = []
    datasets = sorted(d.name for d in AUG_ROOT.iterdir() if d.is_dir() and not d.name.startswith("__"))
    for dataset in datasets:
        if only_dataset and dataset != only_dataset:
            continue
        ds_dir = AUG_ROOT / dataset
        scenarios = sorted(s.name for s in ds_dir.iterdir() if s.is_dir())
        if limit:
            scenarios = scenarios[:limit]
        for scenario in scenarios:
            sc_dir = ds_dir / scenario
            for model in MODELS:
                for variant, suffix in VARIANTS.items():
                    csv = sc_dir / f"{model}__{suffix}.csv"
                    if csv.exists():
                        tasks.append((dataset, scenario, model, variant, csv))
    return tasks


def _run_one(args, dataset, scenario, model, variant, csv) -> dict[str, Any]:
    sc_dir = csv.parent
    original = sc_dir / "original.csv"
    gt_q = _gt_query(dataset, scenario)
    query = str(gt_q.get("text") or "")
    subtype = b2.resolve_subtype(gt_q)
    focus = str(gt_q.get("focus_variable") or "") or None
    concept = focus if subtype == "faceted_decomposition" else None

    augment = semrec._read_table(csv).reset_index(drop=True)
    src_cols = [str(c) for c in semrec._read_table(original).columns] if original.exists() else []
    new_columns = [str(c) for c in augment.columns if str(c) not in set(src_cols)]

    out_dir = OUT_ROOT / dataset / model
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = f"{scenario}__{variant}"

    common = dict(
        augment_table=augment, new_columns=new_columns, specs_by_name={},
        query=query, judge_model=args.judge_model, judge_timeout=args.judge_timeout,
        attempts=args.attempts, no_llm_judge=args.no_llm_judge,
    )
    meta = {"dataset": dataset, "scenario": scenario, "model": model,
            "variant": variant, "subtype": subtype, "n_new_columns": len(new_columns)}
    results = {}
    for scorer in args.scorers:
        out_path = out_dir / f"{tag}_{scorer}.json"
        if out_path.exists() and not args.force:
            try:
                prev = semrec._read_json(out_path)
                if prev.get("status") == "scored":
                    results[scorer] = "cached"
                    continue
            except Exception:
                pass
        try:
            if scorer == "b1":
                rep = b1.evaluate(**common, source_columns=src_cols,
                                  log_path=out_dir / f"{tag}_b1_call.json",
                                  n_evidence_rows=args.evidence_rows)
            else:
                rep = b2.evaluate(**common, subtype=subtype, focus=focus, concept=concept,
                                  source_columns=src_cols, log_path=out_dir / f"{tag}_b2_call.json")
            rep["status"] = "scored"
            results[scorer] = "scored"
        except Exception as exc:
            rep = {"status": "judge_failed", "error": str(exc)[:400], "n_new_columns": len(new_columns)}
            results[scorer] = "failed"
        rep.update(meta)
        semrec._write_json(out_path, rep)
    return {**meta, "results": results}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--judge-model", default="claude-opus-4.8-xhigh")
    ap.add_argument("--scorers", nargs="*", default=["b1", "b2"], choices=["b1", "b2"])
    ap.add_argument("--judge-timeout", type=int, default=300)
    ap.add_argument("--attempts", type=int, default=3)
    ap.add_argument("--evidence-rows", type=int, default=5)
    ap.add_argument("--workers", type=int, default=32)
    ap.add_argument("--only-dataset", default=None)
    ap.add_argument("--limit", type=int, default=0, help="每数据集仅前 N scenario(冒烟)")
    ap.add_argument("--no-llm-judge", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    tasks = _iter_tasks(args.only_dataset, args.limit)
    print(f"tables={len(tasks)} scorers={args.scorers} judge={args.judge_model} workers={args.workers}", flush=True)
    done = 0
    counts = {"scored": 0, "cached": 0, "failed": 0}
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futs = [ex.submit(_run_one, args, *t) for t in tasks]
        for f in as_completed(futs):
            try:
                r = f.result()
                for v in r["results"].values():
                    counts[v] = counts.get(v, 0) + 1
            except Exception as exc:
                print(f"[warn] {exc}", flush=True)
            done += 1
            if done % 25 == 0 or done == len(tasks):
                print(f"[{done}/{len(tasks)}] scored={counts['scored']} cached={counts['cached']} failed={counts['failed']}", flush=True)
    print(f"DONE tables={len(tasks)} {counts}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
