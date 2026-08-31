---
dataset: airlines_review_full
scenario: causal_qatar_business
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "non_recommendation_outcome"
query: "Explain why some Qatar Airways Business-Class flights receive a non-recommended (Recommended = no) result."
source_table: augment_table/airlines_review_full/causal_qatar_business/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-08-03T05:49:43.835158+00:00
wall_seconds: 58.49
---

# Why Some Qatar Airways Business-Class Flights Receive a Non-Recommended Result

## Dataset Overview

All 592 reviews in the augmented table are Qatar Airways Business-Class records. Of these, **127 (21.5%)** carry `Recommended = no` and **465 (78.5%)** carry `Recommended = yes`.

**TAPP-generated columns used in this report:**
- `inflight_service_quality`
- `service_consistency_across_sectors`
- `seat_product_received`

---

## 1. Primary Driver: Value For Money Perception

The single strongest structured predictor of non-recommendation is **Value For Money** (correlation with recommendation = **0.66**, equal to Overall Rating itself). The gap between the two groups is stark:

| Metric | Recommended = no (n=127) | Recommended = yes (n=465) | Difference |
|---|---|---|---|
| Value For Money (mean) | 2.22 / 5 | 4.29 / 5 | **−2.07** |
| Overall Rating (mean) | 3.82 / 10 | 8.43 / 10 | **−4.61** |
| Staff Service (mean) | 4.01 / 5 | 4.39 / 5 | −0.38 |
| Seat Comfort (mean) | 3.87 / 5 | 4.01 / 5 | −0.14 |
| Food & Beverages (mean) | 3.85 / 5 | 3.94 / 5 | −0.09 |
| Inflight Entertainment (mean) | 4.16 / 5 | 4.12 / 5 | ≈0 |

Passengers who do not recommend Qatar Airways Business Class overwhelmingly feel the price paid was not justified — a finding consistent across traveller segments (see §4).

---

## 2. Inflight Service Quality (`inflight_service_quality`)

This TAPP facet captures narrative descriptions of onboard service and adds strong semantic signal beyond the numeric Staff Service score.

| `inflight_service_quality` | n | No-recommend rate | Mean VFM (no) | Mean VFM (yes) |
|---|---|---|---|---|
| excellent | 280 | **1.1%** | 5.00 | 4.62 |
| good | 105 | **8.6%** | 3.00 | 4.17 |
| inconsistent | 104 | **38.5%** | 2.68 | 3.62 |
| poor | 98 | **72.4%** | 1.80 | 2.93 |

Service quality being rated **poor** or **inconsistent** in the review narrative (covering 202 reviews, 34% of the sample) drives the bulk of non-recommendations. Crucially, even within the "poor" service group, VFM remains very low (mean 1.80 for non-recommenders), confirming the two dimensions compound each other: bad service *and* perceived overpricing.

---

## 3. Service Consistency Across Sectors (`service_consistency_across_sectors`)

Multi-sector itineraries expose passengers to variable cabin crew, aircraft, and ground experiences. This TAPP facet captures whether the passenger perceived consistency.

| `service_consistency_across_sectors` | n | No-recommend rate |
|---|---|---|
| consistent_high | 298 | **2.3%** |
| variable_across_sectors | 248 | **33.9%** |
| consistently_poor | 17 | **76.5%** |

Passengers on routes with **variable or consistently poor** cross-sector service account for **97 of 127 non-recommendations (76%)**. This facet is partially redundant with `inflight_service_quality` but adds the multi-leg dimension: a pleasant first sector followed by a poor second sector generates disappointment disproportionate to a uniformly mediocre experience.

---

## 4. Seat Product (`seat_product_received`)

This TAPP facet identifies the physical seat type and adds signal beyond Seat Comfort scores.

| `seat_product_received` | n | No-recommend rate | Mean Seat Comfort |
|---|---|---|---|
| QSuite | 127 | **13.4%** | — |
| standard_lie_flat_1x2x1 | 166 | **14.5%** | — |
| angled_flat_2x2x2 | 71 | **39.4%** | — |
| recliner_non_lie_flat | 8 | **37.5%** | — |

Passengers receiving **angled-flat or recliner seats** — which fall short of full lie-flat — are non-recommended at roughly 3× the rate of those on QSuite or standard lie-flat. These products are found on some regional/short-haul segments, but when passengers pay Business-Class fares expecting a lie-flat bed and receive an angled-flat seat, VFM dissatisfaction follows. Mean Overall Rating for angled-flat non-recommenders is only **3.89 / 10**.

---

## 5. Traveller Type Context

Business travellers have the highest non-recommendation rate (32.4%), likely because their expectations for consistent, high-quality service are most demanding and value judgements most price-sensitive.

| Traveller Type | n | No-recommend rate |
|---|---|---|
| Business | 142 | **32.4%** |
| Family Leisure | 44 | 22.7% |
| Couple Leisure | 150 | 20.0% |
| Solo Leisure | 256 | 16.0% |

---

## 6. Causal Summary

Non-recommendation in Qatar Airways Business Class is driven by a small set of compounding factors:

1. **Poor perceived value for money** — the strongest single predictor (r = 0.66), reflecting a gap between fare paid and experience received.
2. **Poor or inconsistent inflight service** (`inflight_service_quality` = poor/inconsistent): 72% and 39% non-recommend rates respectively; 202 reviews affected.
3. **Variable cross-sector service** (`service_consistency_across_sectors` = variable or consistently_poor): accounts for 76% of all non-recommendations.
4. **Sub-standard seat product** (`seat_product_received` = angled_flat or recliner): ~38–40% non-recommend rate, driven by unmet lie-flat expectations on premium fares.

The interaction is clear: when any of these failures occurs on a route where the ticket price implies a premium experience, passengers judge the value negatively and do not recommend the airline.

---

*Method note: TAPP-generated columns `inflight_service_quality`, `service_consistency_across_sectors`, and `seat_product_received` were all used. `inflight_service_quality` and `service_consistency_across_sectors` provide meaningful incremental signal over the structured numeric ratings. `seat_product_received` partially overlaps with Seat Comfort scores but adds qualitative seat-type context. All three were cross-validated against structured columns (Overall Rating, Value For Money, Staff Service, Seat Comfort) and the binary Recommended outcome.*
