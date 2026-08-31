# Artifact Index

Claim-by-claim map from every number in the paper to the code that produced it,
the prompt that drove it, the raw per-item output it was aggregated from, and the
table a reviewer can regenerate.

`README.md` has the reproduction protocol and the directory layout. This file is
for locating things.

---

## 1. Fastest path for a reviewer

```bash
./1_verify/verify_all.sh
```

Standard library only, no model calls, no network. Expected output:
`Reproduction status: PASS` over **235 paper-facing values**.

Then read, in order:

1. `1_verify/report/REPRODUCTION_REPORT.md` — what was checked, per paper table
2. `1_verify/report/verification.json` — machine-readable pass/fail
3. `3_experiments/<exp>/README.md` — one experiment at a time
4. `3_experiments/<exp>/tables/*.csv` — the regenerated tables, with the paper
   value beside each recomputed value
5. `5_reference/paper/experiments.tex` — the paper section under test
6. `5_reference/paper/appendix.pdf` — the supplementary appendix, including the
   verbatim judge prompts of appendix D.1–D.4 referenced in §5

---

## 2. Paper number → artifact map

Table numbers are those of the compiled `main.pdf`.

| Paper location | Content | Regenerated table | Raw output | Verified |
|---|---|---|---|---:|
| Table 1 | FOI intent taxonomy | — (conceptual) | queries in `5_reference/configs/grounding_queries.json` | n/a |
| Table 2 | Exp. 1 end-to-end Bradley–Terry | `3_experiments/exp1_end_to_end_utility/tables/exp1_bt.csv` | `.../exp1_end_to_end_utility/raw/bt/` | 8 |
| Table 3 | Exp. 2 analysis-form distribution | `3_experiments/exp2_analysis_form/tables/exp2_form.csv` | `.../exp2_analysis_form/raw/form_class/` | 24 |
| Table 4(a) | Exp. 3 adherence by sub-type | `3_experiments/exp3_schema_suitability/tables/exp3_table4a.csv` | `.../exp3_schema_suitability/raw/characteristic_adherence/` | 36 |
| Table 4(b) | Exp. 3 causal component signals | `3_experiments/exp3_schema_suitability/tables/exp3_table4b_and_appendix_table1.csv` | same | 18 |
| Appendix Table 1 | Exp. 3 remaining component signals | same file as Table 4(b) | same | 21 |
| §5.5 prose | Exp. 4 grounding: 471,200 cells; 12.98→10.29 Haiku, 24.29→5.47 Sonnet | `3_experiments/exp4_scale_and_grounding/tables/exp4_grounding.csv` | `.../exp4_scale_and_grounding/raw/grounding/` | 18 |
| §5.5 prose | Exp. 4 mechanism: 8 of 9 baseline scripts are rule-based | — | `.../exp4_scale_and_grounding/raw/mechanism_artifacts/`, `raw/tagging_traces/` | by inspection |
| Table 5 | Exp. 5 no-text-embedding | `3_experiments/exp5_predictive_features/tables/table5_no_text.csv` | `.../exp5_predictive_features/raw/xgboost/` | part of 110 |
| Table 6 | Exp. 5 text-embedding, SHAP top-64 | `3_experiments/exp5_predictive_features/tables/table6_text_k64.csv` | same | part of 110 |

**Total machine-verified for Experiments 1–5: 235.**

Four tables that earlier drafts carried are `\iffalse`-commented in the current
paper and so have no numbered location: the rubric-dimension table (its data is
in `3_experiments/exp1_end_to_end_utility/tables/SCORE_SUMMARY_exp1_exp2.md`),
the family-level adherence table (`.../exp3_schema_suitability/tables/SUMMARY_by_family.md`),
the adherence sub-signal table (superseded by Appendix Table 1), and Experiment
4's `tab:scale`, whose numbers now appear inline in §5.5 and are verified here in
full.

---

## 3. Experiment by experiment

Each experiment directory holds the same four parts — `README.md`, `prompts/`,
`raw/`, `tables/` — and its README maps them onto the paper claim. Read those
rather than this section for detail; the table below is the entry point.

| Experiment | Directory | Paper | Verified |
|---|---|---|---:|
| End-to-end analysis utility | `3_experiments/exp1_end_to_end_utility/` | Table 2 | 8 |
| The form of the resulting analysis | `3_experiments/exp2_analysis_form/` | Table 3 | 24 |
| Semantic schema suitability | `3_experiments/exp3_schema_suitability/` | Table 4(a)(b), Appendix Table 1 | 75 |
| Semantic augmentation at scale | `3_experiments/exp4_scale_and_grounding/` | §5.5 | 18 |
| Predictive feature engineering | `3_experiments/exp5_predictive_features/` | Tables 5–6 | 110 |

Cross-experiment dependencies worth knowing:

- **Experiments 1 and 2 share one report corpus.** Experiment 2 classifies the
  reports Experiment 1 generated; it does not generate its own. The analyst
  prompts that produced them live in `exp1_end_to_end_utility/prompts/`.
- **Experiments 3, 4 and 5 all invoke the operator** in `2_operator/`, each
  through its own driver.
- **Experiment 4's mechanism claim rests on a contrast**, not on a metric: the
  baseline's emitted scripts (`raw/mechanism_artifacts/`) against SADA's per-row
  tagging traces (`raw/tagging_traces/`, 15,058 files in 14 per-unit archives).

### Code behind each experiment

The code is one tree, `4_code/`, because several modules are shared and the
archived scripts resolve them as siblings.

| Experiment | Entry points under `4_code/` |
|---|---|
| Exp. 1 | `benchmark/gen_update_reports.py`, `benchmark/gen_augment_table_reports.py`, `benchmark/grade_bt_update.py`, `benchmark/score_semantic_recall/grader_v3.py` |
| Exp. 2 | `benchmark/classify_form_update.py` |
| Exp. 3 | `benchmark/run_v11_update.py`, `benchmark/scorer_v2/{run_scorer_v2,run_v11_update,b1_general_quality,b2_characteristic_adherence}.py` |
| Exp. 4 | `benchmark/augmenter/run_skill_off_agentic_augment.py`, `benchmark/grounding_eval/{run_grounding,col_stats}.py`, `benchmark/scorer_grounding/_g_judge.py` |
| Exp. 5 | `TextTabBench/augment_process_result_v11_update/*`, `TextTabBench/pipelines/*` |
| shared | `benchmark/scorer/` (Claude-CLI invocation, table IO), `benchmark/scorer_characteristic/` (rubric helpers imported by `scorer_v2`) |

`benchmark/scorer/` and `benchmark/score_semantic_recall/` are two
differently-evolved copies of the same helper set. Three of five files are
byte-identical, including `grader_v3.py`, which is the one Experiment 1 imports.
Both are live: `scorer/` is the sibling `scorer_v2/`, `grounding_eval/` and
`augmenter/` resolve, `score_semantic_recall/` is Experiment 1's.

---

## 4. The SADA operator

`2_operator/` is the canonical and only copy of the operator that produced every
SADA result in the paper.

```text
2_operator/
├── SKILL.md                 operator contract: stage sequence, visual-preview rule,
│                            row-alignment and closed-vocabulary contracts
├── README.md                v10 -> v11 change list
├── config/model_recipe.json per-stage model/tier recipe
├── prompts/
│   ├── execution_decision.md          planning / tier and concurrency decision
│   ├── categorization.md              category proposal (single chunk)
│   ├── categorization_large_scale.md  category proposal (map phase)
│   ├── tagging_consolidation.md       hierarchical consolidation (reduce phase)
│   ├── tagging.md                     row-level tagging (single chunk)
│   ├── tagging_large_scale.md         row-level tagging (map phase)
│   └── subagent_invocation.md         isolated sub-agent contract (appendix C)
└── scripts/
    ├── run_tapp.py          the operator: plan -> schema -> chunk -> tag -> merge
    ├── host_executor.py     stage execution, retry, artifact manifest
    ├── reference_comparison.py, run_reference_comparison_parallel.ps1
    └── visual_preview.py, visual_preview_feasibility.py
```

**On the version string.** `run_tapp.py` sets `SKILL_VERSION = "skill_v10"`. That
constant is the tag written into run artifacts, and it was not bumped when the
v11 concept-fidelity rules landed. It is therefore the expected value: every
archived run under `3_experiments/*/raw/` records
`"skill_version": "skill_v10"`, which is how a reviewer confirms the results came
from exactly this directory and not from a later revision.

A later revision of the operator does exist — it fixes an evidence-contract
whitelist and adds a pre-tag facet de-duplication — but it was written after
these experiments, for ground-truth annotation work, and produced no paper number.
It is deliberately not in this artifact. The illustrative Figure 3 of §4.2 was run
with a later revision still; see §7.

Development prototypes and smoke-test workdirs were moved out of the operator
directory and are not published here. They contribute to no paper number. The
stage artifacts they would illustrate — `execution_plan.json`, `specs.json`,
`categorization.json`, `merge_report.json`, `artifact_manifest.json` — are
produced by `scripts/run_tapp.py` in this directory, and the schema-integrity
rules they must satisfy are stated in Appendix B of the paper.

---

## 5. Prompt inventory

Every LLM-facing prompt in the paper. The files under `3_experiments/*/prompts/`
are **generated from the code** by `3_experiments/_extract_prompts.py`, so they
cannot drift; `--check` verifies them without writing.

| Prompt | Appendix | Rendered file | Source under `4_code/` |
|---|---|---|---|
| Analyst prompt (baselines + `skill_on`) | — | `exp1_end_to_end_utility/prompts/analyst_prompt_all_conditions.md` | `benchmark/gen_augment_table_reports.py` (`PROMPT_TEMPLATE`) |
| Analyst prompt (`skill_on_e2e`) | — | `exp1_end_to_end_utility/prompts/analyst_prompt_skill_on_e2e.md` | same file (`E2E_PROMPT_TEMPLATE`) |
| Exp. 1 pairwise report grading | D.1 | `exp1_end_to_end_utility/prompts/judge_pairwise_report_grading.md` | `benchmark/score_semantic_recall/grader_v3.py` (`PAIRWISE_PROMPT`) |
| Exp. 2 analytical-form classification | D.2 | `exp2_analysis_form/prompts/judge_analytical_form_classification.md` | `benchmark/classify_form_update.py` (`PROMPT`) |
| Exp. 3 characteristic adherence, ×6 sub-types | D.3 | `exp3_schema_suitability/prompts/judge_adherence_<subtype>.md` | `benchmark/scorer_v2/b2_characteristic_adherence.py` (`build_prompt`, `_RUBRICS`) |
| Exp. 3 general quality | — | `exp3_schema_suitability/prompts/judge_general_quality.md` | `benchmark/scorer_v2/b1_general_quality.py` (`build_prompt`) |
| Exp. 4 baseline agentic augmentation | — | `exp4_scale_and_grounding/prompts/baseline_agentic_augmentation.md` | `benchmark/augmenter/run_skill_off_agentic_augment.py` (`_agent_prompt`) |
| Exp. 4 row-level grounding audit | D.4 | `exp4_scale_and_grounding/prompts/judge_row_level_grounding.md` | `benchmark/scorer_grounding/_g_judge.py` (`SYSTEM`) |
| Exp. 5 baseline augmentation | — | `exp5_predictive_features/prompts/baseline_augmentation.md` | `TextTabBench/augment_process_result_v11_update/skilloff_augment.py` (`PROMPT`) |
| Operator stage prompts (7) | C describes the isolation contract | — | `2_operator/prompts/` |

All four judges of Experiments 1–4 run on one fixed model
(`claude-opus-4.8-xhigh`), held constant across every condition and substrate, and
every judge emits strict JSON so downstream scoring is deterministic.

Two prompt facts a reviewer may want to confirm directly, since both are load-
bearing claims:

- The three non-e2e conditions share **one** analyst prompt, so the analyst is
  never told which columns are augmented.
- The `skill_off` baseline prompt constrains only the deliverable's CSV format,
  never what the columns should be — it leaks none of the operator's analytical
  guidance.

---

## 6. Provenance and traceability

| Question | Where to look |
|---|---|
| Did SADA label rows with an LLM, or with regexes? | `3_experiments/exp4_scale_and_grounding/raw/tagging_traces/` vs `raw/mechanism_artifacts/` |
| Is a run reconstructible from disk alone? | every stage input and output is registered by sha256 into `artifact_manifest.json`; see `2_operator/scripts/host_executor.py` |
| Does every augmented column trace to a schema node? | `specs.json` + `categorization.json` in the same workdirs (`SelectedNodeId`, `Role`, `Parent`, `StructurePath`) |
| What does a complete operator workdir look like? | the stage sequence and its artifacts are specified in `2_operator/SKILL.md`; no example workdir is published here |
| How were adherence scores assigned? | `3_experiments/exp3_schema_suitability/tables/CHARACTERISTIC_SCORING_PROVENANCE.md` |
| What exactly was excluded from each experiment? | `5_reference/configs/experiment_scope.json` |
| Which upstream repository, at which commit? | `5_reference/configs/upstream_sources.json`, `THIRD_PARTY.md` |
| Which package versions? | `requirements.txt` (suggested), `requirements-observed.txt` (observed snapshot) |
| Which operator revision produced a given run? | grep `skill_version` in the run's artifacts, not the directory name |

---

## 7. Not included, and why

- **Source datasets.** Not redistributed; third-party licences apply. The
  TextTabBench pool must be obtained upstream. See `5_reference/data/README.md`
  and `THIRD_PARTY.md`. No source table is redistributed here.
- **Model credentials.** Regeneration needs Claude CLI/API access.
- **The full working repository.** `4_code/run_method.sh` and
  `4_code/run_baselines.sh` need `UPSTREAM_ROOT` pointed at a complete checkout.
  The offline verification path does not.
- **`.git` metadata of the upstream checkout.** Not retained, so the exact
  upstream commit cannot be asserted; `5_reference/configs/upstream_sources.json`
  records the observed public HEAD instead and says so explicitly.
- **The illustrative Figure 3 of §4.2, and the operator revision behind it.** That
  three-panel Yelp comparison was run with a later revision (`v14`/`v15`) than
  Experiments 1–5. Neither the panels nor that revision is part of this
  repository. The figure supports no quantitative claim: every number the paper
  reports rests on Experiments 1–5, all of which are verified here.

### Deliberate changes to the archived material

Some archived scripts still contain original absolute paths. They are preserved
as-run, and the offline verification path depends on none of them. Where a
fallback was needed to make the code resolve from a fresh checkout, the original
path is kept first or alongside and the change is commented in place:

| File under `4_code/` | Change |
|---|---|
| `benchmark/grade_bt_update.py` | sibling `score_semantic_recall/` tried before the original absolute `sys.path` entry |
| `benchmark/scorer_grounding/_g_judge.py` | sibling `scorer/` tried alongside the original absolute `sys.path` entry |
| `benchmark/grounding_eval/run_grounding.py` | `queries.json` falls back to `5_reference/configs/grounding_queries.json`, byte-equivalent content, so the artifact keeps one copy |
| `benchmark/run_v11_update.py` | operator path falls back to `2_operator/` now that the skill is promoted to the top level |
| `TextTabBench/.../run_skillon_e2e_linux.py` | same |

And in `1_verify/reproduce_paper_results.py`: the Experiment 4 loader accepts
`opus.jsonl.gz` as well as `opus.jsonl` because the grounding cache is shipped
gzipped, and the component-signal averages are rounded half up on exact fractions
rather than binary floats (one paper value, PFE `predictive_utility` under
`skill_on_e2e`, has an exact mean of 0.555).

---

## 8. Packed material

Two locations are stored compressed. Nothing needs to be unpacked to run the
verification.

| Location | Form | Note |
|---|---|---|
| `3_experiments/exp4_scale_and_grounding/raw/tagging_traces/` | 14 `.tar.gz`, one per analysis unit | 15,058 files, 153 MB raw, 11:1 compressible. `extract.sh` unpacks in place; the verifier does not read them |
| `3_experiments/exp4_scale_and_grounding/raw/grounding/_cache/**/opus.jsonl.gz` | gzipped JSONL | read directly by the verifier |

## 9. Deliberately not published here

Three kinds of material were left out of this repository. None of them is on the
path to any paper number, and the verification in §1 does not read them:

| What | Why |
|---|---|
| Development-time operator prototypes and smoke-test workdirs | development scaffolding; contribute to no paper value |
| Superseded scorers and earlier baselines | replaced by the code in `4_code/`; kept outside the repository for provenance only |
| The illustrative Figure 3 case study of §4.2 | run with a later operator revision than Experiments 1–5, and supports no quantitative claim |
