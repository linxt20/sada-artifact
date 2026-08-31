---
dataset: flag_6
scenario: concept_attribute_workload
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "agent_workload_burden"
query: "What kinds of tickets create heavier agent workload?"
source_table: augment_table/flag_6/concept_attribute_workload/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:19:47.050757+00:00
wall_seconds: 73.58
---

# Agent Workload Analysis: What Kinds of Tickets Create Heavier Agent Workload?

**Dataset:** 500 IT service management incidents  
**Workload proxy:** Resolution time in hours (closed/resolved tickets, n = 478); open/active ticket count (n = 22)  
**Method note:** TAPP-generated columns used in this report: `incident_category`, `failure_mode`, `affected_system_type`, `scope_indicator`, `recurrence_pattern`, `self_resolved`. The `requires_escalation` column had zero positive values in the dataset (all False) and therefore provided no analytical signal; it is excluded from substantive claims.

---

## 1. Overall Workload Baseline

| Metric | Value |
|---|---|
| Total tickets | 500 |
| Closed / Resolved | 478 (95.6%) |
| Still open (New / In Progress) | 22 (4.4%) |
| Mean resolution time | 223 hrs |
| Median resolution time | 150 hrs |

---

## 2. Workload by Original Category and Priority

**Category** is the strongest structured driver of resolution time.

| Category | Mean hrs | Median hrs | n |
|---|---|---|---|
| Software | **248** | 150 | 70 |
| Network | 231 | 162 | 271 |
| Database | 204 | 131 | 103 |
| Hardware | 187 | 113 | 26 |
| Inquiry / Help | 135 | 143 | 8 |

Software and Network tickets impose the highest workload per ticket. Network also accounts for the largest share of open tickets (13 of 22 still active).

**Priority** shows a counter-intuitive pattern: lower-priority tickets take longer.

| Priority | Mean hrs | Median hrs | n |
|---|---|---|---|
| 3 - Moderate | 247 | 155 | 30 |
| 2 - High | 230 | 152 | 364 |
| 1 - Critical | 188 | 131 | 84 |

Critical tickets are resolved fastest, consistent with triage urgency. Moderate-priority tickets linger, accumulating passive agent burden.

---

## 3. Failure Mode (`failure_mode`) — Strongest TAPP Signal

`failure_mode` sharply differentiates workload intensity beyond category alone.

| Failure Mode | Mean hrs | Median hrs | n |
|---|---|---|---|
| slow_performance | **664** | 595 | 7 |
| error_message | 274 | 132 | 30 |
| disconnection | 242 | 163 | 134 |
| Unknown | 238 | 174 | 16 |
| intermittent | 220 | 152 | 43 |
| sync_failure | 204 | 99 | 12 |
| crash_outage | 202 | 140 | 110 |
| no_access | 188 | 134 | 125 |

**`slow_performance`** is an extreme outlier (664 hrs mean, 595 hrs median) — nearly 3× the dataset mean. These are likely chronic degradation issues with no clean resolution path. Within Software specifically, `crash_outage` and `error_message` failures average 294 hrs and 244 hrs respectively.

---

## 4. Affected System Type (`affected_system_type`)

| Affected System Type | Mean hrs | Median hrs | n |
|---|---|---|---|
| file_share | **535** | 262 | 4 |
| endpoint_device | 376 | 225 | 20 |
| web_application | 275 | 275 | 2 |
| vpn_gateway | 268 | 177 | 106 |
| database_server | 208 | 131 | 99 |
| network_infrastructure | 201 | 150 | 75 |
| email_server | 190 | 123 | 132 |
| application_server | 189 | 139 | 40 |

`file_share` and `endpoint_device` tickets carry the highest mean resolution times. VPN gateway issues (n = 106, mean 268 hrs) represent the largest high-workload volume segment.

---

## 5. Incident Category (`incident_category`) — Sub-category Detail

| Incident Category | Mean hrs | Median hrs | n |
|---|---|---|---|
| file_share | 535 | 262 | 4 |
| application_software | **409** | 220 | 17 |
| vpn_access | 267 | 177 | 107 |
| server_connectivity | 210 | 175 | 30 |
| network_wifi | 209 | 126 | 34 |
| database | 208 | 131 | 99 |
| internet_connectivity | 194 | 163 | 41 |
| email | 190 | 123 | 132 |
| other | 154 | 94 | 14 |

`application_software` (17 tickets, mean 409 hrs) and `vpn_access` (107 tickets, mean 267 hrs) are the highest-burden sub-categories. Email incidents dominate by volume (132 tickets) but resolve faster than average.

---

## 6. Scope Indicator (`scope_indicator`)

| Scope | Mean hrs | Median hrs | n |
|---|---|---|---|
| remote_access | **284** | 177 | 92 |
| single_user | 226 | 162 | 104 |
| production_system | 207 | 137 | 262 |
| department_wide | 193 | 99 | 11 |
| floor_location | 100 | 86 | 9 |

**Remote-access-scoped tickets** require 37% more time than the overall median. Within Network tickets alone, remote-access scope averages 290 hrs vs. 69–108 hrs for floor/department scopes.

---

## 7. Recurrence Pattern (`recurrence_pattern`)

| Recurrence | Mean hrs | Median hrs | n |
|---|---|---|---|
| systemic_outage | **288** | 293 | 5 |
| isolated | 232 | 146 | 111 |
| repeat_same_system | 220 | 150 | 362 |

Systemic outages have the highest mean but small sample (n = 5). Repeat-same-system tickets dominate volume (362 tickets, 76% of closed set), representing chronic recurring burden.

---

## 8. Self-Resolution (`self_resolved`) — Limited Workload Differentiation

Tickets marked `self_resolved = True` (n = 99, 21%) show nearly identical resolution times (median 162 hrs) compared to non-self-resolved tickets (median 148 hrs). Self-resolution rate is highest for Inquiry/Help (62.5%) and lowest for Network (17.7%). This column does not meaningfully reduce measured agent workload time in this dataset.

---

## 9. Composite Profile of High-Workload Tickets

Combining evidence from original structured fields and TAPP-generated columns, the highest-burden tickets share the following profile:

| Driver | High-Workload Value | Evidence |
|---|---|---|
| `category` | Software, Network | Mean 248 hrs, 231 hrs; 13 open Network tickets |
| `failure_mode` | slow_performance, error_message | Mean 664 hrs, 274 hrs |
| `affected_system_type` | endpoint_device, vpn_gateway | Mean 376 hrs, 268 hrs |
| `incident_category` | application_software, vpn_access | Mean 409 hrs, 267 hrs |
| `scope_indicator` | remote_access | Mean 284 hrs |
| `priority` | 2 - High or 3 - Moderate | Longer tail vs. Critical |
| `recurrence_pattern` | repeat_same_system | 76% of volume; chronic load |

---

## 10. Key Findings

1. **Software tickets with slow-performance or crash/error failure modes are the heaviest per-ticket burden** (avg. 248–664 hrs depending on failure mode).
2. **VPN and remote-access incidents** (vpn_access + remote_access scope) combine high frequency (107 tickets) with high resolution time (267 hrs), making them the largest aggregate workload driver.
3. **Email tickets are high volume (132 closed) but relatively fast** (190 hrs mean), making them operationally manageable.
4. **Repeat-same-system recurrence dominates ticket volume** (76%), indicating unresolved root causes generate chronic agent load rather than isolated spikes.
5. **Endpoint device tickets** (mean 376 hrs) warrant proactive attention despite low volume (n = 20).
