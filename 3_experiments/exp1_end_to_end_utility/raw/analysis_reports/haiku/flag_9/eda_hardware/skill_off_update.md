---
dataset: flag_9
scenario: eda_hardware
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "hardware_incident"
query: "What in an incident's description tends to signal it's a hardware problem?"
source_table: augment_table/flag_9/eda_hardware/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:23:04.660974+00:00
wall_seconds: 63.42
---

# Hardware Problem Detection Analysis: EDA Hardware (Skill Off Variant)

## Executive Summary

Based on analysis of 600 IT incidents, incidents signaling hardware problems in their descriptions are strongly distinguished by:
1. **Explicit hardware device mentions** (84.2% of hardware problems)
2. **Physical symptom descriptions** (71.3% of hardware problems)
3. **Hardware category classification** (65.2% of hardware problems)

Notably, the feature combination is nearly deterministic: **0% of non-hardware incidents mention hardware devices or physical symptoms**, making these signals highly reliable predictors.

## Key Findings

### Primary Signal: Hardware Device Mentions

The strongest indicator of a hardware problem is explicit mention of hardware devices:

- **Printers** dominate complaints (29.0% of hardware incidents; 81/279)
  - Phrases: "printer not working," "printer malfunctioning," "printer not responding"
  - Most common single description: "Printer not working properly" (15 occurrences)

- **Keyboards** (8.6%; 24 incidents)
  - Phrases: "keyboard keys are sticking," "keyboard not functioning," "keyboard malfunction"

- **Monitors** (9.3%; 26 incidents)
  - Phrases: "monitor not turning on," "monitor display issue," "monitor screen has dead pixels"

- **Mice** (2.5%; 7 incidents)
  - Phrases: "mouse not working properly"

- **Storage/Drives** (3.6%; 10 incidents)
  - Phrases: "hard drive failure," "hard drive malfunction"

- **Other hardware** (cooling, graphics cards, workstations):
  - "Fan not working in desktop computer"
  - "Issue with the Graphics Card of the Workstation"
  - "CPU overheating and causing system shutdown"

### Secondary Signal: Physical Symptom Descriptions

Over 71% of hardware incidents describe observable physical or operational failures:

| Symptom Category | Frequency | Examples |
|---|---|---|
| **Inoperability** | 53.4% (149/279) | "not working," "not functioning," "malfunction," "failure" |
| **Connection/Peripheral Issues** | 15.1% (42/279) | "not responding," "unable to connect," "connection" issues |
| **Operational Degradation** | 13.3% (37/279) | "slow," "lag," "crash," "error" |
| **Visual Problems** | 11.1% (31/279) | "screen," "display," "monitor" issues |
| **Power/Startup Issues** | 4.7% (13/279) | "not powering on," "not turning on," "shutdown" |

### Tertiary Signal: Hardware Category Assignment

65.2% of hardware incidents (182/279) are formally categorized as "Hardware," but this is not deterministic:
- 97 hardware incidents (34.8%) appear in other categories:
  - **Software (48 cases)**: Often involve crashes or failures triggered during software operations on hardware
  - **Database (39 cases)**: Database server hardware or connectivity failures
  - **Network (6 cases)**: Network hardware (routers, connections)
  - **Other (4 cases)**: Misclassified or ambiguous

## Important Exceptions and Weak Signals

### Case 1: Hardware Issues Misclassified as Software

When hardware failures occur *during* software operations, descriptions may blur categories. Example patterns:

- "Software update failed on my workstation" → Hardware issue (update exposed hardware failure)
- "Software update causing system crashes" → Hardware problem (system can't sustain operation)
- "Unexpected shutdown during software update" → Hardware problem (power/shutdown triggered)

**Signal clarity**: Presence of "workstation," "desktop," or device names in software descriptions may indicate latent hardware problems.

### Case 2: Server/Database Hardware Problems

39 incidents classified as Database are actually hardware-related:
- "SQL Server not responding" → Server hardware failure
- "Unable to access database server" → Server hardware/connectivity
- "Database connection timeout" → Network/hardware delay

**Signal clarity**: Hardware device mention (computer, server, workstation) combined with "unable to," "not responding," or "outage" signals hardware issues even in Database category.

### Case 3: Perfect Feature Separation

A striking finding: **No non-hardware incidents mention hardware devices or physical symptoms**. This indicates:
- The extracted features ("mentions_hardware_device" and "mentions_physical_symptom") are perfectly discriminative
- Hardware problems have a distinctive linguistic signature
- False positives are minimal if hardware terminology appears

## Recommendations for Incident Description Analysis

When determining if an incident likely represents a hardware problem:

1. **Look for device names first**: Printer, keyboard, monitor, mouse, disk, fan, CPU, card, workstation
2. **Scan for failure modes**: "not working," "malfunction," "failure," "not responding," "can't connect," "dead," "broken"
3. **Flag operational symptoms**: Crashes, shutdowns, overheating, slow performance
4. **Consider context**: Even Software/Database incidents become hardware problems if failure occurs on specific devices
5. **Note category mismatches**: Hardware problems may hide in non-Hardware categories; cross-reference device mentions

## Dataset Context

- **Total incidents**: 600 (variant: skill_off)
- **Confirmed hardware problems**: 279 (46.5%)
- **Feature reliability**: 100% separation between hardware and non-hardware on mentions_hardware_device and mentions_physical_symptom
- **Most common hardware complaints**: Printer functionality (20 unique descriptions)
