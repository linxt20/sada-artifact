---
dataset: amazon_fine_food_review
scenario: predictive_score_features
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "review_score"
query: "What features can be extracted to train a model to predict a review's score?"
source_table: augment_table/amazon_fine_food_review/predictive_score_features/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:08:04.052502+00:00
wall_seconds: 43.26
---

# Feature Analysis: Predicting Amazon Fine Food Review Score

**Dataset:** 10,000 reviews · 20 columns · Target variable: `Score` (1–5 integer)  
**Score distribution:** heavily skewed toward 5 (62%), with 1–3 together ~24%.

---

## 1. Augmented Categorical Features (Strongest Predictors)

These columns were derived from review text and show the clearest signal for Score.

| Feature | Key finding |
|---|---|
| `overall_sentiment` | `positive` → mean 4.85; `negative` → 1.56. Largest spread of any feature. |
| `expectation_match` | `exceeded_expectations` → 4.92; `below_expectations` → 1.97. Near-monotonic with Score. |
| `taste_texture_quality` | `positive` → 4.82; `negative` → 1.59. Strong for food/snack categories. |
| `product_effectiveness` | `works_as_claimed` → 4.80; `does_not_work` → 1.41. Strongest for supplements/pet food. |
| `description_accuracy` | `accurate` → 4.40; `inaccurate` → 1.95. `not_evaluated` middle ground (4.29). |

**Recommendation:** These five augmented features are the highest-value inputs for a classifier; `overall_sentiment` and `expectation_match` alone would likely dominate a simple model.

---

## 2. Augmented Categorical Features (Moderate Predictors)

| Feature | Notes |
|---|---|
| `review_specificity` | Counterintuitively, `vague` → 4.69 vs `highly_specific` → 3.86. Highly specific reviews may reflect complaints or detailed criticism. Weak directional predictor. |
| `product_category` | Narrow range (3.81–4.47). `condiment_sauce` highest, `other` lowest. Useful as a control variable more than a strong predictor. |
| `use_case_context` | Range 3.03–4.56. `Unknown` (3.03) likely marks unclear/negative reviews; other contexts cluster near 4.0–4.6. |

---

## 3. Boolean Features (Weak Predictors)

| Feature | False mean | True mean | Δ |
|---|---|---|---|
| `health_dietary_mention` | 4.07 | 4.37 | +0.30 |
| `comparison_to_alternative` | 4.21 | 3.88 | −0.33 |

Both show small but consistent differences. Reviews mentioning comparisons to alternatives skew slightly lower (possibly dissatisfied customers), while health/dietary mentions skew slightly higher (niche loyal customers). Useful as binary flags but not decisive on their own.

---

## 4. Raw Metadata Features (Weak or Indirect)

| Feature | Notes |
|---|---|
| `HelpfulnessNumerator` / `HelpfulnessDenominator` | Helpfulness ratio correlates with Score at only **r = 0.034** — essentially no linear relationship. Not recommended as a standalone predictor. |
| `Time` (Unix timestamp) | Could capture temporal drift in review standards; not analyzed here but worth testing. |
| `ProductId` / `UserId` | High-cardinality IDs; useful as embedding or frequency-encoded features (e.g., per-product average score, per-user rating bias). |

---

## 5. Text Features (Require NLP Engineering)

| Source field | Derivable features |
|---|---|
| `Text` | TF-IDF / embeddings; sentiment polarity score; review length; presence of negation words; exclamation count |
| `Summary` | Short-text sentiment; keyword extraction (e.g., "great", "terrible") |

The augmented columns (`overall_sentiment`, `expectation_match`, etc.) are likely already derived from `Text`, making them compressed but information-rich proxies. Including raw text embeddings alongside them may add marginal lift.

---

## 6. Feature Priority Summary

| Priority | Feature(s) | Type |
|---|---|---|
| **High** | `overall_sentiment`, `expectation_match`, `taste_texture_quality`, `product_effectiveness`, `description_accuracy` | Augmented categorical |
| **Medium** | `review_specificity`, `use_case_context`, `product_category` | Augmented categorical |
| **Low** | `health_dietary_mention`, `comparison_to_alternative`, `Time`, user/product aggregates | Boolean / metadata |
| **Exploratory** | `Text`, `Summary` (NLP) | Raw text |

---

## Caveats

- The dataset is **heavily imbalanced** (62% Score=5); models should use stratified sampling or class-weight adjustments.
- The augmented features were themselves extracted from the review text, so they may introduce **label leakage** if the model is eventually deployed on raw text — pipelines must generate these features at inference time using the same extraction method.
- `review_specificity`'s inverse relationship with Score is **counterintuitive** and warrants further investigation before relying on it.
- Helpfulness ratio has near-zero correlation with Score and should likely be **excluded** unless combined with other signals.
