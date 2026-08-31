---
dataset: flag_9
scenario: concept_attribute_hardware
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "hardware_hiccups"
query: "What kinds of hardware issues appear in these incidents?"
source_table: augment_table/flag_9/concept_attribute_hardware/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:21:04.583305+00:00
wall_seconds: 79.47
---

# Hardware Issues in IT Service Incidents: Analysis Report

**Analysis Date:** 2026-07-30  
**Dataset:** Augmented table with TAPP-generated semantic columns  
**Query:** What kinds of hardware issues appear in these incidents?

## Executive Summary

Hardware incidents represent **182 out of 600 total incidents (30.3%)** in the dataset. The analysis reveals a diverse portfolio of hardware failure modes affecting different device categories and scopes, with predominantly high-priority issues (79.7% rated 2-High) and intermittent or degraded performance as the dominant impact pattern.

## Methodology

**TAPP-Generated Columns Used in Analysis:**
- `failure_mode`: Semantic classification of hardware malfunction types (e.g., not_functioning, malfunction, power_issue, display_issue)
- `affected_scope`: Infrastructure layer affected—individual_workstation, office_shared_resource, or department_server
- `severity_indicator`: Outcome classification indicating incident impact (intermittent_failure, degraded_performance, critical_outage)

These augmented columns provide 100% coverage across all 182 hardware incidents and add explicit semantic structure beyond category labels, enabling systematic categorization of root cause patterns and operational impact.

---

## Key Hardware Issue Categories

### 1. Failure Mode Breakdown (failure_mode column)

Hardware incidents cluster into eight distinct failure patterns:

| Failure Mode | Count | % of Hardware | Typical Devices |
|---|---|---|---|
| **Not Functioning** | 59 | 32.4% | Printers (46), Keyboards (5) |
| **Malfunction** | 48 | 26.4% | Printers (22), Server hardware (9), Keyboards (8) |
| **Not Responding** | 21 | 11.5% | Printers (10), Keyboards (7) |
| **Display Issue** | 20 | 11.0% | Monitors (20) |
| **Power Issue** | 18 | 9.9% | Desktops/Laptops (15), Monitors (2) |
| **Physical Damage** | 10 | 5.5% | Hard drives (4), Server hardware (3), Graphics cards (2) |
| **Connectivity** | 5 | 2.7% | Printers (4), Monitors (1) |
| **Performance Degradation** | 1 | 0.5% | CPU thermal (1) |

**Key Observation:** Not functioning and malfunction account for 58.8% of all hardware incidents, primarily affecting output devices (printers, keyboards) and system-critical peripherals.

### 2. Hardware Devices Most Impacted

**By frequency (inferred from incident descriptions):**

- **Printers** (81 incidents, 44.5%): Dominant issue type; 46 not functioning, 22 malfunctions, 10 not responding
- **Monitor/Display** (27 incidents, 14.8%): Primarily display issues (20 incidents); 7 others with power/connectivity concerns
- **Keyboard** (24 incidents, 13.2%): Mix of not responding (7), not functioning (5), malfunction (8), key sticking
- **Desktop/Computer** (23 incidents, 12.6%): Power issues (17), display issues (4), malfunction (2)
- **Server Hardware** (12 incidents, 6.6%): Malfunction (9), physical damage (2), connectivity (1)
- **Hard Drive/Storage** (8 incidents, 4.4%): All 8 classified as physical_damage; direct correlation with critical outages
- **Laptop** (7 incidents, 3.8%): Power issues (5), display (2)
- **Mouse** (7 incidents, 3.8%): Primarily not functioning
- **Fan/Thermal** (4 incidents, 2.2%): Malfunction (3), performance degradation (1)
- **Graphics Card** (3 incidents, 1.6%): Physical damage (3)

### 3. Scope and Organizational Impact

Hardware incidents affect three distinct infrastructure layers:

| Affected Scope | Count | % | Critical Rate | Dominant Failure Mode |
|---|---|---|---|---|
| **Individual Workstation** | 88 | 48.4% | 12.5% | Display issue (20), Malfunction (17), Power issue (17) |
| **Office Shared Resource** | 83 | 45.6% | 1.2% | Not functioning (46), Malfunction (22), Not responding (10) |
| **Department Server** | 11 | 6.0% | 36.4% | Malfunction (9), Physical damage (2) |

**Key Insight:** Department server hardware, despite fewer incidents (11 total), exhibits the highest critical priority rate (36.4%). Individual workstations show balanced failure mode distribution. Shared office resources (mostly printers) have high incident volume but low severity.

### 4. Severity and Impact Assessment

**Severity Indicators (severity_indicator column):**

- **Intermittent Failure** (114 incidents, 62.6%): Periodic rather than complete breakdowns
  - Most common failure modes: Not functioning (46), Malfunction (32), Not responding (10)
  - Critical priority rate: 6.1%
  - Typical devices: Printers, keyboards, displays

- **Degraded Performance** (41 incidents, 22.5%): Reduced functionality or partial operation
  - Dominated by display issues (12 incidents; flickering, dead pixels, reduced output)
  - Critical priority rate: 2.4%
  - Secondary pattern: Malfunction affecting performance (8 incidents)

- **Critical Outage** (25 incidents, 13.7%): Complete system/device unavailability
  - Malfunction is the primary failure mode (13 incidents, 52%)
  - Power issues account for 28% (7 incidents)
  - Physical damage: 3 incidents (12%)
  - Critical priority rate: 32.0% (8 of 25 classified as 1-Critical)
  - High concentration in individual workstations (68%) and department servers (28%)

### 5. Priority Distribution

| Priority | Count | % | Severity Indicator Profile |
|---|---|---|---|
| **1 - Critical** | 16 | 8.8% | Malfunction (5), Power issue (4), Physical damage (3), Not functioning (3) |
| **2 - High** | 145 | 79.7% | Intermittent failure (98), Degraded performance (35), Critical outage (12) |
| **3 - Moderate** | 21 | 11.5% | Intermittent failure (16), Degraded performance (5) |

**Observation:** Critical hardware incidents concentrate in power-related and malfunction failure modes, affecting individual workstations (11/16) and department servers (4/16).

### 6. Critical Hardware Issue Patterns

#### Printers (81 incidents, 44.5% of all hardware)
- **Issue profile:** Primarily not functioning (56.8%) or malfunctioning (27.2%)
- **Impact:** Intermittent failure dominates (78.0%); low escalation to critical (1.2%)
- **Scope:** All classified as office_shared_resource, limiting individual user impact
- **Exemplar issues:** "Printer not working properly," "Printer malfunction," "Printer not responding"

#### Power and Startup Issues (15 incidents, 8.2%)
- **Root causes:** System won't power on, boot failures, monitor not displaying, laptop unable to start
- **Impact:** 20% critical priority rate; mixed severity indicators (intermittent failure 73.3%, critical outage 26.7%)
- **Affected devices:** Desktops (9), Monitors (2), Laptops (3)
- **Risk level:** Higher escalation pathway than printer issues

#### Server Hardware Malfunction (14 incidents, 7.7%)
- **Issue types:** Server malfunction (9), CPU/thermal issues (3), graphics card damage (2)
- **Impact:** 35.7% critical priority rate; 50% result in critical outages
- **Scope:** Mix of individual workstations and department servers
- **Severity indicators:** 57.1% critical outage; 42.9% degraded performance
- **Exemplar issues:** "Faulty server hardware needs replacement," "CPU overheating causing system shutdown," "Graphics Card of Workstation issue"

#### Storage Failures (8 incidents, 4.4%)
- **Classification:** All marked as physical_damage in failure_mode column
- **Impact:** 12.5% critical rate; 62.5% result in critical outages
- **Devices:** Hard drive failures (4), general storage issues (4)
- **High correlation with operational disruption**

#### Display/Monitor Issues (27 incidents, 14.8%)
- **Failure modes:** Display issue dominant (74.1%); others are power-related or malfunction
- **Impact:** 81.5% degraded performance; only 7.4% critical priority
- **Exemplar issues:** "Monitor not turning on," "Monitor screen flickering," "Monitor displaying no visual output," "Dead pixels on display"

#### Keyboard and Input Device Issues (24 incidents, 13.2%)
- **Failure modes:** Mixed—not responding (29.2%), malfunction (33.3%), not functioning (20.8%)
- **Impact:** 79.2% intermittent failure; 8.3% critical priority
- **Exemplar issues:** "Keyboard keys sticking," "Keys not functioning," "Keyboard not working on office PC"

---

## Relationships Between TAPP Columns and Incident Drivers

### Failure Mode vs. Affected Scope

The failure_mode and affected_scope columns reveal distinct risk patterns:

- **Individual Workstations:** Exhibit the broadest failure mode distribution (display_issue, malfunction, power_issue, malfunction)—reflecting device diversity on desktops. Power issues and display problems are workstation-specific.
- **Office Shared Resources (Printers):** Converge on not_functioning and malfunction; structural reliability issues in shared infrastructure.
- **Department Servers:** Concentrated in malfunction (81.8%) and physical_damage (18.2%); fewer but higher-stakes failure types.

### Failure Mode vs. Severity Indicator

- **Intermittent Failure:** Associated with not_functioning (40.4%), malfunction (28.1%), not_responding (8.8%). Devices operate periodically but unreliably.
- **Degraded Performance:** Dominated by display_issue (29.3%) and malfunction (19.5%). Partial or reduced functionality is the outcome.
- **Critical Outage:** Strongly linked to malfunction (52.0%) and power_issue (28.0%). Complete loss of device availability.

### Affected Scope vs. Priority

- **Department Servers:** 36.4% critical priority (4 of 11); concentrated in malfunction category
- **Individual Workstations:** 12.5% critical priority (11 of 88); spread across malfunction, power_issue, and physical_damage
- **Office Shared Resources:** 1.2% critical priority (1 of 83); lower escalation despite high incident volume

---

## Summary Findings

1. **Volume and Scope:** Hardware incidents (182, 30.3% of dataset) predominantly affect printers (44.5%) and individual workstations (48.4%).

2. **Primary Failure Modes:** "Not functioning" (32.4%) and "malfunction" (26.4%) dominate, accounting for 58.8% of all hardware incidents.

3. **Severity Distribution:** 62.6% intermittent, 22.5% degraded performance, 13.7% critical outage. Critical outages correlate strongly with malfunction (52%) and power issues (28%).

4. **Risk Stratification:**
   - **High risk:** Server hardware (36.4% critical rate), power/boot issues (20% critical rate), storage failures (62.5% critical outage rate)
   - **Medium risk:** Keyboard/input devices (8.3% critical rate), workstation display issues (7.4% critical rate)
   - **Low risk:** Shared office printers (1.2% critical rate), despite representing nearly half of hardware incidents

5. **TAPP Column Value:** The three augmented columns (failure_mode, affected_scope, severity_indicator) provide complete semantic coverage (100%) and clarify root cause patterns (e.g., power_issue strongly predicts critical outages) and organizational impact (server incidents far more critical than printer incidents).
