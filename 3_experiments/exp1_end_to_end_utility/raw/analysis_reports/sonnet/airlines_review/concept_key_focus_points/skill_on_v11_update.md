---
dataset: airlines_review
scenario: concept_key_focus_points
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "airline_service_quality"
query: "Help me understand the key points in this table — what should I concentrate on?"
source_table: augment_table/airlines_review/concept_key_focus_points/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:03:37.294549+00:00
wall_seconds: 39.44
---

# Airlines Review Dataset — Key Focus Points

## Overview

The dataset contains **900 verified airline reviews** across Economy, Business, Premium Economy, and First Class. The mean Overall Rating is **5.7/10** with high variance (std ≈ 3.5), and the split between recommended (480) and not-recommended (420) is near-even — signalling a polarised passenger experience.

---

## 1. Value for Money Is the Dominant Driver of Satisfaction

The correlation between **Value for Money** and Overall Rating is overwhelmingly strong ($r = 0.88$), far outpacing every other rated dimension:

| Dimension | Correlation with Overall Rating |
|---|---|
| Value For Money | **0.878** |
| Staff Service | 0.206 |
| Seat Comfort | 0.205 |
| Food & Beverages | 0.130 |
| Inflight Entertainment | 0.089 |

**Implication:** Pricing perception shapes the overall verdict more than any single service attribute. Improvements to other dimensions will have limited impact unless passengers feel they are getting fair value.

---

## 2. Staff Behaviour & Crew Responsiveness Are Strongly Polarised

These two augmented columns show the clearest separation between high- and low-rated experiences:

**Staff Behavior Tone vs. Avg Rating:**

| Tone | Avg Rating | Share of Reviews |
|---|---|---|
| friendly_attentive | 8.8 | 43% |
| professional_neutral | 7.5 | 5% |
| indifferent | 3.5 | 26% |
| rude_or_dismissive | 2.0 | 24% |

**Crew Responsiveness vs. Avg Rating:**

| Responsiveness | Avg Rating | Share of Reviews |
|---|---|---|
| proactive_attentive | 9.2 | 34% |
| reactive_adequate | 6.9 | 19% |
| slow_or_forgetful | 4.4 | 5% |
| absent_or_dismissive | 2.3 | 39% |

Nearly **40% of reviews** feature `absent_or_dismissive` crew, a major negative cluster averaging only 2.3/10. Combined with `rude_or_dismissive` tone (24% of reviews at 2.0/10), roughly **half the dataset reflects a seriously deficient crew experience**.

---

## 3. Disruption Handling Is a Make-or-Break Moment

Only ~18.5% of reviews involved a disruption, but the outcome splits sharply:

| Handling Quality | Avg Rating |
|---|---|
| well_handled_proactive | 9.3 |
| adequate_reactive | 7.6 |
| poor_communication | 2.5 |
| abandoned_no_support | **1.4** |

`poor_communication` and `abandoned_no_support` account for **237 reviews** combined — reviews that are near-uniformly terrible. When disruptions are handled proactively, they can actually *lift* satisfaction above the dataset average.

---

## 4. Customer Service Resolution Matters Enormously

| Resolution Outcome | Avg Rating | Count |
|---|---|---|
| resolved_promptly | 9.3 | 47 |
| no_issue_raised | 7.1 | 578 |
| resolved_with_effort | 5.0 | 14 |
| unresolved_or_ignored | **1.9** | 261 |

**261 reviews (29%)** involve unresolved complaints, averaging 1.9/10. This is the single largest identifiable group of dissatisfied passengers.

---

## 5. Cabin Class Differences Are Real but Moderate

Business Class earns the highest average rating (6.8) versus Economy (5.2), but the gap is narrower than staff/service factors suggest. Within-class variance is high — a poorly staffed Business Class flight scores comparably to a well-served Economy flight, underscoring that **service execution outweighs cabin class** in determining satisfaction.

---

## 6. Aircraft Type Mismatch Is a Minor but Real Issue

Only **23 reviews (2.6%)** flag `aircraft_type_mismatch = True`. This is too small a sample to draw strong conclusions, but it warrants monitoring — especially for Business Class expectations.

---

## Key Takeaways

1. **Prioritise Value for Money perception** — it is the strongest lever on Overall Rating.
2. **Address crew engagement gaps** — ~50% of reviews exhibit indifferent or dismissive crew behaviour, directly corresponding to low ratings.
3. **Invest in disruption response protocols** — proactive handling converts crises into positive moments; abandonment produces the worst outcomes in the dataset.
4. **Close the loop on complaints** — 29% of reviewers feel ignored; resolving issues promptly correlates with the highest possible ratings.
5. Inflight Entertainment has **minimal impact** on overall satisfaction; it is not a priority investment area relative to the above.
