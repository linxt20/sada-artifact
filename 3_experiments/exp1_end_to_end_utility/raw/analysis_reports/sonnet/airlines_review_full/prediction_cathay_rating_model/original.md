---
dataset: airlines_review_full
scenario: prediction_cathay_rating_model
variant: original
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating_gt7"
query: "(Cathay MD) Build a model to organise/optimise routes and service so Overall Rating > 7."
source_table: augment_table/airlines_review_full/prediction_cathay_rating_model/original.csv
generated_at: 2026-08-03T05:42:48.696630+00:00
wall_seconds: 75.76
---

# Cathay Pacific: Model to Achieve Overall Rating > 7
**Dataset:** 744 verified/unverified reviews | Rating scale: 1–10 | Target: Overall Rating > 7

---

## 1. Current Baseline

| Metric | Value |
|--------|-------|
| Mean Overall Rating | 6.17 |
| Median Overall Rating | 7.0 |
| % Reviews with Rating > 7 | ~47% |

The median sits exactly at the threshold, meaning roughly half of reviews already meet the target — but consistent delivery above 7 requires structural improvements.

---

## 2. Key Driver: Value For Money (VFM) Dominates

Correlation of sub-scores with Overall Rating:

| Feature | Correlation with Overall Rating | LR Coefficient |
|---|---|---|
| **Value For Money** | **0.877** | **2.17** |
| Seat Comfort | 0.156 | 0.22 |
| Food & Beverages | 0.109 | 0.08 |
| Staff Service | 0.110 | 0.07 |
| Inflight Entertainment | 0.089 | 0.05 |

**Value For Money is by far the strongest predictor.** The effect is near-binary:

| VFM Score | % Reviews with Rating > 7 |
|---|---|
| Low (1–2) | 0% |
| Mid (3–4) | 49% |
| High (5) | **93%** |

> **Primary lever:** Any intervention that lifts perceived value — pricing, bundled amenities, upgrade policies, or loyalty perks — has the highest probability of pushing Overall Rating above 7.

---

## 3. Cabin Class Analysis

| Class | Mean Rating | % Rating > 7 | Mean VFM |
|---|---|---|---|
| First Class | 7.38 | 50% | 3.62 |
| **Business Class** | **7.09** | **59%** | **3.66** |
| Premium Economy | 6.09 | 39% | 3.15 |
| Economy Class | 5.73 | 43% | 3.21 |

**Business Class is the only cabin consistently above the 7.0 target.** Premium Economy underperforms its price positioning (VFM = 3.15, rating = 6.09). Economy's low VFM score (3.21) is the main drag on network-wide averages.

**Recommendation:** Focus Premium Economy differentiation — the cabin is neither economy nor business in perception. Improve seat comfort and food offering to justify the price premium and close the VFM gap.

---

## 4. Route Performance

### High-performing routes (≥5 reviews, mean rating ≥ 7.0)

| Route | Mean Rating | % > 7 | n |
|---|---|---|---|
| Singapore → Bangkok | 8.83 | 83% | 6 |
| Manila → Hong Kong | 8.60 | 80% | 10 |
| HKG → LHR | 8.40 | 60% | 5 |
| Hong Kong → Taipei | 8.00 | 88% | 8 |
| Bangkok → Hong Kong | 7.93 | 71% | 14 |
| Hong Kong → San Francisco | 7.80 | 80% | 5 |
| Hong Kong → Singapore | 7.23 | 77% | 13 |

### Low-performing routes (mean rating < 5.5)

| Route | Mean Rating | % > 7 | n |
|---|---|---|---|
| Hong Kong → Sydney | 3.86 | 14% | 7 |
| Los Angeles → Hong Kong | 4.00 | 0% | 5 |
| New York → Hong Kong | 4.88 | 25% | 8 |
| Sydney → London via HKG | 5.00 | 43% | 7 |
| Hong Kong → Manila | 5.14 | 29% | 7 |

**Insight:** Short-to-medium haul intra-Asia routes (Manila–HKG, BKK–HKG, HKG–Taipei, SIN–BKK) consistently outperform. Long-haul trans-Pacific and Kangaroo routes (LAX, SYD, NYC) are significantly below target. These routes likely face heightened value-for-money scrutiny due to higher ticket prices, longer flight times, and competitive alternatives.

**Route optimisation recommendation:**
- **Invest service resources in long-haul routes** (improved catering, crew ratios, lounges) to close the perceived value gap.
- **Use intra-Asia routes as service benchmarks** — identify operational practices from BKK and MNL routes and replicate on underperformers.

---

## 5. Traveller Type

| Traveller Type | Mean Rating | % > 7 |
|---|---|---|
| Solo Leisure | 6.68 | 54% |
| Family Leisure | 5.97 | 45% |
| Business | 5.83 | 43% |
| Couple Leisure | 5.56 | 37% |

Solo leisure travellers rate highest; business travellers rate relatively low despite flying in premium cabins. This signals a **service expectation gap for corporate travellers** — reliability, punctuality, and ground experience (lounge, connections) matter more for this segment and are likely dragging scores down.

---

## 6. Temporal Trend (Caution)

| Year | Mean Rating | n |
|---|---|---|
| 2016 | 7.15 | 98 |
| 2017 | 7.31 | 170 |
| 2018 | 6.72 | 169 |
| 2019 | 5.13 | 166 |
| 2020–2022 | 1–3.7 | 60 |
| 2023–2024 | 5.7 | 81 |

Pre-pandemic ratings routinely exceeded 7. The sharp decline in 2019 pre-dates COVID, suggesting **service quality degradation began before the pandemic**. The 2023–24 recovery to ~5.7 shows partial recovery, but has not yet returned to 2016–17 levels. This provides evidence that Cathay has historically operated above the 7.0 threshold and can do so again.

---

## 7. Predictive Model Summary

A logistic regression on the five sub-scores achieves a straightforward decision rule:

$$P(\text{Rating} > 7) \approx \sigma\left(2.17 \cdot \text{VFM} + 0.22 \cdot \text{Comfort} + 0.08 \cdot \text{Food} + 0.07 \cdot \text{Staff} + 0.05 \cdot \text{IFE} - \beta_0\right)$$

The dominant term is VFM. **Increasing average VFM score from 3.2 → 4.0 across Economy and Premium Economy would be the single highest-leverage operational change.**

---

## 8. Actionable Recommendations

| Priority | Action | Target Segment | Expected Impact |
|---|---|---|---|
| 🔴 High | Reprice or rebundle Premium Economy to improve VFM perception | Premium Economy | Lift VFM 3.15 → 4.0+ |
| 🔴 High | Redesign Economy long-haul value proposition (catering, seat pitch, IFE) on SYD, LAX, NYC routes | Economy long-haul | Lift low-performing routes toward 7.0 |
| 🟠 Medium | Identify operational practices on intra-Asia routes and apply to long-haul | All classes | Benchmark replication |
| 🟠 Medium | Improve ground experience and punctuality for business travellers | Business travellers | Close expectation gap |
| 🟡 Low | Standardise IFE availability across aircraft types | All routes | Minor uplift |

---

## 9. Caveats

- Route-level sample sizes are small (5–16 reviews); route conclusions should be treated as directional, not statistically conclusive.
- VFM is highly correlated with Overall Rating but may partially reflect post-hoc rationalisation of the overall experience rather than an independent driver.
- First Class has only 16 reviews — results are not reliable for that cabin.
- 2020–2022 data is severely disrupted by pandemic operations and should not anchor service targets.
