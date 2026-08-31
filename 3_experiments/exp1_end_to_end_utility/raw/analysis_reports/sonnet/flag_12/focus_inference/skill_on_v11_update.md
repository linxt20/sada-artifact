---
dataset: flag_12
scenario: focus_inference
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth analyzing in these incident tickets."
source_table: augment_table/flag_12/focus_inference/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:13:43.388085+00:00
wall_seconds: 47.36
---

# Incident Ticket Analysis Report

## Dataset Overview

- **500 incident tickets** spanning January–early 2023
- **18 columns** covering ticket metadata, classification, asset details, and resolution flags
- Key focus variable: **`self_resolved`** — whether the incident resolved without agent intervention (~19.4% of tickets, n=97)

---

## 1. Ticket Composition

### Category Breakdown
| Category | Count | % of Total |
|---|---|---|
| Hardware | 406 | 81.2% |
| Software | 33 | 6.6% |
| Network | 22 | 4.4% |
| Inquiry / Help | 20 | 4.0% |
| Database | 19 | 3.8% |

Hardware dominates overwhelmingly. Analytical insights here will have the most statistical weight; other categories have small samples and conclusions should be treated cautiously.

### Incident Category (Subcategory)
| Incident Category | Count |
|---|---|
| Printer | 203 (40.6%) |
| Monitor display | 71 (14.2%) |
| Keyboard/mouse/peripheral | 71 (14.2%) |
| Hardware component (HDD, PSU, etc.) | 59 (11.8%) |
| Software | 52 (10.4%) |
| Network connectivity | 25 (5.0%) |
| Database | 19 (3.8%) |

**Printer issues alone account for 40% of all tickets** — a clear concentration worth operational attention.

---

## 2. Priority Distribution

| Priority | Count | % |
|---|---|---|
| 2 - High | 394 | 78.8% |
| 3 - Moderate | 77 | 15.4% |
| 1 - Critical | 27 | 5.4% |
| 4 - Low | 2 | 0.4% |

Nearly 79% of tickets are tagged "High." This near-uniform high-priority labeling reduces the discriminatory power of the priority field for triage or escalation analysis.

---

## 3. Self-Resolution Patterns (Focus Variable)

**Overall self-resolution rate: 19.4%** (97/500 tickets).

### By Category
| Category | Self-Resolved Rate |
|---|---|
| Network | **31.8%** |
| Database | **26.3%** |
| Software | 21.2% |
| Hardware | 18.7% |
| Inquiry / Help | 10.0% |

Network and Database tickets self-resolve at higher rates despite being fewer in number — suggesting transient or environmental issues. Inquiry/Help tickets almost never self-resolve (expected: they require human guidance).

### By Incident Subcategory
| Incident Category | Self-Resolved Rate |
|---|---|
| Network connectivity | **32.0%** |
| Database | **26.3%** |
| Keyboard/mouse/peripheral | 22.5% |
| Monitor display | 18.3% |
| Printer | 17.7% |
| Software | 17.3% |
| Hardware component | 16.9% |

Network connectivity has the highest self-resolution rate — consistent with transient outages resolving on their own.

### By Priority
Self-resolution rates are nearly flat across priority levels (17–22%), suggesting **priority is not a reliable predictor of self-resolution** in this dataset.

---

## 4. Resolution Time

| Self-Resolved | Mean Hours | Max Hours |
|---|---|---|
| False | 180.9 hrs (~7.5 days) | 514 hrs |
| True | 167.9 hrs (~7.0 days) | 502 hrs |

Self-resolved tickets close slightly faster on average, but the difference is small (~13 hours). **Resolution times are long across the board**, regardless of self-resolution status — the bottleneck appears systemic rather than agent-specific.

**Critical tickets do not resolve faster** (mean: 167 hrs) than High priority tickets (180 hrs), which is a notable anomaly worth investigating.

---

## 5. Symptom Types & Software Trigger

- **"not_responding"** is the dominant symptom (268/500, 53.6%) — mostly physical hardware issues
- **"Unknown" symptom type** affects 73 tickets (14.6%) — a data quality gap that limits automated triage
- **`software_trigger = True`** for 54 tickets (10.8%), concentrated in Software category; all have `installation_request` or related symptoms

---

## 6. Workload Distribution

Five agents handle all tickets relatively evenly (85–116 tickets each): Luke Wilson, Howard Johnson, Charlie Whitherspoon, Fred Luddy, Beth Anglin. No single agent is a bottleneck from volume alone.

---

## Key Takeaways for Analysis

| Finding | Actionable Implication |
|---|---|
| Printers = 40% of tickets | Prioritize preventive maintenance or self-service guides for printers |
| Network/DB tickets self-resolve ~30% of the time | Consider auto-hold or watch-and-wait workflow for these categories |
| Priority field is near-uniform (79% "High") | Re-evaluate priority assignment; current labeling adds little signal |
| 73 tickets have "Unknown" symptom type | Improve intake forms to reduce classification gaps |
| Critical tickets resolve no faster than High | Investigate whether escalation paths are being followed |
| Resolution times 7+ days for most tickets | Systemic process review warranted regardless of ticket type |
