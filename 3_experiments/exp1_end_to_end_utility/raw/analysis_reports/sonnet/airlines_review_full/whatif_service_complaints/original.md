---
dataset: airlines_review_full
scenario: whatif_service_complaints
variant: original
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "Overall Rating"
query: "If airlines eliminated the most common cabin-service complaints in the reviews, how much would the average Overall Rating improve?"
source_table: augment_table/airlines_review_full/whatif_service_complaints/original.csv
generated_at: 2026-08-03T05:44:09.037621+00:00
wall_seconds: 57.62
---

# What-If Analysis: Eliminating Cabin-Service Complaints and Impact on Overall Rating

## Dataset Overview

- **Total reviews:** 8,100  
- **Current average Overall Rating:** **5.63 / 10**  
- Cabin-service dimensions tracked: *Staff Service*, *Food & Beverages*, *Inflight Entertainment* (each rated 1–5)

---

## Identifying the Most Common Cabin-Service Complaints

A rating of ≤ 2 on a cabin-service dimension is treated as a complaint. Complaint frequencies:

| Cabin-Service Dimension | Complaint Reviews (rating ≤ 2) | Share of All Reviews |
|---|---|---|
| **Food & Beverages** | **2,346** | **29.0%** — most common |
| Staff Service | 2,212 | 27.3% |
| Inflight Entertainment | 1,605 | 19.8% |

**Food & Beverages** is the single most common source of cabin-service complaints, with 1,368 reviews rating it 1/5 and 978 rating it 2/5.

---

## Impact on Overall Rating

Reviews with a Food & Beverages complaint (≤ 2) average **4.88** on Overall Rating, versus **5.94** for reviews without such a complaint — a gap of **1.06 points**.

| Group | Avg Overall Rating |
|---|---|
| All reviews | 5.63 |
| F&B complaint reviews | 4.88 |
| No F&B complaint reviews | 5.94 |

### Counterfactual Estimate — Eliminating F&B Complaints

If the 2,346 F&B-complaint reviews had been lifted to the non-complaint average (i.e., those service failures were eliminated):

$$\text{New Avg} = \frac{\sum_{\text{non-complaint}} \text{Rating} + 2346 \times 5.94}{8100} \approx \mathbf{5.94}$$

> **Estimated improvement: +0.31 points** (from 5.63 → 5.94)

---

## Broader Scenario — Eliminating All Cabin-Service Complaints

If all cabin-service complaints (Staff Service, F&B, or IFE ≤ 2) were resolved:

- Affected reviews: **4,420** (54.6% of all reviews)
- Non-complaint baseline avg: **6.48**
- Counterfactual overall average: **~6.48**
- **Estimated improvement: +0.84 points** (from 5.63 → 6.48)

### Correlation with Overall Rating

| Dimension | Correlation with Overall Rating |
|---|---|
| Staff Service | 0.23 |
| Inflight Entertainment | 0.14 |
| Food & Beverages | 0.16 |

Correlations are modest (~0.14–0.23), meaning cabin-service sub-ratings explain only part of the Overall Rating variance. Other factors (seat comfort, value for money, flight operations) also drive scores.

---

## Key Patterns and Exceptions

- **Economy Class** accounts for the majority of F&B complaints (1,649 of 2,346), consistent with generally lower catering standards in that cabin.
- **Staff Service** has the largest gap between complaint and non-complaint Overall Ratings (1.53 points), making it arguably the highest-leverage improvement even though it is the second most frequently complained-about dimension.
- Correlations are statistically meaningful but modest, suggesting that **many passengers rate Overall poorly for multiple reasons simultaneously** — eliminating one complaint type alone may not fully recover the 1+ point gap.
- The counterfactual assumes linear additive effects and that no review has hidden confounders (e.g., a flight delay) that independently drag down both cabin ratings and Overall Rating.

---

## Summary

| Scenario | Estimated Average Overall Rating | Gain |
|---|---|---|
| Baseline (current) | 5.63 | — |
| Eliminate F&B complaints only | ~5.94 | **+0.31** |
| Eliminate all cabin-service complaints | ~6.48 | **+0.84** |

Addressing Food & Beverages — the most common complaint — would yield a modest but meaningful **~0.3-point** improvement. A broader campaign targeting all cabin-service failures (staff, food, entertainment) could lift the average by **~0.8 points**, approaching a score of 6.5/10. Given that Staff Service has the strongest correlation with Overall Rating, airlines seeking the highest return on investment should prioritize crew training alongside food quality improvements.
