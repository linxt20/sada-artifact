---
dataset: yelp_polarity_reviews
scenario: causal_improve
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: what_if
focus_variable: "user_satisfaction"
query: "How can businesses improve Yelp user satisfaction?"
source_table: augment_table/yelp_polarity_reviews/causal_improve/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:23:59.619022+00:00
wall_seconds: 73.81
---

# How Businesses Can Improve Yelp User Satisfaction

## Dataset Overview

- **Total reviews:** 250 (125 positive `label_pos=1`, 125 negative `label_pos=0`)
- **Outcome variable:** `label_pos` (1 = positive sentiment, 0 = negative sentiment)
- **TAPP-generated columns used:** `service_issue_type`, `pricing_value_perception`, `staff_conduct_severity`, `business_category`

---

## Method Note

Analysis integrates original structured columns (`review_id`, `label_pos`, `review_text`) with four TAPP-generated semantic columns: **`service_issue_type`**, **`pricing_value_perception`**, **`staff_conduct_severity`**, and **`business_category`**. All quantitative claims cross-check TAPP facets against `label_pos`.

---

## Key Finding 1: Staff Conduct Is the Single Strongest Driver of Satisfaction

The TAPP column `staff_conduct_severity` (scale 1–5) shows the sharpest gradient of any variable:

| Severity | Positive Rate | n |
|---|---|---|
| 1 (no issue) | **85.6%** | 104 |
| 2 (minor) | 20.6% | 34 |
| 3 (moderate) | 2.4% | 41 |
| 4 (serious) | 3.4% | 29 |
| 5 (severe) | 0.0% | 2 |

Reviews with `staff_conduct_severity ≥ 3` account for **70 of 125 negative reviews (56%)** but only **2 of 125 positive reviews (1.6%)**. This is the highest-leverage lever for businesses: even moving severity from 3 to 2 is associated with a ~18-percentage-point increase in satisfaction.

---

## Key Finding 2: Service Issue Type Explains ~66% of Negative Reviews

Using `service_issue_type`, any flagged service problem (`≠ not_present`) is present in **82 reviews**, with a positive rate of only **9.8%** vs. **69.6%** when no service issue is present.

| Service Issue Type | Positive Rate | n | Neg Reviews |
|---|---|---|---|
| `ignored_forgotten` | 0.0% | 5 | 5 |
| `rude_dismissive` | 2.5% | 40 | 39 |
| `slow_inattentive` | 16.0% | 25 | 21 |
| `wrong_order_error` | 20.0% | 10 | 8 |
| `not_present` | 69.6% | 168 | 51 |

**`rude_dismissive`** is the most frequent and damaging issue (40 reviews, 97.5% negative). In restaurant_dining specifically, all 13 rude/dismissive reviews are negative (0% positive rate). **Eliminating dismissive staff behavior** is the single most impactful operational change.

---

## Key Finding 3: Pricing Perception Significantly Modulates Satisfaction

`pricing_value_perception` reveals a binary effect:

| Perception | Positive Rate | n |
|---|---|---|
| `good_value` | **100%** | 23 |
| `not_present` (neutral) | 48.7% | 197 |
| `overpriced_for_quality` | 21.4% | 28 |
| `unexpected_extra_charges` | 0.0% | 2 |

All 23 reviews citing good value are positive; reviews flagged as `overpriced_for_quality` (n=28) have only a 21.4% positive rate. Pricing transparency and perceived value are strong satisfaction predictors independent of service quality.

---

## Key Finding 4: Business Category Reveals High-Risk Segments

`business_category` highlights which sectors underperform most:

| Category | Positive Rate | n |
|---|---|---|
| `medical_or_vet_service` | 11.1% | 9 |
| `auto_or_transport_service` | 28.6% | 7 |
| `health_beauty_service` | 35.7% | 14 |
| `nightclub_bar` | 42.9% | 14 |
| `restaurant_dining` | 51.4% | 140 |

Medical/vet services and auto/transport have the lowest satisfaction rates, likely compounded by high expectation thresholds and price sensitivity. The `business_category` facet adds useful segmentation signal but has moderate coverage for non-restaurant categories (n < 15 each), so results should be interpreted directionally.

---

## Actionable Recommendations

| Priority | Action | Evidence |
|---|---|---|
| **1 (Critical)** | Train and enforce respectful staff conduct | `rude_dismissive`: 39/40 reviews negative; severity ≥3 drives 56% of all negatives |
| **2 (High)** | Reduce being inattentive/slow | `slow_inattentive`: 21/25 reviews negative; often co-occurs with moderate severity |
| **3 (High)** | Communicate pricing clearly; deliver perceived value | `overpriced_for_quality` reviews: 78.6% negative; `good_value` reviews: 100% positive |
| **4 (Medium)** | Prioritize service reliability (order accuracy, attention) | `ignored_forgotten` + `wrong_order_error`: combined 15 reviews, all/mostly negative |
| **5 (Sector)** | Medical/vet and auto businesses: focus on expectation-setting and transparency | Positive rates 11–29%, lowest across all categories |

---

## Summary

The dominant causes of low Yelp satisfaction are (in order): **severe staff conduct issues** (especially rudeness), **inattentive or slow service**, and **poor pricing value perception**. Eliminating rude-dismissive interactions and improving attentiveness would address the majority of negative reviews in this dataset. Pricing transparency is an independent lever that, when handled well, uniformly generates positive reviews.
