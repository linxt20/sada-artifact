---
dataset: flag_2
scenario: predictive_long
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "resolution_time"
query: "What signals suggest an incident will take longer to resolve?"
source_table: augment_table/flag_2/predictive_long/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:17:21.289515+00:00
wall_seconds: 64.56
---

# Incident Resolution Time: Predictive Signals Analysis

**Dataset:** `sonnet__skill_on_v11_update.csv` — 500 incidents, 372 with computable resolution times  
**Focus variable:** Resolution hours (elapsed time from `opened_at` to `closed_at`)  
**Distribution:** Median **1,032 hours (~43 days)**, range 24–2,206 hours

---

## 1. Strongest Signal: Assignment Lag

`assignment_lag` (boolean) is the single most predictive column, with a Pearson correlation of **r = 0.856** against resolution hours.

| Assignment Lag | Median Resolution | Mean Resolution | Count |
|---|---|---|---|
| **False** (no lag) | 485 hours (~20 days) | 483 hours | 175 |
| **True** (lag present) | **1,486 hours (~62 days)** | 1,541 hours | 197 |

Incidents where assignment was delayed resolve in ~3× more time. This is the clearest operational lever: **any incident that is not immediately assigned is at high risk of extended resolution.**

---

## 2. Assigned Agent

Agent-level median resolution times vary substantially:

| Agent | Median Hours | Count |
|---|---|---|
| Beth Anglin | **1,298** | 73 |
| Fred Luddy | **1,100** | 74 |
| Charlie Whitherspoon | 1,061 | 71 |
| Howard Johnson | 910 | 69 |
| Luke Wilson | 816 | 85 |

Incidents assigned to **Beth Anglin** take ~60% longer to resolve than those assigned to **Luke Wilson**. This pattern is consistent and may reflect workload, skill alignment, or ticket complexity routing.

---

## 3. Incident Category & Failure Mode

| Incident Category | Median Hours |
|---|---|
| server | **1,162** |
| email | **1,100** |
| vpn | **1,100** |
| database | 960 |
| network | 895 |
| hardware_peripheral | 794 |

**Server, email, and VPN incidents** consistently take longer. On failure mode:

| Failure Mode | Median Hours |
|---|---|
| service_outage | **1,111** |
| Unknown | **1,090** |
| connection_failure | 1,043 |
| authentication_failure | 809 |
| sync_failure | 730 |
| performance_degradation | 366 |

`service_outage` and `Unknown` failure modes are associated with longer resolution. **Unknown** is notable — incidents where the failure mode is not categorized upfront trend toward the longest tails.

---

## 4. Assignment Group

| Assignment Group | Median Hours | Count |
|---|---|---|
| Service Desk | **1,129** | 32 |
| Network | **1,046** | 221 |
| Database | 960 | 89 |
| Software | 823 | 25 |
| Hardware | 794 | 4 |

**Service Desk** and **Network** group tickets take longer on average. Service Desk likely acts as a triage layer, adding handoff delays.

---

## 5. Priority

Priority shows a **weak and non-monotonic** relationship with resolution time:

| Priority | Median Hours | Count |
|---|---|---|
| 1 - Critical | **1,255** | 57 |
| 3 - Moderate | 1,100 | 32 |
| 2 - High | 974 | 283 |

Surprisingly, **Critical incidents take longest**, which may reflect complexity rather than mismanagement — or that critical incidents involve harder problems. Priority alone is not a reliable predictor; it should be combined with other signals.

---

## 6. Scope Indicator

| Scope | Median Hours |
|---|---|
| remote_access | **1,097** |
| server_side | **1,068** |
| individual_user | 920 |
| location_specific | 686 |
| department_wide | 46 |

`remote_access` and `server_side` scopes trend longer. Notably, `department_wide` incidents resolve fastest (median ~46 hours, n=3) — likely due to escalation urgency — but the sample is too small to generalize.

---

## 7. Caller Type

| Caller Type | Median Hours | Count |
|---|---|---|
| itil_user | **1,090** | 79 |
| named_user | 989 | 293 |

ITIL users (internal IT staff raising tickets) are associated with ~10% longer resolution times. This is a weak signal and may reflect that ITIL-raised tickets tend to be more complex back-end issues.

---

## Summary: Decision-Ready Signal Ranking

| Signal | Strength | Direction |
|---|---|---|
| **Assignment lag = True** | ⭐⭐⭐⭐⭐ (r=0.856) | Strong increase |
| **Assigned agent** (Beth Anglin / Fred Luddy) | ⭐⭐⭐⭐ | Moderate–large increase |
| **Incident category**: server, email, VPN | ⭐⭐⭐ | Moderate increase |
| **Failure mode**: service_outage, Unknown | ⭐⭐⭐ | Moderate increase |
| **Assignment group**: Service Desk, Network | ⭐⭐ | Moderate increase |
| **Priority = 1 - Critical** | ⭐⭐ | Moderate increase (non-monotonic) |
| **Scope**: remote_access, server_side | ⭐⭐ | Moderate increase |
| **Caller type = itil_user** | ⭐ | Weak increase |

---

## Caveats

- 128 of 500 records (26%) have no resolvable `closed_at` timestamp and are excluded from all statistics — these open/in-progress tickets may represent the longest-running cases and would skew estimates further upward.
- The `department_wide` scope result (very fast) is based on only 3 records and should not be operationalized.
- Priority's non-linear relationship with resolution time means it should not be used in isolation.
