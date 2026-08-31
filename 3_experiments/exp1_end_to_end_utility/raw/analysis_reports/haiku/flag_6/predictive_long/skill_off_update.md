---
dataset: flag_6
scenario: predictive_long
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "resolution_time"
query: "What signals suggest an agent's tickets will take longer to resolve?"
source_table: augment_table/flag_6/predictive_long/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:21:29.699563+00:00
wall_seconds: 54.59
---

# Analysis Report: Signals for Longer Ticket Resolution Times

## Executive Summary

This analysis examines factors associated with longer ticket resolution times in the IT helpdesk dataset (*skill_off* variant, N=500). The target variable is `resolution_days`. We define "long resolution" as tickets exceeding 10.33 days (75th percentile), representing approximately 24% of tickets.

## Dataset Overview

- **Total Tickets**: 500
- **Mean Resolution Time**: 9.31 days
- **Median Resolution Time**: 6.25 days  
- **Range**: -16.70 to 65.80 days (note: 50 tickets have negative values, indicating data quality issues)
- **75th Percentile (Long ticket threshold)**: 10.33 days

## Primary Signals for Longer Resolution Times

### 1. **Software-related Issues (Strongest Signal)**

**Software assignment group** shows the clearest association with longer resolution times:
- **Mean resolution**: 14.47 days (57% longer than dataset average)
- **% Long tickets**: 30.8% (highest among all groups)
- **Count**: 25 tickets
- **Priority 2 Software**: 10.74 days mean (26.3% long)

**Software category** also signals longer times:
- **Mean resolution**: 10.34 days  
- **% Long tickets**: 26.4%
- **Count**: 70 tickets

This is the strongest visible pattern—software tickets consistently take longer regardless of priority level.

### 2. **Network Issues (Moderate Signal)**

Network-related tickets show elevated resolution times:
- **Category**: Mean 9.61 days, 25% long tickets (N=271)
- **Assignment Group**: Mean 9.24 days, 24.1% long (N=314)
- **Network + Priority 2**: 10.03 days mean, 27.9% long (largest subgroup, N=222)

Network problems represent the largest ticket volume and moderately elevated resolution times.

### 3. **Moderate Priority (Priority Level 2-3)**

Counter-intuitive finding: lower-urgency tickets take longer:
- **Priority 2**: 9.58 days mean, 25.9% long (largest group, N=364)
- **Priority 3**: 10.27 days mean, 24.2% long (N=30)
- **Priority 1** (Critical): 7.82 days mean, 15.9% long (N=84)

This suggests critical tickets receive accelerated handling, while moderate-priority items may experience longer queuing or lower resource allocation focus.

## Weak or Contradictory Signals

The following factors show minimal predictive value:

- **Agent Changes** (correlation: +0.011): Agent handoffs correlate negligibly with resolution time. Agent changed: 9.39 days vs. stayed same: 9.03 days (not significant).
  
- **Critical Domain Status** (correlation: -0.044): Surprisingly, critical domain tickets resolve *slightly faster* (8.37 vs. 9.66 days), opposite to expectations. This weak negative signal suggests domain criticality alone doesn't determine resolution speed.

- **Same-Agent Assignment** (correlation: -0.011): No meaningful difference whether the same agent stays on the ticket.

- **Network Category Flag** (correlation: +0.026): The binary network flag shows almost no correlation.

## Data Quality Notes

- **Negative resolution values**: 50 tickets (10% of data) have negative resolution_days, indicating tickets closed before formally opened or timestamp errors. These cases introduce noise but don't reverse the identified patterns.

- **Extreme cases**: Software and Network tickets dominate the longest resolution times (top 10 longest are all Software or Network, mean ~62 days).

## Summary: Key Signals for Longer Ticket Resolution

| Signal | Mean Days | % Long | Strength |
|--------|-----------|--------|----------|
| Software assignment group | 14.47 | 30.8% | **Strong** |
| Software category | 10.34 | 26.4% | **Strong** |
| Network + Priority 2 | 10.03 | 27.9% | **Moderate** |
| Priority 2 (Moderate) | 9.58 | 25.9% | **Moderate** |
| Priority 3 (Low) | 10.27 | 24.2% | **Moderate** |
| Non-critical domain | 9.66 | 24.9% | **Weak** |
| Priority 1 (Critical) | 7.82 | 15.9% | Baseline |

## Recommendations

1. **Focus on Software tickets**: 31% exceed the long-resolution threshold. This category warrants investigation into root causes (complexity, skill gaps, resource constraints).

2. **Prioritize Critical tickets**: Priority 1 tickets resolve 2-4 days faster than moderate/low priorities, suggesting effective fast-track handling exists. Apply similar mechanisms to software issues.

3. **Deprioritize agent/domain factors** for predictive models: Agent changes and critical domain status show negligible predictive power in this dataset.

4. **Address data quality**: Investigate 50 negative-resolution-time cases to understand timestamp anomalies.
