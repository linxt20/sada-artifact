---
dataset: airlines_review_full
scenario: causal_improve_singapore
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "overall_rating_recommendation"
query: "How can Singapore Airlines improve its overall rating and recommendation rate, especially on flights where passengers do not recommend it (Recommended = no)?"
source_table: augment_table/airlines_review_full/causal_improve_singapore/sonnet__skill_off_update.csv
generated_at: 2026-08-03T05:38:47.867100+00:00
wall_seconds: 52.1
---

# Singapore Airlines: Improving Overall Rating & Recommendation Rate

**Dataset:** 8,100 verified reviews | **Not Recommended:** 3,813 (47.1%) | **Recommended:** 4,287 (52.9%)

---

## 1. The Core Gap

| Metric | Recommended = yes | Recommended = no |
|---|---|---|
| Overall Rating (mean) | 8.53 | 2.37 |
| Value For Money | 4.39 | **1.75** |
| Staff Service | 3.87 | 3.23 |
| Seat Comfort | 3.67 | 3.13 |
| Food & Beverages | 3.59 | 3.16 |
| Inflight Entertainment | 3.78 | 3.48 |

The gap is largest for **Value For Money** (−2.64 points), far exceeding any other sub-rating. The `class_adjusted_vfm` score confirms this: non-recommenders average **−1.35** vs. **+1.21** for recommenders — a structural, not incidental, deficit.

---

## 2. Primary Driver: Value For Money

Among non-recommending passengers:

- **Value For Money is the #1 weakest dimension** in 30.4% of reviews and the #1 improvement priority in 31.1%.
- Correlation of sub-ratings with Overall Rating (non-recommenders): **Value For Money = 0.59** — roughly 4–5× stronger than any other dimension (Seat Comfort: 0.12, Staff Service: 0.13, etc.).
- **76.1% of non-recommenders fall in the `poor_value` experience segment**, meaning perceived price-to-quality mismatch is the dominant failure mode.

**Implication:** Pricing strategy, ancillary fees, and the perception of what is included at each fare class are the primary levers for improving the recommendation rate.

---

## 3. Secondary Drivers: Seating & Staff Service

Among non-recommending passengers, the `top_complaint_category` distribution is:

| Complaint Category | Share |
|---|---|
| Seating Comfort | 43.2% |
| Staff Service | 39.3% |
| Punctuality | 7.5% |
| Food Quality | 3.4% |
| General Experience | 3.1% |

Despite not being the strongest correlate with Overall Rating in regression terms, **seating discomfort and staff inconsistency together account for ~82% of top complaints** among non-recommenders. These are frequent friction points even when passengers accept the overall experience.

The weakest dimension breakdown reinforces this: Seat Comfort (25.4%) and Staff Service (22.2%) are the 2nd and 3rd most-cited weakest dimensions behind Value For Money.

---

## 4. Economy Class Is the Focal Problem

- **76.5% of non-recommending reviews come from Economy Class passengers**, versus 18.5% from Business Class.
- Economy passengers have the lowest `class_adjusted_vfm` scores (median ≈ −1.99), suggesting they consistently feel they are not getting value proportional to their fare.
- Business Class passengers who do not recommend (18.5%) likely have different pain points — service execution and seat quality matter more at that fare level.

---

## 5. Concrete Improvement Priorities

### Priority 1 — Value For Money (Economy & Business)
- Review Economy fare bundling: passengers appear to penalize add-on fees, sparse inclusions, or pricing relative to competitors.
- Consider transparent fare-class comparisons or enhanced base inclusions (e.g., checked baggage, meal choice) to shift VFM perception.

### Priority 2 — Seat Comfort (Economy Class)
- Seat comfort is the top complaint category overall (43.2%). Cabin retrofits or clearer seat-selection guidance (e.g., exit rows, extra-legroom seats) on older aircraft would address recurring reviews about narrow pitch and poor padding.

### Priority 3 — Staff Service Consistency
- Staff Service scores drop from 3.87 (recommended) to 3.23 (not recommended). While Singapore Airlines has a strong service reputation, the 39.3% share of staff-related complaints among non-recommenders suggests inconsistency across routes or crew rotations.
- Targeted coaching on interactions flagged in reviews (attentiveness, responsiveness to requests) could close this gap.

### Priority 4 — Punctuality (Operational)
- Punctuality complaints account for 7.5% of top complaints among non-recommenders — notable but secondary. Operational reliability improvements (or better communication of delays) would have a modest but real impact.

---

## 6. Caveats & Weak Evidence

- **Inflight Entertainment** shows the smallest gaps and lowest complaint share; investment here is unlikely to move the recommendation rate materially.
- The correlation between sub-ratings and Overall Rating is moderate even for Value For Money (r = 0.59), suggesting that some non-recommenders are influenced by factors not fully captured in the five sub-rating dimensions (e.g., ground experience, booking process — represented in <2% of top complaints, possibly undercounted).
- Traveller type distribution among non-recommenders (Solo Leisure 34.5%, Couple 25.3%, Family 21.7%, Business 18.5%) is fairly uniform, meaning improvements should target the product broadly rather than a single segment.

---

## Summary

To improve Singapore Airlines' overall rating and recommendation rate, the clearest causal pathway is: **fix the Value For Money perception in Economy Class** (primary driver, 76% of non-recommenders are `poor_value`), then **address seating comfort** (top complaint category at 43%), then **raise staff service consistency** (39% of complaints). Inflight entertainment is a weak lever and should not be the focus of remediation investment.
