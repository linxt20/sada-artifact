---
dataset: flag_9
scenario: concept_attribute_hardware
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "hardware_hiccups"
query: "What kinds of hardware issues appear in these incidents?"
source_table: augment_table/flag_9/concept_attribute_hardware/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:22:10.353563+00:00
wall_seconds: 24.08
---

# Hardware Issues in Incidents

## Overview

Out of 600 total incidents, **182 (30.3%)** are flagged as hardware incidents (`is_hardware_incident = Yes`). These are captured in the `hardware_issue_type` column, which is `N/A` for all non-hardware incidents.

## Hardware Issue Types

| Hardware Issue Type | Count | % of Hardware Incidents |
|---|---|---|
| Printer | 83 | 45.6% |
| Monitor/Display | 28 | 15.4% |
| Keyboard | 24 | 13.2% |
| Power/Boot | 9 | 4.9% |
| Storage | 8 | 4.4% |
| General Hardware | 8 | 4.4% |
| Mouse | 7 | 3.8% |
| Fan/Cooling | 6 | 3.3% |
| Server Hardware | 6 | 3.3% |
| Graphics Card | 3 | 1.6% |

## Key Findings

1. **Printer issues dominate** — nearly half of all hardware incidents (83/182) relate to printers not working or malfunctioning. This is a disproportionately large share, suggesting either a systemic fleet issue or high printer usage in the organization.

2. **Peripheral failures are most common** — Printer, Monitor/Display, Keyboard, and Mouse together account for ~78% of hardware incidents. These are all user-facing peripherals rather than core compute infrastructure.

3. **Power/Boot and Storage issues** — 9 power/boot failures (e.g., "Desktop computer is not powering on", "Unable to boot laptop") and 8 storage incidents (e.g., "Hard drive failure") represent lower-frequency but potentially higher-severity problems.

4. **Cooling and Server Hardware** — Fan/Cooling (6) and Server Hardware (6) incidents are the least common, indicating infrastructure-level hardware problems are rare in this dataset.

5. **General Hardware** — 8 incidents are labelled `General Hardware`, suggesting some incidents could not be classified into a specific component type.

## Caveats

- The `hardware_issue_type` field appears to have been algorithmically assigned rather than manually entered, so individual misclassifications are possible.
- Priority for hardware incidents is predominantly **2 - High**, with some **3 - Moderate** cases; no hardware incidents appear at **1 - Critical** in the sampled rows, though this may not hold across the full dataset.
- Non-hardware incidents use `N/A` in `hardware_issue_type`, so the column cleanly separates the two populations.
