---
dataset: flag_13
scenario: concept_attribute_operational
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "operational_burden"
query: "What operational burdens appear in incident descriptions?"
source_table: augment_table/flag_13/concept_attribute_operational/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:14:19.962064+00:00
wall_seconds: 48.71
---

# Operational Burdens in Incident Descriptions

**Dataset:** 500 incidents | IT service desk, 2023  
**Focus variable:** Operational burden, surfaced across `failure_symptom`, `incident_category`, `off_hours_incident`, `recurrence_signal`, `recurrent_caller`, `self_resolved`, `incident_blast_radius`, and `priority`.

---

## 1. Dominant Failure Patterns

| Failure Symptom | Count | % of Total |
|---|---|---|
| `connectivity_failure` | 227 | 45.4% |
| `access_denied` | 120 | 24.0% |
| `not_responding` | 47 | 9.4% |
| `outage` | 41 | 8.2% |
| `Unknown` | 32 | 6.4% |
| `performance_degradation` | 11 | 2.2% |
| `installation_failure` | 11 | 2.2% |
| `sync_failure` | 11 | 2.2% |

**Connectivity failure** is the single largest operational burden — nearly half of all incidents represent users unable to reach a required resource. **Access denial** (24%) adds a secondary layer of authentication/authorization friction. Together these two account for ~70% of all incidents, implying a persistent infrastructure reliability gap.

---

## 2. Affected Service Areas

The top three incident categories are tightly clustered:

| Category | Count |
|---|---|
| `database` | 136 (27.2%) |
| `email_service` | 134 (26.8%) |
| `vpn_connectivity` | 109 (21.8%) |
| `network_connectivity` | 74 (14.8%) |

No single service dominates; the operational burden is broadly distributed across core infrastructure layers (data, communication, remote access, network).

---

## 3. Off-Hours Burden

- **306 of 500 incidents (61.2%)** occurred outside normal business hours (`off_hours_incident = True`).
- Of those, **250 required manual resolution** (`self_resolved = False`), meaning IT staff were called upon outside working hours for the majority of all incidents.  
- Only 97 incidents (19.4%) were self-resolved across the whole dataset, indicating a high dependence on human intervention.

This is a significant staffing/on-call burden.

---

## 4. Recurrence and Repeat Callers

- **400 of 500 callers (80%)** are flagged as `recurrent_caller = True`, meaning the same users repeatedly open incidents — indicating that underlying problems are not being permanently resolved.
- **99 incidents (19.8%)** carry a `recurrence_signal = True`, meaning those specific issues have recurred.
- **98 of the 99 recurrence-signal incidents also occurred off-hours**, concentrating recurring, unresolved problems in the most operationally costly time window.
- Only 3 incidents have both `recurrent_caller` and `recurrence_signal` simultaneously flagged — suggesting the two flags measure related but distinct dimensions (caller habit vs. issue recurrence).

---

## 5. Blast Radius and Priority

| Blast Radius | Count |
|---|---|
| `individual_user` | 276 (55.2%) |
| `system_wide` | 189 (37.8%) |
| `location_specific` | 35 (7.0%) |

- **189 system-wide incidents** represent the highest-impact operational burden; **61 of these are also Priority 1 – Critical**, potentially causing organization-wide work stoppages.
- Priority distribution: 78.2% are `2 - High`, 16.6% are `1 - Critical`, confirming that incidents are routinely severe rather than routine maintenance noise.

---

## 6. Affected Resource Scope

| Resource Scope | Count |
|---|---|
| `server_side` | 238 (47.6%) |
| `network_infrastructure` | 186 (37.2%) |
| `client_side` | 76 (15.2%) |

Server-side and network-infrastructure problems dominate, requiring specialized IT expertise rather than self-service resolution — consistent with the low self-resolution rate.

---

## 7. Summary of Operational Burdens

| Burden Type | Evidence |
|---|---|
| **Persistent connectivity failures** | 45% of incidents; VPN, WiFi, server connectivity top descriptions |
| **Off-hours staffing demand** | 61% of incidents occur off-hours; 250 require manual intervention after hours |
| **Unresolved recurring issues** | 80% recurrent callers; recurrence signal concentrated in off-hours |
| **Broad service impact** | 38% system-wide blast radius; 61 critical + system-wide incidents |
| **High manual intervention rate** | Only 19% self-resolve; 80% require IT staff action |
| **Multi-service fragility** | No single root cause — database, email, VPN, and network all near-equally burdened |

---

## Caveats

- `failure_symptom = Unknown` (6.4%) limits full classification of a non-trivial share of incidents.
- `sys_updated_on` and `closed_at` are stored in elapsed-time format (e.g., `24:34.6`), not absolute timestamps, making duration-based burden analysis (e.g., MTTR) infeasible from this dataset alone.
- The `recurrent_caller` flag (80% True) may reflect a small user population generating most tickets rather than a universal recurrence problem — caller-level disaggregation is not available in the visible data.
