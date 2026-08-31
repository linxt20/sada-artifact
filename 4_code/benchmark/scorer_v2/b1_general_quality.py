"""B-1: general augmentation quality (2 necessary-condition checks, no completeness).

Experiment B-1 (SADA_experiment_design_final.md)
-----------------------------------------------
Judge the augmented columns on two *necessary* conditions, scored one variant
at a time (no pairwise comparison, no reference schema):

  1. ``analytical_usefulness`` -- is the column useful for the FOLLOW-UP analysis?
  2. ``source_groundedness`` -- are the column VALUES derived from information that
     is actually present in the table (sound derivation, no hallucination)?

Column-name semantic relevance to the query is intentionally NOT judged here; that
signal is carried by B-2 characteristic adherence instead.

Explicitly **not** judged: completeness. We never ask "did it miss a relevant
column", because B-1 is a necessary-condition screen, not a recall measure.

Design notes
------------
* Judged **per column**, then averaged to the table level, so a table is not
  rewarded for adding one great column among many junk ones (and vice versa).
* ``source_groundedness`` is the only dimension where we show the judge actual
  ROW EVIDENCE: sampled (source-text, produced-value) pairs. Without rows the
  judge can only guess whether a value was hallucinated. This is the main
  methodological fix over the B-2-only scorers, which never look at cell values.
* Deliberately category-agnostic: B-1 asks the same three questions of every
  intent category. Category-specific instruction-following lives in B-2
  (``characteristic_adherence_v2.py``).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
SCORER_DIR = ROOT / "scorer"
CHAR_DIR = ROOT / "scorer_characteristic"
for _p in (str(SCORER_DIR), str(CHAR_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import semantic_reference_recall as semrec  # noqa: E402
import characteristic_adherence as charadh  # noqa: E402


DIMENSIONS = ("analytical_usefulness", "source_groundedness")


# --------------------------------------------------------------------------- #
# Row evidence: what the judge needs to tell derivation from hallucination
# --------------------------------------------------------------------------- #
def _text_source_columns(table: pd.DataFrame, source_columns: list[str], limit: int = 3) -> list[str]:
    """Pick the most text-rich ORIGINAL columns -- these are what an augmentation
    is supposed to have read in order to produce its values."""
    scored: list[tuple[float, str]] = []
    for col in source_columns:
        if col not in table.columns:
            continue
        series = table[col].dropna().astype(str)
        if series.empty:
            continue
        scored.append((series.str.len().mean(), col))
    scored.sort(reverse=True)
    return [c for _, c in scored[:limit]]


def build_row_evidence(
    table: pd.DataFrame,
    new_columns: list[str],
    source_columns: list[str],
    *,
    n_rows: int = 5,
    text_chars: int = 600,
) -> list[dict[str, Any]]:
    """Sample rows as {source_text: ..., produced_values: {col: value}}.

    Deterministic (head of the table) so re-runs are reproducible.
    """
    text_cols = _text_source_columns(table, source_columns)
    rows: list[dict[str, Any]] = []
    for _, row in table.head(n_rows).iterrows():
        source_text = {c: str(row[c])[:text_chars] for c in text_cols}
        produced = {c: (None if pd.isna(row[c]) else str(row[c])[:200]) for c in new_columns if c in table.columns}
        rows.append({"source_text": source_text, "produced_values": produced})
    return rows


# --------------------------------------------------------------------------- #
# Prompt
# --------------------------------------------------------------------------- #
def build_prompt(
    *,
    query: str,
    source_columns: list[str],
    columns_payload: list[dict[str, Any]],
    row_evidence: list[dict[str, Any]],
) -> str:
    task = {
        "analytical_query": query,
        "original_table_columns": source_columns,
        "added_columns": columns_payload,
        "row_evidence_samples": row_evidence,
    }
    return (
        "You are a strict evaluator of a text-to-table augmentation operator.\n"
        "An augmentation system read a text-rich table and ADDED the columns below, in order to help an "
        "analyst answer the analytical query. Judge the GENERAL QUALITY of these added columns on exactly "
        "two necessary conditions. Judge EACH added column independently, then give an overall verdict.\n\n"
        "THE TWO DIMENSIONS (score each 0-1, continuous):\n\n"
        "1. analytical_usefulness -- Would this column actually HELP the downstream analysis that the query "
        "calls for? Score low for columns that are: near-constant, trivially redundant with an existing "
        "original column, a mere restatement of another added column, or so generic (e.g. raw text length, "
        "token count, a bare positive/negative sentiment flag) that they add no analytical leverage for THIS "
        "query. Score high for columns that give a genuine new axis to group, compare, or model on.\n\n"
        "2. source_groundedness -- Are the column VALUES derivable from information ACTUALLY PRESENT in the "
        "table? Use 'row_evidence_samples': each sample pairs the original source text of a row with the "
        "values this augmentation produced for that row. Score high when the produced value is a sound "
        "reading of the source text (extraction, categorisation, or a clearly warranted inference). Score "
        "LOW when the value asserts something the source text does not support -- an invented fact, a "
        "confident specific where the text is silent, or a value that contradicts the text. A reasonable "
        "'unknown'/'not stated' value for a silent row is CORRECT behaviour and should NOT be penalised.\n\n"
        "CRITICAL SCOPE RULE: Do NOT judge COMPLETENESS. Never lower any score because some other relevant "
        "column is missing, because the set is too small, or because a better decomposition exists. You are "
        "screening the columns that ARE here against necessary conditions only.\n\n"
        "Also do not reward or penalise naming style, casing, or column ordering.\n\n"
        "Return strict JSON only:\n"
        "{\n"
        '  "per_column": [\n'
        '    {"name": "...", "analytical_usefulness": 0.0, '
        '"source_groundedness": 0.0, "hallucination_observed": false, "rationale": "..."}\n'
        "  ],\n"
        '  "analytical_usefulness": 0.0,   // table-level, holistic\n'
        '  "source_groundedness": 0.0,\n'
        '  "rationale": "..."\n'
        "}\n\n"
        f"Evaluation input JSON:\n{json.dumps(task, ensure_ascii=False, indent=2)}"
    )


# --------------------------------------------------------------------------- #
# Evaluate
# --------------------------------------------------------------------------- #
def evaluate(
    *,
    augment_table: pd.DataFrame,
    new_columns: list[str],
    specs_by_name: dict[str, dict[str, Any]],
    query: str,
    source_columns: list[str],
    judge_model: str,
    judge_timeout: int,
    attempts: int,
    log_path: Path,
    no_llm_judge: bool = False,
    n_evidence_rows: int = 5,
) -> dict[str, Any]:
    columns_payload = charadh._columns_payload(new_columns, specs_by_name, augment_table)
    row_evidence = (
        build_row_evidence(augment_table, new_columns, source_columns, n_rows=n_evidence_rows)
        if new_columns
        else []
    )

    if no_llm_judge or not new_columns:
        judge = {"per_column": [], "rationale": "no added columns or judge skipped"}
    else:
        prompt = build_prompt(
            query=query,
            source_columns=source_columns,
            columns_payload=columns_payload,
            row_evidence=row_evidence,
        )
        judge = semrec._invoke_judge(
            prompt, model=judge_model, timeout_s=judge_timeout, attempts=attempts, log_path=log_path
        )

    metrics = _metrics(judge, n_added=len(new_columns))
    return {
        "scorer": "B-1 general augmentation quality",
        "query": query,
        "n_added_columns": len(new_columns),
        "added_columns": new_columns,
        "n_evidence_rows": len(row_evidence),
        "metrics": metrics,
        "judge": judge,
    }


def _clip(value: Any) -> float:
    return round(max(0.0, min(1.0, charadh._f(value))), 4)


def _metrics(judge: dict[str, Any], *, n_added: int) -> dict[str, Any]:
    """Per-column means are the primary signal; table-level judge scores are kept
    as a secondary view. ``b1_overall`` is the mean of the three dimensions."""
    per = [c for c in (judge.get("per_column") or []) if isinstance(c, dict)]
    out: dict[str, Any] = {"n_added_columns": n_added, "n_judged_columns": len(per)}

    for dim in DIMENSIONS:
        col_scores = [_clip(c.get(dim)) for c in per if c.get(dim) is not None]
        out[dim] = round(sum(col_scores) / len(col_scores), 4) if col_scores else 0.0
        out[f"{dim}__table_level"] = _clip(judge.get(dim))

    out["b1_overall"] = round(sum(out[d] for d in DIMENSIONS) / len(DIMENSIONS), 4)
    out["hallucination_rate"] = (
        round(sum(1 for c in per if c.get("hallucination_observed")) / len(per), 4) if per else 0.0
    )
    return out


# --------------------------------------------------------------------------- #
# CLI (single table)
# --------------------------------------------------------------------------- #
def _main() -> int:
    parser = argparse.ArgumentParser(description="B-1 general quality evaluation of one augmented table.")
    parser.add_argument("--augment", required=True, type=Path)
    parser.add_argument("--specs", type=Path, default=None)
    parser.add_argument("--source", type=Path, default=None)
    parser.add_argument("--query", default="")
    parser.add_argument("--judge-model", default="claude-opus-4.8-xhigh")
    parser.add_argument("--judge-timeout", type=int, default=240)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--evidence-rows", type=int, default=5)
    parser.add_argument("--no-llm-judge", action="store_true")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    augment = semrec._read_table(args.augment).reset_index(drop=True)
    specs_payload = semrec._read_json(args.specs) if args.specs and args.specs.exists() else {}
    specs_by_name = {str(s.get("name")): s for s in (specs_payload.get("specs") or []) if s.get("name")}

    if specs_by_name:
        new_columns = [c for c in specs_by_name if c in augment.columns]
    elif args.source and args.source.exists():
        source = semrec._read_table(args.source)
        new_columns = semrec._source_new_columns(source, augment)
    else:
        new_columns = [str(c) for c in augment.columns]
    source_columns = [str(c) for c in augment.columns if str(c) not in set(map(str, new_columns))]

    report = evaluate(
        augment_table=augment,
        new_columns=[str(c) for c in new_columns],
        specs_by_name=specs_by_name,
        query=args.query,
        source_columns=source_columns,
        judge_model=args.judge_model,
        judge_timeout=args.judge_timeout,
        attempts=args.attempts,
        log_path=(args.out.parent if args.out else Path.cwd()) / "_b1_judge_call.json",
        no_llm_judge=args.no_llm_judge,
        n_evidence_rows=args.evidence_rows,
    )
    if args.out:
        semrec._write_json(args.out, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
