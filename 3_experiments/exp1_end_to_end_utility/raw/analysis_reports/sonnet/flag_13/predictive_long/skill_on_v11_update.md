---
dataset: flag_13
scenario: predictive_long
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "duration_like_resolution_value"
query: "What signals are linked to longer resolution duration values?"
source_table: augment_table/flag_13/predictive_long/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:14:48.485936+00:00
wall_seconds: 49.49
---

# Signals Linked to Longer Resolution Duration

## Dataset Overview

The dataset contains 500 closed/resolved incidents. Resolution duration was derived from the `closed_at` column (format `HH:MM.s`, representing elapsed time). Duration ranges from **~11 minutes to ~3,597 minutes**, with a mean of **~1,803 minutes (~30 hours)** and a median of **~1,791 minutes**.

---

## Key Signals Associated with Longer Resolution Duration

### 1. Affected System Scope — Strongest Signal

| Scope | Mean Duration (min) |
|---|---|
| `location_specific` | **2,146** |
| `system_wide` | 1,888 |
| `single_user` | 1,783 |
| `service_wide` | 1,653 |

`location_specific` incidents resolve ~27% slower than `service_wide` incidents. In the top-quartile duration group, `location_specific` accounts for **10.4%** of cases vs. only **3.2%** in the bottom quartile — the largest relative shift of any feature. This is the clearest structural predictor.

---

### 2. Incident Symptom Type

| Symptom Type | Mean Duration (min) |
|---|---|
| `installation_failure` | **1,893** |
| `connectivity_failure` | **1,893** |
| `hardware_malfunction` | 1,826 |
| `sync_failure` | 1,746 |
| `access_denied` | 1,739 |
| `outage` | 1,688 |
| `performance_degradation` | **1,416** |

`connectivity_failure` is the dominant symptom type (n=241, 48%) and is **over-represented in the high-duration quartile** (58.4% vs. 45.6% in the low quartile). Conversely, `performance_degradation` and `outage` are associated with shorter resolutions. `installation_failure` also skews long but has a very small sample (n=11).

---

### 3. Open Hour Band

| Band | Mean Duration (min) |
|---|---|
| `overnight` | **1,874** |
| `after_hours` | 1,802 |
| `business_hours` | **1,715** |

Incidents opened **overnight** take ~9% longer on average than those opened during business hours. The effect is modest but consistent — overnight cases are over-represented in the high-duration quartile (32.8% vs. 29.6%).

---

### 4. Opened Day of Week

| Day | Mean Duration (min) |
|---|---|
| `weekend` | **1,899** |
| `weekday` | 1,766 |

Weekend-opened incidents resolve ~7.5% slower on average. However, the high/low quartile split shows minimal difference (27.2% vs. 26.4%), suggesting this is a mild, consistent shift rather than a tail driver.

---

### 5. Category

| Category | Mean Duration (min) |
|---|---|
| Software | **1,893** |
| Hardware | 1,847 |
| Network | 1,805 |
| Database | 1,750 |
| Inquiry / Help | **1,683** |

`Software` and `Hardware` categories trend longer; `Inquiry / Help` tickets resolve fastest. Differences are moderate (~12% spread).

---

### 6. Priority — Weak / Counterintuitive Signal

| Priority | Mean Duration (min) |
|---|---|
| `3 - Moderate` | **1,887** |
| `1 - Critical` | 1,821 |
| `2 - High` | 1,796 |
| `4 - Low` | **1,500** |

Moderate-priority incidents actually show the longest mean duration, while Critical and High are nearly identical. `4 - Low` resolves fastest. Priority is **not a reliable predictor of long duration** in this dataset — likely reflecting SLA enforcement on critical tickets.

---

### 7. Resolver Match — Negligible Effect

`resolver_match = False` (1,806 min) vs. `True` (1,793 min): effectively no difference. This variable has minimal predictive value for duration.

---

## Summary Table

| Signal | Direction | Strength |
|---|---|---|
| `affected_system_scope = location_specific` | ↑ longer | **Strong** |
| `incident_symptom_type = connectivity_failure` | ↑ longer | Moderate |
| `incident_symptom_type = performance_degradation` | ↓ shorter | Moderate |
| `open_hour_band = overnight` | ↑ longer | Mild |
| `opened_day_of_week = weekend` | ↑ longer | Mild |
| `category = Software/Hardware` | ↑ longer | Mild |
| `priority = 3 - Moderate` | ↑ longer | Weak/counterintuitive |
| `resolver_match` | — | Negligible |

---

## Caveats

- The `Unknown` symptom type (n=1) shows the highest mean duration (2,820 min) but is statistically meaningless.
- Many effects are distributed across the full range rather than being tail-specific; no single factor dominates extreme durations.
- `priority = 4 - Low` (n=4 only) mean should be treated cautiously.
