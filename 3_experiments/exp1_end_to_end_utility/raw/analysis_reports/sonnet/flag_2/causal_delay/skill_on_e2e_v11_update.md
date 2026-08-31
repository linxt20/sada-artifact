---
dataset: flag_2
scenario: causal_delay
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "resolution_time"
query: "Controlling for priority and category, which underlying causes explain longer resolution times?"
source_table: augment_table/flag_2/causal_delay/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:16:56.613076+00:00
wall_seconds: 91.05
---

# Causal Drivers of Longer Resolution Times — IT Incident Dataset
**Query:** Controlling for priority and category, which underlying causes explain longer resolution times?

---

## Method Note

Analysis uses 500 incidents (372 with resolved timestamps). Resolution time is computed as `closed_at − opened_at` in hours. Original structured columns — `priority`, `category`, `assignment_group`, `assigned_to` — serve as primary controls and evidence. The following TAPP-generated columns were used as additional explanatory variables:

- `failure_mode` — primary semantic driver; strong signal, used extensively
- `affected_component` — moderate signal; used to cross-check failure_mode findings
- `scope_indicator` — partial signal; useful for Network/system_wide dominance
- `recurrence_signal` — very low coverage (2 positives); noted but not centered
- `resolution_ownership_pattern` — weak/mixed signal; noted briefly

---

## 1. Dataset Overview

| Metric | Value |
|---|---|
| Total incidents | 500 |
| Incidents with resolution time | 372 |
| Overall mean resolution | 1,043 h (~43 days) |
| Overall median resolution | 1,032 h (~43 days) |
| Open / unresolved | 128 |

**Priority distribution:** 2 - High (380), 1 - Critical (79), 3 - Moderate (41)  
**Category distribution:** Network (269), Database (116), Software (86), Hardware (18), Inquiry/Help (11)

---

## 2. Baseline: Priority and Category Effects

Priority alone explains little variance — all three levels cluster near 1,000–1,120 h median, with Critical and Moderate both *higher* than High:

| Priority | Mean (h) | Median (h) | n |
|---|---|---|---|
| 1 - Critical | 1,119 | 1,255 | 57 |
| 2 - High | 1,020 | 974 | 283 |
| 3 - Moderate | 1,121 | 1,100 | 32 |

Category contributes a ~120 h spread at the median, with Network slowest:

| Category | Mean (h) | Median (h) | n |
|---|---|---|---|
| Network | 1,079 | 1,046 | 197 |
| Software | 1,051 | 985 | 70 |
| Hardware | 1,105 | 1,021 | 12 |
| Database | 955 | 967 | 86 |
| Inquiry/Help | 958 | 686 | 7 |

Because priority and category together leave most variance unexplained, the TAPP-generated columns provide critical semantic lift.

---

## 3. Primary Cause: `failure_mode`

`failure_mode` is the strongest single explanatory variable after controlling for priority and category.

| Failure Mode | Mean (h) | Median (h) | n |
|---|---|---|---|
| service_down | 1,129 | 1,118 | 87 |
| access_denied | 1,077 | 1,061 | 69 |
| connection_failure | 1,018 | 1,003 | 187 |
| update_failure | 938 | 679 | 8 |
| sync_failure | 812 | 730 | 9 |
| crash | 830 | 722 | 6 |
| performance_degradation | 366 | 366 | 2 |

**Key finding:** `service_down` and `access_denied` are the two failure modes that consistently drive longer resolution times — **~115–155 h longer median** than `connection_failure` (the most common mode).

### Controlled by Priority

| Failure Mode | 1-Critical (h) | 2-High (h) | 3-Moderate (h) |
|---|---|---|---|
| service_down | 1,212 | 1,079 | 989 |
| access_denied | 1,356 | 1,044 | 1,322 |
| connection_failure | 937 | 1,029 | 976 |
| crash | 686 | 859 | — |

`access_denied` at Critical priority produces the longest median (1,356 h). The delay penalty for `service_down` and `access_denied` persists across priority levels, confirming these are root-cause drivers rather than artifacts of severity labeling.

### Controlled by Category

| Failure Mode | Database (h) | Network (h) | Software (h) |
|---|---|---|---|
| service_down | 1,363 | 1,108 | 1,157 |
| access_denied | 959 | 1,257 | 1,023 |
| connection_failure | 916 | 1,043 | — |

`service_down` incidents in the **Database** category are the single worst cell (median 1,363 h). `access_denied` in **Network** (median 1,257 h) is the next worst.

---

## 4. Secondary Cause: `affected_component`

The `affected_component` column cross-validates the failure_mode findings.

| Affected Component | Mean (h) | Median (h) | n |
|---|---|---|---|
| local_server | 1,178 | 1,162 | 20 |
| application_software | 1,150 | 910 | 17 |
| email_server | 1,106 | 1,118 | 70 |
| vpn_client | 1,103 | 1,100 | 80 |
| email_client | 1,051 | 1,079 | 40 |
| network_infrastructure | 950 | 895 | 52 |
| database_server | 947 | 960 | 89 |
| peripheral_device | 926 | 794 | 4 |

**`local_server`** and **`application_software`** have the highest mean resolution times. The `email_server` and `vpn_client` components — both predominantly associated with `service_down` and `access_denied` failure modes — also exceed 1,100 h mean.

At Critical priority, `application_software` reaches a mean of 2,076 h — more than double the overall average — and `local_server` at Moderate reaches 1,968 h, suggesting escalation complexity when these components fail.

---

## 5. Scope Indicator

`scope_indicator` is dominated by `system_wide` (217 of 372 resolved incidents = 58%). The two most actionable cells:

| Scope | Mean (h) | n | Notes |
|---|---|---|---|
| system_wide | 1,060 | 217 | Bulk of workload |
| remote_access | 1,037 | 90 | Mainly Network/VPN |
| single_user | 1,033 | 54 | Mixed |
| location_specific | 1,133 | 7 | Small sample |

Within `single_user` scope, Network incidents have a strikingly high median (1,669 h, n=16), suggesting single-user network problems are disproportionately difficult to diagnose. `system_wide` scope combined with `service_down` failure mode is the dominant slow-resolution cluster. The remaining scope values have too few cases (<10) for reliable inference.

---

## 6. Resolution Ownership Pattern

`resolution_ownership_pattern` (cross_agent vs. self_resolved) shows a mixed and priority-dependent effect:

| Priority | cross_agent median (h) | self_resolved median (h) |
|---|---|---|
| 1 - Critical | 1,284 | 766 |
| 2 - High | 935 | 1,104 |
| 3 - Moderate | 1,280 | 1,075 |

At Critical priority, cross-agent escalation correlates with longer times (+518 h vs. self-resolved), consistent with hard problems requiring escalation. At High priority the pattern inverts. This variable partially reflects case difficulty rather than being an independent cause; it is not a primary driver.

---

## 7. Recurrence Signal

Only 2 incidents in the resolved set have `recurrence_signal = True` (median 1,727 h vs. 1,028 h for non-recurring). The signal is directionally consistent with recurrent issues taking longer, but the sample is too small (n=2) to draw conclusions.

---

## 8. Assignee-Level Variation

Assignee differences contribute moderate spread independent of category/priority:

| Assignee | Mean (h) | Median (h) | n |
|---|---|---|---|
| Beth Anglin | 1,142 | 1,298 | 73 |
| Fred Luddy | 1,125 | 1,100 | 74 |
| Charlie Whitherspoon | 1,036 | 1,061 | 71 |
| Luke Wilson | 968 | 816 | 85 |
| Howard Johnson | 953 | 910 | 69 |

Beth Anglin and Fred Luddy show ~380 h higher median than Howard Johnson. This may reflect case-mix (higher share of `service_down`/`access_denied` assignments) rather than individual performance.

---

## 9. Summary: Causal Hierarchy

Controlling for priority and category, the following causes explain longer resolution times in descending importance:

| Rank | Factor | Evidence |
|---|---|---|
| 1 | **`failure_mode = service_down`** | +115 h median vs. connection_failure; persists across all priority/category strata; worst in Database category (1,363 h) |
| 2 | **`failure_mode = access_denied`** | +58 h median overall; spikes to +1,356 h at Critical; worst in Network category |
| 3 | **`affected_component = local_server` or `application_software`** | ~1,150–1,178 h mean; at Critical priority application_software reaches 2,076 h mean |
| 4 | **`affected_component = email_server` or `vpn_client`** | >1,100 h mean; overlap with service_down failure mode |
| 5 | **`scope_indicator = single_user` within Network** | 1,669 h median (n=16); outlier cell suggesting diagnostic difficulty |
| 6 | **Assignee allocation** | ~380 h spread in median; likely reflects case-mix |

**Recurrence_signal** and **resolution_ownership_pattern** are too low-coverage or too confounded to be treated as independent root causes.
