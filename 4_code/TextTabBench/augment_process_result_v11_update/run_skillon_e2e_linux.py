"""Run skill_on_e2e (TA++ v11 augment) XGBoost+SHAP for TextTabBench datasets.

For each (dataset, model):
  1. reuse augment_process_result_v11/<ds>/data.csv (exported by the baseline runner)
  2. augment-e2e via the skill (claude via Agent Maestro) -> skill_on_e2e/augment_<mtag>.csv
  3. generate skrub embeddings (custom_tag <ds>_e2e_<mtag>)
  4. eval text (skrub) + no_text  (xgb, downsample=shap)
  5. move result jsons -> augment_process_result_v11/<ds>/skill_on_e2e/

Idempotent: skips steps whose outputs already exist. Continues past per-item failures.
Needs the Agent Maestro proxy running + ~/.claude/settings.json pointing at it.
Run from repo root with the .venv python.

Usage:
  python augment_process_result_v11/run_skillon_e2e.py                # all datasets, both models
  python augment_process_result_v11/run_skillon_e2e.py wine           # one dataset, both models
  python augment_process_result_v11/run_skillon_e2e.py wine haiku     # one dataset, one model tag
"""
import os, sys, glob, shutil, subprocess
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("TEXTTABBENCH_ROOT", os.path.abspath(os.path.dirname(SCRIPT_DIR)))
os.chdir(REPO)
if REPO not in sys.path:
    sys.path.insert(0, REPO)  # allow importing pipelines.* in-process (row cap)
PY = os.path.join(REPO, ".venv", "bin", "python")
PIPE = os.path.join(REPO, "pipelines", "main_pipeline.py")
artifact_src = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
# Artifact note: the operator is promoted to the top level as `2_operator/`; the
# original `<src>/benchmark/skill-v11/` location is kept as the fallback.
canonical_tapp = os.path.join(os.path.dirname(artifact_src), "2_operator", "scripts", "run_tapp.py")
if not os.path.exists(canonical_tapp):
    canonical_tapp = os.path.join(artifact_src, "benchmark", "skill-v11", "scripts", "run_tapp.py")
TAPP = os.environ.get(
    "SADA_TAPP",
    canonical_tapp if os.path.exists(canonical_tapp)
    else os.path.join(REPO, ".claude", "skill-v11", "scripts", "run_tapp.py"),
)
OUT = os.path.join(REPO, "augment_process_result_v11_update")
RAW = os.path.join(REPO, "datasets_notebooks", "datasets_files", "raw")

# model full name -> short tag (Agent Maestro proxy accepts DASH ids only)
MODELS = {"sonnet": "claude-sonnet-4-6", "haiku": "claude-haiku-4-5"}

# Optional: cap augmentation input to the pipeline's eval subset (seed-0, ds_rows=3000).
# Currently DISABLED (empty) — sf_permits is augmented on the FULL table and run in a
# separate phase with dedicated concurrency (see RUN_LAST + run_phases.ps1).
AUGMENT_ROW_CAP = {"sf_permits": 3000}

# Datasets excluded from a *default* run (no dataset arg) and launched separately by
# name, e.g. `run_skillon_e2e.py sf_permits`, so they can get their own thread budget.
RUN_LAST = {"sf_permits"}

# --- experiment variant controls (env-driven; default = leak-proof, no suffix) ---
# VARIANT     : suffix appended to every output name (augment csv, workdir, custom_tag,
#               result json) so a comparison run does NOT overwrite existing results.
# KEEP_TARGET : if truthy, DO NOT hide the target column from the augmentation input
#               (the old "with-target" behaviour) — used for the ablation comparison.
VARIANT = os.environ.get("VARIANT", "")
KEEP_TARGET = os.environ.get("KEEP_TARGET", "").strip().lower() not in ("", "0", "false", "no")

# small -> large (augment full rows; sf_permits is the heavy one, kept last)
DATASETS = [
    "laptops", "wine", "hs_cards", "beer", "airbnb", "osha_accidents",
    "spotify", "mercari", "job_frauds", "customer_complaints", "kickstarter", "sf_permits",
]

# focus-variable queries (configs/query_2.md)
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
ENV["PYTHONUTF8"] = "1"
ENV["PYTHONIOENCODING"] = "utf-8"
ENV["PROJECT_ROOT"] = REPO
# Remove CLAUDECODE so that child Claude Code processes are not blocked
# from launching (nested-session guard checks this variable).
ENV.pop("CLAUDECODE", None)

# tag-chunk workers inside ONE augmentation (concurrent claude calls to the proxy)
TAPP_WORKERS = os.environ.get("TAPP_WORKERS", "4")


def find_pkl(ds):
    hits = glob.glob(os.path.join(RAW, "*", ds, f"{ds}_processed.pkl"))
    return hits[0] if hits else None


def task_of(ds):
    return "classification" if find_pkl(ds).split(os.sep)[-3] == "classification" else "regression"


def target_of(ds):
    """Target/label column name for a dataset (from its processed.pkl config)."""
    bundle = pd.read_pickle(find_pkl(ds))
    return bundle["config"]["target"]


def embed_dir(ds, tag):
    return os.path.join(REPO, "datasets_files", "embeddings", task_of(ds), f"{ds}__{tag}")


def run_pipe(cmd):
    print("  $ main_pipeline " + " ".join(cmd), flush=True)
    r = subprocess.run([PY, "-u", PIPE] + cmd, env=ENV, cwd=REPO,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        tail = "\n".join((r.stdout or "").splitlines()[-8:] + (r.stderr or "").splitlines()[-8:])
        raise RuntimeError(f"pipeline rc={r.returncode}\n{tail}")


def augment(ds, mtag, model):
    e2e = os.path.join(OUT, ds, "skill_on_e2e")
    os.makedirs(e2e, exist_ok=True)
    name = f"{mtag}{VARIANT}"  # variant suffix keeps a comparison run from overwriting existing outputs
    aug_csv = os.path.join(e2e, f"augment_{name}.csv")
    if os.path.exists(aug_csv):
        print(f"  [skip augment] {aug_csv}", flush=True)
        return aug_csv
    data_csv = os.path.join(OUT, ds, "data.csv")
    tgt = target_of(ds)
    data_df = pd.read_csv(data_csv)

    # --- optional row cap for very large tables (e.g. sf_permits) ---
    # Augment exactly the pipeline's seed-0 eval subset (ds_rows=3000) instead of the
    # full table: identical eval rows as the skill_off baseline, tiny fraction of cost.
    cap = AUGMENT_ROW_CAP.get(ds)
    if cap and len(data_df) > cap:
        cfg_task = pd.read_pickle(find_pkl(ds))["config"]["task"]
        if cfg_task == "reg":
            # identical to main_pipeline's reg downsampling
            data_df = data_df.sample(n=cap, random_state=0).reset_index(drop=True)
        else:
            from pipelines.row_downsampling import downsample_rows_stratified
            data_df = downsample_rows_stratified(
                {"x": data_df.reset_index(drop=True)}, target_col=tgt,
                task=cfg_task, downsampled_rows=cap, seed=0)["x"].reset_index(drop=True)
        print(f"  [row-cap] {ds}: augmenting {len(data_df)} rows "
              f"(pipeline's seed-0 eval subset) instead of the full table", flush=True)

    # --- leak-proof augmentation input ---
    # Hide the target column from the model so it cannot copy the label into a new
    # "augmented" column (observed with osha_accidents). Re-attached after augmentation.
    # KEEP_TARGET=1 disables this (the "with-target" ablation) for comparison runs.
    strip_tgt = (tgt in data_df.columns) and not KEEP_TARGET
    aug_input = os.path.join(e2e, f"input_{name}.csv")
    (data_df.drop(columns=[tgt]) if strip_tgt else data_df).to_csv(aug_input, index=False)

    wd = os.path.join(e2e, f"wd_{name}")
    # Keep the workdir across retries so augment-e2e RESUMES (reuses already-completed
    # categorize-proposal chunks + tag chunks) instead of restarting from scratch. The
    # skill validates each cached chunk (parse + index coverage) and redoes corrupt ones.
    log = os.path.join(e2e, f"augment_{name}.log")
    aug_raw = os.path.join(e2e, f"augment_{name}.raw.csv")
    cmd = [PY, "-u", TAPP, "augment-e2e",
           "--input", aug_input, "--workdir", wd,
           "--query", QUERIES[ds], "--model", model,
           "--output", aug_raw, "--attempts", "3",
           "--allow-low-coverage-fallback", "--max-workers", str(TAPP_WORKERS),
           "--categorize-chunk-size", "300",
           "--tag-chunk-size", "150"]  # Larger chunks for speed (user 2026-07-22); skill subchunk fallback handles token limits
    print(f"  $ augment-e2e {ds}/{name} (model={model}, target '{tgt}' hidden={strip_tgt})", flush=True)
    with open(log, "w", encoding="utf-8") as lf:
        r = subprocess.run(cmd, env=ENV, cwd=REPO, stdout=lf,
                           stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 or not os.path.exists(aug_raw):
        raise RuntimeError(f"augment-e2e rc={r.returncode}; see {log}")

    # Re-attach the target column (row-position aligned) for downstream eval.
    out_df = pd.read_csv(aug_raw)
    if strip_tgt and tgt not in out_df.columns:
        if len(out_df) != len(data_df):
            raise RuntimeError(
                f"row-count mismatch after augment ({len(out_df)} vs {len(data_df)}); cannot re-attach target")
        out_df[tgt] = data_df[tgt].values
    out_df.to_csv(aug_csv, index=False)
    print(f"  [OK augment] {aug_csv}", flush=True)
    return aug_csv


def do(ds, mtag, model):
    name = f"{mtag}{VARIANT}"
    print(f"\n=== {ds} / {name} ===", flush=True)
    e2e = os.path.join(OUT, ds, "skill_on_e2e")
    text_out = os.path.join(e2e, f"xgb_results_{ds}_text_skrub_shap_{name}.json")
    notext_out = os.path.join(e2e, f"xgb_results_{ds}_no_text_{name}.json")
    if os.path.exists(text_out) and os.path.exists(notext_out):
        print("  [skip] both results exist", flush=True)
        return

    aug_csv = augment(ds, mtag, model)
    tag = f"{ds}_e2e_{name}"
    tag_nt = f"{ds}_e2e_{name}_nt"

    if not os.path.exists(os.path.join(embed_dir(ds, tag), "skrub_text_embeddings.npy")):
        run_pipe(["--dataset", ds, "--custom_csv", aug_csv, "--custom_tag", tag,
                  "--embed_methods", "skrub", "--generate_embeddings"])
    if not os.path.exists(os.path.join(embed_dir(ds, tag_nt), "skrub_text_embeddings.npy")):
        shutil.copytree(embed_dir(ds, tag), embed_dir(ds, tag_nt), dirs_exist_ok=True)

    if not os.path.exists(text_out):
        run_pipe(["--dataset", ds, "--custom_csv", aug_csv, "--custom_tag", tag,
                  "--embed_methods", "skrub", "--eval_method", "xgb",
                  "--downsample_methods", "shap", "--run_pipe"])
        shutil.move(os.path.join(REPO, f"xgb_results_{ds}__{tag}.json"), text_out)
        print(f"  [OK] text -> {text_out}", flush=True)

    if not os.path.exists(notext_out):
        run_pipe(["--dataset", ds, "--custom_csv", aug_csv, "--custom_tag", tag_nt,
                  "--embed_methods", "skrub", "--eval_method", "xgb",
                  "--downsample_methods", "shap", "--run_pipe", "--no_text"])
        shutil.move(os.path.join(REPO, f"xgb_results_{ds}__{tag_nt}.json"), notext_out)
        print(f"  [OK] no_text -> {notext_out}", flush=True)


def _acquire_singleton_lock():
    """Ensure only ONE runner instance runs at a time (ends the duplicate-race problem).

    Atomic O_EXCL create of a lock file holding this PID. If the lock is already held
    by a LIVE process -> this instance exits immediately. A stale lock (holder dead) is
    reclaimed. So no matter how many times the runner is launched, only one runs.
    """
    import atexit
    lock = os.path.join(OUT, "_logs", "runner.lock")
    os.makedirs(os.path.dirname(lock), exist_ok=True)

    def _alive(p):
        try:
            os.kill(int(p), 0)
            return True
        except (ProcessLookupError, ValueError):
            return False
        except PermissionError:
            return True

    for _ in range(3):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            atexit.register(lambda: os.remove(lock) if os.path.exists(lock) else None)
            print(f"[lock] acquired singleton lock (PID {os.getpid()}).", flush=True)
            return
        except FileExistsError:
            try:
                holder = open(lock).read().strip()
            except Exception:
                holder = ""
            if holder and holder != str(os.getpid()) and _alive(holder):
                print(f"[lock] another runner (PID {holder}) is active; this instance exits.", flush=True)
                sys.exit(0)
            try:
                os.remove(lock)  # stale lock, reclaim
            except Exception:
                pass
    print("[lock] could not acquire lock; exiting.", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    _acquire_singleton_lock()
    from concurrent.futures import ThreadPoolExecutor, as_completed
    args = sys.argv[1:]
    # outer parallelism: how many (dataset, model) jobs run at once.
    # total concurrent proxy calls ~= JOBS * TAPP_WORKERS -> keep modest for rate limits.
    jobs = int(os.environ.get("JOBS", "1"))
    if "--jobs" in args:
        i = args.index("--jobs"); jobs = int(args[i + 1]); del args[i:i + 2]
    max_passes = int(os.environ.get("MAX_PASSES", "5"))
    ds_args = [a for a in args if a in DATASETS]
    m_args = [a for a in args if a in MODELS]
    # A default run (no dataset arg) skips RUN_LAST datasets (e.g. sf_permits); those are
    # launched explicitly by name in a separate phase with their own concurrency.
    targets = ds_args or [d for d in DATASETS if d not in RUN_LAST]
    models = m_args or list(MODELS.keys())
    all_pairs = [(ds, mtag) for ds in targets for mtag in models]

    def _pair_done(ds, mtag):
        e2e = os.path.join(OUT, ds, "skill_on_e2e")
        name = f"{mtag}{VARIANT}"
        return (os.path.exists(os.path.join(e2e, f"xgb_results_{ds}_text_skrub_shap_{name}.json"))
                and os.path.exists(os.path.join(e2e, f"xgb_results_{ds}_no_text_{name}.json")))

    # Work-queue with IMMEDIATE auto-retry: the moment a pair fails it is re-queued and
    # picked up by the freed worker slot (resuming from its on-disk checkpoint) instead of
    # waiting for a whole new pass to come around. Per-pair attempts are capped at max_passes.
    from concurrent.futures import wait, FIRST_COMPLETED

    def _run_pool(pairs):
        pairs = [p for p in pairs if not _pair_done(*p)]
        if not pairs:
            return
        attempts: dict = {}
        backlog = list(pairs)
        futs: dict = {}
        with ThreadPoolExecutor(max_workers=jobs) as ex:
            def _fill():
                while backlog and len(futs) < jobs:
                    p = backlog.pop(0)
                    attempts[p] = attempts.get(p, 0) + 1
                    futs[ex.submit(do, p[0], p[1], MODELS[p[1]])] = p
            _fill()
            while futs:
                done, _ = wait(list(futs), return_when=FIRST_COMPLETED)
                for fut in done:
                    p = futs.pop(fut)
                    try:
                        fut.result()
                        print(f"  [pair-done] {p[0]}/{p[1]}", flush=True)
                    except Exception as e:
                        n = attempts.get(p, 0)
                        if not _pair_done(*p) and n < max_passes:
                            print(f"  [FAIL->retry] {p[0]}/{p[1]} attempt {n} failed: {e} "
                                  f"| requeueing NOW (resume from checkpoint)", flush=True)
                            backlog.insert(0, p)   # retry ASAP in the freed slot
                        else:
                            print(f"  [GIVE-UP] {p[0]}/{p[1]} after {n} attempts: {e}", flush=True)
                _fill()

    # RUN_LAST datasets (e.g. sf_permits) run only after everything else is done.
    pending_all = [(ds, m) for ds, m in all_pairs if not _pair_done(ds, m)]
    non_last = [(ds, m) for ds, m in pending_all if ds not in RUN_LAST]
    last = [(ds, m) for ds, m in pending_all if ds in RUN_LAST]
    print(f"[start] {len(pending_all)} not-done | jobs={jobs} | tag-workers={TAPP_WORKERS} "
          f"| ~{jobs * int(TAPP_WORKERS)} concurrent proxy calls | immediate auto-retry (cap {max_passes})",
          flush=True)
    if non_last:
        _run_pool(non_last)
    if last:
        print(f"[run-last] {len(last)} RUN_LAST pair(s): {[f'{d}/{m}' for d, m in last]}", flush=True)
        _run_pool(last)
    print("\n==== RUNNER DONE ====", flush=True)
