---
dataset: flag_13
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth attention in these incident descriptions."
source_table: augment_table/flag_13/focus_inference/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:15:09.876333+00:00
wall_seconds: 72.51
---

# Incident Description Analysis — What's Worth Attention

**Dataset:** 500 incidents | **Method note:** TAPP-generated columns used: `incident_category`, `problem_nature`, `affected_system_type`, `self_resolved`, `cross_assignment`, `opened_hour_of_day`. The `recurrent_caller` column mirrors `caller_id` exactly (4 unique callers, all recurrent by definition in this dataset) and adds no incremental signal beyond `caller_id`; it is noted but not centered in the analysis.

---

## 1. Priority Distribution — Severity Is Skewed High

| Priority | Count | % |
|---|---|---|
| 2 - High | 391 | 78.2% |
| 1 - Critical | 83 | 16.6% |
| 3 - Moderate | 24 | 4.8% |
| 4 - Low | 2 | 0.4% |

Nearly **95% of all incidents are High or Critical**. The dataset is not a balanced sample of routine work — it is heavily weighted toward serious operational failures.

---

## 2. The Email Outage Signal Is the Single Biggest Alert

`incident_category = email` combined with `problem_nature = outage` is the most concentrated cluster of critical pain:

- **69 of the 88 outage incidents** (78%) are email outages.
- **43 of 83 Critical-priority incidents** (52%) are email incidents — the largest Critical share of any category.
- Example descriptions: *"Email server not responding," "Email server outage," "Email server down"* — near-identical phrasing across many tickets, suggesting a **single recurring platform issue** being logged repeatedly.
- Email incidents have a **cross_assignment rate of 79%** (106/134) and a self-resolution rate of only **21%** (28/134), meaning they consistently require escalation and do not resolve on their own.

> **Decision signal:** The email platform is a chronic, high-severity, high-escalation failure point. It warrants a dedicated root-cause investigation, not per-incident triage.

---

## 3. Database and VPN: High Volume, Persistent Access Problems

| `incident_category` | Count | Critical | `problem_nature` = access_denied (share) | `cross_assignment` rate |
|---|---|---|---|---|
| database | 135 | 20 (15%) | ~65% of db incidents | 78% |
| vpn | 109 | 7 (6%) | connectivity_failure dominant | 83% |
| email | 134 | 43 (52%) | outage dominant | 79% |
| network_connectivity | 72 | 4 (6%) | connectivity_failure dominant | 85% |

**Database** incidents are the largest single category by count (135) and are dominated by `problem_nature = access_denied` — users repeatedly losing access to data stores. The `affected_system_type = server` accounts for 66 of the 118 access_denied incidents overall.

**VPN** (109 incidents) is almost entirely `connectivity_failure` on `network_infrastructure`. Together with `network_connectivity` (72 incidents), network-layer connectivity failures account for **181 tickets**, nearly all resolved via cross-team escalation.

---

## 4. Cross-Assignment Is the Norm, Not the Exception

- **403 of 500 incidents (80.6%) required cross-team assignment** (`cross_assignment = True`).
- `self_resolved = True` and `cross_assignment = True` are **mutually exclusive** in this dataset (0 overlap) — every self-resolved incident was handled within one team.
- `software` (93%) and `hardware` (89%) categories have the highest cross-assignment rates, indicating routing mismatches on initial intake.
- Only **96 incidents self-resolved** (19%), concentrated in database (30), email (28), and "other" (2/5 = 40%).

> **Decision signal:** First-contact resolution is rare. Initial assignment accuracy is weak — especially for software and hardware tickets, which almost always need rerouting.

---

## 5. Outage Incidents Are Uniformly Critical

| `problem_nature` | Count | Critical | High |
|---|---|---|---|
| outage | 88 | 59 (67%) | 29 (33%) |
| connectivity_failure | 229 | 17 (7%) | 203 (89%) |
| access_denied | 118 | 5 (4%) | 109 (92%) |
| crash | 11 | 1 (9%) | 9 (82%) |
| performance_degradation | 11 | 0 | 10 (91%) |

`outage` is the only `problem_nature` value with a majority of Critical incidents. All other natures skew High. **Detecting "outage" language in descriptions is a reliable proxy for Critical priority** — and nearly all outages point to the email system.

---

## 6. Timing: After-Hours Incidents Are as Severe as Business-Hours Ones

| | 1-Critical | 2-High | 3-Moderate |
|---|---|---|---|
| Business hours (06:00–17:59) | 41 | 193 | 12 |
| After hours (18:00–05:59) | 42 | 198 | 12 |

Critical and High incidents split **almost exactly 50/50 across business vs. after-hours** (`opened_hour_of_day`). There is no meaningful concentration of severity in any shift window — on-call coverage needs to be equivalent to daytime staffing given this distribution.

---

## 7. Four Callers Account for 100% of Incidents

All 500 incidents come from only 4 callers: Don Goodliffe (143), Bud Richman (127), ITIL User (117), David Loo (113). The `recurrent_caller` column encodes this but adds no new analytical dimension — every caller is by definition a repeat caller. Each caller has broadly proportional Critical shares (~15–20%), so no single user is driving the severity spike.

---

## Summary: Top Priorities for Attention

| Finding | Evidence | Action Signal |
|---|---|---|
| **Email platform chronic outages** | 43/83 Critical tickets; 69/88 outages; 79% escalation rate | Root-cause fix, not per-ticket response |
| **Database access failures** | 135 tickets, access_denied dominant, 78% escalation | Audit access-control/provisioning pipeline |
| **VPN/network connectivity** | 181 combined tickets, near-total escalation | Infrastructure or capacity review |
| **Routing accuracy is poor** | 80.6% cross-assignment rate; software/hardware worst | Improve intake categorization / triage rules |
| **After-hours coverage parity needed** | 50% of Criticals open after 18:00 | Equal on-call capacity required |
