# Experiment 3 — Semantic Schema Suitability

**Paper: Table 4(a)** — mean characteristic adherence by intent sub-type and
substrate (36 values). **Table 4(b)** — causal component signals: treatment
presence, confounder presence, confounder quality (18 values). **Appendix
Table 1** — the remaining component signals for the correlational and
focus-internal families (21 values). **75 values in total, all
machine-verified.**

This experiment grades the *schema*, not the values: does the emitted column set
satisfy the specific technical requirement of the intent sub-type it was asked
to serve? A causal request must surface a treatment and adjustment variables; a
predictive request must avoid restating the withheld target; a faceted request
must decompose the named concept into constitutive facets. The judge sees column
names and aggregate value distributions, not row-level correctness — so this
measures schema suitability, not value grounding (that is Experiment 4).

## What is here

| | |
|---|---|
| **Prompts** | `prompts/judge_adherence_<subtype>.md` — the adherence judge (appendix D.3), rendered once per sub-type. The frame is shared; only the spliced-in rubric differs |
| | `prompts/judge_general_quality.md` — the general-quality judge, reported as a component signal |
| **Code** | `../../4_code/benchmark/run_v11_update.py` — regenerates the `skill_on` / `skill_on_e2e` augmentations by invoking the operator |
| | `../../4_code/benchmark/scorer_v2/b2_characteristic_adherence.py` — the adherence judge, the six rubrics, and the metric definitions |
| | `../../4_code/benchmark/scorer_v2/b1_general_quality.py` — the general-quality judge |
| | `../../4_code/benchmark/scorer_v2/run_scorer_v2.py`, `run_v11_update.py` — the scoring drivers |
| **Operator** | `../../2_operator/` — the augmentation under test |
| **Raw** | `raw/characteristic_adherence/<dataset>/<substrate>/<unit>__<variant>_b2.json` — one judge output per unit, carrying the per-column verdicts and the `metrics` block every table below is computed from |
| | `raw/scoring_logs/` — the scoring run logs |
| **Tables** | `tables/exp3_table4a.csv` — Table 4(a), regenerated |
| | `tables/exp3_table4b_and_appendix_table1.csv` — Table 4(b) and Appendix Table 1, regenerated, one row per (sub-type, signal) with the paper value beside each recomputed value |
| | `tables/SUMMARY_by_family.md` — family-level roll-up |
| | `tables/CHARACTERISTIC_SCORING_PROVENANCE.md` — how the scores were assigned |

## Scope

- `airlines_review_full` is excluded, matching Experiments 1–2.
- **Unequal sample counts are preserved as they occurred.** Haiku `what_if` is
  `17/16/16` across the three variants, not trimmed to a common denominator. The
  regenerated CSVs carry an `n` column per variant so this is visible.
- The six sub-types are enumerated in
  `../../5_reference/configs/experiment_scope.json`.

## How the numbers are rebuilt

Every value in all three tables comes from the same `metrics` block of the same
per-unit judge output. Table 4(a) averages `adherence` per (sub-type, substrate,
variant). Table 4(b) and Appendix Table 1 average the component signals per
(sub-type, variant) **pooled over both substrates**, matching the paper's
"averaged over both substrates".

Two details a reviewer may want to check:

- `treatment_present` and `confounder_present` are per-unit **booleans**; the
  paper reports them as the fraction of units where they hold, so they are
  averaged as 1/0.
- The averages are rounded half up on exact fractions rather than on binary
  floats. One value needs this: PFE `predictive_utility` under `skill_on_e2e`
  has an exact mean of 0.555, which the paper shows as 0.56 while
  `f"{x:.2f}"` on the float yields 0.55.

Verify with:

```bash
../../1_verify/verify_all.sh
```
