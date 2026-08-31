---
dataset: flag_13
scenario: focus_inference
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth attention in these incident descriptions."
source_table: augment_table/flag_13/focus_inference/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:14:39.410703+00:00
wall_seconds: 49.7
---

# Incident Description Analysis — What's Worth Attention

## Overview

The dataset contains **500 IT incidents** spanning early 2023. Each incident description encodes five analytically useful facets: **affected service**, **failure symptom type**, **scope**, **recurrence**, and **priority**. Together these reveal where systemic risk concentrates.

---

## 1. Affected Service — Where Volume Clusters

| Service | Count | % of Total |
|---|---|---|
| Database | 135 | 27% |
| Email | 134 | 27% |
| VPN | 109 | 22% |
| Network Connectivity | 56 | 11% |
| Server | 23 | 5% |
| WiFi | 16 | 3% |
| Software | 13 | 3% |
| Printer / Other | 14 | 3% |

**Database, Email, and VPN together account for ~76% of all incidents.** This is the primary triage signal: the three services dominate description volume and drive downstream analysis.

---

## 2. Failure Symptom Type — What Actually Goes Wrong

| Symptom | Count | Notes |
|---|---|---|
| Connection failure | 225 (45%) | Dominant; VPN (96), DB (55), Network (36) |
| Access denied | 108 (22%) | DB (55), Email (22), Network (12) |
| Not responding | 48 (10%) | Email (39) — concentrated there |
| Outage | 43 (9%) | Email (29) — highest severity signal |
| Unknown | 25 (5%) | Mostly printers; data quality gap |
| Other symptoms | 51 (10%) | Slow perf, sync, install failures |

**Connection failure is the single most common mechanism** (45%), but its spread across VPN and DB differs: VPN failures are almost exclusively connection-type, while DB failures split evenly between connection and access-denied — suggesting different root causes (auth vs. routing).

---

## 3. Priority & Severity — Where the Critical Mass Lies

- **83 incidents (17%) are Priority 1 – Critical**; 391 (78%) are Priority 2 – High.
- **Email is disproportionately critical**: 43 of 83 Critical incidents (~52%) involve email.
- Critical incidents are dominated by **outage** (37) and **not_responding** (20) symptoms — both signaling full service unavailability.
- **59 of 83 Critical incidents (71%) are system-wide in scope**, making email outages and email server unresponsiveness the single highest-stakes pattern in the dataset.

---

## 4. Scope — Individual vs. Systemic Impact

| Scope | Count | Key Services |
|---|---|---|
| Individual user | 308 (62%) | VPN (majority), DB, Email clients |
| System-wide | 156 (31%) | Email (85), Database (47), Server (19) |
| Location-specific | 36 (7%) | WiFi, Network |

**System-wide scope is concentrated in email and database.** When descriptions mention "server down," "email system outage," or "database server issue," they reliably map to system_wide scope and higher priority — these phrases are the strongest triage signals in the text.

---

## 5. Recurrence — Chronic vs. One-Off

- **373 of 500 incidents (75%) are flagged as recurring** within the period.
- Recurrence is near-universal for VPN (107/109 = 98%), Database (118/135 = 87%), and Email (117/134 = 87%).
- **High recurrence + high volume = structural/unresolved root causes**, particularly for VPN connectivity and database access.
- WiFi and printer incidents show lower recurrence, suggesting more isolated events.

---

## 6. Cross-Assignment & Self-Resolution

- **402 incidents (80%) required cross-team assignment**, indicating most descriptions reflect issues that cannot be resolved within the first-touch team.
- Only **96 incidents (19%) self-resolved** — nearly all non-self-resolved cases needed active intervention.
- Cross-assignment is nearly universal for VPN (90/109), Email (105/134), and Database (105/135) — consistent with these services requiring infrastructure-team escalation.

---

## 7. Patterns Most Worth Attention

| Signal | Why It Matters |
|---|---|
| **Email outages (system-wide, Critical)** | 43 Critical incidents, 85 system-wide; highest blast radius |
| **Database access-denied + connection failures** | 110 incidents split evenly between two distinct failure modes; likely two separate root causes |
| **VPN connection failures (recurring, 98%)** | Near-total recurrence suggests unresolved infrastructure; 109 incidents |
| **"Not responding" in email** | 39 of 48 not_responding incidents are email — server-side availability issue |
| **Unknown symptom type (25 incidents)** | Mostly printers; data quality gap that may undercount printer severity |

---

## Caveats & Weak Evidence

- **`opened_hour_bucket`** data is available but not analyzed here; off-hours incidents may warrant separate review for staffing impact.
- **25 incidents have `Unknown` failure_symptom_type** — mostly printers — limiting conclusions about that category.
- Priority is assigned externally; the descriptions themselves don't always signal severity explicitly (e.g., "Cannot connect to VPN" appears at both High and Critical).
- The dataset covers a single multi-month window; seasonality or trend analysis would require time-series decomposition beyond this snapshot.
