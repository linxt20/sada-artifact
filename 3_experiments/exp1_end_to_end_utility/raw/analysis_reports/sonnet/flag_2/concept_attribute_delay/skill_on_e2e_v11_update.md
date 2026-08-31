---
dataset: flag_2
scenario: concept_attribute_delay
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "incident_delay_reasons"
query: "Why do some incidents take longer to resolve?"
source_table: augment_table/flag_2/concept_attribute_delay/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:17:12.561636+00:00
wall_seconds: 84.69
---

# Why Do Some Incidents Take Longer to Resolve?

**Dataset:** 500 incidents · 372 resolved/closed · 128 open or in-progress  
**Outcome measure:** Resolution time in hours (opened_at → closed_at) for the 372 resolved/closed incidents  
**Overall resolution time:** mean **1,043 h**, median **1,032 h** (range: 24 – 2,206 h)

---

## Method Note

TAPP-generated columns used in this analysis: `incident_category`, `failure_pattern`, `scope_indicator`, `assignment_lag`, `assignee_workload_signal`, `reassignment_indicator`, `remote_context`, `incident_is_open_unresolved`. The column `caller_repeat_reporter` was inspected but is constant (all True) and provides no discriminating signal.

---

## 1. Scope of Impact Is the Strongest Predictor of Resolution Time

Incidents tagged by `scope_indicator` as **outage_wide** take substantially longer than those affecting individual users or departments, and this is amplified when combined with Critical priority.

| `scope_indicator` | Mean hours | Median hours | n |
|---|---|---|---|
| production_environment | 312 | 312 | 2 |
| department_wide | 479 | 481 | 4 |
| location_specific | 1,010 | 794 | 34 |
| individual_user | 1,042 | 1,043 | 280 |
| **outage_wide** | **1,144** | **1,180** | **52** |

Outage-wide incidents are 10% slower than the average and 139% slower than department-wide ones. Within outage_wide, Critical-priority incidents (n=29) average **1,200 h** vs. 1,074 h for High-priority (n=23), confirming that enterprise-wide failures with high urgency are the hardest and slowest to close.

---

## 2. Incident Category and Failure Pattern Drive Meaningful Variation

Using `incident_category` (TAPP) alongside the structured `category` field:

| `incident_category` | Mean hours | Median hours | n | Structured `category` |
|---|---|---|---|---|
| authentication | 1,181 | 1,165 | 4 | Software |
| server | 1,178 | 1,162 | 20 | Network/Database |
| software_update | 1,166 | 956 | 12 | Software |
| vpn | 1,103 | 1,100 | 80 | Network |
| email | 1,086 | 1,100 | 110 | Network/Software |
| network_connectivity | 948 | 895 | 53 | Network |
| database | 947 | 960 | 89 | Database |
| hardware | 926 | 794 | 4 | Hardware |

VPN and email incidents (190 incidents combined, 51% of resolved volume) resolve ~13–15% slower than database/network-connectivity incidents, suggesting these service types involve more diagnostic complexity. The structured `category` = Network has a mean of **1,079 h** vs. Database at **955 h**, consistent with this finding.

By `failure_pattern`:

| `failure_pattern` | Mean hours | n |
|---|---|---|
| service_down | 1,103 | 83 |
| connection_failure | 1,036 | 239 |
| login_failure | 1,005 | 17 |
| sync_crash | 944 | 17 |
| performance_degradation | 366 | 2 |

**Service-down** incidents take ~16% longer than performance-degradation issues, though the latter has a very small sample (n=2). Connection failures are the dominant failure type (64% of resolved incidents).

---

## 3. Unresolved / Stuck Incidents Are Concentrated in Specific Areas

**79 incidents** are flagged as `incident_is_open_unresolved = True` (all are in state New or In Progress). These represent 15.8% of the dataset. Backlog concentration:

| Assignment Group | Open-Unresolved | Total | Open Rate |
|---|---|---|---|
| Service Desk | 8 | 41 | **19.5%** |
| Database | 22 | 121 | 18.2% |
| Network | 46 | 300 | 15.3% |
| Software | 3 | 32 | 9.4% |
| Hardware | 0 | 5 | 0% |

Service Desk and Database have the highest rates of unresolved incidents. By `incident_category`, the open backlog skews toward **database** (22), **vpn** (21), and **email** (15) — the same categories that are slowest to resolve among closed tickets.

---

## 4. Assignment Lag Is a Key Structural Bottleneck

`assignment_lag` reveals that **400 of 500 incidents (80%)** had a multi-day lag before assignment, and **66 (13.2%)** remain **unassigned** entirely — all of which appear in the open/in-progress population. Only 17 incidents were assigned same-day, and they resolved dramatically faster (mean **24 h**) compared to multi-day assignments (mean **1,057 h**). The 4 next-day assignments resolved in a mean of **38 h**.

| `assignment_lag` | Mean resolution hours | n (resolved) |
|---|---|---|
| same_day | 24 | 1 |
| next_day | 38 | 4 |
| multi_day | 1,057 | 367 |
| unassigned | — | 0 (all open) |

The structural implication is clear: the overwhelming majority of incidents enter a multi-day assignment queue, which alone accounts for the bulk of elapsed time before resolution work begins.

---

## 5. Assignee Workload and Reassignment Add Secondary Delay

- **Reassignment** (`reassignment_indicator = True`) affects 290 of the 372 resolved incidents (78%). Reassigned incidents average **1,047 h** vs. **1,032 h** for non-reassigned — a modest but directionally consistent signal. High-volume assignees are more likely to have reassigned incidents (160 vs. 54), suggesting routing inefficiencies.
- **Assignee workload** shows Beth Anglin and Fred Luddy averaging **1,142 h** and **1,125 h** respectively, vs. Howard Johnson at **953 h** and Luke Wilson at **968 h** — a ~20% spread across individual assignees, independent of category.
- **Remote context** (`remote_context = True`): incidents involving remote workers resolve in mean **1,091 h** vs. **1,030 h** for non-remote (+6%), a modest effect across 81 resolved remote-context incidents.

---

## 6. Priority Does Not Straightforwardly Drive Faster Resolution

| Priority | Mean hours | Median hours | n |
|---|---|---|---|
| 1 - Critical | 1,119 | 1,255 | 57 |
| 2 - High | 1,020 | 974 | 283 |
| 3 - Moderate | 1,121 | 1,100 | 32 |

Critical incidents resolve **slower** on average than High-priority ones, likely because critical incidents disproportionately represent outage-wide scope (29 of 52 outage-wide resolved tickets are Critical). This confounding relationship between priority and scope is a key finding.

---

## Summary of Delay Drivers

| Driver | Effect | Evidence |
|---|---|---|
| **Multi-day assignment lag** (structural) | Dominant — median 1,032 h vs. 24–38 h for same/next-day | `assignment_lag`, 98% of resolved = multi_day |
| **Outage-wide scope** | +10% over average; +139% over dept-wide | `scope_indicator`, n=52 |
| **VPN/email/server incident types** | +13–27% vs. database/hardware | `incident_category` + `category` |
| **Service-down failure pattern** | +7% vs. average | `failure_pattern`, n=83 |
| **Unassigned incidents** | Never resolved (100% open) | `assignment_lag`, n=66 |
| **Reassignment** | Modest (+15 h mean) | `reassignment_indicator`, 78% reassigned |
| **Assignee identity** | ~20% spread across individuals | `assigned_to`, structured column |
| **Remote context** | +6% | `remote_context`, n=81 |

**Bottom line:** The primary driver of long resolution times is structural — almost all incidents wait multiple days before assignment begins, making assignment speed the single most actionable lever. Among incidents in the queue, outage-wide scope, VPN/email/server incident types, service-down failure patterns, and high-load assignees further extend time to resolution.
