---
dataset: flag_2
scenario: concept_attribute_delay
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: faceted_decomposition
focus_variable: "incident_delay_reasons"
query: "Why do some incidents take longer to resolve?"
source_table: augment_table/flag_2/concept_attribute_delay/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_2__concept_attribute_delay/analyses/original/analysis.md
wall_seconds: 76.14
---

# Analysis: Why do some incidents take longer to resolve

## What was measured
Resolution time was computed from **`opened_at`** to **`closed_at`** for incidents with a recorded closure. That covers **372 of 500** incidents; the remaining **128** are still **`New`** or **`In Progress`** and cannot be timed to completion yet.

## Decision-ready answer

### 1. The strongest driver is **when the incident was opened**
The dominant pattern is temporal, not operational.

- Overall completed-incident resolution time:
  - **Mean:** **1043.4 hours** ($\approx 43.5$ days)
  - **Median:** **1032.0 hours** ($\approx 43.0$ days)
  - **75th percentile:** **1557.6 hours** ($\approx 64.9$ days)
  - **95th percentile:** **2047.2 hours** ($\approx 85.3$ days)

- By **`opened_at` month**, mean resolution time rises almost monotonically:
  - **2023-01:** **141.3 h**
  - **2023-04:** **765.4 h**
  - **2023-07:** **1425.7 h**
  - **2023-10:** **2096.6 h**

This is the clearest pattern in the table. Later-opened incidents take much longer on average than earlier-opened ones. In this dataset, the opening date is almost perfectly aligned with the final duration, which strongly suggests a **calendar/backlog or data-generation effect** is driving most of the delay variation.

### 2. Ticket type matters somewhat, but much less than timing
There are smaller differences by **`category`** and **`assignment_group`**:

- By **`category`** mean resolution time:
  - **Hardware:** **1105.2 h**
  - **Network:** **1078.7 h**
  - **Software:** **1050.6 h**
  - **Database:** **955.0 h**
  - **Inquiry / Help:** **957.9 h**

- By **`assignment_group`** mean resolution time:
  - **Service Desk:** **1102.4 h**
  - **Network:** **1074.0 h**
  - **Software:** **1028.3 h**
  - **Database:** **946.5 h**

This indicates that **Network-, Hardware-, and Service Desk-related work** tends to run longer than **Database** work, but the spread is modest relative to the month effect. For example, the gap between **Hardware** and **Database** is about **150 hours** ($\approx 6.3$ days), far smaller than the roughly **1955-hour** gap between January and October openings.

### 3. Priority does **not** explain long resolution well
If higher urgency were the main cause, **`priority`** would separate clearly. It does not.

- **3 - Moderate:** **1120.7 h**
- **1 - Critical:** **1118.7 h**
- **2 - High:** **1019.5 h**

Critical incidents are **not** materially faster or slower than moderate ones, and both are only about **100 hours** slower than high-priority incidents. That is a weak signal.

### 4. Specific owners show differences, but evidence is weak
There are visible differences by **`assigned_to`** and **`closed_by`**:

- By **`assigned_to`** mean resolution time:
  - **Beth Anglin:** **1141.9 h**
  - **Fred Luddy:** **1125.4 h**
  - **Charlie Whitherspoon:** **1035.5 h**
  - **Luke Wilson:** **967.5 h**
  - **Howard Johnson:** **952.8 h**

- By **`closed_by`** mean resolution time:
  - **Charlie Whitherspoon:** **1115.8 h**
  - **Luke Wilson:** **1079.2 h**
  - **Fred Luddy:** **1054.0 h**
  - **Beth Anglin:** **999.4 h**
  - **Howard Johnson:** **949.6 h**

However, this should **not** be over-read. The dataset does not show workload, queue age, escalation reason, or incident complexity, so these differences may reflect **case mix** rather than individual performance.

### 5. Hand-offs are not the reason
A simple hand-off check using **`assigned_to` != `closed_by`** does not support the idea that reassignment is causing the longest delays.

- **Same person assigned and closed:** **1054.7 h**
- **Different person closed:** **1040.6 h**

That difference is negligible.

## Important exceptions and caveats

- The **longest incidents** are often **Network/Software** issues, with recurring descriptions such as **VPN**, **email**, and **network drive** access problems. But those areas also have the largest ticket volumes, so this is only suggestive.
- **128 incidents are still open** (**`New`** or **`In Progress`**). Their final durations are unknown, so the true upper tail of delay may be worse than the completed-case analysis shows.
- The near-perfect link between **opening date** and **resolution time** is unusual for real operations data. It likely means the main explanation here is **dataset structure or aging logic**, not purely process differences across teams.

## Bottom line
Some incidents take longer to resolve in this dataset **primarily because they were opened later in the observed period**. Category, assignment group, and owner show **secondary** differences, with **Network/Hardware/Service Desk** work tending to run longer than **Database** work, but these effects are much smaller than the time-based pattern. Before making staffing or process decisions, the first check should be whether the dataset embeds a **systematic time-delay artifact or backlog effect**.
