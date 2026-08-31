---
dataset: airlines_review
scenario: focus_inference
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's in these airline reviews — I'm not sure which aspect is most worth analyzing."
source_table: augment_table/airlines_review/focus_inference/original.csv
generated_at: 2026-07-26T12:49:39.684275+00:00
wall_seconds: 65.4
---

# Airline Reviews Dataset — Exploratory Analysis

## Dataset Overview

| Attribute | Detail |
|---|---|
| Total reviews | 900 |
| Date range | Approx. 2023–2024 |
| Columns | Title, Name, Review Date, Verified, Reviews (text), Type of Traveller, Month Flown, Route, Class, Seat Comfort, Staff Service, Food & Beverages, Inflight Entertainment, Value For Money, Overall Rating, Recommended |

Sub-ratings (Seat Comfort, Staff Service, Food & Beverages, Inflight Entertainment, Value For Money) are scored **1–5**; Overall Rating is scored **1–10**. All 900 rows have complete numeric data.

---

## Most Analytically Valuable Aspect: **Value For Money**

Of all available dimensions, **Value For Money (VFM)** is the clearest signal in this dataset.

### Correlations with Overall Rating

| Sub-Rating | Correlation with Overall Rating |
|---|---|
| **Value For Money** | **0.885** |
| Food & Beverages | 0.087 |
| Staff Service | 0.070 |
| Seat Comfort | 0.011 |
| Inflight Entertainment | −0.033 |

VFM has an overwhelming correlation (r ≈ 0.89) with Overall Rating, while every other sub-rating is essentially flat. This suggests passengers' overall satisfaction is primarily a reflection of whether they felt they got their money's worth — not any specific service element.

### VFM and the Recommendation Decision

| VFM Score | Count |
|---|---|
| 1 | 167 |
| 2 | 86 |
| 3 | 126 |
| 4 | 223 |
| 5 | 298 |

- **73.4%** of all "not recommended" reviews (235 / 320) have VFM ≤ 2.
- Among reviewers who would recommend the airline, mean VFM = **4.34** vs **1.82** for those who would not.
- Mean Overall Rating: 8.61 (recommended) vs 2.77 (not recommended).

The recommendation split (580 yes / 320 no, ≈ 64% / 36%) is therefore largely explained by VFM alone.

---

## Secondary Aspects Worth Examining

### Cabin Class

| Class | N | Mean Overall Rating |
|---|---|---|
| First Class | 14 | 7.93 |
| Business Class | 237 | 7.10 |
| Economy Class | 563 | 6.37 |
| Premium Economy | 86 | 5.83 |

First Class and Business Class reviewers rate higher on average. Notably, **Premium Economy scores lower than Economy** — possibly a value-for-money perception issue given its higher price tier. However, First Class n = 14 is small; treat that mean cautiously.

### Traveller Type

| Type | N | Mean Overall Rating |
|---|---|---|
| Solo Leisure | 332 | 6.87 |
| Family Leisure | 180 | 6.57 |
| Couple Leisure | 242 | 6.37 |
| Business | 146 | 5.99 |

Business travellers rate slightly lower — plausibly due to higher expectations or cost sensitivity — but differences are modest.

### Service Sub-Ratings (Context)

All sub-ratings are mid-range on average:

| Sub-Rating | Mean (out of 5) |
|---|---|
| Staff Service | 3.93 |
| Inflight Entertainment | 3.89 |
| Seat Comfort | 3.68 |
| Food & Beverages | 3.57 |
| Value For Money | 3.44 |

Staff Service is the highest-rated element, and VFM the lowest — consistent with the idea that passengers are broadly satisfied with service delivery but feel the price is not fully justified. Food & Beverages shows the largest gap between recommended (3.65) and not-recommended (3.42) groups after VFM, making it a potential secondary driver.

---

## Key Takeaways

1. **Focus analysis on Value For Money** — it is the primary driver of overall ratings and recommendation decisions, far outweighing any other scored dimension.
2. **Premium Economy is an outlier to investigate** — it scores worse than Economy despite higher prices, which is a concrete operational concern.
3. **Staff Service and Inflight Entertainment are relative strengths** but show little discriminatory power between happy and unhappy passengers in this dataset.
4. **The free-text Reviews column** is present and could unlock nuances (e.g., specific complaints, route-level issues) that numeric scores obscure.
5. **Weak evidence caution**: correlations between Seat Comfort / Entertainment and Overall Rating are near zero, so those dimensions should not be prioritised for improvement based on this data alone.
