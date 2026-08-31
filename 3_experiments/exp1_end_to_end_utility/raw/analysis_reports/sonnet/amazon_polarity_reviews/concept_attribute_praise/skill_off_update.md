---
dataset: amazon_polarity_reviews
scenario: concept_attribute_praise
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "praise_and_complaint_drivers"
query: "What drives praise and complaints in Amazon reviews?"
source_table: augment_table/amazon_polarity_reviews/concept_attribute_praise/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:01:57.164440+00:00
wall_seconds: 44.59
---

# What Drives Praise and Complaints in Amazon Reviews?

**Dataset:** 250 reviews (125 positive / 125 negative) with engineered signal columns: `praise_signal_count`, `complaint_signal_count`, `dominant_driver`, `mentioned_aspects`, `repeat_purchase_signal`, `has_comparison`, `exclamation_count`, and `review_length_bucket`.

---

## 1. Dominant Driver Distribution

| Driver | Negative (label=0) | Positive (label=1) |
|---|---|---|
| `praise_driven` | 23 (18%) | **76 (61%)** |
| `complaint_driven` | **37 (30%)** | 3 (2%) |
| `neutral` | 57 (46%) | 45 (36%) |
| `mixed` | 8 (6%) | 1 (1%) |

Positive reviews are predominantly `praise_driven` (61%), while negative reviews split between `complaint_driven` (30%) and a large `neutral` block (46%). The high share of `neutral` across both classes is a key limitation—nearly half of all reviews were not assigned a clear directional driver, suggesting the signal extraction was conservative or many reviews rely on implicit sentiment.

---

## 2. Praise and Complaint Signal Counts

| Metric | Negative (label=0) | Positive (label=1) |
|---|---|---|
| Mean `praise_signal_count` | 0.30 | **0.98** |
| Mean `complaint_signal_count` | **0.42** | 0.06 |

Praise signals are ~3× more concentrated in positive reviews; complaint signals are ~7× more concentrated in negative reviews. Signal counts top out at 4 (praise) and 2 (complaint), indicating most reviews carry at most one explicit signal per direction.

---

## 3. Mentioned Aspects

The dominant aspect tag is `general` for both polarities (~70%), meaning the majority of reviews do not pinpoint a specific product dimension.

Among reviews **with** specific aspects:
- **Positive reviews** most frequently cite `performance` (10), `value` (9), and `quality` (6).
- **Negative reviews** most frequently cite `value` (7), `performance` (6), `quality` (4), and `customer_service` (3+).

Both polarities converge on `performance` and `value` as the top named drivers—praise for meeting expectations on these dimensions; complaints for falling short. `customer_service` appears only in negative reviews, acting as a pure complaint driver.

---

## 4. Behavioural Signals

| Signal | Negative (label=0) | Positive (label=1) |
|---|---|---|
| `repeat_purchase_signal` rate | **9.6%** | 2.4% |
| `has_comparison` rate | 4.0% | **8.0%** |
| Mean `exclamation_count` | 0.97 | **1.15** |

- **Repeat purchase** is paradoxically higher in negative reviews (9.6% vs 2.4%). This likely reflects regret-purchase narratives ("I keep buying this hoping it improves") rather than loyalty—an important exception to the usual interpretation.
- **Comparisons** are modestly more frequent in positive reviews, suggesting satisfied buyers more often benchmark favorably against alternatives.
- **Exclamation marks** are slightly higher in positive reviews, consistent with enthusiasm, but the difference is small and should not be over-weighted.

---

## 5. Review Length

| Length | Negative | Positive |
|---|---|---|
| Short | 11 | 21 |
| Medium | 80 | 66 |
| Long | 34 | 38 |

Positive reviews skew slightly shorter; negative reviews concentrate in medium length. Long reviews are roughly balanced. Length alone is not a reliable predictor of sentiment in this dataset.

---

## 6. Key Findings

1. **Praise is the primary driver of positive reviews**—explicit praise signals and `praise_driven` classification strongly predict `label_pos = 1`.
2. **Complaint signals are a reliable negative indicator** but cover only ~30% of negative reviews; a large neutral residual suggests that absence of praise (rather than active complaint) is another path to negative ratings.
3. **Performance, value, and quality** are the core named battlegrounds; customer service complaints appear exclusively on the negative side.
4. **Repeat purchase is not a reliable positivity signal** here—it appears more in negative reviews, possibly reflecting habitual but dissatisfied buyers.
5. **Aspect tagging is coarse**—70%+ of reviews are tagged `general`, limiting fine-grained conclusions about specific product dimensions.
