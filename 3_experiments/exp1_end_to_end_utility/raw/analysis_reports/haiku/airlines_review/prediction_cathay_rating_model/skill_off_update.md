---
dataset: airlines_review
scenario: prediction_cathay_rating_model
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating_gt7"
query: "(Cathay MD) Build a model to organise/optimise routes and service so Overall Rating > 7."
source_table: augment_table/airlines_review/prediction_cathay_rating_model/haiku__skill_off_update.csv
generated_at: 2026-07-28T12:59:12.832616+00:00
wall_seconds: 101.35
---

# Cathay Pacific Route & Service Optimization Analysis
## Predictive Model for Overall Rating > 7

**Dataset:** haiku__skill_off_update.csv  
**Analysis Date:** 2026-07-28  
**Variant:** skill_off  
**Target Variable:** Overall Rating > 7

---

## Executive Summary

This analysis examines Cathay Pacific Airways flight reviews (n=744) to identify factors driving high customer ratings (>7) and optimize route and service strategies. Currently, **46.8% of flights achieve ratings above 7** (348/744), leaving substantial room for improvement.

### Key Finding
**Value for Money is the overwhelmingly dominant predictor** of high ratings, with a correlation of +0.877 and a 2.22-point differential between high and low-rated flights. This single factor outweighs all service quality metrics combined.

---

## Target Variable Performance

| Metric | Value |
|--------|-------|
| High Ratings (>7) | 348 flights (46.8%) |
| Low/Medium (≤7) | 396 flights (53.2%) |
| Rating Distribution | 1-10 scale, bimodal (peaks at 1 and 9-10) |
| **Actionability** | **Moderate**: Existing high performers show improvement is achievable |

---

## 1. Predictors of High Ratings: Ranked by Impact

### 1.1 Value For Money (Strongest, +2.22 point differential)
- **High-rated flights (>7):** 4.51/5.0 average
- **Low-rated flights (≤7):** 2.29/5.0 average
- **Insight:** This dominates customer perception. Perceived pricing fairness correlates far more strongly with overall satisfaction than specific service components.

### 1.2 Seat Comfort (+0.41 point differential)
- **High-rated:** 3.84/5.0
- **Low-rated:** 3.42/5.0
- **Insight:** Moderate impact; long-haul routes show particular pressure on this metric.

### 1.3 Food & Beverages (+0.29 point differential)
- **High-rated:** 3.40/5.0
- **Low-rated:** 3.11/5.0
- **Insight:** Secondary factor; absence of positive food mentions correlates with lower ratings.

### 1.4 Staff Service (+0.27 point differential)
- **High-rated:** 3.76/5.0
- **Low-rated:** 3.49/5.0
- **Insight:** Crew quality positively mentioned in 23.6% of high-rated reviews vs. 20.2% of low-rated.

### 1.5 Inflight Entertainment (+0.12 point differential)
- **High-rated:** 3.88/5.0
- **Low-rated:** 3.76/5.0
- **Insight:** Minimal predictor; engagement gaps between segments are negligible.

---

## 2. Route Performance & Optimization Opportunities

### 2.1 High-Performing Routes (75%+ high rating rate)

| Route | High Rating % | Avg Rating | Sample Size |
|-------|---|---|---|
| Hong Kong ↔ Taipei | 87.5% | 8.00 | 8 |
| Singapore ↔ Bangkok | 83.3% | 8.83 | 6 |
| Manila → Hong Kong | 80.0% | 8.60 | 10 |
| Hong Kong → San Francisco | 80.0% | 7.80 | 5 |
| Bangkok → Hong Kong | 71.4% | 7.93 | 14 |

**Pattern:** Medium-haul Intra-Asia routes dominate; flight duration and regional consistency appear supportive.

### 2.2 Problem Routes (50% or lower high rating rate)

| Route | High Rating % | Avg Rating | Sample Size |
|-------|---|---|---|
| **Asia-Australia (grouped)** | **28.6%** | **4.64** | **70** |
| Hong Kong ↔ London | 50-53% | 6.31-6.33 | 15-16 |
| Hong Kong ↔ Vancouver | 42.9% | 7.00 | 7 |

**Critical Finding:** Long-haul Asia-Australia routes show **severe underperformance** with only 28.6% high rating rate and average 4.64 rating. This represents Cathay's most fragile route segment.

### 2.3 Route Category Analysis

| Route Type | Flights | Avg Rating | High Rating % |
|---|---|---|---|
| Intra-Asia | 544 | 6.45 | 49.8% |
| Asia-Europe | 130 | 5.82 | 43.8% |
| **Asia-Australia** | **70** | **4.64** | **28.6%** |

**Interpretation:** Geographic distance and flight duration inversely correlate with satisfaction. Ultra-long-haul operations carry structural satisfaction challenges.

---

## 3. Service Class Impact

### 3.1 Performance by Cabin Class

| Class | Sample | Avg Rating | High Rating % |
|---|---|---|---|
| **Business** | 195 | **7.09** | **59.0%** ✓ |
| First | 16 | 7.38 | 50.0% |
| Premium Economy | 95 | 6.09 | 38.9% |
| Economy | 438 | 5.73 | 42.9% |

**Key Insight:** Business Class generates 59% high-rating rate (1.9× economy), indicating premium passengers have expectations better aligned with service delivery or greater value perception.

### 3.2 Business Class Performance by Route Type

| Route Type | Avg Rating | High Rating % | Seat Comfort | Value For Money |
|---|---|---|---|---|
| **Intra-Asia** | **7.37** | **62.6%** | 3.50 | 3.74 |
| Asia-Europe | 6.53 | 53.5% | 3.81 | 3.56 |
| **Asia-Australia** | **5.92** | **38.5%** | 3.46 | **3.15** |

**Critical Gap:** Business-class Asia-Australia service is failing premium expectations with a 24.1 percentage-point drop in high ratings vs. Intra-Asia.

---

## 4. Traveller Type Dynamics

| Segment | Sample | Avg Rating | High Rating % |
|---|---|---|---|
| Solo Leisure | 328 | 6.68 | 54.0% |
| Business | 129 | 5.83 | 42.6% |
| Family Leisure | 128 | 5.97 | 44.5% |
| Couple Leisure | 159 | 5.56 | 37.1% |

**Insight:** Solo travelers show highest satisfaction (54%), while couples show lowest (37.1%). Business travelers underperform vs. their premium pricing tier, suggesting unmet premium expectations.

---

## 5. Review Text Evidence

### 5.1 High-Rated Flight Characteristics (>7)
- **Service excellence keywords:** Present in 29.6% of reviews
- **Disruption mentions:** Only 14.9% (vs. 30.1% in low-rated)
- **Comfort complaints:** Rare (2.6% mention discomfort issues)

### 5.2 Low-Rated Flight Characteristics (≤7)
- **Delay/disruption keywords:** Present in 30.1% of reviews
- **Crew quality issues:** 20.2% mention crew
- **Comfort complaints:** 9.8% report comfort problems

**Interpretation:** Operational reliability (avoiding delays) and crew consistency are hygiene factors; absence of complaints is more predictive than presence of praise.

---

## 6. Predictive Model Implications

### 6.1 Feature Engineering Recommendations

Based on the augmented schema design (CabinCrewServiceQuality, FlightDisruptionType, ValueForMoneyPerception, etc.), a model should prioritize:

1. **Value perception module** (highest weight):
   - Pricing logic relative to route type
   - Premium class tier satisfaction gaps
   - Long-haul cost-of-service perception

2. **Operational reliability** (second priority):
   - Flight disruption flags (delays, cancellations, diversions)
   - Disruption handling quality scoring

3. **Comfort/service consistency** (tertiary):
   - Route-specific seat comfort expectations
   - Staff service consistency across legs
   - Food quality relative to route duration

### 6.2 Model Challenges

- **Class imbalance within routes:** Asia-Australia (n=70) is severely under-indexed
- **Service consistency signal:** Review text suggests subjective crew quality variance not fully captured
- **Long-haul structural limits:** Inherent fatigue and expectation management issues on ultra-long-haul may cap achievable rating improvement to ~50-60% vs. Intra-Asia ~65%

---

## 7. Actionable Recommendations for Route/Service Optimization

### Priority 1: Asia-Australia Route Intervention
- **Current state:** 28.6% high-rating rate (critical failure)
- **Action:** Audit operational procedures on HKG-SYD, HKG-MEL
- **Focus areas:** Value-for-money perception, seat comfort consistency, crew service standards on longest segments
- **Success metric:** Increase to 45%+ high-rating rate (still below Intra-Asia but defensible)

### Priority 2: Long-Haul Value Recalibration
- **Current state:** Asia-Europe (43.8%) underperforms Intra-Asia (49.8%)
- **Action:** Review pricing strategy and expectation-setting relative to 13-16 hour flight duration
- **Consider:** Enhanced amenities, food/beverage refresh for value perception
- **Success metric:** Align Europe performance to 50%+

### Priority 3: Business Class Experience Parity
- **Current state:** Business on Asia-Australia = 5.92; Business on Intra-Asia = 7.37
- **Gap:** 1.45 rating points; 24 percentage-point high-rating difference
- **Action:** Premium class should not regress by route; maintain consistent premium experience
- **Success metric:** Business class minimum 55% high rating rate across all routes

### Priority 4: Couples Segment Engagement
- **Current state:** 37.1% high-rating rate (lowest segment)
- **Action:** Investigate whether couples are more price-sensitive or have unmet expectations
- **Potential:** Couple-specific amenities or communication around value proposition
- **Success metric:** Increase to 45%+

---

## 8. Data Quality & Model Limitations

### 8.1 Constraints Observed
- Augmented columns (specified in GT.json) are not present in this dataset variant
- Variant label "skill_off" suggests augmentation features were not generated
- Analysis relies entirely on original 17 columns + derived metrics

### 8.2 Evidence Grounding
- Findings grounded in concrete column distributions (Overall Rating, Service Scores, Route, Class)
- Sample sizes for low-volume routes (n<5) noted; conclusions drawn only on routes with n≥5
- Keyword analysis on review text is pattern-based, not exhaustive NLP

### 8.3 Exceptions & Caveats
- First Class (n=16) shows high avg rating (7.38) but small sample; not reliable for optimization
- Asia-Australia routes (n=70) have sufficient sample to flag as problem area but may include seasonal/operational variation
- Value For Money perception may reflect survivor bias (dissatisfied customers may not complete reviews)

---

## 9. Conclusion

To achieve **Overall Rating > 7 across Cathay Pacific's network**, optimize in this sequence:

1. **Address Value For Money perception** (2.22-point leverage): This is the dominant driver. Ensure long-haul routes (especially Asia-Australia) are priced fairly relative to service delivery.

2. **Fix Asia-Australia performance** (operational audit): 28.6% high rating is untenable; root cause analysis required on crew, fleet, or turnaround procedures.

3. **Standardize Business Class experience** (premium consistency): Business should not degrade by 24 points between route types.

4. **Maintain Intra-Asia excellence** (preserve 62%+ high rating): These routes set the gold standard; replicate their operational model globally.

**Current achievable baseline:** 46.8% (348/744 flights). **Realistic target:** 55-60% with focused interventions; 65%+ would require structural changes to ultra-long-haul operations or pricing model.
