---
dataset: flag_13
scenario: predictive_long
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "duration_like_resolution_value"
query: "What signals are linked to longer resolution duration values?"
source_table: augment_table/flag_13/predictive_long/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:15:30.116304+00:00
wall_seconds: 85.12
---

# Signals Linked to Longer Resolution Duration

**Dataset:** 500 incidents · **Outcome:** `closed_at` (resolution duration, minutes) · **Mean:** 30.1 min · **Median:** 29.8 min · **P25/P75:** 15.9 / 45.1 min

---

## Method Note

TAPP-generated columns used in this analysis: `incident_category`, `affected_system_layer`, `failure_mode`, `location_scope`, `opened_hour_of_day`. Columns `reassigned`, `assigned_agent`, and `caller_id_group` were examined but showed negligible or no incremental signal beyond original structured fields.

---

## 1. Category and Priority (Original Structured Columns)

`category` is the strongest original predictor of duration.

| Category | Mean (min) | Median (min) | N |
|---|---|---|---|
| Software | **31.5** | 33.5 | 73 |
| Hardware | **30.8** | 32.0 | 25 |
| Network | 30.1 | 29.7 | 260 |
| Database | 29.2 | 29.7 | 134 |
| Inquiry / Help | 28.0 | 28.6 | 8 |

`priority` alone shows a counterintuitive flat pattern (Critical: 30.3 min vs Moderate: 31.5 min), but cross-tabulation reveals meaningful interactions:

| Priority × Category | Software | Hardware | Database | Network |
|---|---|---|---|---|
| 1 - Critical | **37.1** | **34.7** | 31.8 | 28.1 |
| 2 - High | 29.5 | 32.7 | 28.6 | 30.6 |
| 3 - Moderate | **39.3** | 20.7 | 32.8 | 27.7 |

**Software + Critical** (mean 37.1 min, n=9) and **Software + Moderate** (mean 39.3 min, n=subset) are the slowest combinations.

---

## 2. Assignment Group and Agent (Original Structured Columns)

`assignment_group = Service Desk` has the longest mean duration (32.8 min, n=34), while `Network` (29.9 min, n=287) and `Software` (28.5 min, n=30) are faster. Individual agents show modest spread: Charlie Whitherspoon (31.1 min, n=91) vs Howard Johnson (28.8 min, n=101). These differences are minor relative to category effects.

---

## 3. Location Scope (TAPP: `location_scope`)

`location_scope` adds meaningful signal not captured by existing columns.

| location_scope | Mean (min) | Median (min) | Long-incident Rate (≥P75) | N |
|---|---|---|---|---|
| building_floor_specific | **37.8** | 39.6 | 42% | 12 |
| localized | **33.6** | 32.0 | 44% | 25 |
| Unknown | 33.5 | 35.6 | 30% | 87 |
| system_wide | 28.8 | 27.7 | **22%** | 376 |

Incidents scoped to a **specific building/floor or localized area** take ~31% longer on average than system-wide incidents (37.8 vs 28.8 min). The long-incident rate for localized incidents (44%) is double that of system-wide incidents (22%). This is a meaningful signal despite smaller sample sizes (n=12–25) and warrants monitoring.

---

## 4. Incident Category (TAPP: `incident_category`)

| incident_category | Mean (min) | Median (min) | N |
|---|---|---|---|
| server | **33.3** | 35.4 | 22 |
| network_connectivity | **31.4** | 31.8 | 72 |
| vpn_access | 30.3 | 30.3 | 109 |
| printing | 30.4 | 24.8 | 9 |
| database | 29.6 | 30.0 | 136 |
| other | 29.5 | 24.7 | 18 |
| email_service | 29.0 | 27.1 | 134 |

**Server incidents** (mean 33.3 min, n=22) and **network_connectivity** (31.4 min, n=72) are consistently slower. `email_service` incidents resolve fastest (29.0 min). This refines the broader `category = Network` signal by separating fast email issues from slower connectivity failures.

---

## 5. Failure Mode (TAPP: `failure_mode`)

| failure_mode | Mean (min) | Median (min) | N |
|---|---|---|---|
| installation_failure | **31.6** | 28.0 | 11 |
| connectivity_failure | **31.4** | 31.2 | 229 |
| outage | 29.6 | 29.7 | 81 |
| access_denied | 29.5 | 30.7 | 115 |
| degraded_performance | 25.8 | 25.8 | 16 |
| other | 26.4 | 22.4 | 46 |

**Connectivity_failure** is the largest-volume slow failure mode (n=229, mean 31.4 min). **Degraded_performance** and **other** resolve fastest. Outages are not the slowest, suggesting that well-practiced runbooks may help even high-severity disruptions.

---

## 6. Affected System Layer (TAPP: `affected_system_layer`)

| affected_system_layer | Mean (min) | Median (min) | N |
|---|---|---|---|
| network_infrastructure | **30.5** | 30.5 | 186 |
| client_side | **30.5** | 27.6 | 78 |
| server_side | 29.5 | 29.7 | 236 |

Differences across system layers are small (~1 min), so `affected_system_layer` adds limited additional discrimination beyond `category` and `failure_mode`.

---

## 7. Time of Day (TAPP: `opened_hour_of_day` and raw `opened_at`)

Time-of-day bands show modest variation. Raw hourly data highlights peaks at hours 2, 17–18, and 20 (mean ~35–36 min) vs troughs at noon–2 PM (~26 min). The TAPP `opened_hour_of_day` buckets flatten this signal (all bands within 31±1 min), so raw hour is more informative if precise scheduling analysis is needed.

---

## 8. Reassignment (TAPP: `reassigned`)

Contrary to expectation, `reassigned=True` (mean 30.0 min, n=403) vs `reassigned=False` (mean 30.1 min, n=97) shows **no duration penalty**. This signal is weak and not decision-relevant.

---

## Summary: Ranked Signals for Longer Resolution Duration

| Rank | Signal | Type | Δ vs Baseline | Key Values |
|---|---|---|---|---|
| 1 | `location_scope` = localized / building | TAPP | +5–9 min (+17–26%) | building_floor_specific: 37.8 min |
| 2 | `category` = Software (esp. + Critical/Moderate) | Original | +1.4–9 min | Software+Critical: 37.1 min |
| 3 | `incident_category` = server | TAPP | +3.3 min | 33.3 min |
| 4 | `failure_mode` = connectivity_failure | TAPP | +1.4 min (large volume) | 31.4 min, n=229 |
| 5 | `assignment_group` = Service Desk | Original | +2.7 min | 32.8 min |
| 6 | Raw hour = 2 AM, 5–6 PM, 8 PM | Original | +5–6 min | ~35–36 min |

**Primary conclusion:** Geographically-scoped incidents (`location_scope` = localized or building-specific), software incidents with critical/moderate priority, and server-type failures (`incident_category = server`, `failure_mode = connectivity_failure`) are the clearest combined signals for above-median resolution duration. Priority alone does not predict duration; its interaction with category matters.
