---
dataset: flag_6
scenario: concept_attribute_workload
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "agent_workload_burden"
query: "What kinds of tickets create heavier agent workload?"
source_table: augment_table/flag_6/concept_attribute_workload/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:19:47.545039+00:00
wall_seconds: 74.8
---

# Agent Workload Analysis: What Kinds of Tickets Create Heavier Workload?

## Executive Summary

Heavy agent workload is driven primarily by **infrastructure-dependent incidents** (56.6% of all tickets) and **tickets requiring prolonged investigation** (6.6%). The top three workload-intensive incident categories are:
1. **Database access issues** (98.1% with heavy patterns, 10.3-day average resolution)
2. **Network connectivity issues** (86.2% with heavy patterns)
3. **Email service incidents** (72.6% with heavy patterns)

Critical and high-priority tickets dominate the workload (76.6% of portfolio), with infrastructure outages and database access problems creating the heaviest sustained demand on agent capacity.

---

## Method Note

This analysis uses the complete augmented table combining original structured columns with three TAPP-generated semantic facets:
- **incident_category**: Semantic classification of ticket type
- **resolution_pattern**: Intensity indicator reflecting expected resolution path
- **ticket_reassignment_pattern**: Handoff complexity between agents

---

## Key Findings

### 1. Ticket Volume and Priority Distribution

The dataset contains **500 closed/resolved tickets** with strong skew toward high-severity work:
- **1 - Critical**: 88 tickets (17.6%)
- **2 - High**: 379 tickets (75.8%)
- **3 - Moderate**: 33 tickets (6.6%)

**Workload implication**: 93.4% of the portfolio is high-priority or critical, requiring elevated urgency and often escalation protocols.

---

### 2. Heavy Workload Patterns

Two TAPP-generated patterns capture the most intensive workload characteristics:

#### A. Infrastructure Dependency (56.6% of tickets, 283 total)
This pattern indicates incidents dependent on backend services rather than quick application fixes.
- **Average resolution time**: ~9-10 days
- **Critical/High priority mix**: 96.1%
- **Distribution by incident type**:
  - Email service: 97 tickets (34.3%)
  - Database access: 86 tickets (30.4%)
  - Network connectivity: 80 tickets (28.3%)
  - Infrastructure outage: 18 tickets (6.4%)

**Workload impact**: These require sustained coordination with infrastructure teams, troubleshooting multiple layers, and often waiting for backend resolution.

#### B. Prolonged Investigation (6.6% of tickets, 33 total)
The most intensive resolution pattern requiring extended problem-solving.
- **Average resolution time**: 16.16 days (51% longer than overall average)
- **Incident breakdown**:
  - Database access (51.5%, 17 tickets): avg 13.52 days
  - Software installation (30.3%, 10 tickets): avg 21.88 days **← longest**

**Workload impact**: These tickets consume disproportionate agent time despite lower volume, particularly database issues and software deployment failures.

#### C. Authentication/Access Control (28.6% of tickets, 143 total)
Secondary complexity pattern requiring credential verification and permission audits.
- **Average resolution time**: ~10-13 days
- **Primary incident types**: VPN connectivity, authentication issues, access control

---

### 3. Highest-Workload Incident Categories

Ranked by percentage of tickets with heavy patterns (infrastructure dependency + prolonged investigation):

| Incident Category | Total Tickets | Heavy Pattern Count | Heavy % | Avg Days to Resolve | Priority Distribution |
|---|---|---|---|---|---|
| Infrastructure Outage | 21 | 21 | **100.0%** | 11.46 days | 95.2% Crit/High |
| Database Access | 105 | 103 | **98.1%** | 10.32 days | 95.2% Crit/High |
| Network Connectivity | 94 | 81 | **86.2%** | 9.70 days | 92.6% Crit/High |
| Email Service | 135 | 98 | **72.6%** | 9.58 days | 91.9% Crit/High |
| Software Installation | 16 | 10 | **62.5%** | 18.93 days | 75.0% Crit/High |
| Device Hardware | 9 | 1 | 11.1% | 8.53 days | 77.8% Crit/High |
| VPN Connectivity | 110 | 1 | 0.9% | 12.06 days | 97.3% Crit/High |
| Authentication | 10 | 1 | 10.0% | 13.13 days | 100% Crit/High |

**Key insight**: Despite VPN connectivity having 110 tickets (high volume), only 1 requires prolonged investigation, indicating most are authentication-only issues. In contrast, **database access and infrastructure outages** drive disproportionate workload intensity due to their infrastructure dependency and troubleshooting complexity.

---

### 4. Combined Workload Drivers: Priority × Resolution Pattern

The most demanding ticket segments combine high severity with intensive resolution needs:

| Severity Level | Resolution Pattern | Count | Avg Days | Workload Impact |
|---|---|---|---|---|
| Critical | Infrastructure Dependency | 77 | 8.95 days | Immediate response, sustained coordination |
| Critical | Prolonged Investigation | 9 | 13.79 days | Extended critical-path delay |
| High | Infrastructure Dependency | 195 | 9.36 days | Bulk of operational load |
| High | Prolonged Investigation | 24 | 17.03 days | Extended troubleshooting |

**Critical finding**: 305 tickets (61% of portfolio) combine critical/high priority with heavy resolution patterns. These represent the core workload driver for support agents.

---

### 5. Agent Coordination Complexity (Reassignment Pattern Impact)

The ticket_reassignment_pattern reveals workflow complexity:

**Multi-Agent Handoffs (Assigned ≠ Closer)**: 378 tickets (75.6%)
- Average resolution: 10.76 days
- 62.7% involve heavy patterns (infrastructure/prolonged investigation)
- **Workload implication**: Requires coordination, context transfer, and potential rework across team members

**Single-Agent Resolution (Assigned = Closer)**: 100 tickets (20.0%)
- Average resolution: 10.72 days
- 62.0% involve heavy patterns
- **Workload implication**: More efficient for eligible incidents, but heavy patterns still present in this group

**Unassigned/Other**: 22 tickets (4.4%)

**Key insight**: The predominance of multi-agent handoffs (75.6%) combined with high infrastructure dependency suggests significant coordination overhead consuming agent time beyond direct problem-solving.

---

### 6. Workload Distribution by Original Category

While TAPP incident_category provides semantic precision, the original category field shows operational assignment:

- **Network**: 284 tickets (56.8%) — largest assignment group
- **Database**: 109 tickets (21.8%) — highest complexity
- **Software**: 72 tickets (14.4%)
- **Hardware**: 26 tickets (5.2%)
- **Inquiry/Help**: 9 tickets (1.8%)

Assignment groups:
- **Network assignment group**: 328 agents/team
- **Database assignment group**: 106 agents/team
- **Service Desk**: 30
- **Software**: 26
- **Hardware**: 10

**Workload implication**: Network teams carry the largest absolute load (284 tickets), but database teams handle the most complex cases (average 10.3-day resolution for 95.2% critical/high priority).

---

### 7. Overall Resolution Time Profile

Across all 428 tickets with measurable resolution times:
- **Mean**: 10.75 days
- **Median**: 6.83 days
- **Std Dev**: 13.09 days

The high standard deviation (1.2× the mean) indicates **bimodal workload**: quick resolutions (~4-7 days) for straightforward issues vs. extended investigations (14+ days) for infrastructure-dependent and database incidents. This creates unpredictable demand on agent capacity.

---

## Workload Characterization Summary

### Heavy-Workload Ticket Profile
Tickets creating the **heaviest agent workload** have these characteristics:

1. **Severity**: Critical (1 - Critical) or High (2 - High) priority — 88.2% of heavy-workload tickets
2. **Type**: Infrastructure-dependent (283 tickets) or requiring prolonged investigation (33 tickets)
3. **Incident Category**: Database access (98.1% heavy), infrastructure outages (100% heavy), or network connectivity (86.2% heavy)
4. **Duration**: 10-16 day average resolution (50-150% above quick-fix baseline of 9.6 days)
5. **Coordination**: 75.6% require multi-agent handoff, creating overhead
6. **Coverage**: 61% of entire portfolio combines heavy patterns with critical/high priority

### Light-Workload Ticket Profile (for contrast)
- **Pattern**: Quick fix expected (41 tickets, 8.2%)
- **Average duration**: 9.6 days (baseline)
- **Types**: Email client sync issues, device hardware, basic software installation
- **Coordination**: Single-agent resolutions more common

---

## Actionable Insights

1. **Database and infrastructure incidents dominate workload intensity**: 208 of 305 high-workload tickets (68%) fall into these categories. Prioritize automation, runbooks, and proactive monitoring in these domains.

2. **Infrastructure dependency is systematic**: 56.6% of portfolio relies on backend coordination. Consider creating dedicated infrastructure escalation workflows to reduce agent friction.

3. **Prolonged investigation cases (33 tickets) consume 16.2 days on average**: Disproportionate to their 6.6% volume. Root cause analysis and problem-solving templates for database/software installation issues would yield high ROI.

4. **Reassignment overhead is significant**: 75.6% of tickets move between agents, suggesting knowledge silos or role specialization. Cross-training or integrated triage might reduce handoff cycles.

5. **VPN connectivity vs. database access**: Despite similar volume (~110 vs. 105 tickets), VPN rarely requires investigation (<1% heavy), while database access nearly always does (98.1% heavy). This suggests VPN issues are well-understood while database problems require persistent troubleshooting.

---

## Conclusion

Heavy agent workload is not uniformly distributed. **Infrastructure-dependent incidents, particularly database access problems and network outages, create disproportionate demand** despite representing 44% of tickets. Combined with the 75.6% multi-agent handoff rate and extended resolution times (10+ days average), these tickets drive both time consumption and coordination complexity. The most effective workload reduction would target database access (105 tickets, 98.1% heavy) and infrastructure outage automation (21 tickets, 100% heavy) while reducing reassignment cycles through process redesign.
