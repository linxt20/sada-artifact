---
dataset: airlines_review
scenario: whatif_service_complaints
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "Overall Rating"
query: "If airlines eliminated the most common cabin-service complaints in the reviews, how much would the average Overall Rating improve?"
source_table: augment_table/airlines_review/whatif_service_complaints/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:05:56.437094+00:00
wall_seconds: 73.5
---

# What-If Analysis: Eliminating Most Common Cabin-Service Complaints

**Dataset:** 935 airline reviews (900 with Overall Rating) | **Current Average Overall Rating: 6.53 / 10**

---

## Identifying the Most Common Cabin-Service Complaints

Three augmented columns capture cabin-service complaint dimensions. The most frequent complaint in each is:

| Dimension | Most Common Complaint | Count | Share of Rated Reviews |
|---|---|---|---|
| Crew Service | `inattentive_or_unresponsive` | 189 | 21% |
| Food & Beverages | `poor_quality_or_taste` | 116 | 13% |
| Cabin-Class Expectation Gap | `below_class_standard` | 390 | 43% |

---

## Impact on Overall Rating by Complaint Type

Reviews **without** the respective complaints score considerably higher:

| Complaint Type | Complaint Group Avg | No-Complaint Group Avg | Rating Gap |
|---|---|---|---|
| Inattentive/unresponsive crew | 3.39 | 7.88 | **+4.49** |
| Poor food quality/taste | 4.96 | 7.03 | **+2.07** |
| Below class standard (cabin) | 3.41 | 8.66 (meets standard) | **+5.26** |

---

## What-If Simulation

Each scenario applies the average rating lift to affected reviews (capped at 10), modelling what would happen if complaints were resolved to the no-complaint / meets-standard baseline.

| Scenario | Simulated Avg Rating | Improvement |
|---|---|---|
| Baseline (current) | 6.53 | — |
| Fix inattentive crew only | 7.41 | **+0.88** |
| Fix poor food quality only | 6.79 | **+0.26** |
| Fix below-class-standard cabin gap only | 8.61 | **+2.08** |
| **Fix all three together** | **9.15** | **+2.62** |

---

## Key Findings

1. **Cabin-class expectation gap is the dominant driver.** Resolving the "below class standard" experience for 390 reviews (43% of rated reviews) alone would improve the average rating by ~2.1 points — the single largest lever available.

2. **Crew attentiveness is the second-largest lever.** Eliminating inattentive/unresponsive crew complaints adds ~0.88 points. The gap between complaint-affected (3.39) and complaint-free (7.88) reviews is nearly 4.5 points, indicating severe satisfaction damage.

3. **Food quality improvements are real but modest (+0.26)** due to smaller affected volume (13% of reviews), even though the per-review rating penalty (~2 points) is significant.

4. **Combined effect (+2.62) is near-additive but partially dampened by overlaps.** 180 of 189 inattentive-crew reviews also appear as "below class standard," and 80 of 116 poor-food reviews do too. In practice, improving the cabin experience holistically addresses all three dimensions simultaneously.

---

## Caveats & Weak Evidence

- **Causal direction is assumed, not proven.** Low ratings may reflect broader dissatisfaction that manifests in multiple complaint labels simultaneously; complaint elimination might not deliver the full average-group lift.
- **"Below class standard"** is a synthetic classification; it bundles crew, food, seat, and environment shortfalls — making it more of a composite outcome than a single operational fix.
- **Ceiling effect:** Many affected reviews already have ratings of 1–3; a pure additive lift overshoots the 10-point cap for some, slightly deflating the simulated combined average.
- The `rushed_service` crew complaint (n=6) and `special_meal_failure` food complaint (n=19) were excluded as they are not the most common.

---

## Decision-Ready Summary

> **Eliminating the three most common cabin-service complaint categories — below-class-standard experience, inattentive crew, and poor food quality — could raise the average Overall Rating from 6.53 to approximately 9.15 (+2.6 points).** The cabin-class expectation gap (43% of reviews) is the highest-priority target, followed by crew attentiveness. Food quality improvements add incremental gains. Given heavy overlap between these complaints, airlines should treat them as a bundled service-quality programme rather than isolated fixes.
