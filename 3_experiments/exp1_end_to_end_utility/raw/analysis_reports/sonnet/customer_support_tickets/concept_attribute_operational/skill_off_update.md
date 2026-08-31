---
dataset: customer_support_tickets
scenario: concept_attribute_operational
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "operational_burden"
query: "What customer issues create the most support burden?"
source_table: augment_table/customer_support_tickets/concept_attribute_operational/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:05:32.254522+00:00
wall_seconds: 35.64
---

# Customer Support Burden Analysis

## Dataset Overview

- **250 tickets** across 11 issue categories, with two key burden metrics: `burden_score` (composite) and `resolution_minutes`.

---

## Top Burden Categories

### By Total Burden Score

| Issue Category | Ticket Count | Total Burden Score | Mean Burden Score | Mean Resolution (min) |
|---|---|---|---|---|
| **other** | 52 | 1,086 | 20.9 | 69.8 |
| **authentication** | 34 | 754 | 22.2 | 65.1 |
| **feature_request** | 57 | 535 | 9.4 | 41.9 |
| **billing** | 19 | 444 | 23.4 | 84.9 |
| **data** | 15 | 356 | 23.7 | 75.6 |
| **performance** | 11 | 348 | 31.6 | 124.2 |
| **outage** | 11 | 311 | 28.3 | 70.2 |
| **integration** | 12 | 294 | 24.5 | 73.1 |

---

## Key Findings

### 1. Authentication — High Volume, High Total Burden
Authentication is the single most burdensome *classifiable* category, with **34 tickets**, a mean burden score of **22.2**, and **753 total burden points**. It also carries the highest Critical-ticket count among non-outage categories (11 Critical). Mean resolution time is 65 minutes. Session drops, SSO misconfigurations, and login failures dominate the descriptions.

### 2. Performance — Highest Per-Ticket Severity
Despite only 11 tickets, performance issues carry the **highest mean burden score (31.6)** and by far the **highest mean resolution time (124 minutes)**. All 11 are High or Medium priority — none are Critical, but the per-ticket cost is the greatest of any category. Slow dashboards and query timeouts are recurring themes.

### 3. Outage — High Urgency, Concentrated Risk
Outages (11 tickets) have a mean burden of **28.3** and 7 out of 11 are **Critical priority**. Individual outage tickets represent the largest single-event impact, even though total volume is low. These generate the most intense agent escalations and require RCAs.

### 4. Billing — Moderate Volume, Long Resolution
Billing (19 tickets) has the **highest mean resolution time (84.9 minutes)** among mid-volume categories and a mean burden of **23.4**. Six are Critical (likely involving finance deadlines), making it disproportionately urgent relative to its ticket count.

### 5. Feature Requests — High Volume, Low Per-Ticket Burden
Feature requests are the **most numerous category (57 tickets)**, but their mean burden score is the lowest at **9.4** and mean resolution is only 42 minutes. Despite high volume, they contribute relatively little individual pressure — though their aggregate burden (535) is third highest.

### 6. "Other" Category — Opaque but Significant
The `other` category has 52 tickets and the **highest total burden (1,086)**. This likely represents miscategorized or edge-case tickets. It warrants auditing and reclassification to surface hidden high-burden issue types.

---

## Summary Table: Burden Tiers

| Tier | Categories | Key Driver |
|---|---|---|
| 🔴 High per-ticket burden | Performance, Outage, Billing | Severity + long resolution |
| 🟠 High total burden | Authentication, Other | Volume × moderate severity |
| 🟡 Mixed | Data, Integration, Account, Access | Small samples, moderate scores |
| 🟢 Low per-ticket burden | Feature Requests, UI/UX | Low priority, fast to handle |

---

## Caveats

- The `other` category (52 tickets) inflates totals but lacks actionable signal without reclassification.
- Performance and outage conclusions rest on small samples (11 tickets each) — patterns may shift with more data.
- `burden_score` methodology is not documented in the dataset; it appears to incorporate priority and resolution time but its exact formula is unknown.

---

## Recommendations

1. **Prioritize authentication self-service tooling** (e.g., SSO diagnostics, session management docs) to reduce the highest-volume burden source.
2. **Invest in performance monitoring/alerting** to catch issues before they escalate — per-ticket cost is the highest.
3. **Streamline billing resolution workflows** to reduce the 85-minute average handle time.
4. **Audit the "other" category** to identify hidden high-burden issue types.
