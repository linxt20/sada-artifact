---
dataset: amazon_fine_food_review
scenario: predictive_score_features
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "review_score"
query: "What features can be extracted to train a model to predict a review's score?"
source_table: augment_table/amazon_fine_food_review/predictive_score_features/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:08:20.825334+00:00
wall_seconds: 60.04
---

# Predictive Features for Amazon Fine Food Review Scores

## Executive Summary

This analysis identifies features that can effectively train a predictive model for Amazon Fine Food review scores. The dataset contains **10,000 reviews** with a target variable (Score) ranging from 1–5 stars, complemented by **10 manually-extracted categorical and boolean features** derived from review text and metadata. These features demonstrate strong predictive power through clear, measurable relationships with review scores.

---

## Dataset Overview

- **Total records**: 10,000 reviews
- **Target variable**: Score (1–5 scale)
- **Score distribution**: Highly imbalanced (61.8% are 5-star reviews)
  - 5 stars: 6,183 (61.8%)
  - 4 stars: 1,433 (14.3%)
  - 1 star: 932 (9.3%)
  - 3 stars: 862 (8.6%)
  - 2 stars: 590 (5.9%)

---

## Extracted Predictive Features

### 1. **Sentiment Polarity** (Categorical)
Strong discriminative power across score levels:
- **Positive sentiment**: avg. score 4.83 (7,001 reviews)
- **Neutral sentiment**: avg. score 3.82 (72 reviews)
- **Mixed sentiment**: avg. score 3.58 (1,058 reviews)
- **Negative sentiment**: avg. score 1.84 (1,868 reviews)

**Insight**: Sentiment polarity shows the clearest separation. Reviews with positive sentiment average 3 points higher than negative reviews.

### 2. **Product Quality Assessment** (Categorical)
Categorical evaluation of overall product quality:
- **Excellent**: avg. score 4.89 (5,630 reviews)
- **Good**: avg. score 4.48 (1,747 reviews)
- **Acceptable**: avg. score 3.13 (1,164 reviews)
- **Poor**: avg. score 1.61 (1,300 reviews)
- **Defective**: avg. score 1.33 (146 reviews)

**Insight**: Quality perception is a strong predictor with monotonic relationship to scores. Defective products consistently receive low scores.

### 3. **Taste/Flavor Experience** (Categorical, 8.3% missing)
Specific sensory evaluation of taste:
- **Excellent taste**: avg. score 4.88 (4,113 reviews)
- **Good taste**: avg. score 4.55 (3,213 reviews)
- **Acceptable taste**: avg. score 3.04 (957 reviews)
- **Poor taste**: avg. score 1.59 (1,038 reviews)
- **Bland/flavorless**: avg. score 2.00 (85 reviews)

**Insight**: High predictive value for food-focused reviews. Missing values (likely reviews without taste commentary) average 3.07 stars.

### 4. **Sensory Assessment** (Categorical)
Broader sensory experience (texture, aroma, mouthfeel):
- **Pleasant**: avg. score 4.84 (6,633 reviews)
- **Acceptable**: avg. score 3.61 (1,406 reviews)
- **Off-profile**: avg. score 4.02 (306 reviews)
- **Unpleasant**: avg. score 1.76 (1,645 reviews)

**Insight**: Sensory quality strongly separates high-rating (5-star) from low-rating (1-star) reviews.

### 5. **Repeat Purchase Intent** (Categorical)
Explicit repurchase signal extracted from review text:
- **Will repurchase**: avg. score 4.84 (6,821 reviews)
- **May repurchase**: avg. score 3.68 (1,237 reviews)
- **Will not repurchase**: avg. score 1.85 (1,861 reviews)

**Insight**: Among the strongest predictors. Repurchase intent typically mirrors overall satisfaction.

### 6. **Price-Value Assessment** (Categorical, 0.2% missing)
Perception of value relative to cost:
- **Excellent value**: avg. score 4.89 (1,172 reviews)
- **Good value**: avg. score 4.78 (4,530 reviews)
- **Fair value**: avg. score 3.48 (813 reviews)
- **Poor value**: avg. score 1.84 (1,045 reviews)
- **Overpriced**: avg. score 3.26 (194 reviews)

**Insight**: Price-value perception is a significant predictor. Interestingly, "overpriced" (3.26) scores higher than "poor value" (1.84), suggesting separate evaluation dimensions.

### 7. **Product Defect or Issue** (Boolean)
Presence/absence of reported defects (damage, malfunction, contamination):
- **No defect reported**: avg. score 4.63 (7,783 reviews, 77.8%)
- **Defect reported**: avg. score 2.38 (2,217 reviews, 22.2%)

**Insight**: 2.25-point score gap. Defect presence is a strong categorical separator with practical significance.

### 8. **Expectation Fit** (Categorical)
Alignment between actual product and reviewer's pre-purchase expectations:
- **Exceeded expectations**: avg. score 4.89 (5,667 reviews)
- **Met expectations**: avg. score 4.45 (1,752 reviews)
- **Partially met expectations**: avg. score 3.23 (876 reviews)
- **Unmet expectations**: avg. score 1.74 (1,674 reviews)

**Insight**: Directly measures satisfaction relative to baseline. 3.15-point gap between exceeded and unmet expectations.

### 9. **Comparison to Alternatives** (Categorical)
Whether reviewer contextualized the product against competitors:
- **Favorable vs. competitor**: avg. score 4.76 (3,316 reviews)
- **No comparison made**: avg. score 4.26 (4,935 reviews)
- **Neutral alternative**: avg. score 3.67 (436 reviews)
- **Unfavorable vs. competitor**: avg. score 2.23 (1,312 reviews)

**Insight**: Comparative framing indicates satisfaction (favorable: 4.76) vs. disappointment (unfavorable: 2.23). Reviews without comparisons trend toward middle-ground scores.

### 10. **Health/Dietary Concern** (Boolean)
Presence of health or dietary consideration:
- **No concern**: avg. score 4.12 (7,494 reviews)
- **Concern present**: avg. score 4.17 (2,505 reviews)

**Weakness**: Minimal discriminative power (0.05-point difference). Not a strong predictor in isolation.

---

## Supporting Numeric Features

### Helpfulness Metrics
- **Helpfulness ratio** (HelpfulnessNumerator ÷ HelpfulnessDenominator):
  - Weak predictor; only marginal variation (0.32–0.41 across scores)
  - High sparsity: 75% of reviews have zero denominator votes

- **Review recency** (Time):
  - No clear correlation with score; included for temporal modeling if needed

---

## Feature Quality Assessment

| Feature | Predictive Strength | Coverage | Type |
|---------|-------------------|----------|------|
| Sentiment Polarity | Very Strong | 100% | Categorical (5 levels) |
| Product Quality | Very Strong | 100% | Categorical (6 levels) |
| Taste/Flavor | Strong | 91.7% | Categorical (7 levels) |
| Sensory Assessment | Very Strong | 100% | Categorical (5 levels) |
| Repeat Purchase Intent | Very Strong | 99.2% | Categorical (4 levels) |
| Price-Value Assessment | Very Strong | 99.8% | Categorical (5 levels) |
| Expectation Fit | Very Strong | 100% | Categorical (5 levels) |
| Comparison to Alternatives | Strong | 99.99% | Categorical (5 levels) |
| Product Defect/Issue | Very Strong | 100% | Boolean |
| Health/Dietary Concern | Weak | 99.99% | Boolean |

---

## Key Patterns & Insights

1. **Strong Polarity**: Most extracted features show monotonic relationships to scores. Low-score reviews (1–2) cluster around negative values; high-score reviews (4–5) around positive values. The 3-star band (moderate reviews) is thin and mixed.

2. **Sentiment Dominance**: Overall sentiment polarity is the simplest proxy, but granular features (quality, taste, sensory) provide richer modeling capacity and handle nuance (e.g., "acceptable" vs. "poor").

3. **Dual Pathways to Low Scores**:
   - **Product failure pathway**: product_defect_or_issue=True, product_quality_assessment=poor/defective
   - **Expectation mismatch pathway**: expectation_fit=unmet, repeat_purchase_intent=will_not_repurchase

4. **Inverse Scaling**: High-quality assessments (excellent, good) consistently yield average scores ≥4.4; poor assessments ≤1.6. This 3-point spread is substantial and actionable.

5. **Boolean Feature Limitation**: Health/dietary concern is too weak as a standalone feature; its predictive value likely depends on contextual interaction with sentiment or defect flags.

---

## Recommendations for Model Training

1. **Feature engineering**:
   - Use all 9 strong features (exclude or downweight health_dietary_concern).
   - Consider interaction terms: e.g., (product_quality × expectation_fit) for edge cases.
   - One-hot encode categorical features; keep boolean as-is.

2. **Class balance**:
   - Dataset is heavily skewed toward 5-star reviews (61.8%). Consider weighted loss functions or stratified sampling.

3. **Missing values**:
   - Taste/flavor is 8.3% missing; impute with mode or treat as separate category (e.g., "not_mentioned").

4. **Baseline performance**:
   - A simple rule (if sentiment=positive, predict 4–5; if negative, predict 1–2) likely achieves >75% accuracy due to feature strength.

---

## Conclusion

The extracted features provide **strong, interpretable, and actionable signals** for predicting review scores. Sentiment polarity, product quality, sensory assessments, repurchase intent, and expectation fit form a robust core. Models trained on these features should achieve high accuracy in distinguishing extreme scores (1 vs. 5) and can be refined further through interaction terms and ensemble methods for improved mid-range discrimination (3–4 stars).
