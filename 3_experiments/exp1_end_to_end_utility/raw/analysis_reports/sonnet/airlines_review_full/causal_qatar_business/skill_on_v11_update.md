---
dataset: airlines_review_full
scenario: causal_qatar_business
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "non_recommendation_outcome"
query: "Explain why some Qatar Airways Business-Class flights receive a non-recommended (Recommended = no) result."
source_table: augment_table/airlines_review_full/causal_qatar_business/sonnet__skill_on_v11_update.csv
generated_at: 2026-08-03T05:48:35.636465+00:00
wall_seconds: 44.29
---

# Why Some Qatar Airways Business-Class Flights Receive a Non-Recommended Result

## Overview

Of 592 Qatar Airways Business-Class reviews in the dataset, **127 (21%)** carry `Recommended = no`. The analysis below identifies the dominant causal patterns using the augmented columns alongside the standard rating fields.

---

## 1. Value For Money Is the Strongest Discriminator

| Metric | Not Recommended | Recommended |
|---|---|---|
| **Value For Money (mean)** | **2.22** | **4.29** |
| Overall Rating (mean) | 3.82 | 8.43 |
| Staff Service (mean) | 4.01 | 4.39 |
| Seat Comfort (mean) | 3.87 | 4.01 |

The gap in *Value For Money* (2.22 vs 4.29) is by far the largest across all numeric dimensions, suggesting that Business-Class passengers who feel the price is unjustified—regardless of individual service elements—tend to withhold a recommendation.

---

## 2. Seat Product Downgrade Without Notice

`downgraded_without_notice` appears in **27.6%** of non-recommended reviews but only **2.8%** of recommended ones. The 35 non-recommended passengers in this category averaged an Overall Rating of just **3.6 / 10**. Passengers who paid for a QSuite or flat-bed product and received a lesser seat without prior warning are a leading driver of dissatisfaction and non-recommendation.

By contrast, QSuite delivery correlates strongly with recommendation (23% of recommended reviews vs 6% of non-recommended).

---

## 3. Cabin Crew Service Quality

| Crew Quality | % of Non-Recommended | % of Recommended |
|---|---|---|
| Poor | **44.1%** | 4.9% |
| Inconsistent | 18.1% | 6.0% |
| Good | 20.5% | 20.6% |
| Excellent | 5.5% | **66.7%** |

Poor or inconsistent cabin-crew service appears in **~62%** of non-recommended reviews. Among those rated "poor," the median Overall Rating is just **2 / 10**, making this the single most concentrated driver of negative outcomes after value perception.

---

## 4. Aircraft Age and Condition

| Condition | % of Non-Recommended | % of Recommended |
|---|---|---|
| new_well_maintained | 13.4% | **39.1%** |
| older_acceptable | 6.3% | 11.4% |
| old_degraded | **22.0%** | 3.2% |
| very_old_unacceptable | 1.6% | 0.4% |
| Unknown | 56.7% | 45.8% |

Old or degraded aircraft account for **~24%** of non-recommended cases versus only **~3.6%** of recommended ones—a roughly 7× enrichment. Seats that malfunction (e.g., recliners that won't stay up), worn cabins, and outdated interiors surface repeatedly in the review text for these rows.

---

## 5. Food & Beverage Quality

| F&B Quality | % of Non-Recommended | % of Recommended |
|---|---|---|
| Poor / Mediocre | **39.3%** | 12.9% |
| Good / Excellent | 9.5% | **58.1%** |
| Unknown | 51.2% | 29.0% |

Poor or mediocre food appears in ~39% of non-recommended reviews (vs 13% of recommended). While food is rarely the sole cause of non-recommendation, it compounds dissatisfaction when paired with crew or seat issues.

---

## 6. Service Consistency Across Legs

`variable_high_low` (e.g., excellent outbound, poor return) is present in **38.6%** of non-recommended reviews vs 27.7% of recommended ones. Passengers who experienced a sharp drop in quality on one leg of a multi-segment itinerary often withhold recommendation even when the overall average might seem acceptable.

---

## 7. FFP / Elite Status Handling

Elite-status mishandling (`ffp_elite_status_handling = True`) is present in only ~4–5% of both groups and is **not a meaningful differentiator** in this dataset.

---

## Summary of Causal Drivers

| Driver | Strength of Signal |
|---|---|
| Poor Value For Money perception | ★★★★★ |
| Seat downgrade without notice | ★★★★☆ |
| Poor / inconsistent cabin crew | ★★★★☆ |
| Old / degraded aircraft | ★★★☆☆ |
| Poor / mediocre food & beverage | ★★★☆☆ |
| Variable service across legs | ★★☆☆☆ |
| FFP elite-status mishandling | ★☆☆☆☆ |

**Key caveat:** The high "Unknown" rates in `aircraft_age_and_condition` (57%) and `food_beverage_quality` (51%) for non-recommended rows limit certainty about the true prevalence of those factors. The crew-quality and value-for-money signals are the most robustly populated and should be weighted most heavily in any intervention.
