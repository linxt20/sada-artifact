---
dataset: airlines_review
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's in these airline reviews — I'm not sure which aspect is most worth analyzing."
source_table: augment_table/airlines_review/focus_inference/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:05:06.393713+00:00
wall_seconds: 69.28
---

# Airline Reviews Analysis: What's Most Worth Analyzing?

## Executive Summary

The dataset contains **900 airline reviews** (verified: 77%) covering Economy (n=563), Business (n=237), Premium Economy (n=86), and First Class (n=14). The primary outcome is **Overall Rating** (mean 6.53/10, SD 3.24) and **Recommended** (64% yes). The single strongest driver is **Value for Money** (r = 0.89 with Overall Rating), making perceived value the most analytically productive focus. Crew service quality — both structured (Staff Service) and semantic (`crew_service_quality`) — is the next most powerful discriminator. Premium Economy stands out as a structurally weak segment worth targeted investigation.

---

## Method Note

TAPP-generated columns used in this report: `crew_service_quality`, `seat_hardware_condition`, `food_quality_assessment`, `disruption_handling_quality`, `service_decline_signal`, `premium_economy_value_gap`. Columns `special_meal_handling` (n=68 positives, 8%) was low-coverage and not a central focus.

---

## 1. Outcome Variables and Their Drivers

### Structured rating correlations with Overall Rating

| Sub-dimension | Mean (1–5) | Corr. with Overall Rating |
|---|---|---|
| **Value For Money** | 3.44 | **0.886** |
| Food & Beverages | 3.57 | 0.087 |
| Staff Service | 3.93 | 0.070 |
| Seat Comfort | 3.68 | 0.011 |
| Inflight Entertainment | 3.89 | −0.033 |

**Value For Money dominates.** The other structured sub-dimensions show near-zero linear correlation with Overall Rating, suggesting reviewers integrate many soft factors into their headline score that the numeric sub-scales do not capture — which is precisely where the TAPP semantic columns add signal.

---

## 2. Crew Service Quality — The Strongest Semantic Discriminator

`crew_service_quality` partitions the dataset sharply:

| Crew Category | Mean Overall Rating | Recommended % | n |
|---|---|---|---|
| attentive_proactive | 9.24 | **98.7%** | 383 |
| professional_standard | 6.50 | 68.5% | 149 |
| inconsistent | 5.45 | 52.3% | 109 |
| reactive_only | 4.69 | 43.6% | 55 |
| rude_dismissive | 2.50 | **9.4%** | 149 |
| Unknown | 2.65 | 9.1% | 55 |

The gap between **attentive_proactive** (9.24) and **rude_dismissive** (2.50) is 6.7 points — nearly double the dataset SD. The structured Staff Service mean of 3.93 masks this bimodal distribution; `crew_service_quality` reveals it clearly. **Crew behavior is the highest-leverage lever for recommendation rates.**

---

## 3. Value for Money by Cabin Class

| Class | Mean Overall Rating | Mean Value For Money | n |
|---|---|---|---|
| First Class | 7.93 | 4.21 | 14 |
| Business Class | 7.10 | 3.67 | 237 |
| Economy Class | 6.37 | 3.40 | 563 |
| **Premium Economy** | **5.83** | **2.94** | 86 |

Premium Economy scores lowest on both Overall Rating and Value For Money despite sitting between Economy and Business in price. The `premium_economy_value_gap` column confirms this structurally: **46 of 86 Premium Economy reviews (53%) flag a value gap**, and those passengers rate the experience 4.41 vs. 7.45 for the non-gap group (ΔVfM: 2.28 vs. 3.70). **Premium Economy dissatisfaction is the most actionable segment-level finding.**

---

## 4. Disruption Handling — A High-Impact Edge Case

| Disruption Category | Mean Overall Rating | n |
|---|---|---|
| proactive_excellent | 9.49 | 41 |
| no_disruption | 7.37 | 658 |
| adequate | 8.36 | 28 |
| poor_reactive | **2.34** | 173 |

173 reviews (19%) describe **poor reactive disruption handling**, which crashes the average rating to 2.34 — lower even than rude crew. Proactive handling (n=41) yields the highest mean in the dataset (9.49), showing the recovery opportunity is real. `disruption_handling_quality` is not redundant with any structured column and directly captures an operational failure mode.

---

## 5. Seat Hardware and Food — Secondary but Meaningful

**Seat condition** (`seat_hardware_condition`):

| Condition | Mean Overall Rating | n |
|---|---|---|
| new_excellent | 8.97 | 101 |
| adequate_functional | 7.89 | 340 |
| worn_dated | 6.01 | 126 |
| broken_faulty | 3.88 | 25 |
| Unknown | 4.67 | 308 |

Broken/faulty seats (n=25) and worn seats (n=126) drag scores down meaningfully. The high Unknown rate (34%) for seat condition suggests many reviews don't mention the seat — reflecting that seat experience only becomes salient when it fails.

**Food quality** (`food_quality_assessment`):

| Category | Mean Overall Rating | n |
|---|---|---|
| excellent_premium | 9.47 | 110 |
| good_acceptable | 8.74 | 260 |
| bland_average | 5.86 | 103 |
| poor_inedible | 3.69 | 122 |
| Unknown | 4.95 | 305 |

122 reviews (14%) flag poor/inedible food, with a mean rating of 3.69. Food appears to matter most in Business/First where expectations are higher, though the structured Food & Beverages column (mean 3.57, r=0.087) again undersells its impact — `food_quality_assessment` better captures the extremes.

---

## 6. Service Decline Signal

`service_decline_signal` = True in **184 reviews (20%)**, associated with a drop from 7.07 to 4.44 in Overall Rating (−2.63 points). This cross-cuts cabin class and route, suggesting a systemic perception of declining standards rather than isolated incidents.

---

## 7. Recommended Focal Areas (Priority Order)

| Priority | Focus | Key Evidence |
|---|---|---|
| 1 | **Value for Money** | r=0.886 with Overall Rating; Premium Economy 53% flag value gap |
| 2 | **Crew Service Quality** | 9.24 vs. 2.50 rating gap; 98.7% vs. 9.4% recommendation rate |
| 3 | **Disruption Handling** | poor_reactive (n=173) averages 2.34; proactive recovers to 9.49 |
| 4 | **Premium Economy Segment** | Lowest Overall Rating (5.83); majority flag value gap |
| 5 | **Food & Seat Hardware** | Secondary — high-impact at extremes, not driving median scores |

---

## Data Notes

- **Route concentration**: Singapore-hub routes dominate (London–Singapore n=21, Singapore–Sydney n=17), so findings are strongly SQ-adjacent.
- **Verified reviews** (77%) show almost identical mean rating (6.56) to unverified (6.45), suggesting no substantial selection bias.
- `special_meal_handling` (n=68, 8%) is too sparse for standalone conclusions.
