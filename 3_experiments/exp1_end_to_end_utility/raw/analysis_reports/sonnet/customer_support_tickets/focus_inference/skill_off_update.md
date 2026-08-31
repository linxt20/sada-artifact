---
dataset: customer_support_tickets
scenario: focus_inference
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What are the main kinds of issues these support tickets are about?"
source_table: augment_table/customer_support_tickets/focus_inference/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:05:58.394535+00:00
wall_seconds: 26.64
---

# Support Ticket Issue Analysis

**Dataset:** `sonnet__skill_off_update.csv` — 250 tickets across 9 issue categories.

---

## Main Issue Categories

| Issue Category | Count | % of Total | Dominant Priority |
|---|---|---|---|
| Feature Request | 69 | 27.6% | Low (61%) |
| Performance & Outage | 35 | 14.0% | High/Critical (69%) |
| Account & User Management | 33 | 13.2% | Medium (58%) |
| Billing & Invoicing | 32 | 12.8% | Mixed |
| Data & Reporting | 32 | 12.8% | Medium/High (69%) |
| Authentication & Access | 26 | 10.4% | Medium (58%) |
| Integration & API | 14 | 5.6% | Critical (43%) |
| Notification & Email | 7 | 2.8% | Medium/Low |
| Bug / Unexpected Behavior | 2 | 0.8% | Mixed |

---

## Key Findings

### 1. Feature Requests Dominate (28%)
The largest single category. These are overwhelmingly **Low priority** (42/69), reflecting enhancement asks (e.g., pinned navigation, competitor parity) rather than urgent problems. This volume may indicate a gap between product capabilities and user expectations.

### 2. Operational Problems Are the Most Urgent Cluster
Combining **Performance & Outage**, **Authentication & Access**, and **Integration & API** yields ~75 tickets (~30%). These carry the highest Critical/High priority concentrations:
- Performance & Outage: 69% High or Critical — e.g., 502 gateway errors, tenant-wide outages blocking presentations.
- Integration & API: 43% Critical — broken webhooks, API authentication failures affecting production workflows.

### 3. Account, Billing, and Data Issues Form a Mid-Tier Core
**Account & User Management**, **Billing & Invoicing**, and **Data & Reporting** together account for ~39% of tickets. Priority is distributed, suggesting these are routine but recurrent: seat provisioning errors, incorrect invoices, dashboard data discrepancies.

### 4. Niche but Notable
- **Notification & Email** (7 tickets) are all Low/Medium — missed digests, misdirected alerts.
- **Bug / Unexpected Behavior** has only 2 explicit entries, likely because bugs are being routed into more specific categories (e.g., Performance, Auth).

---

## Summary

The ticket mix reflects a **dual pressure**: a large volume of product improvement requests (Feature Requests) sitting alongside a significant proportion of high-urgency operational failures (outages, auth breaks, API failures). Billing and account management issues form a steady, moderate-priority background load. The near-absence of a standalone "Bug" category suggests inconsistent classification that may undercount defects.
