#!/usr/bin/env python3
"""Rerun the text regime with a fixed embedding budget (SHAP top-k).

Every cell goes through the SHAP selector with the same top_k, so the embedding
budget no longer floats with the augmented column count. Only the text regime is
rerun; no_text results are unaffected (they have no embedding columns).

Usage:  rerun_k64.py [K] [ds ...]
Env:    JOBS (parallel cells, default 4), SEEDS (default "0")
"""
import os, subprocess, sys, json, shutil
from concurrent.futures import ThreadPoolExecutor

REPO = os.environ.get(
    "TEXTTABBENCH_ROOT",
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)
OUT = os.path.join(REPO, "augment_process_result_v11_update")
PY = os.path.join(REPO, ".venv", "bin", "python")
PIPE = os.path.join(REPO, "pipelines", "main_pipeline.py")

K = int(sys.argv[1]) if len(sys.argv) > 1 else 64
SEEDS = [int(s) for s in os.environ.get("SEEDS", "0").split()]
JOBS = int(os.environ.get("JOBS", "4"))

DATASETS = ["airbnb", "beer", "customer_complaints", "hs_cards", "job_frauds",
            "kickstarter", "laptops", "osha_accidents", "sf_permits", "spotify", "wine"]
if len(sys.argv) > 2:
    DATASETS = sys.argv[2:]

ENV = dict(os.environ)
ENV["PYTHONUTF8"] = "1"; ENV["PYTHONIOENCODING"] = "utf-8"; ENV["PROJECT_ROOT"] = REPO

LOG = os.path.join(OUT, f"_rerun_k{K}_log.txt")
_lock_print = __import__("threading").Lock()


def say(m):
    with _lock_print:
        print(m, flush=True)
        with open(LOG, "a") as f:
            f.write(m + "\n")


def n_runs(p):
    try:
        return len(json.load(open(p)))
    except Exception:
        return 0


def run_pipe(cmd):
    r = subprocess.run([PY, "-u", PIPE] + cmd, env=ENV, cwd=REPO,
                       capture_output=True, text=True)
    if r.returncode != 0:
        tail = "\n".join((r.stdout or "").splitlines()[-8:] + (r.stderr or "").splitlines()[-8:])
        raise RuntimeError(f"pipeline failed: {' '.join(cmd[:6])}\n{tail}")
    return r.stdout or ""


def csv_for(variant, ds, mtag):
    if variant == "baseline":
        return os.path.join(OUT, ds, "data.csv")
    return os.path.join(OUT, ds, variant, f"augment_{mtag}.csv")


def do(variant, ds, mtag):
    outdir = os.path.join(OUT, ds, variant)
    os.makedirs(outdir, exist_ok=True)
    suf = "" if variant == "baseline" else f"_{mtag}"
    out = os.path.join(outdir, f"xgb_results_{ds}_text_skrub_shap{suf}_k{K}.json")
    if n_runs(out) >= len(SEEDS):
        say(f"  [skip] {variant}/{ds}{suf}")
        return

    aug = csv_for(variant, ds, mtag)
    if not os.path.exists(aug):
        raise RuntimeError(f"missing csv {aug}")

    tagbase = {"baseline": "base", "skill_on_e2e": "e2e", "skill_off": "off"}[variant]
    tag = f"{ds}_{tagbase}{suf}_k{K}"

    base = ["--dataset", ds, "--custom_csv", aug, "--custom_tag", tag,
            "--embed_methods", "skrub"]

    task = "reg" if ds in ("airbnb", "beer", "laptops", "sf_permits", "wine") else "clf"
    emb_ok = os.path.join(REPO, "datasets_files", "embeddings", task,
                          f"{ds}__{tag}", "skrub_text_embeddings.npy")
    if not os.path.exists(emb_ok):
        run_pipe(base + ["--generate_embeddings"])

    stray = os.path.join(REPO, f"xgb_results_{ds}__{tag}.json")
    for seed in SEEDS:
        if n_runs(out) >= SEEDS.index(seed) + 1:
            continue
        if os.path.exists(out):
            shutil.copy(out, stray)
        run_pipe(base + ["--eval_method", "xgb", "--downsample_methods", "shap",
                         "--run_pipe", "--seed", str(seed), "--emb_top_k", str(K)])
        shutil.move(stray, out)
        say(f"  [OK] {variant}/{ds}{suf} seed={seed}")


def main():
    tasks = []
    for ds in DATASETS:
        tasks.append(("baseline", ds, "sonnet"))
        for v in ("skill_off", "skill_on_e2e"):
            for m in ("haiku", "sonnet"):
                tasks.append((v, ds, m))
    say(f"[start] k={K} datasets={len(DATASETS)} cells={len(tasks)} jobs={JOBS} seeds={SEEDS}")
    errs = []
    with ThreadPoolExecutor(max_workers=JOBS) as ex:
        futs = {ex.submit(do, *t): t for t in tasks}
        for f in futs:
            pass
        for f, t in futs.items():
            try:
                f.result()
            except Exception as e:
                errs.append((t, str(e)[:300]))
                say(f"  [FAIL] {t}: {str(e)[:300]}")
    say(f"[done] {len(tasks)-len(errs)}/{len(tasks)} ok, {len(errs)} failed")


if __name__ == "__main__":
    main()
