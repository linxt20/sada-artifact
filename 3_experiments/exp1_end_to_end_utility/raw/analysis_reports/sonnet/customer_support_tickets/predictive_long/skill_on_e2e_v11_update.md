---
dataset: customer_support_tickets
scenario: predictive_long
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "resolution_minutes"
query: "What signals suggest a support ticket will take longer to resolve?"
source_table: augment_table/customer_support_tickets/predictive_long/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:11:26.226649+00:00
wall_seconds: 61.91
---

# Signals That Suggest a Support Ticket Will Take Longer to Resolve

**Dataset:** 250 customer support tickets  
**Outcome variable:** `resolution_minutes` (mean 64.9 min, median 58 min, 75th pct 88.75 min, max 180 min)  
**"Long" ticket threshold (top quartile):** > 88.75 min (n = 63 tickets)

---

## Method Note

TAPP-generated columns used in this analysis: `ticket_category`, `product_area`, `is_active_outage`, `business_impact_type`, `urgency_driver`, `root_cause_mechanism`, `is_regression`, `affected_user_scope`, `involves_third_party_integration`, `involves_data_integrity_risk`, `has_security_or_compliance_dimension`, `workaround_available`.

---

## 1. Priority (Original Column) — Strongest Single Predictor

| Priority | Mean (min) | Median (min) | n |
|---|---|---|---|
| **High** | **131.1** | **131.0** | 50 |
| Critical | 74.4 | 72.5 | 50 |
| Medium | 41.6 | 37.0 | 76 |
| Low | 37.5 | 24.0 | 74 |

**High priority tickets take nearly 3× longer than Medium/Low.** The counterintuitive result — Critical resolves faster than High — suggests Critical tickets receive immediate triage resources (phone/live escalation) that accelerate closure, while High-priority tickets represent complex, escalated cases that are queued but not war-roomed.

---

## 2. Channel (Original Column) — Email Dramatically Slower

| Channel | Mean (min) | Median (min) | n |
|---|---|---|---|
| **Email** | **98.3** | **92.5** | 100 |
| Phone | 70.2 | 72.5 | 50 |
| In-app | 35.0 | 31.0 | 50 |
| Chat | 22.5 | 23.0 | 50 |

Email tickets average 4.4× longer than chat. Email captures asynchronous, document-heavy issues (billing disputes, security reviews) that inherently require more back-and-forth cycles.

---

## 3. Is Regression (TAPP: `is_regression`) — High-Impact Flag

| is_regression | Mean (min) | Median (min) | n |
|---|---|---|---|
| **True** | **128.6** | **135.0** | 29 |
| False | 56.5 | 54.0 | 221 |

Regression tickets take **2.3× longer** than non-regressions. These are exclusively High-priority bugs (all 29 regressions are High or Medium priority), confirming the signal is additive to priority: High + regression averages 139.8 min vs. High non-regression at 123.1 min (n=24 vs. n=26).

---

## 4. Ticket Category (TAPP: `ticket_category`)

| Category | Mean (min) | Median (min) | n |
|---|---|---|---|
| **performance_degradation** | **142.1** | 140.0 | 24 |
| data_loss | 89.0 | 95.0 | 5 |
| billing_inquiry | 85.2 | 82.5 | 20 |
| security_incident | 83.3 | 82.5 | 6 |
| configuration_question | 73.1 | 65.0 | 17 |
| access_auth | 71.0 | 68.5 | 16 |
| outage | 65.0 | 62.5 | 16 |
| bug | 60.4 | 48.0 | 91 |
| feature_request | 22.5 | 22.0 | 55 |

**Performance degradation** is the slowest category (142 min mean), often requiring infrastructure-level investigation. **Feature requests** close fastest (22.5 min) as they require no troubleshooting.

---

## 5. Affected User Scope (TAPP: `affected_user_scope`)

| Scope | Mean (min) | Median (min) | n |
|---|---|---|---|
| **entire_tenant** | **96.1** | 85.0 | 73 |
| subset_of_tenant | 68.6 | 52.0 | 32 |
| single_user | 58.2 | 50.0 | 79 |
| not_specified | 33.9 | 25.5 | 62 |

Tenant-wide issues average 65% longer than single-user issues (96.1 vs. 58.2 min), consistent with the coordination overhead of blast-radius incidents.

---

## 6. Root Cause Mechanism (TAPP: `root_cause_mechanism`)

| Root Cause | Mean (min) | Median (min) | n |
|---|---|---|---|
| **unknown_root_cause** | **95.6** | 92.5 | 8 |
| infrastructure_or_capacity | 90.9 | 70.0 | 21 |
| data_corruption_or_inconsistency | 85.8 | 85.0 | 11 |
| regression_after_deploy | 79.2 | 61.0 | 64 |
| configuration_mismatch | 78.4 | 75.0 | 33 |
| race_condition_or_cache_bug | 61.5 | 52.0 | 27 |
| not_applicable | 37.1 | 25.0 | 78 |

**Unknown root cause** and **infrastructure/capacity** issues are the slowest — diagnosis uncertainty and backend access requirements both extend resolution time.

---

## 7. Data Integrity Risk & Security Dimension (TAPP)

| Flag | Mean (min) | Median (min) | n |
|---|---|---|---|
| `involves_data_integrity_risk` = True | 87.4 | 85.0 | 37 |
| `involves_data_integrity_risk` = False | 60.9 | 50.0 | 213 |
| `has_security_or_compliance_dimension` = True | 74.2 | 72.5 | 42 |
| `has_security_or_compliance_dimension` = False | 63.0 | 53.0 | 208 |

Data integrity risk adds ~26 min on average (+43% vs. baseline); security/compliance adds ~11 min (+18%). Both effects are consistent with mandatory review steps that add latency.

---

## 8. Business Impact Type (TAPP: `business_impact_type`)

| Business Impact | Mean (min) | n |
|---|---|---|
| **revenue_at_risk** | **88.4** | 11 |
| compliance_or_audit_deadline | 78.3 | 9 |
| customer_facing_downtime | 76.2 | 20 |
| internal_productivity_loss | 70.6 | 141 |
| no_explicit_impact | 43.2 | 67 |

Revenue and compliance impacts drive longer resolution — these cases require stakeholder escalation, approvals, or audit trails beyond pure technical fixes.

---

## 9. Active Outage & Third-Party Integration (TAPP)

| Flag | Mean (min) | n |
|---|---|---|
| `is_active_outage` = True | 78.9 | 51 |
| `is_active_outage` = False | 61.3 | 199 |
| `involves_third_party_integration` = True | 71.1 | 29 |
| `involves_third_party_integration` = False | 64.0 | 221 |

Active outages add ~18 min (+29%) over non-outage tickets. Third-party integration involvement is a weaker signal (+7 min, +11%), partially because many are resolved via escalation to the external vendor.

---

## 10. Urgency Driver (TAPP: `urgency_driver`)

| Urgency Driver | Mean (min) | n |
|---|---|---|
| financial_close_or_billing_risk | 89.4 | 9 |
| users_blocked_from_core_workflow | 80.4 | 52 |
| security_exposure_active | 72.1 | 12 |
| none_stated | 58.1 | 173 |

Tickets where users are blocked or face financial deadlines resolve slower — paradoxically, external urgency does not speed resolution when the problem itself is complex.

---

## Summary: Ranked Signals for Long Resolution Time

| Rank | Signal | Type | Mean Δ vs. baseline |
|---|---|---|---|
| 1 | Priority = High | Original | +66 min above overall mean |
| 2 | `is_regression` = True | TAPP | +64 min |
| 3 | Channel = Email | Original | +33 min |
| 4 | `ticket_category` = performance_degradation | TAPP | +77 min |
| 5 | `affected_user_scope` = entire_tenant | TAPP | +31 min |
| 6 | `root_cause_mechanism` = infrastructure_or_capacity | TAPP | +26 min |
| 7 | `involves_data_integrity_risk` = True | TAPP | +26 min |
| 8 | `business_impact_type` = revenue_at_risk | TAPP | +24 min |
| 9 | `is_active_outage` = True | TAPP | +14 min |
| 10 | `has_security_or_compliance_dimension` = True | TAPP | +11 min |

**Key takeaway:** The strongest predictors of long resolution are **High priority + regression flag + email channel + performance-degradation category + tenant-wide scope**. A ticket exhibiting all five of these signals will likely require 130–180 minutes to resolve. TAPP columns `is_regression`, `ticket_category`, `affected_user_scope`, and `root_cause_mechanism` add meaningful semantic signal beyond what the original structured fields alone provide.
