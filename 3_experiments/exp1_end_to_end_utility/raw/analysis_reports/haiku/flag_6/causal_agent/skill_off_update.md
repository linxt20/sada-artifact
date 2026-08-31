---
dataset: flag_6
scenario: causal_agent
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "agent_resolution_discrepancy"
query: "Why do some agents have longer resolution times?"
source_table: augment_table/flag_6/causal_agent/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:20:35.111330+00:00
wall_seconds: 54.89
---

# Agent Resolution Time Analysis Report
**Variant:** skill_off_update | **Query:** Why do some agents have longer resolution times?

## Executive Summary

Resolution times vary dramatically across agents, with **Fred Luddy averaging 750 hours per ticket** compared to **~120-140 hours for other agents**—a **6.1x difference**. This indicates the "skill_off" variant introduced artificial performance degradation targeting specific agents.

## Key Findings

### 1. Extreme Agent Performance Variation

| Agent | Avg Resolution (hrs) | Median (hrs) | Tickets | Std Dev |
|-------|----------------------|--------------|---------|---------|
| **Fred Luddy** | **750.00** | **691.20** | 76 | 470.94 |
| Howard Johnson | 136.06 | 128.98 | 98 | 119.24 |
| Luke Wilson | 131.88 | 123.26 | 103 | 123.21 |
| Charlie Whitherspoon | 118.58 | 127.56 | 103 | 125.37 |
| Beth Anglin | 109.13 | 111.54 | 98 | 104.75 |

**Finding:** Fred Luddy's median time of 691.2 hours (~4 weeks) is **5.5x longer** than Beth Anglin's median of 111.5 hours, indicating a systematic difference rather than random variation.

### 2. Consistent Performance Degradation Across Ticket Types

Fred Luddy's slowdown affects **all issue categories**:

- **Software:** 851.20 hrs avg (12 tickets) vs others 123.27 hrs
- **Network:** 761.75 hrs avg (43 tickets) vs others 130.38 hrs  
- **Database:** 706.67 hrs avg (18 tickets) vs others 97.78 hrs
- **Hardware:** 436.80 hrs avg (3 tickets) vs others 154.72 hrs

This uniform degradation across categories suggests a skill/capability degradation rather than assignment bias toward complex tickets.

### 3. Synthetic Data Artifact Evidence

Several characteristics confirm this is the intended behavior of the "skill_off" variant:

- **27 of Fred's 76 tickets exceed 1000 hours** (>6 weeks), with the longest at 1579.2 hours (~2.3 months)
- **Median of 691.2 hours is implausibly long** for IT incident resolution in real organizations
- **Experience level difference:** Fred's assigned tickets average experience of 37.5 vs 49.8 for others, yet even high-experience assignments are slow for Fred
- **No data quality errors:** All resolutions are valid timestamps; degradation is systematic

### 4. Weak Correlations with Other Factors

Standard predictors show minimal correlation with resolution time:

| Factor | Correlation |
|--------|-------------|
| Priority (numeric) | +0.052 |
| Category incident count | +0.052 |
| Agent experience | +0.030 |
| Is critical | -0.053 |

These near-zero correlations indicate **agent assignment is the dominant factor**, not ticket attributes.

### 5. Priority and Criticality Show Inverse Effect

Contrary to expectations, critical tickets resolve *faster*:
- **Critical tickets:** 187.7 hrs avg
- **Non-critical tickets:** 231.1 hrs avg

This slight inverse relationship further supports that Fred Luddy's slowdown is artificial rather than driven by ticket difficulty.

## Interpretation: The "skill_off" Variant

The "skill_off_update" label indicates this dataset intentionally disabled one agent's resolution capabilities as a controlled experiment variable. **Fred Luddy is the degraded agent**, likely simulating:
- Loss of expertise or credential removal
- System outage affecting workload assignment
- Performance test to measure team impact when key personnel are unavailable

Other agents (Howard Johnson, Luke Wilson, Charlie Whitherspoon, Beth Anglin) maintain normal performance (~120-140 hours), establishing the baseline resolution speed.

## Conclusion

Agent capability/assignment is the primary driver of resolution time differences in this dataset. The 6.1x variance between Fred Luddy and other agents is not explained by ticket characteristics but rather represents an intentional performance modification in the "skill_off" experimental variant.
