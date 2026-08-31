---
dataset: flag_13
scenario: concept_attribute_operational
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "operational_burden"
query: "What operational burdens appear in incident descriptions?"
source_table: augment_table/flag_13/concept_attribute_operational/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:14:57.391229+00:00
wall_seconds: 77.06
---

# Operational Burdens in Incident Descriptions
**Query:** What operational burdens appear in incident descriptions?

---

## Method Note

TAPP-generated columns used in this analysis: `task_nature`, `failure_pattern`, `incident_scope`, `cross_resolver`, `off_hours_incident`, `recurrence_signal`, `incident_category`. These columns were evaluated against original structured fields (`priority`, `category`, `assignment_group`, `state`) and the numeric resolution-time proxy derived from `sys_updated_on`. Columns `affected_resource_type` was reviewed but found largely redundant with `category` and `incident_category`, so it is not centered in the findings.

---

## Dataset Overview

- **500 incidents** (all Closed or Resolved); priority skew: 78% High (2 - High), 17% Critical (1 - Critical).
- **Primary categories:** Network (260, 52%), Database (134, 27%), Software (73, 15%), Hardware (25, 5%), Inquiry/Help (8, 2%).
- Resolution time derived from `sys_updated_on` (format HH:MM:SS.s → minutes). Overall mean: **1,803 min (~30 hrs)**; median: **1,792 min**.

---

## 1. Volume and Nature of Work: Break-Fix Dominance

`task_nature` classifies the operational demand type:

| task_nature | Count | % | Mean Res. Time (min) |
|---|---|---|---|
| break_fix | 344 | 69% | 1,772 |
| access_request | 150 | 30% | 1,873 |
| maintenance_task | 6 | 1% | 1,831 |

**Break-fix** is the dominant burden (69% of incidents), reflecting reactive, unplanned work. **Access requests** (30%) represent a persistent administrative burden—one in three incidents is an access or connectivity provisioning issue rather than a failure.

---

## 2. Failure Patterns: Connectivity and Access Drive Volume

`failure_pattern` identifies the nature of each failure:

| failure_pattern | Count | % | Mean Res. Time (min) |
|---|---|---|---|
| connectivity_failure | 228 | 46% | 1,881 |
| access_denied | 117 | 23% | 1,779 |
| service_down | 112 | 22% | 1,688 |
| performance_degradation | 11 | 2% | 1,419 |
| installation_update_failure | 11 | 2% | 1,893 |
| sync_failure | 11 | 2% | 1,803 |
| hardware_malfunction | 9 | 2% | 1,826 |

Connectivity failures and access-denied events together account for **69% of all incidents**. Installation/update failures carry the second-highest mean resolution time (1,893 min), indicating disproportionate effort relative to volume.

---

## 3. Scope of Impact: Mostly System-Wide

`incident_scope` indicates breadth of impact:

| incident_scope | Count | Mean Res. Time (min) |
|---|---|---|
| system_wide | 268 (54%) | 1,781 |
| remote_access | 110 (22%) | 1,823 |
| location_specific | 38 (8%) | **2,060** |
| user_specific | 84 (17%) | 1,732 |

Over half of incidents are **system-wide** (54%), meaning the most common scope is broad-impact. Notably, **location-specific** incidents take the longest to resolve (mean 2,060 min), likely reflecting physical access and on-site coordination burdens. System-wide Network incidents dominate at 104 cases; Database system-wide issues account for 121 cases.

---

## 4. Cross-Team Coordination Burden (`cross_resolver`)

**80% of incidents (401/500)** required cross-resolver coordination. Cross-resolver rate by category:

| category | Cross-resolver rate |
|---|---|
| Inquiry / Help | 87.5% |
| Hardware | 84.0% |
| Network | 81.9% |
| Software | 78.1% |
| Database | 76.9% |

Despite the near-universal cross-resolver involvement, resolution time is not meaningfully differentiated by this flag alone (cross=True: mean 1,804 min; cross=False: 1,801 min). This suggests cross-team coordination is structurally baked into the workflow rather than an exceptional escalation path.

---

## 5. Off-Hours Incidents: Half of All Work

**249/500 incidents (49.8%)** occurred off-hours, nearly evenly split with business-hours incidents. Off-hours rate rises with priority:

| Priority | Off-hours rate |
|---|---|
| 1 - Critical | 53.0% |
| 2 - High | 50.4% |
| 3 - Moderate | 33.3% |

Critical-priority incidents are slightly more likely to occur off-hours. Email service had the highest off-hours rate among `incident_category` types (56.7%), followed by network_connectivity (54.8%) and software_update (54.5%).

---

## 6. Recurrence: Persistent Unresolved Issues

**99/500 incidents (19.8%)** show a recurrence signal, indicating repeated occurrence of the same issue. Recurrence rate by original `category`:

| category | Recurrence rate | Count |
|---|---|---|
| Inquiry / Help | 37.5% | 8 |
| Database | 23.1% | 134 |
| Network | 19.6% | 260 |
| Software | 17.8% | 73 |
| Hardware | 4.0% | 25 |

Recurring incidents take significantly longer to resolve: **mean 1,991 min vs. 1,757 min for non-recurring** (+13.3%). By `incident_category`, `database_access` (22.8% recurrence) and `vpn_access` (22.0%) are the highest-recurrence issue types, pointing to structural deficiencies not addressed by break-fix resolution.

---

## 7. Compound Burden: Incidents with Multiple Burden Signals

A **burden score** (0–3) was constructed by summing the three binary TAPP burden flags (`cross_resolver`, `off_hours_incident`, `recurrence_signal`):

| Burden Score | Count | Mean Res. Time (min) |
|---|---|---|
| 0 | 41 (8%) | 2,004 |
| 1 | 205 (41%) | 1,706 |
| 2 | 218 (44%) | 1,792 |
| **3 (all burdens)** | **36 (7%)** | **2,195** |

The 36 incidents carrying all three burden flags (cross-resolver + off-hours + recurring) have the **highest mean resolution time (2,195 min, ~36.6 hrs)**—25% above the overall mean. These represent the most operationally taxing incident type.

---

## 8. High-Burden Incident Hotspot: Critical/High + Off-Hours + Cross-Resolver

**199 incidents (40%)** simultaneously satisfied: priority 1–2, off-hours, and cross-resolver. Network (107 cases, mean 1,851 min) and Database (49 cases, mean 1,729 min) dominate this tier, confirming infrastructure connectivity and data access as the dual engines of operational burden.

---

## Summary: Key Operational Burdens

| Burden Type | Evidence | Scale |
|---|---|---|
| Reactive break-fix volume | `task_nature` = break_fix | 69% of incidents |
| Persistent access/connectivity failures | `failure_pattern`: connectivity + access_denied | 69% of incidents |
| Broad system-wide impact | `incident_scope` = system_wide | 54% of incidents |
| Cross-team coordination overhead | `cross_resolver` = True | 80% of incidents |
| Off-hours response demand | `off_hours_incident` = True | 50% of incidents |
| Recurring unresolved issues | `recurrence_signal` = True | 20% of incidents; +13% longer resolution |
| Compound high-burden incidents | All three burden flags = True | 36 incidents; mean 2,195 min |

**The primary operational burdens are:** (1) near-constant reactive break-fix work dominated by connectivity and access-denied failures, (2) half of all incident response falling outside business hours, (3) structurally required cross-team coordination on 80% of tickets, and (4) a recurrence problem concentrated in Database and Network categories that lengthens resolution time by ~13%. The 7% of incidents bearing all burden signals represent a high-impact tail requiring targeted remediation.
