#!/usr/bin/env python3
"""Produce skill_off (naive free-augmentation) CSVs into _update/<ds>/skill_off/.

Mirrors the proven v11 skill_off pipeline (run_skilloff_e2e.augment): hide target ->
naive whole-table+query augmentation via a global claude pool -> re-attach target,
row-aligned. Large tables capped to the seed-0 3000-row eval subset (same subset the
pipeline evaluates + the same rows skill_on_e2e augmented). Output naming matches what
eval_5seed.py expects: augment_<mtag>.csv.

Idempotent: skips a (ds,model) whose augment_<mtag>.csv already exists.
Eval is a separate step (eval_5seed.py skill_off).

Usage: run_skilloff_augment.py [ds...] [haiku|sonnet ...]
Env: W_API (claude pool, def 64), JOBS (pairs, def 6), DEFAULT_CAP (def 3000)
"""
import os, sys, glob, threading
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("TEXTTABBENCH_ROOT", "/mnt/data/TextTabBench")
os.chdir(REPO); sys.path.insert(0, REPO)
sys.path.insert(0, SCRIPT_DIR)
legacy_helper = os.path.join(REPO, "augment_process_result_v11")
if os.path.isdir(legacy_helper):
    sys.path.insert(0, legacy_helper)
import skilloff_augment

OUT = os.path.join(REPO, "augment_process_result_v11_update")
RAW = os.path.join(REPO, "datasets_notebooks", "datasets_files", "raw")
MODELS = {"haiku": "claude-haiku-4-5", "sonnet": "claude-sonnet-4-6"}
DATASETS = ["laptops", "wine", "hs_cards", "beer", "airbnb", "osha_accidents",
            "spotify", "mercari", "job_frauds", "customer_complaints", "kickstarter", "sf_permits"]
DEFAULT_CAP = int(os.environ.get("DEFAULT_CAP", "3000"))
W_API = int(os.environ.get("W_API", "64"))
JOBS = int(os.environ.get("JOBS", "6"))

QUERIES = {
    "customer_complaints": "What complaint-level factors are related to company response outcomes in the consumer complaint data?",
    "job_frauds": "What job-posting signals are related to posting credibility and potential fraud risk?",
    "hs_cards": "What card-level attributes are related to player class organization in the Hearthstone card data?",
    "kickstarter": "What campaign-level factors are related to campaign status in the Kickstarter data?",
    "osha_accidents": "What accident-record characteristics are related to assigned task categories in the OSHA data?",
    "spotify": "What track-level metadata and textual signals are related to genre organization in the Spotify data?",
    "airbnb": "What listing-level factors are related to price variation in the Airbnb data?",
    "beer": "What review-level and product-level factors are related to overall beer review scores?",
    "laptops": "What product-level factors are related to pricing in the laptop product data?",
    "mercari": "What listing-level factors are related to item price in the Mercari product data?",
    "sf_permits": "What permit-application factors are related to approval time in the San Francisco building permit data?",
    "wine": "What wine-level factors are related to price variation in the wine data?",
}

ENV = dict(os.environ)
ENV["PYTHONUTF8"] = "1"; ENV["PYTHONIOENCODING"] = "utf-8"; ENV["PROJECT_ROOT"] = REPO
ENV["IS_SANDBOX"] = "1"; ENV.pop("CLAUDECODE", None)
os.environ.update(ENV)

api_pool = ThreadPoolExecutor(max_workers=W_API)


def find_pkl(ds):
    return glob.glob(os.path.join(RAW, "*", ds, f"{ds}_processed.pkl"))[0]


def augment(ds, mtag, model):
    outdir = os.path.join(OUT, ds, "skill_off")
    os.makedirs(outdir, exist_ok=True)
    aug = os.path.join(outdir, f"augment_{mtag}.csv")
    if os.path.exists(aug):
        print(f"  [skip] {aug}", flush=True)
        return
    cfg = pd.read_pickle(find_pkl(ds))["config"]
    tgt, tk = cfg["target"], cfg["task"]
    data = pd.read_csv(os.path.join(OUT, ds, "data.csv")).reset_index(drop=True)
    data = data.loc[:, ~data.columns.duplicated()]
    if DEFAULT_CAP and len(data) > DEFAULT_CAP:
        if tk == "reg":
            data = data.sample(n=DEFAULT_CAP, random_state=0).reset_index(drop=True)
        else:
            from pipelines.row_downsampling import downsample_rows_stratified
            data = downsample_rows_stratified({"x": data}, target_col=tgt, task=tk,
                                              downsampled_rows=DEFAULT_CAP, seed=0)["x"].reset_index(drop=True)
        print(f"  [row-cap] {ds}: {len(data)} rows (seed-0 eval subset)", flush=True)
    for c in data.columns:
        if data[c].dtype == object or str(data[c].dtype).startswith("string"):
            data[c] = data[c].map(lambda x: x.replace("\r", " ").replace("\n", " ") if isinstance(x, str) else x)
    data = data.reset_index(drop=True)
    strip = tgt in data.columns
    df_aug = (data.drop(columns=[tgt]) if strip else data).reset_index(drop=True)
    inp = os.path.join(outdir, f"input_{mtag}.csv")
    df_aug.to_csv(inp, index=False)
    raw = os.path.join(outdir, f"augment_{mtag}.raw.csv")
    print(f"  $ free_augment {ds}/{mtag} (model={model}, target '{tgt}' hidden={strip})", flush=True)
    merged = skilloff_augment.free_augment(inp, model, QUERIES[ds], raw,
                                           os.path.join(outdir, f"wd_{mtag}"), executor=api_pool, df=df_aug)
    merged = merged.reset_index(drop=True)
    if len(merged) != len(data):
        raise RuntimeError(f"rowcount mismatch ({len(merged)} vs {len(data)})")
    if strip:
        merged[tgt] = data[tgt].values
    merged.to_csv(aug, index=False)
    print(f"  [OK augment] {aug} rows={len(merged)} cols={merged.shape[1]}", flush=True)


if __name__ == "__main__":
    args = sys.argv[1:]
    ds_args = [a for a in args if a in DATASETS]
    m_args = [a for a in args if a in MODELS]
    targets = ds_args or DATASETS
    models = m_args or list(MODELS)
    pairs = [(ds, m) for ds in targets for m in models]
    print(f"[start] skill_off augment pairs={len(pairs)} jobs={JOBS} w_api={W_API}", flush=True)
    backlog = list(pairs); futs = {}; attempts = {}
    with ThreadPoolExecutor(max_workers=JOBS) as ex:
        def fill():
            while backlog and len(futs) < JOBS:
                ds, m = backlog.pop(0)
                attempts[(ds, m)] = attempts.get((ds, m), 0) + 1
                futs[ex.submit(augment, ds, m, MODELS[m])] = (ds, m)
        fill()
        while futs:
            done, _ = wait(list(futs), return_when=FIRST_COMPLETED)
            for f in done:
                p = futs.pop(f)
                try:
                    f.result(); print(f"  [pair-done] {p[0]}/{p[1]}", flush=True)
                except Exception as e:
                    if attempts[p] < 4:
                        print(f"  [retry] {p[0]}/{p[1]} attempt {attempts[p]}: {e}", flush=True)
                        backlog.insert(0, p)
                    else:
                        print(f"  [GIVE-UP] {p[0]}/{p[1]}: {e}", flush=True)
            fill()
    print("==== SKILLOFF AUGMENT DONE ====", flush=True)
