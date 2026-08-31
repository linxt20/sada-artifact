---
dataset: flag_6
scenario: whatif_workload
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: what_if
focus_variable: "resolution_time"
query: "If the ticket types that create the heaviest agent workload were reduced, how much would resolution time drop?"
source_table: augment_table/flag_6/whatif_workload/original.csv
generated_at: 2026-07-26T13:44:03.296163+00:00
wall_seconds: 178.79
---

# What-If Analysis: Reducing Heavy-Workload Ticket Types and Impact on Resolution Time

## Dataset Overview

- **500 tickets** across 5 categories, 5 agents, and 3 priority levels (Jan–Feb 2023)
- Resolution time computed as `closed_at − opened_at`; 50 tickets have negative values (data quality issue) and are excluded from mean-based analysis (428 valid records)
- **Baseline mean resolution time: ~258 hours** (median: ~150 hours, reflecting right-skewed distribution)

---

## Which Ticket Types Create the Heaviest Agent Workload?

"Heaviest workload" is assessed on two dimensions: **volume** (ticket count) and **total agent hours consumed** (count × mean resolution time).

### By Category

| Category | Tickets | Volume Share | Mean Res. Time (h) | Total Agent Hours | Hour Share |
|---|---|---|---|---|---|
| **Network** | 284 | **56.8%** | 264.9 | 62,482 | **58.5%** |
| Database | 109 | 21.8% | 249.2 | 21,031 | 19.7% |
| Software | 72 | 14.4% | **278.0** | 17,364 | 16.3% |
| Hardware | 26 | 5.2% | 199.2 | 4,869 | 4.6% |
| Inquiry / Help | 9 | 1.8% | 158.9 | 1,079 | 1.0% |

**Network tickets dominate on both dimensions**: 56.8% of ticket volume and 58.5% of total agent-hours.  
**Software tickets carry the highest per-ticket resolution time** (278 h mean), adding disproportionate burden relative to their volume (14.4%).

### By Priority

| Priority | Tickets | Volume Share | Mean Res. Time (h) | Hour Share |
|---|---|---|---|---|
| 2 - High | 379 | 75.8% | 229.9 | 78.3% |
| 1 - Critical | 88 | 17.6% | 187.7 | 14.8% |
| 3 - Moderate | 33 | 6.6% | 246.6 | 6.9% |

"2 - High" priority tickets account for 78% of total agent-hours. Notably, **Critical tickets resolve faster on average (188 h) than High or Moderate tickets**, suggesting expedited handling for the most urgent cases.

---

## What-If Scenarios: Reducing Network Ticket Volume

Because Network tickets drive 58.5% of all agent-hours, they are the primary lever.

| Scenario | New Mean Res. Time (h) | Drop from Baseline (h) | % Reduction |
|---|---|---|---|
| Baseline | 258.0 | — | — |
| Network −25% | 251.2 | 6.8 | 2.6% |
| Network −50% | 246.3 | 11.6 | **4.5%** |
| Network −100% (eliminated) | 249.0 | 9.0 | 3.5% |

**Key finding:** Reducing Network ticket volume by 50% lowers the mean resolution time by approximately **11.6 hours (~4.5%)**. Even full elimination of Network tickets yields only a ~3.5% drop, because the remaining categories (Database, Software) have similar or higher per-ticket resolution times.

---

## Notable Exception: Agent-Level Outlier (Fred Luddy)

Fred Luddy handles **84 tickets** but with a mean resolution time of **750 hours** — roughly **6× the mean of other agents** (~124 h). His tickets span all categories (Network: 43, Database: 18, Software: 12, Hardware: 3). His resolution times follow a structured pattern (many values are multiples of 4.8 h), suggesting possible data encoding differences or a systematic process anomaly rather than genuine inefficiency.

> **If Fred Luddy's tickets are excluded**, overall mean resolution time drops from **223 h to 124 h** — a reduction of ~44%. This dwarfs any category-level what-if scenario and suggests **agent assignment or data quality is a more significant driver of mean resolution time than ticket type alone**.

---

## Summary and Decision Guidance

| Action | Expected Mean RT Drop | Confidence |
|---|---|---|
| Reduce Network ticket volume by 50% | ~11.6 h (4.5%) | Moderate — volume effect real, but similar RT across categories limits gain |
| Reduce Software tickets (highest per-ticket RT) by 50% | ~0.9–2.0 h (<1%) | Weak — small volume share limits overall impact |
| Investigate/resolve Fred Luddy data anomaly | ~99 h (~44%) | High — single-agent outlier dominates the mean |

**Bottom line:** Reducing Network tickets—the heaviest workload category by volume and total hours—would produce a **modest but real ~4–5% drop** in mean resolution time. However, the data reveals that **agent-level resolution time variability (particularly Fred Luddy's anomalous times) is a far larger driver** of overall mean resolution time. Decision-makers should prioritize understanding and correcting that anomaly before expecting category-level workload reductions to materially move the aggregate metric.
