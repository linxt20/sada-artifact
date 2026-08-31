---
dataset: flag_9
scenario: eda_hardware
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "hardware_incident"
query: "What in an incident's description tends to signal it's a hardware problem?"
source_table: augment_table/flag_9/eda_hardware/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:23:09.645369+00:00
wall_seconds: 59.29
---

# Hardware Signal Analysis in Incident Descriptions

## Dataset Overview

- **Total incidents:** 600
- **Hardware-flagged (`hw_signal_flag = 1`):** 201 (33.5%)
- **Hardware category incidents:** 182; of these, 179 (98.4%) were correctly flagged

The dataset includes engineered columns—`hw_device_mentions`, `hw_symptom_signals`, and `hw_signal_score`—that capture the signals the query asks about.

---

## Key Signals in Hardware Incident Descriptions

### 1. Device Name Mentions (`hw_device_mentions`)

The single strongest predictor of a hardware incident is an explicit mention of a physical device in the short description:

| Device | Flagged Incidents |
|---|---|
| printer | 79 |
| monitor | 24 |
| server | 17 |
| keyboard | 15 |
| desktop | 15 |
| mouse | 7 |
| laptop | 6 |
| hard drive | 5 |

Terms like **"printer," "monitor," "keyboard," "desktop," "laptop," and "mouse"** appear exclusively in hardware-flagged incidents (ratio ≫ 10×). The word **"server"** is an exception—it appears in both hardware and non-hardware incidents (e.g., "SQL server"), making it a weak standalone signal.

### 2. Symptom Language (`hw_symptom_signals`)

Hardware descriptions consistently use symptom vocabulary that implies a physical failure state rather than a configuration or software issue:

| Symptom Signal | Count |
|---|---|
| not_working | 89 |
| malfunction | 41 |
| failure | 19 |
| physical_symptom | 11 |
| unable_to_boot | 2 |

Concretely, phrases such as **"not working properly," "not responding," "malfunctioning," "failure," "not turning on,"** and **"keys are sticking"** dominate hardware descriptions. High-ratio words vs. non-hardware: *"printer"* (81×), *"monitor"* (26×), *"keyboard"* (24×), *"properly"* (11.5×), *"functioning"* (12×), *"not"* (8.9×).

### 3. Signal Score (`hw_signal_score`)

Hardware-flagged incidents have a mean score of **~3.0** (range 2–5); non-flagged incidents score near **0**. A score ≥ 2 reliably separates the two groups, indicating the score aggregates device + symptom co-occurrence.

---

## Pattern Summary

A description is likely a hardware problem when it combines:
1. **A physical device noun** (printer, monitor, keyboard, desktop, laptop, mouse, hard drive, fan)
2. **A failure/symptom verb or adjective** (not working, not responding, malfunctioning, failure, not turning on, not powering on, sticking, crashing)

Example patterns seen in data:
- *"Printer not working properly"*
- *"Monitor not turning on"*
- *"Hard drive failure in office desktop machine"*
- *"Keyboard keys are sticking"*
- *"Desktop PC is not turning on"*

---

## Exceptions and Weak Evidence

- **"Server"** is ambiguous: it appears in hardware incidents (*"server fan not working"*) but also non-hardware ones (*"SQL server not responding," "database server not responding"*). Alone it is insufficient.
- **22 false positives** were flagged (hw_signal_flag = 1, category ≠ Hardware): these include descriptions mentioning hardware device words in a software context (e.g., *"Software update failed on my workstation," "Issue with installed software on my desktop"*). The word **"workstation"** or **"desktop"** in a software-failure context can trigger a false flag.
- **3 hardware incidents were missed** by the flag (e.g., *"Unable to start the company issued PC," "Printing machine malfunctioning"*)—suggesting synonyms like "PC" or "printing machine" may not always be caught.

---

## Decision-Ready Summary

> **To identify a hardware incident from its description: look for a concrete physical device name (printer, monitor, keyboard, desktop, laptop, mouse, hard drive) combined with failure/malfunction language (not working, not responding, not turning on, malfunctioning, failure). This combination achieves ~98% recall on the Hardware category. Descriptions mentioning only "server" or only vague terms like "not working" without a device name are weaker signals and require additional context.**
