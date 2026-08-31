---
dataset: airlines_review
scenario: prediction_satisfaction_drivers
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating"
query: "What drives customer satisfaction (Overall Rating) across the different airlines?"
source_table: augment_table/airlines_review/prediction_satisfaction_drivers/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:05:14.152624+00:00
wall_seconds: 58.14
---

# Customer Satisfaction Drivers — Airlines Review Dataset

**Dataset:** 900 reviews · 23 columns · Overall Rating scale 1–10 (mean 5.66, std 3.52)

---

## 1. Strongest Single Driver: Value For Money

| Factor | Correlation with Overall Rating |
|---|---|
| **Value For Money** | **0.878** |
| Staff Service | 0.206 |
| Seat Comfort | 0.205 |
| Food & Beverages | 0.130 |
| Inflight Entertainment | 0.089 |

Value For Money is by far the dominant quantitative predictor. Passengers who feel they received good value rate the airline highly regardless of cabin class — the mean VFM score rises from 1.5 (low-rated reviews) to 4.4 (high-rated reviews). This suggests that **perceived price-quality balance is the single most important lever for overall satisfaction**.

---

## 2. Crew Behavior: Attitude and Proactivity Are Near-Binary

| crew_attitude | Mean Overall Rating | n |
|---|---|---|
| positive | **8.94** | 375 |
| mixed | 5.95 | 143 |
| negative | **2.31** | 376 |

| crew_proactivity | Mean Overall Rating | n |
|---|---|---|
| proactive | **9.04** | 335 |
| reactive_only | 6.66 | 157 |
| absent_neglectful | **2.49** | 404 |

Crew attitude and proactivity split reviews almost bimodally. 87% of high-rated reviews (≥8) have positive crew attitude; 91% of low-rated reviews (≤3) have negative crew attitude. Proactive service yields ratings nearly as high as positive attitude alone.

---

## 3. Service Consistency Is a Gate-Keeper

| service_consistency | Mean Overall Rating | n |
|---|---|---|
| consistent_high | **9.25** | 284 |
| inconsistent | 6.52 | 273 |
| consistently_poor | **1.99** | 343 |

Consistently poor service virtually guarantees a low score (mean 2.0). 89% of low-rated reviews carry the `consistently_poor` tag. Inconsistency lands in the middle — suggesting passengers penalize unpredictability but not as harshly as chronic failure.

---

## 4. Operational Disruptions Are Major Satisfaction Destroyers

| disruption_handling_quality | Mean Overall Rating | n |
|---|---|---|
| no_disruption | 6.83 | 589 |
| proactive_good | **9.41** | 32 |
| reactive_adequate | 7.94 | 33 |
| passive_poor | **2.07** | 246 |

| operational_disruption_type | Mean Overall Rating | n |
|---|---|---|
| no_disruption | 6.26 | 706 |
| flight_delay | 4.23 | 102 |
| missed_connection | 3.38 | 39 |
| cancellation | 2.04 | 48 |
| overbooking | 2.20 | 5 |

Disruptions per se lower satisfaction, but **how the airline handles them matters most**. Proactive handling lifts ratings above the no-disruption baseline (9.41 vs 6.83). Passive or poor handling (n=246) collapses ratings to 2.1.

---

## 5. Post-Flight Resolution Amplifies or Deepens Damage

| post_flight_resolution_quality | Mean Overall Rating | n |
|---|---|---|
| resolved_promptly | **8.84** | 44 |
| no_issue_raised | 6.96 | 609 |
| resolved_delayed | 4.00 | 5 |
| refused_or_ignored | **1.82** | 242 |

Refused or ignored complaints push ratings to the floor (1.82). Prompt resolution (8.84) nearly matches the satisfaction of passengers who had no problems at all — a strong recovery opportunity.

---

## 6. Cabin Class and Traveller Type

| Class | Mean Overall Rating |
|---|---|
| Business Class | 6.78 |
| First Class | 6.36 |
| Premium Economy | 5.98 |
| Economy Class | 5.24 |

Business and First Class passengers rate slightly higher, but the gap is modest (~1.5 points). Economy travellers represent 70% of reviews and drive aggregate scores. Solo leisure travellers (mean 6.03) are marginally more satisfied than family or couple leisure segments.

---

## 7. Key Exceptions and Caveats

- **Inflight Entertainment** has the weakest correlation (0.089), suggesting it is a hygiene factor rather than a differentiator.
- **Special needs accommodation** shows almost no rating difference (5.65 vs 5.84) — likely due to very small n (37 flagged reviews).
- The dataset appears concentrated on routes through Singapore (likely a single carrier), which limits airline-to-airline comparisons. "Across different airlines" findings therefore reflect within-airline variation by class, traveller type, and trip circumstances rather than cross-carrier benchmarking.
- The `resolved_delayed` cell has only 5 observations — treat that result as directional only.

---

## Summary: Decision-Ready Takeaways

| Priority | Driver | Action |
|---|---|---|
| 1 | **Value For Money** | Pricing strategy and expectation-setting are foundational |
| 2 | **Crew attitude & proactivity** | Training and culture change with near-binary impact |
| 3 | **Service consistency** | Process standardization eliminates the largest pool of low ratings |
| 4 | **Disruption + resolution handling** | Recovery protocols can flip a bad experience to near-perfect |
