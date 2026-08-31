---
dataset: airlines_review_full
scenario: eda_rating_drivers
variant: original
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "Overall Rating"
query: "Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?"
source_table: augment_table/airlines_review_full/eda_rating_drivers/original.csv
generated_at: 2026-08-03T05:41:32.127492+00:00
wall_seconds: 62.65
---

# Review Themes & Overall Rating Drivers: Airlines Dataset
**Dataset:** 8,100 reviews | **Focus variable:** Overall Rating (1–10, mean 5.63)

---

## 1. Dominant Rating Driver: Value For Money

Across every segment, **Value For Money** is overwhelmingly the strongest predictor of Overall Rating (r ≈ 0.88 globally). This holds without exception:

| Segment | Value For Money r | Next-strongest |
|---|---|---|
| Business travellers | 0.873 | Staff Service (0.19) |
| Couple Leisure | 0.888 | Staff Service (0.20) |
| Family Leisure | 0.897 | Staff Service (0.29) |
| Solo Leisure | 0.875 | Staff Service (0.23) |
| Economy Class | 0.890 | Staff Service (0.24) |
| Business Class | 0.853 | Staff Service (0.19) |
| First Class | 0.840 | Food & Beverages (0.16) |
| Premium Economy | 0.884 | Seat Comfort (0.25) |

High-rated reviews (7–10) average a **Value For Money score of 4.48/5**, while low-rated reviews (1–3) average just **1.52/5** — the widest spread of any sub-rating dimension.

---

## 2. Secondary Themes: Staff Service and Seat Comfort

**Staff Service** is the second-most correlated factor for most traveller types and Economy/Business Class. For **Family Leisure** travellers it is notably stronger (r = 0.287) than for other groups, suggesting families weight crew interaction more heavily.

**Seat Comfort** matters more in Economy and Premium Economy (r ≈ 0.22–0.25) than in Business Class (r = 0.15) or First Class (r = 0.06), reflecting a floor-effect — higher-class seats are generally comfortable enough not to be a differentiator.

**Food & Beverages** and **Inflight Entertainment** are weakly correlated (r ≈ 0.10–0.19 depending on segment) and are secondary themes across all groups. In First Class, Food & Beverages slightly edges out other secondary factors (r = 0.16), the only class where cuisine becomes relatively more prominent.

---

## 3. Overall Rating by Type of Traveller

| Type of Traveller | Mean Overall Rating | Recommended % |
|---|---|---|
| Solo Leisure | **6.07** | **59.3%** |
| Couple Leisure | 5.48 | 49.1% |
| Business | 5.38 | 50.2% |
| Family Leisure | **5.14** | **46.7%** |

Solo Leisure travellers rate consistently higher, likely because they tend to fly more premium cabins and have lower expectation mismatches. Family Leisure travellers rate lowest — their Value For Money mean (2.95) is the lowest across traveller types, suggesting perceived poor value relative to cost.

---

## 4. Overall Rating by Cabin Class

| Class | Mean Overall Rating | Recommended % |
|---|---|---|
| First Class | **7.60** | **76.9%** |
| Business Class | 6.65 | 66.4% |
| Premium Economy | 5.97 | 56.6% |
| Economy Class | **5.18** | **47.0%** |

There is a clear monotonic premium-cabin advantage. Economy Class scores lower on every sub-dimension, particularly Value For Money (mean 2.99 vs. 3.79 for First Class).

**Notable exception:** Premium Economy does not clearly outperform Economy on Staff Service (3.82 vs 3.49) enough to lift its overall score much beyond Economy — its Value For Money score (3.11) is lower than Business Class (3.52), indicating Premium Economy passengers feel under-served for the price premium paid.

---

## 5. Cross-Segment: Traveller × Class

| Traveller \ Class | Business | Economy | First | Prem. Eco |
|---|---|---|---|---|
| Solo Leisure | **7.29** | 5.57 | **8.21** | 6.52 |
| Couple Leisure | 6.83 | 4.89 | 7.38 | 5.70 |
| Family Leisure | 6.45 | 4.87 | 5.55 | 6.02 |
| Business | 5.80 | 4.96 | 6.87 | 5.22 |

- **Highest ratings:** Solo Leisure in First Class (8.21) and Business Class (7.29)
- **Lowest ratings:** Economy Class travellers across all non-solo types (≈4.87–4.96)
- **Family Leisure in First Class (5.55)** is a notable outlier — despite flying the premium cabin, families rate lower than Solo/Couple travellers in the same class, possibly due to unmet expectations around child-friendliness or space
- **Business travellers in Business Class (5.80)** trail Leisure travellers in the same cabin, suggesting frequent flyers apply stricter standards

---

## 6. Summary: High vs. Low Rating Themes

**Themes associated with higher Overall Rating:**
- **High perceived Value For Money** — by far the dominant theme in every segment
- Premium cabin class (First > Business > Premium Eco > Economy)
- Solo or Couple travel context
- Strong Staff Service — especially relevant for Family Leisure and Economy Class passengers

**Themes associated with lower Overall Rating:**
- **Poor Value For Money perception** — consistently the key differentiator
- Economy Class travel (lowest sub-ratings on all dimensions)
- Family Leisure context (lowest VFM perception, toughest reviewers)
- Business travellers in premium cabins show a professional-expectations penalty

**Weak or limited evidence:**
- Food & Beverages and Inflight Entertainment have modest correlations (0.10–0.19) and are not primary drivers in any segment
- Staff Service in First Class shows near-zero correlation (r = −0.004), suggesting it is not a differentiator at the top of the market
