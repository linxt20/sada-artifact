---
dataset: flag_2
scenario: causal_reduce
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: what_if
focus_variable: "resolution_time"
query: "How can we reduce incident resolution time?"
source_table: augment_table/flag_2/causal_reduce/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:16:52.536787+00:00
wall_seconds: 76.01
---

# Reducing Incident Resolution Time: Analysis Report

**Query:** How can we reduce incident resolution time?  
**Dataset:** 500 incidents | 372 resolved (closed_at populated) | 128 open (`is_open_incident = True`)  
**Resolution time metric:** Hours from `opened_at` to `closed_at`

---

## Key Metrics

| Statistic | Value |
|-----------|-------|
| Median resolution time | **1,032 hours (~43 days)** |
| Mean resolution time | 1,043 hours |
| Min / Max | 24 h / 2,206 h |
| Open (unresolved) incidents | 128 (25.6% of all 500) |

Resolution times are very long across the board, suggesting systemic backlogs rather than isolated outliers. All 372 resolved incidents were assigned (`is_assigned = True`), so assignment coverage alone does not distinguish fast from slow cases.

---

## 1. Assignment Group — Primary Structural Bottleneck

The **Network** group handles 44% of resolved incidents (n=221) and is the slowest group by median:

| Assignment Group | Median Hours | Mean Hours | n |
|-----------------|-------------|-----------|---|
| Database | 960 | 946 | 89 |
| Hardware | 794 | 926 | 4 |
| Software | 823 | 1,028 | 25 |
| Service Desk | 1,129 | 1,102 | 32 |
| **Network** | **1,046** | **1,074** | **221** |

Network also holds the majority of the 128 open incidents (72 of 128). Within the Network group, `incident_category` (TAPP) reveals that **VPN** (median 1,100 h, n=80) and **email** (median 1,104 h, n=69) sub-categories are the slowest, while **network_connectivity** tickets resolve ~20% faster (median 895 h, n=51).

---

## 2. Failure Mode × System Tier — Highest-Impact Combinations

Using TAPP columns `failure_mode` and `affected_system_tier`, the five slowest combinations with ≥5 incidents are:

| Failure Mode | System Tier | Median Hours | n |
|---|---|---|---|
| access_denied | network_infrastructure | **1,738** | 15 |
| unresponsive_service | application | 1,356 | 27 |
| access_denied | application | 1,176 | 13 |
| unresponsive_service | server_side | 1,090 | 37 |
| connection_failure | server_side | 1,054 | 69 |

**Access_denied** incidents on network infrastructure take nearly 1.7× the median. **Unresponsive_service** on application-tier (n=27) is the second-worst cluster — both suggest handoff delays between infrastructure and application teams.

The fastest failure modes are `performance_degradation` (median 366 h, n=2) and `sync_failure` (median 730 h, n=9), though small sample sizes limit confidence.

---

## 3. Agent Performance Varies Substantially

| Agent | Median Hours | Mean Hours | n |
|-------|-------------|-----------|---|
| Luke Wilson | **816** | 967 | 85 |
| Howard Johnson | 910 | 953 | 69 |
| Charlie Whitherspoon | 1,061 | 1,036 | 71 |
| Fred Luddy | 1,100 | 1,125 | 74 |
| Beth Anglin | 1,298 | 1,142 | 73 |

Luke Wilson resolves tickets **37% faster** (median) than Beth Anglin. For **Critical (P1)** incidents specifically, Beth Anglin and Luke Wilson perform best (medians 755 h and 802 h respectively), while Fred Luddy is slowest at 1,392 h median on critical tickets (n=12).

---

## 4. Priority Inversion — Critical Not Resolved Fastest

| Priority | Median Hours | Mean Hours | n |
|----------|-------------|-----------|---|
| 2 - High | 974 | 1,019 | 283 |
| 3 - Moderate | 1,100 | 1,121 | 32 |
| **1 - Critical** | **1,255** | **1,119** | **57** |

Critical incidents have the **highest median resolution time** — a clear process gap. P1 incidents may be harder, but the 1,255-hour median suggests escalation paths or staffing for critical incidents need improvement.

---

## 5. Recurrence Signal — Most Tickets Are Repeat Issues

`recurrence_signal = True` for **337 of 372 resolved incidents (91%)**, versus only 35 non-recurring. Median resolution for recurring vs. non-recurring is 1,046 h vs. 888 h respectively (non-recurring resolves ~15% faster). The overwhelming prevalence of recurring incidents indicates that root-cause fixes are not being applied — repeat tickets accumulate and compete for agent capacity.

---

## 6. Open Incident Backlog

128 open incidents (`is_open_incident = True`), breakdown:
- **Priority:** 97 High, 22 Critical, 9 Moderate
- **Category:** 72 Network, 30 Database, 16 Software
- **Failure mode:** connection_failure (67), access_denied (27), crash_or_outage (13)

The 22 open Critical incidents represent an immediate risk. Connection failures (67 open) align with the Network group bottleneck identified above.

---

## 7. Resolved-by-Assignee Rate

`resolved_by_assignee = True` for only **73 of 372 resolved incidents (20%)**, meaning 80% were closed by someone other than the assigned agent. This suggests widespread reassignment or closure by supervisors, which inflates resolution time and obscures ownership accountability.

---

## Prioritized Recommendations

| Priority | Action | Supporting Evidence |
|----------|--------|---------------------|
| 🔴 High | Focus Network group capacity on VPN and email sub-categories | Network = 221 resolved (44%), VPN+email median ≥1,100 h |
| 🔴 High | Fix P1 escalation path — Critical tickets take longest | P1 median 1,255 h vs. P2 median 974 h |
| 🔴 High | Resolve 22 open Critical incidents immediately | 22 open P1 incidents with no `closed_at` |
| 🟠 Medium | Address access_denied + unresponsive_service root causes | Median 1,738 h and 1,356 h respectively; likely missing IAM/provisioning process |
| 🟠 Medium | Share practices from Luke Wilson across agents | 37% faster median than slowest agent |
| 🟠 Medium | Increase `resolved_by_assignee` rate (currently 20%) | Reassignment/handoffs inflate resolution time |
| 🟡 Lower | Implement known-issue KB articles for top recurring failure modes | 91% of tickets flagged `recurrence_signal = True` |

---

## Method Note

**TAPP-generated columns used in this report:** `incident_category`, `failure_mode`, `affected_system_tier`, `recurrence_signal`, `is_assigned`, `resolved_by_assignee`, `is_open_incident`.  

Columns `assigned_agent` and `caller_id_group` were reviewed but were redundant with `assigned_to` and `caller_id` respectively and added no new signal. All TAPP-column findings were cross-checked against original structured fields (`priority`, `category`, `assignment_group`, `assigned_to`, `opened_at`, `closed_at`).
