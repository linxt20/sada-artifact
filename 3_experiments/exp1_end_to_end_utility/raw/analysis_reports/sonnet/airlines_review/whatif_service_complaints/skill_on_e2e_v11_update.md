---
dataset: airlines_review
scenario: whatif_service_complaints
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: what_if
focus_variable: "Overall Rating"
query: "If airlines eliminated the most common cabin-service complaints in the reviews, how much would the average Overall Rating improve?"
source_table: augment_table/airlines_review/whatif_service_complaints/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:05:51.602692+00:00
wall_seconds: 61.29
---

# What-If Analysis: Impact of Eliminating Common Cabin-Service Complaints on Overall Rating

**Query:** If airlines eliminated the most common cabin-service complaints in the reviews, how much would the average Overall Rating improve?

---

## Key Finding

Eliminating the two most common cabin-service complaint types (`crew_attentiveness` and `food_quality`) would raise the average Overall Rating by approximately **+1.2 points** (from 6.53 → 7.76). Eliminating all identifiable cabin-service complaint categories would yield a **+1.8-point improvement** (6.53 → 8.35), approaching the no-complaint mean of **9.23**.

---

## Dataset Overview

| Metric | Value |
|---|---|
| Total reviews | 900 |
| Baseline mean Overall Rating | 6.53 |
| Reviews with no cabin-service complaint | 395 (43.9%) |
| Reviews with an identified complaint type | 390 (43.3%) |
| Reviews with Unknown classification | 115 (12.8%) |

---

## Complaint Type Distribution and Ratings

The `cabin_service_complaint_type` TAPP column classifies each review into one of eight complaint categories or `no_complaint`.

| Complaint Type | Count | Share of Total | Mean Overall Rating |
|---|---|---|---|
| no_complaint | 395 | 43.9% | **9.23** |
| crew_attentiveness | 127 | 14.1% | 4.54 |
| food_quality | 126 | 14.0% | 5.19 |
| seat_comfort | 77 | 8.6% | 5.05 |
| ife_failure | 34 | 3.8% | 6.29 |
| amenity_omission | 14 | 1.6% | 5.43 |
| beverage_omission | 7 | 0.8% | 4.86 |
| cleanliness | 5 | 0.6% | 4.00 |
| Unknown | 115 | 12.8% | 2.36 |

**`crew_attentiveness` and `food_quality` are the two most common complaint categories, each affecting ~14% of reviews and depressing ratings to the 4.5–5.2 range—roughly 4 points below the no-complaint baseline.**

---

## What-If Scenarios

The simulation replaces complaint-bearing reviews' ratings with the `no_complaint` mean (9.23), representing full resolution of each complaint type.

| Scenario | Complaints Resolved | Reviews Affected | Simulated Mean | Improvement vs. Baseline |
|---|---|---|---|---|
| Baseline | — | — | 6.53 | — |
| Fix top 2 | `crew_attentiveness` + `food_quality` | 253 (28.1%) | **7.76** | **+1.23** |
| Fix all named | All 7 identified types | 390 (43.3%) | **8.35** | **+1.82** |

---

## Cross-Validation with Original Structured Columns

### By Cabin Class

Complaint presence (any named type) uniformly suppresses ratings across all classes, confirming the complaint effect is not class-specific:

| Class | No-Complaint Mean | Complaint Mean | Gap |
|---|---|---|---|
| Business Class | 8.49 | 5.33 | −3.16 |
| Economy Class | 7.34 | 4.98 | −2.35 |
| First Class | 8.17 | 6.50 | −1.67 |
| Premium Economy | 7.68 | 4.62 | −3.06 |

### TAPP Supporting Facets

The `crew_proactivity` column strongly aligns with `crew_attentiveness` findings: reviews flagged `proactive` average **9.16** (n=442) vs. `reactive` at **4.47** (n=347) and `absent` at **2.44** (n=110), a 6.7-point spread that independently validates the crew-attentiveness complaint signal.

The `service_consistency_issue` column shows `consistently_good` reviews averaging **9.47** (n=297) vs. `consistently_poor` at **2.25** (n=199), reinforcing that complaint elimination would require sustained (not one-off) service improvements to realize the full projected gains.

The `cabin_class_service_gap` and `post_covid_service_decline_flag` columns had moderate coverage and were correlated with existing structured fields (Class, date); they did not add independent predictive signal beyond what `cabin_service_complaint_type` and original ratings already capture.

---

## Method Note

**TAPP-generated columns used:** `cabin_service_complaint_type` (primary), `crew_proactivity`, `service_consistency_issue`. Columns `cabin_class_service_gap`, `post_covid_service_decline_flag`, and `route_type` were examined but found to be either redundant with original structured columns or insufficiently discriminating for the what-if query.

---

## Summary

| Action | Expected Rating Gain |
|---|---|
| Eliminate crew attentiveness complaints (n=127) | ~+0.6 pts |
| Eliminate food quality complaints (n=126) | ~+0.6 pts |
| **Eliminate both top complaint types** | **~+1.2 pts** |
| Eliminate all identified complaint types | ~+1.8 pts |

The biggest lever is crew attentiveness: it is the single most common complaint and has the largest rating penalty (mean 4.54, vs. 9.23 for no-complaint reviews). Food quality is equally prevalent and offers a comparable gain. Together, fixing these two issues could lift average ratings from **6.5 to ~7.8**, moving the airline from below-average to solidly positive territory.
