---
dataset: yelp_polarity_reviews
scenario: predictive_low
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict low Yelp user satisfaction?"
source_table: augment_table/yelp_polarity_reviews/predictive_low/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:24:36.821240+00:00
wall_seconds: 63.72
---

# What Review Signals Predict Low Yelp User Satisfaction?

**Dataset:** 250 reviews (125 low-satisfaction `label_pos=0`, 125 high-satisfaction `label_pos=1`), balanced split.  
**Method note:** TAPP-generated columns used — `staff_attitude`, `complaint_intensity`, `unresolved_complaint`, `revisit_intent`. All four were informative; `complaint_intensity` had 101 missing values (present for 149/250 reviews, 98% coverage in negative reviews).

---

## Key Findings

Four signals — spanning raw review text semantics and TAPP-extracted facets — strongly and independently predict low satisfaction. When combined, they approach near-perfect discrimination.

### 1. Unresolved Complaints (`unresolved_complaint`)

The single highest-recall predictor.

| unresolved_complaint | Low-sat (label=0) | High-sat (label=1) | Precision | Recall |
|---|---|---|---|---|
| True | **91** | 5 | **0.95** | **0.73** |
| False | 34 | 120 | — | — |

**73% of all low-satisfaction reviews** contain an unresolved complaint, vs. only 4% of positive reviews. This is the strongest individual signal.

---

### 2. Staff Attitude (`staff_attitude`)

Negative staff attitude categories are nearly exclusive to low-satisfaction reviews.

| staff_attitude | Low-sat | High-sat | Neg. rate |
|---|---|---|---|
| `rude_hostile` | 27 | 0 | **100%** |
| `discriminatory` | 1 | 0 | **100%** |
| `dismissive_indifferent` | 25 | 1 | 96% |
| `unprofessional` | 7 | 1 | 88% |
| `not_present` | 58 | 72 | 45% |
| `friendly_positive` | 7 | 51 | 12% |

Collectively, negative staff attitude (`rude_hostile` + `dismissive_indifferent` + `unprofessional` + `discriminatory`) identifies 60 low-satisfaction reviews with **precision 0.97** and recall 0.48. `friendly_positive` is a strong positive-satisfaction signal (51/58 = 88% positive).

---

### 3. Revisit Intent (`revisit_intent`)

| revisit_intent | Low-sat | High-sat | Neg. rate |
|---|---|---|---|
| `will_not_return` | 47 | 1 | **98%** |
| `unlikely_to_return` | 6 | 0 | **100%** |
| `neutral_or_uncertain` | 15 | 6 | 71% |
| `not_present` | 56 | 74 | 43% |
| `will_definitely_return` | 1 | 27 | 4% |
| `likely_to_return` | 0 | 17 | 0% |

`will_not_return` / `unlikely_to_return` combined: **precision 0.98, recall 0.42**. This facet serves as a strong near-confirming signal when present.

---

### 4. Complaint Intensity (`complaint_intensity`)

Available for 149/250 reviews (123 negative, 26 positive with scores).

| | Low-sat (n=123) | High-sat (n=26) |
|---|---|---|
| Mean | **3.19** | **1.65** |
| Median | 3.0 | 2.0 |
| ≥ 4 (high intensity) | 45 | 1 |

High-intensity complaints (score ≥ 4) identify low-satisfaction reviews with **precision 0.98, recall 0.36** among the scored subset. The ~1.5-point mean gap is substantial given the 1–5 scale.

---

### Combined Signal Performance

Combining `unresolved_complaint=True` AND negative `staff_attitude`:

| Combo signal | Low-sat | High-sat | Precision |
|---|---|---|---|
| Both present | **57** | 2 | **0.97** |
| Not both | 68 | 123 | — |

A union of all four signals (any one triggered) would cover the vast majority of low-satisfaction reviews with high precision.

---

## Summary: Predictive Signal Ranking

| Signal | Precision | Recall | Coverage |
|---|---|---|---|
| `complaint_intensity` ≥ 4 | 0.98 | 0.36 | Partial (149 reviews) |
| `revisit_intent` = will_not_return/unlikely | 0.98 | 0.42 | Full |
| `staff_attitude` = rude/dismissive/unprofessional | 0.97 | 0.48 | Full |
| `unresolved_complaint` = True | 0.95 | **0.73** | Full |

**Conclusion:** Low Yelp satisfaction is most reliably predicted by the presence of an **unresolved complaint** (broadest coverage), combined with **negative staff attitude** (rude, dismissive, or unprofessional). Explicit statements of **intent not to return** and **high complaint intensity scores** serve as near-certain confirmatory signals when present. Positive-satisfaction reviews are strongly characterized by `friendly_positive` staff attitude and `will_definitely_return` / `likely_to_return` revisit intent — the absence of these is a soft but meaningful negative signal.
