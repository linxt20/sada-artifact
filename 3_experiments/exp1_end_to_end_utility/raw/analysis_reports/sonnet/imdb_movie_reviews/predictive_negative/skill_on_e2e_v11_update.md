---
dataset: imdb_movie_reviews
scenario: predictive_negative
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict negative IMDb audience satisfaction?"
source_table: augment_table/imdb_movie_reviews/predictive_negative/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:23:36.190248+00:00
wall_seconds: 64.01
---

# Signals Predicting Negative IMDb Audience Satisfaction

**Dataset:** 250 IMDB movie reviews (125 negative `label_pos=0`, 125 positive `label_pos=1`), balanced split.

**Method note:** TAPP-generated columns used in this analysis: `rec_signal`, `reviewer_emotional_tone`, `script_quality_verdict`, `acting_quality_verdict`, `production_quality_verdict`, `plot_coherence`, `comparative_benchmark`.

---

## 1. Strongest Single-Variable Predictors of Negative Outcome

| Signal | Value | Neg Count | Total | Neg Rate |
|---|---|---|---|---|
| `reviewer_emotional_tone` | strongly_negative | 65 | 65 | **100%** |
| `rec_signal` | explicit_avoid | 68 | 68 | **100%** |
| `acting_quality_verdict` | poor | 68 | 69 | **98.6%** |
| `script_quality_verdict` | poor | 90 | 92 | **97.8%** |
| `production_quality_verdict` | poor | 91 | 93 | **97.8%** |
| `plot_coherence` | predictable | 14 | 15 | **93.3%** |
| `plot_coherence` | incoherent | 39 | 42 | **92.9%** |
| `rec_signal` | implicit_avoid | 41 | 46 | **89.1%** |
| `reviewer_emotional_tone` | mildly_negative | 44 | 49 | **89.8%** |
| `comparative_benchmark` | negative_comparison | 43 | 53 | **81.1%** |

Conversely, `strongly_positive` emotional tone (n=48) and `explicit_recommend` rec_signal (n=34) each have a **0% negative rate**, and `good` verdicts for any craft dimension yield negative rates below 5%.

---

## 2. Craft Quality Verdicts (Script, Acting, Production)

All three craft dimensions individually achieve near-perfect separation when rated `poor`:

- **`script_quality_verdict`** coverage: 215/250 (86%). `poor` → 97.8% negative; `good` → 5.0% negative.
- **`acting_quality_verdict`** coverage: 141/250 (56%, lower coverage). `poor` → 98.6% negative; `good` → 3.5% negative. Mixed coverage reduces standalone utility.
- **`production_quality_verdict`** coverage: 249/250 (100%). `poor` → 97.8% negative; `good` → 3.2% negative.

**Combined signal:** Reviews where all three craft verdicts are simultaneously `poor` number 64; 63/64 (98%) are negative. This compound indicator is the most precise craft-based negative predictor.

---

## 3. Reviewer Emotional Tone and Recommendation Signal

`reviewer_emotional_tone` is fully populated (250/250) and achieves perfect or near-perfect separation at the extremes:

| Tone | Neg | Total | Neg Rate |
|---|---|---|---|
| strongly_negative | 65 | 65 | 100% |
| mildly_negative | 44 | 49 | 90% |
| neutral_mixed | 14 | 30 | 47% |
| mildly_positive | 2 | 58 | 3% |
| strongly_positive | 0 | 48 | 0% |

`rec_signal` (250/250 coverage) shows the same pattern: `explicit_avoid` is a perfect negative marker (68/68); `implicit_avoid` captures an additional 41 negatives at 89% precision. Together, the two avoid-signal categories cover 109/125 negatives (87%).

---

## 4. Plot Coherence

`plot_coherence` covers 179/250 (72%). Among negatives, `incoherent` (39) and `predictable` (14) account for 53 negative reviews; nearly all (92–93%) are negative. Importantly, `coherent` does **not** protect against negativity alone (19/122 coherent reviews are still negative), meaning poor plot is a strong positive signal for negativity but coherent plot is not sufficient for positivity.

---

## 5. Comparative Benchmarking

`comparative_benchmark` is fully populated. Reviews that invoke a `negative_comparison` (e.g., "worse than…") predict negativity at 81% (43/53). Positive comparisons nearly eliminate it (1/36 = 3%). The majority of reviews (161/250) make no comparison, with a 50% negative rate reflecting the base rate.

---

## 6. Summary: Ranked Negative Predictors

| Rank | Signal | Coverage | Neg Rate When Present |
|---|---|---|---|
| 1 | `reviewer_emotional_tone` = strongly_negative | 100% | 100% |
| 2 | `rec_signal` = explicit_avoid | 100% | 100% |
| 3 | `acting_quality_verdict` = poor | 56% | 98.6% |
| 4 | `script_quality_verdict` = poor | 86% | 97.8% |
| 5 | `production_quality_verdict` = poor | 100% | 97.8% |
| 6 | `plot_coherence` = incoherent/predictable | 72% | 92–93% |
| 7 | `rec_signal` = implicit_avoid | 100% | 89.1% |
| 8 | `reviewer_emotional_tone` = mildly_negative | 100% | 89.8% |
| 9 | `comparative_benchmark` = negative_comparison | 100% | 81.1% |

**Decision rule:** A review is near-certain to be negative if it displays any of: (a) `strongly_negative` emotional tone, (b) `explicit_avoid` rec signal, or (c) `poor` verdicts for both script and production quality. These signals cover the vast majority of the 125 negative reviews with minimal false positives.
