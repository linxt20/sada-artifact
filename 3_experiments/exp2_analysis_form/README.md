# Experiment 2 — The Form of the Resulting Analysis

**Paper: Table 3.** Distribution of analysis form per condition, as a percentage
of reports (rows sum to 100). C3 — text-augmented quantification — is the target
form. **24 values, machine-verified.**

The question is not whether the analysis is *better* but whether it is a
*different kind* of analysis. C1 is entirely qualitative, C2 quantifies only the
pre-existing numeric columns while treating text qualitatively, and C3 quantifies
over variables derived from the text. A fixed judge assigns each report to one
of the three.

## What is here

| | |
|---|---|
| **Prompt** | `prompts/judge_analytical_form_classification.md` — the judge (appendix D.2) |
| **Code** | `../../4_code/benchmark/classify_form_update.py` — owns the prompt and runs the classification |
| **Raw** | `raw/form_class/` — one JSON per report, carrying `dataset`, `model`, `variant` and the assigned `category` |
| **Tables** | `tables/exp2_form.csv` — Table 3, regenerated, with per-row PASS status |

**Input reports:** this experiment does not generate reports. It classifies the
ones in `../exp1_end_to_end_utility/raw/analysis_reports/`, so Tables 2 and 3
describe the same corpus under two different measurements. The analyst prompts
that produced them are documented in
`../exp1_end_to_end_utility/prompts/`.

The rubric-dimension summary shared with Experiment 1 is at
`../exp1_end_to_end_utility/tables/SCORE_SUMMARY_exp1_exp2.md`.

## Scope

`airlines_review_full` is excluded, matching Experiments 1 and 3. See
`../../5_reference/configs/experiment_scope.json`.

## How the 24 numbers are rebuilt

`../../1_verify/reproduce_paper_results.py` counts the assigned categories per
(substrate, condition) over `raw/form_class/**/*.json`, drops the excluded
dataset, and converts the counts to row percentages at one decimal. Verify with:

```bash
../../1_verify/verify_all.sh
```
