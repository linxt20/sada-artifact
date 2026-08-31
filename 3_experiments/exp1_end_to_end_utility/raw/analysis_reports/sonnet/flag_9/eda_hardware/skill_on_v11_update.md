---
dataset: flag_9
scenario: eda_hardware
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "hardware_incident"
query: "What in an incident's description tends to signal it's a hardware problem?"
source_table: augment_table/flag_9/eda_hardware/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:20:31.098417+00:00
wall_seconds: 44.05
---

# Hardware Incident Signal Analysis

**Dataset:** 600 incidents · Focus variable: `affected_system_domain` (hardware_device = 184 rows, ~31%)

---

## Key Signals in Incident Descriptions

### 1. `description_action_type` = `failure_malfunction` — Strongest single signal

| Action Type | Hardware Share | Non-Hardware Share |
|---|---|---|
| `failure_malfunction` | **71%** | 29% |
| `installation_request` | 0.6% | 99.4% |
| `connectivity_issue` | 4% | 96% |
| `access_recovery` | 3% | 97% |
| `configuration_assistance` | 43% | 57% |

> **94% of hardware incidents carry `failure_malfunction`** as their description action type. No other action type comes close. An incident description signaling a device that has stopped working, broken, or is not functioning is the overwhelmingly dominant pattern for hardware.

### 2. `software_keyword_present` = `False` — Perfect negative predictor

- **100%** of hardware-domain incidents have `software_keyword_present = False`.
- Conversely, ~60% of non-hardware incidents contain a software keyword.
- Any description mentioning software terms (install, update, application, etc.) is very unlikely to be a hardware problem.

### 3. Short Description Vocabulary

The most frequent hardware short descriptions reveal consistent natural-language patterns:

| Pattern | Examples |
|---|---|
| **Device + "not working/functioning"** | *"Printer not working properly"*, *"Mouse not working properly"* |
| **Device + malfunction** | *"Printer malfunctioning"*, *"Keyboard malfunction on workstation"* |
| **Display/physical symptoms** | *"Monitor display issue"*, *"Monitor screen is flickering"* |
| **Not responding** | *"Printer not responding"* |

Physical peripheral devices — **printers, monitors, keyboards, mice** — dominate. The descriptions are terse, device-named, and describe a physical failure state.

### 4. Category Alignment

- 182 of 184 hardware-domain incidents fall under the `Hardware` category; only 2 were routed to `Inquiry / Help`. This confirms strong internal consistency.

### 5. Priority Skew

Hardware incidents skew toward **2 - High** (79%) vs. 61% for non-hardware, and less often **3 - Moderate** (13% vs. 29%). Urgency language in descriptions likely reflects physical device outages affecting immediate productivity.

---

## Summary of Signals

| Signal | Direction | Strength |
|---|---|---|
| Description action type = `failure_malfunction` | ✅ Positive | Very strong (94% of HW incidents) |
| No software keyword in description | ✅ Positive | Perfect within dataset (100%) |
| Peripheral device name (printer, monitor, keyboard, mouse) | ✅ Positive | Strong (dominant in HW short descs) |
| Words: "not working", "not functioning", "malfunctioning", "not responding" | ✅ Positive | Strong |
| Description contains "install", "update", "software", "application" | ❌ Negative | Very strong exclusion signal |
| Action type = `connectivity_issue` or `access_recovery` | ❌ Negative | Strong (rarely hardware) |

---

## Exceptions & Caveats

- A small fraction of `configuration_assistance` incidents (43%) map to hardware, suggesting device setup/config requests can also be hardware-related — weak but non-negligible signal.
- `performance_degradation` is rarely hardware (8%), so slowness complaints alone are not reliable hardware signals.
- The dataset lacks raw free-text descriptions; signals above derive from engineered columns (`description_action_type`, `software_keyword_present`, `short_description`). Patterns are consistent but vocabulary coverage depends on those upstream labels.
