# Experiment 1 — End-to-End Analysis Utility

**Paper: Table 2.** Mean swap-stabilized Bradley–Terry scores over the four
conditions (`original`, `skill_off`, `skill_on`, `skill_on_e2e`), each row
aggregating all 108 analysis units under one substrate.
**8 values, machine-verified.**

The question: given the same analytical request, does the analysis produced on a
SADA-augmented table beat the analysis produced on the raw table and on a
generically augmented table? A fixed judge grades reports pairwise; the pairwise
outcomes are fitted to a Bradley–Terry model.

## What is here

| | |
|---|---|
| **Prompts** | `prompts/analyst_prompt_all_conditions.md` — the single prompt shared by `original`, `skill_off` and `skill_on`, so the analyst is never told which columns were added |
| | `prompts/analyst_prompt_skill_on_e2e.md` — the one condition that is told an augmentation happened |
| | `prompts/judge_pairwise_report_grading.md` — the judge (appendix D.1) |
| **Code** | `../../4_code/benchmark/gen_update_reports.py` — generates the reports |
| | `../../4_code/benchmark/gen_augment_table_reports.py` — owns both analyst prompts and the Claude-CLI plumbing |
| | `../../4_code/benchmark/grade_bt_update.py` — runs the pairwise judging and the BT fit |
| | `../../4_code/benchmark/score_semantic_recall/grader_v3.py` — the judge prompt and BT implementation |
| **Raw** | `raw/analysis_reports/` — every generated report, per substrate × dataset × unit × condition |
| | `raw/bt/` — per-unit `bt_4way.json` (the fitted scores) and `meta.json`, plus the pairwise verdicts |
| | `raw/supplemental_analysis_report/` — additional reports not aggregated into Table 2 |
| **Tables** | `tables/exp1_bt.csv` — Table 2, regenerated, with per-cell PASS status |
| | `tables/SCORE_SUMMARY_exp1_exp2.md` — the rubric-dimension detail behind the BT scores |

`raw/analysis_reports/` is also **Experiment 2's input**: Experiment 2 classifies
these same reports rather than generating new ones.

## Scope

`airlines_review_full` is excluded — it was added to the pool after this
experiment ran. See `../../5_reference/configs/experiment_scope.json`.

## How the 8 numbers are rebuilt

`../../1_verify/reproduce_paper_results.py` walks `raw/bt/**/bt_4way.json`,
drops the excluded dataset, reads each unit's substrate from the sibling
`meta.json`, and averages the per-unit BT score per (substrate, condition). The
result is compared against the values printed in Table 2.

The judge is never re-invoked. Verify with:

```bash
../../1_verify/verify_all.sh
```
