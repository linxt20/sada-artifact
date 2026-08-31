---
dataset: flag_6
scenario: concept_attribute_workload
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "agent_workload_burden"
query: "What kinds of tickets create heavier agent workload?"
source_table: augment_table/flag_6/concept_attribute_workload/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:20:40.349142+00:00
wall_seconds: 40.73
---

# Analysis Report: Ticket Types Creating Heavier Agent Workload

## Overview
This report examines which types of IT support tickets create heavier agent workload. The analysis is based on 500 tickets with workload intensity scores (range: -3.46 to 9.0, mean: 4.02).

---

## Key Finding: Database and Network Tickets Drive Highest Workload

### Primary Drivers of Heavy Workload

**Database-related tickets** dominate the high-workload category:
- **Mean workload intensity: 4.68** (highest among all categories)
- **39.4%** of database tickets fall into the high workload segment (≥5.21)
- **Count: 109 tickets** representing the highest impact category

**Network-related tickets** are the second major contributor:
- **Mean workload intensity: 3.99**
- **23.2%** in high workload segment
- **Count: 284 tickets** (most frequent overall, but lower average intensity)

### Quantitative Evidence

| Category | Mean Workload | High Workload % | Count | Examples |
|----------|---------------|-----------------|-------|----------|
| **Database** | **4.68** | **39.4%** | 109 | Database access failures, server downtime, connection errors |
| **Network** | **3.99** | **23.2%** | 284 | VPN connectivity, email server outage, internet disconnections |
| **Software** | **3.69** | **20.8%** | 72 | Email sync issues, application crashes |
| **Hardware** | **2.99** | **7.7%** | 26 | Printer malfunction, display issues |

---

## Specific Ticket Characteristics Associated with Heavy Workload

### Issue Type
High-workload tickets concentrate in:
- **Database access/connectivity failures (28.6%)** – unable to access database, SQL server issues
- **Email and email server problems (42.1%)** – email outage, email server down, sync failures
- **Network connectivity problems (22.2%)** – VPN failures, internet disconnections
- **Service outages (13.5%)** – system-wide service unavailability

### Priority Level
- **Critical (1 - Critical):** Mean workload **4.69** (highest priority tier)
- **High (2 - High):** Mean workload **3.95**
- **Moderate (3 - Moderate):** Mean workload **3.11**
- Critical tickets generate 50% higher workload than moderate tickets

### Critical Infrastructure Status
- **Critical infrastructure YES:** Mean workload **4.18**
- **Critical infrastructure NO:** Mean workload **3.45**
- Tickets affecting critical infrastructure carry **21% higher average workload** intensity

### Resolution Time Correlation
- **Strong positive correlation (0.684)** between resolution time and workload intensity
- High-workload tickets require significantly longer to resolve:
  - Long-resolution tickets (>75th percentile) average **6.02 workload intensity**
  - Suggests both complexity and agent effort accumulation

---

## Top Workload-Driving Scenarios

The highest-workload tickets (9.0 intensity) involve:
1. **"Database server response time high"** – 59.6 days resolution
2. **"Unable to access company database"** – 23.8 days resolution
3. **"Email system failure"** – 23.2 days resolution

Extended resolution times (20+ days) consistently appear with workload scores ≥7.5, indicating systemic service disruptions requiring sustained agent effort.

---

## Summary: Ticket Types Creating Heaviest Agent Workload

1. **Database access and connectivity issues** (39.4% high workload)
2. **Email and messaging system failures** (42.1% of high-workload tickets mention email)
3. **Critical priority network/infrastructure outages** affecting multiple users
4. **Issues impacting critical business infrastructure** (21% workload premium)
5. **Extended-resolution problems** requiring sustained investigation and troubleshooting

**Actionable Insight:** Database and email service failures, especially at critical priority levels, consistently generate the highest agent workload. These represent candidates for automation, runbook development, or preventive monitoring to reduce repeated agent effort.
