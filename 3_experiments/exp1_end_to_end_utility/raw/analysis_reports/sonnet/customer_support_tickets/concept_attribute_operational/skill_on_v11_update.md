---
dataset: customer_support_tickets
scenario: concept_attribute_operational
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "operational_burden"
query: "What customer issues create the most support burden?"
source_table: augment_table/customer_support_tickets/concept_attribute_operational/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:10:50.512555+00:00
wall_seconds: 61.84
---

# Customer Support Burden Analysis

**Dataset:** 250 tickets | **Focus:** Which customer issues create the most support burden

---

## Key Findings

Support burden is assessed across four dimensions: **ticket volume**, **resolution time**, **total agent-minutes consumed**, and **escalation / engineering involvement**.

### 1. Burden Summary by Issue Category

| Issue Category | Tickets | Avg Resolution (min) | Total Agent-Min | Engineering Required | High/Critical | Engineering Escalations |
|---|---|---|---|---|---|---|
| **bug_regression** | 82 | 62.8 | **5,152** | 100% | 25 | 29 |
| **performance_degradation** | 22 | **143.2** | 3,150 | 100% | 22 (all) | 19 |
| **incident_outage** | 33 | 70.8 | 2,336 | 100% | 30 (91%) | 22 |
| how_to_question | 25 | 68.9 | 1,723 | 0% | 0 | 0 |
| feature_request | 57 | 22.8 | 1,299 | 9% | 0 | 0 |
| auth_access | 11 | 62.2 | 684 | 100% | 4 | 4 |
| billing_payment | 7 | 94.3 | 660 | 57% | 6 | 0 |
| security_concern | 7 | 90.7 | 635 | 100% | 7 (all) | 0 |
| data_integrity | 6 | 95.8 | 575 | 100% | 6 (all) | 4 |

---

## Top Burden Categories

### 🔴 Bug Regressions — Highest Overall Burden
- **82 tickets** (33% of all tickets), consuming **5,152 total agent-minutes** — by far the largest share.
- **100% require engineering involvement**; 29 tickets escalated to engineering teams.
- 75 of 82 tickets (91%) had **no available workaround**, leaving users blocked until resolved.
- Operational impacts include `degraded_performance` (50 tickets) and `blocked_users` (27 tickets), plus 4 `data_loss_or_corruption` cases.
- 14 tickets affected an **entire tenant**, amplifying blast radius.

### 🔴 Performance Degradation — Highest Per-Ticket Cost
- Only 22 tickets but the **longest average resolution at 143 minutes** — more than double most categories.
- All 22 are High or Critical priority; all require engineering; 19 escalated.
- 12 tickets impacted an **entire tenant**, 6 affected a subset. No workarounds existed for any of them.
- Total agent-minutes (3,150) is second only to bug regressions.

### 🔴 Incident / Outages — Highest Urgency Concentration
- 33 tickets, with **30 (91%) rated High or Critical** — the highest urgency concentration of any category.
- 25 tickets caused **full tenant outages** (`entire_tenant` scope), including 6 `full_outage` and 5 `partial_outage` impacts.
- 22 engineering escalations; 5 P1 bridge calls were requested exclusively from this category.
- All 33 had no workaround available.

---

## Secondary Burden Sources

| Category | Key Concern |
|---|---|
| **how_to_question** (25 tickets) | Meaningful volume with 69-min avg resolution despite requiring *zero* engineering — suggests documentation/self-service gaps driving avoidable contacts. |
| **auth_access** (11 tickets) | 100% engineering required; all had no workaround; all users were blocked. Small volume but high per-ticket intensity. |
| **security_concern** (7 tickets) | All Critical/High; 100% engineering; all flagged as `security_escalation`. Low volume but non-negotiable priority. |
| **data_integrity** (6 tickets) | Highest average resolution (95.8 min); 5 of 6 involve `data_loss_or_corruption` — severe risk even at low count. |

---

## Feature Requests — Low Burden Despite High Volume
- 57 tickets (23% of volume) but only **22.8 min avg resolution** and 9% engineering involvement.
- They consume 1,299 total agent-minutes but create negligible operational impact.

---

## Conclusions & Caveats

**Bug regressions dominate by total agent effort** and should be the primary focus for burden reduction (via better QA/regression testing). **Performance degradation** is the costliest per incident and warrants infrastructure investment. **Incidents/outages**, while fewer in number, carry the highest urgency and widest user impact.

> **Weak evidence note:** `billing_payment`, `security_concern`, and `data_integrity` have very small sample sizes (6–7 tickets each), so their average resolution times and patterns should be interpreted cautiously. The `security_concern` `operational_impact` field shows "Unknown" for most tickets, limiting impact assessment for that category.
