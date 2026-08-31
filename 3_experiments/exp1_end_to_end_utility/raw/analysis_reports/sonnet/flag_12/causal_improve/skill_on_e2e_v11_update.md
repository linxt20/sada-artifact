---
dataset: flag_12
scenario: causal_improve
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: what_if
focus_variable: "incident_resolution_efficiency"
query: "How can we improve incident resolution efficiency?"
source_table: augment_table/flag_12/causal_improve/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:14:07.310155+00:00
wall_seconds: 98.77
---

# Incident Resolution Efficiency Analysis

## Executive Summary

The dataset contains **500 incidents** (256 Closed, 244 Resolved) with a median resolution time of **173 hours (~7.2 days)**. The dominant bottleneck is hardware incidents requiring physical repair — 75% of all incidents — combined with high escalation rates across all categories. Targeted interventions in printer/hardware repair workflows, reduction of unnecessary escalations, and prioritization of software-resolvable issues can meaningfully cut resolution times.

---

## Method Note

TAPP-generated columns used in this analysis: `incident_category`, `affected_component`, `failure_symptom`, `resolution_action_type`, `involves_escalation_or_reassignment`, `is_recurring_issue_type`, `software_trigger_indicated`.

**`is_recurring_issue_type`** is constant (`True` for all 500 rows) — zero discriminative value; excluded from substantive analysis.  
**`affected_component`** closely mirrors `incident_category` and `category`; not independently cited.

---

## 1. Baseline: Resolution Time Distribution

| Statistic | Value |
|-----------|-------|
| Count | 500 |
| Median | 173 h |
| Mean | 178 h |
| 25th pct | 87 h |
| 75th pct | 253 h |
| Max | 514 h |

Priority is **not** a reliable differentiator: Critical (median 165 h), High (177 h), and Moderate (164 h) all resolve at similar speeds, suggesting priority is not being operationally acted upon.

---

## 2. Category and Incident Type — Biggest Volume Drivers

| Category (original) | Median hrs | Mean hrs | n |
|---|---|---|---|
| Software | **148** | 154 | 33 |
| Hardware | 175 | 181 | 406 |
| Database | 178 | 172 | 19 |
| Inquiry / Help | 183 | 182 | 20 |
| Network | 186 | 162 | 22 |

Hardware dominates volume (81% of incidents) and resolves slower than Software by ~27 hours at the median. Within hardware, `incident_category` (TAPP) reveals critical sub-segments:

| incident_category (TAPP) | Median hrs | n | Notes |
|---|---|---|---|
| monitor | **146** | 71 | Fastest hardware sub-type |
| software_update | 153 | 44 | |
| network_or_vpn | 161 | 25 | |
| keyboard_or_input_device | 175 | 70 | |
| database | 180 | 19 | |
| **printer** | **182** | **203** | Largest single category, 41% of all incidents |
| storage_hardware | 203 | 13 | |
| **software_crash** | **259** | **220** | Slowest; 80% escalation rate |

**Printer incidents (n = 203, 41% of volume)** are both the largest group and above median resolution time — the single highest-impact target for efficiency improvements.

---

## 3. Resolution Action Type — Repair Bottleneck

`resolution_action_type` (TAPP) reveals that the slowest action type is the most common:

| Resolution Action (TAPP) | Median hrs | n | % of total |
|---|---|---|---|
| software_install_or_update | **153** | 46 | 9% |
| replacement_needed | 161 | 25 | 5% |
| connectivity_fix | 178 | 48 | 10% |
| **repair_needed** | **182** | **374** | **75%** |
| configuration_fix | 182 | 2 | <1% |

**`repair_needed` accounts for 75% of all incidents and has the worst median resolution time.** Software-solvable paths (`software_install_or_update`) resolve ~29 hours faster. Shifting diagnosable software-trigger cases from repair queues to software action queues is a direct lever.

---

## 4. Software Trigger Signal

`software_trigger_indicated` (TAPP) flags 54 incidents (11%) where a software cause is indicated. These resolve **18 hours faster at the median** (157 h vs. 175 h, n = 54 vs. 446). The `Inquiry / Help` category shows the strongest effect: software-triggered inquiries resolve at 180 h vs. 290 h for non-software ones (n = 19 vs. 1, small sample). Ensuring triage correctly routes software-triggered incidents to the Software/Network groups rather than Hardware would capture this speed advantage at scale.

---

## 5. Escalation and Reassignment

`involves_escalation_or_reassignment` (TAPP) shows **76.8% of incidents (384/500) involve escalation or reassignment** — an abnormally high rate. However, at the aggregate level, escalated incidents have virtually the same median resolution time (173.2 h) as non-escalated ones (173.2 h). The effect is nuanced by action type:

| Resolution Action | No Escalation (median hrs) | With Escalation (median hrs) |
|---|---|---|
| connectivity_fix | 161 | 192 (+31 h) |
| repair_needed | 174 | 182 (+8 h) |
| software_install_or_update | 142 | 153 (+11 h) |

Escalation adds meaningful delay for **connectivity_fix** incidents (+31 h, n = 17 vs. 31). Printer connectivity incidents with escalation average 276 h vs. 95 h without (n = 6 vs. 4). Reducing unnecessary escalations for connectivity and software issues is a concrete efficiency gain.

---

## 6. Failure Symptom Patterns

`failure_symptom` (TAPP) shows `not_responding` (n = 237, 47%) is both the most common and slowest symptom (median 182 h), while `crashing_or_error` (n = 33) resolves in 154 h and `installation_or_info_request` (n = 25) in 157 h. Hardware symptoms like `physical_failure` (median 185 h, n = 40) and `not_responding` are slow because they almost universally require `repair_needed`.

---

## 7. Agent and Closure Process

| Assigned Agent | Median hrs | n |
|---|---|---|
| Howard Johnson | 163 | 106 |
| Beth Anglin | 165 | 85 |
| Charlie Whitherspoon | 168 | 103 |
| Fred Luddy | 170 | 90 |
| **Luke Wilson** | **195** | **116** |

Luke Wilson handles the most incidents (116) but resolves them ~32 hours slower than the fastest agent (Howard Johnson). Workload redistribution or targeted coaching could yield gains.

Incidents closed by **`system`** (automated closure) have the worst median resolution time (199 h vs. 168 h for `admin` and 160 h for `employee`), suggesting automated closures may be capturing stale or poorly triaged tickets.

---

## 8. Key Recommendations

| Priority | Action | Evidence |
|---|---|---|
| **1** | Streamline printer repair workflows (create dedicated SLA and parts pre-stocking) | Printers = 41% of incidents, median 182 h, escalation inflates to 186 h |
| **2** | Reduce escalation rate for connectivity and software incidents | Escalation adds +31 h for connectivity_fix; overall escalation rate is 77% |
| **3** | Improve triage to route software-triggered incidents away from repair queues | `software_trigger_indicated` incidents resolve 18 h faster; `software_install_or_update` action is 29 h faster than `repair_needed` |
| **4** | Address software_crash incidents with specialist handling | Median 259 h, 80% escalation rate, n = 5 (small but extreme) |
| **5** | Investigate Luke Wilson's caseload and automated system closures | +32 h vs. fastest agent; system-closed tickets avg 199 h |
| **6** | Enforce priority-based SLAs | Critical incidents currently resolve no faster than Moderate (165 h vs. 164 h) |
