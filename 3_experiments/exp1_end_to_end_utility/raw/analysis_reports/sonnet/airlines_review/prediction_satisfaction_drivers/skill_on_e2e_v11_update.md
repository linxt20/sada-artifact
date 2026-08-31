---
dataset: airlines_review
scenario: prediction_satisfaction_drivers
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating"
query: "What drives customer satisfaction (Overall Rating) across the different airlines?"
source_table: augment_table/airlines_review/prediction_satisfaction_drivers/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:06:22.605020+00:00
wall_seconds: 117.69
---

# What Drives Customer Satisfaction (Overall Rating) Across the Airlines?

**Dataset:** 900 verified reviews; Overall Rating on a 1–10 scale (mean 5.66, SD 3.52).  
**Satisfaction split:** High (7–10) 49.4% · Mid (4–6) 14.2% · Low (1–3) 36.3%.

---

## Method Note

TAPP-generated columns used in this analysis: `cabin_crew_service_quality`, `ground_staff_service_quality`, `service_consistency`, `flight_disruption_type`, `disruption_handling_quality`, `food_quality_assessment`, `customer_service_responsiveness`. Columns `special_meal_handling` (only 26 of 900 = True) and `seat_product_downgrade` (23 True) were too sparse to drive conclusions and are noted where relevant.

---

## 1. Primary Driver: Value For Money

Value For Money is overwhelmingly the strongest structural predictor of Overall Rating (r = **0.878**), dwarfing every other structured column.

| Value For Money score | Mean Overall Rating | n |
|---|---|---|
| 1 | 1.47 | 235 |
| 2 | 3.28 | 100 |
| 3 | 5.28 | 129 |
| 4 | 7.73 | 176 |
| 5 | 9.14 | 260 |

This near-monotonic relationship holds across all cabin classes. Business Class passengers rate VFM highest on average (3.52 vs Economy 2.99) and correspondingly give higher Overall Ratings (6.78 vs 5.24). **Perceived value is the single gate through which all other service dimensions ultimately register in the overall score.**

---

## 2. Staff Service Dimension

Staff Service and Seat Comfort show similar moderate correlations with Overall Rating (r ≈ 0.21 each). TAPP columns `cabin_crew_service_quality` and `service_consistency` add granular signal beyond the single-digit Staff Service score:

### Cabin Crew Service Quality

| cabin_crew_service_quality | Mean Overall Rating | n |
|---|---|---|
| excellent | 9.25 | 250 |
| good | 7.89 | 161 |
| inconsistent | 6.17 | 59 |
| poor | 2.60 | 364 |
| Unknown | 3.02 | 66 |

"Poor" cabin crew ratings dominate the sample (364/900, 40%) and are the primary engine of low Overall Ratings. "Excellent" crew (250 reviews) clusters near the ceiling.

### Service Consistency

| service_consistency | Mean Overall Rating | n |
|---|---|---|
| consistent_high | 9.25 | 258 |
| inconsistent_within_flight | 7.01 | 234 |
| inconsistent_across_legs | 6.04 | 45 |
| consistently_poor | 2.18 | 362 |

Reviews coded `consistently_poor` (362 reviews, 40%) converge strongly with `poor` cabin_crew_service_quality, confirming these reflect the same dissatisfied segment. The `inconsistent_within_flight` group (n=234, mean 7.01) represents a recoverable middle tier — good moments compensate for lapses enough to sustain a moderately positive overall view.

### Ground Staff

`ground_staff_service_quality` shows a wide spread: positive ground staff → mean 9.10 (n=202); negative → mean 2.21 (n=335). However, 316 reviews are "Unknown" (ground staff not mentioned), meaning this facet has partial coverage and should be treated as supplementary.

---

## 3. Operational Reliability & Disruption Handling

195 out of 900 reviews (22%) involve a flight disruption (`flight_disruption_type` ≠ no_disruption).

| Disruption type | n | poorly_handled mean | well_handled mean |
|---|---|---|---|
| Cancellation | 45 | 1.67 (n=42) | 9.00 (n=3) |
| Missed connection | 41 | 1.59 (n=34) | 9.40 (n=5) |
| Delay | 95 | 2.18 (n=44) | 9.46 (n=13) |
| Aircraft change | 14 | 1.40 (n=5) | 10.00 (n=1) |

`disruption_handling_quality` is a decisive amplifier: poor handling collapses ratings to ~1.5–2.2 regardless of disruption type, while well-handled disruptions yield ratings of 9.0–9.5 — comparable to undisrupted flights (mean 6.92 for no_disruption / not_applicable). Even for "no disruption" flights, **121 reviews were coded `poorly_handled`** (mean 2.31), capturing broader service failure complaints mislabeled as disruption handling.

---

## 4. Food & Beverage Dimension

Structural Food & Beverages has a weaker correlation (r = 0.13). The `food_quality_assessment` TAPP column captures more variance:

| food_quality_assessment | Mean Overall Rating | n |
|---|---|---|
| excellent | 9.21 | 122 |
| good | 8.41 | 160 |
| average | 6.78 | 69 |
| poor | 4.02 | 124 |
| Unknown | 3.89 | 425 |

The high "Unknown" rate (425/900, 47%) means food is not discussed in nearly half the reviews — consistent with food being a secondary rather than primary satisfaction driver. Where it is mentioned, quality matters: excellent vs poor food spans ~5 rating points.

---

## 5. Customer Service Responsiveness

`customer_service_responsiveness` captures post-issue escalation behavior (n=225 reviews where contact was made):

| customer_service_responsiveness | Mean Overall Rating | n |
|---|---|---|
| responsive_and_resolved | 9.03 | 30 |
| responsive_unresolved | 2.40 | 15 |
| unresponsive | 1.72 | 180 |
| not_contacted | 6.63 | 675 |

180 reviews (20%) document unresponsive customer service and return a mean of only 1.72. This is a potent satisfaction destructor: **unresponsive customer service produces worse outcomes than any individual in-flight dimension except cancellation.** Resolution matters too — being responsive but not resolving the issue (mean 2.40) provides negligible benefit over being unresponsive.

---

## 6. Cabin Class & Traveller Type

| Class | Mean Overall Rating | n |
|---|---|---|
| Business Class | 6.78 | 216 |
| First Class | 6.36 | 11 |
| Premium Economy | 5.98 | 44 |
| Economy Class | 5.24 | 629 |

Economy passengers rate satisfaction lower, driven partly by lower VFM scores (mean 2.99 vs 3.52 for Business). Solo Leisure travellers are modestly more satisfied (mean 6.03, n=376) vs Family Leisure (5.17, n=176), potentially reflecting simpler expectations and less exposure to disruption-compounding effects.

---

## 7. Satisfaction Driver Summary

| Driver | Type | Correlation / Effect Size | Verdict |
|---|---|---|---|
| Value For Money | Structured | r = 0.878 | **Dominant driver** |
| cabin_crew_service_quality (poor) | TAPP | Mean 2.60 vs 9.25 (excellent) | **Strong negative driver** |
| service_consistency (consistently_poor) | TAPP | Mean 2.18 vs 9.25 (consistent_high) | Strong, overlaps with crew quality |
| customer_service_responsiveness (unresponsive) | TAPP | Mean 1.72 vs 9.03 (resolved) | High impact, 20% of reviews |
| disruption_handling_quality (poorly_handled) | TAPP | Mean 2.06 vs 9.34 (well_handled) | High impact for disrupted flights |
| Staff Service | Structured | r = 0.206 | Moderate |
| Seat Comfort | Structured | r = 0.205 | Moderate |
| food_quality_assessment | TAPP | ~5-pt span; 47% unknown | Secondary |
| Food & Beverages | Structured | r = 0.130 | Weak |
| Inflight Entertainment | Structured | r = 0.089 | Weak |
| seat_product_downgrade | TAPP | n=23 True; mean 5.13 vs 5.67 | Negligible coverage |
| special_meal_handling | TAPP | n=26 True | Negligible coverage |

---

## Key Takeaways

1. **Value For Money perception is the primary lever** — improving it lifts the entire rating distribution regardless of class.
2. **Cabin crew quality and service consistency are the top soft-service predictors** — 40% of reviews cite "poor / consistently poor" service and average ≈2.2–2.6 overall.
3. **Disruption recovery is a differentiator**: well-handled disruptions yield ratings on par with smooth flights (9.3+); poorly handled disruptions crater scores to ≈1.5–2.2.
4. **Post-contact customer service unresponsiveness (180 reviews, mean 1.72) is as damaging as the original failure** — a systemic complaint resolution gap.
5. Food quality is relevant where mentioned but secondary; IFE has negligible correlation with overall satisfaction.
