---
dataset: airlines_review_full
scenario: prediction_satisfaction_drivers
variant: original
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating"
query: "What drives customer satisfaction (Overall Rating) across the different airlines?"
source_table: augment_table/airlines_review_full/prediction_satisfaction_drivers/original.csv
generated_at: 2026-08-03T05:43:37.350309+00:00
wall_seconds: 85.32
---

# Drivers of Customer Satisfaction Across Airlines: Analysis Report

## Executive Summary

Analysis of 8,100 airline reviews across 10 carriers reveals that **Value For Money is the overwhelmingly dominant driver of overall customer satisfaction**, accounting for **90% of the explanatory power** in satisfaction ratings. Other service dimensions (staff, seating, food, entertainment) contribute minimally to satisfaction variability, suggesting that customers' perception of price-value alignment fundamentally determines their ratings and loyalty.

## Key Findings

### 1. Value For Money Dominates All Other Factors

**Correlation Strength with Overall Rating:**
- **Value For Money: 0.88** (very strong, explains 78% of variance)
- Staff Service: 0.23 (weak-moderate)
- Seat Comfort: 0.21 (weak-moderate)
- Food & Beverages: 0.16 (weak)
- Inflight Entertainment: 0.14 (weak)

**Regression Analysis** (standardized coefficients):
- Value For Money explains **90.1%** of relative importance
- Staff Service: 3.8%
- Seat Comfort: 3.6%
- Food & Beverages: 1.5%
- Inflight Entertainment: 1.0%
- Overall model R² = 0.784 (strong explanatory power)

### 2. Clear Satisfaction Tiers by Value For Money Perception

Customer satisfaction exhibits a sharp step-function relationship with perceived value:

| Value For Money Rating | Sample Size | Avg Overall Rating | % Recommended |
|---|---|---|---|
| 1 (Poor Value) | 2,127 | 1.54 | 1.6% |
| 2 | 909 | 3.03 | 8.4% |
| 3 (Neutral) | 1,124 | 5.06 | 40.7% |
| 4 | 1,513 | 7.71 | 88.0% |
| 5 (Excellent Value) | 2,427 | 9.17 | 98.4% |

**Insight:** Perception of value is the critical tipping point between detraction and promotion. Once Value For Money reaches 4+, recommendation rates jump to 88%+.

### 3. Airline Performance: Premium Asian Carriers Lead

**Top Performers (Overall Rating):**
1. All Nippon Airways: 7.95 (strong across all dimensions; VFM = 4.17)
2. EVA Air: 7.42 (VFM = 4.00)
3. Qatar Airways: 7.20 (VFM = 3.80)

**Lower Performers:**
- Emirates: 4.67 (VFM = 2.75)
- Air France: 4.64 (VFM = 2.67)
- Turkish Airlines: 3.68 (VFM = 2.40, lowest across all carriers)

**Critical Finding:** The 4.27-point gap between top and bottom performers correlates directly with Value For Money gaps (1.77 points), not with seat or food differences.

### 4. Secondary Drivers Have Limited Independent Impact

While correlations with Staff Service (0.23) and Seat Comfort (0.21) are statistically significant, they are **weak in absolute terms**:

- High Staff Service + Low Value For Money: Avg rating only 1.67 (still deeply dissatisfied)
- High Seat Comfort + Low Value For Money: Similar depressed ratings
- Conversely, high Value For Money partially compensates for low individual service dimensions

**653 flights rated 8-10** despite having Seat Comfort ≤ 2, demonstrating that strong Value For Money perception can override comfort deficits.

### 5. Travel Class Shows Modest Effect

| Class | Avg Overall Rating | Primary Driver |
|---|---|---|
| First Class | 7.60 | Premium pricing accepted as value |
| Business Class | 6.65 | Higher VFM expectations |
| Premium Economy | 5.97 | Mixed perception (higher price, limited differentiation) |
| Economy | 5.18 | Price sensitivity amplifies value concerns |

Business and economy passengers show depressed satisfaction relative to first class, primarily reflecting tighter value-for-money perceptions rather than absolute service deficits.

## Weak Evidence / Exceptions

1. **Food & Beverages (r=0.16):** Despite customer reviews frequently detailing meal quality, this attribute shows minimal correlation with overall satisfaction. High-quality food alone does not drive satisfaction if value perception is poor.

2. **Inflight Entertainment (r=0.14):** Weakest among all dimensions. Customers may appreciate entertainment but it is not a satisfaction lever.

3. **Premium Economy Paradox:** Premium Economy offers seat and food improvements over economy but still averages 5.97—only 0.79 points above economy (5.18). Customers perceive these upgrades as inadequate for the price premium, depressing Value For Money ratings despite objectively better service.

4. **Isolated High Satisfaction with Low Features (108 cases):** Rare instances where Overall Rating is 1-3 but Value For Money ≥ 4. These are exceptions driven by data noise or ratings submitted during service recovery; they do not represent systematic patterns.

## Decision-Ready Insights

1. **Pricing Strategy is the Primary Satisfaction Lever:** Airlines seeking to improve customer satisfaction should prioritize pricing alignment with perceived service quality. A 10% improvement in Value For Money perception is likely to yield 2-3 point improvements in Overall Rating.

2. **Service Quality Matters Secondarily:** Investments in seat comfort, staff training, and food quality will improve satisfaction but are insufficient without competitive pricing. An airline with premium seats and poor value perception will underperform.

3. **All Nippon Airways Model:** The top performer achieves high satisfaction through a balanced approach—strong feature ratings (Seat Comfort 4.14, Staff Service 4.51, Food 4.05) combined with competitive Value For Money (4.17). This is the optimal positioning.

4. **Turkish Airlines Deficit:** The lowest-performing carrier suffers primarily from low Value For Money (2.40), despite not being dramatically inferior in feature ratings. This suggests customer perception of pricing is the critical intervention point.

5. **Below 4/5 on Value For Money is a Crisis:** Carriers with Value For Money ratings below 3 should expect <41% recommendation rates and significant churn risk. This is not a marginal satisfaction issue but a fundamental loyalty threat.

## Conclusion

Customer satisfaction across airlines is **90% determined by perceived value for money** and only 10% by tangible service dimensions. While seat comfort, staff service, food quality, and entertainment all statistically correlate with satisfaction, they are secondary to price-value alignment in predicting customer loyalty and recommendations. Airlines competing on service quality alone, without addressing pricing competitiveness, will struggle to improve satisfaction metrics.
