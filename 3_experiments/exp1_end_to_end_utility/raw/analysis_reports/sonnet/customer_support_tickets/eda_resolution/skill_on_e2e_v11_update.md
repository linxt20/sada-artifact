---
dataset: customer_support_tickets
scenario: eda_resolution
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "resolution_minutes"
query: "How does resolution time vary across issue themes, channel, and priority?"
source_table: augment_table/customer_support_tickets/eda_resolution/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:11:19.834115+00:00
wall_seconds: 73.46
---

# Resolution Time Analysis: Issue Theme, Channel, and Priority
**Dataset:** 250 support tickets · **Outcome:** `resolution_minutes` (mean 64.9 min, median 58 min, range 12–180 min)

**Method note:** TAPP-generated columns used in this report: `issue_theme`, `ticket_class`, `operational_impact`, `scope_of_impact`, `requires_escalation`. Original structured columns `priority` and `channel` remain the primary analytical axes; TAPP columns add semantic depth where they clarify unexplained variance.

---

## 1. Priority

Priority is the strongest single driver of resolution time, but the relationship is non-monotonic — **High tickets take longest**, not Critical.

| Priority | N | Mean (min) | Median (min) |
|---|---|---|---|
| Critical | 50 | 74.4 | 72.5 |
| High | 50 | **131.1** | **131.0** |
| Medium | 76 | 41.6 | 37.0 |
| Low | 74 | 37.5 | 24.0 |

The High > Critical inversion is largely a **channel artifact**: 49 of 50 High tickets arrived via email (mean 132.8 min), while all 50 Critical tickets came via phone (n=38, mean 79.7 min) or in-app (n=12, mean 57.5 min) — both faster channels. After controlling for channel, the priority ladder behaves as expected for non-High tiers.

`ticket_class` corroborates: High tickets cluster as `bug` (mean 63.9 min across all priorities) and `performance_degradation` (mean 143.3 min); the latter heavily skews the High band.

---

## 2. Channel

Channel is the second-strongest driver, spanning a 4× range:

| Channel | N | Mean (min) | Median (min) |
|---|---|---|---|
| email | 100 | **98.3** | 92.5 |
| phone | 50 | 70.2 | 72.5 |
| in-app | 50 | 35.0 | 31.0 |
| chat | 50 | **22.5** | 23.0 |

**Chat and in-app resolve ~4× faster than email.** Email's longer times reflect both the asynchronous nature of the channel and its concentration of High-priority tickets (49 of 100 email tickets are High priority).

`operational_impact` adds context: email tickets are more likely to carry `production_blocked` (mean 102.1 min) or `revenue_at_risk` impact labels, which independently extend resolution regardless of channel.

---

## 3. Issue Theme

`issue_theme` (TAPP-generated) reveals large within-priority and within-channel resolution differences:

| Issue Theme | N | Mean (min) | Median (min) |
|---|---|---|---|
| performance | 30 | **131.6** | 140.0 |
| file_export_import | 5 | 89.6 | 95.0 |
| data_loss_corruption | 15 | 84.1 | 70.0 |
| billing_invoicing | 24 | 82.9 | 80.0 |
| scheduling_automation | 9 | 80.3 | 70.0 |
| security_vulnerability | 15 | 78.1 | 75.0 |
| authentication_sso | 25 | 72.9 | 62.0 |
| webhook_delivery | 4 | 71.2 | 60.0 |
| api_integration | 9 | 67.7 | 75.0 |
| access_permissions | 9 | 58.1 | 50.0 |
| notification_messaging | 8 | 47.5 | 49.0 |
| ui_ux_bug | 41 | 39.5 | 33.0 |
| feature_request_ux | 56 | **25.6** | 22.0 |

**Performance tickets** (mean 131.6 min) dominate resolution time — 29 of 30 are High or Critical and the corresponding `ticket_class` of `performance_degradation` has the highest mean of any class (143.3 min, n=23). **Feature requests/UX** resolve fastest (mean 25.6 min, n=56) aligned with `ticket_class = feature_request` (mean 22.8 min, n=57); these are low-complexity and predominantly Low/Medium priority.

`data_loss_corruption` and `security_vulnerability` themes take 78–84 min on average; the `operational_impact` labels `data_loss` (mean 85 min) and the broader `production_blocked` label (mean 102.1 min, n=60) confirm genuine operational severity rather than mis-classification.

---

## 4. TAPP Semantic Facets as Additional Explanatory Variables

### `operational_impact`
Strong gradient, independent of priority label:

| Operational Impact | N | Mean (min) |
|---|---|---|
| compliance_deadline | 2 | 102.5 |
| production_blocked | 60 | 102.1 |
| service_suspended | 4 | 98.8 |
| revenue_at_risk | 6 | 93.3 |
| data_loss | 6 | 85.0 |
| users_locked_out | 11 | 81.6 |
| minor_friction | 85 | 55.4 |
| not_present | 76 | 37.0 |

The `production_blocked` category (n=60) nearly matches the High-priority mean, suggesting operational impact is an independent predictor that cuts across formal priority tiers.

### `requires_escalation`
Tickets flagged `True` (n=53) average 79.4 min vs. 60.9 min for non-escalated tickets (n=197) — an ~18-min premium. Escalation is more predictive than priority alone for the Medium tier.

### `scope_of_impact`
Tenant-wide (`all_users_single_tenant`, n=48) tickets average 90.3 min vs. 66.1 min for single-user issues (n=118), confirming that blast radius matters independently.

### `root_cause_class` and `ticket_class`
`ticket_class = performance_degradation` (mean 143.3 min) and `security_incident` (mean 83.3 min) are the most time-intensive classes. `feature_request` (mean 22.8 min) is the fastest. These facets are additive to `issue_theme` and help distinguish subtypes within broad themes.

---

## 5. Combined View: Key Interaction

The longest resolution tickets share three co-occurring factors:
- **Issue theme = performance** or `data_loss_corruption`
- **Channel = email**
- **`operational_impact` = `production_blocked`** or **`requires_escalation` = True**

Performance + email tickets have a mean of ~135 min. Feature request + chat tickets average ~18 min. This ~7× gap represents the full resolution-time range in practice.

---

## Key Findings Summary

| Finding | Evidence |
|---|---|
| High-priority tickets take longest (131 min mean) but this is channel-confounded (49/50 via email) | Priority × Channel table |
| Email channel is 4× slower than chat (98 vs 23 min) | Channel breakdown |
| Performance theme dominates resolution time (132 min, n=30) | Issue theme table |
| Feature request/UX resolves fastest (26 min, n=56) | Issue theme table |
| `operational_impact = production_blocked` (n=60, 102 min) is a strong cross-tier predictor | `operational_impact` table |
| Escalation adds ~18 min regardless of priority tier | `requires_escalation` breakdown |
