---
dataset: airlines_review_full
scenario: prediction_satisfaction_drivers
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating"
query: "What drives customer satisfaction (Overall Rating) across the different airlines?"
source_table: augment_table/airlines_review_full/prediction_satisfaction_drivers/sonnet__skill_off_update.csv
generated_at: 2026-08-03T05:43:40.177110+00:00
wall_seconds: 48.41
---

# Customer Satisfaction Drivers — Airlines Review Dataset
**Analysis date:** 2026-08-03 | **Rows:** 8,100 | **Focus variable:** Overall Rating (1–10)

---

## 1. Executive Summary

**Value For Money is by far the strongest individual driver of Overall Rating** (r = 0.883). Cabin class, airline brand, and traveller type also differentiate satisfaction meaningfully. High consistency across service dimensions (low `Service_Score_Std`) is a secondary positive signal, while seat comfort is the most common pain point in volume terms.

---

## 2. Key Drivers

### 2.1 Value For Money — Dominant Factor
| Metric | Value |
|---|---|
| Correlation with Overall Rating | **0.883** |
| `Value_Gap` correlation with Overall Rating | 0.727 |

No other single sub-score comes close. When passengers feel they received good value, overall satisfaction follows almost automatically.

- In **low-satisfaction reviews**, `Value For Money` is the single most-cited weakest dimension (33% of low-tier reviews).
- In **high-satisfaction reviews**, `Value For Money` is almost never the weakest link (only 4%).

### 2.2 Composite Service Quality
`Service_Score_Mean` (average of the five sub-scores) correlates at **r = 0.593** with Overall Rating, confirming that broad service quality matters — but value perception amplifies or suppresses that signal.

Consistency also matters: `Service_Score_Std` correlates at **r = −0.32** with Overall Rating, meaning uneven service (one great dimension but one terrible one) tends to pull ratings down.

### 2.3 Individual Service Dimensions
| Dimension | Correlation with Overall Rating |
|---|---|
| Value For Money | **0.883** |
| Staff Service | 0.229 |
| Seat Comfort | 0.210 |
| Food & Beverages | 0.160 |
| Inflight Entertainment | 0.140 |

Staff service and seat comfort are the next most influential sub-scores, but their individual effects are modest relative to value perception.

### 2.4 Cabin Class
| Class | Mean Overall Rating |
|---|---|
| First Class | 7.60 |
| Business Class | 6.65 |
| Premium Economy | 5.97 |
| Economy Class | 5.18 |

Premium passengers (First/Business) rate roughly 1.4–2.4 points higher on average. This likely reflects both better absolute service and better value alignment with expectations (`Is_Premium_Class` mean: 6.70 vs 5.23 for non-premium).

### 2.5 Airline Brand
| Airline | Mean Rating |
|---|---|
| All Nippon Airways | 7.95 |
| EVA Air | 7.42 |
| Qatar Airways | 7.20 |
| Japan Airlines | 7.10 |
| Singapore Airlines | 6.54 |
| Turkish Airlines | 3.68 |
| Air France | 4.64 |
| Emirates | 4.67 |

A ~4-point spread between top and bottom airlines suggests brand-level operational quality is a real satisfaction driver beyond individual review variation.

### 2.6 Traveller Type
| Type | Mean Rating |
|---|---|
| Solo Leisure | 6.07 |
| Couple Leisure | 5.48 |
| Business | 5.38 |
| Family Leisure | 5.14 |

Solo leisure travellers rate highest; family leisure travellers lowest, possibly reflecting heightened practical needs (space, food variety, flexibility).

---

## 3. Weakest Service Dimension Patterns

Seat Comfort is the **most frequently identified weakest dimension** overall (2,465 reviews, 30%), but it is not the strongest predictor of low ratings. Value For Money failures are most predictive of ending up in the *low satisfaction tier*. This suggests seat comfort is a widespread but tolerated complaint, whereas poor value perception is a deal-breaker.

---

## 4. Exceptions & Weak Evidence

- **Inflight Entertainment** has the weakest correlation (0.14) — passengers may view it as a bonus rather than a core expectation.
- **Food & Beverages** correlates modestly (0.16) overall, though it may matter more on long-haul routes (not disaggregated here).
- The **`Rating_vs_Airline_Avg`** column correlates very strongly with Overall Rating (r = 0.92), but this is a derived variable that partially encodes the outcome itself — it should not be interpreted as an independent causal driver.
- Traveller type differences are real but modest; causality is confounded with class (business travellers may fly economy more often on short hauls).

---

## 5. Decision-Ready Summary

| Priority | Driver | Action Implication |
|---|---|---|
| 🔴 Critical | Value For Money perception | Pricing, ancillary fees, and transparent fare communication are the highest-leverage levers |
| 🟠 High | Cabin class experience | Continued investment in premium cabins yields above-average satisfaction returns |
| 🟡 Moderate | Staff service & seat comfort | Operational consistency training and seat refurbishment programs |
| 🟢 Lower | IFE, food | Baseline expectations; improvements are positive but not satisfaction-defining for most passengers |
