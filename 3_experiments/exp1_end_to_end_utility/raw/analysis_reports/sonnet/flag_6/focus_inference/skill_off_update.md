---
dataset: flag_6
scenario: focus_inference
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth analyzing in these incident tickets."
source_table: augment_table/flag_6/focus_inference/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:21:14.241506+00:00
wall_seconds: 42.14
---

# Incident Ticket Analysis Report

## Dataset Overview

- **500 incident tickets** spanning January–February 2023
- **17 columns**: ticket metadata, assignee info, timestamps, priority, category, topic cluster, resolution hours, and SLA status

---

## Key Focus Variable: `sla_status`

The dataset's central signal is SLA compliance:

| SLA Status | Count | % of Total |
|---|---|---|
| **Breached** | 407 | 81.4% |
| **Unknown** | 72 | 14.4% |
| **Within SLA** | 21 | 4.2% |

> ⚠️ **SLA breach is the overwhelming norm**, not the exception. This warrants systemic investigation rather than individual ticket review.

---

## 1. Topic Cluster Distribution

The workload is heavily concentrated in two areas:

| Topic Cluster | Tickets | Breached |
|---|---|---|
| Network/Connectivity | 220 (44%) | 176 (80%) |
| Email | 129 (26%) | 107 (83%) |
| Database | 105 (21%) | 82 (78%) |
| Software/Access | 18 | 15 |
| Server | 14 | 13 |
| Hardware/Print | 6 | 6 |

**Network/Connectivity** and **Email** together account for 70% of tickets and sustain very high breach rates. These are the highest-volume, highest-risk categories.

---

## 2. Priority vs. SLA Breach

Counterintuitively, Critical tickets do not breach at a higher rate than High tickets:

| Priority | Tickets | Breached | Within SLA | Breach Rate |
|---|---|---|---|---|
| Critical | 88 | 72 | 0 | 81.8% |
| High | 379 | 310 | 18 | 81.8% |
| Moderate | 33 | 25 | 3 | 75.8% |

- **No Critical tickets resolved within SLA** — this is a serious finding.
- High-priority tickets make up 75.8% of the entire ticket volume.
- Priority triage does not appear to be improving resolution timeliness.

---

## 3. Resolution Time

- **Mean resolution (Breached tickets):** ~271 hours (~11 days)
- **Mean resolution (Within SLA):** ~14 hours
- The gap is stark: compliant resolutions are ~19× faster.
- **72 tickets (14.4%)** have no `resolution_hours` recorded (`Unknown` SLA status), likely indicating incomplete closure data or tickets closed before opening timestamp anomalies.

---

## 4. Assignee Performance

All five agents show similarly high breach rates, suggesting a systemic capacity or process issue rather than individual underperformance:

| Assignee | Tickets | Breach Rate | Mean Hours |
|---|---|---|---|
| Fred Luddy | 84 | **90.5%** | 750 |
| Luke Wilson | 104 | 82.7% | 160 |
| Beth Anglin | 98 | 81.6% | 136 |
| Charlie Whitherspoon | 103 | 81.6% | 150 |
| Howard Johnson | 100 | 81.0% | 160 |

> ⚠️ **Fred Luddy is a notable outlier**: same breach rate range as peers but a mean resolution time of ~750 hours — roughly 4–5× higher. This could reflect assignment to the most complex tickets or a performance gap worth investigating.

---

## 5. Category / Assignment Group Mismatches

A non-trivial share of tickets show **category ≠ assignment_group** (e.g., category = "Hardware" but routed to "Network"). These misclassifications likely contribute to delays and should be audited — incorrect routing adds queue time before the right team even begins work.

---

## 6. Open / Stale Tickets

- **11 tickets in "New"** and **11 "In Progress"** state — likely unresolved at data snapshot time. These are candidates for immediate triage.

---

## Summary: What's Worth Analyzing

| Priority | Finding |
|---|---|
| 🔴 High | 81% breach rate is systemic — focus on process/capacity, not just individual tickets |
| 🔴 High | Zero Critical tickets resolved within SLA |
| 🟠 Medium | Fred Luddy's ~750h mean resolution vs. ~150h peers |
| 🟠 Medium | Category–group mismatches causing likely misrouting |
| 🟡 Low | 72 tickets with no resolution time recorded (Unknown SLA) |
| 🟡 Low | 22 open tickets requiring triage |
