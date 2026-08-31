---
dataset: airlines_review
scenario: prediction_cathay_rating_model
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating_gt7"
query: "(Cathay MD) Build a model to organise/optimise routes and service so Overall Rating > 7."
source_table: augment_table/airlines_review/prediction_cathay_rating_model/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:05:22.459868+00:00
wall_seconds: 81.66
---

# Cathay Pacific: Route & Service Optimisation Model — Overall Rating > 7

**Dataset:** 744 verified/unverified reviews | **Target:** Overall Rating > 7 (348/744 = 46.8% currently achieve this)

---

## 1. Executive Summary

Achieving Overall Rating > 7 is strongly governed by three controllable service levers — **cabin crew warmth**, **service frequency**, and **perceived value-for-class** — rather than route geography. When all three levers are positive, 94.7% of passengers (n = 244) rate above 7 (mean = 9.17). When any one of them is negative, the hit rate collapses to 1.0% (mean = 2.82). This gives Cathay Pacific a clear, actionable optimisation surface.

---

## 2. Key Drivers (Correlation & Factor Analysis)

### 2.1 Numeric Correlations with Overall Rating

| Factor | Correlation |
|---|---|
| **Value For Money** | **0.877** |
| Seat Comfort | 0.156 |
| Staff Service | 0.110 |
| Food & Beverages | 0.109 |
| Inflight Entertainment | 0.089 |

**Value For Money** is the dominant numeric predictor by a wide margin. A score of ≥ 4/5 yields a 70% hit rate; ≥ 5/5 yields a 93% hit rate for Overall Rating > 7.

### 2.2 Categorical Factor Impact

| Factor | Best Level | Mean Rating | Worst Level | Mean Rating |
|---|---|---|---|---|
| **cabin_crew_warmth** | warm_and_personalized | **8.85** | rude_or_dismissive | 2.31 |
| **cabin_service_frequency** | proactive_and_frequent | **9.03** | infrequent/absent | 3.41 |
| **cabin_class_value_gap** | exceeded_expectations | **9.46** | significant_shortfall | 2.73 |
| **service_consistency_vs_pre_covid** | maintained_or_improved | **9.05** | significant_decline | 3.05 |
| **food_quality_signal** | excellent | **9.23** | poor_quality | 4.52 |
| **seat_comfort_issue_type** | spacious_or_excellent | **9.05** | narrow_or_cramped | 4.04 |

---

## 3. Model Rules for Routing and Service Design

### Rule 1 — Crew Warmth is Non-Negotiable
- `warm_and_personalized` crew: mean 8.85 (n = 310, 41.7% of reviews)
- `professional_but_cold`: mean 5.95 — borderline, needs other factors to compensate
- `rude_or_dismissive` or `robotic_or_absent`: mean 2.3–3.3 — virtually no path to > 7

**Recommendation:** Crew selection and training targeting warmth/personalisation is the single highest-leverage intervention. Pairing `maintained_or_improved` service consistency with warm crew achieves mean 9.16 (n = 174).

### Rule 2 — Service Frequency Must Be Proactive
- `proactive_and_frequent` service: mean 9.03 vs. `infrequent_or_absent_between_meals`: mean 3.41
- Even `adequate_on_request` (mean 7.46) clears the > 7 bar when combined with warm crew

**Recommendation:** Establish minimum proactive check intervals per cabin class on all routes.

### Rule 3 — Value Perception Drives the Headline Score
- Value For Money is the strongest numeric correlate (r = 0.88). Passengers rating VFM ≤ 3 essentially never rate Overall > 7.
- `cabin_class_value_gap = significant_shortfall_for_class` has the sharpest penalty (mean 2.73)

**Recommendation:** For Business and Premium Economy (where shortfall is most damaging), price-point review and amenity alignment to class expectations are critical.

### Rule 4 — Food Quality is a Threshold Factor
- `excellent` food: mean 9.23; `acceptable`: mean 7.98 — both clear > 7
- `poor_quality`: mean 4.52 — sinks the overall rating even when crew is adequate
- **254 reviews (34%) have Unknown food signal** — capturing structured food quality data on more routes would improve the model

### Rule 5 — Service Recovery from Pre-COVID Decline
- `significant_decline` reviews: mean 3.05 (n = 111, 14.9% of reviews) — concentrated drag on aggregate score
- `maintained_or_improved`: mean 9.05 (n = 214) — suggests the airline can deliver > 7 when fully recovered

**Recommendation:** Identify routes/crew pools still showing `significant_decline` and prioritise retraining or staffing adjustments there first.

---

## 4. Class and Route Findings

### By Cabin Class

| Class | Mean Rating | Count | Notes |
|---|---|---|---|
| First Class | 7.38 | 16 | Above target; small sample |
| Business Class | 7.09 | 195 | Above target on average |
| Premium Economy | 6.09 | 95 | Below target — value gap frequent |
| Economy Class | 5.73 | 438 | Largest segment; most drag |

Economy Class is the largest segment and the primary source of sub-7 scores. Seat comfort (legroom, cramping) is cited specifically here.

### Routes with Highest Performance (≥ 10 reviews)

| Route | Mean Rating | % High (>7) |
|---|---|---|
| Manila to Hong Kong | 8.60 | 80% |
| Bangkok to Hong Kong | 7.93 | 71% |
| Hong Kong to Bangkok | 7.60 | 60% |
| Hong Kong to Singapore | 7.23 | 77% |
| London to Hong Kong | 6.33 | 53% |
| Hong Kong to London | 6.31 | 50% |

Short/medium-haul intra-Asia routes outperform long-haul routes (London ↔ Hong Kong). Long-haul routes may need premium service protocols, better meal programmes, and seat product upgrades to close the gap.

---

## 5. Decision Model (Scoring Rubric)

To predict/target Overall Rating > 7, score each flight on:

| Signal | Points |
|---|---|
| cabin_crew_warmth = warm_and_personalized | +3 |
| cabin_service_frequency = proactive_and_frequent | +2 |
| cabin_class_value_gap = exceeded/meets expectations | +2 |
| food_quality_signal = excellent or acceptable | +1 |
| service_consistency = maintained_or_improved | +1 |
| seat_comfort_issue = none / spacious | +1 |

**Score ≥ 7 → high probability of Overall Rating > 7**. Any `rude_or_dismissive` crew or `significant_shortfall_for_class` is an immediate disqualifier regardless of other scores.

---

## 6. Caveats and Weak Evidence

- **Special needs handling** (True, n = 11) shows *lower* mean rating (4.36 vs 6.20) — counterintuitive and likely confounded by small sample and self-selection bias; not reliable for modelling.
- **34% of food reviews are "Unknown"** — food's true predictive weight may be underestimated.
- Route-level sample sizes are small (most routes have < 10 reviews), limiting route-specific conclusions beyond intra-Asia vs. long-haul patterns.
- Causality is directional but unconfirmed: low ratings may cause negative recall bias in service descriptions (and thus augmented categorical signals).

---

## 7. Priority Action Matrix

| Priority | Action | Expected Impact |
|---|---|---|
| **1 (Immediate)** | Crew warmth/personalisation training on Economy long-haul | Highest single-factor leverage |
| **2 (Immediate)** | Audit routes with `significant_decline` service consistency; redeploy or retrain | Fix 14.9% of reviews dragging mean below 3 |
| **3 (Short-term)** | Premium Economy value proposition review (pricing, seat, meal) | Close value gap for 95 pax/period |
| **4 (Short-term)** | Proactive service cadence standards on all routes | Lifts `adequate_on_request` segment into >7 range |
| **5 (Medium-term)** | Seat/legroom upgrade programme for Economy long-haul | Removes seat comfort as drag factor |
