---
dataset: flag_6
scenario: predictive_long
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "resolution_time"
query: "What signals suggest an agent's tickets will take longer to resolve?"
source_table: augment_table/flag_6/predictive_long/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:21:30.903581+00:00
wall_seconds: 50.55
---

# Predictive Analysis: Signals That Lengthen Ticket Resolution Times

**Dataset:** 500 tickets | **Focus variable:** `agent_avg_resolution_hrs`

---

## Key Finding: Bimodal Distribution Dominated by Agent Identity

The resolution time distribution is **not continuous** — it clusters around a small number of discrete values:

| Value (hrs) | Count | Agent |
|-------------|-------|-------|
| 136.31 | 98 | Beth Anglin |
| 150.13 | 103 | Charlie Whitherspoon |
| 159.65 | 100 | Howard Johnson |
| 160.22 | 104 | Luke Wilson |
| **750.00** | **84** | **Fred Luddy** |
| 257.98 | 11 | (mixed) |

> **Each agent has a fixed `agent_avg_resolution_hrs` value.** This means the variable encodes a historical per-agent average, not a per-ticket outcome. Predictions about "longer resolution" effectively reduce to predicting *which agent* will handle the ticket.

---

## Signal 1: Low Agent Workload → Longer Resolution (Strongest Signal)

- **Correlation:** `agent_workload` vs `agent_avg_resolution_hrs` = **−0.33** (the only meaningful numeric predictor)
- Fred Luddy, the slowest agent (750 hrs), has a **fixed workload of 76** — well below the dataset mean of ~85.
- All other agents have workloads in the 85–90 range and resolve tickets 4–5× faster.

> **Rule of thumb:** If `agent_workload < 80`, expect resolution times near **750 hrs**.

---

## Signal 2: Assignment to "Software" or "Database" Groups

| Assignment Group | Mean Avg Resolution (hrs) |
|-----------------|--------------------------|
| Software | 289.2 |
| Database | 263.5 |
| Network | 252.2 |
| Service Desk | 233.4 |
| Hardware | 210.3 |

Software and Database groups are elevated, partly because Fred Luddy handles Network/Database tickets and other slow-resolving agents concentrate there.

---

## Signal 3: Category — Database and Software

| Category | Mean Avg Resolution (hrs) |
|----------|--------------------------|
| Database | 266.0 |
| Software | 258.7 |
| Network | 255.1 |
| Hardware | 220.8 |
| Inquiry / Help | 164.3 |

**"Inquiry / Help"** tickets resolve fastest (~164 hrs). Database and Software tickets take ~60% longer on average.

---

## Weak or Null Signals

| Feature | Correlation | Verdict |
|---------|-------------|---------|
| `priority_numeric` | 0.005 | **Negligible** — priority has almost no effect |
| `opened_hour_of_day` | 0.013 | Negligible |
| `opened_day_of_week` | −0.031 | Negligible |
| `category_avg_resolution_hrs` | 0.054 | Weak |

Priority level (Critical / High / Moderate) does **not** meaningfully predict resolution time in this dataset.

---

## Summary: Decision-Ready Signals

1. **Agent workload below ~80** → ticket is likely assigned to Fred Luddy → expect ~750 hrs resolution time.
2. **Software or Database assignment group** → elevated resolution risk.
3. **"Inquiry / Help" category** → fastest resolution; all other categories carry higher risk.
4. **Priority and timing features are not useful predictors** in this dataset.

> **Caveat:** Because `agent_avg_resolution_hrs` is a fixed per-agent historical average rather than a true per-ticket duration, these signals are proxies for agent identity. The dataset does not contain direct per-ticket resolution durations, which limits causal inference.
