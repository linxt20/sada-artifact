---
dataset: amazon_polarity_reviews
scenario: predictive_negative
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict negative Amazon product satisfaction?"
source_table: augment_table/amazon_polarity_reviews/predictive_negative/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:10:09.659560+00:00
wall_seconds: 112.04
---

# Analysis Report: Review Signals Predicting Negative Amazon Product Satisfaction

## Executive Summary

This analysis identifies key linguistic and semantic signals that predict negative Amazon product reviews using an augmented dataset combining original review text features with TAPP-generated semantic dimensions. The findings reveal that **negative reviews are characterized by a constellation of emotional and evaluative signals**, with disappointment and frustration/annoyance serving as nearly universal markers (96.8% and 91.2% prevalence respectively among negative reviews), while waste/loss framing and product comparisons appear in specific frustration contexts.

## Dataset Overview

- **Total reviews analyzed:** 250 (balanced binary classification)
- **Negative reviews (label_pos=0):** 125
- **Positive reviews (label_pos=1):** 125

## Methodology Note

This analysis employs both original structured features and five TAPP-generated semantic columns from the augmented table:
1. `disappointment_signal` (Boolean)
2. `frustration_or_annoyance_tone` (Categorical: high_frustration, moderate_annoyance, sarcasm_or_irony, not_present)
3. `waste_or_resource_loss_framing` (Boolean)
4. `personal_inconvenience_or_burden` (Categorical: not_present, repeated_effort_required, incompatibility_with_need, logistical_burden, health_or_safety_risk)
5. `explicit_product_comparison` (Categorical: not_present, comparison_to_expectations, comparison_to_competitor, comparison_to_prior_model)

These TAPP facets complement original review content analysis and are cited by their exact column names when central to claims.

---

## Primary Findings

### 1. Disappointment Signal: Nearly Universal Marker of Negative Sentiment

**Disappointment_signal** is the strongest univariate predictor of negative reviews:

| Metric | Negative Reviews | Positive Reviews | Difference |
|--------|-----------------|-----------------|------------|
| Presence (True) | 114/125 (91.2%) | 7/125 (5.6%) | **85.6 pp** |

This 85.6 percentage-point differential demonstrates that disappointment framing is a robust and nearly deterministic signal of negative satisfaction. Only 11 negative reviews lack explicit disappointment signals, while positive reviews rarely express disappointment (5.6%).

**Interpretation:** Negative reviews predominantly articulate unmet expectations or unsatisfactory product performance through language of disappointment. This semantic marker reliably distinguishes dissatisfied from satisfied customers.

---

### 2. Frustration and Annoyance Tone: High-Intensity Emotional Signal

The `frustration_or_annoyance_tone` dimension reveals emotional intensity stratification:

#### Distribution in Negative Reviews:
| Tone Type | Count | Percentage |
|-----------|-------|-----------|
| High frustration | 76 | 60.8% |
| Moderate annoyance | 43 | 34.4% |
| Sarcasm/irony | 2 | 1.6% |
| Not present | 4 | 3.2% |

#### Distribution in Positive Reviews:
| Tone Type | Count | Percentage |
|-----------|-------|-----------|
| Not present | 107 | 85.6% |
| Moderate annoyance | 16 | 12.8% |
| Sarcasm/irony | 2 | 1.6% |
| High frustration | 0 | 0.0% |

**Key observations:**
- **High frustration** appears exclusively in negative reviews (76/125, 60.8%) with zero occurrence in positive reviews
- 96.8% of negative reviews contain some form of frustration/annoyance signal
- Positive reviews maintain emotional neutrality 85.6% of the time

This stark contrast demonstrates that **high-frustration tone is a perfect discriminator**: its presence strongly predicts negative reviews, and its complete absence from the positive sample indicates frustrated language is incompatible with satisfaction expression.

---

### 3. Waste and Resource Loss Framing: Amplifying Signal in Specific Contexts

The `waste_or_resource_loss_framing` variable captures a secondary but important negative frame:

| Metric | Negative Reviews | Positive Reviews |
|--------|-----------------|-----------------|
| Presence (True) | 31/125 (24.8%) | 0/125 (0.0%) |

**Distribution context:** Among the 76 high-frustration negative reviews:
- 27 include waste/loss framing (35.5%)
- This suggests high frustration reviews frequently emphasize financial, time, or functional loss

**Exemplar signals:** Negative reviews mention "waste of time," "waste of money," product failure as "junk," and unrecoverable investments. This framing amplifies dissatisfaction by extending the complaint from product failure to broader resource loss.

**Significance:** The 24.8% prevalence in negative reviews and 0% in positive reviews indicates that waste/loss framing is a **strong amplifier of negative sentiment** when combined with frustration and disappointment.

---

### 4. Personal Inconvenience and Burden: Friction Points in Customer Experience

The `personal_inconvenience_or_burden` dimension identifies specific friction types:

#### Negative Reviews (n=125):
| Burden Type | Count | Percentage |
|------------|-------|-----------|
| Not present | 67 | 53.6% |
| Repeated effort required | 29 | 23.2% |
| Incompatibility with need | 13 | 10.4% |
| Logistical burden | 11 | 8.8% |
| Health or safety risk | 5 | 4.0% |

#### Positive Reviews (n=125):
| Burden Type | Count | Percentage |
|------------|-------|-----------|
| Not present | 111 | 88.8% |
| Repeated effort required | 8 | 6.4% |
| Incompatibility with need | 4 | 3.2% |
| Logistical burden | 2 | 1.6% |

**Pattern interpretation:**
- 46.4% of negative reviews cite tangible burdens (vs. 11.2% of positive reviews)
- **Repeated effort required** (23.2%) dominates, indicating products requiring warranty work, returns, or troubleshooting
- **Incompatibility with need** (10.4%) reflects products failing to meet intended use cases
- **Health/safety concerns** (4.0%), though rare, constitute critical negative signals

This dimension captures operational friction often absent from high-level satisfaction discourse. It represents the "effort tax" imposed by problematic products.

---

### 5. Explicit Product Comparison: Contextual Evaluation Framework

The `explicit_product_comparison` variable reveals how negative reviews situate products within competitive or expectation contexts:

#### Negative Reviews (n=125):
| Comparison Type | Count | Percentage |
|-----------------|-------|-----------|
| Not present | 54 | 43.2% |
| Comparison to expectations | 36 | 28.8% |
| Comparison to competitor | 19 | 15.2% |
| Comparison to prior model | 16 | 12.8% |

#### Positive Reviews (n=125):
| Comparison Type | Count | Percentage |
|-----------------|-------|-----------|
| Not present | 80 | 64.0% |
| Comparison to expectations | 16 | 12.8% |
| Comparison to prior model | 15 | 12.0% |
| Comparison to competitor | 14 | 11.2% |

**Strategic insight:** 56.8% of negative reviews include explicit comparisons, significantly higher than the 36.0% rate in positive reviews. Negative reviewers frequently:
1. **Compare to expectations** (28.8%): express gap between promised and delivered performance
2. **Compare to competitors** (15.2%): identify superior alternatives
3. **Compare to prior models** (12.8%): document product quality regression

This suggests negative reviewers employ comparative reasoning to substantiate dissatisfaction, strengthening their critique through external reference points.

---

## Multi-Signal Synergies: How Negative Signals Co-Occur

The most predictive signal combinations reveal how disappointment interacts with other dimensions:

| Signal Combination | Negative Reviews | Percentage |
|-------------------|-----------------|-----------|
| Disappointment + High Frustration | 75/125 | 60.0% |
| Disappointment + Moderate Annoyance | 37/125 | 29.6% |
| Disappointment + Comparison (any type) | 67/125 | 53.6% |
| Disappointment + Inconvenience/Burden | 57/125 | 45.6% |
| Disappointment + Waste/Loss Framing | 31/125 | 24.8% |

**Pattern synthesis:**
- Core signal: **91.2% of negative reviews show disappointment**
- Enhanced by frustration: **89.6% show disappointment + some frustration tone**
- Substantiated by comparison: **53.6% add comparative context**
- Amplified by burden: **45.6% document specific inconveniences**

Among the 76 high-frustration reviews, 51.3% cite inconvenience/burden and 51.3% include product comparisons, demonstrating that high frustration reviews systematically combine emotional intensity with evidence-based critique.

---

## Predictive Model Implications

### Strongest Discriminators (by differential prevalence):

1. **Disappointment_signal (91.2% vs. 5.6%):** 85.6 pp advantage → Essential primary signal
2. **High frustration tone (60.8% vs. 0.0%):** 60.8 pp advantage → Perfect separator
3. **Waste/loss framing (24.8% vs. 0.0%):** 24.8 pp advantage → Rare but definitive
4. **Inconvenience/burden (46.4% vs. 11.2%):** 35.2 pp advantage → Strong secondary signal
5. **Product comparison (56.8% vs. 36.0%):** 20.8 pp advantage → Moderate amplifier

### Interpretation for NLP Classification:

A hierarchical signal model would weight:
- **Tier 1 (Essential):** disappointment_signal + frustration_or_annoyance_tone ≠ "not_present"
  - 96.8% coverage of negative reviews
  - Near-zero false positive rate
- **Tier 2 (Reinforcing):** waste_or_resource_loss_framing, personal_inconvenience_or_burden presence
  - 24.8%-46.4% additional coverage
  - High specificity (minimal positive review overlap)
- **Tier 3 (Substantiating):** explicit_product_comparison presence
  - 56.8% of negative reviews; contextual value

---

## Boundary Cases and Limitations

**Negative reviews without expected signals (n=11):**
- 4 reviews (3.2%) lack frustration tone while maintaining disappointment signal
- These rare cases likely represent measured, quiet dissatisfaction (e.g., "disappointed... but will try again")

**Positive reviews with frustration/annoyance (n=18):**
- 16 show moderate annoyance only (no high frustration)
- Likely context: Mild reservations expressed within primarily positive appraisals (e.g., "Great except for...")
- Demonstrates that tone intensity (high vs. moderate) is critical for discrimination

**Comparison signal presence in both groups:**
- Both negative (56.8%) and positive (36.0%) reviews use comparisons
- Comparative framing alone is insufficient; it must combine with disappointment/frustration for negative prediction

---

## Conclusion

Review signals predictive of negative Amazon product satisfaction follow a **primary-secondary-tertiary hierarchy**:

1. **Primary signal (nearly deterministic):** `disappointment_signal` combined with `frustration_or_annoyance_tone` (96.8% of negative reviews) with high frustration being exclusive to negative sentiment

2. **Secondary signals (high specificity):** `waste_or_resource_loss_framing` (24.8% negative, 0% positive) and `personal_inconvenience_or_burden` (46.4% negative, 11.2% positive), which amplify or document the primary emotional signal

3. **Tertiary signals (substantiating context):** `explicit_product_comparison` (56.8% negative, 36% positive), which provides comparative evidence within negative reviews but requires pairing with primary signals for reliable prediction

**Key predictive insight:** Negative satisfaction is characterized by the **combination of emotional intensity (frustration) with cognitive processing (disappointment, comparison, documented burden)**. This multi-dimensional signal constellation—not any single facet—defines negative review sentiment.
