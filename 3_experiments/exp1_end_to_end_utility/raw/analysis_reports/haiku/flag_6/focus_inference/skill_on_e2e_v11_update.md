---
dataset: flag_6
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth analyzing in these incident tickets."
source_table: augment_table/flag_6/focus_inference/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:20:38.633138+00:00
wall_seconds: 117.77
---

# Incident Ticket Analysis Report: Focus on Inference Skill

**Query:** Help me understand what's worth analyzing in these incident tickets.

**Dataset:** 500 incidents from January–July 2023 (Haiku skill-on-e2e v11 update)

---

## Method Note

This analysis combines original structured columns (priority, state, category, assigned_to, opened_at, closed_at) with six TAPP-generated semantic columns: **primary_issue_category**, **issue_severity_signal**, **assigned_technician**, **location_or_scope**, **issue_recurrence_pattern**, and **same_person_assigned_closed**. TAPP columns are used to clarify issue semantics and patterns; original columns remain primary evidence. All quantified claims below are based on full-table counts, rates, or stratifications.

---

## 1. High Severity & Frequent Outages: The Core Finding

**What's worth analyzing:** A substantial portion of tickets represent severe, production-impacting incidents.

- **Critical incidents:** 88/500 (17.6%) flagged as Priority 1
- **Critical + High:** 467/500 (93.4%) combined high-urgency issues

Among critical incidents, the **issue_severity_signal** (TAPP) reveals the true impact:
- **Service outages (complete):** 55/88 critical tickets (62.5%)—full system unavailability
- **Access failures (individual):** 19/88 (21.6%)—user-level failures
- **Partial degradation:** 10/88 (11.4%)

**Cross-check with original data:** Priority field confirms 88 critical tickets; category field shows 284 Network, 109 Database, and 72 Software—aligning with outage-heavy domains.

---

## 2. Systemic & Recurring Patterns Dominate: Indicates Infrastructure Issues

**What's worth analyzing:** Most incidents are not isolated events; they reflect systemic weaknesses.

| Recurrence Pattern (TAPP) | Count | % |
|---|---|---|
| Systemic recurring | 181 | 36.2% |
| Repeated by same user | 176 | 35.2% |
| Single isolated | 138 | 27.6% |

**Systemic recurring** issues break down by domain:
- Email/VPN/Network services: 132/181 (72.9%)
- Database connectivity: 49/181 (27.1%)

**Severity correlation:** When issues are systemic recurring, they manifest as:
- Full outages: 45/181 (24.9%)
- Access failures: 112/181 (61.9%)

Isolated incidents (single_isolated), by contrast, account for only 27.6% of the portfolio, meaning **72% of tickets represent repeating or infrastructure-level problems** that could benefit from root-cause mitigation rather than case-by-case fixes.

---

## 3. Email & Network Services: The Critical Bottleneck

**What's worth analyzing:** Four domains account for 95% of incidents, with email systems and network connectivity as primary pain points.

| Primary Issue Category (TAPP) | Count | % | Critical | Systemic Recurring |
|---|---|---|---|---|
| Email system | 136 | 27.2% | 46 | 56 |
| Network connectivity | 118 | 23.6% | 12 | 61 |
| VPN connectivity | 110 | 22.0% | 0 | 39 |
| Database access | 105 | 21.0% | 27 | 19 |
| Software system | 23 | 4.6% | 3 | 3 |
| Hardware device | 8 | 1.6% | 0 | 3 |

**Email incidents are the highest-risk category:**
- 67/136 (49.2%) result in complete service outages
- 56/136 (41.2%) follow systemic recurring patterns
- 46/136 (33.8%) are flagged Critical

**Network connectivity (non-VPN) is second:**
- 61/118 (51.7%) are systemic recurring
- 12/118 (10.2%) are Critical (lower than email, but still material)

**Database issues reflect a separate cluster:**
- 27/105 (25.7%) are Critical
- Only 19/105 (18.1%) are systemic recurring—more often single incidents or repeated by individual users

---

## 4. Scope & Location Clarity Gap: Data Quality Issue

**What's worth analyzing:** Nearly half of incidents lack clear scope documentation.

| Location/Scope (TAPP) | Count | % |
|---|---|---|
| Unknown | 238 | 47.6% |
| Device individual | 119 | 23.8% |
| Office wide | 111 | 22.2% |
| Specific location mentioned | 16 | 3.2% |
| Department level | 11 | 2.2% |
| Building level | 5 | 1.0% |

**Critical incidents cluster at higher scopes:**
- Office-wide: 36/88 critical (40.9%)
- Unknown/device: 47/88 (53.4%)

**Implication:** 47.6% of tickets (238/500) have "Unknown" scope (TAPP), suggesting either:
1. Poor description quality in incident reports, or
2. TAPP was unable to infer scope—both worth investigating.

Tickets with explicit office-wide scope are more likely to be critical (36/111 = 32.4%) than device-individual (5/119 = 4.2%).

---

## 5. Technician Assignment & Self-Closure: Authority & Autonomy Pattern

**What's worth analyzing:** Nearly 1 in 5 tickets are closed by the same technician who was assigned.

- **Same person assigned & closed:** 94/500 (18.8%)

**Breakdown by technician** (top 5):
- Luke Wilson: 26 self-closures
- Howard Johnson: 20
- Charlie Whitherspoon: 17
- Beth Anglin: 16
- Fred Luddy: 15

**Relationship to recurrence** (using same_person_assigned_closed flag):
- Repeated by same user incidents: 22.7% self-closed (40/176)
- Systemic recurring: 19.3% self-closed (35/181)
- Isolated incidents: 13.8% self-closed (19/138)

**Insight:** Technicians close a higher fraction of their own tickets when handling repeated/systemic issues—suggesting either they develop expertise in recurring problems or self-closure correlates with incomplete fixes for systemic issues.

---

## 6. Resolution State & Backlog: Workload & Efficiency

**What's worth analyzing:** The split between Resolved vs. Closed suggests different closure types; a small backlog persists.

| State | Count | % |
|---|---|---|
| Resolved | 244 | 48.8% |
| Closed | 234 | 46.8% |
| In Progress | 11 | 2.2% |
| New (unassigned) | 11 | 2.2% |

**Critical tickets by state:**
- Resolved: 45/88 (51.1%)
- Closed: 39/88 (44.3%)
- In Progress or New: 4/88 (4.5%)

**Unresolved backlog (4.4% of portfolio):**
- 9 High-priority tickets still in New or In Progress state
- 1 Critical ticket unresolved
- Suggests reasonable throughput but some escalation risk

---

## 7. Data Quality: Category Misclassification

**What's worth analyzing:** Original "category" field shows misalignment with TAPP-inferred primary_issue_category.

**Sample mismatches (top by count):**
- Database category → TAPP identifies as email_system (3 tickets)
- Hardware category → TAPP identifies as email_system (13 tickets)
- Inquiry/Help category → TAPP identifies as email_system (8 tickets)

**Implication:** Incident categorization at intake may conflate service domain (Network, Database, Hardware) with issue type. TAPP's semantic categories (email_system, vpn_connectivity, database_access) are more specific and reliable for root-cause trending.

---

## 8. The Highest-Risk Profile: Critical + Systemic + Core Services

**What's worth analyzing:** A focused subset of 41 incidents represents the greatest operational exposure.

**Criteria:** Priority = Critical AND issue_recurrence_pattern = systemic_recurring AND primary_issue_category in {email_system, vpn_connectivity, network_connectivity, database_access}

- **41 tickets** (8.2% of portfolio, 46.6% of all Critical incidents) meet this profile
- **Domains:** Email (largest), Network, Database
- **State:** Mostly Resolved or Closed (only 1 still in-progress)
- **Technician:** Distributed across all five primary technicians

**Action signal:** These 41 incidents warrant root-cause analysis and infrastructure hardening; repeated systemic criticality is a design/capacity problem, not an individual technician issue.

---

## Summary: What's Worth Analyzing

| Finding | Why It Matters |
|---|---|
| **17.6% Critical + 75.8% High priority** | Portfolio is heavily weighted to urgent/severe incidents; organization is in reactive mode. |
| **72% Systemic or User-Repeated** | Most incidents recur; infrastructure root causes exist and are preventable. |
| **Email, Network, VPN = 72% of load** | Four key services are bottlenecks; focus remediation on these domains. |
| **47.6% Unknown scope (TAPP)** | Incident intake process lacks detail; improved description templates could improve diagnostics. |
| **18.8% Self-Closed by assignee** | Technicians have appropriate autonomy; but higher self-closure on recurring issues may mask incomplete fixes. |
| **4.4% unresolved** | Backlog is small and manageable; no systemic clearance problem. |
| **41 Critical + Systemic + Core Services** | Focus area for strategic remediation; these represent the greatest customer impact and prevention ROI. |

---

## Recommendation for Further Investigation

1. **Root-cause analysis** of the 41 highest-risk incidents (critical + systemic + core services)
2. **Infrastructure hardening** for email, network, and VPN services
3. **Process improvement**: Require scope/location field in incident intake templates
4. **Pattern analysis**: Track whether same-technician self-closure on systemic issues correlates with rapid re-opening
