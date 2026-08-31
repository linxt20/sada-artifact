---
dataset: yelp_polarity_reviews
scenario: causal_improve
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "user_satisfaction"
query: "How can businesses improve Yelp user satisfaction?"
source_table: augment_table/yelp_polarity_reviews/causal_improve/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:23:37.145475+00:00
wall_seconds: 53.8
---

# How Businesses Can Improve Yelp User Satisfaction

**Dataset:** 250 Yelp reviews, balanced (125 positive `label_pos=1`, 125 negative `label_pos=0`) across seven business categories. Augmented columns capture `staff_conduct`, `value_perception`, `atmosphere_ambiance_signal`, `visit_context`, and `business_category`.

---

## 1. Staff Conduct Is the Strongest Lever

Staff behavior is the single most powerful predictor of review sentiment in this dataset.

| `staff_conduct` value | Positive review rate | N |
|---|---|---|
| `friendly_positive` | **85%** | 75 |
| `dismissive_unhelpful` | 8% | 50 |
| `rude_aggressive` | **0%** | 23 |
| `unprofessional_inappropriate` | **0%** | 5 |
| *(not mentioned)* | 59% | 97 |

**Implication:** Friendly, engaged staff are nearly a guarantee of a positive review. Rude or dismissive behavior is a near-guarantee of a negative one. Training staff in hospitality and conflict resolution offers the highest ROI of any single improvement.

---

## 2. Value Perception Drives Satisfaction in a Binary Fashion

When customers comment on pricing, the verdict is stark:

| `value_perception` value | Positive review rate | N |
|---|---|---|
| `good_value_positive` | **100%** | 27 |
| `fair_value` | 100% | 3 |
| `overpriced_poor_value` | 18% | 28 |
| `pricing_surprise_hidden_charge` | **0%** | 2 |

The majority of reviews (190/250) do not mention value at all. When pricing *is* mentioned negatively, it almost always produces a negative review. Transparent pricing and eliminating hidden charges are low-cost signals of trustworthiness.

---

## 3. Atmosphere and Ambiance Have a Moderate but Consistent Effect

| `atmosphere_ambiance_signal` | Positive review rate | N |
|---|---|---|
| `positive_ambiance` | **76%** | 33 |
| `noise_crowding_issue` | 20% | 10 |
| `decor_condition_poor` | 29% | 7 |
| `layout_seating_discomfort` | 0% | 2 |
| *(not mentioned)* | 48% | 198 |

Positive ambiance strongly correlates with satisfaction. Noise/crowding and poor decor depress satisfaction rates. This category has a smaller sample than staff conduct, so caution is warranted in over-weighting it, but the directional signal is consistent.

---

## 4. Visit Context: Group / Special Events Are a Hidden Win

| `visit_context` | Positive review rate | N |
|---|---|---|
| `special_event_group` | **88%** | 8 |
| `dine_in_regular` | 48% | 142 |
| `first_time_visitor` | 17% | 6 |

Special-event visits yield disproportionately positive reviews (though N=8 is small). First-time visitors are at risk of disappointment — businesses should invest in first-impression protocols. **Note:** the N for non-regular contexts is too small for strong causal claims.

---

## 5. Business Category Context

Restaurant/food (151 reviews) is the dominant category and shows near-balanced sentiment (72 negative, 79 positive). Medical/veterinary skews negative (8 vs. 1), while retail and hotel/accommodation lean slightly positive. Category-specific norms matter, but the staff-conduct and value signals hold across verticals.

---

## Summary: Priority Actions

| Priority | Action | Evidence Strength |
|---|---|---|
| 🔴 High | Train staff to be friendly and professional; eliminate rude/dismissive behavior | Strong — large N, near-zero positive rate for rude staff |
| 🔴 High | Eliminate hidden charges; communicate pricing clearly | Strong — 0% positive when surprise charges appear |
| 🟡 Medium | Invest in ambiance (noise control, decor maintenance) | Moderate — consistent directional signal, smaller N |
| 🟡 Medium | Create dedicated onboarding for first-time visitors | Weak evidence — only 6 first-time reviews |
| 🟢 Opportunity | Capitalize on group/event occasions with tailored service | Promising but very small sample |

---

*Limitations: The dataset is balanced by design (125/125), so base rates do not reflect real-world Yelp distributions. Many reviews (~40%) do not trigger staff or value labels, making "not_present" a noisy catch-all. Causal direction (staff behavior → satisfaction) is inferred from text patterns, not experimental data.*
