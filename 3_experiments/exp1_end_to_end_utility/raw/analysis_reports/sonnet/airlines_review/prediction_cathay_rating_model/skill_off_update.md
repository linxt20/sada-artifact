---
dataset: airlines_review
scenario: prediction_cathay_rating_model
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating_gt7"
query: "(Cathay MD) Build a model to organise/optimise routes and service so Overall Rating > 7."
source_table: augment_table/airlines_review/prediction_cathay_rating_model/sonnet__skill_off_update.csv
generated_at: 2026-07-28T12:58:43.020500+00:00
wall_seconds: 53.19
---

# Cathay Pacific: Model to Optimise Routes & Service for Overall Rating > 7

## Executive Summary

Of 744 reviews in this dataset, **348 (46.8%)** achieve an Overall Rating > 7 (median = 7, mean = 6.17). A predictive model built on the available features points to **Value For Money** as the dominant lever, with cabin class, route, and traveller type providing actionable segmentation.

---

## 1. Key Driver: Value For Money

Value For Money has by far the strongest correlation with Overall Rating ($r = 0.877$), dwarfing all other service attributes:

| Attribute | Correlation with Overall Rating |
|---|---|
| **Value For Money** | **0.877** |
| Seat Comfort | 0.156 |
| Staff Service | 0.110 |
| Food & Beverages | 0.109 |
| Inflight Entertainment | 0.089 |

The relationship is near-monotonic across score bins:

| VFM Score | Avg Overall Rating |
|---|---|
| 1–2 | 2.4 |
| 3 | 5.3 |
| 4 | 8.0 |
| **5** | **9.1** |

**Implication:** Achieving a VFM score ≥ 4 is essentially sufficient to push Overall Rating above 7. Pricing strategy, fare-vs-product alignment, and clear communication of value are the primary levers.

---

## 2. Cabin Class Segmentation

| Class | Avg Overall Rating | % Reviews > 7 |
|---|---|---|
| First Class | 7.4 | 50.0% |
| **Business Class** | **7.1** | **59.0%** |
| Premium Economy | 6.1 | 38.9% |
| Economy Class | 5.7 | 42.9% |

Business Class already exceeds the target threshold on average. **Premium Economy and Economy are the deficit segments.** Mean VFM scores for these classes (3.15–3.21) sit below the critical score of 4, confirming that perceived value—not hard service quality—is the gap.

---

## 3. Route-Level Priorities

**Top-performing routes (≥ 5 reviews, avg rating ≥ 7.0):**

| Route | Avg Rating | Count |
|---|---|---|
| Singapore → Bangkok | 8.8 | 6 |
| Manila → Hong Kong | 8.6 | 10 |
| HKG → LHR | 8.4 | 5 |
| Hong Kong → Taipei | 8.0 | 8 |
| Bangkok → Hong Kong | 7.9 | 14 |

**Underperforming routes (avg rating < 5.5):**

| Route | Avg Rating | Count |
|---|---|---|
| Hong Kong → Sydney | 3.9 | 7 |
| Los Angeles → Hong Kong | 4.0 | 5 |
| HKG → TPE | 4.6 | 5 |
| New York → Hong Kong | 4.9 | 8 |

Long-haul transpacific and Australia routes consistently underperform. These likely suffer from unfavourable price-to-comfort ratios (Economy seat comfort on ultra-long flights) and elevated customer expectations.

**Hub routes** (hub_route = 1, n = 714) average 6.1 vs. 7.2 for non-hub routes—suggesting that regional/connecting point-to-point routes deliver stronger perceived value.

---

## 4. Priority Action Framework

The augmented `priority_action` column classifies reviews as follows:

| Priority Action | Count | Interpretation |
|---|---|---|
| on_track | 348 | Overall Rating > 7; maintain standards |
| high_impact | 331 | Below threshold; highest fix priority |
| borderline_inconsistent | 39 | Near threshold, unstable |
| borderline_stable | 26 | Near threshold, stable |

Among **high_impact** reviews, the most common weakest attribute is **Value For Money (105)**, followed by Seat Comfort (72), Staff Service (70), and Food & Beverages (65). Among **on_track** reviews, VFM is rarely the weakest attribute (only 10 cases), confirming VFM as the decisive factor.

---

## 5. Traveller Segment Insights

| Traveller Type | Avg Overall Rating | Count |
|---|---|---|
| Solo Leisure | 6.7 | 328 |
| Family Leisure | 6.0 | 128 |
| Business | 5.8 | 129 |
| Couple Leisure | 5.6 | 159 |

Solo Leisure passengers rate highest; Business travellers are notably lower despite higher fares, suggesting expectations are most acute in that segment.

---

## 6. Model Recommendations

### Route Optimisation
- **Deprioritise or restructure** long-haul Economy on Hong Kong → Sydney, Los Angeles, and New York routes; upgrade product or adjust fares to close the value gap.
- **Replicate** the short/medium-haul Asia Pacific model (Manila–HK, Bangkok–HK, Singapore–Bangkok) where ratings consistently exceed 7.

### Service Optimisation
- **Business Class** is performing well (59% > 7); protect staffing and product quality on these routes.
- **Premium Economy** is the biggest opportunity: mean rating 6.1 with VFM ≈ 3.1. Modest improvements to meal quality and seat pitch, or pricing recalibration, could push a large share above the threshold.
- **Economy long-haul**: address Seat Comfort (second most common weakest attribute in high-impact rows) on wide-body ultra-long-haul aircraft.

---

## 7. Caveats & Weak Evidence

- **Correlation ≠ causation**: VFM's dominance may partly reflect that passengers who already feel negative rate all dimensions lower (halo effect).
- **Route sample sizes are small** (many routes have < 10 reviews); route-level conclusions should be validated against larger booking/survey data.
- **Non-hub route advantage** (avg 7.2) is based on only 30 reviews—treat with caution.
- **Temporal shifts**: reviews span multiple years; recent service changes may not be captured uniformly.
