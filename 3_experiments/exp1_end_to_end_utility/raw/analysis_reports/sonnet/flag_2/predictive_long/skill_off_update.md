---
dataset: flag_2
scenario: predictive_long
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "resolution_time"
query: "What signals suggest an incident will take longer to resolve?"
source_table: augment_table/flag_2/predictive_long/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:16:22.090552+00:00
wall_seconds: 44.75
---

# Incident Resolution Time — Signal Analysis
**Dataset:** `sonnet__skill_off_update.csv` (500 rows, 372 with resolved `resolution_hours`)  
**Focus variable:** `resolution_hours` (mean ≈ 1,043 h; range 24 – 2,206 h)

---

## Key Signals That Predict Longer Resolution

### 1. Assignment Group / Team (`assignment_group`)
The strongest categorical predictor. Groups with high average resolution times:

| Assignment Group | Avg Resolution (hrs) |
|---|---|
| Openspace | **1,853** |
| Service Desk | 1,102 |
| Network | 1,074 |
| Software | 1,028 |
| Database | 946 |
| Hardware | 926 |

Incidents routed to **Openspace** take ~2× longer than average. *Caution:* Openspace may represent a small or miscategorized group—verify sample size before acting on this outlier.

---

### 2. Assignee's Historical Performance (`assignee_avg_resolution_hours`, r = 0.13)
Incidents assigned to agents with a high historical average resolve notably longer:

| Assignee Avg Quartile | Actual Avg Resolution (hrs) |
|---|---|
| Q1 (fastest historical) | 961 |
| Q2 | 1,036 |
| Q3 | 1,125 |
| Q4 (slowest historical) | **1,142** |

This is the strongest numeric predictor, suggesting agent workload/skill history is actionable for early triage.

---

### 3. After-Hours Opening (`is_afterhours_open`, r = 0.12)
Incidents opened outside business hours take ~16% longer on average:

| Opened After Hours | Avg Resolution (hrs) |
|---|---|
| No | 950 |
| Yes | **1,103** |

Weekend openings show a smaller but consistent effect (+54 hrs on average).

---

### 4. Category (`category`)
Hardware and Network incidents consistently resolve more slowly than Database or Inquiry/Help tickets:

| Category | Avg Resolution (hrs) |
|---|---|
| Hardware | 1,105 |
| Network | 1,079 |
| Software | 1,051 |
| Inquiry / Help | 958 |
| Database | 955 |

---

### 5. Priority (`priority`)
Counterintuitively, **Critical (1)** and **Moderate (3)** incidents take longer than **High (2)**:

| Priority | Avg Resolution (hrs) |
|---|---|
| 3 - Moderate | 1,121 |
| 1 - Critical | 1,119 |
| 2 - High | 1,019 |

The near-equivalence of Critical and Moderate suggests priority assignment may not reliably reflect true urgency, or critical tickets involve more complex coordination despite high attention.

---

### 6. Unassigned Tickets (`is_unassigned`)
65 tickets (13%) are unassigned. **None of these have a recorded `resolution_hours`**, meaning unassigned incidents have no confirmed resolution — a strong proxy for indefinite delays or dropped tickets.

---

## Weak / Absent Signals
- **Description length** (r = −0.07): Very short descriptions (Q1) trend slightly longer, but the effect is weak and non-monotonic.
- **Hour of day opened** (r = −0.06): Negligible linear effect.
- **Priority score** (r = −0.02): Essentially no predictive value on its own.

---

## Summary Decision Table

| Signal | Direction | Strength |
|---|---|---|
| Assignment to Openspace/Service Desk group | ↑ Longer | Strong (categorical) |
| Assignee historical avg (high quartile) | ↑ Longer | Moderate (r = 0.13) |
| After-hours opening | ↑ Longer | Moderate (r = 0.12) |
| Hardware or Network category | ↑ Longer | Moderate |
| Ticket is unassigned | ↑ Unresolved risk | High (100% missing resolution) |
| Priority 1-Critical | ↑ Slightly longer | Weak/unexpected |
