---
dataset: airlines_review_full
scenario: prediction_satisfaction_drivers
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating"
query: "What drives customer satisfaction (Overall Rating) across the different airlines?"
source_table: augment_table/airlines_review_full/prediction_satisfaction_drivers/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-08-03T05:56:43.374504+00:00
wall_seconds: 90.42
---

# Drivers of Customer Satisfaction (Overall Rating) Across Airlines

## Dataset Overview

- **8,100 reviews** across 10 airlines; Overall Rating scale 1–10 (mean 5.6, median 6.0)
- **TAPP-generated columns used:** `staff_attitude`, `service_consistency_pattern`, `food_quality_signal`, `hard_product_condition`, `flight_disruption_type`, `disruption_handling_quality`, `overbooking_seat_assignment_issue`, `customer_service_resolution_quality`, `value_perception`

---

## 1. Headline Finding: Value For Money Is the Dominant Driver

OLS regression on the five structured sub-ratings reveals **Value For Money** as by far the strongest predictor, with a coefficient nearly 20× larger than any other sub-rating:

| Structured Driver       | Correlation w/ Overall Rating | OLS Coefficient |
|-------------------------|-------------------------------|-----------------|
| Value For Money         | **0.883**                     | **1.919**       |
| Staff Service           | 0.229                         | 0.085           |
| Seat Comfort            | 0.210                         | 0.087           |
| Food & Beverages        | 0.160                         | 0.034           |
| Inflight Entertainment  | 0.140                         | 0.026           |

This is confirmed by `value_perception` (TAPP): passengers labelled `good_value` average **9.1/10** (n=3,120), `fair_value` **6.9** (n=1,028), and `poor_value` **2.5** (n=3,937). Nearly half the dataset (49%) is tagged `poor_value`, concentrated at the bottom airlines.

---

## 2. Airline Rankings and Their Driver Profiles

| Airline              | Mean Rating | Warm-Friendly Staff % | Good-Value % | Consistently High % | Disruption Rate % |
|----------------------|-------------|----------------------|-------------|---------------------|-------------------|
| All Nippon Airways   | **7.95**    | 73.6                 | 67.8        | 62.4                | 14.0              |
| EVA Air              | 7.42        | 59.8                 | 63.0        | 49.8                | 17.1              |
| Qatar Airways        | 7.20        | 63.8                 | 54.0        | 46.2                | 17.3              |
| Japan Airlines       | 7.10        | 63.7                 | 58.7        | 49.3                | 12.4              |
| Singapore Airlines   | 6.54        | 52.0                 | 45.9        | 35.5                | 11.8              |
| Korean Air           | 6.49        | 51.9                 | 52.4        | 36.9                | 16.0              |
| Cathay Pacific       | 6.17        | 42.7                 | 42.3        | 33.1                | 23.9              |
| Emirates             | 4.67        | 26.7                 | 24.6        | 19.6                | 17.9              |
| Air France           | 4.64        | 36.6                 | 31.8        | 21.1                | 27.1              |
| Turkish Airlines     | **3.68**    | 21.5                 | 19.5        | 13.2                | **33.9**          |

The three columns (`staff_attitude`, `value_perception`, `service_consistency_pattern`) form a consistent hierarchy: airlines at the top score well on all three; airlines at the bottom score poorly on all three.

---

## 3. Staff Attitude — Second Most Impactful After Value

`staff_attitude` (TAPP) shows a steep gradient:

| Category              | Mean Rating | Count |
|-----------------------|-------------|-------|
| warm_friendly         | 8.87        | 3,456 |
| neutral_professional  | 6.47        | 799   |
| indifferent_unhelpful | 2.73        | 2,866 |
| rude_hostile          | 1.98        | 970   |

This mirrors the structured **Staff Service** sub-rating (r=0.229) but adds semantic granularity. Turkish Airlines (24.3% `rude_hostile`) and Emirates (16.0%) are worst; ANA (1.6%) and EVA Air (2.5%) are best.

---

## 4. Service Consistency — Strong Differentiator

`service_consistency_pattern` spans a 7-point range:

| Category         | Mean Rating | Count |
|------------------|-------------|-------|
| consistently_high| 9.31        | 2,464 |
| mixed_within_flight | 6.32     | 2,541 |
| declining_vs_past| 4.01        | 230   |
| consistently_poor| 1.98        | 2,861 |

Turkish Airlines (59.6% `consistently_poor`) and Emirates (49.5%) drive the bottom. ANA (62.4% `consistently_high`) leads the top. This facet is partially redundant with Staff Service scores but captures a temporal/trend dimension not available in any single structured column.

---

## 5. Flight Disruptions Compound Dissatisfaction

`flight_disruption_type` and `disruption_handling_quality` interact powerfully:

| Disruption Type               | Mean Rating | Count |
|-------------------------------|-------------|-------|
| no_disruption                 | 6.24        | 6,357 |
| delay_only                    | 4.93        | 635   |
| overbooking/itinerary change  | 3.00        | 354   |
| missed_connection             | 2.54        | 408   |
| cancellation                  | 2.12        | 346   |

**Handling quality mediates the damage.** When disruptions are handled proactively (`disruption_handling_quality = proactive_resolution`), ratings average **9.3** (n=321) — higher than many undisrupted flights. Poor handling yields **2.0** (n=2,393).

`overbooking_seat_assignment_issue = True` (n=327) averages only **2.6** vs **5.8** for `False` — a sharp penalty consistent with the lowest-rated overbooking/itinerary-change disruption type.

Turkish Airlines (33.9% disruption rate) and Air France (27.1%) are the most disruption-prone airlines.

---

## 6. Hard Product and Food Signal — Moderate, Secondary Effects

| `hard_product_condition` | Mean Rating | Count |
|--------------------------|-------------|-------|
| new_clean                | 8.73        | 713   |
| acceptable               | 7.43        | 3,104 |
| worn_dated               | 5.02        | 862   |
| broken_faulty            | 2.81        | 110   |

| `food_quality_signal`    | Mean Rating | Count |
|--------------------------|-------------|-------|
| excellent                | 9.12        | 1,746 |
| adequate                 | 7.65        | 1,604 |
| poor                     | 4.01        | 1,094 |
| not_served_adequately    | 3.05        | 223   |

Both show clear effects, consistent with the structured **Food & Beverages** sub-rating (r=0.16) and **Seat Comfort** (r=0.21), but their smaller OLS coefficients confirm they are secondary to value perception and staff.

---

## 7. Customer Service Resolution Quality

`customer_service_resolution_quality` matters enormously when contacted:

| Category               | Mean Rating | Count |
|------------------------|-------------|-------|
| resolved_satisfactorily| 9.18        | 286   |
| not_contacted          | 6.89        | 5,577 |
| partially_resolved     | 3.94        | 178   |
| unresolved_or_ignored  | 1.91        | 1,265 |
| rude_or_dismissive     | 1.84        | 794   |

Unresolved or dismissive service interactions (n=2,059 combined) are strongly associated with the lowest ratings and cluster at the lowest-rated airlines.

---

## 8. Cabin Class Effect

| Class           | Mean Rating | Count |
|-----------------|-------------|-------|
| First Class     | 7.60        | 121   |
| Business Class  | 6.65        | 2,104 |
| Premium Economy | 5.97        | 371   |
| Economy Class   | 5.18        | 5,504 |

Higher cabin class correlates with higher satisfaction, likely mediated through better value perception, staff attention, and hard product quality.

---

## 9. Summary: Key Satisfaction Drivers

| Priority | Driver | Evidence |
|----------|--------|----------|
| **1** | Value for money | r=0.883; OLS coef 1.92; `value_perception` spans 9.1→2.5 |
| **2** | Staff attitude/consistency | `staff_attitude` 8.9→2.0; `service_consistency_pattern` 9.3→2.0 |
| **3** | Disruption handling | Proactive resolution 9.3; poor handling 2.0; cancellation mean 2.1 |
| **4** | Hard product & seat comfort | `hard_product_condition` spans 8.7→2.8; Seat Comfort r=0.21 |
| **5** | Food quality | `food_quality_signal` spans 9.1→3.1; F&B r=0.16 |
| **6** | Post-service resolution | Resolved 9.2; unresolved/dismissive <2.0 |

**Airlines performing well (ANA, EVA Air, Qatar, JAL)** consistently score high on value perception, staff warmth, service consistency, and low disruption rates. **Underperformers (Turkish Airlines, Air France, Emirates)** are characterized by high rates of `poor_value`, `indifferent_unhelpful`/`rude_hostile` staff, `consistently_poor` service patterns, and high disruption rates with `poor_handling`.

---

*Method note: TAPP-generated columns `staff_attitude`, `service_consistency_pattern`, `food_quality_signal`, `hard_product_condition`, `flight_disruption_type`, `disruption_handling_quality`, `overbooking_seat_assignment_issue`, `customer_service_resolution_quality`, and `value_perception` were all used in this analysis. All facets showed meaningful effect sizes and added semantic signal beyond the structured sub-ratings. Coverage varied: `food_quality_signal` and `hard_product_condition` had ~41% "Unknown" tags, so absolute counts should be interpreted with caution, though directional findings are consistent.*
