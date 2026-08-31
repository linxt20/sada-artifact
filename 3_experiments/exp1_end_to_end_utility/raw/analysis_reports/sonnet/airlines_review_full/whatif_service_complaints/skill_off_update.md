---
dataset: airlines_review_full
scenario: whatif_service_complaints
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "Overall Rating"
query: "If airlines eliminated the most common cabin-service complaints in the reviews, how much would the average Overall Rating improve?"
source_table: augment_table/airlines_review_full/whatif_service_complaints/sonnet__skill_off_update.csv
generated_at: 2026-08-03T05:44:18.797760+00:00
wall_seconds: 41.45
---

# What-If Analysis: Eliminating Cabin-Service (Food & Beverage) Complaints

## Dataset Overview
- **Total reviews:** 8,100
- **Focus variable:** Overall Rating (scale 1–10; mean = **5.63**, median = 6)
- **Complaint flag:** `is_food_service_complaint` — identifies reviews containing food/cabin-service complaints

---

## Prevalence of Food/Cabin-Service Complaints

| Segment | Count | Share |
|---|---|---|
| Reviews **with** food-service complaint | 2,346 | **29.0%** |
| Reviews **without** food-service complaint | 5,754 | 71.0% |

Nearly **1 in 3 reviews** contains an identifiable food or cabin-service complaint, making this the single most common complaint category in the dataset.

---

## Impact on Overall Rating

### Observed ratings
| Group | Avg Overall Rating |
|---|---|
| With food-service complaint | **4.88** |
| Without food-service complaint | **5.94** |
| **Gap** | **−1.06 points** |

Reviewers who raise food/cabin-service complaints rate their experience on average **1.06 points lower** than those who do not, a substantial difference on a 10-point scale.

### Model-predicted improvement (counterfactual)
The dataset includes predicted ratings under both baseline and complaint-free scenarios:

| Metric | Value |
|---|---|
| Mean predicted Overall Rating (baseline) | 5.633 |
| Mean predicted Overall Rating (no food complaint) | 5.668 |
| **Estimated improvement** | **+0.035 points** |
| Avg lift among affected reviews only | +0.12 points |
| Maximum lift for any single review | +0.14 points |

Eliminating food-service complaints is estimated to raise the fleet-wide **average Overall Rating by ~0.04 points** (on a 10-point scale). This is modest in absolute terms because:
1. The predicted lift per affected review is small (capped at ~0.14 points in the model).
2. The model captures diminishing returns — many complaint-havers already gave low overall scores driven by multiple issues, not food alone.

---

## Complaint Rate by Cabin Class

| Class | Complaint Rate |
|---|---|
| Economy Class | 30.0% |
| Premium Economy | 29.6% |
| First Class | 26.4% |
| Business Class | 26.4% |

Economy and Premium Economy passengers complain about food/cabin service at slightly higher rates, suggesting these classes offer the greatest improvement opportunity.

---

## Supporting Signal: Food & Beverages Sub-Score

| Group | Avg Food & Beverages Rating |
|---|---|
| With complaint | **1.42 / 5** |
| Without complaint | **4.19 / 5** |

The `Food & Beverages` sub-score closely mirrors the complaint flag, confirming internal consistency. Improving catering quality to close even half this gap would be operationally meaningful.

---

## Key Caveats

- **Model ceiling effect:** The predicted lift is bounded (max 0.14 points), suggesting the model treats food satisfaction as one of several drivers of Overall Rating — not the dominant one. Seat comfort, staff service, and value for money also matter.
- **Correlation ≠ causation:** Complaint-associated reviews may reflect a generally negative travel experience; eliminating food complaints alone may not fully recover the 1.06-point observed gap.
- **Weak evidence for premium classes:** Business and First Class complaint rates are lower, so the aggregate benefit would be concentrated in Economy operations.
- **29% complaint prevalence** is high enough that even small per-review improvements compound across the fleet.

---

## Summary

If airlines eliminated the most common cabin-service (food & beverage) complaints, the model estimates the average Overall Rating would improve by approximately **+0.04 points** (from 5.63 → 5.67). The observed rating gap between complaint and non-complaint reviews is a larger **1.06 points**, but causal attribution to food alone is limited — other correlated dissatisfiers account for much of that gap. The clearest actionable target is **Economy Class**, where complaint rates are highest (~30%) and volume is greatest.
