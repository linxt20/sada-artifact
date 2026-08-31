---
dataset: flag_6
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth analyzing in these incident tickets."
source_table: augment_table/flag_6/focus_inference/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:20:27.062555+00:00
wall_seconds: 103.59
---

# Incident Ticket Analysis Report

**Dataset:** 500 incident tickets, January 2023 – January 2024  
**Method note:** TAPP-generated columns used in this analysis: `affected_component`, `symptom_type`, `scope_indicator`, `self_resolved`, `recurrence_signal`, `remote_access_context`. These supplement original structured columns (`priority`, `category`, `assignment_group`, `assigned_to`, `state`, `opened_at`, `closed_at`).

---

## 1. Dataset at a Glance

| Dimension | Value |
|---|---|
| Total tickets | 500 |
| Closed / Resolved | 478 (95.6%) |
| Open (New / In Progress) | 22 (4.4%) |
| Date range | Jan 2023 – Jan 2024 |
| Median resolution time | **150 hours (~6.3 days)** |
| Mean resolution time | 223 hours (right-skewed by outliers) |

Volume is stable month-to-month (32–48 tickets/month) — no obvious seasonal spike requiring attention.

---

## 2. What Drives Ticket Volume

**Category** is the primary driver of volume, with Network dominant:

| Category | Tickets | % of Total |
|---|---|---|
| Network | 284 | 56.8% |
| Database | 109 | 21.8% |
| Software | 72 | 14.4% |
| Hardware | 26 | 5.2% |
| Inquiry / Help | 9 | 1.8% |

TAPP's `affected_component` disaggregates this further into actionable targets:

| Affected Component | Tickets | Top Symptom (`symptom_type`) |
|---|---|---|
| email_server | 136 | outage_down (92 tickets) |
| vpn_gateway | 110 | connectivity_failure (92 tickets) |
| database_server | 105 | access_denied (48), connectivity_failure (34) |
| lan_network | 69 | connectivity_failure (51) |
| application | 21 | Unknown (9) |

The **email_server + vpn_gateway pair accounts for 246/500 tickets (49.2%)** — nearly half of all work.

---

## 3. Priority and Severity

| Priority | Tickets | % | Median Resolution (hrs) |
|---|---|---|---|
| 1 - Critical | 88 | 17.6% | 131 |
| 2 - High | 379 | 75.8% | 152 |
| 3 - Moderate | 33 | 6.6% | 155 |

**Counterintuitively, Critical tickets resolve faster (131 hrs) than High or Moderate.** This likely reflects escalation urgency rather than lower complexity.

Critical tickets are overwhelmingly infrastructure-wide (`scope_indicator = infrastructure_wide`: 76/88, 86%) and driven by `symptom_type = outage_down` (59/88, 67%), concentrated on **email_server** (46 tickets) and **database_server** (23 tickets). These are the highest-impact events to monitor.

---

## 4. Scope and Blast Radius

`scope_indicator` classifies impact breadth:

| Scope | Tickets | Median Resolution (hrs) |
|---|---|---|
| individual_user | 249 | 152 |
| infrastructure_wide | 227 | 147 |
| team_department_floor | 24 | 110 |

Individual-user and infrastructure-wide tickets have similar median resolution times, suggesting the team does not systematically prioritize broad-impact incidents over user-level issues. The 76 **Critical + infrastructure_wide** tickets (centered on email_server and database_server) represent the most operationally significant cluster.

---

## 5. Resolution Time: What Slows Tickets Down

**By symptom type** (TAPP `symptom_type`):

| Symptom Type | Tickets | Median Resolution (hrs) |
|---|---|---|
| slow_performance | 7 | **595** |
| connectivity_failure | 218 | 163 |
| outage_down | 113 | 138 |
| access_denied | 105 | 116 |
| error_message | 17 | 113 |
| sync_failure | 12 | 99 |
| crash | 4 | 14 |

`slow_performance` tickets are a clear outlier — only 7 tickets but median 595 hours (~25 days), nearly 4× the overall median. These deserve investigation.

**By category:**

| Category | Median Resolution (hrs) |
|---|---|
| Hardware | 113 |
| Database | 131 |
| Software | 150 |
| Inquiry/Help | 143 |
| Network | 162 |

Network tickets take longest on median, consistent with high vpn_gateway/connectivity_failure volume.

---

## 6. Assignee Performance and Workload

Workload is evenly distributed across 5 agents (~84–104 tickets each), with one outlier:

| Assignee | Tickets | Median Resolution (hrs) |
|---|---|---|
| Beth Anglin | 98 | **112** |
| Luke Wilson | 103 | 123 |
| Charlie Whitherspoon | 103 | 128 |
| Howard Johnson | 98 | 129 |
| **Fred Luddy** | **84** | **691** |

**Fred Luddy's median resolution time is ~5.5× higher than peers.** This is not explained by category mix alone (he handles mostly Network tickets, same as others). His 4 `slow_performance` tickets have resolutions of 595–1,430 hours, which heavily inflate his median, but even excluding those, his median is 679 hours — still dramatically higher than others. Fred also holds **8 of the 22 currently open tickets** (36%), making him the top bottleneck for unresolved work.

---

## 7. TAPP Semantic Facets: Signal Strength Assessment

| TAPP Column | Signal Quality | Key Finding |
|---|---|---|
| `affected_component` | **Strong** — adds sub-category detail absent from raw `category` | email_server and vpn_gateway dominate volume |
| `symptom_type` | **Strong** — differentiates resolution difficulty | slow_performance tickets are resolution outliers |
| `scope_indicator` | **Moderate** — maps to priority well but resolution time difference is small | Critical = 86% infrastructure_wide |
| `remote_access_context` | **Moderate** — 92 tickets flagged; all are vpn_gateway/Network, all 2-High; adds 32 hrs to median resolution (177 vs 145) | Remote-access VPN tickets are a coherent slow-to-resolve cluster |
| `self_resolved` | **Weak** — 21% of tickets flagged True, but self-resolved tickets actually take *longer* (162 vs 148 hrs median), suggesting the label reflects eventual user workaround rather than quick auto-resolution |
| `recurrence_signal` | **Weak as differentiator** — 94.4% of tickets flagged True; Network (100%), Database (99%), Inquiry/Help (100%) are saturated. Only Hardware (77%) and Software (72%) show meaningful non-recurrence. The near-universal flag makes it uninformative for most categories |

---

## 8. Open / Unresolved Tickets (22 tickets — immediate action)

| Priority | Count |
|---|---|
| 1 - Critical | 4 |
| 2 - High | 15 |
| 3 - Moderate | 3 |

- 13 of 22 open tickets are **Network** category; 6 are **Database**
- **Fred Luddy holds 8** open tickets vs. 2 (Howard Johnson) and 1 (Luke Wilson) for all others
- The 4 open Critical tickets warrant immediate escalation review

---

## 9. Key Analytical Priorities (Summary)

| Priority | What to Analyze / Act On |
|---|---|
| 🔴 High | **Fred Luddy's resolution backlog** — 691-hr median, 8 open tickets; investigate capacity, skill gaps, or reassignment need |
| 🔴 High | **email_server outage_down + Critical/infrastructure_wide cluster** — 46 Critical email tickets; assess whether root cause is recurring (high `recurrence_signal`) |
| 🟠 Medium | **VPN gateway (110 tickets, 92 remote-access flagged)** — remote_access_context correlates with +32 hrs resolution; evaluate VPN infrastructure reliability |
| 🟠 Medium | **slow_performance symptom type** — 7 tickets, 595-hr median; disproportionate resolution drag; likely needs escalation path |
| 🟡 Low | **self_resolved and recurrence_signal** — both TAPP columns have limited discriminating power in this dataset; do not center further analysis on them |
