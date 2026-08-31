# Code

All runnable generation and scoring code, preserved as it ran. `benchmark/`
covers Experiments 1–4; `TextTabBench/` covers Experiment 5.

This is one tree rather than one directory per experiment because several modules
are shared and the archived scripts resolve them as siblings — splitting it would
mean rewriting import paths in code that is otherwise untouched. Each
experiment's `README.md` under `../3_experiments/` links the exact files it uses.

## Entry points per experiment

| Experiment | Files |
|---|---|
| Exp. 1 | `benchmark/gen_update_reports.py`, `benchmark/gen_augment_table_reports.py` (owns both analyst prompts), `benchmark/grade_bt_update.py`, `benchmark/score_semantic_recall/grader_v3.py` |
| Exp. 2 | `benchmark/classify_form_update.py` |
| Exp. 3 | `benchmark/run_v11_update.py`, `benchmark/scorer_v2/{run_scorer_v2,run_v11_update,b1_general_quality,b2_characteristic_adherence}.py` |
| Exp. 4 | `benchmark/augmenter/run_skill_off_agentic_augment.py`, `benchmark/grounding_eval/{run_grounding,col_stats}.py`, `benchmark/scorer_grounding/_g_judge.py` |
| Exp. 5 | `TextTabBench/augment_process_result_v11_update/`, `TextTabBench/pipelines/` |

## Shared modules

- `benchmark/scorer/` — the Claude-CLI invocation, table IO and JSON-extraction
  helpers. `scorer_v2/`, `grounding_eval/` and `augmenter/` all resolve it as
  `<parent>/scorer`.
- `benchmark/scorer_characteristic/` — rubric helpers imported by `scorer_v2` at
  module load time. Despite the historical name it is a live dependency of
  Experiment 3, not legacy code.
- `benchmark/score_semantic_recall/` — Experiment 1's copy of the same helper
  set. Three of its five files are byte-identical to `scorer/`, including
  `grader_v3.py`, which is the one Experiment 1 imports. The two that differ are
  a later variant supporting a consolidated `--layout report` corpus.

## The operator

The SADA operator is **not** here. It is promoted to `../2_operator/` because it
is the paper's contribution rather than experiment plumbing. `run_v11_update.py`
and `run_skillon_e2e_linux.py` resolve it there, falling back to the original
sibling location if present.

## Regeneration entry points

```bash
UPSTREAM_ROOT=/path/to/full/repository ./run_method.sh    <task>
UPSTREAM_ROOT=/path/to/full/repository ./run_baselines.sh <task>
```

Both need the source data, the complete upstream repository layout, Claude
CLI/API access and the corresponding Python environment. Neither is needed for
the offline verification in `../1_verify/`.

Superseded scorers and earlier baselines are not published here; they are kept
outside this repository for provenance only, and no current paper number depends
on them.
