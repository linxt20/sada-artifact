"""Agentic (skill-off) augmentation: give the substrate model ONLY the table, the
natural-language query, and a working directory with tools -- no schema/label
prompt split, no chunking, no retry policy, no output contract beyond "produce
augment.csv".

Unlike ``run_skill_off_query_only_augment.py`` (which hand-implements a two-stage
propose-schema-then-label pipeline on the model's behalf), this variant hands the
model the whole job. It must decide on its own whether to split schema induction
from row labelling, how to chunk 500+ rows, whether to write code or label by
hand, and how to keep column definitions constant across the table.

This isolates the value of the SKILL AS AN OPERATOR rather than the value of its
prompt text: skill-v11's SKILL.md Boundary Rule assigns pipeline decisions
(chunk sizes, retries, spec normalisation, row-index filling) to the skill, so a
runner-provided pipeline is a runner-provided piece of that capability.

Failure IS a result. Scenarios where the agent produces no augment.csv, drops
rows, or emits inconsistent columns are recorded with a diagnosis rather than
silently retried -- see ``_verdict``.

Output goes to a NEW subfolder, leaving all existing variants untouched::

    augment_table/<dataset>/<scenario>/_agentic/<model>/
        input.csv         # copy of original.csv (the agent's only data input)
        augment.csv       # the agent's deliverable (may be absent -> FAIL)
        _prompt.txt       # exact prompt sent
        _session.json     # raw claude CLI json output (transcript + cost)
        _verdict.json     # mechanical check of the deliverable

Usage::

    python3 augmenter/run_skill_off_agentic_augment.py --pilot
    python3 augmenter/run_skill_off_agentic_augment.py --scenario flag_6/focus_inference
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scorer"))
import semantic_reference_recall as semrec  # noqa: E402

AUG_TABLE = ROOT / "augment_table"
GT_DIR = ROOT / "gt_annotations"

# 10 scenarios covering all 6 subtypes, 202-943 rows.
# Deliberately includes 3 scenarios whose GT the QC audit flagged, so the pilot
# also tells us whether a free agent reproduces the same degenerate columns.
PILOT: list[tuple[str, str]] = [
    ("airlines_review", "causal_qatar_business"),            # causal_attribution, 608
    ("flag_20", "causal_declined"),                          # causal_attribution, 500
    ("flag_28", "eda_achievement"),                          # eda, 550  (GT has a 1.0-constant col)
    ("healthcare_visit_notes", "eda_duration"),              # eda, 250
    ("airlines_review", "concept_key_focus_points"),         # faceted_decomposition, 943
    ("education_survey_responses", "concept_attribute_needs"),  # faceted_decomposition, 250
    ("flag_6", "focus_inference"),                           # focus_inference, 500 (GT 95% Unknown)
    ("company_profile_location", "concept_attribute_focus"), # focus_inference, 202
    ("flag_9", "predictive_hardware"),                       # predictive_feature_engineering, 600
    ("imdb_movie_reviews", "whatif_complaints"),             # what_if, 250
]

MODELS = ["substrate-claude-haiku-4-5", "substrate-claude-sonnet-4-6"]

ALLOWED_TOOLS = "Read,Write,Edit,Glob,Grep,Bash"


def _query_text(dataset: str, scenario: str) -> str:
    """Return ONLY the NL query text from the GT package (no other GT fields)."""
    for name in (dataset, dataset.replace("_", "-")):
        p = GT_DIR / name / "augmentations" / scenario / "GT.json"
        if p.exists():
            return str((semrec._read_json(p).get("query") or {}).get("text") or "").strip()
    return ""


def _agent_prompt(query: str, csv_hygiene: bool = False) -> str:
    """The whole task, stated once. No pipeline, no schema contract, no rules
    about what makes a good column -- only the deliverable and its format.

    Deliberately does NOT state the row count: ``input.csv`` is right there, and
    reading it is part of the job. Stating it would also be actively misleading
    on tables whose text cells contain newlines, where ``wc -l`` and the record
    count disagree (e.g. concept_key_focus_points: 943 lines, 900 records).

    ``csv_hygiene`` adds one extra requirement about quoting/escaping. It is OFF
    for the corpus run and must be recorded per-run wherever it is used: the
    prompt is then no longer identical across scenarios. Like the other
    requirements it constrains only the deliverable's format (is the file valid
    CSV), not what the new columns should be, so it does not leak any of the
    skill's analytical guidance."""
    hygiene = (
        "- It must be valid CSV: any field containing a comma, a quote character, "
        "or a newline must be quoted and escaped accordingly.\n"
        if csv_hygiene else ""
    )
    return (
        "You are working in the current directory.\n\n"
        "`input.csv` is a table.\n\n"
        f"Analytical query:\n{query}\n\n"
        "Task: add new columns to this table so that it can help answer that query, "
        "and write the result to `augment.csv` in this directory.\n\n"
        "Requirements for `augment.csv`:\n"
        "- It must contain all original rows, in their original order, "
        "with all original columns unchanged.\n"
        "- It must contain at least one new column beyond the original ones.\n"
        "- Every new column must have a value for every row.\n"
        f"{hygiene}"
        "\n"
        "Everything else -- what the new columns are, how you determine their "
        "values, and how you go about it -- is your decision.\n\n"
        "When you are done, reply with a one-paragraph summary of what you added and why."
    )


def _invoke_agent(prompt: str, *, model: str, cwd: Path, timeout_s: int) -> dict[str, Any]:
    """Run the claude CLI as an agent with tools, rooted at ``cwd``.

    Differs from ``semrec._invoke_judge`` in two ways that matter: no
    ``CLAUDE_CODE_SIMPLE`` (which disables tools), and ``cwd`` is the scenario
    workdir so the agent can only see its own input.
    """
    cmd = [
        semrec._find_claude(),
        "-p",
        "--no-session-persistence",
        "--permission-mode",
        "bypassPermissions",
        "--allowed-tools",
        ALLOWED_TOOLS,
        "--output-format",
        "json",
        "--model",
        model,
    ]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env.pop("CLAUDE_CODE_SIMPLE", None)

    started = time.time()
    try:
        proc = subprocess.run(
            cmd,
            input=prompt,
            cwd=str(cwd),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_s,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {"_error": f"timeout after {timeout_s}s", "_elapsed_s": time.time() - started}

    elapsed = time.time() - started
    out: dict[str, Any] = {"_elapsed_s": round(elapsed, 1), "_returncode": proc.returncode}
    try:
        payload = json.loads(proc.stdout or "")
        if isinstance(payload, dict):
            out.update(payload)
    except Exception:
        out["_stdout_raw"] = (proc.stdout or "")[:20000]
    if proc.returncode != 0:
        out["_stderr"] = (proc.stderr or "")[:4000]
    return out


def _verdict(work: Path, src: pd.DataFrame) -> dict[str, Any]:
    """Mechanically check the deliverable. No repair, no retry -- this is the
    measurement."""
    out = work / "augment.csv"
    v: dict[str, Any] = {"produced": out.exists()}
    if not out.exists():
        v["status"] = "FAIL_NO_OUTPUT"
        return v

    try:
        aug = pd.read_csv(out, dtype=str, keep_default_na=False)
    except Exception as exc:
        v["status"] = "FAIL_UNREADABLE"
        v["error"] = str(exc)[:500]
        return v

    orig_cols = [str(c) for c in src.columns]
    aug_cols = [str(c) for c in aug.columns]
    new_cols = [c for c in aug_cols if c not in orig_cols]
    missing = [c for c in orig_cols if c not in aug_cols]

    v.update({
        "n_rows_expected": int(len(src)),
        "n_rows_actual": int(len(aug)),
        "rows_match": int(len(aug)) == int(len(src)),
        "original_cols_preserved": not missing,
        "missing_original_cols": missing,
        "n_new_cols": len(new_cols),
        "new_cols": new_cols,
    })

    # Per-new-column fill + degeneracy, mirroring the GT QC checks so the two are
    # directly comparable.
    stats = {}
    for c in new_cols:
        s = aug[c].astype(str).str.strip()
        blank = s.isin(["", "nan", "None", "NaN", "null"])
        nonblank = s[~blank]
        top = float(nonblank.value_counts(normalize=True).iloc[0]) if len(nonblank) else 1.0
        stats[c] = {
            "blank_rate": round(float(blank.mean()), 3),
            "n_distinct": int(nonblank.nunique()),
            "top_value_share": round(top, 3),
        }
    v["column_stats"] = stats

    if not v["rows_match"]:
        v["status"] = "FAIL_ROW_COUNT"
    elif missing:
        v["status"] = "FAIL_DROPPED_ORIGINAL_COLS"
    elif not new_cols:
        v["status"] = "FAIL_NO_NEW_COLS"
    elif any(st["blank_rate"] > 0.001 for st in stats.values()):
        v["status"] = "PARTIAL_INCOMPLETE_FILL"
    else:
        v["status"] = "OK"
    return v


def _publish(work: Path, sc_dir: Path, model: str, verdict: dict[str, Any]) -> str | None:
    """Copy a usable deliverable up to the scenario dir as
    ``<short_model>__skill_off_update.csv``, alongside the other variants.

    Only OK / PARTIAL_INCOMPLETE_FILL are published: those are real augmentation
    attempts whose columns can be scored. Structural failures (no output, wrong
    row count, dropped original columns) are left in ``_agentic/`` only, so a
    broken table never silently enters the evaluation set."""
    if verdict.get("status") not in {"OK", "PARTIAL_INCOMPLETE_FILL"}:
        return None
    src = work / "augment.csv"
    if not src.exists():
        return None
    short = model.replace("substrate-claude-", "").replace("-4-5", "").replace("-4-6", "")
    dst = sc_dir / f"{short}__skill_off_update.csv"
    shutil.copyfile(src, dst)
    return dst.name


def _run_one(dataset: str, scenario: str, model: str, args: argparse.Namespace) -> dict[str, Any]:
    sc_dir = AUG_TABLE / dataset / scenario
    original = sc_dir / "original.csv"
    tag = f"{dataset}/{scenario} [{model.replace('substrate-claude-', '')}]"
    if not original.exists():
        return {"dataset": dataset, "scenario": scenario, "model": model,
                "status": "SKIP_NO_INPUT", "path": str(original)}

    query = _query_text(dataset, scenario)
    if not query:
        return {"dataset": dataset, "scenario": scenario, "model": model, "status": "SKIP_NO_QUERY"}

    work = sc_dir / "_agentic" / model
    work.mkdir(parents=True, exist_ok=True)

    src = pd.read_csv(original, dtype=str, keep_default_na=False)
    shutil.copyfile(original, work / "input.csv")

    if (work / "augment.csv").exists() and not args.force:
        v = _verdict(work, src)
        _publish(work, sc_dir, model, v)
        print(f"  [cached] {tag} -> {v['status']}", flush=True)
        return {"dataset": dataset, "scenario": scenario, "model": model, "cached": True, **v}

    prompt = _agent_prompt(query, csv_hygiene=args.csv_hygiene)
    (work / "_prompt.txt").write_text(prompt, encoding="utf-8")

    print(f"  [run] {tag} ({len(src)} rows)", flush=True)
    session = _invoke_agent(prompt, model=model, cwd=work, timeout_s=args.timeout)
    (work / "_session.json").write_text(json.dumps(session, ensure_ascii=False, indent=2), encoding="utf-8")

    v = _verdict(work, src)
    v["elapsed_s"] = session.get("_elapsed_s")
    v["cost_usd"] = session.get("total_cost_usd")
    v["num_turns"] = session.get("num_turns")
    v["csv_hygiene_hint"] = bool(args.csv_hygiene)
    if session.get("_error"):
        v["agent_error"] = session["_error"]
        if v["status"] == "FAIL_NO_OUTPUT":
            v["status"] = "FAIL_TIMEOUT"
    (work / "_verdict.json").write_text(json.dumps(v, ensure_ascii=False, indent=2), encoding="utf-8")
    _publish(work, sc_dir, model, v)

    print(f"  [done] {tag} -> {v['status']}  ({v.get('elapsed_s')}s, ${v.get('cost_usd')})", flush=True)
    return {"dataset": dataset, "scenario": scenario, "model": model, **v}


def _all_scenarios() -> list[tuple[str, str]]:
    """Every scenario in augment_table that has both an original.csv and a GT query."""
    pairs = []
    for ds_dir in sorted(AUG_TABLE.iterdir()):
        if not ds_dir.is_dir():
            continue
        for sc_dir in sorted(ds_dir.iterdir()):
            if sc_dir.is_dir() and (sc_dir / "original.csv").exists():
                pairs.append((ds_dir.name, sc_dir.name))
    return pairs


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--all", action="store_true", help="run every scenario in augment_table")
    p.add_argument("--pilot", action="store_true", help="run the 10-scenario pilot set")
    p.add_argument("--scenario", action="append", default=None,
                   help="dataset/scenario, repeatable")
    p.add_argument("--model", action="append", default=None)
    p.add_argument("--workers", type=int, default=4, help="agent runs in parallel")
    p.add_argument("--timeout", type=int, default=2400, help="per-run wall clock (s)")
    p.add_argument("--force", action="store_true", help="rerun even if augment.csv exists")
    p.add_argument("--csv-hygiene", action="store_true",
                   help="add an explicit CSV quoting/escaping requirement to the prompt. "
                        "OFF for the corpus run; recorded per-run as csv_hygiene_hint.")
    p.add_argument("--out", default=str(ROOT / "_agentic_pilot_result.json"))
    args = p.parse_args()

    if args.scenario:
        pairs = [tuple(s.split("/", 1)) for s in args.scenario]
    elif args.all:
        pairs = _all_scenarios()
    elif args.pilot:
        pairs = PILOT
    else:
        p.error("pass --all, --pilot, or --scenario dataset/scenario")

    models = args.model or MODELS
    jobs = [(d, s, m) for d, s in pairs for m in models]
    print(f"agentic skill-off: {len(pairs)} scenarios x {len(models)} models = {len(jobs)} runs", flush=True)

    results: list[dict[str, Any]] = []
    with futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(_run_one, d, s, m, args): (d, s, m) for d, s, m in jobs}
        for f in futures.as_completed(futs):
            d, s, m = futs[f]
            try:
                results.append(f.result())
            except Exception as exc:
                print(f"  [error] {d}/{s} [{m}]: {exc}", flush=True)
                results.append({"dataset": d, "scenario": s, "model": m,
                                "status": "FAIL_RUNNER_EXCEPTION", "error": str(exc)[:500]})

    Path(args.out).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    import collections
    tally = collections.Counter(r.get("status") for r in results)
    print("\n=== status tally ===", flush=True)
    for k, n in tally.most_common():
        print(f"  {k:32s} {n}", flush=True)
    published = len(list(AUG_TABLE.glob("*/*/*__skill_off_update.csv")))
    cost = sum(r.get("cost_usd") or 0 for r in results)
    print(f"\npublished skill_off_update.csv: {published}", flush=True)
    print(f"total cost: ${cost:.2f}", flush=True)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
