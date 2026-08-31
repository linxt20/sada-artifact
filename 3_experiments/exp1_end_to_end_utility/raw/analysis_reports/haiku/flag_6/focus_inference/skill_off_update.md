---
dataset: flag_6
scenario: focus_inference
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth analyzing in these incident tickets."
source_table: augment_table/flag_6/focus_inference/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:21:06.962538+00:00
wall_seconds: 59.86
---

# Incident Ticket Analysis Report: skill_off Variant
**Focus:** Understanding what's worth analyzing in these incident tickets

## Executive Summary

This dataset contains **500 IT incident tickets** spanning 2023–2024, primarily focused on **infrastructure and network issues**. The variant label `skill_off` suggests this data may reflect scenarios where AI models lack domain-specific tuning. The analysis identifies several actionable focus areas for deeper investigation.

---

## Key Findings Worth Investigating

### 1. **Data Quality & Temporal Anomalies**
- **Negative Resolution Times (10% of tickets)**: 50 records have negative `resolution_time_hours` (range: -400.7 to -2.9 hours)
  - **Implication**: Timestamps are misaligned (closed before opened, or updated timestamp earlier than creation)
  - **Worth analyzing**: Root cause of temporal reversals; affects SLA calculation reliability
  - **Variant relevance**: A skill-off model might not flag these as data quality issues

### 2. **Incomplete/Open Tickets (4.4%)**
- **22 tickets remain unresolved**: 11 "New" and 11 "In Progress"
  - 22 of these lack a `closed_by` assignee (as expected)
  - 3 of these 22 are marked as critical priority
  - **Database server outage (INC0000000496)** is marked critical but unresolved since 2024-01-28
  - **Worth analyzing**: Why critical tickets stall; handling of long-running incidents

### 3. **Domain-Specific Risk Profiles**
- **Database incidents** show highest critical priority rate: **24.8%** (27/109 incidents)
- **Infrastructure/Network** incidents: **18.7%** (58/310 critical priority)
- **Software incidents** are least critical: **1.4%** (1/72 critical priority)
  - **Implication**: Database issues pose greater risk and warrant separate SLA/handling
  - **Worth analyzing**: Whether critical database incidents have faster resolution (average resolution time: ~171 hours across all)

### 4. **Recurrence Patterns**
- **High recurrence baseline**: ~69% of tickets show recurrence indicator > 0
- **By domain**:
  - Database: avg recurrence = 1.13
  - Infrastructure: avg recurrence = 1.12
  - Software: avg recurrence = **0.65** (notably lower)
  - **Implication**: Network and database problems repeat; software issues are more isolated
  - **Worth analyzing**: Underlying systemic issues vs. one-time fixes

### 5. **Dominant Problem Categories**
- **Email-related issues**: 134 tickets (26.8%) — likely miscellaneous network/software problems miscategorized
- **VPN connectivity**: 109 tickets (21.8%) — represents ~22% of all incidents
- **Database connectivity**: 98 tickets (19.6%)
  - **Network assignment group** dominates: 328/500 (65.6%) of all tickets
  - **Implication**: Infrastructure stability is the core operational concern
  - **Worth analyzing**: Whether root causes (hardware, configuration, capacity) are being logged vs. symptoms

### 6. **Priority vs. Actual Status Mismatch**
- **High priority incidents (379 of 500)**:
  - Mean resolution time: **~224 hours** (9.3 days)
  - But 50 tickets show negative times, and 88 are marked critical with priority "1 - Critical"
  - **Critical priority (88 tickets)**:
    - 84/88 are either Closed or Resolved
    - Mean resolution time for these: varies widely due to negative times
  - **Worth analyzing**: Whether priority levels correlate with actual urgency or are arbitrarily assigned

### 7. **Assignment & Closure Patterns**
- **Assigned staff**: Most tickets handled by Luke Wilson, Howard Johnson, Fred Luddy, Beth Anglin, Charlie Whitherspoon
- **Closure rate by assignee**: Not uniformly distributed (weak evidence in current data)
- **Worth analyzing**: Whether certain assignees resolve critical issues faster, or if some domains are understaffed

---

## Weak Evidence / Important Caveats

1. **Resolution time validity**: 50 negative values make time-based analytics unreliable without preprocessing
2. **Category labels**: "Network" appears only 3 times in descriptions but 328 tickets are Network-assigned—suggests mismatch between assignment group and category fields
3. **Recurrence indicator meaning**: Values range 0–3 but semantics unclear (frequency? severity escalation?); difficult to interpret trend
4. **Missing root cause data**: Short descriptions don't include resolution details or underlying cause, limiting root-cause analysis
5. **Variant relevance unclear**: No explicit "skill_off" metric visible; unclear whether this refers to ML prediction error, human action removal, or benchmark condition

---

## Actionable Recommendations

1. **Prioritize data cleaning**: Fix temporal anomalies before computing resolution SLAs
2. **Investigate VPN/Email clusters**: These two categories represent ~48% of incidents—focus on systemic fixes
3. **Segment by domain**: Treat Database and Infrastructure incidents separately; apply different resolution timeouts
4. **Track recurrence by root cause**: Identify repeat issues to prevent false-fix closures
5. **Audit critical ticket escalation**: Ensure "1 - Critical" priority is consistently applied and resolved within defined SLA

---

## Dataset Characteristics (Summary)

| Metric | Value |
|--------|-------|
| Total Tickets | 500 |
| Closed/Resolved | 478 (95.6%) |
| Critical (is_critical=1) | 88 (17.6%) |
| High Priority (2 - High) | 379 (75.8%) |
| Avg Resolution Time | 223.5 hours |
| Median Resolution Time | 150 hours |
| Recurrence Avg | 1.10 |
| Data Quality Issues | ~10% negative times, ~4.4% incomplete |
