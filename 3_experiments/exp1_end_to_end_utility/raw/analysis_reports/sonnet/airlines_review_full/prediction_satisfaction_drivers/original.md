---
dataset: airlines_review_full
scenario: prediction_satisfaction_drivers
variant: original
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating"
query: "What drives customer satisfaction (Overall Rating) across the different airlines?"
source_table: augment_table/airlines_review_full/prediction_satisfaction_drivers/original.csv
generated_at: 2026-08-03T05:43:25.373832+00:00
wall_seconds: 46.91
---

# Customer Satisfaction Drivers Across Airlines

**Dataset:** 8,100 airline reviews across 10 carriers | **Target:** Overall Rating (1–10)

---

## 1. The Dominant Driver: Value For Money

**Value For Money (VFM) is overwhelmingly the strongest predictor of Overall Rating**, both globally and within every individual airline.

| Metric | Value |
|---|---|
| Global correlation (VFM ↔ Overall Rating) | **r = 0.883** |
| Mean VFM for low-rated flights (Overall ≤ 3) | 1.52 / 5 |
| Mean VFM for high-rated flights (Overall ≥ 8) | 4.58 / 5 |

Per-airline correlations between VFM and Overall Rating range from **r = 0.75 (Qatar Airways)** to **r = 0.91 (Air France, Korean Air, Turkish Airlines)** — consistently the highest of any sub-score for every carrier. This suggests that customers ultimately frame their entire experience through a value lens: whether the product delivered matches the price paid.

---

## 2. Secondary Drivers: Staff Service and Seat Comfort

After VFM, **Staff Service** (r = 0.229) and **Seat Comfort** (r = 0.210) are the next most correlated sub-scores at the aggregate level. **Food & Beverages** (r = 0.160) and **Inflight Entertainment** (r = 0.140) are noticeably weaker predictors globally.

Within specific airlines, Staff Service gains more weight:
- **Japan Airlines**: Staff Service r = 0.25 (the highest among all airlines for that factor)
- **Korean Air**: Staff Service r = 0.21

This suggests service quality matters more as a differentiator on routes where passengers already expect hard-product parity.

---

## 3. Airline-Level Satisfaction Landscape

| Airline | Mean Overall Rating | Mean VFM | Mean Staff Service |
|---|---|---|---|
| All Nippon Airways | **7.95** | 4.17 | 4.51 |
| EVA Air | 7.42 | 4.00 | 4.26 |
| Qatar Airways | 7.20 | 3.80 | 4.29 |
| Japan Airlines | 7.10 | 3.77 | 4.24 |
| Singapore Airlines | 6.54 | 3.45 | 3.94 |
| Korean Air | 6.49 | 3.56 | 3.85 |
| Cathay Pacific Airways | 6.17 | 3.33 | 3.62 |
| Emirates | 4.67 | 2.75 | 2.97 |
| Air France | 4.64 | 2.67 | 3.27 |
| Turkish Airlines | **3.68** | **2.40** | **2.88** |

The ranking closely mirrors VFM scores: airlines perceived as offering poor value (Turkish Airlines, Air France, Emirates) cluster at the bottom regardless of their brand positioning. Notably, **Emirates** scores relatively well on Inflight Entertainment (mean 3.72) but still lands near the bottom — entertainment alone cannot compensate for poor VFM or staff perception.

---

## 4. Travel Class and Traveller Type Effects

**Travel class** matters, but as context rather than a primary driver:

| Class | Mean Overall Rating |
|---|---|
| First Class | 7.60 |
| Business Class | 6.65 |
| Premium Economy | 5.97 |
| Economy Class | 5.18 |

Higher classes are more satisfied, consistent with expectations being calibrated to price — reinforcing the centrality of VFM (passengers in premium cabins tend to rate value higher when the product matches the premium).

**Traveller type** shows modest variation: Solo Leisure travellers rate highest (6.07) while Family Leisure rates lowest (5.14), possibly due to the added complexity and stress of family travel amplifying service shortcomings.

---

## 5. Key Exceptions and Weak Evidence

- **Food & Beverages and Inflight Entertainment** are weak global predictors, though they may matter more in specific segments (long-haul, premium) — the dataset does not isolate route length.
- **Seat Comfort correlations within individual airlines are very low** (often < 0.15), suggesting customers may adapt expectations by carrier, making it hard to attribute satisfaction gains to seating alone.
- The VFM dominance could partly reflect **response bias**: dissatisfied customers may uniformly score all dimensions low, inflating cross-variable correlations. Causal interpretation requires caution.
- **Singapore Airlines** performs modestly (mean 6.54) despite a premium brand reputation, with relatively low VFM scores (3.45) — suggesting its premium pricing may not consistently meet expectations in this review sample.

---

## Summary

> **Value For Money is the single most powerful lever for Overall Rating across all airlines, explaining the vast majority of cross-airline satisfaction variance. Staff Service is the most meaningful secondary differentiator. Airlines wishing to improve ratings must address perceived value first; soft-product improvements (entertainment, food) are unlikely to compensate for a value gap.**
