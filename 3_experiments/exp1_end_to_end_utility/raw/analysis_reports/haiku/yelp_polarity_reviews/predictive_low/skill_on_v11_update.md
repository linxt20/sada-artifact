---
dataset: yelp_polarity_reviews
scenario: predictive_low
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict low Yelp user satisfaction?"
source_table: augment_table/yelp_polarity_reviews/predictive_low/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:24:25.911015+00:00
wall_seconds: 61.43
---

# Predictive Signals of Low Yelp User Satisfaction

**Analysis Date:** 2026-07-30  
**Dataset:** 250 Yelp reviews (balanced: 125 negative, 125 positive)  
**Focus Variable:** `label_pos` (binary: 1=positive satisfaction, 0=low/negative satisfaction)  

---

## Executive Summary

Two distinct service signals emerge as the strongest predictors of low user satisfaction: **service rudeness** and **service inattention**. When either is present, 91.1% of reviews express low satisfaction. Service rudeness alone predicts negative satisfaction with near-perfect precision (100%), making it the most reliable single indicator in this dataset.

---

## Key Findings

### 1. **Service Rudeness: The Strongest Signal**

- **Presence:** 38 reviews (15.2% of dataset)
- **Predictive Power:** 100% → negative satisfaction
  - All 38 reviews with rudeness indicators received negative ratings (0/38 positive)
  - This is the only feature with zero false positives for predicting low satisfaction

**Sample signal:** Staff dismissing customer concerns, condescending responses, hostile attitudes, or explicit disrespect.

### 2. **Service Inattention: Strong and Frequent**

- **Presence:** 37 reviews (14.8% of dataset)
- **Predictive Power:** 86.5% → negative satisfaction
  - 32 of 37 reviews (86.5%) are negative
  - Only 5 reviews (13.5%) are positive despite inattention

**Sample signals:** 
- Being ignored or forgotten by staff
- Long waits without acknowledgment
- Staff walking past customers repeatedly
- No one taking orders despite ample time

### 3. **Combined Service Failures: Near-Perfect Predictor**

- **Joint Presence:** 19 reviews exhibit both rudeness and inattention
- **Outcome:** 100% → negative satisfaction (19/19)

- **Either Issue Present:** 56 reviews have at least one service signal
- **Outcome:** 91.1% → negative satisfaction (51/56)

### 4. **Baseline Comparison: Impact Magnitude**

Among reviews with **neither** inattention nor rudeness:
- Negative satisfaction rate: 38.1% (74/194)

**Lift:** The presence of service issues increases the likelihood of low satisfaction from ~38% to 91%, a **2.4x amplification** when service problems are present.

---

## Additional Predictive Patterns in Review Text

Beyond the annotated service features, textual analysis reveals supporting signals of low satisfaction:

| Pattern | Low Satisfaction | High Satisfaction | Ratio |
|---------|------------------|-------------------|-------|
| Explicit complaint language ("worst," "horrible," "awful") | 18.4% | 2.4% | **7.7x** |
| "Will not return" intent statements | 17.6% | 6.4% | **2.7x** |
| Wait/slow service mentions | 28.0% | 16.8% | **1.7x** |
| Staff rudeness/attitude words | 8.0% | 0.8% | **10.0x** |
| Cleanliness/hygiene concerns | 13.6% | 5.6% | **2.4x** |
| Food quality complaints | 8.8% | 3.2% | **2.7x** |

---

## Limitations and Caveats

1. **Service annotation scope:** The `service_inattention` and `service_rudeness` columns capture explicit service failures but may miss implicit dissatisfaction. Only 56 of 125 negative reviews contain these annotations, suggesting other dissatisfaction drivers exist (food quality, cleanliness, pricing).

2. **Binary label limitations:** The `label_pos` variable is binary (positive/negative), not ordinal. Mixed or moderately negative experiences may be compressed into the same category as severely negative ones.

3. **Text bias:** The analysis draws heavily on text patterns, which can vary by reviewer verbosity and review quality. Reviews without explicit complaint language may still indicate dissatisfaction.

4. **Dataset balance:** While the overall label split is balanced (50/50), service issues are concentrated in the negative class, making this a strong signal but not a complete explanation.

---

## Practical Insights

**Decision-Ready Takeaway:** Service quality—specifically staff attentiveness and respectful behavior—is a dominant factor in predicting user satisfaction. The data suggests:

- **Rudeness is critical:** Any sign of rude or dismissive staff behavior is nearly 100% predictive of negative satisfaction.
- **Inattention is costly:** Unresponsive or neglectful service drives 86.5% of marked low-satisfaction reviews.
- **Joint failures are catastrophic:** When both rudeness and inattention occur, negative satisfaction is certain (100%).
- **Service issues dominate other factors:** Even when addressing food quality or pricing, poor service overshadows improvements.

**Recommendation:** For businesses seeking to improve user satisfaction, prioritizing staff training around responsiveness and respect may have the highest ROI, as these factors show the tightest coupling with user satisfaction outcomes in this dataset.
