---
dataset: flag_9
scenario: eda_hardware
variant: original
model: substrate-claude-haiku-4-5
query_subtype: exploratory_data_analysis
focus_variable: "hardware_incident"
query: "What in an incident's description tends to signal it's a hardware problem?"
source_table: augment_table/flag_9/eda_hardware/original.csv
generated_at: 2026-07-26T13:44:16.067871+00:00
wall_seconds: 77.17
---

# Signals of Hardware Problems in Incident Descriptions

## Executive Summary

Incident descriptions with specific hardware device names and functional failure language strongly signal hardware problems. The dataset contains 182 hardware incidents (30% of 600 total) with highly distinctive linguistic patterns that differentiate them from software, database, network, and general inquiry issues.

## Key Linguistic Signals

### 1. **Device-Specific Terminology (Strongest Indicators)**

Hardware incidents contain explicit device names that virtually never appear in other incident categories:

| Device/Component | Hardware % | Non-Hardware % | Ratio |
|---|---|---|---|
| Printer mentions | 44.5% | 0.0% | 445× |
| Monitor/Screen | 14.3% | 0.0% | 143× |
| Keyboard | 13.2% | 0.0% | 132× |
| Hard drive | 4.4% | 0.5% | 44× |
| Desktop computer | 9.9% | 0.7% | 12× |

The presence of these concrete device terms is the strongest predictor. Over 60% of hardware descriptions mention at least one specific device (printer, keyboard, monitor, desktop, laptop, fan, or mouse).

### 2. **Functional Failure Verbs (Second Strongest Signal)**

Hardware problems describe *physical malfunction* rather than configuration or access issues:

| Failure Pattern | Hardware % | Non-Hardware % |
|---|---|---|
| "Not working" / "not functioning" | 40.1% | 3.1% |
| "Malfunctioning" / "malfunction" | 20.9% | 1.4% |
| "Not turning on" / "powering on" | 5.5% | 0.0% |
| "Failure" / "failed" | 6.0% | 3.6% |

Hardware descriptions focus on whether equipment operates ("not working," "not functioning," "malfunctioning") rather than whether someone can access or use it ("unable to," "cannot," "install"). 40% of hardware incidents use the "not working/functioning" pattern vs. only 3% of non-hardware incidents.

### 3. **Absence of Software/Access Keywords**

Non-hardware incidents overwhelmingly reference:
- "Software" (46.7% vs. 0.2% in hardware)
- "Installation/install" (21.3% vs. 3.3% in hardware)
- "Unable/cannot/cannot" (28.2% vs. 3.8% in hardware)
- "Database" (17.2% vs. 0% in hardware)
- "Connection/connect" (15.1% vs. 3.8% in hardware)

The absence of these terms is a weak but supportive signal that an incident is hardware-related.

## Concrete Description Examples

**Hardware descriptions typically follow these patterns:**
- "Printer not working properly"
- "Desktop computer is not powering on"
- "Keyboard keys not functioning"
- "Monitor not turning on"
- "Hard drive failure in office desktop machine"
- "Fan not working in desktop computer"
- "Server hardware overheating issue"

**Non-hardware descriptions follow different patterns:**
- "Unable to install new software update" (software)
- "Unable to establish connection to database" (database)
- "Unable to connect to VPN" (network)
- "Need assistance with software installation" (inquiry/help)

## Decision Guidance

**Strong hardware indicators (high confidence):**
- Explicit device mentions (printer, keyboard, monitor, laptop, hard drive, fan, server hardware)
- Functional failure verbs: "not working," "not functioning," "malfunctioning," "not turning on," "won't power"
- Combined description pattern: [device name] + [failure verb] (e.g., "Monitor not turning on")

**Weak or absent indicators:**
- Software terminology (installation, updates, bugs, crashes)
- Connectivity terminology (unable to connect, VPN, internet)
- Access terminology (unable to access, establish connection)
- Generic help requests ("need assistance," "need help")

**Important caveat:**
Some incidents mention physical devices in non-hardware contexts (e.g., "server" appears in 6.6% of hardware but 9.1% of non-hardware incidents, often referring to database or application servers). Context matters: "server hardware overheating" is hardware; "unable to establish connection to SQL server" is database-related.

---
*Analysis based on 600 IT incidents: 182 hardware (30%), 130 software (22%), 102 database (17%), 78 network (13%), 108 inquiry/help (18%)*
