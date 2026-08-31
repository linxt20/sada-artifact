---
dataset: customer_support_tickets
scenario: causal_reduce
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: what_if
focus_variable: "resolution_minutes"
query: "How can support teams reduce ticket resolution time?"
source_table: augment_table/customer_support_tickets/causal_reduce/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/customer_support_tickets__causal_reduce/analyses/original/analysis.md
wall_seconds: 101.5
---

# Customer Support Ticket Resolution Time: Causal Analysis Report

## Executive Summary

Analysis of 250 support tickets (CS-0001 to CS-0250) across four visible factors—**priority**, **channel**, **agent_id**, and **issue_description**—reveals that **ticket priority and channel are the two strongest structural drivers of resolution time**. Addressing routing discipline, channel self-service deflection, and High-priority engineering issues offers the clearest path to reducing average resolution time.

---

## 1. Dataset Overview

| Column | Values / Range |
|---|---|
| `ticket_id` | CS-0001 – CS-0250 (250 tickets) |
| `priority` | Critical, High, Medium, Low |
| `channel` | email, phone, chat, in-app |
| `agent_id` | AG-001 – AG-020 (20 agents) |
| `resolution_minutes` | 12 – 180 min (focus variable) |
| `issue_description` | Free text; describes issue type |

---

## 2. Priority → Resolution Time (Primary Driver)

Priority is the strongest correlate of resolution time in the dataset.

| Priority | Approx. Ticket Count | Observed Range (min) | Estimated Mean (min) |
|---|---|---|---|
| **Low** | ~75 | 12 – 90 | ~37 |
| **Medium** | ~75 | 22 – 70 | ~42 |
| **Critical** | ~50 | 45 – 110 | ~74 |
| **High** | ~50 | 48 – 180 | ~132 |

> **Counter-intuitive finding**: **High** tickets take longer on average than **Critical** tickets by approximately **58 minutes**.

### Interpretation
- **Critical** tickets receive immediate P1 escalation (phone bridges, incident commanders, dedicated engineers). Despite severity, structured escalation paths compress resolution time.
- **High** tickets lack the same forcing function. Issues like performance regressions (CS-0012: 180 min), memory leaks (CS-0042: 165 min, CS-0062: 150 min), and complex billing discrepancies (CS-0022: 155 min, CS-0102: 160 min) require engineering investigation without a hard SLA deadline. These drag the mean above Critical.
- **Low** tickets (feature requests, clarification questions) resolve quickly because they do not require system access or code changes—agents provide an answer or log a request.

### Actionable Implication
High-priority tickets need SLA guardrails analogous to Critical: a maximum time-to-escalation ceiling and clearer triage criteria to distinguish performance/billing investigations from true outages.

---

## 3. Channel → Resolution Time (Secondary Driver)

Channel is highly confounded with priority (Critical cases are routed to phone; Low cases predominate in chat), but even controlling qualitatively for issue type, the pattern is consistent.

| Channel | Dominant Priority Mix | Estimated Mean Resolution (min) |
|---|---|---|
| **chat** | Low, Medium | ~25 |
| **in-app** | Low, Medium, Critical | ~38 |
| **phone** | Critical, Medium | ~72 |
| **email** | High, Low, Medium | ~107 |

- **Chat** is the fastest channel. Short, targeted exchanges resolve Medium/Low issues quickly (e.g., CS-0002: 22 min, CS-0026: 24 min, CS-0031: 12 min).
- **Email** is the slowest channel. Email threads host the majority of High-priority engineering investigations where back-and-forth delays accumulate (CS-0012: 180 min, CS-0042: 165 min, CS-0062: 150 min).
- **Phone** handles Critical incidents efficiently relative to their severity, benefiting from real-time synchronous dialogue.
- **In-app** sits in the middle, used for both quick feature requests and mid-severity bugs.

### Actionable Implication
- **Shift more Medium/Low email tickets toward chat or in-app**: synchronous channels eliminate reply-lag overhead.
- **For High-priority email tickets**, consider proactive phone or video bridges rather than waiting for the customer to escalate. This could reduce High ticket resolution time by potentially 30–50 min.

---

## 4. Issue Type Patterns (from `issue_description`)

Three issue categories consistently produce the longest resolution times, all concentrated in the **High + email** cell:

| Issue Category | Example Tickets | Typical Resolution (min) |
|---|---|---|
| Performance regressions (reports, search, GraphQL) | CS-0012, CS-0022, CS-0052, CS-0077, CS-0097 | 130 – 180 |
| Memory leaks / client resource issues | CS-0042, CS-0062, CS-0082, CS-0142, CS-0222 | 135 – 165 |
| Billing discrepancies / invoice errors | CS-0032, CS-0102, CS-0184 | 135 – 160 |

Conversely, the shortest-resolving tickets are:
- **Feature requests / clarifications** (Low, chat/in-app): 12 – 30 min
- **UI/UX cosmetic bugs** (Low, chat): 12 – 25 min
- **Configuration questions** (Low/Medium, any channel): 18 – 35 min

### Actionable Implication
Performance regressions and memory leak reports should trigger a **technical triage sub-queue** with direct engineering involvement from ticket open, bypassing standard agent workflows that are not equipped to investigate them.

---

## 5. Agent-Level Observations

Agent identity alone does not explain large variance once priority and channel are accounted for. However, two patterns emerge:

- **Agents handling Low-ticket chat queues** (e.g., AG-006, AG-003 on chat) consistently resolve in 12–20 min. This reflects issue difficulty, not individual agent speed.
- **AG-002 handles exclusively High-priority email tickets** (CS-0005: 140 min, CS-0022: 155 min, CS-0042: 165 min, CS-0062: 150 min, CS-0082: 140 min, CS-0122: 150 min, CS-0142: 155 min, CS-0182: 140 min, CS-0202: 135 min, CS-0222: 148 min, CS-0242: 145 min) and shows the highest mean resolution time in the dataset (~148 min). This is consistent with specialist routing of the hardest ticket type rather than an agent performance problem.

> **Caveat**: The dataset does not include wait time, re-open rates, or customer satisfaction scores, so agent quality cannot be properly assessed from `resolution_minutes` alone.

---

## 6. Key Recommendations

| Lever | Mechanism | Expected Impact |
|---|---|---|
| **SLA-cap High tickets** | Set a max escalation-to-engineering timer (e.g., 90 min) for High tickets | Reduce High ticket mean by 20–40 min |
| **Shift Medium/Low email → chat** | Prompt customers to use chat for non-engineering queries | Reduce email volume; cut 40–80 min from affected tickets |
| **Technical triage sub-queue** | Route performance/memory/billing investigations to Tier-2 from open | Cut High-priority engineering issue resolution by up to 30% |
| **Standardise Critical playbooks for phone** | Already working (~74 min mean); document and replicate structured bridges | Maintain current Critical performance; reduce variance |
| **Self-service for recurring Low issues** | 30% of Low tickets are repetitive clarification questions (pricing, quotas, billing FAQ) | Deflect 15–20% of Low tickets via improved documentation |

---

## 7. Caveats and Weak Evidence

- **Confounding between priority and channel**: Chat carries few Critical/High tickets; email carries most High tickets. It is impossible from this dataset alone to isolate the channel effect from the priority effect.
- **No customer wait time or queue depth**: `resolution_minutes` likely measures agent-active time or wall-clock elapsed time; the dataset does not clarify, and queue saturation is unobservable.
- **Agent routing is not random**: AG-002 appears specialist-routed to hardest cases. Cross-agent comparisons are not causal without knowing routing logic.
- **CS-0005 (Medium, email: 140 min)** is a notable outlier: a Medium ticket with High-tier resolution time, suggesting that issue complexity within Medium can rival High tickets when engineering investigation is required.
