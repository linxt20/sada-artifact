---
dataset: flag_12
scenario: predictive_inefficient
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "inefficient_resolution"
query: "What signals suggest an incident resolution will be inefficient?"
source_table: augment_table/flag_12/predictive_inefficient/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:14:04.998698+00:00
wall_seconds: 53.57
---

# Incident Resolution Inefficiency Analysis

## Executive Summary

This analysis identifies signals that predict inefficient incident resolution by examining 500 incident records. We define **inefficiency** as resolution times exceeding the 75th percentile (282 hours or ~11.7 days). Using this threshold, 87 incidents (17.4%) were classified as inefficient.

## Key Signals of Inefficient Resolution

### 1. **Hardware & Printer Issues Dominate Inefficiency**
- **Printer incidents** account for 44% of all inefficient resolutions (38 of 87 incidents)
- **Hardware category** comprises 84% of inefficient cases (73 of 87)
- Printer incidents average 184 hours vs. connectivity issues at 169 hours
- **Implication**: Hardware failures, especially printers, systematically take longer to resolve

### 2. **Recurring Device Problems Signal Prolonged Resolution**
- **Recurring device issues** comprise 66% of inefficient incidents (57 of 87)
- Recurring problems average 181 hours vs. novel issues at 173 hours
- **Pattern insight**: Issues that repeat across similar device types suggest incomplete root cause resolution or systemic resource constraints

### 3. **Specific Incident Types Drive Inefficiency**
Resolution times by incident type reveal:
- **Printer issues**: 184 hours avg, 19% inefficiency rate
- **Hardware issues**: 181 hours avg, 18% inefficiency rate  
- **Connectivity issues**: 169 hours avg, 15% inefficiency rate
- **Software issues**: 159 hours avg, 14% inefficiency rate (least problematic)

### 4. **Assignment Patterns Correlate with Resolution Speed**
Assignee performance varies significantly:
- **Fred Luddy**: 165 hours avg, 10% inefficiency (fastest)
- **Luke Wilson**: 196 hours avg, 22% inefficiency (slowest)
- **Howard Johnson**: 176 hours avg, 22% inefficiency
- **Difference span**: 31 hours between fastest and slowest, suggesting skill, workload, or process differences

### 5. **High Priority Status Does Not Prevent Inefficiency**
- High priority incidents (2 - High) are 79% of the dataset but still show 18% inefficiency rate
- Critical incidents (1 - Critical) average 167 hours with 15% inefficiency
- **Finding**: Priority labeling alone does not ensure rapid resolution; underlying incident complexity matters more

### 6. **Upstream Dependencies Weakly Predict Efficiency**
- Incidents with upstream dependencies resolve slightly *faster* (172 hours avg) vs. without (179 hours avg)
- Upstream incidents show 13% inefficiency vs. 18% for standalone issues
- **Implication**: Incidents with clear external dependencies may force parallelization or escalation paths

### 7. **Description Clarity Shows Minimal Correlation**
- Incidents with unclear descriptions average 177 hours, clear descriptions 182 hours
- Inefficiency rates are nearly identical (17% vs. 18%)
- **Insight**: Resolution time is driven more by incident complexity than documentation quality

## Typical Inefficient Incident Profile

Based on analysis of the longest-resolution cases (>400 hours):

| Attribute | Pattern |
|-----------|---------|
| **Incident Type** | Printer or hardware (keyboard, monitor, hard drive) |
| **Category** | Hardware |
| **Priority** | Usually 2-High or 3-Moderate |
| **Recurrence** | Recurring across similar devices |
| **Duration** | 17–21 days |
| **Assigned To** | Luke Wilson or Howard Johnson (higher workload incidents) |

## Weak Signals (No Clear Predictive Power)

- **Description clarity**: Nearly identical efficiency between clear and unclear descriptions
- **Caller type**: No meaningful variation by caller identity
- **State (Closed vs. Resolved)**: Both show ~18% inefficiency
- **Upstream dependency**: Weakly protective, not strongly predictive

## Recommendations

1. **Prioritize hardware/printer incident automation**: Recurring printer and device issues are low-complexity but time-consuming; establish self-service or faster escalation paths
2. **Skill-based routing**: Route hardware incidents to Fred Luddy (10% inefficiency) rather than Luke Wilson (22% inefficiency) when possible
3. **Investigate bottlenecks for recurring issues**: 66% of inefficient cases are recurring; lack of permanent fixes suggests process or resource gaps
4. **Monitor assignment workload**: Performance variance by assignee suggests uneven workload distribution or skill gaps

## Confidence and Limitations

- **Threshold definition**: Inefficiency based on statistical percentile; business-driven thresholds may differ
- **Causal vs. correlative**: Signal analysis identifies patterns, not causes; hardware complexity may naturally demand longer resolution
- **Limited outcome data**: Dataset contains only resolution time; cost, customer impact, or escalation frequency not available

---

**Analysis Date**: 2026-07-30  
**Dataset**: haiku__skill_on_v11_update.csv (500 incidents, flag_12)  
**Focus Variable**: Inefficient resolution (time > 282 hours)
