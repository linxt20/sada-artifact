# Experiment 5 and TextTabBench

Experiment 5 builds on the dataset pool and preprocessing instructions from:

- Repository: <https://github.com/mrazmartin/TextTabBench>
- Paper: *Towards Benchmarking Foundation Models for Tabular Data With Text*,
  ICML 2025 Workshop on Foundation Models for Structured Data.

The original local checkout under `/mnt/data/TextTabBench` did not retain its
`.git` directory, so the exact upstream commit used when the experiment was run
cannot be recovered. On 2026-08-31, the public repository's `main`/`HEAD` was
observed at `773b69c2d5cc8d137852c25cdb763d7af26ec1df`. This observed commit is
recorded for reference only and must not be represented as the proven original
experiment commit.

## What came from TextTabBench

The experiment reused TextTabBench's:

- dataset collection and task definitions;
- download and notebook-based preprocessing instructions;
- processed dataset/config format;
- distinction between regression and classification tasks.

The upstream README instructs users to install its requirements and download
datasets with its downloader, for example:

```bash
python src/download_datasets/download_datasets.py \
  --task <reg-or-clf> --selection <dataset-name>
```

Some datasets have their own access terms. The upstream README specifically
notes Kaggle requirements for certain datasets. This artifact does not
redistribute those source datasets.

## Project-specific extensions

The following are SADA project additions rather than files found under the same
names in the observed public TextTabBench checkout:

- `augment_process_result_v11_update/run_skilloff_augment.py`
- `augment_process_result_v11_update/skilloff_augment.py`
- `augment_process_result_v11_update/run_skillon_e2e_linux.py`
- `augment_process_result_v11_update/eval_5seed.py`
- `augment_process_result_v11_update/rerun_k64.py`
- `augment_process_result_v11_update/rebuild_summary_k64.py`
- the files under `pipelines/`

These extensions implement target hiding and reattachment, generic and SADA
augmentation, the fixed XGBoost evaluation, Skrub text embeddings, fold-wise
SHAP feature selection, the top-64 embedding budget, and paper table assembly.

## Paper execution outline

With a complete upstream data checkout at `UPSTREAM_ROOT`:

```bash
# Generic LLM augmentation
UPSTREAM_ROOT=/path/to/repository \
  ../../scripts/run_baselines.sh exp5_skill_off

# SADA augmentation
UPSTREAM_ROOT=/path/to/repository \
  ../../scripts/run_method.sh exp5_augmentation

# Baseline/skill-off/skill-on XGBoost evaluation
UPSTREAM_ROOT=/path/to/repository \
  ../../scripts/run_method.sh exp5_evaluate baseline
UPSTREAM_ROOT=/path/to/repository \
  ../../scripts/run_method.sh exp5_evaluate skill_off
UPSTREAM_ROOT=/path/to/repository \
  ../../scripts/run_method.sh exp5_evaluate skill_on_e2e

# Text-embedding rerun with SHAP top-k=64
UPSTREAM_ROOT=/path/to/repository \
  ../../scripts/run_method.sh exp5_k64 64
```

The paper reports 11 datasets and excludes `mercari`. Tables 5 and 6 are
verified offline from the archived XGBoost JSON files by `1_verify/verify_all.sh`.

## Citation

```bibtex
@inproceedings{TextTabBench2024,
  title={Towards Benchmarking Foundation Models for Tabular Data With Text},
  author={Mraz, Das, Gupta and others},
  booktitle={ICML 2025 Workshop on Foundation Models for Structured Data (FMSD)},
  year={2025},
  url={https://openreview.net/pdf?id=yrmoQG9NAV}
}
```

No license file was present at the observed public repository head. Users must
obtain permission and comply with the upstream repository and dataset terms.
