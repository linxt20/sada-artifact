---
dataset: yelp_polarity_reviews
scenario: predictive_low
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict low Yelp user satisfaction?"
source_table: augment_table/yelp_polarity_reviews/predictive_low/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:26:23.824372+00:00
wall_seconds: 34.25
---

# Review Signals Predicting Low Yelp User Satisfaction

## Dataset Overview
- **Total reviews**: 250
- **Low satisfaction (label=0)**: 125 reviews
- **High satisfaction (label=1)**: 125 reviews
- **Analysis variant**: skill_off

## Key Predictive Signals for Low Satisfaction

### 1. **Negative Word Density (Strongest Predictor)**
- **Low satisfaction mean**: 1.08 negative words per review
- **High satisfaction mean**: 0.30 negative words per review
- **Correlation**: -0.3654 (strong inverse correlation)
- **Signal**: Reviews flagged as dissatisfactory contain **3.6× more negative vocabulary** on average, making word choice the most reliable linguistic marker of low satisfaction.

### 2. **Complaint Phrase Frequency (Strongest Predictor)**
- **Low satisfaction mean**: 0.50 complaint phrases per review
- **High satisfaction mean**: 0.04 complaint phrases per review
- **Correlation**: -0.3659 (strong inverse correlation)
- **Signal**: Low satisfaction reviews explicitly reference complaints at **12.5× the rate** of high satisfaction reviews. Even a single complaint phrase is predictive.

### 3. **Pricing or Refund Complaints (High Specificity)**
- **Low satisfaction prevalence**: 6.4% (8 of 125 reviews)
- **High satisfaction prevalence**: 0% (0 of 125 reviews)
- **Signal**: The presence of pricing or refund complaints is a **strong negative signal**—no high satisfaction reviews mentioned these issues, while 6.4% of dissatisfactory reviews did.

### 4. **Comparison Mentions (Moderate Predictor)**
- **Low satisfaction prevalence**: 17.6% (22 of 125 reviews)
- **High satisfaction prevalence**: 9.6% (12 of 125 reviews)
- **Correlation**: -0.1167
- **Signal**: References to competitor products or alternative options occur 1.8× more often in dissatisfactory reviews, suggesting reviewers use comparisons to justify low ratings.

### 5. **Excessive Capitalization (Weak to Moderate Predictor)**
- **Low satisfaction prevalence**: 7.2% (9 of 125 reviews)
- **High satisfaction prevalence**: 2.4% (3 of 125 reviews)
- **Correlation**: -0.1123
- **Signal**: Excessive caps appear roughly 3× more often in low satisfaction reviews, though the absolute prevalence remains low (only 4.8% of all reviews).

### 6. **Exclamation Mark Usage (Counterintuitive)**
- **Low satisfaction mean**: 0.79 exclamation marks
- **High satisfaction mean**: 1.18 exclamation marks
- **Correlation**: +0.1156 (positive, slightly favors satisfaction)
- **Signal**: Exclamation marks are **more frequent in satisfied reviews**, likely expressing enthusiasm rather than frustration. This is not a strong predictor of low satisfaction.

### 7. **Review Length (Weak Predictor)**
- **Low satisfaction mean**: 91.3 words
- **High satisfaction mean**: 84.7 words
- **Correlation**: -0.0837
- **Signal**: Dissatisfied reviewers write slightly longer reviews on average, possibly to elaborate on issues. The difference is modest (6.6 words) and not a strong discriminator.

## Interpretation for Yelp Satisfaction Prediction

**Strongest predictors of low user satisfaction:**
1. High density of negative vocabulary (3.6× higher in low satisfaction reviews)
2. Explicit complaint phrases (12.5× higher in low satisfaction reviews)
3. Pricing/refund grievances (exclusive to low satisfaction set)

**Moderate predictors:**
- Comparisons to alternatives (1.8× higher in low satisfaction)
- Excessive capitalization (3× higher in low satisfaction)

**Weak/unreliable predictors:**
- Exclamation mark frequency (counterintuitively higher in satisfied reviews)
- Review word length (minimal predictive value)

## Recommendations for Application

For predicting low Yelp satisfaction, prioritize the linguistic features with the strongest signal-to-noise ratio:
- **Negative word count** and **complaint phrase count** are the most reliable quantitative signals
- **Pricing complaints** are rare but 100% specific to dissatisfaction
- Traditional markers like exclamation marks and review length should be weighted lower or deprioritized
