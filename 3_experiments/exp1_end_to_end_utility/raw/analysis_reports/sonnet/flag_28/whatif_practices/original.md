---
dataset: flag_28
scenario: whatif_practices
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: what_if
focus_variable: "percent_complete"
query: "If teams adopted the goal-management practices described by top performers, how much would achievement improve?"
source_table: augment_table/flag_28/whatif_practices/original.csv
generated_at: 2026-07-26T13:38:31.223961+00:00
wall_seconds: 101.23
---

# What-If Analysis: Impact of Adopting Top-Performer Goal-Management Practices

## Dataset Overview

The dataset contains **550 goals** across departments (HR, IT, Finance, Marketing) with columns including `percent_complete` (the achievement focus variable), `target_percentage`, `priority`, `state`, `metric`, `category`, and `department`.

---

## Defining Top Performers

Goals with `percent_complete ≥ 80` are treated as top performers — **89 goals (16%)**.  
The remaining **461 goals (84%)** average 43.3% completion.

| Cohort | Count | Avg `percent_complete` | Completion Rate |
|---|---|---|---|
| Top performers (≥ 80%) | 89 | ~88% | 84.3% |
| All others (< 80%) | 461 | 43.3% | 41.4% |
| **Overall** | **550** | **50.8%** | **48.4%** |

---

## Key Practice Differentiating Top Performers: Priority

The single strongest differentiator is **goal priority**:

| Priority | % of Top Performers | % of Others | Avg `percent_complete` |
|---|---|---|---|
| Critical | 49.4% | 10.8% | 75.0% |
| High | 46.1% | 10.8% | 76.0% |
| Medium | 4.5% | 41.0% | 38.3% |
| Low | 0% | 37.3% | 38.4% |

- **95.5%** of top performers have Critical or High priority.
- **78%** of non-top-performers are Medium or Low priority.
- Critical/High goals average **75.5%** completion vs. **38.4%** for Medium/Low — a gap of **~37 percentage points**.

Secondary signals (category mix, metric type, target percentage) are broadly similar across cohorts, suggesting priority classification drives the achievement gap more than goal subject matter.

---

## Counterfactual: If Underperformers Adopted Top-Performer Practices

If the **361 Medium/Low-priority goals** were managed with the same priority-level focus as top performers, and their `percent_complete` rose to the Critical/High average (~75.5%):

| Scenario | Avg `percent_complete` |
|---|---|
| Current baseline | 50.8% |
| All goals at Critical/High level | **75.5%** |
| **Estimated uplift** | **+24.7 percentage points (+49% relative)** |

Even a **partial adoption** — say Medium/Low goals reaching 60% completion (halfway toward top-performer levels) — would improve the portfolio average to ~**63%**, a +12 pp gain.

---

## Supporting Evidence

- **Shorter timelines correlate with higher achievement**: Top performers average **178-day** goal durations vs. **202 days** for others, suggesting tighter, more focused goals.
- **Completion state aligns**: 84.3% of top-performer goals are "Completed" vs. 41.4% for others.
- **Target percentage is similar** across cohorts (top: 74.4 vs. others: 74.8), ruling out "easy goals" as an explanation for top-performer success.

---

## Caveats and Weak Evidence

- **Causality is unclear**: Priority may be assigned to goals already likely to succeed (resource-backed projects), not be an independent lever.
- The dataset has **no resource, headcount, or budget columns**, so it cannot confirm whether higher priority translates to more investment or just stricter oversight.
- The ~5% of top performers with Medium priority (n ≈ 4) shows priority is not the only driver; a small number of well-executed Medium-priority goals do reach high completion.
- Cancelled goals (n=24, avg 44.5% completion) are excluded from straightforward adoption scenarios, but their prevalence at Medium/Low priority adds complexity.

---

## Decision-Ready Summary

> Adopting the goal-management practices of top performers — primarily **elevating goal priority from Medium/Low to High/Critical** — is associated with an estimated **+24.7 percentage point** improvement in average goal achievement (from 50.8% to ~75.5%). Even partial adoption by the majority of the portfolio could yield a **+12 pp** gain. The clearest lever is priority classification, which predicts completion rates almost twice as strongly as any other observable factor in this dataset.
