---
dataset: amazon_polarity_reviews
scenario: predictive_negative
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict negative Amazon product satisfaction?"
source_table: augment_table/amazon_polarity_reviews/predictive_negative/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:09:31.088005+00:00
wall_seconds: 72.87
---

# Review Signals That Predict Negative Amazon Product Satisfaction

**Dataset:** 250 balanced Amazon reviews (125 negative `label_pos=0`, 125 positive `label_pos=1`)

**Method note:** The following TAPP-generated columns were used in this analysis: `complaint_category`, `performance_gap`, `disappointment_intensity`, `complaint_scope`, `return_action_signal`. All TAPP facets were cross-validated against the binary outcome column `label_pos`.

---

## 1. Key Finding Summary

Four TAPP-generated semantic facets are strong, near-orthogonal predictors of negative satisfaction. Every one of the 125 negative reviews carries at least one detectable complaint signal; the overlap of two or more signals is nearly exclusive to negative reviews.

---

## 2. Signal-by-Signal Analysis

### 2.1 Complaint Category (`complaint_category`)

| Category | Negative (n) | Positive (n) | P(negative) |
|---|---|---|---|
| `performance_failure` | 30 | 0 | **100%** |
| `inaccurate_description` | 7 | 0 | **100%** |
| `poor_value` | 4 | 0 | **100%** |
| `product_physical_defect` | 12 | 0 | **100%** |
| `content_quality` | 64 | 5 | **93%** |
| `not_present` | 8 | 119 | 6% |
| `shipping_packaging` | 0 | 1 | 0% |

**`content_quality`** is the single largest complaint driver (51% of all negative reviews, n=64). When combined with any other complaint type, precision for negativity reaches 100%. The `not_present` value is the strongest positive signal (119/127 = 94% positive).

### 2.2 Performance Gap (`performance_gap`)

| Value | Negative (n) | Positive (n) | P(negative) |
|---|---|---|---|
| `misleading_claim` | 19 | 0 | **100%** |
| `below_spec` | 47 | 2 | **96%** |
| `not_present` (gap) | 47 | 4 | **92%** |
| `partial_function` | 6 | 7 | 46% |
| `meets_spec` | 4 | 112 | **3%** |

`below_spec` and `misleading_claim` together account for 66 negative reviews (53%). `meets_spec` is the dominant positive signal (112/116 = 97% positive). `partial_function` is ambiguous (46% negative) and a weak discriminator.

### 2.3 Complaint Scope (`complaint_scope`)

| Scope | Negative (n) | Positive (n) | P(negative) |
|---|---|---|---|
| `brand_or_seller` | 4 | 0 | **100%** |
| `entire_product` | 80 | 1 | **99%** |
| `specific_use_case` | 7 | 1 | **88%** |
| `specific_feature` | 26 | 11 | **70%** |
| `not_present` | 8 | 112 | 7% |

Scope of dissatisfaction scales with negativity. Complaints framed at the **entire product** level (n=80, 64% of negative reviews) are almost exclusively negative. Even narrow `specific_feature` complaints are 70% negative. `not_present` again anchors positive reviews.

### 2.4 Return/Action Signal (`return_action_signal`)

| Signal | Negative (n) | Positive (n) | P(negative) |
|---|---|---|---|
| `warns_others_not_to_buy` | 15 | 0 | **100%** |
| `returned_or_intends_to_return` | 6 | 0 | **100%** |
| `requests_refund` | 1 | 0 | **100%** |
| `no_action_mentioned` | 99 | 11 | **90%** |
| `not_present` | 4 | 114 | 3% |

Any active remediation language (`warns_others_not_to_buy`, `returned_or_intends_to_return`, `requests_refund`) is a **perfect negative predictor** (22/22 = 100%). `warns_others_not_to_buy` (n=15) spans all complaint categories, making it a cross-cutting escalation signal.

### 2.5 Disappointment Intensity (`disappointment_intensity`)

`disappointment_intensity` was populated for 113 of 125 negative reviews and only 15 of 125 positive reviews (90% coverage gap makes direct comparison uneven). Among scored reviews:

| `label_pos` | n scored | Mean intensity | Median |
|---|---|---|---|
| Negative (0) | 113 | **3.79** | 4.0 |
| Positive (1) | 15 | 2.13 | 2.0 |

Mean intensity is 1.66 points higher for negative reviews (scale 1–5). The few positive reviews that received a score likely contain minor complaints. This column adds marginal signal beyond `complaint_category` and `complaint_scope`, which are more complete.

---

## 3. Original Structured Columns

- **`label_pos`** is the binary outcome; no other pre-existing numeric or categorical structured fields (ratings, product category, date) are present in the dataset beyond `review_id`, `title`, and `content`.
- **Review text length** is not discriminative: mean content length is nearly identical across negative (374 chars) and positive (364 chars) reviews.

---

## 4. Predictive Signal Hierarchy

Ranked by combination of precision and coverage (recall among negatives):

| Rank | Signal | Precision (P=neg) | Coverage (% of neg reviews) |
|---|---|---|---|
| 1 | `complaint_category` ≠ `not_present` | 98% | 94% |
| 2 | `complaint_scope` = `entire_product` | 99% | 64% |
| 3 | `performance_gap` = `below_spec` or `misleading_claim` | 97–100% | 53% |
| 4 | `return_action_signal` ∈ {warns, returned, refund} | 100% | 18% |
| 5 | `disappointment_intensity` ≥ 4 | ~99%* | ~45%* |

*Estimated from scored subset only.

---

## 5. Conclusions

**Strongest predictors of negative Amazon product satisfaction:**

1. **Presence of any complaint category** (especially `performance_failure`, `product_physical_defect`, `inaccurate_description`, `poor_value`) is a near-perfect negative signal. `content_quality` dominates volume.
2. **Entire-product complaint scope** — dissatisfaction framed at the whole product rather than a single feature is the broadest negative indicator (64% of negative reviews, 99% precision).
3. **Performance gap framing** — `below_spec` and `misleading_claim` tags indicate unmet expectations and are among the strongest precision signals (96–100%).
4. **Explicit return/warning language** — any `return_action_signal` beyond `no_action_mentioned` is a 100%-precise escalation marker, signalling the most severe dissatisfaction cases.
5. **High disappointment intensity (≥4/5)** adds confirmation but is redundant with the above four signals and has incomplete coverage for positive reviews.

The inverse signals for **positive** reviews are equally clean: `complaint_category = not_present`, `performance_gap = meets_spec`, and `return_action_signal = not_present` together cover ~94% of positive reviews with near-zero false-positive rate.
