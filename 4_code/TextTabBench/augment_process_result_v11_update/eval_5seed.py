#!/usr/bin/env python3
"""Unified 5-seed evaluator for the _update comparison tables.

For a given augmented CSV (or the raw data.csv baseline), run the pipeline eval
with seeds 0..4, text (--run_pipe) and no_text (--no_text). Embeddings are seed-
independent (computed on the full custom_csv once), so they are generated a single
time per tag and reused across all seeds. Each seed appends a new run_timestamp to
the SAME result json (save_partial_results merges, never overwrites), so a finished
json holds 5 runs.

This drives THREE variants into augment_process_result_v11_update/<ds>/<variant>/:
  - skill_off   : naive free-augmentation csv (produced by skilloff_augment)
  - skill_on_e2e: TA++ skill-v11 csv (already produced by run_skillon_e2e_linux)
  - baseline    : the raw data.csv (no augmentation, model-agnostic)

Idempotent & resumable: a (variant,model,setting) json that already has >=5 runs is
skipped; fewer -> only the missing seeds run.

Usage:
  eval_5seed.py <variant> <ds> [ds...] [haiku|sonnet ...]
    variant in {skill_off, skill_on_e2e, baseline}
Env: SEEDS (default "0 1 2 3 4"), W_CPU (concurrent evals, def 4), JOBS (pairs, def 6)
"""
import os, sys, glob, json, shutil, subprocess, threading
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED

REPO = os.environ.get("TEXTTABBENCH_ROOT", "/mnt/data/TextTabBench")
os.chdir(REPO); sys.path.insert(0, REPO)
PY = os.path.join(REPO, ".venv", "bin", "python")
PIPE = os.path.join(REPO, "pipelines", "main_pipeline.py")
OUT = os.path.join(REPO, "augment_process_result_v11_update")
RAW = os.path.join(REPO, "datasets_notebooks", "datasets_files", "raw")

MODELS = ("haiku", "sonnet")
DATASETS = ["laptops", "wine", "hs_cards", "beer", "airbnb", "osha_accidents",
            "spotify", "mercari", "job_frauds", "customer_complaints", "kickstarter", "sf_permits"]
SEEDS = [int(s) for s in os.environ.get("SEEDS", "0 1 2 3 4").split()]
W_CPU = int(os.environ.get("W_CPU", "4"))
JOBS = int(os.environ.get("JOBS", "6"))
OMP = str(max(1, 64 // max(1, W_CPU)))

ENV = dict(os.environ)
ENV["PYTHONUTF8"] = "1"; ENV["PYTHONIOENCODING"] = "utf-8"; ENV["PROJECT_ROOT"] = REPO
for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    ENV[k] = OMP
cpu_sem = threading.Semaphore(W_CPU)


def find_pkl(ds):
    return glob.glob(os.path.join(RAW, "*", ds, f"{ds}_processed.pkl"))[0]

def task_of(ds):
    return "classification" if find_pkl(ds).split(os.sep)[-3] == "classification" else "regression"

def embed_dir(ds, tag):
    return os.path.join(REPO, "datasets_files", "embeddings", task_of(ds), f"{ds}__{tag}")

def n_runs(path):
    if not os.path.exists(path):
        return 0
    try:
        return len(json.load(open(path)))
    except Exception:
        return 0

def run_pipe(cmd):
    r = subprocess.run([PY, "-u", PIPE] + cmd, env=ENV, cwd=REPO,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        tail = "\n".join((r.stdout or "").splitlines()[-6:] + (r.stderr or "").splitlines()[-6:])
        raise RuntimeError(f"pipeline rc={r.returncode}\n{tail}")


def csv_for(variant, ds, mtag):
    if variant == "baseline":
        return os.path.join(OUT, ds, "data.csv")
    if variant == "skill_on_e2e":
        return os.path.join(OUT, ds, "skill_on_e2e", f"augment_{mtag}.csv")
    if variant == "skill_off":
        return os.path.join(OUT, ds, "skill_off", f"augment_{mtag}.csv")
    raise ValueError(variant)


def do(variant, ds, mtag):
    outdir = os.path.join(OUT, ds, variant)
    os.makedirs(outdir, exist_ok=True)
    # baseline is model-agnostic -> single mtag "" (no model suffix)
    suf = "" if variant == "baseline" else f"_{mtag}"
    text_out = os.path.join(outdir, f"xgb_results_{ds}_text_skrub_shap{suf}.json")
    nt_out = os.path.join(outdir, f"xgb_results_{ds}_no_text{suf}.json")
    if n_runs(text_out) >= len(SEEDS) and n_runs(nt_out) >= len(SEEDS):
        print(f"  [skip] {variant}/{ds}{suf} both have {len(SEEDS)} seeds", flush=True)
        return

    aug = csv_for(variant, ds, mtag)
    if not os.path.exists(aug):
        raise RuntimeError(f"missing csv {aug}")
    # distinct tags so the three variants never collide in the embedding cache
    tagbase = {"baseline": "base", "skill_on_e2e": "e2e", "skill_off": "off"}[variant]
    tag = f"{ds}_{tagbase}{suf}_5s"
    tag_nt = f"{tag}_nt"

    with cpu_sem:
        if not os.path.exists(os.path.join(embed_dir(ds, tag), "skrub_text_embeddings.npy")):
            run_pipe(["--dataset", ds, "--custom_csv", aug, "--custom_tag", tag,
                      "--embed_methods", "skrub", "--generate_embeddings"])
        if not os.path.exists(os.path.join(embed_dir(ds, tag_nt), "skrub_text_embeddings.npy")):
            shutil.copytree(embed_dir(ds, tag), embed_dir(ds, tag_nt), dirs_exist_ok=True)

        for seed in SEEDS:
            # text
            stray = os.path.join(REPO, f"xgb_results_{ds}__{tag}.json")
            if n_runs(text_out) < SEEDS.index(seed) + 1:
                # move any accumulated json back to repo root so the pipeline appends to it
                if os.path.exists(text_out):
                    shutil.copy(text_out, stray)
                run_pipe(["--dataset", ds, "--custom_csv", aug, "--custom_tag", tag,
                          "--embed_methods", "skrub", "--eval_method", "xgb",
                          "--downsample_methods", "shap", "--run_pipe", "--seed", str(seed)])
                shutil.move(stray, text_out)
                print(f"  [OK] {variant}/{ds}{suf} text seed={seed} (runs={n_runs(text_out)})", flush=True)
            # no_text
            stray_nt = os.path.join(REPO, f"xgb_results_{ds}__{tag_nt}.json")
            if n_runs(nt_out) < SEEDS.index(seed) + 1:
                if os.path.exists(nt_out):
                    shutil.copy(nt_out, stray_nt)
                run_pipe(["--dataset", ds, "--custom_csv", aug, "--custom_tag", tag_nt,
                          "--embed_methods", "skrub", "--eval_method", "xgb",
                          "--downsample_methods", "shap", "--run_pipe", "--no_text", "--seed", str(seed)])
                shutil.move(stray_nt, nt_out)
                print(f"  [OK] {variant}/{ds}{suf} no_text seed={seed} (runs={n_runs(nt_out)})", flush=True)


if __name__ == "__main__":
    args = sys.argv[1:]
    variant = args[0]
    assert variant in ("skill_off", "skill_on_e2e", "baseline"), variant
    rest = args[1:]
    ds_args = [a for a in rest if a in DATASETS]
    m_args = [a for a in rest if a in MODELS]
    targets = ds_args or DATASETS
    models = [""] if variant == "baseline" else (m_args or list(MODELS))
    pairs = [(ds, m) for ds in targets for m in models]
    print(f"[start] variant={variant} seeds={SEEDS} pairs={len(pairs)} jobs={JOBS} w_cpu={W_CPU}", flush=True)

    backlog = list(pairs); futs = {}
    with ThreadPoolExecutor(max_workers=JOBS) as ex:
        def fill():
            while backlog and len(futs) < JOBS:
                ds, m = backlog.pop(0)
                futs[ex.submit(do, variant, ds, m)] = (ds, m)
        fill()
        while futs:
            done, _ = wait(list(futs), return_when=FIRST_COMPLETED)
            for f in done:
                p = futs.pop(f)
                try:
                    f.result(); print(f"  [pair-done] {variant}/{p[0]}/{p[1]}", flush=True)
                except Exception as e:
                    print(f"  [FAIL] {variant}/{p[0]}/{p[1]}: {e}", flush=True)
            fill()
    print("==== EVAL DONE ====", flush=True)
