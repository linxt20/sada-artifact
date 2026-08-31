---
dataset: flag_2
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What recurring types of problems show up in these incident tickets?"
source_table: augment_table/flag_2/focus_inference/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:17:11.215335+00:00
wall_seconds: 65.04
---

# Recurring Problem Types in Incident Tickets

## Method Note
TAPP-generated columns used in this analysis: `incident_category`, `failure_mode`, `affected_component`, `scope_context`, `recurrence_signal`, `resolution_same_day`. The `recurrence_signal` column was uniform (all `True`, n=500) and therefore provided no differentiating signal; it is noted but not centered in the analysis. All other TAPP columns added semantic granularity cross-checked against original structured fields (`category`, `priority`, `assignment_group`).

---

## Dataset Overview

| Metric | Value |
|---|---|
| Total incidents | 500 |
| Priority breakdown | High: 380 (76%), Critical: 79 (16%), Moderate: 41 (8%) |
| Same-day resolution rate | 86% (430/500) |
| Original `category` values | Network (269), Database (116), Software (86), Hardware (18), Inquiry/Help (11) |

---

## 1. Five Dominant Recurring Problem Types

Using `incident_category` (TAPP) cross-checked against original `category` and `assignment_group`, five clearly recurring problem patterns emerge:

| Rank | Incident Category (`incident_category`) | Count | % of Total | Primary Failure Mode (`failure_mode`) | Same-Day Resolution Rate |
|---|---|---|---|---|---|
| 1 | **VPN** | 115 | 23.0% | connection_failure (107) | 80.9% |
| 2 | **Email** | 137 | 27.4% | outage (86), access_denied (25) | 91.2% |
| 3 | **Database** | 119 | 23.8% | connection_failure (64), access_denied (40) | 88.2% |
| 4 | **Network** | 75 | 15.0% | connection_failure (53), access_denied (19) | 81.3% |
| 5 | **Server** | 28 | 5.6% | connection_failure (19), outage (7) | 82.1% |

These five categories account for **474/500 (94.8%)** of all tickets. The remaining 5.2% cover software update issues and hardware faults.

---

## 2. Dominant Failure Modes Across All Categories

`failure_mode` (TAPP) reveals that only three modes drive the vast majority of incidents:

| Failure Mode | Count | % of Total | Notes |
|---|---|---|---|
| **connection_failure** | 253 | 50.6% | Primary driver in VPN, Database, Network, Server |
| **outage** | 111 | 22.2% | Dominates Email; heavily critical (48/79 critical incidents) |
| **access_denied** | 99 | 19.8% | Spread across Database (40), Email (25), Network (19) |
| sync_failure | 11 | 2.2% | Almost entirely in Email |
| update_required | 9 | 1.8% | Software category only |
| crash | 7 | 1.4% | Email (5), Software (2) |

**Connection failures + outages + access denials = 92.6% of all incidents.** This is the core recurring pattern.

---

## 3. Top 10 Specific Problem Clusters

Combining `incident_category` × `failure_mode` surfaces the most granular recurring types:

| Problem Cluster | Count | Priority Skew | Same-Day Res. |
|---|---|---|---|
| VPN / connection_failure | 107 | Mostly High (102) | ~81% |
| Email / outage | 86 | Critical-heavy (35 critical email total) | ~92% |
| Database / connection_failure | 64 | High (92 database total) | ~88% |
| Network / connection_failure | 53 | Mostly High | ~81% |
| Database / access_denied | 40 | — | ~88% |
| Email / access_denied | 25 | — | ~91% |
| Network / access_denied | 19 | — | ~81% |
| Server / connection_failure | 19 | 7 critical | ~82% |
| Database / outage | 11 | — | ~88% |
| Email / sync_failure | 10 | — | ~91% |

---

## 4. Affected Components and Scope

`affected_component` (TAPP) clarifies where failures occur:
- **server_side** (229 tickets, 45.8%): concentrates in Database (119) and Email (79)
- **remote_access** (115 tickets, 23.0%): almost exclusively VPN tickets (114/115)
- **client_application** (65 tickets, 13.0%): mostly Email (57)
- **network_infrastructure** (63 tickets, 12.6%): Network category (52)

`scope_context` (TAPP) shows most incidents are **individual-user scoped** (313/500, 62.6%), with remote-access scoped incidents (127, 25.4%) almost entirely representing VPN connectivity issues. Production-environment scope (42 tickets) clusters in Database (17) and Email (17), aligning with the higher criticality of those categories.

---

## 5. Severity Profile of Recurring Types

Email and Database incidents disproportionately drive **1 - Critical** priority tickets:

| Category | Critical Count | Critical % of Category |
|---|---|---|
| Email | 35 | 25.5% |
| Database | 22 | 18.5% |
| VPN | 8 | 7.0% |
| Server | 7 | 25.0% |
| Network | 6 | 8.0% |

Outage-mode failures are nearly all critical (48/79 = 61% of all critical tickets involve an outage), confirming **email outages and database outages** as the highest-severity recurring cluster.

---

## Summary

The dataset reveals **three recurring problem archetypes** that together account for >90% of tickets:

1. **Connectivity failures** (VPN connection failures, database connection failures, network connection failures) — highest volume, server-side or remote-access components, mostly individual-user scope.
2. **Service outages** (email outages, database outages, server outages) — lower volume but highest criticality; production-environment scoped; drive the majority of Critical-priority tickets.
3. **Access / permission denials** (database access_denied, email access_denied, network access_denied) — mid-volume, likely credential or policy-related, spread across server-side and client-application components.

All 500 tickets carry a `recurrence_signal = True`, indicating the TAPP model flagged the entire corpus as recurrent; this column provides no within-dataset differentiation and should be disregarded for prioritization.
