---
dataset: imdb_movie_reviews
scenario: predictive_negative
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict negative IMDb audience satisfaction?"
source_table: augment_table/imdb_movie_reviews/predictive_negative/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:23:20.122855+00:00
wall_seconds: 52.16
---

# Predicting Negative IMDb Audience Satisfaction: Review Signal Analysis

**Dataset:** 250 reviews, balanced (125 negative / 125 positive, `label_pos = 0/1`)  
**Features analyzed:** `writing_quality`, `directing_quality`, `technical_production_quality`, `acting_quality`, `reviewer_disgust_intensity`, `franchise_sequel_fatigue`

---

## Key Predictive Signals

### 1. Craft Quality Ratings (Strongest Predictors)

| Feature | Rating | % Negative | % Positive |
|---|---|---|---|
| `acting_quality` | poor | **98.5%** | 1.5% |
| `acting_quality` | mixed | 84.6% | 15.4% |
| `acting_quality` | good | 1.6% | 98.4% |
| `writing_quality` | poor | **100%** | 0% |
| `writing_quality` | mixed | 58.7% | 41.3% |
| `writing_quality` | good | 5.0% | 95.0% |
| `directing_quality` | poor | **98.9%** | 1.1% |
| `directing_quality` | good | 5.9% | 94.1% |
| `technical_production_quality` | poor | **98.9%** | 1.1% |
| `technical_production_quality` | good | 2.4% | 97.6% |

**All four quality dimensions are near-perfect discriminators.** A rating of `poor` on any single craft dimension is almost exclusively associated with negative reviews. `writing_quality = poor` has a 100% negative rate in the sample.

Among negative reviews: 66% (83/125) carry `writing_quality = poor`, 52% carry `acting_quality = poor`, and 59 of 125 have all three of writing, directing, and acting rated poor simultaneously.

---

### 2. Reviewer Disgust Intensity (Strong, Monotone Signal)

| Score | % Negative |
|---|---|
| 2 | 88.5% |
| 3 | 97.2% |
| 4 | **100%** |
| 5 | **100%** |

Disgust intensity is strongly monotonically linked to negative outcomes. Scores ≥ 4 are exclusively negative in this dataset. Note: 15 negative reviews (12%) have no disgust intensity recorded, so this feature is informative but not universally populated.

---

### 3. Franchise / Sequel Context (Moderate Signal)

| Category | % Negative |
|---|---|
| `standalone_poorly_received` | 97.6% |
| `sequel_inferior` | 88.2% |
| `remake_inferior` | 83.3% |
| `not_applicable` | 16.4% |
| `positive_franchise_continuation` | **0%** |

Films flagged as `standalone_poorly_received`, `sequel_inferior`, or `remake_inferior` are overwhelmingly negative. `positive_franchise_continuation` maps exclusively to positive reviews, making it a useful negative-class exclusion rule. `not_applicable` skews positive (83.6%), representing reviews without franchise context.

---

## Combined Signal Strength

The most reliable predictor of a negative review is **any `poor` craft quality rating**, particularly writing or acting. These alone correctly identify ~84–100% of negatives with very low false-positive rates. Disgust intensity ≥ 3 and a `standalone_poorly_received` / `sequel_inferior` franchise tag further corroborate negativity.

---

## Exceptions and Weak Evidence

- **Mixed ratings** are ambiguous: `writing_quality = mixed` yields 59% negative, `acting_quality = mixed` yields 85% negative — acting mixed leans more decisively negative than writing mixed.
- **5 negative reviews carry `writing_quality = good`** and **1 carries `acting_quality = good`**, indicating rare cases where high craft scores still accompany negative audience sentiment (possibly due to other unmeasured factors like story or pacing).
- **Missing values**: `acting_quality` is missing for 48 negatives (38%), `technical_production_quality` for 25 (20%), limiting coverage of those features. Patterns hold within populated records but cannot be extrapolated to all reviews.
- The dataset is perfectly balanced by design, which may not reflect real-world IMDb distributions.

---

## Decision-Ready Summary

> **A review predicts negative IMDb audience satisfaction when it rates writing, directing, acting, or technical production as `poor`; when reviewer disgust intensity is ≥ 3; or when franchise context is `standalone_poorly_received`, `sequel_inferior`, or `remake_inferior`.** These signals are near-independently reliable, and co-occurrence of multiple `poor` ratings (present in 47% of negatives) provides the highest-confidence negative classification.
