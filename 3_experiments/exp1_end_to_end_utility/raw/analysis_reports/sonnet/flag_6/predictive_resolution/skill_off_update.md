---
dataset: flag_6
scenario: predictive_resolution
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary by agent and issue type?"
source_table: augment_table/flag_6/predictive_resolution/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:21:46.268479+00:00
wall_seconds: 39.3
---

# Resolution Time by Agent and Issue Type

## Dataset Overview

- **500 closed incidents** across 5 agents and 5 issue categories.
- Key numeric columns: `resolution_hours` (actual), `agent_avg_resolution_hours`, `category_avg_resolution_hours`, `agent_category_avg_resolution_hours`.

---

## Resolution Time by Agent

| Agent | Mean Resolution (hrs) | Relative Performance |
|---|---|---|
| Beth Anglin | 127.3 | Fastest |
| Charlie Whitherspoon | 140.9 | 2nd |
| Luke Wilson | 148.1 | 3rd |
| Howard Johnson | 150.6 | 4th |
| Fred Luddy | **750.0** | **Severe outlier** |

Four agents cluster tightly between ~127–151 hours. **Fred Luddy is a dramatic outlier**, averaging ~750 hours — roughly 5× slower than the next-slowest agent. This pattern is consistent across all categories he handles and is not driven by ticket volume alone (84 tickets, similar to peers).

---

## Resolution Time by Issue Category

| Category | Mean Resolution (hrs) |
|---|---|
| Inquiry / Help | 143.2 |
| Hardware | 195.8 |
| Database | 231.3 |
| Network | 242.6 |
| Software | 260.2 |

**Inquiry / Help** tickets resolve fastest (~143 hrs). **Software** and **Network** tickets are the most time-consuming (~242–260 hrs). The ~1.8× spread between fastest and slowest category is meaningful but much smaller than the agent-driven variance.

---

## Agent × Issue Type Interaction

Mean `resolution_hours` (hrs):

| Agent | Database | Hardware | Inquiry / Help | Network | Software |
|---|---|---|---|---|---|
| Beth Anglin | 117.6 | 132.9 | 106.2 | 119.7 | 163.8 |
| Charlie Whitherspoon | 149.9 | 243.1 | 77.7 | 135.4 | 110.0 |
| Howard Johnson | 127.9 | 137.7 | 171.1 | 164.9 | 126.3 |
| Luke Wilson | 128.2 | 112.4 | — | 158.9 | 147.6 |
| **Fred Luddy** | **706.7** | **436.8** | — | **761.7** | **851.2** |

**Key patterns among the four baseline agents:**
- **Beth Anglin** is consistently fast across all categories, with no clear weak spot.
- **Charlie Whitherspoon** handles Inquiry / Help and Software quickly but is slow on Hardware (243 hrs).
- **Howard Johnson** is notably slower on Inquiry / Help (171 hrs) compared to peers.
- **Luke Wilson** excels at Hardware (112 hrs) and Database (128 hrs).
- **Fred Luddy** dominates all categories with extreme resolution times; Software is his slowest (851 hrs) and Hardware his best (437 hrs) — still far above any peer.

---

## Exceptions and Caveats

- **Missing cells**: Fred Luddy and Luke Wilson have no Inquiry / Help tickets, limiting cross-agent comparison for that category.
- **Small cell sizes**: Hardware has only 3–7 tickets per agent, so those averages carry higher uncertainty (e.g., Charlie's 243-hr Hardware figure).
- **Fred Luddy anomaly**: The extreme values are consistent with the pre-computed `agent_avg_resolution_hours` column (750 hrs), confirming this is a dataset-level pattern, not a calculation artifact. The cause (skill gap, ticket type routing, data quality) cannot be determined from available columns alone.

---

## Decision-Ready Summary

- **Agent identity is the dominant driver** of resolution time. Assigning tickets to Fred Luddy should be flagged for review or avoided until the cause of his ~750-hr average is understood.
- Among the four efficient agents, **category matters secondarily**: Software and Network tickets take longest regardless of agent; Inquiry / Help resolves fastest.
- For routing optimization, **Beth Anglin** is the most reliable all-rounder; **Luke Wilson** is preferred for Hardware/Database; **Charlie Whitherspoon** is effective on Network and Software but should be monitored for Hardware tickets.
