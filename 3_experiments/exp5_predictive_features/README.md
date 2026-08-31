# Experiment 5 — Predictive Feature Engineering

**Paper: Tables 5 and 6.** Five-fold cross-validated XGBoost, mean±std across
folds, over 11 TextTabBench datasets. Table 5 uses no text embedding; Table 6
adds a Skrub `GapEncoder` embedding of the raw text column, downsampled to its 64
most important dimensions by SHAP in every condition. Metric is $R^2$ for
regression and accuracy for classification. **110 mean/std pairs,
machine-verified.**

This is the one experiment with a downstream task metric rather than a judge: do
the augmented columns actually predict better? The `baseline` uses the
non-textual columns only; every other condition retains all of its structured
and augmented columns.

## What is here

| | |
|---|---|
| **Prompt** | `prompts/baseline_augmentation.md` — the `skill_off` augmentation instruction |
| **Code** | `../../4_code/TextTabBench/augment_process_result_v11_update/run_skilloff_augment.py`, `skilloff_augment.py` — the baseline augmentation |
| | `../../4_code/TextTabBench/augment_process_result_v11_update/run_skillon_e2e_linux.py` — the SADA augmentation |
| | `../../4_code/TextTabBench/augment_process_result_v11_update/eval_5seed.py` — the five-fold evaluation |
| | `../../4_code/TextTabBench/augment_process_result_v11_update/rerun_k64.py`, `rebuild_summary_k64.py` — the SHAP top-64 rerun |
| | `../../4_code/TextTabBench/pipelines/embedd_text.py` — the Skrub embedding |
| | `../../4_code/TextTabBench/pipelines/feature_selection.py` — per-fold SHAP selection |
| | `../../4_code/TextTabBench/pipelines/main_pipeline.py`, `evaluation.py`, `row_downsampling.py`, `download_datasets.py` — the upstream pipeline |
| **Operator** | `../../2_operator/` — invoked by `run_skillon_e2e_linux.py` |
| **Raw** | `raw/xgboost/xgb_results_<dataset>[_variant].json` — per-fold metrics per dataset and condition |
| | `raw/_rerun_k64_log.txt` — the k=64 rerun log |
| **Tables** | `tables/table5_no_text.csv` — Table 5, regenerated |
| | `tables/table6_text_k64.csv` — Table 6, regenerated |
| | `tables/summary_v11_update.csv`, `summary_v11_update_k64.csv` — the full summaries the tables are cut from |

## Scope

- 11 datasets: `airbnb`, `beer`, `laptops`, `sf_permits`, `wine`,
  `customer_complaints`, `hs_cards`, `job_frauds`, `kickstarter`,
  `osha_accidents`, `spotify`.
- `mercari` is **excluded**.
- Table 6 uses the SHAP top-k=64 JSON, not the full embedding.

All three are recorded in `../../5_reference/configs/experiment_scope.json`.

## Upstream dependency

The dataset pool, task definitions, download procedure and processed-dataset
format come from [TextTabBench](https://github.com/mrazmartin/TextTabBench). This
project adds the SADA and skill-off augmentation, target hiding and
re-attachment, the five-fold XGBoost evaluation, the Skrub embedding, the
per-fold SHAP top-64 selection, and the summarization code.

The source data is **not redistributed** — see `../../5_reference/data/README.md`
and `../../THIRD_PARTY.md`. The exact upstream commit used at run time cannot be
asserted because the original checkout did not retain `.git` metadata;
`../../5_reference/configs/upstream_sources.json` records what is and is not
known.

## How the 110 numbers are rebuilt

`../../1_verify/reproduce_paper_results.py` reads the per-fold metrics from
`raw/xgboost/`, computes mean and std across the five folds per (dataset,
condition), and compares against the paper's cells. Verify with:

```bash
../../1_verify/verify_all.sh
```
