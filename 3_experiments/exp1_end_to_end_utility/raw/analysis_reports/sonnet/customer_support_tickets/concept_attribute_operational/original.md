---
dataset: customer_support_tickets
scenario: concept_attribute_operational
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: faceted_decomposition
focus_variable: "operational_burden"
query: "What customer issues create the most support burden?"
source_table: augment_table/customer_support_tickets/concept_attribute_operational/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/customer_support_tickets__concept_attribute_operational/analyses/original/analysis.md
wall_seconds: 129.84
---

# Customer Support Burden Analysis
## Dataset: `customer_support_tickets` — 250 Tickets

---

## 1. Overview

The dataset contains **250 tickets** spanning four priority levels (`Critical`, `High`, `Medium`, `Low`) across four channels (`email`, `phone`, `chat`, `in-app`), handled by 20 agents (`AG-001` – `AG-020`). The key operational metric is **`resolution_minutes`** — the time to resolve each ticket — along with the free-text `issue_description`, which is the primary source for issue categorization.

**Priority distribution is balanced** (50 tickets each for Critical and Low; the remaining 150 split roughly equally between High and Medium), which suggests a dataset structured for balanced coverage rather than reflecting a natural incident distribution. Caution is warranted in treating priority counts as proportional to real-world frequency.

---

## 2. What Creates the Most Support Burden?

"Burden" is assessed across two dimensions visible in the data: **(a) resolution time** (time-in-queue cost per ticket) and **(b) priority/severity** (operational risk and escalation overhead). Issue categories are extracted from `issue_description`.

---

## 3. Issue Categories and Their Burden Profiles

### 3.1 Performance Regressions — **Highest Resolution Time, High Priority**

Tickets describing degraded query speed, API latency, search slowdowns, memory leaks, or client-side lag constitute roughly **15–18% of all tickets** and carry the highest resolution minutes among High-priority cases:

| Example Tickets | Issue | Resolution (min) |
|---|---|---|
| CS-0012 | 30% report generation slowdown (500k+ rows) | 180 |
| CS-0042 | Inbox freezes with 5,000+ conversations | 165 |
| CS-0062 | Desktop Electron client 3 GB memory use | 150 |
| CS-0022 | Knowledge base search 6–9 s after ES version bump | 155 |
| CS-0102 | Historical data returns empty post data-residency migration | 160 |
| CS-0142 | Back-end report worker crashes (memory leak, new pivot) | 155 |
| CS-0092 | Background indexing takes 18 h after tenant scale-up | 155 |
| CS-0052 | Connection pool exhaustion after schema migration | 145 |

These tickets **average ≈148 minutes** for High-priority performance cases and consistently require engineering escalation, giving them the heaviest per-ticket burden.

**Sub-pattern:** Post-deployment regressions are specifically costly — descriptions repeatedly mention that issues "began after" a specific release, schema migration, or index rebuild (CS-0022, CS-0052, CS-0082, CS-0097, CS-0112, CS-0137, CS-0162, CS-0197, CS-0217, CS-0237). This makes them a systemic rather than isolated cost.

---

### 3.2 Authentication & Access Failures — **Highest Priority, Broad User Impact**

Authentication issues (SSO/SAML failures, API key rejections, MFA problems, admin lockouts) account for the **largest share of Critical tickets** — approximately 14 out of 50 Critical tickets:

| Example Tickets | Issue | Priority | Resolution (min) |
|---|---|---|---|
| CS-0009 | Okta SSO rejects all logins (480 users locked out) | Critical | 110 |
| CS-0024 | All API calls return 401 despite valid key | Critical | 90 |
| CS-0064 | Tenant suspended (false positive) with demo in 45 min | Critical | 100 |
| CS-0164 | Admin MFA device lost, recovery pending 11 days | Critical | 95 |
| CS-0199 | Admin locked out via credential stuffing | Critical | 90 |
| CS-0059 | Admin account deleted by SCIM deprovisioning | Critical | 80 |

Auth failures create **multi-user, tenant-wide blockages** and require both technical triage and identity/security escalations. Their Critical classification means they consume disproportionate senior agent and on-call engineering time. High-priority auth cases (CS-0047, CS-0097, CS-0187, CS-0207, CS-0227) average ≈116 minutes.

**Burst risk:** Several tickets describe a single event locking out hundreds of users simultaneously (CS-0009: 480 users; CS-0204: 600 users at renewal risk), meaning one ticket can carry the operational weight of hundreds of user-side contacts.

---

### 3.3 Billing & Invoicing Errors — **Critical + High Priority, Finance-Escalation Overhead**

Billing anomalies appear throughout the dataset (≈8–10% of tickets) and generate outsized overhead because they require cross-functional coordination (finance, legal, engineering):

| Example Tickets | Issue | Priority | Resolution (min) |
|---|---|---|---|
| CS-0049 | Double-charged 312 end-users via Stripe | Critical | 95 |
| CS-0144 | Duplicate billing line items doubling Enterprise invoice | Critical | 90 |
| CS-0184 | 47 phantom users billed (seat inflation) | Critical | 85 |
| CS-0084 | Auto-retry failed silently → unexpected suspension | Critical | 90 |
| CS-0204 | Billing portal shows zero seats before renewal | Critical | 80 |
| CS-0017 | Invoice charged to deactivated card; dunning to ex-employee | High | 125 |
| CS-0032 | 500k API call billing discrepancy (potential unauthorized key) | High | 135 |

These tickets frequently involve **board-level reporting, credit memos, CFO escalations, and audit trails**, making resolution more complex than the `resolution_minutes` field alone may capture — downstream work continues after ticket close.

---

### 3.4 Integration & Webhook Failures — **High Critical Volume, Ops-Blocking**

Integration failures (webhooks, third-party syncs, OAuth) are the **most common Critical issue category** by raw count (~12 Critical tickets):

| Example Tickets | Issue | Priority | Resolution (min) |
|---|---|---|---|
| CS-0014 | Webhook 504 timeouts; warehouse cannot pick orders | Critical | 55 |
| CS-0044 | E-commerce order syncs failing (schema breaking change) | Critical | 85 |
| CS-0099 | Salesforce OAuth refresh token revoked unexpectedly | Critical | 75 |
| CS-0124 | Twilio outbound calls failing 100% (invalid auth token) | Critical | 80 |
| CS-0169 | Webhooks retried for acknowledged events; downstream rate-limiting | Critical | 65 |
| CS-0224 | All integrations down after OAuth secret rotation | Critical | 80 |
| CS-0229 | NetSuite duplicating journal entries (finance close at risk) | Critical | 60 |

Integration issues are operationally blocking — they halt downstream business processes (warehouse ops, finance close, SLA obligations). High-priority integration tickets (CS-0067, CS-0037, CS-0127, CS-0177) average ≈120 minutes.

---

### 3.5 Data Loss & Corruption Events — **Highest Severity, Low Frequency, Extreme Overhead**

Though less frequent (~6–7 Critical tickets), data loss events generate the most extreme escalation burden:

| Example Tickets | Issue | Priority | Resolution (min) |
|---|---|---|---|
| CS-0039 | Data loss after snapshot restore (wrong target) | Critical | 70 |
| CS-0089 | Production board with 4,300 cards deleted (retention dispute) | Critical | 80 |
| CS-0109 | Restore stuck for 36+ hours; modules unavailable | Critical | 70 |
| CS-0119 | Year-end audit export failed at 92% after 14 hours | Critical | 95 |
| CS-0189 | Confirmed data exposure via un-expiring share link | Critical | 75 |
| CS-0249 | Complete loss of historical analytics data | Critical | 95 |

Recorded `resolution_minutes` for these cases (60–95) likely **undercount true burden** — data recovery, forensic analysis, RCAs, and contractual communications extend far beyond ticket close.

---

### 3.6 UX/Product Bugs — **Highest Ticket Volume, Lower Severity**

Bugs such as broken modals, mis-behaving UI controls, export format errors, and editor glitches make up the **majority of Medium tickets** (≈40–50 Medium tickets) and resolve in 30–65 minutes. Individually lightweight, they represent the **broadest surface area** of the queue.

Notable higher-burden Medium examples:
- CS-0005: BOM character breaking Snowflake pipelines (140 min — outlier likely due to data engineering coordination)
- CS-0020: Password reset race condition (70 min; 1-in-10 failure rate means recurring tickets)
- CS-0063: Bulk-edit modal crashes with >100 rows (36 min but recurring)

These issues create **repeat-contact risk** when workarounds are imperfect or not communicated proactively.

---

### 3.7 Feature Requests & Billing Questions — **Low Resolution Time, High Volume**

Low-priority tickets (50 tickets) consist almost entirely of enhancement requests and informational billing/compliance queries. Resolution times cluster tightly between **12–27 minutes** (chat/in-app) and **55–90 minutes** (email), consistent with quick documentation lookups or standard "log and close" handling.

While individually cheap, they form a constant background load. Notably, several billing-clarification tickets hint at **documentation gaps** (CS-0007, CS-0025, CS-0055, CS-0065, CS-0075, CS-0095) that could be self-served with better content.

---

## 4. Channel and Priority Interaction

| Channel | Dominant Priority | Pattern |
|---|---|---|
| **phone** | Critical exclusively | All Critical tickets come via phone — phone is reserved for (or escalated to) the most urgent incidents |
| **email** | High | High-priority engineering/performance issues predominantly arrive by email, with the longest resolution times (avg ≈130 min) |
| **chat** | Medium/Low | Chat handles UX bugs and feature requests quickly (avg ≈28 min) |
| **in-app** | Mixed Medium/Critical | In-app channel handles both quick UX reports and escalated critical outages |

The **phone + Critical** pairing is perfectly consistent across all 50 Critical tickets, confirming that phone is the channel for the highest-impact triage. This means phone call volume is a reliable proxy for operational crisis load.

---

## 5. Resolution Time Summary by Burden Tier

| Tier | Priority | Avg Resolution (min) | Dominant Issue Types |
|---|---|---|---|
| **Highest burden** | Critical | ~74 | Auth failures, integration outages, data loss, billing emergencies |
| **High burden** | High | ~133 | Performance regressions, memory leaks, query slowdowns, webhook errors |
| **Moderate burden** | Medium | ~38 | UX/product bugs, export format issues, permission glitches |
| **Low burden** | Low | ~44* | Feature requests, billing questions, compliance queries |

*Low tickets have higher avg than Medium due to several documentation/legal inquiry emails that require research time (55–90 min) despite low urgency.

---

## 6. Key Findings and Prioritization

1. **Performance regressions are the single costliest High-priority issue type** by resolution minutes and engineering escalation frequency. Post-deployment regressions are a systemic pattern (~10–12 tickets explicitly blame a recent release or migration).

2. **Authentication failures drive the most Critical-tier volume** with the highest user-impact breadth. A single SSO outage can functionally multiply one ticket into hundreds of affected users.

3. **Billing errors require the most cross-functional coordination** and likely have the longest true resolution cycle (post-ticket follow-up with finance/legal), making their `resolution_minutes` an undercount.

4. **Integration and webhook failures** are the most operationally blocking — they halt downstream business processes and occur at a high Critical rate.

5. **Data loss/corruption events** are low-frequency but highest-severity; their recorded resolution time understates true effort.

6. **UX bugs** dominate by ticket count but carry moderate burden individually; repeat-contact risk from recurring bugs (e.g., race conditions, permission caching, session drops) is the main multiplier.

---

## 7. Caveats and Weak Evidence

- **Issue categories are inferred from free text** — no structured `issue_type` column exists. Classification is based on recurring keywords and patterns in `issue_description`.
- **`resolution_minutes` captures time-to-close, not total engineering effort** — Critical tickets often generate continued work (RCAs, forensics, credits) after closure.
- **Priority distribution is artificially balanced** (50 per tier), which prevents drawing conclusions about which issue type is most *frequent* in production — only about which carries highest per-ticket burden.
- The **20 agent IDs rotate regularly** across tickets without obvious specialization signals, so agent-level burden analysis is not meaningful from this data.
- Several tickets explicitly mention **multi-tenant impact** (e.g., CS-0054: "multiple tenants likely impacted"), meaning actual user-impact figures may be significantly higher than the single-ticket framing suggests.
