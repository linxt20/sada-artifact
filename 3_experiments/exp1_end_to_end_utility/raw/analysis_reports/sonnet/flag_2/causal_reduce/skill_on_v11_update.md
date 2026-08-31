---
dataset: flag_2
scenario: causal_reduce
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "resolution_time"
query: "How can we reduce incident resolution time?"
source_table: augment_table/flag_2/causal_reduce/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:16:28.634293+00:00
wall_seconds: 58.03
---

# Incident Resolution Time Reduction Analysis

## Dataset Overview

- **500 total incidents** across Network, Database, Software, Hardware, and Service Desk groups
- **372 incidents** with computable resolution times (closed/resolved state)
- **28 incidents** remain open and unresolved (`is_open_unresolved = True`)
- Overall median resolution time: **~1,032 hours (~43 days)**; mean: **~1,043 hours**

---

## Key Factors Affecting Resolution Time

### 1. Assignment Group & Category
Assignment group is the strongest differentiator for resolution speed:

| Assignment Group | Median Resolution (hrs) | Count |
|---|---|---|
| Hardware | 794 | 4 |
| Software | 823 | 25 |
| Database | 960 | 89 |
| Network | 1,046 | 221 |
| Service Desk | 1,129 | 32 |

**Network** incidents dominate the backlog (221 of 372 resolved, plus 18 of 28 open-unresolved), and they resolve ~35% slower than Software incidents. **Service Desk** is the slowest group. Improving throughput and staffing in **Network** and **Service Desk** would have the largest systemic impact.

### 2. Failure Symptom Type
Symptom type shows a clear gradient in resolution speed:

| Failure Symptom | Median Resolution (hrs) |
|---|---|
| not_syncing | 679 |
| degraded_performance | 708 |
| crash_error | 708 |
| update_required | 740 |
| login_failure | 910 |
| cannot_connect | 989 |
| access_denied | 1,068 |
| service_outage | 1,100 |
| other | 1,108 |

Symptoms like **service_outage** and **access_denied** are ~60% slower than **not_syncing** or **degraded_performance**. These high-severity symptom types are also the most frequent (service_outage: 82; access_denied: 60). Targeted runbooks or automation for these two symptoms could deliver disproportionate gains.

### 3. Priority — Counter-Intuitive Pattern
Critical incidents do **not** resolve faster than lower-priority ones:

| Priority | Median Resolution (hrs) | Count |
|---|---|---|
| 1 - Critical | 1,255 | 57 |
| 3 - Moderate | 1,100 | 32 |
| 2 - High | 974 | 283 |

Critical incidents take ~29% longer than High-priority ones. Drilling down, **Critical + Software** (1,421 hrs) and **Critical + Inquiry/Help** (1,417 hrs) are the worst-performing combinations. The SLA/escalation process for Critical incidents appears to be a bottleneck, not an accelerator — this warrants investigation.

### 4. Resolver Match (`resolver_match`)
Whether the right specialist handles the incident has a **priority-dependent** effect:

| Priority | resolver_match = False (hrs) | resolver_match = True (hrs) |
|---|---|---|
| 1 - Critical | 1,288 | **672** |
| 2 - High | **938** | 1,068 |
| 3 - Moderate | 1,280 | **1,075** |

For **Critical incidents**, routing to a matched resolver cuts resolution time nearly in **half** (672 vs. 1,288 hrs). Only 127 of 421 resolved incidents (30%) have `resolver_match = True`, indicating significant routing inefficiency. Improving skill-based routing, especially for Critical tickets, is a high-leverage action.

### 5. Caller Segment
Incidents from **end users** resolve faster (median 989 hrs) than those originating from **ITIL automated processes** (median 1,090 hrs). This may reflect that automated incidents are more complex or systemic in nature, but it also suggests the automated intake pipeline may lack urgency metadata.

### 6. Who Updates the Ticket (`sys_updated_by`)
Tickets last updated by **employees** resolve fastest (median 938 hrs), while **system**-touched tickets are slowest (1,075 hrs). This is consistent with automated/batch processing adding latency without resolution progress.

### 7. Open-Unresolved Backlog
28 incidents (5.6%) are open and unresolved. These are concentrated in:
- **Network** group: 18 tickets (64%)
- **Database** group: 8 tickets
- Predominantly **2-High** priority (25 of 28)

This backlog, if left unmanaged, will continue to inflate mean resolution times.

---

## Recommendations

| Action | Expected Impact | Evidence Strength |
|---|---|---|
| Improve skill-based routing for Critical incidents | ~48% reduction for Critical | Strong (672 vs. 1,288 hrs) |
| Increase capacity/tooling in Network group | Broad impact (44% of volume) | Strong |
| Deploy runbooks for `service_outage` and `access_denied` symptoms | ~10–25% reduction on ~142 incidents | Moderate |
| Audit Service Desk escalation paths (slowest group) | Reduce tail latency | Moderate |
| Investigate Critical priority SLA process | Counter-intuitive slowness | Moderate (needs root cause) |
| Clear the 28 open-unresolved tickets | Direct backlog reduction | Strong |
| Review ITIL automated ticket quality/metadata | Reduce itil_automated lag | Weak (111 tickets) |

---

## Caveats

- Resolution times (~43-day median) appear unusually long and may reflect calendar/SLA time rather than actual work hours — interpret magnitudes relatively, not absolutely.
- `resolver_match = True` effect reversal for **2-High** priority (slower, not faster) is anomalous and may indicate data quality issues or that matched resolvers are assigned harder sub-types.
- `Hardware` group shows fastest resolution but has only 4 resolved tickets — insufficient for strong conclusions.
- `Openspace` assignment group (1 incident, 1,853 hrs) is an outlier and likely a miscategorization.
