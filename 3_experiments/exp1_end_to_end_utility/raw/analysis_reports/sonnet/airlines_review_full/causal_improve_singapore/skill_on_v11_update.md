---
dataset: airlines_review_full
scenario: causal_improve_singapore
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "overall_rating_recommendation"
query: "How can Singapore Airlines improve its overall rating and recommendation rate, especially on flights where passengers do not recommend it (Recommended = no)?"
source_table: augment_table/airlines_review_full/causal_improve_singapore/sonnet__skill_on_v11_update.csv
generated_at: 2026-08-03T05:48:45.344286+00:00
wall_seconds: 54.0
---

# Singapore Airlines: Improving Overall Rating & Recommendation Rate

**Dataset scope:** 972 Singapore Airlines reviews | 626 recommend (`yes`, 64%) · 346 do not recommend (`no`, 36%)  
**Focus:** Identifying drivers of non-recommendation and actionable levers for improvement.

---

## 1. Headline Numbers

| Metric | Recommended = yes | Recommended = no |
|---|---|---|
| Overall Rating (mean) | 8.63 | 2.76 |
| Seat Comfort | 3.70 | 3.65 |
| Staff Service | 4.02 | 3.80 |
| Food & Beverages | 4.01 | 3.84 |
| Inflight Entertainment | 4.10 | 3.78 |
| **Value For Money** | **4.35** | **1.80** |

The gap in **Value For Money** (4.35 vs 1.80) is by far the largest sub-score difference and correlates most strongly with Overall Rating in the non-recommending cohort ($r = 0.59$). All other sub-scores are comparatively close between groups, making value perception the single most critical lever.

---

## 2. Primary Driver: Value-for-Money Perception

Among non-recommending passengers, **326 of 346 (94%)** carry the label `poor_value_premium_not_justified`. This is near-universal in the no-recommend group compared to only occasional occurrence in the yes-recommend group.

**Cabin class breakdown of non-recommenders:** Economy (231), Business (71), Premium Economy (41), First Class (3). The value problem is strongest in Economy (216/231 = 94% `poor_value_premium_not_justified`), but Business class is also heavily represented, suggesting the issue extends beyond budget travelers.

**Implication:** Pricing strategy, fare transparency, and the perceived ratio of product quality to ticket cost must be addressed across all cabins, not just Economy.

---

## 3. Crew Attitude & Service Proactivity

| cabin_crew_attitude (no-recommend) | Count |
|---|---|
| indifferent | 184 (53%) |
| rude_dismissive | 45 (13%) |
| professional_neutral | 44 (13%) |
| inconsistent | 29 (8%) |
| warm_attentive | 19 (6%) |

| service_proactivity (no-recommend) | Count |
|---|---|
| absent_neglectful | 285 (82%) |
| reactive_on_request | 55 (16%) |
| proactive_attentive | 6 (2%) |

**82%** of non-recommenders experienced absent or neglectful service, and **53%** encountered indifferent crew. This stands in stark contrast to the yes-recommend group. Improving cabin crew training to shift from `absent_neglectful` to `proactive_attentive` is the most operationally direct fix.

---

## 4. Product Gap: Cabin Expectations

**331 of 346 (96%)** non-recommending passengers experienced `below_class_expectations` on the cabin product gap metric, versus `meets_class_expectations` or higher for virtually all recommenders. This reinforces the value-for-money finding: passengers feel the physical product (seat, amenities) does not deliver what the class or price implies.

---

## 5. Disruption Handling & Complaint Resolution

When disruptions did occur among non-recommenders:
- **82 passengers received no support** when disrupted; 23 had compensation denied.
- **122 complaints were unresolved or ignored** (35% of the non-recommend group raised a complaint that went unaddressed).

Poor recovery amplifies dissatisfaction. Passengers who experience a disruption *and* receive no support or have complaints ignored are likely to anchor negative reviews.

---

## 6. IFE & Digital Failures

- 28 non-recommenders cited IFE `hardware_malfunction`, 25 `dated_limited_content`.
- 38 non-recommenders (11%) experienced a `digital_system_failure` vs 30/626 (5%) for recommenders — a meaningful gap.

While IFE issues are not the primary driver, hardware reliability and content freshness are important on long-haul routes.

---

## 7. Route Length & Segment Patterns

Non-recommendation rates and low ratings are **consistent across all flight durations** (short, medium, long haul), meaning the problem is not route-specific. However, long-haul non-recommenders give the lowest mean rating (2.73), suggesting that on extended flights the accumulated effect of service gaps and value dissatisfaction is most damaging.

---

## 8. Ground Service

Among non-recommenders, 100 passengers experienced ground-level issues: check-in problems (32), seat assignment errors (26), connection mismanagement (22), lounge access issues (10), boarding chaos (10). While the majority (246) had `no_issue` on the ground, these failures compound the in-flight experience negatively.

---

## 9. Prioritized Recommendations

| Priority | Action | Evidence |
|---|---|---|
| **1 (Critical)** | Recalibrate pricing or enhance perceived value across all cabin classes | 94% of non-recommenders cite `poor_value_premium_not_justified`; $r=0.59$ with Overall Rating |
| **2 (High)** | Invest in crew proactivity training; target shift from `absent_neglectful` to proactive service | 82% of non-recommenders experienced neglectful service |
| **3 (High)** | Improve complaint handling and disruption recovery processes | 122 unresolved complaints; 82 received no support during disruptions |
| **4 (Medium)** | Refresh IFE hardware and content on aging aircraft | 53 non-recommenders cited IFE malfunction or dated content |
| **5 (Medium)** | Tighten ground operations: check-in, seat assignments, connection management | 100 non-recommenders had pre-flight issues |

---

## 10. Caveats & Weak Evidence

- Sub-score correlations (Seat Comfort, Staff Service, F&B, IFE) with Overall Rating are **weak** ($r < 0.1$) within the non-recommend group, suggesting they are contributing factors but not primary drivers individually.
- The `service_decline_perceived` flag is True for 77/346 (22%) of non-recommenders vs 37/626 (6%) of recommenders — directionally meaningful but the absolute count is modest.
- First Class non-recommenders are only 3 in number; conclusions about that cabin are not reliable.
- The augmented columns (e.g., `cabin_crew_attitude`, `value_for_money_perception`) are model-inferred labels; they corroborate review text patterns but should be validated against raw reviews before operational decisions.
