---
dataset: flag_9
scenario: predictive_hardware
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "is_hardware_anomaly_window"
query: "What signals indicate a hardware incident is in the anomaly window?"
source_table: augment_table/flag_9/predictive_hardware/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:21:35.658321+00:00
wall_seconds: 84.35
---

# Hardware Incident Anomaly Window: Signal Analysis

**Query:** What signals indicate a hardware incident is in the anomaly window?  
**Dataset:** 600 incidents total; 182 categorized as `Hardware` (30.3%)  
**Anomaly window definition:** Hardware incidents with resolution time ≥ 241.5 hours (75th percentile), yielding **46 anomaly incidents** (25.3%) and **136 normal incidents**.

---

## Method Note

TAPP-generated columns used in this report: `incident_category`, `failure_mode`, `symptom_severity_signal`, `resolution_lag_band`, `affected_scope`, `opener_to_closer_match`, `software_update_related`. Original structured columns (`priority`, `opened_at`, `closed_at`, `assignment_group`, `caller_id`, `state`) are used as primary evidence; TAPP columns add semantic granularity where noted. `software_update_related` was uniformly `False` for all 182 hardware incidents and provides no discriminating signal.

---

## Key Findings Summary

| Signal | Anomaly Rate | N | Strength |
|--------|-------------|---|----------|
| `resolution_lag_band` = `over_fourteen_days` | **100%** | 5 | ★★★★★ |
| `resolution_lag_band` = `eight_to_fourteen_days` | **50.6%** | 81 | ★★★★☆ |
| `resolution_lag_band` = `same_day` / `two_to_three_days` / `four_to_seven_days` | **0%** | 96 | ★★★★★ (negative) |
| `affected_scope` = `shared_resource` | 42.9% | 7 | ★★★☆☆ |
| `affected_scope` = `server_room` | 40.0% | 5 | ★★★☆☆ |
| `failure_mode` = `connection_failure` | 40.0% | 5 | ★★★☆☆ |
| `failure_mode` = `not_responding` | 36.8% | 19 | ★★★☆☆ |
| `priority` = `1 - Critical` or `2 - High` | 31.2% / 27.6% | 16 / 145 | ★★☆☆☆ |
| `priority` = `3 - Moderate` | 4.8% | 21 | ★★★☆☆ (negative) |

---

## 1. Strongest Signal: `resolution_lag_band` (TAPP)

This TAPP column is the clearest predictor. Anomaly window membership is **perfectly correlated** with lag bands ≥ 8 days:

| `resolution_lag_band` | Anomaly (n) | Total | Rate |
|-----------------------|------------|-------|------|
| `same_day` | 0 | 26 | 0% |
| `two_to_three_days` | 0 | 20 | 0% |
| `four_to_seven_days` | 0 | 50 | 0% |
| `eight_to_fourteen_days` | 41 | 81 | **50.6%** |
| `over_fourteen_days` | 5 | 5 | **100%** |

> **Interpretation:** Any hardware incident with `resolution_lag_band` ∈ {`eight_to_fourteen_days`, `over_fourteen_days`} is either in or approaching the anomaly window. The 86 incidents in these bands account for **100% of all anomaly-window cases**.

---

## 2. Failure Mode Signals (TAPP: `failure_mode`)

Among modes with ≥ 5 incidents:

| `failure_mode` | Anomaly (n) | Total | Rate |
|----------------|------------|-------|------|
| `connection_failure` | 2 | 5 | 40.0% |
| `not_responding` | 7 | 19 | **36.8%** |
| `flickering_display` | 2 | 6 | 33.3% |
| `not_turning_on` | 5 | 18 | 27.8% |
| `malfunction` | 28 | 126 | 22.2% |
| `overheating` | 0 | 4 | 0% |

`not_responding` and `connection_failure` carry elevated anomaly risk relative to the 25.3% baseline. `malfunction` (n=126) is the dominant failure mode and contributes 28 of 46 anomaly incidents by volume. `overheating` (n=4) had 0 anomaly cases.

---

## 3. Scope Signal (TAPP: `affected_scope`)

| `affected_scope` | Anomaly (n) | Total | Rate |
|------------------|------------|-------|------|
| `shared_resource` | 3 | 7 | **42.9%** |
| `server_room` | 2 | 5 | **40.0%** |
| `individual_device` | 14 | 46 | 30.4% |
| `peripheral_device` | 26 | 122 | 21.3% |
| `department` | 1 | 2 | 50% (n too small) |

Incidents touching `shared_resource` or `server_room` scope show elevated anomaly rates, reflecting systemic or infrastructure-level hardware issues that take longer to resolve.

---

## 4. Priority Signal (Original Column)

| `priority` | Anomaly (n) | Total | Rate |
|------------|------------|-------|------|
| `1 - Critical` | 5 | 16 | 31.2% |
| `2 - High` | 40 | 145 | 27.6% |
| `3 - Moderate` | 1 | 21 | **4.8%** |

`3 - Moderate` priority is a strong **negative** indicator—only 1 in 21 moderate hardware incidents entered the anomaly window. However, priority alone is weak as a positive predictor because 90.7% of hardware incidents are `2 - High` or above regardless.

---

## 5. Symptom Severity (TAPP: `symptom_severity_signal`)

| `symptom_severity_signal` | Anomaly (n) | Total | Rate |
|--------------------------|------------|-------|------|
| `malfunction_unresponsive` | 38 | 152 | 25.0% |
| `failure` | 4 | 13 | 30.8% |
| `general_issue` | 4 | 14 | 28.6% |
| `crash_shutdown` | 0 | 2 | 0% |

Distributions are broadly uniform across the baseline (25.3%), so `symptom_severity_signal` adds limited incremental discriminating power beyond what `failure_mode` and `resolution_lag_band` already capture.

---

## 6. Opener-to-Closer Match (TAPP: `opener_to_closer_match`)

Anomaly rate when `opener_to_closer_match = False` is **26.0%** vs. 21.9% when `True`—a marginal difference (n=150 vs. 32). This facet is **weak** as a standalone anomaly signal for hardware incidents.

---

## 7. Incident Sub-Category (TAPP: `incident_category`)

Both hardware sub-categories show similar anomaly rates:
- `hardware` (general): 28/99 = **28.3%**
- `printer`: 18/83 = **21.7%**

Printer-related incidents are slightly less likely to enter the anomaly window, consistent with `peripheral_device` scope being the lowest-risk scope.

---

## 8. Temporal Pattern

Monthly anomaly rates show elevated risk in early 2023 (Jan: 50%, n=8; Sep: 50%, n=4) and the start of 2024 (Jan: 33.3%, n=12), suggesting possible seasonal or infrastructure-cycle effects. Mid-2023 (Jul–Aug) had the highest absolute anomaly volume (24 cases) due to incident surge volume.

---

## Composite Prediction Rule

A hardware incident is likely in the anomaly window when **two or more** of the following hold:

1. **`resolution_lag_band` ∈ `eight_to_fourteen_days` or `over_fourteen_days`** — highest specificity (all anomalies fall here)
2. **`failure_mode` ∈ `not_responding`, `connection_failure`** — elevated base rates (~37–40%)
3. **`affected_scope` ∈ `shared_resource`, `server_room`** — systemic scope (40–43%)
4. **`priority` ∈ `1 - Critical`, `2 - High`** — necessary but not sufficient (rules out only `3 - Moderate`)
5. **`incident_category` = `hardware`** (vs. `printer`) — marginally higher anomaly rate

`software_update_related` is uniformly `False` for hardware incidents and carries no signal.
