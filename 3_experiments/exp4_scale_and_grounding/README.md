# Experiment 4 — Semantic Augmentation at Scale

**Paper: §5.5 prose.** This experiment's table (`tab:scale`) is commented out in
the current draft, so its numbers appear inline in the text: 471,200 audited
cells; hallucination falling from 12.98% to 10.29% on Haiku and from 24.29% to
5.47% on Sonnet; 8 of 9 baseline scripts assigning semantic columns by keyword
or regex. **18 grounding percentages, machine-verified.** The mechanism count is
verified by inspection rather than numerically.

Experiments 1–3 grade the augmented table through a judge that sees the schema
and a sample of values, but not *how* those values were produced. This experiment
opens that box on the largest table in the pool: the 10,000-row
`amazon_fine_food_review` corpus, an order of magnitude beyond the median unit.

## What is here

| | |
|---|---|
| **Queries** | `../../5_reference/configs/grounding_queries.json` — the analysis units, including the 7 on this table |
| **Prompts** | `prompts/baseline_agentic_augmentation.md` — the whole `skill_off` instruction. It constrains only the CSV format, never what the columns should be |
| | `prompts/judge_row_level_grounding.md` — the grounding auditor (appendix D.4) |
| **Code** | `../../4_code/benchmark/augmenter/run_skill_off_agentic_augment.py` — the baseline augmenter |
| | `../../4_code/benchmark/grounding_eval/run_grounding.py`, `col_stats.py` — the audit driver |
| | `../../4_code/benchmark/scorer_grounding/_g_judge.py` — the auditor prompt and row-alignment validation |
| **Operator** | `../../2_operator/` — the SADA side of the comparison |
| **Raw** | `raw/grounding/_cache/**/opus.jsonl.gz` — the per-cell verdicts, read directly by the verifier |
| | `raw/grounding/per_column.csv`, `per_table.csv` — the aggregates as produced at run time |
| | `raw/grounding/value_domain.jsonl` — the observed value domain per augmented column |
| | `raw/mechanism_artifacts/` — the Python scripts the `skill_off` conditions emitted |
| | `raw/tagging_traces/` — SADA's per-row LLM tagging traces, 15,058 files in 14 per-unit archives |
| | `raw/generation_logs/`, `raw/scoring_logs/` |
| **Tables** | `tables/exp4_grounding.csv` — the 6 conditions × (cells, supported, inferable, hallucinated) |

## The mechanism claim is checkable by direct inspection

`raw/mechanism_artifacts/` holds the scripts the baseline emitted: the sentiment
lexicons, facet dictionaries and `\b`-delimited pattern banks are visible in
them, and none contains a model call. `raw/tagging_traces/` holds SADA's per-row
tagging traces over the same table — the artifact the baseline has no counterpart
for. That contrast is the claim.

```bash
grep -rn "re\.\|lexicon\|POSITIVE_WORDS" raw/mechanism_artifacts/ | head
cd raw/tagging_traces && ./extract.sh     # optional; nothing needs unpacking
```

## Scope — read this before comparing against the paper

Grounding was audited on **3 of the 7 units** for `skill_off` and **2** for the
SADA variants. The reported percentages aggregate the **2 units common to all
conditions** (`experiment_4_common_units` in
`../../5_reference/configs/experiment_scope.json`), which is where the 471,200
cell count comes from. Over its full 3-unit coverage `skill_off` is 12.32%
(Haiku) and 24.09% (Sonnet), so the conclusion does not depend on this choice.

The paper's §5.5 prose says "over the 7 analysis units" when introducing the
experiment and then reports the cell count without restating that the grounding
audit covers 2 of them; the caveat paragraph that said so was commented out along
with the table. The scope above is what this directory contains.

## How the 18 numbers are rebuilt

`../../1_verify/reproduce_paper_results.py` streams the gzipped per-cell verdict
JSONL for the two common units, counts SUPPORTED / INFERABLE / HALLUCINATED per
condition, and converts to percentages of the condition's total cells. Verify
with:

```bash
../../1_verify/verify_all.sh
```
