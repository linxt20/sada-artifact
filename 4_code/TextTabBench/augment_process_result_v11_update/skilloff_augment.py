#!/usr/bin/env python3
"""Naive skill-OFF augmenter (NO TA++ skill).

The whole point of "skill off": a model that never saw our skill just gets the
table + a plain query and is asked to add useful structured columns directly.
No evidence selection / visual preview / faceted decomposition / schema-then-tag /
closed vocabulary / merge validation. Just: rows in, augmented columns out.

Small tables -> one call. Larger tables are split into naive row-chunks ONLY because
of the ~32k output-token ceiling (a token limit, not methodology): each chunk is
independent (whole rows + the same query), the model decides its own columns per
chunk, and columns are UNIONed across chunks (missing -> NaN). Column inconsistency
across chunks is the honest cost of "no skill".

Per-chunk results are checkpointed to <workdir>/chunk_NNNN.json so a re-run resumes.
"""
import os, sys, json, math, subprocess
import pandas as pd

CLAUDE = os.environ.get("CLAUDE_BIN", "/root/.local/bin/claude")
ROWS_PER_CHUNK = int(os.environ.get("SKILLOFF_CHUNK", "300"))   # keep model output < ~32k tokens
CLAUDE_TIMEOUT = int(os.environ.get("SKILLOFF_CLAUDE_TIMEOUT", "900"))
ATTEMPTS = int(os.environ.get("SKILLOFF_ATTEMPTS", "3"))

PROMPT = """You are enriching a data table by deriving NEW STRUCTURED columns from its (mostly text) fields, to support this analysis goal:

{query}

Below is a batch of rows as JSON records. Each row has an "__row_id__" field that you MUST echo back unchanged so rows stay aligned.

Instructions:
- Invent a small set (roughly 6-12) of useful new structured columns derived ONLY from the visible fields: categorical tiers, boolean flags, ordinal buckets, or extracted numbers. Use concise snake_case names.
- Use the SAME set of new columns for EVERY row in this batch, with short, consistent values (a small closed set per column). Use "Unknown" when a value cannot be inferred.
- Do NOT copy or restate existing columns. Do NOT create any target/label/outcome column.
- Output ONLY a JSON array: one object per input row, each containing "__row_id__" plus your new columns. No prose, no markdown code fence.

ROWS (JSON records):
{rows_json}
"""


def _call_claude(model, prompt):
    cmd = [CLAUDE, "-p", "--no-session-persistence", "--permission-mode",
           "bypassPermissions", "--output-format", "json", "--model", model]
    env = dict(os.environ)
    env["IS_SANDBOX"] = "1"
    env.pop("CLAUDECODE", None)
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=CLAUDE_TIMEOUT, env=env)
    if r.returncode != 0:
        raise RuntimeError(f"claude rc={r.returncode}: {(r.stderr or '')[:300]}")
    try:
        wrap = json.loads(r.stdout)
        return wrap.get("result", r.stdout) if isinstance(wrap, dict) else r.stdout
    except Exception:
        return r.stdout


def _extract_array(text):
    t = text.strip()
    if "```" in t:
        seg = t.split("```")
        # take the longest fenced block
        cand = max(seg, key=len)
        t = cand[4:] if cand.lstrip().lower().startswith("json") else cand
    i, j = t.find("["), t.rfind("]")
    if i == -1 or j == -1 or j < i:
        raise ValueError("no JSON array in model output")
    return json.loads(t[i:j + 1])


def _augment_chunk(df_chunk, model, query):
    recs = df_chunk.to_dict(orient="records")
    prompt = PROMPT.format(query=query, rows_json=json.dumps(recs, ensure_ascii=False, default=str))
    last = None
    for _ in range(ATTEMPTS):
        try:
            arr = _extract_array(_call_claude(model, prompt))
            out = pd.DataFrame(arr)
            if "__row_id__" not in out.columns:
                raise ValueError("model dropped __row_id__")
            out["__row_id__"] = out["__row_id__"].astype(int)
            return out
        except Exception as e:
            last = e
    raise RuntimeError(f"chunk failed after {ATTEMPTS} attempts: {last}")


def free_augment(input_csv, model, query, out_csv, workdir, executor=None, df=None):
    """executor: optional shared ThreadPoolExecutor (global worker pool -> chunk-grain
    work-stealing). df: optional in-memory DataFrame to augment (PREFERRED - avoids CSV
    round-trip row drift from embedded newlines/quotes); falls back to reading input_csv.
    Per-chunk checkpoints make it safe & resumable either way."""
    os.makedirs(workdir, exist_ok=True)
    df = (df.copy() if df is not None else pd.read_csv(input_csv)).reset_index(drop=True)
    df = df.loc[:, ~df.columns.duplicated()]
    df["__row_id__"] = range(len(df))
    n = len(df)
    nchunks = max(1, math.ceil(n / ROWS_PER_CHUNK))

    def _do(ci):
        ckpt = os.path.join(workdir, f"chunk_{ci:04d}.json")
        if os.path.exists(ckpt) and os.path.getsize(ckpt) > 2:
            return ci, pd.read_json(ckpt)
        lo, hi = ci * ROWS_PER_CHUNK, min(n, (ci + 1) * ROWS_PER_CHUNK)
        out = _augment_chunk(df.iloc[lo:hi], model, query)
        out.to_json(ckpt, orient="records", force_ascii=False)
        return ci, out

    parts = [None] * nchunks
    if executor is not None and nchunks > 1:
        from concurrent.futures import as_completed
        futs = [executor.submit(_do, ci) for ci in range(nchunks)]
        for f in as_completed(futs):
            ci, out = f.result()
            parts[ci] = out
    else:
        for ci in range(nchunks):
            _, parts[ci] = _do(ci)
    for ci, out in enumerate(parts):
        print(f"  [skilloff] {os.path.basename(workdir)} chunk {ci+1}/{nchunks} cols={list(out.columns)}", flush=True)
    newcols = pd.concat(parts, ignore_index=True)
    # Robust row-alignment: coerce row ids to int, drop hallucinated/out-of-range/dup ids,
    # then REINDEX to exactly the original rows (extras dropped, missing -> NaN). Guarantees
    # output row count == input row count regardless of model over/under-production.
    newcols["__row_id__"] = pd.to_numeric(newcols["__row_id__"], errors="coerce")
    newcols = newcols.dropna(subset=["__row_id__"])
    newcols["__row_id__"] = newcols["__row_id__"].astype(int)
    newcols = newcols[(newcols["__row_id__"] >= 0) & (newcols["__row_id__"] < len(df))]
    newcols = newcols.drop_duplicates("__row_id__", keep="first")
    orig = set(df.columns)
    addcols = [c for c in newcols.columns if c not in orig]
    aligned = newcols.set_index("__row_id__")[addcols].reindex(range(len(df))).reset_index(drop=True)
    base = df.drop(columns=["__row_id__"]).reset_index(drop=True)
    merged = pd.concat([base, aligned], axis=1)
    merged.to_csv(out_csv, index=False)
    print(f"  [skilloff] wrote {out_csv} rows={len(merged)} (input {len(df)}) newcols={len(addcols)}", flush=True)
    return merged


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--query", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--workdir", required=True)
    a = ap.parse_args()
    free_augment(a.input, a.model, a.query, a.output, a.workdir)
    print("SKILLOFF_AUGMENT_OK", a.output)
