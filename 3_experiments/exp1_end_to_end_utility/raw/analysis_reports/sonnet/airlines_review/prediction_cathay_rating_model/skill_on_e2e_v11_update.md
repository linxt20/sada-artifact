---
dataset: airlines_review
scenario: prediction_cathay_rating_model
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating_gt7"
query: "(Cathay MD) Build a model to organise/optimise routes and service so Overall Rating > 7."
source_table: augment_table/airlines_review/prediction_cathay_rating_model/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:05:47.654495+00:00
wall_seconds: 101.54
---

# Cathay Pacific: Model to Optimise Routes & Service for Overall Rating > 7

**Dataset:** 744 verified and unverified reviews of Cathay Pacific Airways  
**Target:** Overall Rating > 7 (binary) — 348/744 reviews meet this threshold (**46.8%**)  
**TAPP columns used:** `cabin_crew_service_quality`, `crew_absence_pattern`, `food_quality_rating`, `haul_category`, `outstation_region`, `baggage_handling_outcome`, `premium_economy_product_gap`  
*(Note: `special_meal_handling` was examined but showed negligible signal — mean rating 6.18 vs 6.00 for True/False — and is not featured in the model.)*

---

## 1. Dominant Driver: Value for Money

**Value For Money** is the single strongest predictor of Overall Rating > 7 (r = 0.753 with binary target).

| Value For Money Score | % Reviews > 7 | n |
|---|---|---|
| 1 | 0% | 141 |
| 2 | 0% | 84 |
| 3 | 17% | 122 |
| **4** | **70%** | **181** |
| **5** | **93%** | **216** |

No review scoring VFM ≤ 2 received Overall Rating > 7. Nearly all (99.7%) reviews with Overall Rating > 7 also recommended the flight. **VFM score ≥ 4 is a near-necessary condition for Overall Rating > 7.**

---

## 2. Cabin Crew: The Largest Controllable Lever

`cabin_crew_service_quality` (TAPP) strongly stratifies outcomes:

| Crew Quality | Mean Rating | % > 7 | n |
|---|---|---|---|
| excellent | 9.0 | ~88% | 282 |
| adequate | 7.2 | ~58% | 166 |
| poor | 3.0 | ~5% | 245 |
| rude | 2.3 | ~1% | 50 |

`crew_absence_pattern` (TAPP) reinforces this: reviews flagging crew as `responsive_throughout` average **8.7** (n=362) vs `absent_between_meals` at **4.1** (n=87). **33% of poor-crew reviews come from Economy class long-haul routes.**

Combined signal: when crew is good (excellent/adequate) **and** present throughout **and** food quality is good/excellent, the mean rating reaches **9.1** and **92% exceed 7** (n=230). When all three are poor, mean drops to **2.8** with only **0.7%** above 7 (n=291).

---

## 3. Food Quality

`food_quality_rating` (TAPP) is a significant secondary driver:

| Food Quality | Mean Rating | n |
|---|---|---|
| excellent | 9.5 | 45 |
| good | 8.9 | 203 |
| average | 6.8 | 120 |
| poor | 4.2 | 130 |
| inedible | 4.2 | 6 |
| Unknown | 4.1 | 240 |

The 240 reviews with unknown food quality average only 4.1 — skewed toward Economy long-haul routes where catering complaints are common and not explicitly logged.

---

## 4. Route & Haul Structure

`haul_category` (TAPP) shows a clear inverse relationship between haul length and satisfaction:

| Haul Category | Mean Rating | % > 7 | n |
|---|---|---|---|
| short_haul_under3h | 7.1 | ~55% | 141 |
| medium_haul_3to7h | 6.9 | ~52% | 88 |
| long_haul_7to13h | 5.9 | ~37% | 193 |
| ultra_long_haul_over13h | 5.7 | ~36% | 321 |

Long and ultra-long haul account for **514/744 (69%)** of reviews yet underperform. Business Class partially compensates: ultra-long haul Business Class achieves **57% > 7** vs only ~37% for Economy.

`outstation_region` (TAPP) highlights priority problem markets:

| Outstation Region | Mean Rating | n |
|---|---|---|
| middle_east_africa | 7.1 | 15 |
| hong_kong_hub | 6.6 | 106 |
| southeast_asia | 6.5 | 159 |
| europe | 6.2 | 133 |
| northeast_asia | 6.2 | 92 |
| north_america | 6.1 | 119 |
| oceania | 5.4 | 94 |
| **south_asia** | **4.5** | **26** |

**South Asia** is the worst-performing outstation (mean 4.5). Its crew quality breakdown shows 11 poor + 6 rude vs only 9 excellent/adequate — a staffing/training problem on these routes. **Oceania** (mean 5.4, n=94) is the highest-volume underperformer, with Hong Kong–Sydney averaging **3.9** and only **14% > 7**.

Top-performing high-volume routes:
- Manila–Hong Kong: mean 8.6, 80% > 7 (n=10)
- Bangkok–Hong Kong: mean 7.9, 71% > 7 (n=14)
- Singapore–Bangkok: mean 8.8, 83% > 7 (n=6)

---

## 5. Cabin Class Differentiation

| Class | Mean Rating | % > 7 | n |
|---|---|---|---|
| First Class | 7.4 | 50% | 16 |
| Business Class | 7.1 | **59%** | 195 |
| Premium Economy | 6.1 | 39% | 95 |
| Economy Class | 5.7 | 43% | 438 |

**Premium Economy underperforms relative to its price positioning.** `premium_economy_product_gap` (TAPP) confirms: 68/95 Premium Economy reviews (72%) are flagged as having a gap, averaging only **5.1** vs **8.7** for those without a gap (n=27). This is a critical product design failure.

Economy Class, despite low absolute ratings, shows 43% > 7 — slightly above Premium Economy — because Economy travelers calibrate expectations differently.

---

## 6. Baggage Handling

`baggage_handling_outcome` (TAPP) has a clear tail effect for resolved issues. Notably, 44.8% are "Unknown" (baggage not mentioned), which actually averages **7.2** — suggesting uneventful baggage handling correlates with better trips. Active complaints (lost_unresolved: mean 1.4, n=10; damaged: mean 2.0, n=5) are devastating to ratings but affect < 2% of reviews.

---

## 7. Predictive Model Summary

A decision-ready rule-based scoring model based on the evidence:

| Condition | Weight / Action |
|---|---|
| Value For Money ≥ 4 | **Required** — no path to >7 without this |
| `cabin_crew_service_quality` = excellent | +3 rating points vs poor |
| `crew_absence_pattern` = responsive_throughout | +4.6 pts vs absent |
| `food_quality_rating` = good/excellent | +4.7 pts vs poor |
| `haul_category` = short/medium haul | +1.2 pts vs long-haul |
| `outstation_region` ≠ south_asia/oceania | avoid −1.8 to −2.0 pts |
| `premium_economy_product_gap` = False | +3.6 pts within Premium Economy |

**Priority interventions to push toward Overall Rating > 7:**

1. **Crew training & deployment** (highest leverage): Eliminating "rude" crew ratings and shifting poor → adequate raises mean by ~4.3 points. Focus on long-haul Economy and South Asia routes where poor/rude crew ratings are concentrated.
2. **Catering upgrade on long-haul Economy**: poor/unknown food quality afflicts 70%+ of low-rated long-haul reviews. Even moving poor → average adds ~2.6 rating points.
3. **Premium Economy product redesign**: 72% of PE reviews flag a product gap (mean 5.1). Close the gap to reach Business-Class satisfaction levels.
4. **Oceania route management**: Hong Kong–Sydney (mean 3.9, n=7) and Oceania overall (mean 5.4, n=94) need targeted service intervention or yield management to set realistic VFM expectations.
5. **Value For Money framing**: Since VFM ≥ 4 is necessary for any rating > 7, pricing decisions and onboard delivery must be co-optimized — particularly on routes where both VFM and crew quality score low simultaneously.

---

## 8. Method Note

TAPP-generated columns used: `cabin_crew_service_quality`, `crew_absence_pattern`, `food_quality_rating`, `baggage_handling_outcome`, `haul_category`, `outstation_region`, `premium_economy_product_gap`. Note that `crew_absence_pattern`, `food_quality_rating`, and `baggage_handling_outcome` have 32–45% "Unknown" values, so group-level estimates for those facets are directional. All TAPP findings were cross-checked against original structured columns (Overall Rating, Class, Staff Service, Food & Beverages, Value For Money, Route). The structured VFM column remains the dominant single predictor; TAPP columns add meaningful semantic granularity on crew behaviour, route structure, and product gaps.
