---
dataset: customer_support_tickets
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What are the main kinds of issues these support tickets are about?"
source_table: augment_table/customer_support_tickets/focus_inference/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:11:17.045600+00:00
wall_seconds: 59.79
---

# Support Ticket Issue Analysis
**Dataset:** 250 tickets · **TAPP columns used:** `issue_category`, `issue_subcategory`, `affected_component`, `impact_scope`, `business_impact_signal`, `root_cause_class`

---

## Executive Summary

Support tickets span **eight issue categories**. Bugs dominate volume (34%), followed by feature requests (23%) and outages (14%). These three categories alone account for 71% of all tickets. Resolution times and priority levels vary sharply across categories, providing clear triage signals.

---

## 1. Issue Category Distribution

| issue_category | Count | Share | Median Res. (min) | Dominant Priority |
|---|---|---|---|---|
| **bug** | 85 | 34% | 46 | Medium (73%) |
| **feature_request** | 57 | 23% | 22 | Low (84%) |
| **outage** | 34 | 14% | 70 | Critical (91%) |
| **question_or_clarification** | 25 | 10% | 70 | Low (100%) |
| **performance_degradation** | 22 | 9% | 140 | High (100%) |
| **configuration_error** | 13 | 5% | 75 | High (46%) |
| **billing_issue** | 8 | 3% | 93 | Critical (50%) |
| **security_incident** | 6 | 2% | 83 | Critical (100%) |

---

## 2. Bugs (n=85, 34%)

The largest category. Subcategories (from `issue_subcategory`):

| Subcategory | Count |
|---|---|
| ui_ux_defect | 37 |
| auth_and_sso | 13 |
| access_permission | 9 |
| api_and_webhook | 5 |
| data_loss_or_corruption | 4 |
| integration_sync | 4 |
| export_import + notification_delivery + performance_query + other | 13 |

- **`root_cause_class`:** Split across data_integrity (16), regression_from_release (15), race_condition_or_cache (14), misconfiguration (11), and design_gap (16) — suggesting a genuinely diverse set of underlying failure modes.
- **`business_impact_signal`:** Primarily `productivity_degradation` (55/85). Nine tickets reached `service_completely_blocked` and five had `sla_breach_risk`.
- **`impact_scope`:** 40 single-user, 23 multiple users (same tenant), 21 entire-tenant — meaning ~52% of bugs affect more than one user.
- **`affected_component`:** admin_console (19) and auth_identity (16) are the hottest components.
- Median resolution is 46 min — the fastest among operational issue types.

---

## 3. Feature Requests (n=57, 23%)

The second-largest category, consisting almost entirely of `feature_enhancement` subcategory (51/57). These are low-urgency (84% Low priority, median resolution 22 min) and concentrated in admin_console (20) and notifications (13). **`root_cause_class`** is uniformly `design_gap` (57/57), confirming these are product gaps rather than defects. Business impact is mostly `cosmetic_or_minor` (30) or `productivity_degradation` (21), with 6 tied to a `compliance_or_audit_deadline`.

---

## 4. Outages (n=34, 14%)

High-severity, tenant-wide events. 91% are Critical priority; 28/34 affect the `entire_tenant` (`impact_scope`). Median resolution is 70 min.

- **`root_cause_class`:** infrastructure_failure (15) and data_integrity (6) lead; third_party_dependency accounts for 4.
- **`business_impact_signal`:** 26/34 are `service_completely_blocked`.
- **`affected_component`:** infrastructure_platform (9), account_management (8), data_loss_or_corruption (6).
- **`issue_subcategory`:** account_management (8) and data_loss_or_corruption (6) are the leading outage sub-types.

---

## 5. Questions / Clarifications (n=25, 10%)

All Low priority, all single-user scope. Subcategories are billing_invoice (12) and compliance_audit (7) — meaning these are mostly customers asking about charges or audit/compliance obligations. `root_cause_class` = design_gap throughout, indicating documentation or UI clarity gaps. Median resolution 70 min despite low urgency, likely due to research required.

---

## 6. Performance Degradation (n=22, 9%)

All High priority, median resolution 140 min — the slowest category. Subcategory is `performance_query` (20/22). `root_cause_class` shows regression_from_release (12) and infrastructure_failure (6) as the key drivers. 15/22 affect the entire_tenant and 5 affect multiple users. `affected_component`: infrastructure_platform (5) and dashboard_analytics (5).

---

## 7. Configuration Errors (n=13, 5%)

Mostly auth_and_sso (5) and access_permission (2) misconfiguration. `root_cause_class` is predominantly misconfiguration (10/13). 7/13 lead to `service_completely_blocked`. Mix of Critical (3), High (6), and Medium (4) priorities; median resolution 75 min.

---

## 8. Billing Issues (n=8, 3%) and Security Incidents (n=6, 2%)

**Billing:** Subcategory is exclusively billing_invoice. `business_impact_signal` is mostly `revenue_or_payment_at_risk` (6/8); `root_cause_class` = data_integrity (4). 4/8 are Critical priority; median resolution 93 min.

**Security:** All Critical priority; 5/6 are `unknown_or_under_investigation` root cause (`root_cause_class`). `business_impact_signal` shows `data_loss_or_exposure` (5/6). Affected component is security_access_control (6/6). These are the highest-risk tickets despite the smallest volume.

---

## 9. Cross-Cutting Patterns

| Dimension | Key Finding |
|---|---|
| Volume driver | Bugs + feature requests = 57% of all tickets |
| Urgency driver | Outages, billing issues, and security incidents are predominantly Critical |
| Slowest to resolve | Performance degradation (median 140 min) |
| Widest blast radius | Outages and performance degradation are mostly entire-tenant scope |
| Root cause concentration | design_gap (102/250 = 41%) dominates overall, driven by feature requests + bugs |
| Most affected component | admin_console (49 tickets across bug + feature_request categories) |

---

## Method Note

TAPP-generated columns used in this report: **`issue_category`**, **`issue_subcategory`**, **`affected_component`**, **`impact_scope`**, **`business_impact_signal`**, **`root_cause_class`**. All six columns provided meaningful semantic signal. `issue_category` and `issue_subcategory` were the primary classification facets. `root_cause_class` and `business_impact_signal` added explanatory depth especially for bugs, outages, and security incidents. Original structured columns (`priority`, `resolution_minutes`, `channel`) were cross-checked against every TAPP facet to confirm consistency. No original column directly encoded issue type, so TAPP columns were essential rather than redundant for this query.
