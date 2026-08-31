---
dataset: flag_2
scenario: causal_reduce
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "resolution_time"
query: "How can we reduce incident resolution time?"
source_table: augment_table/flag_2/causal_reduce/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:15:25.438949+00:00
wall_seconds: 62.46
---

# Reducing Incident Resolution Time — Analysis Report

**Dataset:** `sonnet__skill_off_update.csv` | 500 incidents, 372 with resolved `resolution_hours`  
**Focus variable:** `resolution_hours` (mean: **1,043 hrs / ~43 days**; range: 24 – 2,206 hrs)

---

## Key Findings

### 1. Assignee Skill is the Strongest Driver (~8-Day Gap)

The `assignee_avg_resolution_hours` column reveals a clear performance spread across the five assignees:

| Assignee | Avg Resolution (hrs) | Avg Resolution (days) |
|---|---|---|
| Howard Johnson | 952.8 | **39.7** |
| Luke Wilson | 967.5 | 40.3 |
| Charlie Whitherspoon | 1,035.6 | 43.1 |
| Fred Luddy | 1,125.4 | 46.9 |
| Beth Anglin | 1,141.9 | **47.6** |

The gap between the fastest (Howard Johnson) and slowest (Beth Anglin) assignee is **189 hours (~7.9 days)**. Routing or reassigning incidents away from the slowest agents—or upskilling them—is the single highest-leverage lever in this dataset.

### 2. Assignment Group / Category Matters

| Assignment Group | Avg Resolution (hrs) |
|---|---|
| Hardware | 925.8 |
| Database | 946.5 |
| Software | 1,028.3 |
| Network | 1,074.0 |
| Service Desk | 1,102.4 |
| Openspace | 1,852.8 *(n=1, outlier)* |

**Database** and **Hardware** groups resolve ~150 hrs faster than **Network** and **Service Desk**. Staffing/skill improvements in Network and Service Desk groups would directly reduce cycle times for the bulk of tickets (Network alone accounts for the majority of incidents).

### 3. Priority Escalation Does Not Reliably Accelerate Resolution

| Priority | Avg Resolution (hrs) | n |
|---|---|---|
| 2 - High | 1,019 | 380 |
| 1 - Critical | 1,119 | 79 |
| 3 - Moderate | 1,121 | 41 |

Counter-intuitively, Critical tickets resolve *slower* than High tickets (correlation of urgency score with resolution hours: **r = 0.016**, essentially zero). This suggests that priority labeling is not driving preferential handling. Review of triage and escalation processes is warranted.

### 4. Handoff Avoidance Helps Only for Critical Incidents

Overall, the `no_handoff` flag shows negligible aggregate difference (1,041 hrs with handoff vs. 1,055 hrs without). However, at the **1 - Critical** level, no-handoff tickets resolve in **892 hrs vs. 1,167 hrs**—a **275-hour advantage**. For high-urgency tickets, direct assignment to the right agent from the start is beneficial.

For 2 - High tickets, handoffs show a slight benefit (1,002 vs. 1,087 hrs), suggesting that for moderate-complexity issues, re-routing to a better-skilled agent may outweigh handoff overhead.

### 5. 128 Open/In-Progress Tickets Have No Resolution Time

25.6% of tickets (128/500) remain unresolved (`state` = "New" or "In Progress"). These tickets span all priority levels, with 97 being 2 - High priority. Improving initial assignment accuracy and SLA monitoring for these tickets is needed.

---

## Recommendations

| Priority Action | Expected Impact |
|---|---|
| **Upskill or redistribute load** from Beth Anglin & Fred Luddy | −100–190 hrs per ticket on affected queue |
| **Improve Network & Service Desk group capacity/skill** | −75–150 hrs; largest volume impact |
| **Enforce direct assignment for Critical tickets** (reduce handoffs) | −275 hrs for 1-Critical tier |
| **Audit priority classification** — Critical is not resolving faster than High | Improve SLA compliance, correct process gaps |
| **Monitor 128 stalled tickets** with triage intervention | Prevent backlog compounding |

---

## Caveats

- The `resolution_vs_assignee_avg` column shows most tickets are resolved *below* the per-assignee mean (median: −32 hrs), but the distribution is wide (std: 613 hrs), indicating high variability not explained by assignee alone.
- Assignee performance differences may partially reflect ticket complexity routing rather than pure skill differences.
- The "Openspace" group (n=1, 1,853 hrs) is an extreme outlier and should be investigated separately.
- Category mismatch between `category` and `assignment_group` columns exists in the data (e.g., INC0000000003: category=Software but group=Network), which may inflate resolution times due to misrouting.
