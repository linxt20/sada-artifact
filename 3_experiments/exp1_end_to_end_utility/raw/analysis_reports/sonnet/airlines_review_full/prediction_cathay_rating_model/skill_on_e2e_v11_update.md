---
dataset: airlines_review_full
scenario: prediction_cathay_rating_model
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating_gt7"
query: "(Cathay MD) Build a model to organise/optimise routes and service so Overall Rating > 7."
source_table: augment_table/airlines_review_full/prediction_cathay_rating_model/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-08-03T05:55:12.949204+00:00
wall_seconds: 92.19
---

# Cathay Pacific: Model to Optimise Routes & Service for Overall Rating > 7

**Dataset:** 744 verified Cathay Pacific reviews. **Target:** Overall Rating > 7 (binary classification). Currently 348 of 744 reviews (46.8%) meet this threshold; mean rating = 6.17, median = 7.0.

---

## Method Note

TAPP-generated columns used in this analysis: `cabin_crew_attitude`, `proactive_crew_service_presence`, `meal_quality_rating`, `meal_timing_appropriateness`, `disruption_type`, `disruption_handling_quality`, `cabin_class_experience_vs_expectation`, `premium_economy_value_gap`, `service_decline_vs_pre_covid`. Column `seat_comfort_issue_type` was examined but is low-coverage (267/744 = Unknown) and largely redundant with the structured **Seat Comfort** score; it is noted but not centred.

---

## 1. Key Drivers of Overall Rating > 7

A Random Forest model trained on both structured and TAPP columns reveals the following feature importances:

| Feature | Importance | Type |
|---|---|---|
| Value For Money | **0.309** | Structured |
| `cabin_crew_attitude` | **0.210** | TAPP |
| `cabin_class_experience_vs_expectation` | **0.183** | TAPP |
| `meal_quality_rating` | 0.082 | TAPP |
| Seat Comfort | 0.040 | Structured |
| Food & Beverages | 0.038 | Structured |
| Inflight Entertainment | 0.034 | Structured |
| Staff Service | 0.032 | Structured |
| `disruption_handling_quality` | 0.025 | TAPP |
| `disruption_type` | 0.020 | TAPP |

**Value For Money is the dominant driver** — but crew attitude and expectation-gap (TAPP) together add ~39% of predictive weight that structured scores alone do not fully capture.

---

## 2. Value For Money — The Non-Negotiable Gate

| VFM Score | Mean Overall Rating | % Reviews > 7 | N |
|---|---|---|---|
| 1 | 1.71 | 0% | 141 |
| 2 | 3.49 | 0% | 84 |
| 3 | 5.27 | 17% | 122 |
| **4** | **7.96** | **70%** | 181 |
| **5** | **9.13** | **93%** | 216 |

VFM ≥ 4 is effectively required to achieve Overall Rating > 7. In Economy Class, only 50% of reviews score VFM ≥ 4 (222/438), explaining Economy's low mean rating of 5.73.

---

## 3. Cabin Class Performance

| Class | Mean Rating | Median | % > 7 | % Recommended | N |
|---|---|---|---|---|---|
| First Class | 7.38 | 7.5 | 50% | 81% | 16 |
| Business Class | 7.09 | 8.0 | **59%** | **71%** | 195 |
| Premium Economy | 6.09 | 6.0 | 39% | 57% | 95 |
| Economy Class | 5.73 | 7.0 | 43% | 54% | 438 |

**Premium Economy underperforms most**: `premium_economy_value_gap = True` in 48 reviews with mean rating 3.94 vs. 6.32 for those without the gap (n=696). Premium Economy passengers who perceive poor value drop nearly 2.2 points vs. the class average.

**Business Class** is the strongest segment. However, `service_decline_vs_pre_covid = True` flags 27 Business Class reviews with mean rating 5.74 vs. 7.30 for the other 168 — a 1.56-point drag affecting 14% of Business reviews.

---

## 4. Crew Attitude — Largest Semantic Driver

`cabin_crew_attitude` (TAPP) is the second-most important feature and maps strongly to outcomes:

| Attitude Category | Mean Rating | N |
|---|---|---|
| warm_and_proactive | **8.89** | 309 |
| polite_but_mechanical | 7.14 | 135 |
| cold_or_indifferent | 3.03 | 233 |
| rude_or_hostile | 2.38 | 63 |

31% of reviews (233) describe crew as `cold_or_indifferent` and another 8% (63) as `rude_or_hostile` — together these 296 reviews have a mean Staff Service score of only 2.1 and a mean Overall Rating of 2.8. This aligns with the structured **Staff Service** column: reviews in the bottom two attitude categories score mean Staff Service = 2.1 vs. 4.4 for `warm_and_proactive`.

The interaction with disruptions is critical: `warm_and_proactive` + `well_handled` disruption → mean 9.21 (n=28). `cold_or_indifferent` + `poorly_handled` → mean 1.90 (n=93). Crew attitude is the biggest lever when things go wrong.

---

## 5. Disruptions — Frequency and Handling

| Disruption Type | Mean Rating | N |
|---|---|---|
| no_disruption | 6.72 | 577 |
| flight_delay | 5.86 | 86 |
| missed_connection | 3.00 | 22 |
| seat_change_without_notice | 2.67 | 12 |
| baggage_loss_or_damage | 2.40 | 15 |
| flight_cancellation | 2.25 | 32 |

167 reviews (22%) experienced a significant disruption. `disruption_handling_quality = poorly_handled` (121 reviews) produces mean rating 2.10 vs. `well_handled` (29 reviews) at 9.03. **Recovery quality, not just disruption frequency, determines outcome.**

---

## 6. Meal Service

`meal_quality_rating` and `meal_timing_appropriateness` (TAPP) both show strong separation:

| meal_quality_rating | Mean Rating | N |
|---|---|---|
| excellent | 9.25 | 140 |
| acceptable | 8.09 | 162 |
| poor | 4.34 | 185 |
| inedible | 4.63 | 8 |
| Unknown | 4.59 | 249 |

`meal_timing_appropriateness = True`: mean 8.73 (n=351). `= False`: mean 3.11 (n=246). These align with the structured **Food & Beverages** score (r = 0.11 with Overall Rating, modest direct correlation, but meal quality rating captures a broader satisfaction component).

---

## 7. Route Optimisation

Routes with ≥5 reviews, sorted by mean rating:

**Underperforming routes (mean < 5.5):**

| Route | Mean Rating | N |
|---|---|---|
| Hong Kong → Sydney | 3.86 | 7 |
| Los Angeles → Hong Kong | 4.00 | 5 |
| New York → Hong Kong | 4.88 | 8 |
| Sydney → London via HKG | 5.00 | 7 |

**Strong routes (mean > 7.5):**

| Route | Mean Rating | N |
|---|---|---|
| Singapore → Bangkok | 8.83 | 6 |
| Manila → Hong Kong | 8.60 | 10 |
| Hong Kong → Taipei | 8.00 | 8 |
| Bangkok → Hong Kong | 7.93 | 14 |
| Hong Kong → Bangkok | 7.60 | 10 |

Long-haul routes (Sydney, LA, NY, London) cluster among the worst performers. Short-haul Southeast Asian routes (Bangkok, Manila, Singapore, Taipei) dominate the top. The long-haul segment suffers from compounding issues: more disruptions, higher price sensitivity (VFM gap), and meal quality degradation on extended flights.

---

## 8. Model for Achieving Overall Rating > 7

Based on the analysis, the following decision rules achieve the target:

### Necessary condition
- **VFM ≥ 4** (eliminates 46% of currently failing reviews if achieved)

### High-impact levers (sorted by model weight)

| Lever | Action | Expected Impact |
|---|---|---|
| **Crew attitude** | Increase `warm_and_proactive` ratio from 42% → target 65%+ via training/accountability | +2–4 rating points for affected customers |
| **Expectation alignment** | Reduce `severely_below_expectations` (22% of reviews, mean 2.0) through honest class marketing and product investment | Largest single category of failure |
| **Meal quality** | Address `poor`/`Unknown` meal quality (58% of reviews); target `acceptable`+ across all classes | Gap between poor and acceptable = +3.7 points |
| **Disruption recovery** | Standardise recovery protocols; `poorly_handled` → `well_handled` shifts mean from 2.1 → 9.0 | Highest leverage per incident |
| **Premium Economy pricing** | Reprice or upgrade PE product to close `premium_economy_value_gap` (currently affects 50% of PE reviews) | Mean +2.4 points for gap closers |
| **Route prioritisation** | Invest in long-haul service quality (HKG–SYD, HKG–LAX, HKG–JFK) or realign VFM pricing | Worst-performing routes are core network |
| **Service consistency** | Address `service_decline_vs_pre_covid = True` flag in Business (14% of reviews, –1.6 point drag) | Protect premium segment anchor |

---

## 9. Summary

The **Overall Rating > 7 threshold** is primarily gated by **Value For Money perception** (RF importance 0.31), then unlocked by **crew warmth** (`cabin_crew_attitude`, 0.21) and **meeting class expectations** (`cabin_class_experience_vs_expectation`, 0.18). Structured sub-scores (Seat Comfort, F&B, Entertainment) are secondary. The clearest operational targets are: improving crew attitude training, fixing meal quality on long-haul, upgrading disruption recovery processes, and repricing or upgrading Premium Economy. Route optimisation should focus management attention on the HKG–Sydney, HKG–North America, and Australia–Europe via HKG corridors, which are systematically below the target threshold.
