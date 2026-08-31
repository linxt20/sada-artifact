---
dataset: airlines_review_full
scenario: focus_inference
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's in these airline reviews — I'm not sure which aspect is most worth analyzing."
source_table: augment_table/airlines_review_full/focus_inference/haiku__skill_off_update.csv
generated_at: 2026-08-03T05:42:51.764681+00:00
wall_seconds: 87.19
---

# Airline Reviews Analysis: Focus on Key Aspects Worth Analyzing

## Executive Summary

This dataset contains 8,100 airline reviews spanning multiple cabin classes, traveller types, and geographic routes. To help you prioritize analytical efforts, this report identifies **which aspects are most driving satisfaction divergence** and where the data reveals the most actionable patterns.

---

## Dataset Overview

| Metric | Value |
|--------|-------|
| **Total Reviews** | 8,100 |
| **Overall Rating Range** | 1–10 |
| **Mean Overall Rating** | 5.63 |
| **Median Overall Rating** | 6.0 |
| **Recommended (Yes)** | 4,287 (52.9%) |
| **Recommended (No)** | 3,813 (47.1%) |

---

## Primary Finding: **Primary Complaint Type is the Dominant Predictor**

The most important insight for your analysis is that **primary complaint category strongly predicts overall satisfaction**, with near-total separation:

### Ratings by Primary Complaint

| Complaint Type | # Reviews | Mean Rating | Recommendation Rate | Median |
|---|---|---|---|---|
| **none** | 5,191 (64.1%) | **7.90** | 75.4% | 9 |
| **service** | 1,350 (16.7%) | **1.57** | 0.0% | 1 |
| **seat** | 628 (7.8%) | **1.75** | 0.0% | 2 |
| **operations** | 371 (4.6%) | **1.39** | 0.0% | 1 |
| **value** | 286 (3.5%) | **1.27** | 0.0% | 1 |
| **food** | 223 (2.8%) | **1.91** | 0.0% | 2 |
| **entertainment** | 51 (0.6%) | **1.49** | 0.0% | 1 |

**Key observation:** When a review has a primary complaint (i.e., a notable problem), the overall rating collapses to the 1–2 range and the recommendation rate drops to zero. When no major complaint is identified, ratings average 7.9/10.

---

## Secondary Finding: Rating Consistency Flags Conflicting Narratives

**72.1% of reviews are flagged as "inconsistent"** – meaning the numeric aspect ratings don't align with the overall rating or review tone. This inconsistency is NOT random:

### How Inconsistency Correlates with Content

| Consistency | Count | Mean Rating | Pattern |
|---|---|---|---|
| **Inconsistent** | 5,838 | 6.84 | Mixed or nuanced experiences; high aspect variance (65%) |
| **Consistent** | 2,262 | 2.51 | Problem-dominated reviews; complainants rate low across the board |

**Insight:** 
- **Inconsistent reviews** (72% of data) typically describe complex experiences: e.g., "excellent crew, but terrible seat" or "great amenities, poor delays." These merit detailed aspect-by-aspect breakdown.
- **Consistent reviews** (28%) are simpler: either very satisfied or very dissatisfied across all metrics.

---

## Aspect-Level Performance Metrics

When reviewers rate individual dimensions, all show **moderate performance** (mean ~3.4–3.6 / 10):

| Aspect | Mean | Median | Stdev |
|---|---|---|---|
| **Inflight Entertainment** | 3.64 | 4 | 1.31 |
| **Staff Service** | 3.57 | 4 | 1.53 |
| **Seat Comfort** | 3.41 | 4 | 1.40 |
| **Food & Beverages** | 3.38 | 4 | 1.46 |
| **Value For Money** | 3.15 | 3 | 1.59 (highest variance) |

**Finding:** Value for money is the weakest and most variable dimension, suggesting pricing sensitivity and perception mismatch across segments.

---

## Cabin Class Reveals Satisfaction Hierarchy

The dataset shows a clear quality/satisfaction gradient by cabin type:

| Class | Count | Mean Rating | % "None" Complaint | Implication |
|---|---|---|---|---|
| **First Class** | 121 | 7.60 | 86.0% | Consistently excellent; little to analyze |
| **Business Class** | 2,104 | 6.65 | 77.9% | Baseline satisfaction; complaints ~13% |
| **Premium Economy** | 371 | 5.97 | 72.2% | Borderline; seat complaints spike (11.6%) |
| **Economy Class** | 5,504 | 5.18 | 57.8% | Lowest satisfaction; 42% have complaints |

**Recommendation:** Economy class is where divergence is largest and where complaints cluster most densely. Premium economy shows emerging seat comfort issues.

---

## Where to Focus Your Analysis

### 🎯 **Highest Priority: Service Complaints (16.7% of reviews)**

- 1,350 reviews explicitly cite service issues
- Mean rating: 1.57 (effectively negative)
- Service spans: cabin crew attentiveness, ground staff, customer service responsiveness
- **Action:** Segment by traveller type and route to identify which service failures (e.g., rude crew vs. slow service vs. no acknowledgement) are most damaging

### 🎯 **High Priority: Seat Comfort (7.8% of reviews + high variance)**

- 628 primary-complaint reviews on seats
- Affects Premium Economy disproportionately (11.6% of complaints)
- Complaints span: width, padding, recline, legroom configurations
- **Action:** Compare Economy vs. Business vs. Premium Economy seat ratings; identify specific aircraft models or routes

### 🎯 **High Priority: Operational Disruptions (4.6% of reviews)**

- 371 reviews on delays, cancellations, gate changes, missed connections
- Mean rating: 1.39 (the lowest among complaint types)
- **Action:** Correlate with route, month flown, and recovery quality (customer service response)

### 🎯 **Moderate Priority: Value For Money (3.5% of reviews + highest variance)**

- 286 explicit value complaints
- Most variable aspect rating (stdev 1.59)
- Suggests pricing/expectations mismatch
- **Action:** Segment by cabin class and route; compare price-to-rating alignment

### 🎯 **Lower Priority: Food & Entertainment**

- Combined < 4% of reviews as primary complaint
- Food (223) and entertainment (51) are niche issues
- **Note:** Food often co-occurs with other complaints; may be secondary

---

## Data Quality Notes

- **High coverage:** All 8,100 rows have ratings and recommendations
- **Rating consistency flag reliability:** 72% inconsistency rate suggests this is a meaningful signal (not random annotation error)
- **Aspect variance:** 65% of reviews show high variance, supporting the mixed-experience hypothesis
- **Sentiment alignment:** 96.9% of reviews have aligned tone-to-rating (only 3% tone-mismatch outliers), suggesting data integrity

---

## Conclusion & Recommended Focus Path

**For maximum insight density, prioritize:**

1. **Service quality** — The dominant complaint (1,350 reviews, clear signal)
2. **Seat comfort** — Segment by cabin class; emerging Premium Economy issue
3. **Operational reliability** — Lowest-rated sub-segment; recovery mechanisms unclear
4. **Value perception** — Most variable; pricing strategy impact evident

**Secondary analysis:** Use the 72% "inconsistent" reviews to identify nuanced trade-offs (e.g., "will tolerate poor seats if crew is excellent").

The 64% "no complaint" baseline (rating 7.9/10) represents your satisfied customer profile. Compare their profiles (routes, travel types, classes) to identify what drives success.
