---
dataset: customer_support_tickets
scenario: causal_handling
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "handling_time_gap"
query: "Why do handling times differ by channel and priority?"
source_table: augment_table/customer_support_tickets/causal_handling/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:10:17.257702+00:00
wall_seconds: 51.62
---

# Why Handling Times Differ by Channel and Priority

**Dataset:** 250 customer support tickets | **Focus variable:** `resolution_minutes`

---

## 1. Handling Time Patterns

### By Channel

| Channel | Mean (min) | Median (min) | n |
|---------|-----------|-------------|---|
| Chat | 22.5 | 23.0 | 50 |
| In-app | 35.0 | 31.0 | 50 |
| Phone | 70.2 | 72.5 | 50 |
| Email | 98.3 | 92.5 | 100 |

Chat is ~4× faster than email; phone sits near the middle.

### By Priority

| Priority | Mean (min) | Median (min) | n |
|----------|-----------|-------------|---|
| Low | 37.5 | 24.0 | 74 |
| Medium | 41.6 | 37.0 | 76 |
| Critical | 74.4 | 72.5 | 50 |
| High | 131.1 | 131.0 | 50 |

Notably, **High-priority tickets take longer than Critical ones** — a counterintuitive finding explained below.

---

## 2. Causal Factors

### Channel differences

**Technical complexity is the primary driver.** Phone tickets carry the highest average complexity (3.78/5), email is next (3.14), while chat is lowest (1.72). This maps directly onto resolution times.

**Scope of impact also varies by channel.** Phone tickets involve entire-tenant outages 52% of the time — the most severe scope — requiring multi-party coordination. Chat tickets are dominated by single-user issues (58%), which resolve quickly. Email handles a broader mix including billing inquiries (15%) and configuration questions (15%), which require asynchronous back-and-forth, inflating clock time even for moderate complexity.

**Issue category mix reinforces this.** Phone channels see outages (24%) and security incidents (14%) — inherently investigative. Chat is split between feature requests and bugs with single-user scope — simpler and self-contained.

### Priority differences

**Technical complexity escalates with priority:** Critical avg 4.24, High 3.84, Medium 2.50, Low 1.54. Higher complexity inherently demands more investigation time.

**Operational urgency profile differs sharply.** Critical tickets are dominated by `production_blocked` (52%) and `active_outage_declared` (28%) — situations where agents must act fast but the issue itself is deep. High tickets are 86% `moderate_impact`, suggesting they are queued and worked methodically rather than triaged immediately.

**Workaround availability is near-zero for Critical (98% `no_workaround`) and High (90%)**, meaning agents cannot deflect or close quickly with a patch solution.

**Root cause domain explains the High > Critical inversion.** High-priority tickets are dominated by `performance_and_scalability` (52% of High), a domain requiring profiling, reproduction, and escalation. Critical tickets are spread across infrastructure, auth/SSO, billing, and security — many of which have clearer runbooks, potentially enabling faster resolution despite higher urgency scores.

---

## 3. Cross-Channel × Priority Patterns

| Channel | Critical | High | Low | Medium |
|---------|---------|------|-----|--------|
| Chat | — | 48.0 | 15.9 | 27.8 |
| Email | — | 132.8 | 71.6 | 58.8 |
| In-app | 57.5 | — | 24.2 | 35.2 |
| Phone | 79.7 | — | — | 40.0 |

*(— = no or negligible observations for that cell)*

Email consistently adds ~40–50 min overhead at every priority level vs. in-app or chat, consistent with its asynchronous nature. Within phone, Critical takes longer than Medium (79.7 vs. 40.0), tracking complexity.

---

## 4. Exceptions and Weak Evidence

- The **High > Critical handling time inversion** is a robust signal (131 vs. 74 min mean) but stems from a confounded mix: High is almost entirely `performance_and_scalability` tickets routed through email (the slow channel + slow domain). This is a routing artifact, not a pure priority effect.
- **Chat has no Critical tickets** in this dataset, limiting cross-channel comparisons at the top severity tier.
- Agent identity (`agent_id`) is present but not analyzed; individual agent variance could partially explain residual differences.
- The **Low priority mean (37.5) is inflated** relative to its median (24.0), indicating a long tail of slow-resolving low-priority email tickets pulling the average up.

---

## 5. Decision-Ready Summary

| Factor | Effect on Resolution Time |
|--------|--------------------------|
| Channel = email | +50–80 min vs. chat (async, broad issue mix) |
| Channel = phone | +45–50 min vs. chat (high complexity, tenant-wide scope) |
| Technical complexity ↑ | Strong positive correlation across both dimensions |
| Scope = entire_tenant | Associated with phone channel; increases coordination overhead |
| Priority = High | Longest times due to `performance_and_scalability` routing through email |
| No workaround available | Concentrates in High/Critical; prevents quick closure |

**Key recommendation:** Channel assignment and issue category are more actionable levers than priority label alone. Routing `performance_and_scalability` tickets away from asynchronous email or providing specialized runbooks could reduce the anomalously high handling times for High-priority tickets.
