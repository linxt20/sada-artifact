---
dataset: customer_support_tickets
scenario: concept_attribute_operational
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "operational_burden"
query: "What customer issues create the most support burden?"
source_table: augment_table/customer_support_tickets/concept_attribute_operational/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:11:40.771925+00:00
wall_seconds: 104.01
---

# Customer Support Burden Analysis
**Dataset:** 250 tickets · Query: *What customer issues create the most support burden?*

---

## Method Note

Support burden is defined as the combination of **ticket volume**, **total agent-time consumed** (`resolution_minutes` summed), **average resolution time**, and **priority severity** (% Critical/High tickets). TAPP-generated columns used in this analysis: `issue_category`, `product_area`, `operational_impact`, `user_scope`, `root_cause_class`, `requires_engineering_escalation`, `workaround_available`. The columns `product_area` and `user_scope` are partially redundant with patterns observable in the raw descriptions but add useful semantic grouping; `requires_engineering_escalation` and `workaround_available` add signal not captured in any original structured column.

---

## 1. Top-Line Burden by Issue Category

| `issue_category` | Tickets | Total Res-Min | Avg Res-Min | % Critical/High |
|---|---|---|---|---|
| **bug** | 76 | 4,328 | 56.9 | 22% |
| **performance_degradation** | 25 | 3,558 | **142.3** | **100%** |
| **outage** | 29 | 2,023 | 69.8 | 97% |
| how_to_question | 25 | 1,723 | 68.9 | 0% |
| configuration_error | 16 | 1,353 | 84.6 | 56% |
| feature_request | 57 | 1,299 | 22.8 | 0% |
| billing_error | 9 | 875 | 97.2 | 89% |
| data_loss_or_corruption | 7 | 555 | 79.3 | 100% |
| security_incident | 6 | 500 | 83.3 | 100% |

**Key findings:**
- **Bugs** dominate by sheer volume (76 tickets, 4,328 total minutes), but most are Medium priority (59/76). They are the single largest drain on agent capacity.
- **Performance degradation** is the most severe per-ticket burden: avg 142 min/ticket, all 25 tagged Critical or High, and all 25 carry `operational_impact = partial_service_degradation`. Total agent time (3,558 min) rivals bugs despite one-third the volume.
- **Outages** (29 tickets) are nearly all Critical (27 Critical, 1 High); 25 are `full_service_outage` per `operational_impact`. High urgency but moderate total time due to structured escalation paths.
- **Feature requests** account for 57 tickets but average only 22.8 min each and carry zero Critical/High priority — they are a volume nuisance, not a severity burden.

---

## 2. Burden by Product Area

| `product_area` | Tickets | Total Res-Min | Avg Res-Min | % Crit/High |
|---|---|---|---|---|
| **performance_and_search** | 21 | 2,794 | 133.0 | 91% |
| **infrastructure_and_platform** | 28 | 2,411 | 86.1 | 93% |
| ui_and_ux | 68 | 2,197 | 32.3 | 3% |
| billing_and_payments | 22 | 1,832 | 83.3 | 36% |
| authentication_and_sso | 24 | 1,720 | 71.7 | 42% |
| security_and_compliance | 25 | 1,657 | 66.3 | 36% |
| api_and_integrations | 21 | 1,321 | 62.9 | 57% |

`performance_and_search` and `infrastructure_and_platform` are the highest-cost product areas per ticket and by total time, consistent with the performance/outage issue categories. `ui_and_ux` is the highest-volume area (68 tickets) but lowest average resolution time (32.3 min), driven predominantly by feature requests and low-priority bugs.

---

## 3. Operational Impact

| `operational_impact` | Tickets | Total Res-Min | Avg Res-Min | % Crit/High |
|---|---|---|---|---|
| **partial_service_degradation** | 37 | 4,244 | **114.7** | 81% |
| **blocked_workflow** | 47 | 3,227 | 68.7 | 30% |
| data_integrity_risk | 32 | 2,379 | 74.3 | 59% |
| full_service_outage | 32 | 2,375 | 74.2 | 97% |
| not_present | 65 | 2,555 | 39.3 | 0% |
| cosmetic_or_minor | 25 | 678 | 27.1 | 0% |

`partial_service_degradation` (37 tickets) generates the largest total agent time (4,244 min) and highest average resolution (114.7 min), reflecting how performance degradation issues — which are all in this bucket — are disproportionately time-consuming. `blocked_workflow` (47 tickets) represents the most frequent high-impact category.

---

## 4. Escalation and Workaround Effects

**Engineering escalation** (`requires_engineering_escalation`) dramatically separates resolution times:

| Escalation path | Tickets | Avg Res-Min | % Crit/High |
|---|---|---|---|
| platform_infra | 37 | 83.5 | 97% |
| identity_team | 5 | 82.2 | 80% |
| billing_ops | 22 | 81.1 | 32% |
| security_team | 13 | 80.8 | 62% |
| engineering_investigation | 116 | 72.4 | 39% |
| **no_escalation_needed** | 57 | **26.1** | 0% |

Tickets requiring any escalation average 72–84 min vs. 26 min for those that don't — a **3× difference**. `engineering_investigation` alone covers 116 tickets (46% of all tickets) and 8,394 total minutes — the single largest escalation-time sink.

**Workaround availability** further amplifies burden:

| `workaround_available` | Tickets | Avg Res-Min |
|---|---|---|
| no_workaround | 159 | 76.5 |
| partial_workaround | 15 | 81.4 |
| not_present (non-impacting) | 76 | 37.2 |

159 tickets (64%) have no workaround at 76.5 min avg, vs. 37.2 min for tickets where the issue has no operational impact (`not_present`).

---

## 5. Root Cause Classes

| `root_cause_class` | Tickets | Avg Res-Min | Total Res-Min | % Crit/High |
|---|---|---|---|---|
| **regression_from_release** | 71 | 78.0 | 5,537 | 41% |
| infrastructure_failure | 31 | 81.4 | 2,523 | 94% |
| configuration_misconfiguration | 23 | 82.6 | 1,900 | 70% |
| race_condition_or_cache_bug | 24 | 63.8 | 1,532 | 42% |
| data_migration_artifact | 10 | 91.8 | 918 | 100% |
| not_present | 75 | 37.3 | 2,801 | 0% |

`regression_from_release` is the dominant root cause (71 tickets, 5,537 total minutes) — the largest single root-cause burden. `infrastructure_failure` (31 tickets, 94% Crit/High) and `configuration_misconfiguration` (23 tickets) are the next highest-severity drivers.

---

## 6. User Scope

| `user_scope` | Tickets | Avg Res-Min | Total Res-Min | % Crit/High |
|---|---|---|---|---|
| **single_user** | 157 | 56.9 | 8,939 | 23% |
| **entire_tenant** | 53 | 95.3 | 5,050 | **96%** |
| subset_of_users | 36 | 53.2 | 1,915 | 25% |
| cross_tenant_or_platform_wide | 4 | 77.5 | 310 | 100% |

Tenant-wide issues (53 tickets) cost 95.3 min each and are nearly all Critical/High — concentrated in outages and performance degradation.

---

## 7. Highest-Burden Combinations

The most burdensome issue clusters combining `issue_category` and `operational_impact`:

| `issue_category` | `operational_impact` | Tickets | Avg Res-Min | Total Res-Min |
|---|---|---|---|---|
| performance_degradation | partial_service_degradation | 23 | 141.7 | **3,258** |
| bug | blocked_workflow | 30 | 58.9 | 1,768 |
| outage | full_service_outage | 25 | 69.4 | 1,735 |
| configuration_error | blocked_workflow | 9 | 83.8 | 754 |
| bug | partial_service_degradation | 9 | 68.7 | 618 |
| billing_error | blocked_workflow | 4 | 97.5 | 390 |

---

## Summary: Priority Burden Ranking

| Rank | Issue Cluster | Why it Burdens Support |
|---|---|---|
| 🔴 1 | **Performance degradation** (perf_and_search, partial_service_degradation) | Highest avg resolution (142 min), 100% Crit/High, no workarounds; root cause: regression_from_release & infrastructure_failure |
| 🔴 2 | **Bugs (blocked_workflow)** | Highest total volume (76 tickets); 30 cause workflow blockages at 58.9 min avg; largest `engineering_investigation` load |
| 🔴 3 | **Outages** (full_service_outage, entire_tenant) | 97% Critical, tenant-wide scope, 95+ min avg for tenant-wide cases |
| 🟠 4 | **Configuration errors** | High avg resolution (84.6 min), 56% Crit/High, mostly `no_workaround` |
| 🟠 5 | **Billing errors** | Small volume but 89% Crit/High, 97 min avg, all require billing_ops escalation |
| 🟡 6 | **How-to questions** | 25 tickets, 0% Crit/High but ~69 min avg — education/documentation gap opportunity |

**Top actionable levers:** (1) Harden release regression testing to reduce the `regression_from_release` root cause (71 tickets, 5,537 min). (2) Invest in performance_and_search infrastructure to reduce the 142-min avg resolution cluster. (3) Improve tenant-isolation for outages to reduce `entire_tenant` blast radius (53 tickets, 96% Crit/High).
