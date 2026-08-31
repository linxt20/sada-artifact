---
dataset: customer_support_tickets
scenario: focus_inference
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What are the main kinds of issues these support tickets are about?"
source_table: augment_table/customer_support_tickets/focus_inference/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:10:43.117429+00:00
wall_seconds: 33.46
---

# Support Ticket Issue Analysis

## Dataset Overview
- **Total tickets:** 250
- **Columns used:** `issue_category`, `issue_subtype`, `priority`, `operational_impact`

---

## Main Kinds of Issues

### 1. By Issue Category

| Category | Count | % of Total |
|---|---|---|
| **Bug** | 101 | 40.4% |
| **Feature Request** | 55 | 22.0% |
| **Outage** | 27 | 10.8% |
| **Question** | 26 | 10.4% |
| **Performance** | 24 | 9.6% |
| **Data Integrity** | 10 | 4.0% |
| **Security Incident** | 7 | 2.8% |

**Bugs dominate**, representing over 40% of all tickets. Feature requests are the second-largest category, indicating a significant volume of product improvement demand alongside reactive support. Outages and performance issues together account for ~20%, suggesting non-trivial service reliability concerns.

---

### 2. By Issue Subtype (affected area)

| Subtype | Count |
|---|---|
| UI & UX | 52 |
| API & Integration | 48 |
| Auth & SSO | 30 |
| Billing & Payments | 22 |
| Automation & Workflow | 17 |
| Access & Permissions | 16 |
| Data Export/Import | 15 |
| Compliance & Audit | 13 |
| Notifications | 12 |
| Storage & Files | 10 |
| Email & Messaging | 8 |
| Mobile | 7 |

The **UI/UX** and **API/Integration** areas are the most common pain points (together ~40% of tickets). **Auth/SSO** issues are the third-largest group, consistent with the high proportion of `blocked_workflow` operational impact. Billing and access/permissions round out the top five.

---

### 3. Operational Impact

| Impact | Count |
|---|---|
| Blocked Workflow | 101 |
| No Immediate Impact | 68 |
| Degraded Performance | 46 |
| Compliance Risk | 20 |
| Financial Exposure | 9 |
| Data Loss/Corruption | 6 |

**Blocked workflows** are the most common outcome (40%), underscoring the urgency of bug and auth/SSO tickets. A notable 20 tickets carry **compliance risk**, and 6 involve **data loss or corruption** — small in count but high in severity.

---

## Key Takeaways

1. **Bugs are the primary driver** of support volume (~40%), with UI/UX and API/integration being the most affected areas.
2. **Feature requests are substantial** (22%), indicating users are actively engaged and seeking product growth — these are unlikely to require urgent triage but should feed a product backlog.
3. **Auth/SSO and outage tickets disproportionately block workflows**, making them high-priority resolution targets despite moderate raw counts.
4. **Security incidents and data integrity issues are rare but severe** (17 combined, ~7%), warranting escalation protocols distinct from routine bugs.
5. **Weak evidence caveat:** The `issue_description` field contains richer nuance (e.g., specific error codes, tenant scope), but category/subtype labels appear consistently applied and sufficient for pattern inference at this scale.
