---
dataset: customer_support_tickets
scenario: causal_handling
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: causal_attribution
focus_variable: "handling_time_gap"
query: "Why do handling times differ by channel and priority?"
source_table: augment_table/customer_support_tickets/causal_handling/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/customer_support_tickets__causal_handling/analyses/original/analysis.md
wall_seconds: 203.43
---

# Customer Support Tickets — Handling Time Analysis

## Dataset Overview

**250 tickets** across four channels (chat, email, in-app, phone) and four priority levels (Critical, High, Medium, Low). The focus variable is `resolution_minutes`. No agent-performance or SLA-clock columns exist; all conclusions are based on `priority`, `channel`, and `issue_description`.

---

## 1. Resolution Times by Priority

| Priority | n | Mean (min) | Range |
|---|---|---|---|
| **High** | 50 | **131.1** | 48–180 |
| **Critical** | 50 | **74.4** | 45–110 |
| **Medium** | 76 | **41.4** | 22–140 |
| **Low** | 74 | **37.5** | 12–90 |

**Key finding:** High priority takes the longest on average — nearly twice Critical's mean — while Medium and Low are comparable to each other. This counter-intuitive ordering is explained almost entirely by **channel confounding** (see §3).

---

## 2. Resolution Times by Channel

| Channel | n | Mean (min) | Range |
|---|---|---|---|
| **email** | 100 | **98.3** | 46–180 |
| **phone** | 50 | **70.2** | 60–110 |
| **in-app** | 50 | **34.6** | 18–70 |
| **chat** | 50 | **22.5** | 12–48 |

Channels span a **4× gap** in average handling time (email 98 min vs. chat 23 min). The within-channel ranges are comparatively tight, especially chat and in-app.

---

## 3. The Channel–Priority Confound (Core Explanation)

Priority and channel are **not independently distributed** in this dataset. Each priority level is routed almost exclusively to one or two channels:

| Priority | Channels observed | Dominant channel |
|---|---|---|
| Critical | phone (38), in-app (12) | phone |
| High | email (49), chat (1) | email |
| Medium | email, chat, in-app, phone | all four |
| Low | email (25), chat (24), in-app (25) | none (balanced) |

This near-perfect aliasing means:

- **High looks slow because it routes to email.** High/email mean = 133 min; the lone High/chat ticket resolves in 48 min. The single data point is not enough to isolate a true "priority effect" for High tickets.
- **Critical looks faster than High because it routes to phone and in-app.** Critical/phone mean ≈ 80 min; Critical/in-app mean ≈ 58 min — both faster than High/email.

Within each channel, the priority gradient is more intuitive where multiple priorities co-exist:

| Channel | Critical (mean) | Medium (mean) | Low (mean) |
|---|---|---|---|
| phone | 79.7 | 40.0 | — |
| email | — | 58.8 | 71.6 |
| in-app | 57.5 | 33.7 | 24.2 |
| chat | — | 27.8 | 15.9 |

Inside **in-app**: Critical (58 min) > Medium (34 min) > Low (24 min) — the expected ordering holds. Inside **phone**: Critical (80 min) > Medium (40 min). Inside **chat** and **email** only one priority per channel appears at scale, so within-channel priority comparison is limited.

---

## 4. Causal Factors Visible in the Data

### 4a. Issue complexity drives High/email duration
High-priority tickets routed to email consistently describe deep technical investigations: performance regressions, memory leaks, schema migrations, security certificate failures, and large-scale bulk-operation bugs. These require engineering escalation and asynchronous written follow-up — structurally slow regardless of urgency. Examples:
- CS-0012 (High/email, 180 min): 30% report-generation slowdown across 500 k-row datasets
- CS-0042 (High/email, 165 min): inbox virtualisation lag with 5 000+ conversations
- CS-0102 (High/email, 160 min): empty query results after data-residency migration

### 4b. Channel interaction mode caps handling speed
- **Chat** is synchronous and real-time; agents resolve issues while the customer waits. Tickets are predominantly Low or Medium (UI bugs, feature questions, minor UX friction), so both complexity and modality favour speed (mean 22.5 min).
- **In-app** widget tickets are similarly low-friction: feature requests, suggestions, and cosmetic bugs dominate the Low tier. Even Critical in-app tickets (e.g. webhook timeouts, blank dashboard canvases) resolve in ~58 min — faster than Critical phone tickets — possibly because the in-app channel captures more targeted, reproducible bug reports.
- **Email** allows lengthy asynchronous threads, attachments, and engineering referrals; this modality self-selects for complex or documentation-heavy tickets.
- **Phone** Critical tickets (mean 80 min) involve live outages and bridge calls, which add bridging-and-escalation overhead but still resolve faster than High/email because the live interaction forces focus.

### 4c. Issue type within Low priority
Low-priority email tickets (mean 71.6 min) take longer than Low chat (15.9 min) or Low in-app (24.2 min). Reading the descriptions reveals that Low/email tickets are predominantly **billing and pricing inquiries, compliance questions, and contract clarifications** — all requiring human research or legal sign-off before responding — whereas Low/chat and Low/in-app are almost exclusively **feature requests and UX suggestions** that can be acknowledged quickly.

---

## 5. Exceptions and Weak Evidence

- **CS-0005 (Medium/email, 140 min)** is a strong outlier for its priority — a data-pipeline BOM-character bug requiring engineering investigation. It inflates Medium/email's mean (58.8 min without it ≈ 56 min; minimal impact at this scale).
- **CS-0009 (Critical/phone, 110 min)** is the maximum for Critical, an Okta SSO lock-out of 480 users requiring a P1 bridge and a temporary auth bypass — an unusually complex critical incident.
- **High/chat** has only **1 ticket** (CS-0006, 48 min). No generalisation about handling time for that cell is possible.
- There is **no agent-ID performance control**; the 20 agents (AG-001–AG-020) are not analyzed because no breakdown by agent is visible in the summary, and agent assignment may co-vary with channel.
- The dataset does not include timestamps (open/close), so queue wait time vs. active-handling time cannot be separated.

---

## 6. Decision-Ready Summary

| Factor | Effect on `resolution_minutes` | Confidence |
|---|---|---|
| Channel routing (email vs. chat/in-app) | +75 min for email vs. chat | **Strong** (n=100 vs 50) |
| Priority-driven complexity (High issues are deep bugs) | +50–80 min above Critical for High/email | **Strong** within email |
| Synchronous (chat/in-app) vs. async (email/phone) mode | Async adds structural delay independent of complexity | **Strong** |
| Live-escalation overhead on Critical/phone | +20 min vs. Critical/in-app | **Moderate** (n=38 vs 12) |
| Issue type within Low (billing/compliance vs. UX requests) | +50 min for email vs. chat | **Moderate** |
| Individual agent skill | Not quantifiable from available data | **Weak** |

**Bottom line:** Channel modality and issue type are the primary drivers of handling time variation. Priority labelling appears to influence routing — and routing is what actually determines speed. Teams looking to reduce High-priority resolution time should examine whether complex High tickets can be partially resolved via chat (live troubleshooting) before transitioning to email for documentation.
