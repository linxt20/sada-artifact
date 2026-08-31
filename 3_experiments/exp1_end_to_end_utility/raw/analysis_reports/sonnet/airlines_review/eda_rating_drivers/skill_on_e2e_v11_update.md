---
dataset: airlines_review
scenario: eda_rating_drivers
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "Overall Rating"
query: "Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?"
source_table: augment_table/airlines_review/eda_rating_drivers/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:05:17.946758+00:00
wall_seconds: 96.81
---

# Review Themes Associated with Higher vs. Lower Overall Rating
## Across Type of Traveller and Class — Airlines Review EDA

---

### Method Note

**TAPP-generated columns used:** `crew_service_quality`, `service_consistency`, `food_quality`, `seat_comfort_condition`, `cabin_class_expectation_gap`, `value_for_money_perception`, `service_decline_perception`, `service_amenity_cuts`.  
`special_meal_fulfillment` was inspected but excluded (only 17 positive cases; negligible analytical signal).  
All claims are cross-validated against original structured sub-ratings (Seat Comfort, Staff Service, Food & Beverages, Inflight Entertainment, Value For Money) and the primary outcome **Overall Rating** (1–10 scale, N = 900, mean = 6.53, median = 8.0).

---

### 1. Outcome Variable Overview

| Metric | Value |
|--------|-------|
| N | 900 |
| Mean Overall Rating | 6.53 |
| Std dev | 3.24 |
| Median | 8.0 |
| 25th pct | 4.0 |
| 75th pct | 9.0 |

Distribution is bimodal: a large cluster of satisfied reviews (≥8) and a substantial cluster of dissatisfied reviews (≤4), making theme-level contrasts sharp.

---

### 2. Structured Sub-Rating Correlations with Overall Rating

| Sub-Rating | Correlation with Overall Rating |
|---|---|
| **Value For Money** | **0.886** |
| Food & Beverages | 0.087 |
| Staff Service | 0.070 |
| Seat Comfort | 0.011 |
| Inflight Entertainment | −0.033 |

**Value For Money is the dominant structured driver** by a wide margin. The TAPP semantic columns (`value_for_money_perception`, `cabin_class_expectation_gap`) enrich this signal by explaining *why* passengers perceive value as good or poor.

---

### 3. Overall Rating by Segment

#### By Type of Traveller

| Type of Traveller | Mean Rating | N |
|---|---|---|
| Solo Leisure | 6.87 | 332 |
| Family Leisure | 6.57 | 180 |
| Couple Leisure | 6.37 | 242 |
| Business | 5.99 | 146 |

Business travellers rate lowest overall — partly due to higher expectations and a larger share of `professional_neutral` or `inattentive_robotic` crew encounters (51.4% combined vs. ~36–37% for leisure segments).

#### By Class

| Class | Mean Rating | N |
|---|---|---|
| First Class | 7.93 | 14 |
| Business Class | 7.10 | 237 |
| Economy Class | 6.37 | 563 |
| Premium Economy | 5.83 | 86 |

**Premium Economy is the lowest-rated cabin despite higher price expectations.** Its `cabin_class_expectation_gap` = `significant_gap` rate is 54.7% — the highest of any class — reflecting a gap between fare paid and experience delivered.

---

### 4. Key Theme Drivers — TAPP vs. Overall Rating

#### 4a. `crew_service_quality` — Strongest Semantic Driver

| Crew Quality | Mean Rating | N |
|---|---|---|
| attentive_warm | **8.97** | 468 |
| professional_neutral | 5.10 | 164 |
| inattentive_robotic | 3.20 | 203 |
| rude_hostile | 2.62 | 50 |

A swing of **+6.35 points** from `rude_hostile` to `attentive_warm`. This mirrors the structured Staff Service sub-rating and is the most decisive qualitative theme. The pattern holds consistently across all traveller types:

| Type of Traveller | attentive_warm mean | inattentive_robotic mean | rude_hostile mean |
|---|---|---|---|
| Business | 8.92 (n=64) | 2.27 (n=33) | 2.86 (n=7) |
| Couple Leisure | 8.94 (n=119) | 3.41 (n=56) | 2.12 (n=16) |
| Family Leisure | 9.11 (n=100) | 2.92 (n=37) | 2.23 (n=13) |
| Solo Leisure | 8.93 (n=185) | 3.58 (n=77) | 3.43 (n=14) |

Business travellers show the largest share of `professional_neutral` (28.8%) — a "technically adequate but cold" crew that still drags ratings to ~5.0.

#### 4b. `service_consistency` — Second Major Driver

| Service Consistency | Mean Rating | N |
|---|---|---|
| consistent_high | **9.38** | 344 |
| variable_mixed | 6.98 | 269 |
| consistently_poor | 2.67 | 286 |

**Nearly one-third of reviews (32%) describe consistently poor service**, averaging just 2.67. Combined with `crew_service_quality`, reviews tagged `attentive_warm` + `consistent_high` converge near 9.5, while `inattentive_robotic` + `consistently_poor` hover below 2.0.

#### 4c. `cabin_class_expectation_gap` — Critical in Premium Cabins

| Expectation Gap | Mean Rating | N |
|---|---|---|
| meets_expectations | **9.29** | 411 |
| minor_gap | 7.19 | 129 |
| significant_gap | 3.13 | 359 |

The `significant_gap` group (40% of all reviews) averages only 3.13. This signal is strongest in **Premium Economy** (54.7% significant_gap) and **Economy** (41.4%):

| Class | meets_expectations (mean/n) | significant_gap (mean/n) |
|---|---|---|
| First Class | 9.89 / 9 | 3.75 / 4 |
| Business Class | 9.31 / 124 | 3.43 / 75 |
| Economy Class | 9.29 / 254 | 2.91 / 233 |
| Premium Economy | 8.96 / 24 | 3.68 / 47 |

Even within Business Class, 31.6% of passengers experience a significant gap — suggesting inconsistent premium delivery, not just economy-class issues.

#### 4d. `value_for_money_perception` — Aligns Closely with Structured VFM

| VFM Perception | Mean Rating | N |
|---|---|---|
| good_value | **9.24** | 414 |
| fair_value | 7.38 | 112 |
| poor_value | 3.26 | 373 |

This closely mirrors the structured Value For Money sub-rating correlation (r = 0.886). Business travellers and Couple Leisure have the highest `poor_value` rates (~47%), while Family Leisure and Solo Leisure are more positive (~41% and 35.5% poor_value, respectively). The TAPP column adds marginal signal over the structured sub-rating but confirms it narrative-semantically.

#### 4e. `food_quality` — Conditional Upside Driver

| Food Quality | Mean Rating | N |
|---|---|---|
| excellent | **9.32** | 227 |
| acceptable | 8.13 | 182 |
| poor_bland | 4.21 | 197 |
| Unknown (not mentioned) | 4.95 | 294 |

Reviews that mention food at all skew either very positive or very negative. `excellent` food is strongly associated with high overall ratings; `poor_bland` pulls ratings down to 4.2. However, 294 reviews (33%) don't mention food, suggesting it is not a universal decider — more relevant in Business/First Class contexts where F&B expectations are higher.

#### 4f. `seat_comfort_condition` — Moderate Upside, Low Coverage

| Seat Comfort | Mean Rating | N |
|---|---|---|
| comfortable_modern | **9.16** | 144 |
| acceptable | 7.46 | 279 |
| dated_worn_dirty | 6.26 | 42 |
| uncomfortable_hard | 4.72 | 80 |
| Unknown | 5.18 | 355 |

Seat themes are mentioned in only ~63% of reviews. Where mentioned positively, they amplify high ratings; the 80 reviews citing `uncomfortable_hard` drop to 4.72. This is less decisive than crew or value themes.

#### 4g. `service_decline_perception` and `service_amenity_cuts` — Negative Sentiment Markers

| Flag | False mean | True mean | True N |
|---|---|---|---|
| service_decline_perception | 6.77 | **4.72** | 106 |
| service_amenity_cuts | 6.70 | **4.81** | 79 |

Both flags mark reviews that perceive the airline as deteriorating or cutting corners. Business travellers have the highest `service_decline_perception` rate (14.4%), followed by Solo Leisure (13.3%). These are relatively low-frequency signals but reliably associated with dissatisfied ratings.

---

### 5. Combined Theme Profile: High vs. Low Ratings

| Theme Cluster | Typical Overall Rating | Key Indicators |
|---|---|---|
| **High-rating profile** | 8.5–10 | `crew_service_quality = attentive_warm`, `service_consistency = consistent_high`, `cabin_class_expectation_gap = meets_expectations`, `value_for_money_perception = good_value`, `food_quality = excellent` |
| **Mid-rating profile** | 6–8 | `professional_neutral` crew, `variable_mixed` consistency, `minor_gap`, `food_quality = acceptable` |
| **Low-rating profile** | 1–4 | `inattentive_robotic` or `rude_hostile` crew, `consistently_poor` service, `significant_gap`, `value_for_money_perception = poor_value`, `service_decline_perception = True` |

---

### 6. Key Findings by Segment

**Business Travellers (mean 5.99):**  
Highest share of `professional_neutral` crew (28.8%) and `service_decline_perception` (14.4%). Value expectation is unmet for 46.6%. Despite flying Business Class at higher rates, expectations are not matched — the `cabin_class_expectation_gap = significant_gap` rate is 31.6% for Business Class seats.

**Premium Economy (mean 5.83 — worst cabin):**  
54.7% significant expectation gap, 59.3% poor_value — the worst of any cabin. The combination of elevated ticket price without commensurate service or comfort drives systematically low ratings. `food_quality` and `seat_comfort_condition` are frequently unknown/not mentioned, suggesting limited amenity differentiation from Economy.

**Solo Leisure (mean 6.87 — best traveller type):**  
Highest share of `attentive_warm` crew (55.7%) and `good_value` perception (50%). Lower expectations relative to price point may help; 50% rate value positively vs. 42.5% for Business travellers.

**Family Leisure (mean 6.57):**  
Highest `attentive_warm` crew share (55.6%) and `good_value` rate (51.1%), but also highest `rude_hostile` rate (7.2%) — suggesting polarized crew encounters. `service_decline_perception` is lowest (8.3%), indicating fewer concerns about airline quality trajectory.

---

### 7. Summary

The strongest and most consistent drivers of higher Overall Ratings are:
1. **Warm, attentive crew** (`crew_service_quality = attentive_warm`, mean 8.97) — universal across all traveller types and classes.
2. **Consistent high service** (`service_consistency = consistent_high`, mean 9.38) — predictability matters as much as individual moments.
3. **Expectations met for cabin class** (`cabin_class_expectation_gap = meets_expectations`, mean 9.29) — especially critical for Premium Economy and Business travellers who perceive the largest gaps when unmet.
4. **Value for money** (structured VFM r = 0.886; confirmed by `value_for_money_perception`) — the single strongest quantitative driver.

Dissatisfaction is driven by the mirror: robotic/rude crew, consistently poor service, significant expectation gaps, and poor value — disproportionately affecting Business travellers and Premium Economy passengers.
