---
dataset: flag_6
scenario: causal_agent
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "agent_resolution_discrepancy"
query: "Why do some agents have longer resolution times?"
source_table: augment_table/flag_6/causal_agent/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:19:53.133751+00:00
wall_seconds: 84.2
---

# Why Do Some Agents Have Longer Resolution Times?

## Executive Summary

Resolution time variance across the five agents is almost entirely driven by one agent — **Fred Luddy** — whose median resolution time is **~5.6× longer** than that of all other agents combined. The gap persists across every category, priority tier, and failure mode, indicating an agent-level bottleneck rather than a caseload or ticket-type effect. Secondary factors (open/unresolved backlogs, severity mix) widen the gap further but do not explain it.

---

## 1. Overall Resolution Time by Agent

| Agent | n (resolved) | Mean hrs | Median hrs |
|---|---|---|---|
| **Fred Luddy** | **76** | **750.0** | **691.2** |
| Howard Johnson | 98 | 136.1 | 129.0 |
| Charlie Whitherspoon | 103 | 118.6 | 127.6 |
| Luke Wilson | 103 | 131.9 | 123.3 |
| Beth Anglin | 98 | 109.1 | 111.5 |

*Source: `opened_at` → `closed_at` delta for all 478 Resolved/Closed tickets.*

Fred Luddy's median of **691 h (~28.8 days)** vs. the peer median of **~123 h (~5.1 days)** is not a statistical outlier artifact — it holds at every quantile.

---

## 2. Gap Is Not Explained by Ticket Mix

### 2a. Priority-controlled comparison (median hours)

| Agent | 1 – Critical | 2 – High | 3 – Moderate |
|---|---|---|---|
| Beth Anglin | 45.5 | 115.5 | 150.4 |
| Charlie Whitherspoon | 99.9 | 132.3 | 127.2 |
| **Fred Luddy** | **556.8** | **705.6** | **806.4** |
| Howard Johnson | 139.2 | 125.2 | 91.7 |
| Luke Wilson | 124.2 | 127.4 | 117.5 |

Fred is slower at **every** priority level, including Critical (557 h vs. peers' 45–139 h).

### 2b. Category-controlled comparison (median hours, Network and Software)

| Agent | Network (n) | Median hrs | Software (n) | Median hrs |
|---|---|---|---|---|
| Beth Anglin | 55 | 114.1 | 17 | 150.4 |
| Charlie Whitherspoon | 60 | 125.8 | 16 | 69.0 |
| **Fred Luddy** | **43** | **681.6** | **12** | **832.8** |
| Howard Johnson | 53 | 161.8 | 11 | 88.8 |
| Luke Wilson | 60 | 152.9 | 14 | 136.7 |

Fred handles a higher share of Network and Database tickets, which are among the slower categories overall — but even within those categories his times are 4–10× peer medians.

---

## 3. Unresolved / Open Ticket Backlog

`is_ticket_unresolved` flags 22 tickets still open at the time of data extraction.

| Agent | Open/In-Progress tickets |
|---|---|
| **Fred Luddy** | **8** (of 84 assigned = **9.5%**) |
| Howard Johnson | 2 (of 100 = 2.0%) |
| Luke Wilson | 1 (of 104 = 1.0%) |
| Beth Anglin | 0 |
| Charlie Whitherspoon | 0 |

Fred has a disproportionate open backlog (36% of all unresolved tickets while handling only 16.8% of the overall caseload), consistent with systemic throughput issues rather than isolated delays.

---

## 4. TAPP-Augmented Column Analysis

*TAPP-generated columns used: `assigned_resolver_match`, `incident_category`, `incident_severity_signal`, `failure_mode`, `affected_scope`, `is_ticket_unresolved`.*

### 4a. `assigned_resolver_match` — Weak discriminator

Overall, tickets where the assigned agent matched the expected resolver (`assigned_resolver_match = True`) showed no meaningful improvement: median 162 h (True) vs. 148 h (False) across all agents. For Fred specifically, the match rate is **19.7%** (vs. 20.6% for peers) — virtually identical — and even matched tickets take a median **624 h**. This column does not explain Fred's delays.

### 4b. `incident_severity_signal` — Confirms severity mix but not a root cause

Fred's caseload skews toward `access_denied` (n=34) and `outage` (n=15) signals. However, Fred's resolution times are elevated uniformly across all severity signals:

| Severity signal (Fred only) | n | Median hrs |
|---|---|---|
| slow_performance | 3 | 1,286.4 |
| Unknown | 8 | 736.8 |
| access_denied | 34 | 679.2 |
| degraded | 16 | 657.6 |
| outage | 15 | 556.8 |

No severity class resolves quickly for Fred — the floor (~557 h for outage) is still 4× higher than peer averages.

### 4c. `failure_mode` — No differential signal

Across all agents, `connection_failure` is the dominant failure mode (315 of 478 resolved tickets). Fred handles 50 connection_failure tickets at median **657.6 h** vs. 99–146 h for peers on the same failure mode. This rules out failure mode complexity as a cause.

### 4d. `affected_scope` — Points to a data quality gap

Fred has 36 of 76 resolved tickets (47%) labeled `affected_scope = Unknown`, the highest unknown rate of any agent. This may reflect incomplete ticket documentation by Fred, which could itself indicate a process compliance gap.

### 4e. `incident_category` — No structural advantage/disadvantage

Fred handles a spread across `email` (18), `vpn` (18), `database` (17), and `network_connectivity` (13). These are mainstream categories handled by all agents; no specialty-category skew explains the delay.

---

## 5. Causal Summary

| Factor | Explains Fred's delay? | Evidence |
|---|---|---|
| Harder ticket mix (priority, category) | **No** | Gap persists in every stratum |
| Failure mode complexity | **No** | 4–6× slower on identical failure modes |
| Mis-assignment (`assigned_resolver_match`) | **No** | Match rate equal to peers; even matched tickets ~624 h |
| Severity signal (complex cases) | **Partial/minor** | Severity mix slightly harder, but gap is 4–10× not 1.5× |
| Agent throughput / capacity bottleneck | **Yes — primary driver** | Systematic 5–6× delay, high open-ticket backlog (9.5%), high `affected_scope` Unknown rate |

---

## 6. Key Findings

1. **Fred Luddy is the dominant driver of long resolution times** — median 691 h vs. 111–129 h for all four peers, across all ticket types and priorities.
2. **The gap is agent-specific, not ticket-type-specific**: category-controlled and priority-controlled comparisons confirm it is not caseload composition.
3. **Fred also carries a disproportionate open-ticket backlog** (8 unresolved = 9.5% of assigned), the highest of any agent.
4. **TAPP columns (`incident_severity_signal`, `failure_mode`, `assigned_resolver_match`) do not explain the gap** — they are roughly equivalent across agents when controlled for. `is_ticket_unresolved` corroborates the backlog signal.
5. **Recommended action**: Investigate Fred Luddy's workload capacity, escalation practices, and whether tickets are being held open awaiting external dependencies (which would not appear in this dataset).
