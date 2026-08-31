---
dataset: flag_6
scenario: concept_attribute_workload
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "agent_workload_burden"
query: "What kinds of tickets create heavier agent workload?"
source_table: augment_table/flag_6/concept_attribute_workload/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:19:25.527449+00:00
wall_seconds: 52.93
---

# Agent Workload Analysis — Incident Ticket Dataset

**Date:** 2026-07-30 | **Records:** 500 tickets

---

## Workload Indicators

The dataset contains four binary workload signals:

| Indicator | Overall Rate |
|---|---|
| `cross_agent_resolution` | 79.1% |
| `recurrence_signal` | 76.6% |
| `long_running_ticket` | 13.2% |
| `ticket_open_unresolved` | 4.4% |

A composite **workload score** (0–4, sum of all four flags) is used to rank ticket dimensions below.

---

## 1. By Category

| Category | Count | Long-Running | Cross-Agent | Recurrence | Avg Score |
|---|---|---|---|---|---|
| **Database** | 109 | 13.6% | 78.6% | 84.4% | **1.77** |
| **Network** | 284 | 13.3% | 82.3% | 77.1% | **1.73** |
| Hardware | 26 | 7.7% | 76.9% | 84.6% | 1.69 |
| Software | 72 | 15.7% | 72.9% | 61.1% | 1.50 |
| Inquiry/Help | 9 | 0.0% | 37.5% | 66.7% | 1.11 |

**Database** and **Network** tickets impose the heaviest workload. Network tickets most commonly require cross-agent handoffs (82.3%), while Database tickets have the highest recurrence rate (84.4%). Software tickets are notably lighter on recurrence. Inquiry/Help tickets are by far the lowest-burden category.

---

## 2. By Priority

| Priority | Count | Long-Running | Cross-Agent | Recurrence | Avg Score |
|---|---|---|---|---|---|
| **1 - Critical** | 88 | 8.3% | 85.7% | 86.4% | **1.81** |
| 2 - High | 379 | 13.5% | 77.7% | 75.2% | 1.67 |
| 3 - Moderate | 33 | 23.3% | 76.7% | 66.7% | 1.67 |

**Critical tickets** drive the highest workload score primarily through cross-agent involvement and recurrence. Interestingly, **Moderate tickets** have the highest long-running rate (23.3%), suggesting they linger without urgency escalation — a less visible but real drain on agent capacity.

---

## 3. By Incident Category

| Incident Category | Count | Long-Running | Cross-Agent | Recurrence | Avg Score |
|---|---|---|---|---|---|
| printing | 8 | 12.5% | 87.5% | 87.5% | **1.88** |
| **vpn_connectivity** | 110 | 15.1% | 81.1% | 80.0% | **1.76** |
| **database_access** | 105 | 13.1% | 78.8% | 83.8% | **1.76** |
| server_access | 32 | 12.9% | 83.9% | 78.1% | 1.75 |
| email_system | 135 | 9.1% | 78.8% | 84.4% | 1.73 |
| software_update | 10 | 33.3% | 88.9% | 50.0% | 1.70 |
| network_internet | 82 | 13.2% | 76.3% | 67.1% | 1.57 |
| authentication_login | 10 | 22.2% | 77.8% | 10.0% | 1.10 |
| other | 8 | 25.0% | 50.0% | 0.0% | 0.75 |

**VPN connectivity**, **database access**, and **email system** tickets are the highest-volume and high-workload incident types. `software_update` tickets show the highest long-running rate (33.3%). `authentication_login` tickets have very low recurrence (10%), limiting their overall burden despite some duration. The `printing` category has high cross-agent and recurrence rates but the sample is too small (n=8) to draw firm conclusions.

---

## 4. By Problem Nature

| Problem Nature | Count | Long-Running | Cross-Agent | Recurrence | Avg Score |
|---|---|---|---|---|---|
| **performance_degradation** | 13 | 46.2% | 84.6% | 46.2% | **1.77** |
| sync_error | 12 | 8.3% | 75.0% | 91.7% | 1.75 |
| **connectivity_failure** | 214 | 14.4% | 79.2% | 78.5% | **1.72** |
| service_down_outage | 114 | 8.3% | 84.4% | 78.9% | 1.72 |
| crash_error | 32 | 18.8% | 68.8% | 81.2% | 1.69 |
| access_denied | 105 | 10.9% | 75.2% | 75.2% | 1.62 |

**Performance degradation** tickets have the highest long-running rate (46.2%) — these are difficult to resolve quickly. **Connectivity failures** dominate by volume (214 tickets) and maintain high workload scores. **Service outages** drive the most cross-agent collaboration (84.4%).

---

## 5. By Scope

| Scope | Count | Long-Running | Cross-Agent | Recurrence | Avg Score |
|---|---|---|---|---|---|
| **system_wide** | 185 | 11.4% | 82.1% | 96.8% | **1.90** |
| individual_user | 216 | 11.4% | 77.7% | 84.3% | 1.74 |
| department_wide | 11 | 9.1% | 72.7% | 81.8% | 1.64 |

**System-wide tickets** are clearly the heaviest: their recurrence rate of 96.8% is the highest of any dimension value, and they require the most cross-agent involvement. This makes scope one of the strongest workload predictors. Note: "Unknown" scope tickets (n=74) show artificially low recurrence due to missing data.

---

## Key Findings Summary

| Factor | Heaviest Workload Type | Primary Driver |
|---|---|---|
| **Category** | Database, Network | Cross-agent resolution + recurrence |
| **Priority** | Critical | Cross-agent + recurrence; Moderate tickets linger longest |
| **Incident Type** | VPN connectivity, Database access, Email system | High volume + dual-signal workload |
| **Problem Nature** | Performance degradation | Long duration (46% long-running) |
| **Scope** | System-wide | Near-universal recurrence (97%) |

> **Decision note:** Workload is dominated by `cross_agent_resolution` (79% overall) and `recurrence_signal` (77%), meaning most tickets inherently involve multiple agents and repeat. The most actionable differentiation lies in **scope** (system-wide vs. individual) and **incident type** (VPN/database/email vs. authentication/inquiry). Targeting preventive measures at system-wide connectivity and database access tickets would address the highest-burden segment by combined volume and workload intensity.
