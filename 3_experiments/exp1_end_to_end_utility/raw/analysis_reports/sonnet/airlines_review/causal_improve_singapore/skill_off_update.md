---
dataset: airlines_review
scenario: causal_improve_singapore
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "overall_rating_recommendation"
query: "How can Singapore Airlines improve its overall rating and recommendation rate, especially on flights where passengers do not recommend it (Recommended = no)?"
source_table: augment_table/airlines_review/causal_improve_singapore/sonnet__skill_off_update.csv
generated_at: 2026-07-28T12:56:48.390925+00:00
wall_seconds: 48.01
---

# Singapore Airlines: Improvement Analysis for Non-Recommending Passengers

## Overview

The dataset contains **900 verified reviews**, of which **320 (35.6%)** are from passengers who do not recommend the airline (`Recommended = no`). These passengers gave an average Overall Rating of **2.77/10**, compared to **8.61/10** among recommenders — a gap of nearly 6 points. Closing this gap is the primary lever for improving the overall rating and recommendation rate.

---

## 1. The Dominant Pain Point: Value For Money

**Value For Money is overwhelmingly the most critical issue** among non-recommending passengers:

| Metric | Non-Recommenders | Recommenders |
|---|---|---|
| Value For Money (mean) | **1.82** | **4.34** |
| Seat Comfort (mean) | 3.66 | 3.69 |
| Staff Service (mean) | 3.80 | 4.01 |
| Food & Beverages (mean) | 3.67 | 4.05 |
| Inflight Entertainment (mean) | 3.54 | 3.79 |

Value For Money shows the **largest gap** between the two groups and has a **correlation of 0.60** with Overall Rating among non-recommenders — far higher than any other dimension (all others < 0.10). This makes it the single most actionable driver.

Further confirming this:
- **138 of 320 non-recommenders** (43%) have `weakest_dimension = Value For Money`
- **270 of 320** (84%) have `improvement_priority = value_perception`
- All non-recommenders are classified as either **detractors** (250) or **passives** (70), with zero promoters

---

## 2. Value For Money Problem Spans All Cabin Classes

The value perception issue is not limited to Economy Class:

| Class | Avg Value For Money (no) | Count |
|---|---|---|
| Economy Class | 1.77 | 214 |
| Premium Economy | 1.67 | 36 |
| Business Class | 2.01 | 67 |
| First Class | 3.00 | 3 |

Economy and Premium Economy passengers feel the worst value. Economy accounts for **67%** of non-recommenders, suggesting that pricing or perceived product quality relative to cost is a systemic issue across the fleet — not merely a premium-tier problem.

---

## 3. Rating Gap: Passengers Feel the "Sub-Score vs. Overall" Disconnect

The `rating_gap` (Overall Rating minus avg sub-score) for non-recommenders averages **−3.47**, with a range of −7.2 to +2.65. This means passengers' holistic impression is markedly worse than even their individual dimension ratings would suggest — pointing to an **emotional or cumulative dissatisfaction** that transcends any single touchpoint.

---

## 4. Secondary Issues: Catering and Service Quality

Among non-recommenders, after value perception:
- **Food & Beverages** is the weakest dimension for 66 passengers (`improvement_priority = catering` for 19)
- **Staff Service** is the weakest for 52 passengers (`improvement_priority = service_quality` for 16)
- **Seat Comfort** is weakest for 49 passengers (`improvement_priority = hardware_comfort` for 14)

These are secondary but non-trivial. Staff Service score of 3.80 (vs. 4.01 for recommenders) suggests service inconsistency, particularly relevant given Singapore Airlines' brand promise of hospitality excellence.

---

## 5. Traveller Segments to Prioritize

| Traveller Type | Count (no) |
|---|---|
| Solo Leisure | 100 |
| Couple Leisure | 97 |
| Family Leisure | 64 |
| Business | 59 |

Leisure travellers dominate non-recommenders. Business travellers (59) are also significant — their dissatisfaction likely involves Business/First Class value perception and service consistency.

---

## Recommendations

| Priority | Action | Evidence |
|---|---|---|
| **1 (Critical)** | Improve perceived Value For Money — e.g., clearer pricing communication, enhanced Economy/Premium Economy product inclusions (meals, baggage, Wi-Fi) | 84% of non-recommenders flagged `value_perception`; VFM corr = 0.60 with Overall Rating |
| **2 (High)** | Targeted upgrades for Economy Class passengers on long-haul routes | Economy = 67% of non-recommenders; avg VFM = 1.77 |
| **3 (Medium)** | Address catering quality consistency | 66 non-recommenders cite Food & Beverages as weakest |
| **4 (Medium)** | Improve staff service reliability | 52 non-recommenders cite Staff Service; gap vs. recommenders is visible |
| **5 (Ongoing)** | Monitor the rating gap metric | Mean gap of −3.47 signals holistic dissatisfaction beyond fixable sub-scores |

---

## Caveats

- Sub-score correlations with Overall Rating are **weak for all dimensions except Value For Money** among non-recommenders, so improving Seat Comfort or IFE alone is unlikely to move the needle significantly.
- The `weakest_dimension` and `improvement_priority` columns are **derived/augmented features** — their exact methodology is not documented, so they should be treated as directional rather than definitive.
- First Class data is too sparse (3 non-recommenders) to draw conclusions about that cabin.
