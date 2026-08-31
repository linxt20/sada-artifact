---
dataset: flag_6
scenario: concept_attribute_workload
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "agent_workload_burden"
query: "What kinds of tickets create heavier agent workload?"
source_table: augment_table/flag_6/concept_attribute_workload/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:20:32.097027+00:00
wall_seconds: 32.1
---

# Agent Workload Analysis — Ticket Characteristics

## Dataset Overview
- **500 tickets** across 5 categories and 3 priority levels  
- Focus variable: `workload_index` (continuous score; higher = heavier agent workload)

---

## Key Finding 1: Priority Is the Strongest Driver of Workload

| Priority | Mean Workload | Median Workload | Count |
|---|---|---|---|
| 1 - Critical | **18.91** | 19.53 | 88 |
| 2 - High | 14.20 | 15.06 | 379 |
| 3 - Moderate | 9.63 | 9.61 | 33 |

Priority alone explains a large part of the variance — `priority_score` correlates with `workload_index` at **r = 0.46**. Critical tickets impose roughly **2× the workload** of Moderate tickets.

---

## Key Finding 2: Resolution Time Strongly Co-varies with Workload

`resolution_hours` and `workload_index` are correlated at **r = 0.60**, the strongest pairwise relationship in the dataset. Tickets that take longer to resolve (regardless of category) consistently drive higher agent effort.

---

## Key Finding 3: Category Has a Secondary Effect

| Category | Mean Workload | Count |
|---|---|---|
| Hardware | **15.55** | 26 |
| Network | 14.89 | 284 |
| Database | 14.78 | 109 |
| Software | 13.90 | 72 |
| Inquiry / Help | 13.39 | 9 |

Differences across categories are modest (~2 points) compared with the priority gap (~9 points). Hardware and Network tickets trend slightly higher, but Hardware has only 26 tickets so this estimate is uncertain.

---

## Key Finding 4: Combined Effect — Critical + Network Dominates Volume

Among Critical tickets, **Network** contributes the most cases (50/88) with a mean workload of **19.30**, making it the single largest source of high-workload tickets in absolute terms. Critical Software tickets show the highest per-ticket mean (26.5) but represent only 1 ticket — too sparse to generalize.

---

## Exceptions and Weak Evidence

- **`updated_after_close`**: All 500 tickets in this dataset have `updated_after_close = 0`, so this variable provides no discriminating signal here.
- **Inquiry / Help**: Only 9 tickets — any category-level conclusions for this group are unreliable.
- **Software at Critical priority**: n = 1; the extreme mean (26.5) should be ignored.

---

## Decision-Ready Summary

> **Tickets that create the heaviest agent workload are high-priority (Critical) tickets with long resolution times, especially in the Network and Database categories.** Priority level is the most actionable lever — routing or escalating Critical tickets differently could have the largest impact on workload distribution. Category is a secondary signal; Hardware and Network tickets warrant slightly more buffer, but the effect is small relative to priority.
