---
dataset: flag_13
scenario: causal_duration
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "resolution_duration_variation"
query: "Why do resolution duration values vary across tickets?"
source_table: augment_table/flag_13/causal_duration/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:11:11.518434+00:00
wall_seconds: 37.77
---

# Why Resolution Duration Values Vary Across Tickets

## Dataset Overview
- **500 tickets** with `resolution_duration_minutes` ranging from **0.18 to 59.95 minutes** (mean ≈ 30.1, std ≈ 16.8).
- Key candidate factors: `assigned_to`, `category`, `priority`, `opened_during_business_hours`, plus engineered columns `assignee_avg_resolution_minutes` and `category_avg_resolution_minutes`.

---

## Factor Analysis

### 1. Assigned Agent (`assigned_to`) — Moderate Effect
Each agent has a consistent, distinct average resolution time, and the `assignee_avg_resolution_minutes` column matches actual per-agent averages precisely:

| Agent | Avg Duration (min) |
|---|---|
| Howard Johnson | 28.78 |
| Beth Anglin | 29.26 |
| Luke Wilson | 30.47 |
| Fred Luddy | 30.69 |
| Charlie Whitherspoon | 31.10 |

The ~2.3-minute spread between the fastest and slowest agent is real but modest. However, the **correlation between `assignee_avg_resolution_minutes` and actual duration is very weak (r ≈ 0.05)**, indicating that agent identity explains only a small fraction of ticket-level variance.

### 2. Category — Small but Consistent Effect
| Category | Avg Duration (min) |
|---|---|
| Inquiry / Help | 28.04 |
| Database | 29.16 |
| Network | 30.08 |
| Hardware | 30.79 |
| Software | 31.55 |

Software and Hardware tickets tend to take slightly longer. Correlation of `category_avg_resolution_minutes` with actual duration is also very weak (r ≈ 0.05), suggesting category contributes systematic but minor differences.

### 3. Priority — Negligible Effect
Priority levels (1 - Critical through 4 - Low) show nearly identical mean durations (~28–31 min). Priority does **not** meaningfully explain duration variation in this dataset.

### 4. Business Hours — Small but Observable Effect
Tickets opened **during business hours** resolve ~2.8 minutes faster on average (28.0 min) compared to those opened outside business hours (30.8 min). This is a consistent directional signal, though the effect size is small.

---

## Key Finding: High Residual Variance

Despite the factors above, the standard deviation (≈16.8 min) is large relative to differences between groups (≈2–3 min). This means the **dominant source of variation is within-group, ticket-level randomness** — potentially reflecting:
- Incident complexity not captured in visible columns (short description content)
- Escalation events or dependencies not recorded
- Individual caller/requester variation

The engineered summary columns (`assignee_avg` and `category_avg`) confirm that agent and category effects exist, but both have near-zero correlations with actual ticket-level duration, reinforcing that they are weak predictors individually.

---

## Summary

Resolution duration varies primarily due to **ticket-level idiosyncratic factors** (complexity, circumstances) rather than any single structural variable. Among observable columns:
- **Assigned agent** and **category** show the clearest (if modest) systematic differences.
- **Business hours** timing provides a small additional signal.
- **Priority** is not a meaningful differentiator in this dataset.

No single factor strongly predicts duration; multi-factor or unobserved explanations account for most of the variance.
