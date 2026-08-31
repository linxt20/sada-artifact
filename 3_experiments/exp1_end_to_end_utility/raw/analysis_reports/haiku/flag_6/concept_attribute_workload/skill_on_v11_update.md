---
dataset: flag_6
scenario: concept_attribute_workload
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "agent_workload_burden"
query: "What kinds of tickets create heavier agent workload?"
source_table: augment_table/flag_6/concept_attribute_workload/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:19:30.493150+00:00
wall_seconds: 60.05
---

# Analysis Report: What Kinds of Tickets Create Heavier Agent Workload?

## Executive Summary

This analysis of 478 tickets identifies several ticket characteristics that significantly impact agent workload. Heavier workload is driven primarily by **software issues, VPN connectivity problems, and system-wide infrastructure tickets**, with resolution durations extending substantially beyond average. The focus variable `skill_on` variant indicates skill-based workload distribution affects ticket complexity and handling requirements.

## Key Findings

### 1. **Software Issues Create Heaviest Workload**

Software-related tickets impose the most severe workload burden:
- **16 tickets** with average **17.02 days** resolution time (83% longer than baseline)
- Maximum duration: **65.8 days**
- All are single-occurrence issues, suggesting complexity rather than frequency
- Primarily High-priority (12 of 16), indicating critical business impact

**Implication**: Software tickets require specialized skill and extended troubleshooting, creating concentrated agent effort.

### 2. **VPN Connectivity Issues Require Extended Resolution**

VPN connectivity represents a secondary but significant workload driver:
- **106 tickets** with average **11.16 days** resolution time (20% above average)
- 86 are system-wide scope, affecting multiple users simultaneously
- High handoff rate: **81.1%** require escalation/agent transfers
- Predominantly High-priority (104 of 106)

**Implication**: VPN issues are widespread, impact many users, and frequently require coordination across agents, multiplying effective workload.

### 3. **System-Wide Scope Multiplies Workload Impact**

Tickets affecting the entire system consume more agent resources:
- **383 system-wide tickets** (80% of dataset) average **9.82 days**
- User-specific tickets average only **7.64 days** (2.3 days faster)
- High-priority system-wide tickets (363 total): **9.67 days** average

**Implication**: System-wide issues demand broader expertise, coordination, and create higher stakes requiring more careful resolution and validation.

### 4. **Infrastructure Categories Dominate Workload Volume**

The top four issue categories account for 444 of 478 tickets (93%):
- **Email server**: 132 tickets, 7.91 days average (high volume, moderate duration)
- **Network connectivity**: 107 tickets, 8.58 days average
- **VPN connectivity**: 106 tickets, 11.16 days average (longest for high-volume category)
- **Database access**: 99 tickets, 8.65 days average

These interconnected infrastructure issues create sustained workload rather than peak bursts.

### 5. **Handoff-Heavy Tickets Increase Overall Workload**

Tickets requiring different agents for closure consume more coordination effort:
- **379 handoff tickets** (79% of dataset): **9.39 days** average
- **99 self-closed tickets**: **9.03 days** average
- Difference: +0.36 days per handoff ticket

While small per-ticket, the volume (300+ handoffs) creates cumulative demand for context-switching and communication across the agent pool.

### 6. **Single-Occurrence Issues Require More Time Than Recurring Problems**

Counterintuitively, non-recurring tickets demand more agent effort:
- **Single-occurrence**: 295 tickets, **9.91 days** average
- **Recurring (same component)**: 183 tickets, **8.35 days** average (16% faster)

**Interpretation**: Once recurring issues are understood, resolution becomes routine. Novel problems require investigation, potentially involving external expertise or escalation.

## Workload Patterns: Combined Effects

High-priority system-wide single-occurrence tickets represent peak workload scenarios:
- **177 such tickets** with **9.70+ days** average resolution
- When involving software or authentication issues, durations extend toward 11-17 days
- These are disproportionately represented in the handoff category

## Recommendations for Workload Management

1. **Prioritize Software Skill Development**: Software tickets take 70% longer than average; specialized training and pre-built runbooks would reduce resolution time.

2. **Establish VPN Escalation Protocols**: With 81% handoff rate and 11+ day average, VPN issues need dedicated expertise to minimize transfers.

3. **Document Recurring Solutions**: Database, network, and email server problems recur frequently; codifying solutions could accelerate resolution by ~1-2 days per ticket.

4. **Plan for System-Wide Impact**: 80% of tickets are system-wide; allocate resources to handle broad-impact issues requiring multi-agent coordination.

5. **Monitor Skill Assignment Alignment**: The `skill_on` variant suggests agents are assigned by skill level; ensure software and VPN specialists are appropriately loaded given 70%+ longer resolution times.

## Data Quality Notes

- Dataset: 478 valid tickets (500 total, 22 with unknown closure patterns excluded)
- Average ticket resolution: 9.31 days
- Analysis focuses on duration as primary workload indicator; agent utilization and concurrent ticket load are not directly measured
- Single-month dataset (January–March 2023) may not reflect seasonal variation
