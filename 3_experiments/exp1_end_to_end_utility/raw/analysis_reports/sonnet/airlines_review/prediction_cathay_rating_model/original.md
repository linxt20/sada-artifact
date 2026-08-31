---
dataset: airlines_review
scenario: prediction_cathay_rating_model
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating_gt7"
query: "(Cathay MD) Build a model to organise/optimise routes and service so Overall Rating > 7."
source_table: augment_table/airlines_review/prediction_cathay_rating_model/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/airlines_review__prediction_cathay_rating_model/analyses/original/analysis.md
wall_seconds: 274.57
---

# Cathay Pacific Airways: Model to Achieve Overall Rating > 7

## 1. Dataset Overview

| Attribute | Value |
|---|---|
| Airline | Cathay Pacific Airways (all 744 rows) |
| Rating range | 1 – 10 (1–5 sub-scales) |
| Reviews with Overall Rating > 7 | **348 / 744 (46.8%)** |
| Median Overall Rating | 7 |
| Missing values | None |

Sub-rating columns: **Seat Comfort, Staff Service, Food & Beverages, Inflight Entertainment, Value For Money** (all 1–5 scale).

---

## 2. Key Driver: Value For Money Dominates

Correlation with Overall Rating and standardised logistic-regression coefficients both point to a single dominant signal:

| Sub-rating | Pearson r with Overall Rating | Standardised LR coefficient |
|---|---|---|
| **Value For Money** | **0.877** | **3.10** |
| Seat Comfort | 0.156 | 0.29 |
| Food & Beverages | 0.109 | 0.11 |
| Staff Service | 0.110 | 0.11 |
| Inflight Entertainment | 0.089 | 0.05 |

Value For Money alone is 3–6× more predictive than any other sub-dimension.

### VFM Score → Probability of Rating > 7

| VFM Score | % Reviews with Rating > 7 | Mean Overall Rating |
|---|---|---|
| 1 | 0% | 1.71 |
| 2 | 0% | 3.49 |
| 3 | 17% | 5.27 |
| **4** | **70%** | **7.96** |
| **5** | **93%** | **9.13** |

**Actionable threshold: VFM ≥ 4 is the primary lever.** When passengers rate VFM ≥ 4, 82% give an Overall Rating > 7.

---

## 3. Predictive Model Performance

Three classifiers were trained on sub-ratings + Class + Type of Traveller, cross-validated (5-fold stratified):

| Model | ROC-AUC | Accuracy |
|---|---|---|
| **Logistic Regression** | **0.938 ± 0.020** | **87.2%** |
| Random Forest | 0.929 ± 0.017 | 85.2% |
| Gradient Boosting | 0.919 ± 0.019 | 85.2% |

The logistic regression achieves near-perfect discrimination, confirming that the sub-rating dimensions are highly informative. A threshold rule of VFM ≥ 4 alone yields **Precision = 0.82, Recall = 0.94**, covering 53% of passengers.

### Random Forest Feature Importances

| Feature | Importance |
|---|---|
| Value For Money | 0.561 |
| Food & Beverages | 0.078 |
| Seat Comfort | 0.076 |
| Inflight Entertainment | 0.075 |
| Staff Service | 0.069 |
| Type of Traveller | 0.057 |
| Class | 0.056 |
| Verified | 0.028 |

---

## 4. Segment Analysis

### 4.1 By Cabin Class

| Class | Mean VFM | % Rating > 7 | % Rating > 7 if VFM ≥ 4 |
|---|---|---|---|
| Business Class | 3.66 | 59% | 89% |
| First Class | 3.62 | 50% | 60%* |
| Premium Economy | 3.15 | 39% | 76% |
| Economy Class | 3.21 | 43% | 81% |

*First Class has only 16 reviews — treat with caution.

**Business Class** shows the best baseline performance. Economy Class underperforms on VFM (mean 3.21) but responds strongly once VFM is improved (81% > 7 when VFM ≥ 4).

### 4.2 By Type of Traveller

| Traveller Type | Mean Rating | % > 7 |
|---|---|---|
| Solo Leisure | 6.68 | 54% |
| Family Leisure | 5.97 | 45% |
| Business | 5.83 | 43% |
| Couple Leisure | 5.56 | 37% |

Solo Leisure passengers rate highest. Couple Leisure is the lowest-performing segment.

### 4.3 Class × Traveller Type (% Rating > 7)

| Class | Business | Couple Leisure | Family Leisure | Solo Leisure |
|---|---|---|---|---|
| Business Class | 48% | 56% | 60% | **68%** |
| Economy Class | 38% | 28% | 42% | 52% |
| Premium Economy | 38% | 35% | 44% | 40% |

---

## 5. Route-Level Evidence

### Best-performing routes (≥ 5 reviews)

| Route | Reviews | Mean Rating | % > 7 | Mean VFM |
|---|---|---|---|---|
| Singapore–Bangkok | 6 | 8.83 | 83% | 4.67 |
| Manila–Hong Kong | 10 | 8.60 | 80% | 4.30 |
| Hong Kong–Taipei | 8 | 8.00 | 88% | 4.00 |
| Bangkok–Hong Kong | 14 | 7.93 | 71% | 4.14 |
| Hong Kong–Singapore | 13 | 7.23 | 77% | 3.77 |

Common pattern: **regional Asian routes** correlate with higher VFM scores and higher satisfaction.

### Worst-performing routes (≥ 5 reviews)

| Route | Reviews | Mean Rating | % > 7 | Mean VFM |
|---|---|---|---|---|
| Hong Kong–Sydney | 7 | 3.86 | 14% | 2.00 |
| Los Angeles–Hong Kong | 5 | 4.00 | 0% | 3.80 |
| New York–Hong Kong | 8 | 4.88 | 25% | 2.88 |
| HKG–TPE (short) | 5 | 4.60 | 40% | 2.80 |
| Sydney–London via HKG | 7 | 5.00 | 43% | 2.71 |

**Long-haul routes to/from Australia and North America** consistently receive low VFM scores and poor Overall Ratings. These are priority intervention targets.

---

## 6. Decision-Ready Rules & Recommendations

### Primary Rule (high coverage)
> **If VFM ≥ 4 → 82% probability of Overall Rating > 7**  
> Covers 53% of the passenger base.

### Reinforcing Rule (combined sub-ratings)
> **VFM ≥ 4 AND Seat Comfort ≥ 4** → mean rating 8.71, 87% > 7 (N=266)

### Operational Recommendations

| Priority | Action | Rationale |
|---|---|---|
| 🔴 High | **Improve VFM perception on Australia & North America long-haul routes** | Mean VFM 2.0–2.9 on worst routes; 0–14% achieve rating > 7 |
| 🔴 High | **Prioritise VFM improvements in Economy Class** | Largest passenger volume, lowest mean VFM (3.21); high elasticity once VFM ≥ 4 |
| 🟠 Medium | **Increase seat comfort investment on medium/long-haul** | Second-strongest predictor; mean comfort for rating ≤ 7 is 3.42 vs 3.84 for > 7 |
| 🟠 Medium | **Target Couple Leisure segment** | Lowest % > 7 (37%); potentially gap in romantic/leisure product design |
| 🟡 Low | **Maintain Business Class service quality** | Already performing best (59% > 7) but relatively small volume |
| 🟡 Low | **Study high-scoring regional Asian routes** | Singapore–Bangkok and Manila–HKG as service benchmarks (VFM 4.1–4.7) |

---

## 7. Caveats and Limitations

- **Passenger sub-ratings are endogenous to Overall Rating** — the model explains what passengers reward, not direct cost/operational inputs. Management must map VFM to actionable pricing or product levers.
- **Route sample sizes are small** (≤ 16 per route); route-level conclusions carry uncertainty and should be validated with larger data.
- **First Class** has only 16 reviews; results (50% > 7) are not stable.
- **Month-level patterns** (e.g., Dec-15 or Nov-15 showing 100% > 7) reflect very few reviews per period and should not guide scheduling decisions.
- The dataset covers all reviews as a single airline (Cathay Pacific); there is no control group, so competitive benchmarking is not possible from this data alone.

---

## 8. Summary

Value For Money is the overwhelmingly dominant predictor of Overall Rating > 7 (Pearson $r = 0.877$, standardised LR coefficient $= 3.1$). A predictive model (Logistic Regression) achieves ROC-AUC of **0.938** using available sub-ratings and segment features. The strategic priority is to push VFM scores from 3 to ≥ 4 — especially on long-haul Australia/North America routes and in Economy Class — which would materially shift the share of passengers giving Overall Rating > 7 from 17% to ~82%.
