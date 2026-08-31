---
dataset: flag_12
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth analyzing in these incident tickets."
source_table: augment_table/flag_12/focus_inference/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:14:17.002988+00:00
wall_seconds: 71.77
---

# Incident Ticket Analysis Report

## Executive Summary

The dataset contains **500 IT incident tickets** opened between January 2023 and January 2024, all either Closed (256, 51%) or Resolved (244, 49%). The tickets are overwhelmingly hardware-centric and exhibit high repeat rates. The most analytically productive dimensions are: (1) volume concentration in printer/hardware failures, (2) resolution time variation by assignee and failure type, (3) the repeat-incident pattern, and (4) critical-ticket composition.

**Method note:** TAPP-generated columns used in this report — `incident_category`, `failure_type`, `resolution_action_type`, `self_resolved`, `is_repeat_incident_type`, `urgency_signal` — supplement original structured columns (`category`, `priority`, `state`, `assigned_to`, `opened_at`, `closed_at`).

---

## 1. What's in the Ticket Population

| Original `category` | Count | % |
|---|---|---|
| Hardware | 406 | 81% |
| Software | 33 | 7% |
| Network | 22 | 4% |
| Inquiry / Help | 20 | 4% |
| Database | 19 | 4% |

TAPP `incident_category` refines the hardware bucket: **printers alone account for 203 tickets (41%)**, followed by monitor/display (71, 14%), keyboard (56, 11%), and hardware component (56, 11%). Software (52, 10%), network connectivity (24, 5%), and database (19, 4%) are minor by volume.

**Priority is skewed high:** 394 tickets (79%) are "2 - High," 27 (5%) are "1 - Critical," and only 77 (15%) are "3 - Moderate." The two "4 - Low" tickets are statistical noise.

Volume is stable across months (~33–46 tickets/month), with no clear trend—ruling out a seasonal spike as a key driver.

---

## 2. Resolution Time: Where Time Is Lost

Overall median resolution time is **173 hours (~7.2 days)**; the mean is 178 hours (std 109 h), indicating right skew.

**Priority does not meaningfully differentiate resolution speed**, which is a notable finding:

| Priority | Median hours | Count |
|---|---|---|
| 1 - Critical | 165 | 27 |
| 2 - High | 177 | 394 |
| 3 - Moderate | 164 | 77 |
| 4 - Low | 33 | 2 |

Critical tickets resolve slightly *faster* than High, but the gap is small (~12 h). Priority is not a reliable predictor of resolution speed in this dataset.

**`failure_type` explains more variation than priority:**

| `failure_type` | Median hours | Count |
|---|---|---|
| not_responding_unresponsive | 183 | 144 |
| service_failure | 182 | 154 |
| physical_damage | 173 | 55 |
| connectivity_failure | 168 | 44 |
| installation_failure | 155 | 38 |
| performance_degradation | 151 | 48 |
| crash_freeze | 103 | 9 |

Unresponsive and service-failure modes—which together account for 60% of all tickets—take ~30 hours longer than crash/freeze incidents. This suggests the "hard to diagnose" failures are a backlog driver.

**Assignee efficiency varies meaningfully:**

| Assigned to | Median hours | Volume |
|---|---|---|
| Howard Johnson | 163 | 106 |
| Beth Anglin | 165 | 85 |
| Charlie Whitherspoon | 168 | 103 |
| Fred Luddy | 170 | 90 |
| Luke Wilson | 195 | 116 |

Luke Wilson handles the most tickets (116) but has the slowest median resolution—32 hours above Howard Johnson. This workload-efficiency mismatch is worth investigating for load-balancing or support.

---

## 3. Repeat Incidents: A Structural Problem

**90% of tickets (452/500) are flagged `is_repeat_incident_type = True`**, meaning the incident type has been seen recurrently. Only 48 tickets (10%) are novel failure modes.

By `incident_category`, repeat rate is uniformly high:

| `incident_category` | Repeat rate | Count |
|---|---|---|
| printer | 100% | 203 |
| peripheral_other | 89% | 19 |
| keyboard | 88% | 56 |
| software | 88% | 52 |
| monitor_display | 83% | 71 |
| network_connectivity | 83% | 24 |
| hardware_component | 79% | 56 |
| database | 79% | 19 |

Printers are **100% repeat**—every single printer ticket is a recurrence of a known pattern. Yet `resolution_action_type` for printers is almost entirely `repair_needed` (no systematic replacement or process fix), pointing to a reactive cycle. The high repeat rate across all categories signals a systemic root-cause gap, not one-off failures.

Repeat vs. non-repeat resolution time difference is small (174 vs. 165 h median), so repeat incidents are not faster to resolve despite being familiar—further evidence of inadequate fix strategies.

---

## 4. Critical Incident Composition

The 27 critical-priority tickets cluster in two `incident_category` groups: **hardware_component (14, 52%)** and **network_connectivity (8, 30%)**. By `failure_type`: physical_damage (12) and connectivity_failure (6) dominate. By `resolution_action_type`: repair_needed (11) and connectivity_fix (8)—with 4 replacement_requested and 3 investigation_needed.

`urgency_signal` aligns well with `priority` for critical tickets: 24 of 27 (89%) are tagged `immediate_attention`, validating the signal. However, `immediate_attention` tickets do **not** resolve faster (median 166 h) than `standard` tickets (175 h)—escalation labeling is not translating into faster closure.

---

## 5. Self-Resolution Patterns

97 tickets (19%) are `self_resolved = True`. Self-resolution is slightly faster (median 169 h vs. 176 h for non-self-resolved) but the gap is modest. Self-resolution is most common in `network_connectivity` tickets (33%) and `database` tickets (26%), suggesting those categories have clearer user-facing workarounds. The `connectivity_failure` failure type has the highest self-resolution rate (30%), while `performance_degradation` has the lowest (8%).

---

## 6. Key Analytical Priorities (Decision-Ready Summary)

| Finding | Signal | Recommended Analysis |
|---|---|---|
| 41% of tickets are printer incidents with 100% repeat rate | Strong | Root cause / preventive maintenance study |
| Priority does not predict resolution time | Strong | Review SLA/priority assignment process |
| Luke Wilson: highest volume + slowest resolution | Moderate | Workload rebalancing |
| `failure_type` (unresponsive/service-failure) drives 60% of volume | Strong | Failure mode reduction; self-service tooling |
| `immediate_attention` urgency not reducing resolution time | Moderate | Escalation-to-action workflow audit |
| 90% repeat-incident rate across all categories | Strong | Knowledge-base / permanent-fix investment |

---

## Appendix: Data Scope

- **Rows:** 500 | **Date range:** Jan 2023 – Jan 2024  
- **Original columns used:** `category`, `priority`, `state`, `assigned_to`, `opened_at`, `closed_at`, `short_description`, `assignment_group`  
- **TAPP columns used:** `incident_category`, `failure_type`, `resolution_action_type`, `self_resolved`, `is_repeat_incident_type`, `urgency_signal`  
- `urgency_signal` adds meaningful signal beyond `priority` (captures connectivity/hardware severity not reflected in the 2-High default). `is_repeat_incident_type` and `incident_category` are the highest-value TAPP additions, surfacing structural patterns invisible in the raw `category` field.
