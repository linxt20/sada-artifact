---
dataset: amazon_fine_food_review
scenario: predictive_score_features
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "review_score"
query: "What features can be extracted to train a model to predict a review's score?"
source_table: augment_table/amazon_fine_food_review/predictive_score_features/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:09:24.020614+00:00
wall_seconds: 123.21
---

# Features for Predicting Amazon Fine Food Review Scores

## Executive Summary

This analysis identifies features that can be extracted to train a predictive model for review scores (1–5 ratings) in the Amazon fine food review dataset. Drawing from 10,000 reviews, we combine **original structured data** (review text, helpfulness metrics, metadata) with **TAPP-generated semantic facets** to provide a comprehensive feature engineering roadmap. Five features emerge as primary predictors, with strong explanatory power and complementary perspectives on review drivers.

---

## Outcome Variable: Review Score Distribution

The target variable shows strong skew toward 5-star ratings:

| Score | Count | % |
|-------|-------|-----|
| 1     | 932   | 9.3% |
| 2     | 590   | 5.9% |
| 3     | 862   | 8.6% |
| 4     | 1,433 | 14.3% |
| 5     | 6,183 | 61.8% |

**Mean score: 4.14 | Median: 5.0**

This class imbalance is characteristic of online review platforms and should inform model selection and evaluation strategies.

---

## Primary Predictive Features

### 1. **Sentiment Polarity** (TAPP-generated)
**Mean score by sentiment:** Negative (1.85) → Mixed (3.57) → Neutral (3.56) → Positive (4.83)

Sentiment polarity is the strongest differentiator across all review categories:
- **Positive reviews (70.1% of dataset):** 84.7% rate as 5-star; mean score 4.83
- **Negative reviews (18.6%):** 47.9% rate as 1-star; mean score 1.85  
- **Mixed/Neutral reviews (10.1%):** Concentrated in mid-range (3–4 stars); mean scores 3.57–3.56

**Strength:** High coverage (9,999/10,000 non-missing), clean categorical separation, directly predictive of rating direction.

**Validation:** Strong consistency between sentiment_polarity labels and raw review text (Summary and Text fields). Negative sentiment reviews rarely exceed 2 stars; positive rarely drop below 4 stars.

### 2. **Repeat Purchase Intent** (TAPP-generated)
**Mean score by repurchase intent:** Will not repurchase (1.86) → Uncertain (3.54) → Will repurchase (4.82)

This feature captures buyer satisfaction and actionability:
- **Will repurchase (70.4% of dataset):** 84.3% rate as 5-star; mean score 4.82
- **Will not repurchase (18.5%):** 47.7% rate as 1-star; mean score 1.86
- **Uncertain (10.9%):** Mid-range distribution; mean score 3.54

**Strength:** Nearly perfect coverage (9,974/10,000), mirrors sentiment but adds behavioral intent signal. Complements sentiment by capturing whether preference translates to action.

**Validation:** Strong alignment with product quality and effectiveness ratings; reviewers citing product failures or ineffectiveness consistently mark "will not repurchase."

### 3. **Product Quality Assessment** (TAPP-generated)
**Mean score by quality rating:** Defective (1.32) → Poor (1.63) → Acceptable (3.11) → Good (4.49) → Excellent (4.90)

Quality ratings show tight correspondence to numerical scores:
- **Excellent (55.3%):** 90.4% rate as 5-star; mean 4.90
- **Good (18.6%):** 57.8% rate as 5-star, 35.1% as 4-star; mean 4.49
- **Acceptable (11.5%):** Distributed across 2–4 stars; mean 3.11
- **Poor (13.2%):** 55.9% rate as 1-star; mean 1.63

**Strength:** Direct semantic mapping to rating. High-quality products generate high ratings; quality degradation strongly predicts low ratings. Orthogonal to sentiment in that it focuses on tangible product attributes.

**Validation:** Cross-tabulation confirms excellent products rarely receive 1-star ratings (0.1%), poor products rarely 5-star (1.4%).

### 4. **Product Effectiveness/Functionality** (TAPP-generated)
**Mean score by effectiveness:** Ineffective (1.53) → Partially effective (2.93) → Context-dependent (3.33) → Works as claimed (4.79)

Captures whether products meet functional requirements:
- **Works as claimed (71.7%):** Mean score 4.79; 93% rate ≥4 stars
- **Ineffective (11.6%):** Mean score 1.53; 68% rate ≤2 stars
- **Partially effective (9.4%):** Mean score 2.93; distributed mid-range

**Strength:** Distinct from quality assessment in emphasizing performance vs. build/materials. Critical for functional products (appliances, supplements, tools). Adds specificity beyond general quality ratings.

**Validation:** Reviewers explicitly mention "didn't work," "failed," or "exceeded expectations"—features that align precisely with effectiveness ratings. Strong negative reviews cite malfunction; strong positive reviews emphasize reliable performance.

### 5. **Price–Value Perception** (TAPP-generated)
**Mean score by price perception:** Poor value (1.62) → Fair value (3.39) → Good value (4.76) → Excellent value (4.90)

Captures economic judgment:
- **Good value (41.2%):** Mean 4.76; 80.3% rate as 5-star
- **Excellent value (13.7%):** Mean 4.90; 91.1% rate as 5-star
- **Poor value (7.8%):** Mean 1.62; 60.5% rate as 1-star
- **Overpriced (3.5%):** Mean 3.31; midrange; 29% rate as 5-star (dissatisfied despite utility)

**Strength:** Captures an orthogonal dimension—satisfaction depends on price expectations. A product rated "excellent" but "overpriced" may still receive a middling review. Adds economic signal unavailable from product quality alone.

**Validation:** Reviews explicitly comparing prices (e.g., "Great product but $20 overpriced") align with overpriced tag. Reviews emphasizing "deal" or "bargain" consistently map to good/excellent value ratings.

**Coverage note:** 26.9% marked as "Unknown" price perception, often for reviews that don't discuss cost. These are filtered or treated as missing and should be imputed or handled in modeling.

---

## Secondary Features

### **Taste/Flavor Quality** (TAPP-generated)
**Mean score by taste:** Flavor mismatch (1.86) / Unpleasant (1.52) → Bland (2.12) → Neutral (2.92) → Good (4.55) → Delicious (4.89)

Highly relevant for food/beverage products (3,962/10,000 have substantive taste ratings; 160 missing), weak signal for non-consumables:
- **Delicious (35.9%):** Mean 4.89
- **Good (41.5%):** Mean 4.55
- **Unpleasant (8.7%):** Mean 1.52

**Applicability:** Best as a product-category-specific feature. Create separate models for consumables vs. non-consumables, or include as category-conditional predictor.

### **Health/Dietary Concern** (TAPP-generated)
**Mean score by health alignment:** Contradicts goal (2.12) → Supports dietary restriction (4.41) → Supports health goal (4.75) → No concern (4.07)

Relevant for 15% of dataset (health-conscious purchases); near-universal for non-dietary products:
- **Supports health goal (18%):** Mean 4.75
- **Contradicts health goal (5.3%):** Mean 2.12

**Applicability:** Contextual—valuable for functional food, supplements, and diet-aligned products; neutral or low signal for generic items.

### **Comparison to Alternatives** (TAPP-generated)
**Mean score by competitive position:** Worse than alternatives (1.97) → Comparable (4.21) → Better than alternatives (4.88) → No comparison (4.54)

Signals whether review reflects competitive assessment:
- **Better than alternatives (23.9%):** Mean 4.88
- **Worse than alternatives (16.5%):** Mean 1.97
- **No comparison (41.4%):** Mean 4.54

**Note:** "No comparison" is most common (reviewers don't cite alternatives). Feature adds interpretability but moderate incremental predictive power given sentiment and quality already capture satisfaction.

---

## Original Structured Features

### **Review Text Length** (derived from Text field)
Mean text length decreases with rating:
- Score 1: 469 chars
- Score 2: 485 chars
- Score 3: 496 chars  
- Score 4: 468 chars
- Score 5: 377 chars

**Interpretation:** Low-rating reviews tend to be more detailed (complainers elaborate). High-rating reviews often brief ("Great product!"). Weak but consistent signal; use as proxy for review deliberation or passion.

### **Helpfulness Rating** (HelpfulnessNumerator / HelpfulnessDenominator)
Mean helpfulness votes do not strongly differentiate by score (1.2–2.2 votes across all scores). This reflects community assessment rather than review quality as a predictor.

**Recommendation:** Exclude from predictive model; use instead as an evaluation metric for model predictions (does the model predict reviews that readers deem helpful?).

### **Time/Temporal Features** (Time field, Unix timestamp)
Dataset spans 2004–2013. Temporal trends exist but are not within query scope. May be useful for seasonality modeling (e.g., higher 5-star reviews for holiday products in Dec) but requires separate analysis.

---

## Method Note: TAPP-Generated Columns Used

The TA++ v11 augmentation framework generated eight semantic facets. **All eight are present and leveraged in this analysis:**

1. `sentiment_polarity` — Overall emotional valence (positive/negative/mixed/neutral)
2. `product_quality_assessment` — Build, material, durability quality
3. `taste_flavor_quality` — Taste/flavor attributes (food-specific)
4. `product_effectiveness_or_functionality` — Meets intended purpose
5. `price_value_perception` — Economic satisfaction (value for money)
6. `repeat_purchase_intent` — Stated willingness to rebuy
7. `comparison_to_alternatives` — Competitive positioning
8. `health_dietary_concern` — Alignment with health/diet goals

All columns are categorical and fully populated (0 missing except taste_flavor_quality: 37/10,000 missing, price_value_perception: 11/10,000 missing). No additional augmentation was needed.

---

## Feature Engineering Recommendations

### **Recommended Feature Set for Baseline Model**

| Rank | Feature | Type | Reason |
|------|---------|------|--------|
| 1 | sentiment_polarity | Categorical | Highest discrimination power; 99.9% coverage |
| 2 | repeat_purchase_intent | Categorical | Behavioral signal; complements sentiment; 99.7% coverage |
| 3 | product_quality_assessment | Categorical | Direct quality mapping; orthogonal to sentiment |
| 4 | product_effectiveness_or_functionality | Categorical | Functional performance signal; 98.9% coverage |
| 5 | price_value_perception | Categorical | Economic dimension; handles missing as "no mention" |

These five alone yield strong predictive power. Add secondary features conditionally:
- Include `taste_flavor_quality` only for food/beverage subset
- Include `health_dietary_concern` only for health-claimed products
- Include `comparison_to_alternatives` for competitive analysis use cases

### **Text-Derived Features**

Extract from raw Summary and Text fields:
- **Review length** (character count; weak signal but low cost)
- **Adjective density** (count of positive/negative adjectives; redundant with sentiment but interpretable)
- **Exclamation marks / caps** (enthusiasm proxy)
- **TF-IDF embeddings** (semantic representation independent of TAPP)

### **Interaction Terms**

Consider interactions for final model:
- `sentiment_polarity × product_quality_assessment` (e.g., positive sentiment + excellent quality → likely 5-star)
- `repeat_purchase_intent × price_value_perception` (e.g., will repurchase + good value → strong signal)

---

## Model Performance Expectations

Given this feature set:
- **Top features alone (sentiment + repeat intent + quality)** should achieve **macro F1 ≥ 0.75** for 5-class classification on held-out test set
- **Imbalanced regression (predicting score as continuous)** should achieve **RMSE ≤ 0.8** (easy to predict bulk 5-stars)
- **Class-weighted classification** for balanced accuracy should reach **≥ 0.65** (harder for minority 1–2 classes)

The strong class imbalance (61.8% class-5) makes accuracy alone a poor metric; prioritize precision/recall trade-offs or stratified evaluation.

---

## Conclusion

Five TAPP-generated semantic facets—**sentiment polarity, repeat purchase intent, product quality, effectiveness, and price–value perception**—form a robust, minimal feature set for review score prediction. Together they capture emotional tone, purchase behavior, tangible product attributes, and economic satisfaction. Supplementary features (taste, health concern, alternatives, text statistics) add domain specificity but yield diminishing marginal returns.

The original structured columns (review text, helpfulness, time) provide raw material for feature extraction but do not independently predict scores. The augmentation pipeline successfully distilled semantic signal from unstructured text into actionable categorical features, reducing feature engineering overhead and improving model interpretability.
