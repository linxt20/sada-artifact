---
dataset: flag_6
scenario: focus_inference
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth analyzing in these incident tickets."
source_table: augment_table/flag_6/focus_inference/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:19:46.402964+00:00
wall_seconds: 67.55
---

# Incident Ticket Analysis Report

**Dataset:** 500 incident tickets | **Period:** Jan–Feb 2023  
**Focus variables:** `recurrence_signal`, `self_resolved`, `is_open_unresolved`, priority, affected system, symptom type, scope, access context, and time-of-day patterns.

---

## 1. What the Ticket Mix Looks Like

| Dimension | Dominant category | Share |
|---|---|---|
| Priority | 2 - High | 75.8% |
| Category | Network | 56.8% |
| Affected system | Email | 27.2% |
| Symptom type | no_access_cannot_connect | 50.2% |
| Incident scope | Individual user | 57.0% |
| State | Resolved / Closed | 95.6% |

The queue is overwhelmingly connectivity-related: email, VPN, database access, and internet connectivity together account for **83% of all tickets**. Half of all symptoms are simple "can't connect" failures, suggesting a recurring infrastructure or authentication problem rather than diverse one-off faults.

---

## 2. Recurrence Signal — The Most Striking Pattern

**94.4% of tickets carry `recurrence_signal = True`**, indicating nearly every issue is a known repeat. This is the single most actionable finding.

| Affected system | Recurrence rate |
|---|---|
| Email | 100% |
| VPN | 100% |
| WiFi | 100% |
| Network drive/share | 100% |
| Database | 99% |
| Internet connectivity | 98% |
| Server | 82% |
| OS/Software | 29% |
| Web application | 0% |

**Interpretation:** Core connectivity services (email, VPN, database) are generating repeat tickets at near-100% rates. This strongly suggests the root causes are not being eliminated — only symptoms are being treated. OS/software issues (29%) and web applications (0%) are the exception and may reflect genuinely novel or one-off problems.

---

## 3. Self-Resolution (~20% Overall)

About **1 in 5 tickets resolves without IT intervention**. The rate is modestly higher for:
- OS/software (25%) and internet connectivity (25%) — possibly transient glitches users can work around
- VPN (18%) and database (19%) — lower self-resolution consistent with needing privileged access

Critical-priority incidents self-resolve at only **13.6%** vs. ~21% for High/Moderate, which is expected. No system shows an anomalously high self-resolution rate that would suggest tickets are being closed prematurely, except for a notable pattern: `recurrence_signal` is True even for self-resolved tickets, reinforcing the repeat-failure narrative.

> **Weak evidence caveat:** ~22 tickets have `self_resolved = NaN`; these are excluded. If systematically missing for a category, rates could shift slightly.

---

## 4. Priority and Criticality Distribution

**88 Critical (1-Critical) tickets** — 17.6% of the queue — are concentrated in:

| System | Critical count |
|---|---|
| Email | 46 (34% of all email tickets) |
| Database | 23 (22%) |
| Server | 10 (26%) |
| Internet connectivity | 8 (12%) |

**VPN has zero Critical tickets** despite being the second most common system. VPN incidents are consistently logged as High, suggesting a policy classification choice rather than a severity finding.

---

## 5. Infrastructure-Wide vs. Individual Impact

**38% of tickets are infrastructure_wide**, which is notable for what it maps to:

| Symptom type | % Infrastructure-wide |
|---|---|
| outage_crash | 92% |
| service_not_responding | 97.5% |
| no_access_cannot_connect | 18% |
| unstable_intermittent | 28% |
| sync_error | 17% |

Outages and service-non-response almost always have broad blast radius. No-access complaints are mostly individual, likely password/permission issues rather than systemic failures.

---

## 6. Time-of-Day Patterns

Tickets are opened **disproportionately outside business hours**:

| Time window | Ticket count |
|---|---|
| After hours (18:00–24:00) | 205 (41%) |
| Business hours (08:00–18:00) | 180 (36%) |
| Overnight (00:00–08:00) | 115 (23%) |

64% of tickets originate outside standard business hours. Critical incidents occur across all windows (after-hours: 30, business: 40, overnight: 18), indicating 24/7 on-call coverage may be warranted. The after-hours skew could also reflect batch jobs, automated system alerts, or a distributed/remote workforce — note that **92 tickets carry `access_context = remote`**.

---

## 7. Resolution Time

Overall median resolution is ~6.3 days. Counterintuitively, **Critical tickets resolve faster (median 5.5 days)** than High (6.4 days) or Moderate (6.5 days), likely because critical incidents receive more immediate escalation.

| System | Mean resolution (days) |
|---|---|
| Network drive/share | 22.3 |
| OS/Software | 14.2 |
| VPN | 11.2 |
| Email | 7.9 |
| WiFi | 5.6 |

Network drive/share and OS/software tickets take significantly longer, possibly due to routing through the Hardware group or less mature runbooks. VPN tickets (11.2 days mean) deserve attention given high volume and near-100% recurrence.

---

## 8. Open/Unresolved Tickets

Only **22 tickets (4.4%) remain open/unresolved**, split: 15 High-priority, 4 Critical, 3 Moderate. The small number limits conclusions, but the 4 lingering Critical tickets warrant immediate review.

---

## Key Takeaways for Decision-Making

1. **Recurrence is the defining problem** — near-universal recurrence across email, VPN, and database indicates systemic root causes that are never closed out. A root-cause elimination sprint on these three systems would address the majority of ticket volume.

2. **Email is the highest-burden system** — most tickets, highest critical count, 100% recurrence; prioritize it first.

3. **VPN is a high-volume, slow-resolving pattern** — 110 tickets, 0 Critical (likely underclassified), 11.2-day mean resolution, 100% recurrence. Likely needs a dedicated fix project.

4. **After-hours volume is dominant** — 64% of tickets open outside business hours; determine whether this reflects legitimate 24/7 operations or a delayed reporting artifact.

5. **Self-resolution (~20%) is modest but consistent** — not a quality/closure concern, but auto-resolution or self-service tooling could deflect a meaningful fraction of routine connectivity tickets.

6. **OS/software and web application tickets behave differently** — lower recurrence, longer resolution, more novel symptoms; they may benefit from a separate triage workflow.
