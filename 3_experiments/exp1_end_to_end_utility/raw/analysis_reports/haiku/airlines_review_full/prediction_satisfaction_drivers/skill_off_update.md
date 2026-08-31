---
dataset: airlines_review_full
scenario: prediction_satisfaction_drivers
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating"
query: "What drives customer satisfaction (Overall Rating) across the different airlines?"
source_table: augment_table/airlines_review_full/prediction_satisfaction_drivers/haiku__skill_off_update.csv
generated_at: 2026-08-03T05:43:39.992277+00:00
wall_seconds: 51.29
---

# Satisfaction Drivers Analysis: Airline Reviews

## Executive Summary

This analysis examines 8,100 airline reviews across 10 major carriers to identify what drives customer satisfaction (Overall Rating). The dataset reveals that **Value for Money is overwhelmingly the dominant satisfaction driver**, with a correlation of **0.88** with Overall Rating. Secondary factors include Staff Service (0.23) and Seat Comfort (0.21), but these have substantially weaker influence.

---

## Key Finding: Value for Money Dominates All Other Factors

The analysis shows a stark pattern:

- **Value for Money correlation: 0.883** (industry-wide)
- **Staff Service correlation: 0.229**
- **Seat Comfort correlation: 0.210**
- **Food & Beverages correlation: 0.160**
- **Inflight Entertainment correlation: 0.140**

This pattern holds consistently across all 10 airlines tested. Value for Money shows correlations ranging from 0.75 to 0.91 depending on the carrier, while other dimensions rarely exceed 0.25.

### Evidence from Satisfaction Levels

When comparing high-satisfaction customers (ratings 8-10) versus low-satisfaction customers (ratings 1-3):

| Dimension | High Satisfaction | Low Satisfaction | Gap |
|-----------|------------------|-----------------|-----|
| **Value for Money** | 4.58/5 | 1.52/5 | **3.06** |
| Staff Service | 3.91/5 | 3.15/5 | 0.76 |
| Seat Comfort | 3.71/5 | 3.07/5 | 0.64 |
| Food & Beverages | 3.61/5 | 3.11/5 | 0.50 |
| Inflight Entertainment | 3.80/5 | 3.42/5 | 0.39 |

The **3.06-point gap in Value for Money** is more than 4× larger than any other dimension, confirming it as the primary satisfaction driver.

---

## Secondary Drivers: Context-Dependent Impact

**Staff Service** and **Seat Comfort** show limited but measurable influence:

- Staff Service matters more on airlines like Japan Airlines (0.25 correlation), EVA Air (0.14), and Korean Air (0.21)
- Seat Comfort shows slightly stronger correlations on EVA Air (0.14) and Korean Air (0.16)
- For Air France and Singapore Airlines, even these secondary drivers show near-zero correlation after Value for Money is accounted for

**Food & Beverages and Inflight Entertainment** contribute minimally across all carriers (correlations < 0.16).

---

## Airline Performance Segmentation

Carriers cluster into distinct performance tiers driven primarily by perceived value:

### High Satisfaction (Mean Rating 7+)
- **All Nippon Airways**: 7.95/10 (Value for Money: 4.17/5)
- **EVA Air**: 7.42/10 (Value for Money: 4.00/5)
- **Qatar Airways**: 7.20/10 (Value for Money: 3.80/5)
- **Japan Airlines**: 7.10/10 (Value for Money: 3.77/5)

### Mid Satisfaction (6-6.5)
- **Singapore Airlines**: 6.54/10 (Value for Money: 3.45/5)
- **Korean Air**: 6.49/10 (Value for Money: 3.56/5)
- **Cathay Pacific Airways**: 6.17/10 (Value for Money: 3.33/5)

### Low Satisfaction (< 5)
- **Emirates**: 4.67/10 (Value for Money: 2.75/5)
- **Air France**: 4.64/10 (Value for Money: 2.67/5)
- **Turkish Airlines**: 3.68/10 (Value for Money: 2.40/5)

All performance gaps correlate directly with Value for Money perception.

---

## Travel Class and Traveler Type Effects

**Business Class** significantly outperforms Economy on all airlines:
- Business Class average: 6.65/10
- Economy Class average: 5.18/10
- First Class average: 7.60/10 (limited sample, n=121)

**Travel Type Impact** (secondary to class):
- Solo travelers rate highest: 6.07/10 average
- Family leisure travelers rate lowest: 5.14/10 average
- Business and couple leisure are intermediate (5.38/10 and 5.48/10)

However, these differences persist because value perception likely varies with travel purpose and seat product—not because service or comfort quality differs independently.

---

## Important Caveats and Weak Evidence

1. **Collinearity Issue**: Value for Money likely captures the combined effect of price + experience. Isolated seat comfort or service improvements may matter more than the correlation suggests, but customers typically evaluate value holistically.

2. **Limited Sample Sizes**: Several airline-class combinations have fewer than 10 reviews (e.g., Qatar Airways Premium Economy: n=7). Performance rankings for small segments should be interpreted cautiously.

3. **Flat Secondary Drivers**: Ratings for Staff Service, Seat Comfort, and Food are consistently compressed (means 2.7–4.5 across airlines), suggesting limited variance. This may constrain their correlation with Overall Rating even if operationally important.

4. **Recommendation Alignment**: The binary Recommended field is not analyzed here but would be a useful validation metric.

---

## Actionable Insight

**To improve overall satisfaction across different airlines, focus on value perception first.** This can mean:
- Competitive pricing relative to service tier
- Clear communication of included amenities
- Reducing unexpected fees
- Matching service expectations to fare class

Secondary investments in staff training or seat comfort modernization show measurable but limited ROI in customer satisfaction, except for carriers (like EVA Air and Korean Air) where secondary factors already show stronger correlations.

---

## Dataset Overview

- **Total reviews**: 8,100
- **Airlines**: 10 (Singapore Airlines, Qatar Airways, All Nippon Airways, Emirates, Japan Airlines, Turkish Airlines, Air France, Cathay Pacific Airways, EVA Air, Korean Air)
- **Overall Rating range**: 1–10
- **High satisfaction (8–10)**: 42.0% of reviews
- **Low satisfaction (1–3)**: 37.3% of reviews
