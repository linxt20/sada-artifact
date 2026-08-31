---
dataset: customer_support_tickets
scenario: causal_handling
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "handling_time_gap"
query: "Why do handling times differ by channel and priority?"
source_table: augment_table/customer_support_tickets/causal_handling/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:10:47.909373+00:00
wall_seconds: 81.84
---

# Why Do Handling Times Differ by Channel and Priority?
**Dataset:** `sonnet__skill_on_e2e_v11_update.csv` — 250 tickets, 14 columns (6 original + 8 TAPP-generated)  
**Outcome variable:** `resolution_minutes` (range 12–180, mean 64.9, median 58.0)

---

## 1. Headline Effects

### 1.1 By Priority

| Priority | n | Mean (min) | Median (min) |
|---|---|---|---|
| Critical | 50 | 74.4 | 72.5 |
| High | 50 | **131.1** | **131.0** |
| Medium | 76 | 41.6 | 37.0 |
| Low | 74 | 37.5 | 24.0 |

**High takes longest**, not Critical. The spread is enormous: High (131 min) is 3.5× Low (37.5 min).

### 1.2 By Channel

| Channel | n | Mean (min) | Median (min) |
|---|---|---|---|
| Chat | 50 | **22.5** | 23.0 |
| In-app | 50 | 35.0 | 31.0 |
| Phone | 50 | 70.2 | 72.5 |
| Email | 100 | **98.3** | 92.5 |

Chat resolves 4.4× faster than Email. Channel alone explains a large share of variance.

---

## 2. Why Priority Drives Handling Time

### 2.1 Technical Complexity (TAPP: `technical_complexity`)

`technical_complexity` is scored 1–5. It rises monotonically with priority and strongly predicts resolution time:

| Priority | Mean complexity | Mean resolution (min) |
|---|---|---|
| Low | 1.57 | 37.5 |
| Medium | 2.46 | 41.6 |
| Critical | 4.30 | 74.4 |
| High | 3.76 | 131.1 |

| Complexity score | Mean resolution (min) | n |
|---|---|---|
| 1 | 23.5 | 38 |
| 2 | 44.5 | 75 |
| 3 | 66.1 | 50 |
| 4 | 105.5 | 67 |
| 5 | 80.5 | 20 |

Correlation is clear through score 4. Score-5 tickets resolve somewhat faster than score-4, possibly because score-5 outages trigger rapid war-room responses.

### 2.2 Engineering Escalation (TAPP: `requires_engineering_escalation`)

Escalated tickets take **twice as long** (78.6 vs 38.7 min). Escalation rates by priority explain the ordering:

| Priority | Escalation rate | Mean resolution (min) |
|---|---|---|
| Low | 0% | 37.5 |
| Medium | 87% | 41.6 |
| High | 96% | 131.1 |
| Critical | 100% | 74.4 |

High and Critical both escalate nearly universally, yet High takes ~57 min longer than Critical. This points to issue **type** differences within priority tiers (see §3).

### 2.3 Operational Severity (TAPP: `operational_severity`)

| Severity | Mean resolution (min) | n |
|---|---|---|
| cosmetic | 30.7 | 13 |
| not_present (feature requests) | 37.9 | 77 |
| single_user_impaired | 53.5 | 63 |
| total_outage | 77.7 | 46 |
| partial_outage | 86.0 | 20 |
| degraded_performance | **136.5** | 31 |

`degraded_performance` is the slowest severity class. It maps predominantly to `issue_category = performance` (23 tickets, all in email channel). These are difficult to diagnose and reproduce — no single failure point triggers a war-room sprint the way a total outage does.

### 2.4 Workaround Availability (TAPP: `workaround_available`)

Tickets with `no_workaround` (n=164, mean 76.8 min) take about twice as long as those tagged `not_present` (feature requests with no applicable concept, n=76, mean 36.9 min). The 10 tickets where a customer found their own workaround still averaged 82.1 min, suggesting workaround discovery is itself a time-consuming step.

---

## 3. Why Channel Drives Handling Time

### 3.1 Issue Mix Routed to Each Channel

Channels attract fundamentally different ticket types:

| Channel | Top issue categories | Dominant complexity |
|---|---|---|
| Chat | feature_request (25), bug (23) | 1.74 avg |
| In-app | bug (15), feature_request (12) | 2.40 avg |
| Phone | outage (19), bug (13), security (6) | 3.80 avg |
| Email | bug (38), question (24), **performance (23)** | 3.09 avg |

- **Chat** is almost exclusively low-complexity feature requests and simple bugs → fast.
- **Phone** skews to outages and security incidents requiring immediate escalation (96% escalation rate).
- **Email** carries all 23 **performance** tickets (slow to diagnose) and 24 questions, inflating its average.

### 3.2 Technical Complexity and Escalation by Channel

| Channel | Mean `technical_complexity` | Escalation rate | Mean resolution (min) |
|---|---|---|---|
| Chat | 1.74 | 40% | 22.5 |
| In-app | 2.40 | 48% | 35.0 |
| Email | 3.09 | 72% | 98.3 |
| Phone | 3.80 | 96% | 70.2 |

Phone has the highest complexity and escalation rate, yet resolves faster than Email (70.2 vs 98.3 min). This is explained by issue type: phone-routed outages and security issues get immediate engineering priority. Email's performance/degradation tickets require iterative back-and-forth across asynchronous turns, extending calendar-time handling.

### 3.3 Scope and Blast Radius (TAPP: `scope_blast_radius`)

| scope_blast_radius | Mean resolution (min) | n |
|---|---|---|
| single_user | 50.1 | 138 |
| subset_of_users | 63.1 | 39 |
| single_tenant_all_users | 94.7 | 70 |
| all_tenants | 71.7 | 3 |

Wider blast radius → longer handling. Phone tickets are concentrated in `single_tenant_all_users` (outages), which drives their higher absolute time even though those are handled urgently.

### 3.4 Channel Effect Persists After Controlling for Escalation

Even within non-escalated tickets, Email (73.8 min) takes 4× Chat (18.2 min) — confirming the channel medium itself adds delay through asynchronous turns, not just ticket content.

---

## 4. Interaction: Priority × Channel

The cross-tab (rows = priority, columns = channel) is sparse due to routing patterns but illustrates key cells:

| Priority | Chat (min) | Email (min) | In-app (min) | Phone (min) |
|---|---|---|---|---|
| Critical | — | — | 57.5 | 79.7 |
| High | 48.0 | 132.8 | — | — |
| Medium | 27.8 | 58.8 | 35.2 | 40.0 |
| Low | 15.9 | 71.6 | 24.2 | — |

High/Email is the single worst-performing cell (132.8 min), driven by performance degradation tickets routed to email at high priority. Critical tickets are routed only to phone/in-app and resolve in 58–80 min.

---

## 5. Causal Summary

The following causal chain explains most of the variance:

1. **Priority → issue type composition** (Critical = outages; High = degraded performance; Low/Medium = feature requests/simple bugs).
2. **Issue type → technical complexity** (`technical_complexity` 1.57 for Low → 4.30 for Critical) and **escalation need** (0% for Low → 100% for Critical).
3. **Technical complexity + escalation → resolution time** (complexity-5 adds ~82 min over complexity-1; escalation adds ~40 min baseline).
4. **Channel selection is non-random**: customers self-select phone for urgent outages and use email for complex asynchronous issues. This makes channel a **proxy for issue type** rather than purely a medium effect.
5. **Email's asynchronous medium** adds independent delay: even controlling for escalation, email is 4× slower than chat, because each interaction loop adds latency.
6. **Workaround availability** (`workaround_available = no_workaround`) is concentrated in complex/high-priority tickets and adds further time when customers must wait for engineering fixes.

---

## 6. Method Note

**TAPP-generated columns used in this report:**  
`technical_complexity`, `requires_engineering_escalation`, `operational_severity`, `workaround_available`, `scope_blast_radius`, `root_cause_domain` (referenced implicitly via issue_category cross-check).  

Columns `customer_impact_type` and `issue_category` were cross-checked against original routing/priority fields and found largely redundant with `operational_severity` and the original `priority` column; they were not centered in the analysis but validated directional claims.
