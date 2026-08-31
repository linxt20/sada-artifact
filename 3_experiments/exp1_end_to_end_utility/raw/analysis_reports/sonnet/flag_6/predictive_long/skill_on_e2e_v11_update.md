---
dataset: flag_6
scenario: predictive_long
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "resolution_time"
query: "What signals suggest an agent's tickets will take longer to resolve?"
source_table: augment_table/flag_6/predictive_long/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:20:06.112647+00:00
wall_seconds: 78.12
---

# Signals That Predict Longer Ticket Resolution Times

**Dataset:** 500 tickets (478 closed/resolved used for resolution-time analysis)  
**Outcome variable:** Resolution time in hours = `closed_at` − `opened_at`  
**Overall median resolution time:** 150 h | Mean: 223 h | IQR: 62–248 h

---

## Method Note

TAPP-generated columns used in this report: `incident_category`, `incident_symptom_type`, `affected_scope`, `remote_access_flag`, `cross_agent_resolution_flag`, `assigned_agent`, `opened_hour_of_day`, `opened_day_of_week`. Columns `service_outage_flag`, `ticket_open_status`, and `opened_hour_of_day` / `opened_day_of_week` were evaluated but showed weak or negligible signal and are noted as such below.

---

## 1. Agent Identity — The Dominant Signal

The strongest predictor of long resolution time is **which agent is assigned**.

| Agent | Median Resolution (h) | Mean (h) | Tickets (closed) |
|---|---|---|---|
| **Fred Luddy** | **691** | **750** | 76 |
| Howard Johnson | 129 | 136 | 98 |
| Charlie Whitherspoon | 128 | 119 | 103 |
| Luke Wilson | 123 | 132 | 103 |
| Beth Anglin | 112 | 109 | 98 |

Fred Luddy's median resolution time is **5.4× the overall median** and **6× higher than Beth Anglin**. He also holds 8 of the 22 currently open tickets (`ticket_open_status = True`), the largest backlog of any agent.

Fred's slowness is consistent across all `incident_category` subtypes (median 460–1,258 h vs. 100–218 h for other agents on the same categories), ruling out case-mix as the sole explanation.

---

## 2. Cross-Agent Resolution Involvement (`cross_agent_resolution_flag`)

Tickets flagged as requiring involvement beyond the primary assignee take materially longer.

| cross_agent_resolution_flag | Median (h) | Mean (h) | n |
|---|---|---|---|
| False | 131 | 136 | 168 |
| **True** | **159** | **271** | 310 |

The mean gap (271 h vs. 136 h) is larger than the median gap, indicating that cross-agent tickets produce more extreme outliers. This effect is amplified for Fred Luddy specifically: his cross-agent tickets median **768 h** vs. 312 h for solo tickets — while for other agents the difference is negligible or even reversed (Howard Johnson, Luke Wilson).

---

## 3. Incident Category (`incident_category`) — Semantic Signal

| incident_category | Median (h) | n |
|---|---|---|
| application_software | 218 | 16 |
| printing | 187 | 8 |
| **server** | **178** | 29 |
| **vpn** | **177** | 106 |
| network_connectivity | 153 | 65 |
| database | 131 | 99 |
| email | 123 | 132 |
| wifi | 100 | 14 |
| authentication | 62 | 9 |

VPN and server incidents run ~18–29 h above the overall median. `vpn` is the largest high-risk category (n=106). Application software issues are slowest but low-volume (n=16).

---

## 4. Remote Access Flag (`remote_access_flag`)

| remote_access_flag | Median (h) | Mean (h) | n |
|---|---|---|---|
| False | 145 | 209 | 386 |
| **True** | **177** | **284** | 92 |

Remote-access tickets take **22% longer** at the median and **36% longer** at the mean. This is structurally linked to VPN incidents: 89 of 106 VPN tickets (84%) carry `remote_access_flag = True`. The combination of `remote_access_flag = True` + `cross_agent_resolution_flag = True` yields a median of **187 h** (n=70), the worst cross-factor combination.

---

## 5. Symptom Type (`incident_symptom_type`)

| incident_symptom_type | Median (h) | n |
|---|---|---|
| slow_performance | 595 | 7 |
| install_error | 218 | 8 |
| **cannot_connect** | **163** | 162 |
| not_responding | 162 | 38 |
| unstable_intermittent | 152 | 41 |
| access_denied | 116 | 99 |
| crash_error | 92 | 9 |

`slow_performance` is the most extreme (595 h median) though low-volume. `cannot_connect` is the highest-volume slow symptom (n=162, median 163 h), making it the most impactful from a queue-management standpoint.

---

## 6. Affected Scope (`affected_scope`)

| affected_scope | Median (h) | n |
|---|---|---|
| **individual_user** | **171** | 207 |
| server_system | 137 | 224 |
| department_floor | 121 | 23 |
| organization_wide | 105 | 24 |

Counterintuitively, individual-user tickets take **longer** than organization-wide outages (171 h vs. 105 h). This likely reflects prioritization: organization-wide and department issues receive faster escalation, while individual-user tickets may queue longer.

---

## 7. Weak or Negligible Signals

| Factor | Finding |
|---|---|
| **Priority** | Negligible: 1-Critical median 131 h, 2-High 152 h, 3-Moderate 155 h — gap is small |
| **service_outage_flag** | Reversed (True=139 h vs. False=152 h) — outages appear prioritized |
| **opened_day_of_week** | Weekday 150 h vs. weekend 146 h — no material difference |
| **opened_hour_of_day** | Business/extended/off-hours all ≈149–150 h — no signal |

---

## Summary: Ranked Signals for Long Resolution

| Rank | Signal | Median uplift vs. baseline |
|---|---|---|
| 1 | **Assigned to Fred Luddy** | +541 h (+360%) |
| 2 | **cross_agent_resolution_flag = True** (esp. with Fred) | +28–437 h depending on agent |
| 3 | **incident_symptom_type = slow_performance** | +445 h (low volume) |
| 4 | **remote_access_flag = True** | +32 h |
| 5 | **incident_category = vpn or application_software** | +27–68 h |
| 6 | **affected_scope = individual_user** | +21 h |
| 7 | **incident_category = server** | +28 h |

**Actionable takeaway:** The combination of (1) Fred Luddy assignment + (2) cross_agent_resolution_flag + (3) VPN/remote-access category accounts for the majority of tickets in the extreme right tail of resolution time. Reassigning Fred Luddy's backlog (currently 8 open tickets) and providing targeted support for VPN + cross-agent cases would have the largest measurable impact on resolution time reduction.
