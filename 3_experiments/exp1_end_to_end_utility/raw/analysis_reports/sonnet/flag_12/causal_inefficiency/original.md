---
dataset: flag_12
scenario: causal_inefficiency
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: causal_attribution
focus_variable: "resolution_efficiency"
query: "Why are some incidents resolved inefficiently, and which underlying issues drive it?"
source_table: augment_table/flag_12/causal_inefficiency/original.csv
generated_at: 2026-07-26T13:13:30.326093+00:00
wall_seconds: 132.11
---

# Causal Inefficiency Analysis: Incident Resolution

## Overview

The dataset contains **500 IT incidents** (all resolved or closed), spanning a resolution time range of **24 h – 514 h**. The overall mean resolution time is **178.4 h (~7.4 days)** with a median of **173.2 h**. The 75th-percentile threshold (Q3 = **252.9 h**) is used to classify **124 incidents (25%)** as resolved inefficiently.

---

## Key Metrics

| Metric | Value |
|---|---|
| Total incidents | 500 |
| Mean resolution time | 178.4 h |
| Median resolution time | 173.2 h |
| 75th percentile (Q3) | 252.9 h |
| Inefficient incidents (> Q3) | 124 (25%) |
| Incidents > 400 h | 14 (3%) |

---

## Driver 1: Category / Assignment Group

Incident category is the strongest structural driver of inefficiency:

| Category | n | Mean (h) | Median (h) | % Inefficient |
|---|---|---|---|---|
| Inquiry / Help | 20 | 182.1 | 182.7 | **35%** |
| Hardware | 406 | 181.4 | 175.4 | **26%** |
| Database | 19 | 172.4 | 177.6 | 11% |
| Network | 22 | 161.6 | 186.4 | 18% |
| Software | 33 | 153.6 | 148.0 | 21% |

- **Hardware** dominates in absolute count: it contributes the most inefficient incidents (≈ 105 of 124) simply because it accounts for 81% of all tickets. Its per-incident inefficiency rate (26%) is also above average.
- **Inquiry / Help** has the highest inefficiency rate (35%), suggesting that vaguely categorised or escalation-heavy tickets lack a clear resolution path.
- **Software** resolves fastest on average (153.6 h, 21% inefficient), indicating more structured troubleshooting procedures.
- The Assignment Group distribution mirrors category almost exactly, confirming that group routing is category-driven with no separate structural delay introduced by the group assignment itself.

---

## Driver 2: Individual Agent Load and Performance

Agent assignment is the second major driver:

| Agent | n | Mean (h) | % Inefficient |
|---|---|---|---|
| Luke Wilson | 116 | **195.5** | **33%** |
| Charlie Whitherspoon | 103 | 178.8 | 24% |
| Howard Johnson | 106 | 175.5 | 27% |
| Beth Anglin | 85 | 172.4 | 19% |
| Fred Luddy | 90 | 165.0 | 18% |

**Luke Wilson** stands out: his mean resolution time is 30 h above the overall mean, and one-third of his assigned incidents exceed Q3. He handles the highest volume (116 tickets), suggesting work-overload as a compounding factor. Howard Johnson (27% inefficient) also warrants attention. Fred Luddy and Beth Anglin perform relatively well.

---

## Driver 3: Priority Paradox

Counter-intuitively, **Critical (P1) incidents do not resolve faster** than lower-priority ones:

| Priority | n | Mean (h) | Median (h) | % Inefficient |
|---|---|---|---|---|
| 1 - Critical | 27 | 167.0 | 164.7 | **19%** |
| 2 - High | 394 | 180.0 | 176.6 | 25% |
| 3 - Moderate | 77 | 177.8 | 164.2 | 26% |
| 4 - Low | 2 | 32.6 | 32.6 | 0% |

- Critical incidents do perform better on the inefficiency rate (19%) and average time, but the difference versus High and Moderate is modest — roughly 10–15 h.
- The 2 database-group Critical incidents averaged **393.6 h**, the worst in the entire dataset, showing priority labels are not always honoured in practice.
- The extremely long tail (14 incidents > 400 h) is dominated by **Hardware / High** combinations (11 of 14), not by Critical incidents — indicating priority escalation may not be adequately enforced.

---

## Driver 4: Ticket Handoffs (Closer ≠ Assignee)

- **79% of all incidents** were closed by someone other than the assigned agent.
- Incidents with handoffs averaged **179.4 h** vs **174.8 h** for those without — a modest but consistent 4.6 h premium.
- Handoffs are ubiquitous across categories; they represent a systemic process gap rather than an isolated anomaly, but their individual contribution to delay is small compared to category or agent factors.

---

## Driver 5: Automated vs. Human Update Paths

| sys_updated_by | n | Mean (h) | % Inefficient |
|---|---|---|---|
| system (automated) | 160 | **198.9** | 28% |
| admin | 174 | 173.9 | 23% |
| employee | 166 | 163.4 | 23% |

Incidents whose lifecycle was managed primarily by automated system updates resolve **35 h slower on average** than employee-driven incidents, suggesting that automation-handled tickets may lack active human follow-through.

---

## Exceptions and Weak Evidence

- **Low (P4) incidents** resolved fastest (32.6 h mean) but there are only **2 records** — insufficient for generalisation.
- The **handoff effect is small** (4.6 h gap) and may not be practically significant at the individual ticket level.
- The **Network category** shows a high median (186.4 h) despite a below-average mean (161.6 h), implying a bimodal distribution with some very quick and some very slow resolutions. Sample size is small (n=22).
- No data on escalation history, reassignment count, or wait/work time breakdown is available, limiting attribution of delay to specific phases of the resolution workflow.

---

## Summary of Underlying Issues

| Rank | Issue | Evidence |
|---|---|---|
| 1 | **Hardware ticket volume overload** | 81% of tickets, 26% inefficiency rate, dominates long-tail |
| 2 | **Agent capacity imbalance (Luke Wilson)** | 195.5 h mean, 33% inefficiency, highest volume |
| 3 | **Weak priority enforcement** | Critical incidents only marginally faster; P1 Database avg = 393.6 h |
| 4 | **Inquiry/Help routing ambiguity** | Highest inefficiency rate (35%) with small but consistent pattern |
| 5 | **Automated update paths without active resolution** | System-updated tickets 35 h slower than employee-updated |
| 6 | **Near-universal handoffs** | 79% of tickets closed by non-assignee; small but systemic delay |
