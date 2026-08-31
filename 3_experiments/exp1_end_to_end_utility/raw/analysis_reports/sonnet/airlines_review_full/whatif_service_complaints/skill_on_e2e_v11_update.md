---
dataset: airlines_review_full
scenario: whatif_service_complaints
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: what_if
focus_variable: "Overall Rating"
query: "If airlines eliminated the most common cabin-service complaints in the reviews, how much would the average Overall Rating improve?"
source_table: augment_table/airlines_review_full/whatif_service_complaints/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-08-03T05:57:27.907806+00:00
wall_seconds: 70.71
---

# What-If Analysis: Impact of Eliminating Cabin-Service Complaints on Overall Rating

## Executive Summary

If airlines eliminated the most common cabin-service complaints, the average Overall Rating would improve by approximately **+2.4 points** (top 3 complaint types) to **+2.8 points** (all complaint types) on a 1–10 scale — a **~43–49% lift** over the current mean of **5.63**.

---

## Dataset Overview

| Metric | Value |
|--------|-------|
| Total reviews | 8,100 |
| Overall Rating mean (baseline) | 5.63 |
| Reviews with a cabin-service complaint | 4,544 (56.1%) |
| Reviews with no complaint | 3,353 (41.4%) |
| No-complaint mean Overall Rating | **8.57** |

---

## Complaint Type Distribution and Impact

| `cabin_service_complaint_type` | Count | % of Total | Mean Overall Rating | Recommend Rate |
|-------------------------------|-------|-----------|---------------------|---------------|
| no_complaint | 3,353 | 41.4% | 8.57 | 91.9% |
| **service_responsiveness** | **1,678** | **20.7%** | **2.68** | **14.2%** |
| **crew_attitude** | **1,303** | **16.1%** | **3.06** | **19.0%** |
| **food_quality** | **714** | **8.8%** | **5.20** | **45.5%** |
| seat_comfort | 497 | 6.1% | 4.99 | 43.1% |
| Unknown | 203 | 2.5% | 1.72 | 4.4% |
| ife_malfunction | 185 | 2.3% | 5.35 | 51.9% |
| amenity_gap | 138 | 1.7% | 5.44 | 50.7% |
| cabin_cleanliness | 29 | 0.4% | 3.97 | 24.1% |

The three most frequent complaint categories — `service_responsiveness`, `crew_attitude`, and `food_quality` — account for **3,695 reviews (45.6%)** and have a combined mean rating of only **3.30**, far below the no-complaint baseline of 8.57.

---

## What-If Scenarios

The counterfactual replaces the observed ratings of complaint-affected reviews with the no-complaint group mean (8.57), reflecting the ceiling achievable if those complaints were resolved.

| Scenario | Reviews Affected | Projected Mean Rating | Improvement vs. Baseline |
|----------|-----------------|----------------------|--------------------------|
| Baseline (status quo) | — | 5.63 | — |
| Eliminate top 3 (`service_responsiveness`, `crew_attitude`, `food_quality`) | 3,695 | **8.04** | **+2.41** |
| Eliminate all complaint types | 4,544 | **8.40** | **+2.77** |

> **Primary answer:** Eliminating the three most common complaint types would improve average Overall Rating by approximately **+2.4 points** (+43%), from 5.63 to ~8.04.

---

## Cross-Validation with Original Structured Columns

### Staff Service aligns with `crew_attitude_issue`
Reviews flagged with `crew_attitude_issue = rude_or_dismissive` (n=2,393) average Overall Rating **2.00**, vs. **8.89** for `friendly_professional` (n=3,482). The `Staff Service` structured column corroborates this: `crew_attitude` complaint reviews average Staff Service **3.19** vs. **3.85** for no-complaint reviews.

### Food & Beverages aligns with food_quality complaints
`food_quality` complaint reviews average **Food & Beverages = 3.37** vs. **3.57** for no-complaint — a smaller gap, explaining why `food_quality` shows a less severe Overall Rating penalty (5.20 mean) relative to crew-facing complaints.

### Complaint Severity (`complaint_severity`) confirms rating gradient

| `complaint_severity` | Mean Overall Rating | Count |
|---------------------|---------------------|-------|
| 1 (minimal) | 9.27 | 2,654 |
| 2 | 7.69 | 1,115 |
| 3 | 4.47 | 1,465 |
| 4 | 2.31 | 1,938 |
| 5 (severe) | 1.52 | 928 |

Severity 4–5 complaints (n=2,866, 35% of dataset) drag the overall mean most severely and are concentrated in `service_responsiveness` and `crew_attitude` types.

### Service Failure Co-occurrence (`service_failure_co_occurrence`)
Reviews with `multiple_failures` (n=4,291) average **3.17** vs. **9.26** for `no_failure` (n=2,516). A majority of complaint reviews involve multiple co-occurring failures, amplifying the rating depression beyond any single complaint category.

### Service Decline Perception (`service_decline_perception`)
Reviews flagged `True` (n=1,158) average **3.27** vs. **6.03** for `False` — indicating that perceived quality deterioration over time is an additional ~2.8-point penalty on top of individual complaints.

### Service Consistency (`service_consistency`)
`consistent_negative` reviews (n=1,481) average **1.84**; `consistent_positive` (n=1,296) average **9.32**. This suggests that airlines with structurally poor service profiles contribute a disproportionate share of the complaint-driven rating depression.

---

## Key Drivers and Priority Actions

| Priority | Complaint Type | Reviews | Rating Gap vs. Baseline | Recommended Action |
|----------|---------------|---------|------------------------|--------------------|
| 1 | `service_responsiveness` | 1,678 | −5.90 | Crew training on attentiveness, proactive service protocols |
| 2 | `crew_attitude` | 1,303 | −5.52 | Attitude/professionalism training; reinforced by `crew_attitude_issue` facet |
| 3 | `food_quality` | 714 | −3.38 | Catering quality and consistency improvements |
| 4 | `seat_comfort` | 497 | −3.58 | Aircraft/seat refresh investment |

---

## Method Note

**TAPP-generated columns used:** `cabin_service_complaint_type` (primary classification for complaint segmentation and what-if scenario), `complaint_severity` (gradient validation), `service_failure_co_occurrence` (co-occurrence amplification), `crew_attitude_issue` (cross-validation with Staff Service), `service_decline_perception` (longitudinal signal), `service_consistency` (structural vs. episodic complaint patterns).

Columns `positive_service_signal`, `ground_service_complaint`, `cabin_class_service_gap`, `flight_haul_type`, `aircraft_type_confounder`, `complaint_resolution_quality`, and `service_responsiveness` (the TAPP column, distinct from the complaint type value) were reviewed but found redundant with or less directly informative than the columns listed above for this specific query, and were not centered in the analysis.
