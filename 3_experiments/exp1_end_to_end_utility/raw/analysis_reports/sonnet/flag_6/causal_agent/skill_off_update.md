---
dataset: flag_6
scenario: causal_agent
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "agent_resolution_discrepancy"
query: "Why do some agents have longer resolution times?"
source_table: augment_table/flag_6/causal_agent/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:20:51.642126+00:00
wall_seconds: 70.43
---

# Analysis Report: Why Some Agents Have Longer Resolution Times

**Dataset:** `sonnet__skill_off_update.csv` | **Variant:** `skill_off` | **Records:** 500 tickets, 5 agents

---

## Key Finding: Agent Identity Is the Dominant Driver

The strongest predictors of `resolution_hours` are **agent-level factors**, not ticket characteristics like priority or category.

| Feature | Correlation with `resolution_hours` |
|---|---|
| `agent_concurrent_load` | **0.74** |
| `agent_avg_resolution_hours` | **0.73** |
| `category_avg_resolution_hours` | 0.06 |
| `priority_numeric` | 0.05 |

Priority and category explain almost nothing. The agent assigned to a ticket largely determines how long it will take.

---

## Agent-Level Performance Gap

| Agent | Actual Mean Resolution (hrs) | `agent_avg_resolution_hours` | Mean Concurrent Load | Ticket Count |
|---|---|---|---|---|
| Fred Luddy | **750.0** | **750.0** | **5.5** | 84 |
| Howard Johnson | 136.1 | 159.7 | 1.4 | 100 |
| Luke Wilson | 131.9 | 160.2 | 1.5 | 104 |
| Charlie Whitherspoon | 118.6 | 150.1 | 1.5 | 103 |
| Beth Anglin | 109.1 | 136.3 | 1.1 | 98 |

Fred Luddy's tickets resolve on average **~5.5× slower** than all other agents combined (mean ≈ 750 hrs vs. ≈ 124 hrs for the rest). This single agent accounts for nearly all variance in long resolution times in the dataset.

---

## Factor 1: Concurrent Workload (Strongest Measurable Driver)

High `agent_concurrent_load` strongly increases resolution times—both across the dataset as a whole and especially for Fred Luddy.

**Dataset-wide — Resolution hours by concurrent load:**

| Load Level | Mean Resolution (hrs) |
|---|---|
| 0 | 127.3 |
| 1–2 | 136.3 |
| 3–4 | 222.5 |
| 5+ | 743.7 |

Fred Luddy's mean concurrent load is **5.5**, while other agents average **1.5**. Within Fred's own tickets, the correlation between load and resolution hours is **r = 0.82**, a very strong relationship. For other agents, this correlation is essentially zero (r ≈ 0.002), suggesting concurrent overload is primarily a Fred Luddy phenomenon.

---

## Factor 2: Inherent Agent Skill / Efficiency (`agent_avg_resolution_hours`)

The column `agent_avg_resolution_hours` encodes each agent's historical baseline performance. Fred Luddy's baseline (750 hrs) is pre-tagged as far above all other agents (136–160 hrs range). Even at **zero concurrent load**, Fred's tickets average ~200+ hours, compared to sub-150 hours for others—indicating a skill or workflow gap independent of workload.

---

## Factor 3: Category and Priority Are Weak Factors

- `category_avg_resolution_hours` ranges only from ~159 to ~278 hrs—a narrow spread that explains little of the observed variance (r = 0.06).
- `priority_numeric` is similarly uncorrelated (r = 0.05) with actual resolution time, suggesting priority assignment does not meaningfully predict outcome speed in this dataset.

---

## Exceptions and Caveats

- **Negative resolution hours** exist for some tickets (e.g., −400.7 hrs), indicating data quality issues (timestamps out of order). These were included in correlations but may distort averages.
- **Fred Luddy's resolution hours are exactly proportional** (many values are multiples of clean numbers like 67.2, 81.6, 192.0), which may suggest some values are computed/synthetic rather than raw timestamps—treat the 750-hr average with some caution.
- The `is_self_closed` flag shows almost no effect on resolution time (self-closed: 216.7 hrs vs. not: 225.3 hrs), making it a negligible factor.

---

## Summary

> **Agents have longer resolution times primarily because of who they are (inherent skill/efficiency) and how overloaded they are (concurrent ticket load).** Fred Luddy, carrying consistently high concurrent workloads (avg 5.5 tickets simultaneously), resolves tickets ~5× slower than peers. Redistributing Fred's load or providing additional support would have the greatest impact on reducing overall resolution times. Ticket category and priority are not actionable levers in this dataset.
