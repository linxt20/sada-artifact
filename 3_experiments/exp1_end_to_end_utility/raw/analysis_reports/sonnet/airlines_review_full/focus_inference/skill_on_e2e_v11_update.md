---
dataset: airlines_review_full
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's in these airline reviews — I'm not sure which aspect is most worth analyzing."
source_table: augment_table/airlines_review_full/focus_inference/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-08-03T05:53:40.761533+00:00
wall_seconds: 73.57
---

# Airline Reviews Dataset: What Is Most Worth Analyzing?

**Dataset:** 8,100 reviews across 10 airlines | **Query:** Identify the aspect(s) most worth analyzing in these airline reviews.

---

## Method Note

TAPP-generated columns used in this report: `cabin_crew_demeanor`, `food_quality_signal`, `ground_service_quality`, `complaint_resolution_outcome`, `service_failure_severity`, `service_consistency_signal`, `cabin_class_product_mismatch`. All seven columns were informative; `cabin_class_product_mismatch` and `ground_service_quality` are secondary signals. Cross-checks against structured fields (`Overall Rating`, `Staff Service`, `Value For Money`, `Recommended`, `Class`, `Airline`) confirmed TAPP-derived patterns throughout.

---

## 1. The Outcome Variable and Its Dominant Driver

`Overall Rating` (1–10, mean 5.6, σ 3.5) is the clearest outcome to anchor analysis around; 53% of reviewers recommend the airline. The structured sub-scores show a striking asymmetry:

| Structured Dimension | Correlation with Overall Rating |
|---|---|
| **Value For Money** | **0.883** |
| Staff Service | 0.229 |
| Seat Comfort | 0.210 |
| Food & Beverages | 0.160 |
| Inflight Entertainment | 0.140 |

**Value For Money is by far the most important structured driver.** The remaining dimensions are modest contributors, suggesting perceived fairness of the transaction matters far more than any single comfort feature.

---

## 2. Most Analytically Valuable Aspect: Service Quality and Its Failures

The TAPP columns reveal that *how service fails* — and how airlines respond to failure — is the clearest source of rating variance.

### 2a. Service Failure Severity

`service_failure_severity` partitions the dataset into four bands with dramatic rating differences:

| Severity Level | Mean Rating | Recommended Rate | N |
|---|---|---|---|
| no_failure | 9.26 | 99.4% | 2,619 |
| minor_inconvenience | 7.27 | 83.6% | 1,536 |
| moderate_dissatisfaction | 3.42 | 16.9% | 2,105 |
| severe_failure | 1.64 | 2.4% | 1,840 |

2,105 reviews (26%) sit in "moderate" and 1,840 (23%) in "severe" — together nearly half the dataset. This is the highest-leverage analytical lens.

### 2b. Complaint Resolution Amplifies Failure Effects

Among the 2,322 reviews that raised a complaint, how the airline responded created a 7-point rating spread:

| Outcome | Mean Rating | N |
|---|---|---|
| resolved_satisfactorily | 9.12 | 249 |
| partially_resolved | 4.10 | 242 |
| promised_not_delivered | 2.26 | 118 |
| denied_or_ignored | 1.86 | 1,913 |

1,913 complaints (83% of all raised complaints) were **denied or ignored** — a red-flag finding. Resolution quality is the most underexplored lever for improving ratings.

---

## 3. The Second Most Important Dimension: Crew Demeanor

`cabin_crew_demeanor` produces the widest single-variable spread and aligns tightly with the structured `Staff Service` field, confirming it as a real signal rather than labeling noise:

| Demeanor | Mean Overall Rating | Mean Staff Service | N |
|---|---|---|---|
| warm_proactive | 8.93 | 3.94 | 3,250 |
| professional_neutral | 6.25 | 3.78 | 1,231 |
| robotic_or_distant | 4.13 | 3.37 | 549 |
| rude_dismissive | 2.19 | 3.20 | 2,270 |

2,270 reviews (28%) describe crew as `rude_dismissive`, yielding a mean rating of 2.2. Crew behavior is both high-frequency and high-impact, making it a priority dimension.

---

## 4. Airline-Level Fault Lines

The five largest airlines (covering 85% of reviews) show very different failure profiles:

| Airline | Mean Rating | Severe Failure Rate | Complaint Denied Rate | Service Declining Rate |
|---|---|---|---|---|
| Qatar Airways | 7.20 | 8.3% | 10.1% | 25.3% |
| Singapore Airlines | 6.54 | 12.0% | 9.9% | 23.5% |
| Emirates | 4.67 | 25.3% | 33.1% | **33.4%** |
| Air France | 4.64 | 30.3% | 29.8% | 3.9% |
| Turkish Airlines | 3.68 | **50.1%** | **45.6%** | 6.9% |

Turkish Airlines has a severe failure rate of 50% and denies 46% of complaints — a structural service quality problem, not merely a perception gap. Emirates' high `service_consistency_signal = declining_vs_past` rate (33%) points to a deterioration story worth investigating over time.

---

## 5. Supporting Dimensions: Food, Ground Service, and Class Mismatch

**Food quality** (`food_quality_signal`) spans 4,435 reviews with scorable signals. Excellent food correlates with a rating of 9.1; poor food/variety drops to 4.0. However, food quality is already partially captured by the `Food & Beverages` structured column (r = 0.16 with Overall Rating), making it a secondary dimension.

**Ground service** (`ground_service_quality`): 2,328 reviews describe ground staff as `rude_or_unhelpful`, yielding mean ratings of 2.0 — comparable to inflight failures. Ground experience is underrepresented in the structured columns (no dedicated field) and warrants dedicated analysis.

**Cabin class product mismatch** (`cabin_class_product_mismatch`): 496 reviews (6%) show a mismatch, concentrated in Business (15.9%) and Premium Economy (18.9%), lowering mean ratings by 1.7 points (4.0 vs 5.7). This is a niche but actionable finding for premium product managers.

---

## 6. Traveller Segment Context

| Traveller Type | Mean Rating | N |
|---|---|---|
| Solo Leisure | 6.07 | 3,237 |
| Couple Leisure | 5.48 | 1,899 |
| Business | 5.38 | 1,413 |
| Family Leisure | 5.14 | 1,551 |

Business travellers rate lower than solo leisure despite flying in premium cabins more often — consistent with higher expectations and lower tolerance for service failures.

---

## Recommendations: Priority Order for Analysis

1. **Service failure severity + complaint resolution** — covers ~50% of reviews and drives the largest rating swings. Focus: why 83% of complaints go unresolved.
2. **Crew demeanor** — 28% of reviews flag rude/dismissive behavior; cross-correlates with Staff Service and Overall Rating. Focus: airline-level crew culture differences.
3. **Airline-level comparison** — Turkish Airlines and Emirates represent structural vs. reputational decline; Qatar and Singapore set the benchmark. TAPP's `service_consistency_signal` adds temporal nuance unavailable from structured columns alone.
4. **Ground service quality** — no structured column exists; TAPP fills a genuine gap here. Worth a dedicated sub-analysis.
5. **Value For Money** — dominant statistical driver but likely reflects overall satisfaction rather than being independently actionable; useful as an index variable.
