---
dataset: airlines_review_full
scenario: causal_improve_singapore
variant: original
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "overall_rating_recommendation"
query: "How can Singapore Airlines improve its overall rating and recommendation rate, especially on flights where passengers do not recommend it (Recommended = no)?"
source_table: augment_table/airlines_review_full/causal_improve_singapore/original.csv
generated_at: 2026-08-03T05:38:47.914599+00:00
wall_seconds: 52.15
---

# Singapore Airlines: How to Improve Overall Rating and Recommendation Rate

## Dataset Overview
- **Total Singapore Airlines reviews:** 972
- **Recommended:** 626 (64.4%) | **Not recommended:** 346 (35.6%)
- **Mean Overall Rating:** 6.54 / 10 (recommended: 8.63; not recommended: 2.76)

---

## 1. Primary Driver: Value For Money (VFM) is the Dominant Lever

The correlation analysis reveals a stark finding:

| Sub-rating | Correlation with Overall Rating |
|---|---|
| **Value For Money** | **0.889** |
| Food & Beverages | 0.085 |
| Staff Service | 0.069 |
| Seat Comfort | 0.012 |
| Inflight Entertainment | −0.043 |

VFM accounts for nearly all the variance in Overall Rating. Among non-recommenders:
- **74.3%** gave VFM a score of ≤ 2/5 (vs. near-zero for recommenders)
- Mean VFM for "no" group: **1.80** vs. **4.35** for "yes" group — a gap of **2.55 points**, far larger than any other dimension

**Implication:** Passengers who do not recommend Singapore Airlines almost universally feel they did not receive fair value. Pricing strategy, fare transparency, and fare-to-product alignment are the highest-priority areas for improvement.

---

## 2. Secondary Drivers: Staff Service and Food & Beverages

Among non-recommenders, the next-largest gaps versus recommenders are:

| Dimension | Not Recommended (mean) | Recommended (mean) | Gap |
|---|---|---|---|
| Value For Money | 1.80 | 4.35 | **2.55** |
| Food & Beverages | 3.40 | 3.63 | 0.23 |
| Staff Service | 3.80 | 4.02 | 0.22 |
| Seat Comfort | 3.65 | 3.70 | 0.05 |
| Inflight Entertainment | 3.93 | 3.86 | −0.06 |

- **30.1%** of non-recommenders rated Food & Beverages ≤ 2/5
- **21.1%** rated Staff Service ≤ 2/5

While the absolute gaps are modest, Food & Beverages and Staff Service are tangible service quality factors that compound the dissatisfaction of passengers already feeling undervalued.

---

## 3. Cabin Class: Premium Economy is the Weakest Segment

| Class | Recommendation Rate |
|---|---|
| First Class | 81.2% |
| Business Class | 71.9% |
| Economy Class | 62.0% |
| **Premium Economy** | **56.8%** |

Premium Economy has the lowest recommendation rate despite being a higher-price tier than Economy. This suggests the product does not sufficiently differentiate from Economy, making passengers feel the premium is not justified — a direct VFM problem.

Economy class mirrors the overall pattern: VFM mean of 1.75 for non-recommenders vs. 4.42 for recommenders.

---

## 4. Route Patterns

Non-recommendation is concentrated on **long-haul routes** (London, Sydney, Melbourne, Frankfurt, Los Angeles). These are routes where:
- Ticket prices are higher, raising VFM expectations
- Seat comfort during long flights becomes more impactful
- Competitor premium products (e.g., Qatar Airways, Emirates) offer direct comparison

This reinforces that VFM perception is especially acute on long-haul premium-priced routes.

---

## 5. Traveller Type

| Type | Not Rec | Yes Rec | Not-Rec Rate |
|---|---|---|---|
| Solo Leisure | 107 | 251 | 29.9% |
| Business | 62 | 93 | 40.0% |
| Couple Leisure | 108 | 156 | 40.9% |
| Family Leisure | 69 | 126 | 35.4% |

Business travellers have a notably high non-recommendation rate (40%), suggesting that price-sensitive corporate travelers find the VFM unacceptable relative to competing carriers.

---

## 6. Actionable Recommendations

| Priority | Action | Evidence |
|---|---|---|
| **Critical** | Improve perceived Value For Money (pricing, bundles, loyalty benefits) | VFM correlation = 0.889; 74.3% of non-recommenders rated it ≤2 |
| **High** | Redesign Premium Economy product to justify the price premium | Lowest recommendation rate at 56.8% |
| **Medium** | Improve food quality and consistency, especially on long-haul economy | 30.1% of non-recommenders rated F&B ≤2 |
| **Medium** | Enhance staff service training, especially on high-volume Economy long-haul routes | 21.1% of non-recommenders rated Staff Service ≤2 |
| **Lower** | Seat comfort and IFE are not differentiating factors in non-recommendation | Near-zero gap vs. recommenders |

---

## Caveats and Weak Evidence

- Sub-rating correlations (other than VFM) with Overall Rating are very weak (≤0.09), suggesting passengers may rate sub-dimensions independently without rolling them into their overall score.
- The route-level analysis has small sample sizes per route; route-specific conclusions should be treated as directional.
- One non-recommender gave an Overall Rating of 10 — a data inconsistency that highlights occasional rating noise.
- Inflight Entertainment shows a slightly *negative* gap (non-recommenders rate it marginally higher), suggesting it is not a pain point at all.
