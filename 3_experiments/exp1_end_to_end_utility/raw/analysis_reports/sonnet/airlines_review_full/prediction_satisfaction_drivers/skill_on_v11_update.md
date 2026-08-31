---
dataset: airlines_review_full
scenario: prediction_satisfaction_drivers
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating"
query: "What drives customer satisfaction (Overall Rating) across the different airlines?"
source_table: augment_table/airlines_review_full/prediction_satisfaction_drivers/sonnet__skill_on_v11_update.csv
generated_at: 2026-08-03T05:55:22.866743+00:00
wall_seconds: 48.31
---

# Customer Satisfaction Drivers — Airlines Review Dataset

## Overview

The dataset contains **8,100 reviews** across 10 airlines with `Overall Rating` (1–10, mean 5.6, SD 3.5) as the satisfaction target. Both original numeric sub-scores and augmented categorical signals are available for analysis.

---

## 1. Primary Driver: Value For Money

`Value For Money` has by far the strongest linear relationship with `Overall Rating` (r = **0.88**), dwarfing all other numeric sub-scores. The augmented `value_for_money_perception` column confirms the effect in categorical form:

| Perception | Mean Overall Rating |
|---|---|
| good_value | 9.1 |
| fair_value | 6.9 |
| poor_value | 2.5 |

This pattern is consistent across airlines: top-rated carriers (ANA, EVA Air, Qatar) also score highest on Value For Money (~4.0/5), while lower-rated carriers (Turkish, Air France, Emirates) cluster near 2.4–2.7/5.

---

## 2. Cabin Crew / Staff Service

`cabin_crew_quality` (augmented) shows a steep gradient and is the clearest qualitative separator:

| Cabin Crew Quality | Mean Overall Rating |
|---|---|
| exceptional | 9.4 |
| good | 8.3 |
| mixed | 5.3 |
| poor | 2.3 |

`Staff Service` (r = 0.23) ranks second among numeric scores, modestly below Value For Money but practically important. High-rated airlines like ANA and EVA Air consistently attract "exceptional" crew labels.

---

## 3. Service Consistency & Disruption Handling

The augmented `service_consistency_trend` splits reviews sharply:

| Trend | Mean Overall Rating |
|---|---|
| stable_positive / improving | 8.9–9.1 |
| stable_average | 5.4 |
| declining | 2.7 |

When disruptions occur, handling quality matters acutely:

| Disruption Handling | Mean Overall Rating |
|---|---|
| well_handled | 9.2 |
| partially_handled | 6.2 |
| poorly_handled | 2.0 |

Turkish Airlines (mean 3.7) — the lowest-rated carrier — has the highest share of "declining" trend and "poorly_handled" disruptions, suggesting operational reliability is a key differentiator at the bottom end.

---

## 4. Food Quality

`food_quality_signal` also stratifies satisfaction meaningfully:

| Food Signal | Mean Overall Rating |
|---|---|
| highly_praised | 9.2 |
| adequate | 7.8 |
| poor / out_of_stock | 3.4–4.0 |

The raw `Food & Beverages` sub-score correlation (r = 0.16) is weaker, likely because food satisfaction is partially captured through value perception.

---

## 5. Cabin Class & Traveller Type

Higher cabin classes rate more positively:

| Class | Mean Overall Rating |
|---|---|
| First Class | 7.6 |
| Business Class | 6.7 |
| Premium Economy | 6.0 |
| Economy Class | 5.2 |

Solo Leisure travellers rate slightly higher (6.1) than Business or Family Leisure travellers (~5.1–5.4), possibly reflecting lower baseline expectations or greater spontaneous delight.

---

## 6. Airline-Level Summary

| Airline | Mean Rating | Key strength |
|---|---|---|
| All Nippon Airways | 7.95 | Crew + value consistency |
| EVA Air | 7.42 | Crew + food |
| Qatar Airways | 7.20 | Product + value |
| Japan Airlines | 7.10 | Crew + consistency |
| Singapore Airlines | 6.54 | Crew + food |
| Korean Air | 6.49 | Mixed |
| Cathay Pacific | 6.17 | Mixed |
| Emirates | 4.67 | Value gap |
| Air France | 4.64 | Value + crew complaints |
| Turkish Airlines | 3.68 | Disruptions + poor value |

---

## Key Takeaways & Caveats

- **Value For Money is the dominant driver** (r = 0.88); airlines that fail to deliver perceived value almost universally receive poor overall ratings regardless of other attributes.
- **Cabin crew quality** is the strongest qualitative amplifier — exceptional service can lift ratings even when hard-product scores are mediocre.
- **Service consistency and disruption recovery** explain much of the gap between mid-tier and low-tier airlines; airlines with "declining" trends or poor disruption handling cluster at the bottom.
- **Weak evidence**: `Inflight Entertainment` (r = 0.14) and `Seat Comfort` (r = 0.21) show relatively modest direct effects; their influence may be mediated through value perception.
- The `Recommended` flag aligns closely with Overall Rating (no: 2.4, yes: 8.5), confirming the rating scale is behaviorally meaningful.
- Correlations are observational; passengers self-select into cabins and airlines, so class and airline differences partially reflect selection bias.
