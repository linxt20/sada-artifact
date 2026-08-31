---
dataset: flag_6
scenario: causal_agent
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "agent_resolution_discrepancy"
query: "Why do some agents have longer resolution times?"
source_table: augment_table/flag_6/causal_agent/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:19:08.295264+00:00
wall_seconds: 43.13
---

# Agent Resolution Time Analysis

**Dataset:** 500 incidents | **Focus variable:** `assigned_to` (agent) and derived `resolution_hours`

---

## Key Finding: Fred Luddy Drives the Majority of Long Resolution Times

Resolution time varies dramatically by agent:

| Agent | Mean Hours | Median Hours | Ticket Count |
|---|---|---|---|
| **Fred Luddy** | **750.0** | **691.2** | 76 |
| Howard Johnson | 136.1 | 129.0 | 98 |
| Luke Wilson | 131.9 | 123.3 | 103 |
| Charlie Whitherspoon | 118.6 | 127.6 | 103 |
| Beth Anglin | 109.1 | 111.5 | 98 |

Fred Luddy's mean resolution time (~31 days) is **~5.5× higher** than the next slowest agent. This is not a caseload issue — he handles fewer tickets (76 vs ~100 for others). The gap is consistent across both mean and median, ruling out a few extreme outliers.

---

## Factors Associated with Longer Resolution Times

### 1. Agent Assignment (Strongest Factor)
Fred Luddy's elevated times persist across every incident category he handles, suggesting an agent-level skill or workload pattern rather than an inherited case-mix:

| Category (Fred Luddy) | Mean Hours |
|---|---|
| Software | 851.2 |
| Network | 761.7 |
| Database | 706.7 |
| Hardware | 436.8 |

### 2. Incident Category / Type
Certain incident types take longer globally:

| Incident Category | Mean Hours |
|---|---|
| `file_share` | 535.5 |
| `software_application` | 420.4 |
| `authentication` | 269.5 |
| `vpn` | 267.8 |
| `wifi` | 133.4 |
| `printing` | 180.7 |

`file_share` and `software_application` tickets are broadly harder — Fred Luddy's caseload is weighted toward network/VPN and email tickets, which also carry above-average times.

### 3. Assignment Group
Tickets routed to the **Software group** average 347 hours, vs. 194–222 hours for other groups, consistent with the complexity of software incidents.

### 4. Affected System Scope
`individual_device` incidents average **253.7 hours** — counterintuitively longer than systemic outages (219 h) or server infrastructure (201 h). This may reflect lower urgency prioritisation of single-user issues, allowing them to linger.

### 5. Priority (Weak / Counter-intuitive)
Lower-priority tickets take *longer*, not shorter:

| Priority | Mean Hours |
|---|---|
| 3 - Moderate | 246.6 |
| 2 - High | 229.8 |
| 1 - Critical | 187.7 |

This is consistent with critical incidents receiving faster escalation and resource allocation.

### 6. Ticket Handoff and Recurrence (Marginal Effect)
Tickets with both handoff and recurrence average ~235 h vs ~209 h for neither — a modest ~12% difference. These variables are not primary drivers.

---

## Data Quality Note
50 of 500 records (~10%) show **negative resolution times** (closed_at before opened_at), indicating data entry errors. These were excluded from the analysis but should be investigated before operational decisions are made.

---

## Summary

The primary driver of long resolution times is **agent assignment** — specifically, Fred Luddy's tickets resolve ~5× slower than peers regardless of category, suggesting a skill gap, bandwidth constraint, or data-quality issue specific to his records. Secondary factors include **incident type** (file_share, software_application, VPN are inherently harder) and **priority level** (critical tickets are resolved faster). Ticket handoff and recurrence have only marginal impact. Decision-makers should audit Fred Luddy's ticket queue and verify whether his resolution timestamps are being recorded correctly.
