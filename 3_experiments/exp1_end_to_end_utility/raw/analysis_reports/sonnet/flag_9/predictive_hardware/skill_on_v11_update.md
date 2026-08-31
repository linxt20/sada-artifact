---
dataset: flag_9
scenario: predictive_hardware
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "is_hardware_anomaly_window"
query: "What signals indicate a hardware incident is in the anomaly window?"
source_table: augment_table/flag_9/predictive_hardware/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:21:05.941814+00:00
wall_seconds: 59.83
---

# Hardware Incident Anomaly Window: Signal Analysis

## Overview

The dataset contains **600 incidents** spanning multiple categories. Hardware incidents total **182 records** (30.3% of all incidents), making them the primary focus. The analysis identifies signals correlated with a hardware incident falling within an **anomaly window**, defined by two Boolean flag columns: `incident_volume_burst` and `recurrence_signal`.

---

## Primary Anomaly Window Signals

### 1. `incident_volume_burst` (True)
- **80 hardware incidents** (43.9% of hardware) carry this flag.
- **Uniquely hardware**: `incident_volume_burst` is **True exclusively for Hardware category** incidents — it is `False` for 100% of Software, Network, Database, and Inquiry/Help incidents in this dataset.
- This makes `incident_volume_burst = True` an **unambiguous predictor** that a hardware incident is in the anomaly window.
- Dominant failure symptoms in burst incidents: `not_responding` (33), `malfunction_intermittent` (16), `display_issue` (10).
- Split evenly between `printer` (40) and `hardware` (40) incident sub-categories.
- Predominantly `peripheral_device` scope (63 of 80).

### 2. `recurrence_signal` (True)
- **76 hardware incidents** (41.8% of hardware) carry this flag.
- Nearly hardware-exclusive: the recurrence signal rate is 41.8% for Hardware vs. only 2.6% for Network and ≤1% for other categories.
- Dominant failure symptoms: `malfunction_intermittent` (38), `not_responding` (11), `no_power` (9), `physical_damage` (6).
- Skews more toward `hardware` sub-category (46) over `printer` (30), and both `peripheral_device` and `single_device` scopes are well-represented.

> **Note:** The two flags are **mutually exclusive** in this dataset — no incident has both `incident_volume_burst = True` and `recurrence_signal = True` simultaneously. Combined, they cover **156 of 182 hardware incidents (85.7%)**.

---

## Secondary / Corroborating Signals

| Signal | In Anomaly Window | Not in Anomaly Window | Notes |
|--------|------------------|-----------------------|-------|
| `caller_repeat_reporter = True` | 88.5% | 100% | Repeat callers appear in *both* groups — not discriminating alone |
| `category = Hardware` | Prerequisite | — | All anomaly-window flags are hardware-only |
| `failure_symptom_type` = `malfunction_intermittent` | 54 (34.6%) | 5 (19.2%) | Elevated in anomaly window |
| `failure_symptom_type` = `not_responding` | 44 (28.2%) | 15 (57.7%) | Higher in non-anomaly window — weak negative signal |
| `affected_system_scope` = `peripheral_device` | 119 (76.3%) | 15 (57.7%) | Elevated in anomaly window |
| `priority` = `2 - High` or `1 - Critical` | 140 (89.7%) | 26 (100%) | Slightly higher critical/high outside anomaly — not strongly predictive |
| `software_trigger_present` | 0% (all hardware) | 0% | No discriminating power |

---

## Key Findings

1. **`incident_volume_burst = True`** is the strongest single indicator: it appears **only** in hardware incidents and tags 44% of them as anomaly-window events.
2. **`recurrence_signal = True`** is the second strongest: nearly exclusive to hardware (41.8% rate) and mutually exclusive with `incident_volume_burst`, suggesting it captures a distinct pathway to anomaly status.
3. Together, these two Boolean flags define the anomaly window completely — an incident is in the anomaly window **if and only if** at least one of them is `True`.
4. `malfunction_intermittent` and `display_issue` failure symptoms are disproportionately represented within the anomaly window; `not_responding` is relatively more common *outside* it.
5. `peripheral_device` scope is modestly elevated in the anomaly window compared to non-anomaly hardware incidents.

---

## Exceptions and Caveats

- **26 hardware incidents (14.3%)** have neither flag set, confirming that hardware category alone is necessary but not sufficient for anomaly window classification.
- `caller_repeat_reporter = True` is present in virtually all hardware incidents regardless of anomaly status — it should not be used as a sole discriminator.
- The dataset contains no hardware incidents with `software_trigger_present = True`, limiting the ability to assess software-hardware interaction as an anomaly signal.
- Small counts for some symptom types (e.g., `overheating`: 4, `crash_shutdown`: 1) limit statistical confidence for those sub-groups.

---

## Decision-Ready Summary

> A hardware incident is in the **anomaly window** when **`incident_volume_burst = True`** (volume spike signal) **or `recurrence_signal = True`** (repeat-failure signal). These two flags are mutually exclusive, collectively cover 85.7% of hardware incidents, and are virtually absent from all other incident categories. Supporting context includes `malfunction_intermittent` or `display_issue` symptom types, `peripheral_device` scope, and `caller_repeat_reporter = True` — though the latter is too prevalent across hardware overall to be individually decisive.
