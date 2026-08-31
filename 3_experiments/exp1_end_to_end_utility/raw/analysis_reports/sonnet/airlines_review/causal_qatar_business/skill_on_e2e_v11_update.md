---
dataset: airlines_review
scenario: causal_qatar_business
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "non_recommendation_outcome"
query: "Explain why some Qatar Airways Business-Class flights receive a non-recommended (Recommended = no) result."
source_table: augment_table/airlines_review/causal_qatar_business/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:04:09.004596+00:00
wall_seconds: 71.15
---

# Why Some Qatar Airways Business-Class Flights Receive a Non-Recommended Result

## Overview

Of 592 Qatar Airways Business Class reviews, **127 (21.5%) are non-recommended** (`Recommended = no`). Non-recommended reviews have a mean Overall Rating of **3.8** versus **8.4** for recommended reviews. The dominant structured driver is **Value For Money** (correlation with recommendation: *r* = 0.66), followed by Staff Service (*r* = 0.14). Inflight Entertainment, Food & Beverages, and Seat Comfort show minimal correlation individually, suggesting the "no" outcome is primarily driven by perceived value and service failures rather than amenity gaps.

---

## Key Causal Factors

### 1. Poor Perceived Value for Money (Primary Driver)

Value For Money is the single strongest predictor of non-recommendation.

| VFM Score | Non-rec count | % of all non-rec |
|-----------|--------------|-----------------|
| 1         | 49           | 38.6%           |
| 2         | 20           | 15.7%           |
| 3         | 42           | 33.1%           |
| 4         | 13           | 10.2%           |
| 5         | 3            | 2.4%            |

**69 of 127 non-rec reviews (54%) gave VFM ≤ 2.** Mean VFM for non-rec is **2.22** vs. **4.29** for recommended. This reflects a mismatch between the premium price paid and the experience delivered — often compounded by one or more of the factors below.

---

### 2. Cabin Crew Service Failures (`cabin_crew_service_quality`)

This TAPP column is highly discriminating:

| Crew Quality          | Total | Non-rec rate |
|-----------------------|-------|-------------|
| exceptional           | 309   | 1.3%        |
| good_standard         | 126   | 24.6%       |
| inconsistent_or_variable | 73 | 43.8%      |
| poor_or_disengaged    | 75    | **69.3%**   |

**52 non-rec reviews** feature `poor_or_disengaged` crew and **32 more** feature `inconsistent_or_variable` crew. Reviews with poor crew consistently score low on Staff Service (mean ~2.1) and drag down the overall experience regardless of seat quality.

---

### 3. Seat Product Downgrade (`seat_product_downgrade`, `seat_product_generation`)

Two distinct seat-related failure modes appear:

**Downgrade from booked product** (`seat_product_downgrade`):
- `qsuite_downgraded_to_standard`: 41 reviews, **61% non-rec** (25 non-rec)
- `standard_downgraded_to_older`: 36 reviews, **47% non-rec** (17 non-rec)
- `qsuite_delivered`: 115 reviews, only **7.8% non-rec**

**Older seat hardware** (`seat_product_generation`):
- `older_angled_or_partial_flat`: 81 reviews, **46.9% non-rec** (38 non-rec) vs. **8.7%** for `new_flat_bed_1x2x1`

Passengers who booked expecting a QSuite but received a standard flat-bed, or who received an older angled seat, disproportionately leave non-recommended reviews. `seat_change_notification_given` is nearly always `False` (590/592 reviews), indicating lack of proactive communication — though sample size is too small (2 `True`) to draw conclusions.

---

### 4. Service Inconsistency Across Legs (`service_consistency_across_legs`)

| Consistency           | Total | Non-rec rate |
|-----------------------|-------|-------------|
| consistent_high       | 300   | 1.7%        |
| variable_high_low     | 255   | 36.1%       |
| consistent_low        | 34    | **79.4%**   |

**27 non-rec reviews** have `consistent_low` service (79% non-rec rate). Another **92 non-rec reviews** come from `variable_high_low` experiences — where a good first leg sets expectations that are then violated on a connecting segment. This particularly affects multi-leg routes (e.g., Europe–Doha–Australia).

---

### 5. Food & Beverage Failures (`food_beverage_quality`)

| Food Quality         | Total | Non-rec rate |
|----------------------|-------|-------------|
| excellent            | 319   | 3.8%        |
| adequate             | 84    | 21.4%       |
| poor_taste_or_cold   | 48    | **47.9%**   |
| ran_out_of_options   | 7     | 57.1%       |
| limited_menu_choice  | 21    | 47.6%       |

**23 non-rec reviews** explicitly involve poor-tasting/cold food or running out of meal choices — a notable failure given Qatar's premium positioning.

---

### 6. FFP Elite Status Failures (`ffp_elite_status_failure`)

`ffp_elite_status_failure = True` appears in **18 reviews**, with a 38.9% non-rec rate (7 non-rec), versus 20.9% for those without. While the sample is small, loyalty program failures (e.g., elite perks not honored, miles not credited) modestly elevate non-recommendation. This is a secondary, low-coverage signal.

---

## Compounding Effects

Most non-recommended reviews reflect **multiple simultaneous failures**, not single-issue complaints:

| Number of failure factors | Count of non-rec reviews |
|--------------------------|-------------------------|
| 0 (no flagged failure)   | 15 (11.8%)              |
| 1                        | 33 (26.0%)              |
| 2                        | 35 (27.6%)              |
| 3                        | 27 (21.3%)              |
| 4+                       | 17 (13.4%)              |

*(Failure factors: poor/inconsistent crew, older/downgraded seat, consistent_low service, VFM ≤ 2, poor/scarce food)*

**89% of non-rec reviews have at least one flagged failure**, and **62% have two or more**. The most toxic combination is a seat product downgrade (especially QSuite-to-standard) paired with poor crew service — this combination captures 25 of the 41 QSuite-downgrade reviews and nearly all score VFM ≤ 2.

---

## Summary of Causal Drivers

| Factor | TAPP Column Used | Non-rec reviews affected | Non-rec rate in segment |
|--------|-----------------|--------------------------|------------------------|
| Low Value For Money (≤2) | — (structured) | 69 | 54% of all non-rec |
| Poor/disengaged crew | `cabin_crew_service_quality` | 52 | 69% rate in group |
| Older/angled seat hardware | `seat_product_generation` | 38 | 47% rate in group |
| QSuite downgrade | `seat_product_downgrade` | 25 | 61% rate in group |
| Consistently low service | `service_consistency_across_legs` | 27 | 79% rate in group |
| Poor food quality/availability | `food_beverage_quality` | 23 | ~50% rate in group |
| FFP elite failure | `ffp_elite_status_failure` | 7 | 39% rate in group (weak signal) |

---

## Method Note

**TAPP-generated columns used:** `seat_product_downgrade`, `seat_product_generation`, `seat_change_notification_given`, `cabin_crew_service_quality`, `service_consistency_across_legs`, `food_beverage_quality`, `ffp_elite_status_failure`.

All seven columns were examined. `seat_change_notification_given` was found to have near-zero positive coverage (2 `True` cases) and was not centered in the analysis. `ffp_elite_status_failure` showed a modest effect but low coverage (18 cases) and is reported as a secondary signal. All major claims are cross-validated against original structured columns (Overall Rating, Value For Money, Staff Service, Seat Comfort).
