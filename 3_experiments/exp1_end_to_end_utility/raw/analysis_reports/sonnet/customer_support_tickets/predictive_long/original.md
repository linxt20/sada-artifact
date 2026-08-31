---
dataset: customer_support_tickets
scenario: predictive_long
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "resolution_minutes"
query: "What signals suggest a support ticket will take longer to resolve?"
source_table: augment_table/customer_support_tickets/predictive_long/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/customer_support_tickets__predictive_long/analyses/original/analysis.md
wall_seconds: 76.06
---

# Customer Support Ticket Resolution Time — Signal Analysis

## Dataset Overview

The dataset contains **250 support tickets** (`CS-0001`–`CS-0250`) with five columns:
`ticket_id`, `priority`, `channel`, `agent_id`, `resolution_minutes`, and `issue_description`.
The target variable is **`resolution_minutes`** (observed range: **12–180 minutes**).

---

## 1. Priority Level (Strongest Structural Signal)

Priority is the single most predictive structured field:

| Priority | Typical Range (min) | Notable Examples |
|----------|--------------------|-|
| **Low** | 12–30 (feature requests/questions); 55–90 (billing/compliance) | CS-0011: 14 min; CS-0012 n/a (High) |
| **Medium** | 22–65 | CS-0002: 22 min; CS-0050: 65 min |
| **High** | 95–180 | CS-0012: 180 min; CS-0042: 165 min; CS-0062: 150 min |
| **Critical** | 45–110 | CS-0003: 65 min; CS-0009: 110 min |

**Key finding:** `High` tickets resolve *slower* on average than `Critical` tickets. Critical issues appear to receive immediate escalation that compresses resolution time; High tickets are serious but lack the urgency override, leading to longer queues. `High` tickets involving performance degradation, billing anomalies, or memory leaks consistently hit 120–180 min. 

**Exception:** Some Low tickets (e.g., CS-0015: 90 min, CS-0135: 90 min) take as long as High tickets when they involve contract/legal questions requiring cross-team consultation.

---

## 2. Channel (Moderate Signal)

| Channel | Typical Resolution | Interpretation |
|---------|-------------------|----------------|
| **chat** | 12–33 min | Synchronous, real-time — fastest channel |
| **in-app** | 14–70 min | Often simpler UI bugs or feature requests |
| **phone** | 36–110 min | Real-time but often involves complex escalation |
| **email** | 50–180 min | Async, highest variance; slowest for complex issues |

Tickets arriving via **email** and flagged **High** form the slowest cluster (e.g., CS-0012, CS-0022, CS-0042, CS-0052, CS-0062 — all 145–180 min). The combination of asynchronous communication and technical complexity appears multiplicative.

**Exception:** Phone-channel Critical tickets can resolve quickly (CS-0003: 65 min, CS-0029: 60 min) when the agent has direct escalation paths.

---

## 3. Issue Type Signals from Descriptions

The `issue_description` field reveals the strongest predictors of long resolution:

### 3a. Performance Degradation / Regression (→ 115–180 min)
Tickets describing measurable slowdowns tied to a specific release/migration are consistently the longest:
- CS-0012 (High/email): "30 percent slowdown on report generation… query that ran in 8 seconds now takes 26" → **180 min**
- CS-0042 (High/email): "Severe lag… scrolling stutters and the UI freezes" → **165 min**
- CS-0052 (High/email): "connection pool exhaustion… 503s" → **145 min**
- CS-0022 (High/email): "search bar… 6 to 9 seconds after elasticsearch version bump" → **155 min**

Signal phrases: *slowdown*, *degraded*, *regressed*, *latency*, *timeout*, *engineering investigation*.

### 3b. Memory Leaks / Resource Exhaustion (→ 130–165 min)
- CS-0062 (High/email): "memory consumption over 3 GB… macOS swap pressure" → **150 min**
- CS-0082 (High/email): "Loading workspace with 12,000 automations takes over 40 seconds" → **140 min**
- CS-0142 (High/email): "steady memory increase… worker restart loops every 20 minutes" → **155 min**

### 3c. Billing / Financial Discrepancies (→ 90–180 min)
- CS-0012 replicated in billing context: CS-0032 (High/email): "2.3M vs 1.8M API call discrepancy" → **135 min**
- CS-0001 (High/email): duplicate invoice line item → **95 min**
- CS-0049 (Critical/phone): double-charged 312 users → **95 min**

These require cross-team validation (engineering + finance) which extends resolution.

### 3d. Large-Scale / Multi-User / Tenant-Wide Impact (→ 65–110 min)
Descriptions mentioning "all users", "entire tenant", "480 active users locked out", or large record counts:
- CS-0009 (Critical/phone): "480 active users locked out" → **110 min**
- CS-0027 (High/email): "18,000 product SKUs… half the catalogue inconsistent" → **105 min**
- CS-0064 (Critical/phone): "sales demo in 45 minutes… tenant suspended" → **100 min**

### 3e. Security / Data Exposure (→ 70–95 min)
- CS-0139 (Critical/phone): session fixation in pen test → **75 min**
- CS-0189 (Critical/phone): data exposure via share link → **75 min**
- CS-0244 (Critical/phone): API keys in plaintext in error response → **85 min**

Security tickets have moderate-to-long resolution because they require careful forensic review before closure.

### 3f. Feature Requests / UX Suggestions / Simple Questions (→ 12–30 min)
The fastest-resolving tickets are Low-priority feature requests or clarifying questions (e.g., dark mode, keyboard shortcuts, wishlist items): CS-0011: 14 min, CS-0021: 16 min, CS-0031: 12 min, CS-0051: 13 min.

---

## 4. Agent Assignment (Weak-to-Moderate Signal)

Certain agents consistently handle specific ticket types and channels:
- **AG-002** (email): handles High tickets; median ~145–155 min — likely reflects complexity routing, not agent skill.
- **AG-003** (chat/Low): handles simple feature requests; median ~15–19 min.
- **AG-011**, **AG-014** (phone/Critical): handle outage bridges; 70–110 min.

Agent ID alone is a **weak signal** — it conflates ticket routing with agent performance. It is more useful as a proxy for *ticket type routing* than as a standalone predictor.

---

## 5. Composite Risk Signals

Tickets combining multiple factors are most at risk for long resolution:

| Risk Factor Combination | Expected Resolution |
|------------------------|---------------------|
| High priority + email + performance regression | **140–180 min** |
| High priority + email + memory leak | **130–165 min** |
| High priority + email + billing discrepancy | **95–180 min** |
| Critical + phone + tenant-wide outage | **65–110 min** |
| Low priority + email + compliance/legal question | **55–90 min** |
| Low priority + chat + feature request | **12–30 min** |

---

## 6. Weak Evidence / Exceptions to Note

- **Critical ≠ slowest**: The urgency override for Critical tickets can compress resolution below High tickets. CS-0034 (Critical/in-app): 45 min; CS-0054 (Critical/in-app): 50 min.
- **Low priority can be slow**: Contract, compliance, and legal clarification tickets (Low priority) sometimes take 65–90 min — rivaling some Medium tickets — because they require external approvals.
- **Description length alone** is not directly observable as a column, but longer descriptions with technical specifics (stack traces, version numbers, large-scale impact) are empirically associated with longer resolution.

---

## Summary

The strongest predictors of longer resolution time are:

1. **`priority = High`** (not Critical) — High tickets lack the urgency override that fast-tracks Critical tickets.
2. **`channel = email`** combined with High priority — async channel prevents rapid back-and-forth.
3. **Issue type: performance regression, memory leak, or billing discrepancy** — evident in the `issue_description` via phrases like *slowdown*, *degraded*, *memory*, *billing discrepancy*, and references to engineering investigation.
4. **Scope of impact: multi-user, tenant-wide, or large-scale data operations** — indicated by user counts, record counts, or phrases like *all users*, *entire tenant*.
5. **Cross-team resolution needs** (security, finance, legal) — signals: *pen test*, *audit*, *finance close*, *contract*, *CFO*, *RCA required*.
