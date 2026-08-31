---
dataset: amazon_fine_food_review
scenario: predictive_score_features
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "review_score"
query: "What features can be extracted to train a model to predict a review's score?"
source_table: augment_table/amazon_fine_food_review/predictive_score_features/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:09:01.008152+00:00
wall_seconds: 100.16
---

# Predictive Score Features — Amazon Fine Food Reviews
**Dataset:** 10,000 reviews · **Outcome:** `Score` (1–5 stars, mean 4.13) · **Date:** 2026-07-30

---

## 1. Score Distribution

| Score | Count | % of Total |
|-------|------:|----------:|
| 1 | 932 | 9.3% |
| 2 | 590 | 5.9% |
| 3 | 862 | 8.6% |
| 4 | 1,433 | 14.3% |
| 5 | 6,183 | 61.8% |

The distribution is strongly right-skewed; any model must account for class imbalance.

---

## 2. Feature Inventory & Predictive Signal

### 2.1 Strongest Predictors (Spearman ρ with Score)

| Feature | Type | ρ | n |
|---------|------|--:|--:|
| `overall_sentiment_polarity` (encoded) | TAPP | **0.823** | 9,999 |
| `review_tone_extremity` (encoded) | TAPP | **0.820** | 10,000 |
| `taste_flavor_satisfaction` (encoded) | TAPP | **0.800** | 9,364 |
| `product_efficacy` (encoded) | TAPP | **0.818** | 6,697 |
| `expectation_match` (encoded) | TAPP | **0.765** | 9,952 |
| `product_quality_judgment` (encoded) | TAPP | **0.735** | 9,953 |
| `helpfulness_ratio` (HelpfulnessNumerator / HelpfulnessDenominator) | Structured | 0.393 | 5,122 |
| `text_length` (character count of `Text`) | Derived | −0.143 | 10,000 |

Encoding notes: polarity negative→positive (1–4); tone strongly_negative→strongly_positive (1–5); expectation not_met→exceeded (1–4); quality defective→exceeds (1–4); taste dissatisfied→highly_satisfied (1–4); efficacy negative→strong_positive (1–4).

---

### 2.2 Sentiment & Tone (Highest Signal)

`overall_sentiment_polarity` and `review_tone_extremity` are the single strongest predictors:

| `overall_sentiment_polarity` | Mean Score | Count |
|------------------------------|----------:|------:|
| negative | 1.56 | 1,375 |
| mixed | 3.43 | 1,853 |
| neutral | 3.53 | 30 |
| positive | **4.85** | 6,741 |

| `review_tone_extremity` | Mean Score | Count |
|--------------------------|----------:|------:|
| strongly_negative | 1.23 | 747 |
| mildly_negative | 2.35 | 1,315 |
| neutral_or_ambivalent | 3.26 | 330 |
| mildly_positive | 4.33 | 1,850 |
| strongly_positive | **4.91** | 5,758 |

Together these two facets capture the hedonic valence and intensity of the review text — information not directly available as a structured column.

---

### 2.3 Expectation Match & Product Quality

`expectation_match` and `product_quality_judgment` provide complementary judgment signal:

| `expectation_match` | Mean Score | Count |
|---------------------|----------:|------:|
| not_met | 1.64 | 1,543 |
| partially_met | 3.30 | 1,260 |
| met | 4.69 | 2,924 |
| exceeded | **4.92** | 4,225 |

| `product_quality_judgment` | Mean Score | Count |
|----------------------------|----------:|------:|
| defective_or_spoiled | 1.44 | 266 |
| below_expectations | 1.93 | 1,681 |
| meets_expectations | 4.42 | 3,671 |
| exceeds_expectations | **4.92** | 4,335 |

---

### 2.4 Category-Specific Taste & Efficacy Facets

`taste_flavor_satisfaction` is highly predictive (ρ = 0.80) and covers ~94% of reviews; `product_efficacy` covers 67% (not applicable where taste dominates):

| `taste_flavor_satisfaction` | Mean Score | Count |
|-----------------------------|----------:|------:|
| dissatisfied | 1.64 | 1,380 |
| neutral | 3.10 | 760 |
| satisfied | 4.37 | 1,979 |
| highly_satisfied | **4.90** | 5,245 |

| `product_efficacy` | Mean Score | Count |
|---------------------|----------:|------:|
| negative_effect | 1.65 | 1,081 |
| no_effect | 2.02 | 46 |
| mild_positive_effect | 3.78 | 1,482 |
| strong_positive_effect | **4.87** | 4,088 |

---

### 2.5 Repurchase Intent

`repurchase_intent` (True/False) is a strong binary signal:

| Repurchase Intent | Mean Score | Count |
|-------------------|----------:|------:|
| False | 3.80 | 6,183 |
| True | **4.83** | 2,795 |

Reviews expressing intent to repurchase average 1.03 stars higher. Note: 1,022 rows have NaN (10.2%); imputation needed.

---

### 2.6 Structured Original Features

| Feature | Description | Signal |
|---------|-------------|--------|
| `HelpfulnessNumerator` / `HelpfulnessDenominator` → helpfulness ratio | Community upvote rate | ρ = 0.393 (n=5,122); higher-scored reviews more helpful |
| `Text` character length | Review verbosity | ρ = −0.143; longer reviews trend slightly lower score (negative reviews are more detailed) |
| `Summary` length | Headline length | Weak signal, complementary to text length |
| `Time` (Unix timestamp) | Review date | Low temporal drift; mean score stable 4.07–4.54 across 2004–2012 |
| `ProductId` | Product identity | 1,422 unique products; product-level mean score std = 1.12, justifying a product-level random effect or target encoding |
| `UserId` | Reviewer identity | 9,015 unique users; sparse repeat reviewers — user-level features viable only with dataset expansion |

---

### 2.7 Weaker / Redundant Features

- **`bitterness_presence`**: binary, weak spread (mean 3.32 vs 4.15 for False/True); mostly subsumed by `taste_flavor_satisfaction`.
- **`flavor_strength_perception`**: signal present (balanced → 4.60, too_weak → 2.34) but covered by `taste_flavor_satisfaction`.
- **`texture_satisfaction`**: not_applicable dominates (78%); informative when present (negative → 1.91, positive → 4.78) but sparse.
- **`ease_of_use`**: not_applicable 79%; useful for health/supplement subcategory.
- **`novelty_value`**: minimal signal (True 3.76 vs False 4.21); not a strong predictor.
- **`reviewer_expertise_signal`**: near-flat (expert 4.12 vs regular 4.14); low discriminative power.
- **`review_specificity_level`**: reversed pattern (generic_brief 4.55 vs detailed_specific 3.93); adds modest signal, correlated with text length.
- **`product_category`** / **`usage_context`**: modest mean variation (3.86–4.48); useful as categorical controls or for category-specific sub-models.

---

## 3. Recommended Feature Set for a Predictive Model

### Tier 1 — High Signal (include in all models)
1. **`overall_sentiment_polarity`** (TAPP) — ρ = 0.823
2. **`review_tone_extremity`** (TAPP) — ρ = 0.820
3. **`product_efficacy`** (TAPP) — ρ = 0.818
4. **`taste_flavor_satisfaction`** (TAPP) — ρ = 0.800
5. **`expectation_match`** (TAPP) — ρ = 0.765
6. **`product_quality_judgment`** (TAPP) — ρ = 0.735
7. **`repurchase_intent`** (TAPP) — mean gap +1.03 stars

### Tier 2 — Moderate Signal (include when available)
8. **`helpfulness_ratio`** (`HelpfulnessNumerator` / `HelpfulnessDenominator`) — ρ = 0.393
9. **`text_length`** (character count of `Text`) — ρ = −0.143
10. **`ProductId`** target-encoded or as random effect
11. **`product_category`** / **`usage_context`** (TAPP) — categorical controls

### Tier 3 — Contextual / Sparse (use for sub-models)
12. **`texture_satisfaction`**, **`ease_of_use`**, **`bitterness_presence`** (TAPP) — sparse but informative for relevant categories
13. **`review_specificity_level`** (TAPP) — modest signal
14. **`Time`** (review date) — low drift but captures platform maturation

---

## 4. Method Note

**TAPP-generated columns used in this report:**
`overall_sentiment_polarity`, `review_tone_extremity`, `repurchase_intent`, `taste_flavor_satisfaction`, `flavor_strength_perception`, `bitterness_presence`, `texture_satisfaction`, `product_quality_judgment`, `product_efficacy`, `ease_of_use`, `product_category`, `usage_context`, `expectation_match`, `novelty_value`, `reviewer_expertise_signal`, `review_specificity_level`

All 16 TAPP columns were evaluated. Spearman correlations were computed after ordinal encoding of ordered categories. Structured columns (`Score`, `HelpfulnessNumerator`, `HelpfulnessDenominator`, `Text`, `Time`, `ProductId`, `UserId`) were treated as primary evidence; TAPP columns provided semantic signal absent from the original schema.
