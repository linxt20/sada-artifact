---
dataset: airlines_review_full
scenario: concept_advantage_attributes
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "airline_competitive_advantage"
query: "What are the common advantage attributes of airlines whose overall rating is high?"
source_table: augment_table/airlines_review_full/concept_advantage_attributes/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-08-03T05:50:39.134434+00:00
wall_seconds: 55.3
---

# Advantage Attributes of High-Rated Airlines
**Query:** What are the common advantage attributes of airlines whose overall rating is high?

---

## Method Note

**TAPP-generated columns used:** `cabin_crew_attitude`, `ground_service_quality`, `service_proactivity`, `service_consistency`, `food_quality`, `seat_comfort_assessment`, `baggage_handling_outcome`, `customer_service_responsiveness`, `refund_rebooking_handling`, `value_for_money_perception`.

All TAPP facets are cross-checked against the original structured columns (`Seat Comfort`, `Staff Service`, `Food & Beverages`, `Inflight Entertainment`, `Value For Money`, `Overall Rating`, `Recommended`).

**Group definitions:** High = Overall Rating ≥ 8 (n = 3,406); Low = Overall Rating ≤ 4 (n = 3,403). Total dataset: 8,100 reviews.

---

## 1. Outcome Baseline

| Metric | High (≥8) | Low (≤4) |
|---|---|---|
| n | 3,406 | 3,403 |
| Recommended = yes | **98.4%** | 3.7% |
| Mean Value For Money | **4.58 / 5** | 1.63 / 5 |
| Mean Staff Service | **3.91 / 5** | 3.20 / 5 |
| Mean Seat Comfort | **3.71 / 5** | 3.10 / 5 |
| Mean Food & Beverages | **3.61 / 5** | 3.13 / 5 |
| Mean Inflight Entertainment | **3.80 / 5** | 3.44 / 5 |

Value For Money shows the largest gap (4.58 vs 1.63), making it the single strongest structural differentiator.

---

## 2. Key Advantage Attributes

### 2a. Value for Money — Dominant Driver

The structured `Value For Money` rating gap (Δ = 2.95 points) is the clearest separator. This is fully corroborated by `value_for_money_perception`:

| Perception | High | Low |
|---|---|---|
| excellent_value | **61.3%** | 0.5% |
| fair_value | 20.4% | 1.8% |
| poor_value_overpriced | 1.6% | **69.6%** |

High-rated airlines are perceived as delivering excellent or fair value by **81.7%** of reviewers.

### 2b. Cabin Crew Attitude — Sharpest Binary Differentiator

`cabin_crew_attitude` shows the starkest split across all TAPP facets:

| Attitude | High | Low |
|---|---|---|
| warm_proactive | **87.2%** | 2.8% |
| professional_neutral | 9.8% | 4.5% |
| cold_indifferent | 2.6% | **66.8%** |
| rude_hostile | 0.2% | 21.9% |

Warm, proactive crew is a hallmark of high-rated airlines, consistent with the structured `Staff Service` mean advantage (3.91 vs 3.20).

### 2c. Service Proactivity and Consistency

`service_proactivity` (True = crew anticipates needs): **80.2%** of high-rated vs only **0.9%** of low-rated reviews report proactive service.

`service_consistency` reinforces this: **72.6%** of high-rated reviews report `consistent_high` service vs **71.9%** of low-rated reporting `consistent_low`.

### 2d. Food Quality

`food_quality` for high-rated: 26.6% `excellent` + 36.7% `good` = **63.3% positive**. For low-rated: 19.4% `poor` and only 2.3% positive. Corroborated by structured Food & Beverages (3.61 vs 3.13). Note: ~26% of high-rated reviews have `Unknown` food quality (likely short-haul flights with no meal service).

### 2e. Seat Comfort

`seat_comfort_assessment` for high-rated: 36.7% `comfortable_spacious` + 31.5% `adequate` = **68.2% non-negative**, versus only 1.5% comfortable in low-rated segment. Structured Seat Comfort confirms: 3.71 vs 3.10.

### 2f. Baggage & Customer Service Reliability

`baggage_handling_outcome`: `no_issue` = **75.8%** (high) vs 64.4% (low). Lost/damaged baggage appears in 11.7% of low-rated reviews vs only 0.5% of high-rated.

`customer_service_responsiveness`: Among those who contacted service, `responsive_helpful` = **94.8%** of high-rated contacts vs near-zero for low-rated (where `unresponsive_dismissive` dominates at 65.1%).

`refund_rebooking_handling`: 93.8% of high-rated reviews have `not_applicable` (no disruption needed), vs 44.7% `refused_obstructed` in low-rated — reflecting that low-rated airlines frequently generate disruption and then handle it poorly.

### 2g. Ground Service

`ground_service_quality` is partially observed (54.8% Unknown in high-rated, 27.9% in low), limiting inference. Where observed: `efficient_helpful` = 34.7% of high-rated vs 0.6% of low-rated.

---

## 3. Leading Airlines in High-Rated Segment

| Airline | High-Rated Reviews |
|---|---|
| Qatar Airways | 974 |
| Singapore Airlines | 504 |
| Emirates | 375 |
| Turkish Airlines | 372 |
| Cathay Pacific Airways | 348 |
| Air France | 253 |

These airlines collectively account for **68%** of high-rated reviews and most belong to the 5-star carrier tier, flying predominantly Economy (60.4%) and Business Class (32.8%).

---

## 4. Summary of Common Advantage Attributes

| Attribute | Signal Source | High-Rated Rate | Low-Rated Rate |
|---|---|---|---|
| Excellent/fair value for money | `Value For Money` + `value_for_money_perception` | 81.7% | 2.3% |
| Warm/proactive crew | `Staff Service` + `cabin_crew_attitude` | 87.2% | 2.8% |
| Proactive service | `service_proactivity` | 80.2% | 0.9% |
| Consistent high service | `service_consistency` | 72.6% | 0.8% |
| Good-to-excellent food | `food_quality` | 63.3% | 2.3% |
| Comfortable seating | `seat_comfort_assessment` | 68.2% | 12.8% |
| No baggage issues | `baggage_handling_outcome` | 75.8% | 64.4% |
| Responsive customer service (when contacted) | `customer_service_responsiveness` | 94.8% | 0.5% |

**Core finding:** High overall ratings cluster around five reinforcing advantages — (1) **perceived value for money**, (2) **warm and proactive cabin crew**, (3) **service consistency**, (4) **food quality**, and (5) **reliable baggage and complaint handling**. Seat comfort contributes but with smaller absolute effect. Ground service data is too sparse to be conclusive. Refund/rebooking friction is distinctly a *low-rating* pathology rather than a direct advantage driver.
