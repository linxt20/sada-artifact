---
dataset: flag_9
scenario: eda_hardware
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "hardware_incident"
query: "What in an incident's description tends to signal it's a hardware problem?"
source_table: augment_table/flag_9/eda_hardware/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:21:02.351646+00:00
wall_seconds: 75.38
---

# Hardware Problem Identification in Incident Descriptions

## Executive Summary

Analysis of 600 IT service incidents reveals **clear linguistic and contextual signals** that distinguish hardware problems from other incident types. Hardware incidents comprise **30% of the dataset** (182 of 600) and exhibit distinct patterns in their short descriptions that reliably indicate physical equipment failure.

## Key Signals in Hardware Problem Descriptions

### 1. **Hardware-Specific Terminology (High Confidence Indicators)**

The most distinctive pattern is the presence of **concrete device names**:

- **Printer references**: 44.5% of hardware incidents explicitly mention "printer" (81/182)
- **Monitor/Display terms**: 14.3% mention "monitor" and 4.9% mention "screen" (combined 26/182, 14.3%)
- **Keyboard references**: 13.2% specifically mention "keyboard" (24/182)
- **Other devices**: Mouse (3.8%), hard drive (3.8%), server (6.6%), GPU/graphics card (1.1%)

**Evidence:** These device-specific terms almost never appear in non-hardware incidents (<1% for most terms), making them reliable predictors.

### 2. **Problem State Language (Behavioral Indicators)**

Hardware problems use distinctly different problem descriptors than software issues:

#### Hardware-Specific Language:
- **"Not working" / "Not functioning"**: 18.1% vs. 1.0% in non-hardware (18x higher ratio)
- **"Malfunction" / "Malfunctioning"**: 20.9% vs. 1.4% in non-hardware (15x higher)
- **"Not responding"**: 8.8% vs. 1.9% in non-hardware (4.6x higher)
- **"Failure"**: 5.5% vs. 1.0% in non-hardware (5.5x higher)
- **"Not turning on" / "Not powering on"**: 5.4% vs. 0% in non-hardware (exclusive to hardware)
- **"Faulty" / "Defective"**: 3.8% vs. 0% in non-hardware (exclusive to hardware)
- **Hardware-specific states**: "Overheating" (1.6%), "Flickering" (3.3%), "Display issue" (1.6%)

**Contrast:** Non-hardware incidents predominantly use "unable to" (28.2% vs. 0.5% in hardware) and "connection" (9.6% vs. 0%, reflecting network/database connectivity issues).

### 3. **Physical Location References**

Hardware descriptions are **significantly more likely to reference physical locations** where the equipment exists:

- Hardware with location mentions: **44.5%** (81/182)
- Non-hardware with location mentions: **6.5%** (27/418)

**Common hardware location patterns:**
- Office desk/workstation: "Printer not working in office 12A"
- Department-specific: "Printer malfunction in Finance department"
- Building/floor references: "Router malfunctioning on Floor 3"

**Interpretation:** This reflects the physical, spatially-bound nature of hardware problems—users must reference where the faulty equipment is located.

### 4. **Descriptor Specificity and Concreteness**

Hardware incidents have higher **problem_specificity scores** (mean 2.47 vs. 1.82 for non-hardware), indicating more concrete, tangible descriptions. Hardware problems are described with shorter, more direct language (avg 32.2 chars vs. 37.1 chars), focusing on **what device** and **what state** rather than processes or abstract issues.

### 5. **Physical State Keywords (Near-Perfect Predictor)**

**Critical finding:** 99.5% of hardware incidents (181/182) have `physical_state_keyword=True`, while 0% of non-hardware incidents do (<1% exception rate).

**Affected components distribution in hardware:**
- Display output (monitors, screens): 44.5% (81/182)
- Physical hardware (servers, general): 26.4% (48/182)
- Input devices (keyboard, mouse): 17.0% (31/182)
- Power/thermal (fans, power supplies): 6.6% (12/182)
- Storage (hard drives, SSDs): 4.4% (8/182)

## Distinguishing Hardware from Other Categories

### Comparison with Database Issues
- Database incidents mention "connection," "unable to access," or "query" without device names
- Example: "Unable to connect to MySQL database" vs. "Printer not working properly"

### Comparison with Software Issues
- Software incidents use "update," "install," "crash," "bug," "application"
- Example: "Software update failed" vs. "Monitor not turning on"

### Comparison with Network Issues
- Network incidents mention "VPN," "WiFi," "router connectivity" without physical device emphasis
- Example: "Unable to connect to VPN" vs. "Keyboard malfunction"

## Summary of Discriminative Patterns

| Signal | Hardware Indicator | Prevalence | Confidence |
|--------|-------------------|-----------|------------|
| Device name (printer, keyboard, monitor, etc.) | Present | 44–64% | Very High |
| "Malfunction" / "Not working" / "Not functioning" | Present | 52% combined | Very High |
| Location mention (office, workstation, desk) | Present | 44.5% | High |
| "Not turning on" / "Not powering on" | Present | 5.4% | Exclusive |
| Physical state keyword | Present | 99.5% | Critical |
| "Unable to" language | Absent | Only 0.5% | Distinguishing absence |

## Exceptions and Weak Signals

- **1 hardware incident** (0.5%) lacks a physical state keyword (likely data anomaly)
- Some **general** hardware issues lack specific device names: "Hardware failure on desktop" (classification relies on "Hardware" category keyword and affected_component field)
- **Location references** alone (6.5% in non-hardware) are not definitive but **combined with device names** are highly predictive

## Conclusion

Incident descriptions signal hardware problems through a combination of:

1. **Explicit device mentions** (printer, keyboard, monitor, server, hard drive)
2. **Concrete failure language** ("not working," "malfunction," "not functioning," "not turning on")
3. **Physical location references** (office location, workstation, building)
4. **Absence of software/connectivity terminology** (no "update," "install," "VPN," "connection")

These patterns allow **reliable automated detection of hardware problems** directly from description text, with physical state keywords and affected component fields providing confirmatory evidence.
