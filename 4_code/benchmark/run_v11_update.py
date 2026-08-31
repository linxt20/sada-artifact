"""Regenerate skill_on / skill_on_e2e augmentations with the UPDATED skill-v11.

Same pipeline as _run_v11_regen.py, but:
  - writes to NEW workdirs (so it does NOT skip-reuse the old -v11 augment.csv)
  - output filename suffix is `_v11_update` (all underscores) instead of `-v11`

Outputs: augment_table/<dataset>/<scenario>/<haiku|sonnet>__<variant>_v11_update.csv
Resumable: skips a run whose (new) augment.csv already exists. Logs to _v11_update_log.txt.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# Artifact note: the operator lived at `<this dir>/skill-v11/` when this ran. In
# the artifact it is promoted to the top level as `2_operator/`; the original
# sibling location is kept as the fallback.
_ARTIFACT_TAPP = ROOT.parents[1] / "2_operator" / "scripts" / "run_tapp.py"
RUN_TAPP = _ARTIFACT_TAPP if _ARTIFACT_TAPP.exists() else ROOT / "skill-v11" / "scripts" / "run_tapp.py"
GT_DIR = ROOT / "gt_annotations"
AUG_TABLE = ROOT / "augment_table"
PORTIONS = ("dataset_portion_1", "dataset_portion_2")
MODELS = {"substrate-claude-haiku-4-5": "haiku", "substrate-claude-sonnet-4-6": "sonnet"}
# variant -> NEW workdir parts (distinct from old -v11 dirs so we truly re-run)
VARIANTS = {
    "skill_on": ("augment_skill_on_v11_update",),
    "skill_on_e2e": ("analyses", "skill_on_e2e_v11_update", "tapp_workdir"),
}
MAX_WORKERS = 3          # concurrent scenarios
TAPP_WORKERS = 8         # --max-workers inside each run_tapp
RUN_TIMEOUT = 36000
LOG = ROOT / "_v11_update_log.txt"
_log_lock = threading.Lock()


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%H:%M:%S")


def _log(msg: str) -> None:
    line = f"[{_now()}] {msg}"
    with _log_lock:
        print(line, flush=True)
        with LOG.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def _gt_query(scenario_folder: str) -> str:
    dataset_key, _, scenario = scenario_folder.partition("__")
    for name in (dataset_key, dataset_key.replace("_", "-")):
        p = GT_DIR / name / "augmentations" / scenario / "GT.json"
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            return str((data.get("query") or {}).get("text") or "").strip()
    return ""


def _run_one(portion: str, model: str, short: str, scenario_dir: Path, variant: str) -> str:
    scenario = scenario_dir.name
    dataset, _, scen = scenario.partition("__")
    workdir = scenario_dir.joinpath(*VARIANTS[variant])
    out_csv = workdir / "augment.csv"
    dest = AUG_TABLE / dataset / scen / f"{short}__{variant}_v11_update.csv"

    if out_csv.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out_csv, dest)
        return f"SKIP (exists) {model} {scenario} {variant}"

    query = _gt_query(scenario)
    if not query:
        return f"FAIL no-query {model} {scenario} {variant}"
    src = scenario_dir / "augment_skill_off" / "augment_original_backup.csv"
    if not src.exists():
        return f"FAIL no-source {model} {scenario} {variant}"

    workdir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, str(RUN_TAPP), "augment-e2e",
        "--input", str(src),
        "--workdir", str(workdir),
        "--query", query,
        "--model", model,
        "--max-workers", str(TAPP_WORKERS),
        "--attempts", "2",
        "--output", str(out_csv),
        "--allow-low-coverage-fallback",
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=RUN_TIMEOUT)
    except subprocess.TimeoutExpired:
        return f"FAIL timeout {model} {scenario} {variant}"
    if out_csv.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out_csv, dest)
        return f"OK {model} {scenario} {variant}"
    tail = (proc.stderr or proc.stdout or "")[-300:].replace("\n", " ")
    return f"FAIL rc={proc.returncode} {model} {scenario} {variant} :: {tail}"


def main() -> int:
    only = sys.argv[1] if len(sys.argv) > 1 else None  # optional substring filter (smoke)
    tasks: list[tuple[str, str, str, Path, str]] = []
    for portion in PORTIONS:
        for model, short in MODELS.items():
            base = ROOT / portion / model
            if not base.exists():
                continue
            for scenario_dir in sorted(p for p in base.iterdir() if p.is_dir() and (p / "augment_skill_off").exists()):
                if only and only not in scenario_dir.name:
                    continue
                for variant in VARIANTS:
                    tasks.append((portion, model, short, scenario_dir, variant))

    _log(f"START v11 UPDATE: {len(tasks)} runs, {MAX_WORKERS} concurrent, tapp_workers={TAPP_WORKERS}")
    done = ok = skip = fail = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futs = {pool.submit(_run_one, *t): t for t in tasks}
        for fut in as_completed(futs):
            res = fut.result()
            done += 1
            if res.startswith("OK"):
                ok += 1
            elif res.startswith("SKIP"):
                skip += 1
            else:
                fail += 1
            _log(f"({done}/{len(tasks)}) {res}")
    _log(f"DONE v11 UPDATE: ok={ok} skip={skip} fail={fail} / {len(tasks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
