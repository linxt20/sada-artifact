---
dataset: flag_12
scenario: predictive_inefficient
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "inefficient_resolution"
query: "What signals suggest an incident resolution will be inefficient?"
source_table: augment_table/flag_12/predictive_inefficient/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:14:35.476469+00:00
wall_seconds: 81.7
---

# Signals of Inefficient Incident Resolution
**Dataset:** 500 incidents | **Outcome:** Resolution time (days); "inefficient" = top quartile (> 10.53 days, n = 125, 25%)

---

## Method Note
TAPP-generated columns used in this analysis: `reassignment_signal`, `repeat_incident_signal`, `hardware_failure_severity`, `affected_asset_type`, `shared_vs_personal_asset`. The column `incident_category` was examined but found largely redundant with the original `category` field and not centered here.

---

## 1. Outcome Variable

Resolution time ranges from 1.0 to 21.4 days (median 7.2 d, mean 7.4 d, P75 = 10.5 d). All 500 incidents are closed or resolved; state alone carries no predictive signal.

| Quartile | Threshold (days) | N | Label |
|---|---|---|---|
| Q1–Q3 | ≤ 10.53 | 375 | Efficient |
| Q4 | > 10.53 | 125 | **Inefficient** |

---

## 2. Primary Inefficiency Signals

### 2.1 Reassignment Signal (strongest single predictor)

`reassignment_signal = True` is the most consistently elevated predictor. Incidents flagged for reassignment constitute 67 % of the dataset (336/500) and show a higher inefficiency rate and longer mean resolution time.

| `reassignment_signal` | N | Ineff. rate | Mean days |
|---|---|---|---|
| False | 164 | 23.2 % | 7.07 |
| **True** | **336** | **25.9 %** | **7.61** |

The effect is amplified when combined with system-driven updates (`sys_updated_by = system`), a proxy for automated or unattended closure:

| Auto-close | Reassigned | Ineff. rate | N |
|---|---|---|---|
| No | No | 22.0 % | 109 |
| No | Yes | 23.8 % | 231 |
| Yes | No | 25.5 % | 55 |
| **Yes** | **Yes** | **30.5 %** | **105** |

Incidents both auto-closed and reassigned reach a 30.5 % inefficiency rate — the highest two-variable combination.

### 2.2 Repeat Incident Signal

`repeat_incident_signal = True` (171 incidents, 34 %) marks incidents that recur, indicating unresolved root causes.

| `repeat_incident_signal` | N | Ineff. rate | Mean days |
|---|---|---|---|
| False | 329 | 23.7 % | 7.27 |
| **True** | **171** | **27.5 %** | **7.74** |

Repeat incidents resolved with reassignment are the worst combination:

| `reassignment_signal` | `repeat_incident_signal` | N | Mean days | Ineff. rate |
|---|---|---|---|---|
| False | False | 95 | 7.20 | 22.1 % |
| False | True | 69 | 6.89 | 24.6 % |
| True | False | 234 | 7.30 | 24.4 % |
| **True** | **True** | **102** | **8.32** | **29.4 %** |

### 2.3 Asset Type (`affected_asset_type`)

Workstations and storage devices are the most inefficiency-prone asset types by a wide margin:

| `affected_asset_type` | N | Ineff. rate | Mean days |
|---|---|---|---|
| workstation | 21 | **47.6 %** | 9.20 |
| storage_device | 13 | 30.8 % | 8.87 |
| monitor | 71 | 28.2 % | 7.22 |
| printer | 203 | 26.6 % | 7.66 |
| keyboard | 56 | 25.0 % | 7.79 |
| software | 71 | 22.5 % | 6.94 |
| network_device | 26 | 15.4 % | 6.72 |
| server | 16 | 12.5 % | 6.00 |

Workstation incidents (n=21) are disproportionately inefficient (48 %) and also carry high reassignment signal (62 % of workstation incidents are flagged as reassigned).

### 2.4 Shared vs. Personal Asset (`shared_vs_personal_asset`)

Shared office assets and personally assigned assets both underperform relative to records where asset ownership is unknown:

| `shared_vs_personal_asset` | N | Ineff. rate | Mean days |
|---|---|---|---|
| Unknown | 88 | 20.5 % | 6.78 |
| personal_assigned_asset | 196 | 25.5 % | 7.53 |
| **shared_office_asset** | **216** | **26.4 %** | **7.61** |

Shared office assets have the highest inefficiency rate, plausibly because contention and coordination overhead delay resolution.

### 2.5 Hardware Failure Severity (`hardware_failure_severity`)

This TAPP facet shows weak differentiation across severity levels:

| `hardware_failure_severity` | N | Ineff. rate | Mean days |
|---|---|---|---|
| not_applicable | 47 | 23.4 % | 6.65 |
| intermittent_fault | 24 | 20.8 % | 7.01 |
| complete_failure | 71 | 25.4 % | 7.49 |
| functional_degradation | 358 | 25.4 % | 7.55 |

The spread is narrow (< 5 pp). `hardware_failure_severity` is a **weak predictor** on its own and adds little beyond the original `category` field.

---

## 3. Original Structured Columns

### 3.1 Priority

Counter-intuitively, **critical priority incidents resolve faster** (mean 6.96 d, 18.5 % inefficiency rate) than High or Moderate — consistent with escalation protocols focusing resources. The bulk category "2 - High" (394 incidents) drives most inefficiency.

| Priority | N | Ineff. rate | Mean days |
|---|---|---|---|
| 1 - Critical | 27 | 18.5 % | 6.96 |
| 2 - High | 394 | 25.4 % | 7.50 |
| 3 - Moderate | 77 | 26.0 % | 7.41 |

### 3.2 Category / Assignment Group

Hardware incidents (406/500) dominate and have the longest mean resolution time (7.56 d, handled by the Hardware group). Software and Network incidents resolve faster (6.40 d and 6.73 d, respectively).

| Assignment Group | N | Mean days |
|---|---|---|
| Hardware | 405 | 7.56 |
| Database | 20 | 7.43 |
| Service Desk | 19 | 7.35 |
| Network | 23 | 6.73 |
| Software | 33 | 6.40 |

### 3.3 Update Actor (`sys_updated_by`)

System-automated updates correlate with slower resolution (mean 8.29 d, 28.8 % inefficiency rate) vs. employee-driven (7.28 d, 23.5 %) or admin-driven (7.12 d, 23.0 %) updates — suggesting incidents closed by automation may lack proper human follow-through.

---

## 4. Summary of Inefficiency Signals

| Signal | Type | Ineff. rate (True vs False or worst bin) | Strength |
|---|---|---|---|
| `affected_asset_type` = workstation | TAPP | 47.6 % | **Strong** |
| `reassignment_signal` = True + `sys_updated_by` = system | TAPP + structured | 30.5 % | **Strong** |
| `reassignment_signal` = True + `repeat_incident_signal` = True | TAPP + TAPP | 29.4 % | **Moderate–Strong** |
| `repeat_incident_signal` = True | TAPP | 27.5 % | Moderate |
| `shared_vs_personal_asset` = shared_office_asset | TAPP | 26.4 % | Moderate |
| `reassignment_signal` = True | TAPP | 25.9 % | Moderate |
| Priority = 2 - High or 3 - Moderate | Structured | ~25–26 % | Moderate |
| Category = Hardware | Structured | ~26 % | Moderate |
| `hardware_failure_severity` | TAPP | ≤ 5 pp spread | **Weak** |

**Key finding:** The clearest predictors of inefficient resolution are **(1) workstation asset type**, **(2) co-occurrence of reassignment and repeat-incident signals** (mean 8.32 d, 29 % inefficiency rate), and **(3) system-automated closure combined with reassignment**. Priority escalation to Critical actually *reduces* inefficiency. Hardware incidents on shared office assets with reassignment and recurrence represent the highest-risk combination.
