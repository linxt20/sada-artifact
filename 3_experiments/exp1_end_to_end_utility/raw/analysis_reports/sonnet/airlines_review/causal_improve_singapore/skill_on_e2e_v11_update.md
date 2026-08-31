---
dataset: airlines_review
scenario: causal_improve_singapore
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "overall_rating_recommendation"
query: "How can Singapore Airlines improve its overall rating and recommendation rate, especially on flights where passengers do not recommend it (Recommended = no)?"
source_table: augment_table/airlines_review/causal_improve_singapore/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:04:19.132354+00:00
wall_seconds: 81.28
---

# Singapore Airlines — Causal Improvement Analysis
**Query:** How can Singapore Airlines improve its overall rating and recommendation rate, especially on flights where passengers do not recommend it (`Recommended = no`)?

---

## 1. Dataset Overview

| Metric | Value |
|---|---|
| Total reviews | 900 |
| Recommended = yes | 580 (64.4%) |
| Recommended = no | 320 (35.6%) |
| Mean Overall Rating (yes) | 8.61 / 10 |
| Mean Overall Rating (no) | 2.77 / 10 |

The gap in overall rating between recommenders and non-recommenders is **5.84 points**, signalling deep dissatisfaction rather than mild disappointment.

---

## 2. Primary Drivers of Non-Recommendation

### 2a. Structured Sub-scores — Mean Comparison

| Attribute | Recommended = no | Recommended = yes | Gap |
|---|---|---|---|
| Seat Comfort | 3.66 | 3.69 | −0.03 |
| Staff Service | 3.80 | 4.01 | −0.21 |
| Food & Beverages | 3.45 | 4.02 | −0.57 |
| Inflight Entertainment | 3.56 | 3.88 | −0.32 |
| **Value For Money** | **1.82** | **4.34** | **−2.52** |

**Value For Money is the single largest differentiator** and the strongest correlate of Overall Rating among non-recommenders (r = 0.60). Staff Service and Food & Beverages are secondary but meaningful gaps.

### 2b. No-Recommendation Rate by Cabin Class

| Class | No-recommend rate | n |
|---|---|---|
| Premium Economy | 41.9% | 86 |
| Economy Class | 38.0% | 563 |
| Business Class | 28.3% | 237 |
| First Class | 21.4% | 14 |

Premium Economy and Economy carry the greatest dissatisfaction volume. Premium Economy's **41.9% no-recommend rate** is disproportionately high given its price premium over Economy.

### 2c. No-Recommendation Rate by Traveller Type

| Traveller Type | No-recommend rate |
|---|---|
| Business | 40.4% |
| Couple Leisure | 40.1% |
| Family Leisure | 35.6% |
| Solo Leisure | 30.1% |

Business and couple travellers are disproportionately dissatisfied, suggesting pain points around premium-tier service consistency.

---

## 3. TAPP-Generated Facet Analysis

**TAPP columns used:** `crew_service_quality`, `food_quality_issue_type`, `amenity_reduction_signal`, `cabin_class_value_gap`, `perceived_service_decline`

### 3a. Crew Service Quality (`crew_service_quality`)

| Label | Recommended = no | Recommended = yes |
|---|---|---|
| `attentive_and_warm` | 19 (5.9%) | 453 (78.1%) |
| `adequate_but_mechanical` | 70 (21.9%) | 84 (14.5%) |
| `inattentive_or_rude` | 226 (70.6%) | 38 (6.6%) |

**70.6% of non-recommenders** experienced crew tagged as `inattentive_or_rude`, versus only 6.6% among recommenders. This is the most decisive semantic signal in the dataset. Improving crew warmth and responsiveness is the highest-leverage single intervention.

### 3b. Food Quality Issues (`food_quality_issue_type`)

| Label | Recommended = no | Recommended = yes |
|---|---|---|
| `praised` | 2 (0.6%) | 355 (61.2%) |
| `poor_taste_or_texture` | 90 (28.1%) | 43 (7.4%) |
| `Unknown` (not mentioned) | 194 (60.6%) | 162 (27.9%) |
| `run_out_of_choice` | 12 | 5 |
| `special_meal_error` | 16 | 12 |

Among Economy no-recommends, 51 of 214 cite `poor_taste_or_texture` and 11 cite `run_out_of_choice` — concrete operational failures. The `Unknown` majority among non-recommenders suggests food simply wasn't noteworthy (unlike the praised majority among recommenders), indicating a quality floor issue more than isolated incidents.

### 3c. Amenity Reduction Signal (`amenity_reduction_signal`)

| Signal | Mean Overall Rating | No-recommend count |
|---|---|---|
| `True` (amenity reduction flagged) | 4.61 | 41 of 320 (12.8%) |
| `False` | 6.69 | 279 |

Amenity reduction affects ~12.8% of non-recommenders and drags average rating down by 2.1 points. This is a real but **minority** factor; it should not be the primary focus.

### 3d. Cabin Class Value Gap (`cabin_class_value_gap`)

| Label | Recommended = no | Recommended = yes |
|---|---|---|
| `economy_as_expected` | 202 (63.1%) | 336 (57.9%) |
| `business_class_subpar` | 72 (22.5%) | 100 (17.2%) |
| `premium_economy_subpar` | 39 (12.2%) | 36 (6.2%) |
| `first_class_subpar` | 3 | 4 |

`premium_economy_subpar` is over-represented among non-recommenders (12.2% vs 6.2%), consistent with the 41.9% no-recommend rate in that cabin. Mean Value For Money for Premium Economy non-recommenders is **1.67** — the lowest across all cabin/recommendation combinations. The `cabin_class_value_gap` facet adds useful nuance beyond the raw structured `Value For Money` column.

### 3e. Perceived Service Decline (`perceived_service_decline`)

| Signal | Mean Overall Rating | Count |
|---|---|---|
| `True` | 4.70 | 105 total (67 no-recommend, 38 yes) |
| `False` | 6.77 | 795 |

20.9% of non-recommenders show `perceived_service_decline`, yielding a mean rating of 4.70 versus 6.77 for those without. This facet captures longitudinal reputation erosion and is especially relevant for Business travellers repeating flights.

---

## 4. Prioritised Improvement Recommendations

| Priority | Lever | Evidence | Affected Segment |
|---|---|---|---|
| **1** | Crew attitude & responsiveness | 70.6% of no-recommends = `inattentive_or_rude`; crew quality most strongly separates groups | All classes, especially Economy & Business |
| **2** | Value For Money perception | Gap of 2.52 points; r = 0.60 with Overall Rating in no-recommend group | Economy & Premium Economy |
| **3** | Premium Economy product redesign | 41.9% no-recommend rate, `premium_economy_subpar` 2× over-represented, mean VFM = 1.67 | Premium Economy |
| **4** | Food quality in Economy | `poor_taste_or_texture` (28.1%) and `run_out_of_choice` (12 cases) among non-recommenders; praised at only 0.6% | Economy Class |
| **5** | Address amenity rollbacks | `amenity_reduction_signal = True` → mean rating 4.61; 12.8% of no-recommends affected | Business & Economy |
| **6** | Manage service consistency for repeat flyers | `perceived_service_decline = True` for 20.9% of no-recommends; important for Business travellers (40.4% no-recommend rate) | Business travellers |

---

## 5. Key Takeaways

1. **Crew service is the dominant failure mode**: 7 in 10 non-recommending passengers explicitly experienced inattentive or rude crew (`crew_service_quality = inattentive_or_rude`). No other factor comes close.
2. **Value For Money is the structural driver of overall score** (r = 0.60 among non-recommenders), particularly in Economy and Premium Economy where price-to-product mismatch is most acute.
3. **Premium Economy is the highest-risk cabin**: worst no-recommend rate (41.9%) and worst mean VFM (1.67). A targeted product review of its seat, meal, and service proposition is warranted.
4. **Food quality issues are operationally fixable**: poor taste/texture and meal run-outs are concrete catering problems solvable through supplier standards and load planning.
5. TAPP facets `amenity_reduction_signal` and `perceived_service_decline` are genuine but secondary concerns, each affecting ~12–21% of non-recommenders, and may reflect service changes since 2022 that long-haul repeat passengers notice.

---

## Method Note

TAPP-generated columns used in this report: **`crew_service_quality`**, **`food_quality_issue_type`**, **`amenity_reduction_signal`**, **`cabin_class_value_gap`**, **`perceived_service_decline`**. All five columns provided additive signal beyond raw structured scores. `crew_service_quality` was the highest-signal facet. `food_quality_issue_type` complemented the raw `Food & Beverages` score by distinguishing issue types. `cabin_class_value_gap` added cabin-specific nuance to the raw `Value For Money` score. `amenity_reduction_signal` and `perceived_service_decline` were genuine but secondary; they are included without being centred in the analysis.
