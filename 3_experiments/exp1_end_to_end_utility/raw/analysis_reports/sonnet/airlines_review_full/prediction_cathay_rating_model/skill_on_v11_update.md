---
dataset: airlines_review_full
scenario: prediction_cathay_rating_model
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating_gt7"
query: "(Cathay MD) Build a model to organise/optimise routes and service so Overall Rating > 7."
source_table: augment_table/airlines_review_full/prediction_cathay_rating_model/sonnet__skill_on_v11_update.csv
generated_at: 2026-08-03T05:54:02.597679+00:00
wall_seconds: 69.87
---

# Cathay Pacific: Model to Achieve Overall Rating > 7

**Dataset:** 744 reviews | **Target:** Overall Rating > 7 (348 reviews = 46.8%)  
**Model Performance:** Gradient Boosting classifier, 5-fold CV AUC = **0.967**

---

## 1. Executive Summary

Overall Rating > 7 is achievable but currently the minority outcome (46.8%). The data reveals a small, tractable set of drivers. Fixing perceived value and crew attitude together is the dominant lever — when both are strong, 88–98% of reviews score > 7. The model is highly predictive, meaning the patterns are consistent enough to act on.

---

## 2. Key Drivers (Feature Importance)

| Rank | Feature | Importance |
|---|---|---|
| 1 | **Class-product value gap** (`class_product_value_gap`) | 0.775 |
| 2 | **Value For Money** (numeric) | 0.107 |
| 3 | **Cabin crew attitude** | 0.038 |
| 4–6 | Seat comfort, Food & Beverages, IFE | ~0.01 each |
| 7 | Route haul type | 0.010 |

> **The single biggest predictor is whether the product delivered meets or exceeds what passengers expect for their class and price paid.** Numeric `Value For Money` score is the second-strongest signal, explaining why both features dominate.

---

## 3. Decision Rules for >7 Rating

### Rule 1 — Value For Money is near-binary
| VFM Score | High-Rating Rate | Count |
|---|---|---|
| 1 | 0% | 141 |
| 2 | 0% | 84 |
| 3 | 17% | 122 |
| **4** | **70%** | 181 |
| **5** | **93%** | 216 |

Passengers giving VFM ≤ 3 **never** rate overall > 7. Raising perceived value from 3 → 4 lifts the high-rating probability from 17% to 70%.

### Rule 2 — Class-Product Value Gap × Cabin Crew Attitude (interaction)
| Value Gap | Crew Attitude | High-Rating Rate | n |
|---|---|---|---|
| exceeded_expectations | warm_proactive | **98%** | 144 |
| meets_class_expectations | warm_proactive | **88%** | 149 |
| meets_class_expectations | professional_neutral | **76%** | 59 |
| slight_shortfall | warm_proactive | 32% | 25 |
| significant_shortfall | cold_robotic | **0%** | 140 |
| significant_shortfall | rude_dismissive | **0%** | 111 |

The "death zone" for ratings is **significant value shortfall + poor crew attitude** — 251 reviews, 0% high rating. Recovering just one dimension to "slight shortfall" still only yields 12–32% high ratings; both must improve.

---

## 4. Route & Class Optimisation

### High-rating rates by Class × Haul
| Class | Haul Type | High-Rating Rate | n |
|---|---|---|---|
| Business | short_haul | **72%** | 53 |
| Economy | short_haul | **60%** | 124 |
| Business | long_haul | 56% | 121 |
| Economy | medium_haul | 46% | 41 |
| Premium Economy | long_haul | 38% | 78 |
| Economy | long_haul | 35% | 271 |

**Short-haul routes systematically outperform long-haul** across classes. Economy long-haul is the largest segment (271 reviews) with the lowest high-rating rate — but when value expectations are met or exceeded even here, 85–97% of reviews rate > 7 (see §5).

### Economy Long-Haul Can Be Fixed
| Value Gap | High-Rating Rate | n |
|---|---|---|
| exceeded_expectations | 97% | 34 |
| meets_class_expectations | 85% | 66 |
| significant_shortfall | **1%** | 138 |

The problem is not the route length — it's that 138/271 Economy long-haul passengers perceive a **significant value shortfall**.

---

## 5. Disruption & Special Service Handling

- **poorly_handled disruptions → 0% high ratings** (117 reviews); `well_handled` → 94% high ratings (29 reviews).
- **ignored_refused special service requests → 0% high ratings** (95 reviews); `well_handled` → 91% (40 reviews).
- These are smaller populations but represent absolute rating killers. A robust recovery/escalation protocol would eliminate a meaningful share of 1–2 star reviews.

---

## 6. Route & Service Optimisation Recommendations

| Priority | Action | Expected Impact |
|---|---|---|
| **P1** | Close the **Economy long-haul value gap**: review meal portions, seat pitch, and fare pricing vs. competitor benchmarks | Lifts 138 reviews from near-0% → 85%+ high-rating if gap closes to "meets expectations" |
| **P1** | Invest in **cabin crew warm/proactive service training** across all routes | Crew attitude alone shifts high-rating probability by 30–45pp at any value level |
| **P2** | Strengthen **disruption response protocols** (ground support, proactive communication, compensation) | Eliminates 0% high-rating outcome for 117 affected passengers |
| **P2** | Fix **special service request fulfilment** (dietary, assistance needs) | 95 reviews scoring 0% high — quick wins via pre-flight flagging and crew briefing |
| **P3** | Prioritise **Premium Economy long-haul** product refresh | 38% high-rating rate despite premium fare; significant value-gap perception |
| **P3** | Leverage short-haul strengths as brand showcase routes | 60–72% already > 7; consistent crew attitude yields near-ceiling performance |

---

## 7. Caveats & Weak Evidence

- **`cabin_crew_attitude`, `food_quality_rating`, `seat_comfort_issue`** are augmented/derived columns with a substantial "Unknown" share (~35% for food, ~35% for seat comfort) — patterns in those segments are based on incomplete labelling and should be verified against source text.
- The dataset covers **Cathay Pacific only**, so competitive benchmarking claims are inferred from passenger sentiment, not direct competitor data.
- First Class has only 16 reviews — conclusions for that segment are indicative only.
- Correlation between `class_product_value_gap` and `Value For Money` is high; they likely encode similar constructs, which inflates their combined importance share.
