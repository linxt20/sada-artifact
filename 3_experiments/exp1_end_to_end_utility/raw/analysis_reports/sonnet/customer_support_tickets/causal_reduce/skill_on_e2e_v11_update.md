---
dataset: customer_support_tickets
scenario: causal_reduce
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: what_if
focus_variable: "resolution_minutes"
query: "How can support teams reduce ticket resolution time?"
source_table: augment_table/customer_support_tickets/causal_reduce/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:11:26.628692+00:00
wall_seconds: 100.52
---

# How Support Teams Can Reduce Ticket Resolution Time
**Dataset:** 250 customer support tickets | Outcome: `resolution_minutes` (mean 64.9 min, median 58 min, range 12–180 min)

---

## Method Note
TAPP-generated columns used in this report: `technical_complexity`, `operational_severity`, `request_type`, `issue_category`, `root_cause_domain`, `requires_external_dependency`, `actionability`, `escalation_signal`, `workaround_available`, `data_or_info_provided`. Columns `repro_reliability` and `affected_scope` were examined but provided weak or redundant signal and are not foregrounded. All claims are cross-checked against original structured columns (`priority`, `channel`, `agent_id`, `resolution_minutes`).

---

## 1. The Biggest Levers at a Glance

| Driver | Low-time segment | Mean (min) | High-time segment | Mean (min) | Δ |
|--------|-----------------|------------|-------------------|------------|---|
| **Channel** | Chat | 22.5 | Email | 98.3 | **+76** |
| **`technical_complexity`** | 1 | 24.8 | 3 | 93.0 | **+68** |
| **`issue_category`** | UI & UX | 30.3 | Performance & Latency | 142.4 | **+112** |
| **`requires_external_dependency`** | No ext. dep. | 38.6 | Internal eng. escalation | 76.9 | **+38** |
| **`actionability`** | Not present (FRs) | 20.4 | Process/workflow change | 109.3 | **+89** |
| **Agent** | AG-006 | 15.3 | AG-002 | 148.3 | **+133** |
| **Priority** | Low | 37.5 | High | 131.1 | **+94** |

---

## 2. Channel: Chat vs. Email Is the Sharpest Structural Split

Email tickets (n=100) average **98.3 min** vs. chat (n=50) at **22.5 min** — a 4.4× difference. In-app (35.0 min, n=50) and phone (70.2 min, n=50) fall in between. Feature requests, which are inherently simple, almost never arrive via email (only 2 email feature-request tickets at 57.5 min), so this is not purely a composition effect. High-complexity bug reports and billing issues dominate the email queue.

**Action:** Route simple, low-complexity requests to chat or in-app channels. Use email deflection or auto-responders for common question types.

---

## 3. Technical Complexity Is the Strongest Single Predictor (r = 0.58)

The TAPP-generated `technical_complexity` score (1–5 scale) has a Pearson correlation of **0.58** with `resolution_minutes` — the highest of any single variable.

| Complexity | Mean (min) | Median (min) | N |
|-----------|------------|--------------|---|
| 1 | 24.8 | 23.0 | 53 |
| 2 | 51.7 | 48.0 | 75 |
| 3 | 93.0 | 85.0 | 76 |
| 4 | 87.0 | 80.0 | 41 |
| 5 | 77.0 | 60.0 | 5 |

Complexity 3 tickets are the largest high-complexity group (76 tickets) and the slowest on average. Nearly all `performance_and_latency` tickets are complexity 3–4 with `degraded_performance` severity and `internal_engineering_escalation` dependency, yielding a mean of **142.4 min**.

**Action:** Create a fast-triage rule: complexity ≥ 3 tickets should immediately open an engineering bridge instead of cycling through L1 agents. This is supported by the `requires_external_dependency` = `internal_engineering_escalation` effect (147 tickets, mean 76.9 min vs. 38.6 min for no dependency).

---

## 4. Priority Anomaly: "High" Is Slower Than "Critical"

| Priority | Mean (min) | Median (min) | N |
|---------|------------|--------------|---|
| Critical | 74.4 | 72.5 | 50 |
| **High** | **131.1** | **131.0** | **50** |
| Medium | 41.6 | 37.0 | 76 |
| Low | 37.5 | 24.0 | 74 |

High-priority tickets take *longer* than Critical ones. Inspection shows that High tickets are overwhelmingly `performance_and_latency` / `degraded_performance` issues with `internal_engineering_escalation` dependency — a category that requires waiting for engineering but may not trigger the same urgency protocols as Critical outages. Critical tickets (complete outages) appear to mobilize faster response.

**Action:** Recalibrate priority tiers so that High+`degraded_performance`+`internal_engineering_escalation` combinations receive Critical-equivalent SLA treatment.

---

## 5. Issue Category: Concentrate Improvement on Performance & Billing

| Issue Category | Mean (min) | N |
|----------------|------------|---|
| UI & UX | 30.3 | 70 |
| Notifications/Email | 42.5 | 11 |
| Mobile | 61.9 | 7 |
| Compliance & Security | 60.4 | 24 |
| Infrastructure & Outage | 71.7 | 15 |
| Integration & API | 69.2 | 17 |
| Data Integrity | 73.5 | 23 |
| Authentication & Access | 67.6 | 29 |
| Automation & Workflows | 74.2 | 8 |
| **Billing & Invoicing** | **83.3** | **22** |
| **Performance & Latency** | **142.4** | **24** |

Performance & Latency is 4.7× slower than UI/UX. `root_cause_domain` = `configuration_error` (mean 81.5 min, n=35) and `regression_from_release` (74.8 min, n=95) are the two highest-volume slow root causes.

**Action:** Pre-build runbooks for regression-from-release and configuration-error scenarios (together n=130, 52% of all tickets) to slash investigation time.

---

## 6. `actionability` and `requires_external_dependency` Signal Where Delays Live

| `actionability` | Mean (min) | N |
|----------------|------------|---|
| Not present (feature requests) | 20.4 | 49 |
| Config change only | 83.7 | 10 |
| Documentation/guidance | 69.3 | 26 |
| Investigation & engineering fix | 74.4 | 150 |
| Hotfix or rollback needed | 81.5 | 8 |
| **Process/workflow change** | **109.3** | **7** |

The 150 tickets classified as `investigation_and_engineering_fix` represent the core queue. Pairing this with `requires_external_dependency`:

| Dependency type | Mean (min) | N |
|----------------|------------|---|
| No external dependency | 38.6 | 79 |
| Third-party vendor | 67.9 | 8 |
| Customer IT/IdP | 82.2 | 16 |
| Internal engineering escalation | 76.9 | 147 |

Tickets with no escalation need average only 38.6 min. The 147 internal-escalation tickets average 76.9 min — nearly double — indicating the engineering handoff is a primary delay point.

**Action:** Reduce the engineering queue backlog by empowering L2 agents with self-serve diagnostic tools for common regression and configuration patterns.

---

## 7. Information Quality (`data_or_info_provided`) Has Modest Effect

For bug reports specifically:

| Info provided | Mean (min) | N |
|--------------|------------|---|
| Repro steps provided | 77.0 | 104 |
| Correlation ID / log | 64.7 | 3 |
| Minimal info only | 85.2 | 17 |

Minimal-info tickets are ~8 min slower than repro-steps tickets — a real but small effect, likely dwarfed by the engineering-dependency bottleneck.

**Action:** Intake forms that force log/correlation ID submission for known slow categories (performance, auth) offer incremental gains.

---

## 8. Agent Variance Is Large and Addressable

Agent mean resolution ranges from **15.3 min (AG-006)** to **148.3 min (AG-002)** across agents with ≥5 tickets. This 10× spread likely reflects both caseload composition and skill differences.

**Action:** Analyze AG-006/AG-003/AG-017's ticket mix and handling patterns as a best-practice baseline. Pair slow agents with high-performers for coaching on the `investigation_and_engineering_fix` category.

---

## 9. `escalation_signal` and `workaround_available`

Escalation signals (`deadline_or_time_pressure`: mean 80.1 min, n=31; `financial_impact`: 92.5 min, n=6) increase resolution time but affect a minority of tickets (22%). Tickets with no workaround (n=159) average 76.8 min vs. 36.7 min for tickets where workaround is not applicable (mostly feature requests). These columns confirm severity direction but don't add actionable cuts beyond what `operational_severity` already captures.

---

## 10. Prioritized Recommendations

| Priority | Action | Expected Impact |
|---------|--------|----------------|
| 🔴 High | **Route simple/low-complexity tickets to chat or in-app**; deflect email for feature requests and FAQs | −40–60 min on ~30% of queue |
| 🔴 High | **Fast-track complexity ≥ 3 directly to engineering**; skip L1 cycling | −20–40 min on 46% of queue |
| 🔴 High | **Reclassify High+degraded_performance to Critical SLA** | Brings 24 performance tickets from 142 → closer to 75 min target |
| 🟡 Medium | **Build runbooks for `regression_from_release` + `configuration_error`** (n=130 tickets, 52%) | −10–20 min per ticket |
| 🟡 Medium | **Intake forms requiring logs/correlation IDs** for auth, performance, API tickets | −5–10 min per ticket |
| 🟢 Lower | **Agent skill-sharing**: pair AG-002/AG-016/AG-012 with top performers | Addressable through coaching |
