---
dataset: flag_13
scenario: whatif_duration
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "resolution_duration"
query: "If the most common operational burdens described in the text were eliminated, how much would resolution duration drop?"
source_table: augment_table/flag_13/whatif_duration/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:15:23.324095+00:00
wall_seconds: 76.01
---

# What-If Analysis: Eliminating Common Operational Burdens and Resolution Duration

## Dataset Overview

- **Total incidents:** 500
- **Overall mean resolution duration:** 30.05 minutes
- **Overall median resolution duration:** 29.85 minutes
- Resolution duration is encoded in the `closed_at` column (format: `MM:SS.s`).

---

## Identifying the Most Common Operational Burdens

The dataset's text fields (`short_description`, `failure_symptom_type`, `incident_category`, `scope_indicator`) reveal two dominant operational burdens:

### 1. `cannot_connect` Failure Symptom (Most Frequent — 233 of 500 incidents, 46.6%)

The single most common burden described in incident text is connectivity failures — phrased as *"cannot connect"*, *"unable to connect"*, or *"unable to access"*. These map directly to `failure_symptom_type = cannot_connect`.

| Symptom Type | Count | Mean Duration (min) |
|---|---|---|
| `cannot_connect` | 233 | **31.62** |
| All others | 267 | 28.68 |

The gap of ~3 minutes is consistent: cannot_connect incidents run systematically longer, likely because diagnosis requires iterative checks across network/VPN/firewall layers.

### 2. Location-Specific Scope (32 incidents, 6.4%)

Incidents with `scope_indicator = location_specific` (e.g., *"printing issues in office"*, *"connection issues with office WiFi"*) are the most burdensome by duration:

| Scope | Count | Mean Duration (min) |
|---|---|---|
| `location_specific` | 32 | **35.13** |
| `individual` | 267 | 29.21 |
| `system_wide` | 201 | 30.36 |

These require on-site or floor-level coordination, adding nearly **6 minutes** per ticket over individual-scope incidents.

---

## What-If Simulations

### Scenario 1: Eliminate `cannot_connect` burden
If the 233 cannot_connect incidents resolved at the same pace as other incident types (28.68 min):

- **New projected mean:** 28.68 min
- **Duration drop: −1.37 min (−4.6%)**

### Scenario 2: Eliminate location-specific scope burden
If the 32 location-specific incidents resolved at the non-location-specific rate (29.70 min):

- **New projected mean:** 29.70 min
- **Duration drop: −0.35 min (−1.2%)**

### Scenario 3: Eliminate both burdens (combined)
- **New projected mean:** 28.50 min
- **Duration drop: −1.55 min (−5.1%)**

---

## Other Factors and Weak Evidence

| Factor | Finding |
|---|---|
| `reassigned_resolver` | Surprisingly **no impact**: True (30.03 min, n=403) vs. False (30.15 min, n=97). Reassignment is very common (80.6%) but does not drive duration in this dataset. |
| `off_hours_open` | Minimal difference: off-hours 29.73 min vs. regular hours 30.34 min. No consistent burden. |
| `recurring_caller_pattern` | Nearly universal (497/500 = True), making it a non-differentiator. |
| `outage_down` incidents | Small sample (n=38) but 33.4 min mean — a secondary concern if outage-handling processes were improved. |

---

## Summary and Decision Guidance

| Intervention | Est. Duration Reduction | Confidence |
|---|---|---|
| Resolve `cannot_connect` faster (tooling, runbooks) | **~1.4 min (~4.6%)** | Moderate — consistent pattern, large sample |
| Reduce location-specific dispatch overhead | **~0.4 min (~1.2%)** | Low — small sample (n=32) |
| Both combined | **~1.6 min (~5.1%)** | Moderate |

The most impactful lever is addressing **connectivity-failure (`cannot_connect`) incidents**, which account for nearly half of all tickets and average ~3 minutes longer than other types. Targeted runbooks, automated pre-checks, or self-service VPN/network diagnostics would be the highest-value interventions.

> **Caveat:** The `closed_at` field appears to encode relative duration rather than a wall-clock timestamp; all duration values fall within a 0–60 minute range. Absolute durations should be validated against source system data before using these figures for SLA commitments.
