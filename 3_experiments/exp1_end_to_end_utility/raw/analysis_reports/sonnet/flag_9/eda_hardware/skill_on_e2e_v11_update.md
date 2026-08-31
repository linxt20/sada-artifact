---
dataset: flag_9
scenario: eda_hardware
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "hardware_incident"
query: "What in an incident's description tends to signal it's a hardware problem?"
source_table: augment_table/flag_9/eda_hardware/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:20:47.072013+00:00
wall_seconds: 59.47
---

# What Signals a Hardware Incident? — EDA Report

**Query:** What in an incident's description tends to signal it's a hardware problem?  
**Dataset:** 600 incidents | **Hardware incidents:** 183 (30.5%) | **Non-hardware:** 417 (69.5%)

---

## Method Note

TAPP-generated columns used in this analysis: `is_hardware_incident`, `hardware_failure_mode`, `scope_context`, `recurrence_signal`, `incident_domain`. The column `software_component_involved` was checked but contained no values for hardware incidents (all NaN) and is not informative here.

---

## 1. Primary Signal: Device/Peripheral Names in Short Description

The strongest discriminators are explicit **physical device references** in the `short_description` field. Among hardware incidents (n=183), the following keywords appear almost exclusively in hardware tickets and are essentially absent from non-hardware incidents:

| Keyword | HW count | HW rate | Non-HW count | Non-HW rate |
|---|---|---|---|---|
| `printer` | 81 | 44.3% | 0 | 0.0% |
| `monitor` | 26 | 14.2% | 0 | 0.0% |
| `keyboard` | 24 | 13.1% | 0 | 0.0% |
| `screen` / `display` | 17 | 9.3% | 1 | 0.2% |
| `mouse` | 7 | 3.8% | 0 | 0.0% |
| `flickering` | 6 | 3.3% | 0 | 0.0% |
| `not turning on` | 7 | 3.8% | 0 | 0.0% |
| `boot` | 3 | 1.6% | 0 | 0.0% |
| `hardware` (explicit) | 11 | 6.0% | 0 | 0.0% |

**Interpretation:** Mentioning any peripheral (printer, monitor, keyboard, mouse) or physical state (screen flickering, not turning on, boot failure) is a near-perfect predictor of a hardware incident.

---

## 2. Failure Verb Patterns

Certain **functional failure phrases** in descriptions are strongly skewed toward hardware:

| Phrase | HW count | HW rate | Non-HW count | Non-HW rate |
|---|---|---|---|---|
| `malfunction` | 38 | 20.8% | 6 | 1.4% |
| `not working` | 33 | 18.0% | 4 | 1.0% |
| `not functioning` | 24 | 13.1% | 1 | 0.2% |
| `not responding` | 16 | 8.7% | 8 | 1.9% |
| `desktop` | 18 | 9.8% | 3 | 0.7% |
| `laptop` | 7 | 3.8% | 3 | 0.7% |

The phrase "not working" or "malfunction" alone is ~15× more likely in hardware tickets. When combined with a device noun (e.g., *"Printer malfunctioning"*, *"Keyboard not functioning"*), the signal is essentially definitive — all such incidents in this dataset are hardware.

---

## 3. `hardware_failure_mode` (TAPP) Confirms Failure Pattern Distribution

Among the 183 hardware incidents, `hardware_failure_mode` reveals the dominant symptom patterns that appear in descriptions:

| Failure Mode | Count | % of HW |
|---|---|---|
| `not_functioning` | 124 | 67.8% |
| `not_powering_on` | 18 | 9.8% |
| `not_responding` | 16 | 8.7% |
| `intermittent_malfunction` | 10 | 5.5% |
| `connection_failure` | 5 | 2.7% |
| `overheating` | 4 | 2.2% |
| `physical_damage` | 1 | 0.5% |

The bulk of hardware descriptions cluster around "not functioning/working" language (67.8%), confirming that **generic dysfunction language paired with a device noun** is the key signal. Words like "intermittently," "frequently," or "keeps" indicate recurrence.

---

## 4. `scope_context` — Physical Scope Elevates Hardware Probability

Cross-tabulating `scope_context` (TAPP) against `is_hardware_incident`:

| Scope Context | HW Rate | n |
|---|---|---|
| `individual_device` | **87.5%** | ~40 |
| `office_general` | 61.1% | ~18 |
| `specific_room_or_floor` | 45.5% | ~11 |
| `server_room` | 42.9% | ~7 |
| `user_workstation` | 22.8% | ~167 |
| `building_wide` | 0.0% | ~8 |

Descriptions referencing a **specific individual device** are hardware incidents 87.5% of the time. Building-wide scope = 0% hardware, consistent with those being network/infrastructure issues.

---

## 5. `recurrence_signal` — Recurring Issues Are All Hardware

All 35 incidents where `recurrence_signal = True` are hardware incidents (100% hardware rate vs. 19.5% for non-recurring). Descriptions containing language like "frequently," "keeps," "intermittently," or "again" are exclusively hardware tickets in this dataset.

---

## 6. `category` Field Cross-Check

The structured `category` field largely confirms TAPP labels: 182 of 183 hardware incidents have `category = Hardware` (one edge case is `Inquiry / Help`). This validates that the description-level signals identified above are genuine and not artefacts of TAPP labeling.

Priority skews moderate-to-high for hardware: 36.5% of High priority tickets are hardware vs. only 15.4% of Moderate. No Low-priority tickets are hardware.

---

## Summary: Description Signals for Hardware Incidents

A description strongly signals a hardware problem when it contains **any combination** of:

1. **Device/peripheral noun** — *printer, monitor, keyboard, mouse, screen, desktop, laptop, fan*
2. **Physical failure phrase** — *not working, not functioning, malfunction, not turning on, not powering on, not responding, flickering, boot*
3. **Recurrence language** — *frequently, intermittently, keeps, again* (100% hardware in this dataset)
4. **Individual/device scope** — references a specific machine or peripheral rather than a system/service

Device noun alone is near-sufficient (e.g., "Printer not working" → 100% hardware). Generic failure phrases without a device noun (e.g., "not responding" in a software/network context) are much weaker signals.
