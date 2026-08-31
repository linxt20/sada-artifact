"""Generate analysis reports for the *update* skill_on tables into analysis_report_update.

Scope:
  <ds>/<scen>/{haiku,sonnet}__skill_on_v11_update.csv       -> skill_on_v11_update.md      (neutral prompt)
  <ds>/<scen>/{haiku,sonnet}__skill_on_e2e_v11_update.csv   -> skill_on_e2e_v11_update.md  (TAPP-aware e2e prompt)

Output: analysis_report_update/<model_prefix>/<dataset>/<scenario>/<stem>.md
Reuses the prompts + claude-CLI plumbing from gen_augment_table_reports.py so the
update corpus stays comparable with the existing one. The only e2e difference is the
workdir: it points at analyses/skill_on_e2e_v11_update/tapp_workdir (the update run).
"""
from __future__ import annotations

import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import gen_augment_table_reports as base

ROOT = Path(__file__).resolve().parent
AUGMENT_TABLE = ROOT / "augment_table"
OUT_ROOT = ROOT / "analysis_report_update"

MODEL_BY_PREFIX = base.MODEL_BY_PREFIX

# csv kind stem -> (report stem, canonical variant, prompt style)
KINDS = {
    "skill_on_v11_update": ("skill_on_v11_update", "skill_on", "neutral"),
    "skill_on_e2e_v11_update": ("skill_on_e2e_v11_update", "skill_on_e2e", "e2e"),
}


def _e2e_workdir_update(dataset: str, scenario: str, model: str) -> Path | None:
    for portion in ("dataset_portion_1", "dataset_portion_2"):
        wd = (ROOT / portion / model / f"{dataset}__{scenario}"
              / "analyses" / "skill_on_e2e_v11_update" / "tapp_workdir")
        if wd.is_dir():
            return wd
    return None


def build_jobs(args: argparse.Namespace) -> list[dict[str, Any]]:
    only_ds = set(args.dataset or [])
    only_scen = set(args.scenario or [])
    jobs: list[dict[str, Any]] = []
    for ds_dir in sorted(p for p in AUGMENT_TABLE.iterdir() if p.is_dir()):
        if only_ds and ds_dir.name not in only_ds:
            continue
        for scen_dir in sorted(p for p in ds_dir.iterdir() if p.is_dir()):
            if only_scen and scen_dir.name not in only_scen:
                continue
            for csv_kind, (stem, variant, style) in KINDS.items():
                for prefix in ("haiku", "sonnet"):
                    table = scen_dir / f"{prefix}__{csv_kind}.csv"
                    if not table.exists():
                        continue
                    dest = OUT_ROOT / prefix / ds_dir.name / scen_dir.name / f"{stem}.md"
                    if dest.exists() and dest.stat().st_size > 0 and not args.force:
                        continue
                    jobs.append({
                        "dataset": ds_dir.name, "scenario": scen_dir.name,
                        "prefix": prefix, "table": table, "dest": dest,
                        "model": MODEL_BY_PREFIX[prefix],
                        "variant": variant, "style": style, "stem": stem,
                    })
    if args.limit:
        jobs = jobs[: args.limit]
    return jobs


def run_job(job: dict[str, Any], exe: str, args: argparse.Namespace) -> dict[str, Any]:
    q = base._gt_query(job["dataset"], job["scenario"])
    if not q["text"]:
        return {**{k: str(job[k]) for k in ("dataset", "scenario", "stem")}, "status": "no_query"}

    if job["style"] == "e2e" and not args.neutral_e2e:
        aug_cols = base._augmented_columns(job["table"])
        workdir = _e2e_workdir_update(job["dataset"], job["scenario"], job["model"])
        if not aug_cols or workdir is None:
            return {"dataset": job["dataset"], "scenario": job["scenario"],
                    "stem": job["stem"], "status": "no_aug_context"}
        prompt_style = "e2e"
        prompt = base.E2E_PROMPT_TEMPLATE.format(
            workdir=workdir.resolve(), dest=job["dest"].resolve(),
            table=job["table"].resolve(), query_source=q["source"] or "GT.json",
            query=q["text"], model=job["model"], aug_columns=repr(aug_cols),
            begin=base.BEGIN, end=base.END,
        )
    else:
        prompt_style = "neutral"
        prompt = base.PROMPT_TEMPLATE.format(
            dest=job["dest"].resolve(), table=job["table"].resolve(),
            query_source=q["source"] or "GT.json", query=q["text"],
            variant=job["variant"], begin=base.BEGIN, end=base.END,
        )

    started = time.time()
    body = None
    rc = -1
    for attempt in range(1, args.attempts + 1):
        rc, raw = base._invoke_claude(exe, prompt, job["model"], args.timeout)
        body = base._extract_report(base._extract_result_text(raw))
        if body and len(body) > 200:
            break
        time.sleep(min(8, 2 * attempt))
        body = None
    wall = round(time.time() - started, 2)

    if not body:
        return {"dataset": job["dataset"], "scenario": job["scenario"],
                "stem": job["stem"], "status": "failed", "rc": rc}

    meta = {
        "dataset": job["dataset"], "scenario": job["scenario"],
        "variant": job["variant"], "model": job["model"],
        "prompt_style": prompt_style, "query": q["text"],
        "query_subtype": q["subtype"], "focus_variable": q["focus_variable"],
        "source_table": job["table"].relative_to(ROOT).as_posix(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "wall_seconds": wall,
    }
    job["dest"].parent.mkdir(parents=True, exist_ok=True)
    job["dest"].write_text(base._front_matter(meta) + body + "\n", encoding="utf-8")
    return {"dataset": job["dataset"], "scenario": job["scenario"],
            "stem": job["stem"], "status": "ok", "chars": len(body), "wall_seconds": wall}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dataset", action="append", default=None)
    p.add_argument("--scenario", action="append", default=None)
    p.add_argument("--neutral-e2e", action="store_true")
    p.add_argument("--workers", type=int, default=32)
    p.add_argument("--timeout", type=int, default=900)
    p.add_argument("--attempts", type=int, default=3)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--force", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    jobs = build_jobs(args)
    print(f"[update-gen] pending jobs: {len(jobs)}", flush=True)
    if args.dry_run:
        for j in jobs[:40]:
            print(f"  {j['prefix']}/{j['dataset']}/{j['scenario']}/{j['stem']}.md <- {j['table'].name} [{j['style']}]")
        if len(jobs) > 40:
            print(f"  ... and {len(jobs) - 40} more")
        return 0
    if not jobs:
        return 0

    exe = base.find_claude()
    results: list[dict[str, Any]] = []
    done = 0
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futs = {ex.submit(run_job, j, exe, args): j for j in jobs}
        for fut in as_completed(futs):
            j = futs[fut]
            try:
                r = fut.result()
            except Exception as exc:
                r = {"dataset": j["dataset"], "scenario": j["scenario"],
                     "stem": j["stem"], "status": "error", "error": repr(exc)[:300]}
            results.append(r)
            done += 1
            print(f"[update-gen] ({done}/{len(jobs)}) {r['dataset']}/{r['scenario']}/{r['stem']} -> {r['status']}", flush=True)

    ok = sum(1 for r in results if r["status"] == "ok")
    print(f"[update-gen] ok={ok} failed={len(results) - ok}")
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    log = OUT_ROOT / "_generation_log.json"
    prev = base._read_json(log).get("runs", []) if log.exists() else []
    import json
    log.write_text(json.dumps(
        {"runs": prev + [{"at": datetime.now(timezone.utc).isoformat(), "results": results}]},
        ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
