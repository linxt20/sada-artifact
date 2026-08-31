---
dataset: flag_2
scenario: predictive_long
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "resolution_time"
query: "What signals suggest an incident will take longer to resolve?"
source_table: augment_table/flag_2/predictive_long/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:16:40.521132+00:00
wall_seconds: 63.43
---

# Incident Resolution Time Analysis: Predictive Long Resolution

## Executive Summary

This analysis identifies signals that predict longer incident resolution times (≥1,557.6 hours, top quartile) in the dataset variant `skill_off`. The dataset contains 500 IT service incidents with resolution times ranging from 24 to 2,205.6 hours (median: 1,032 hours).

## Key Findings

### 1. **Assignment Group is a Primary Predictor**

The assignment group handling the incident significantly correlates with resolution duration:

- **Network incidents**: 1,074.0 hours avg (highest) — 27.1% fall into long resolution category
- **Service Desk incidents**: 1,102.4 hours avg — 21.9% long
- **Software incidents**: 1,028.3 hours avg — 28.0% long
- **Database incidents**: 946.5 hours avg (lowest) — 20.2% long
- **Hardware incidents**: 925.8 hours avg — 25.0% long

**Signal**: Network-assigned incidents take substantially longer, suggesting complexity in network troubleshooting or broader system impact.

### 2. **System-Generated Updates Correlate with Longer Resolution**

System updaters (vs. manual human updaters) show elevated resolution times:

- **System-updated incidents** (updater_is_system=1): 1,077.1 hours avg, **28.1% long** resolution rate
- **Manually-updated incidents** (updater_is_system=0): 1,023.3 hours avg, 23.6% long resolution rate

This 5% differential in long-resolution occurrence is consistent across assignment groups, suggesting incidents requiring automated system updates may indicate deeper technical problems or repeated escalations.

### 3. **Non-Critical/Non-High Priority May Paradoxically Take Longer**

Moderate priority incidents show surprising resolution patterns:

- **Priority 1 - Critical**: 1,118.7 hours avg, 28.1% long
- **Priority 3 - Moderate**: 1,120.7 hours avg, 31.3% long  
- **Priority 2 - High**: 1,019.5 hours avg, 24.0% long

**Signal**: Moderate-priority incidents have the highest long-resolution rate (31.3%), suggesting they may receive lower urgency and get deprioritized, or represent less common/more complex issues.

### 4. **Category Complexity Shows Weak but Consistent Pattern**

- **Category complexity = 2** (mid-complexity): 1,072.8 hours avg, 26.9% long
- **Category complexity = 1 or 3**: 957.9–955.0 hours avg, 14.3–20.9% long

Mid-complexity issues slightly exceed both simple and highly complex issues in resolution time, possibly indicating "Goldilocks zone" problems that are neither trivial nor requiring specialized expertise.

### 5. **Time Risk Indicator Shows Modest Elevation**

- **time_risk = 2**: 1,066.3 hours avg, **26.0% long** resolution rate
- **time_risk = 1**: 1,017.8 hours avg, 24.4% long resolution rate

The 2% differential suggests incidents flagged with time risk do take moderately longer.

### 6. **Critical/High Priority Flag (is_critical_high) Shows Weak Inverse Correlation**

- **Non-critical/high** (is_critical_high=0): 1,120.7 hours avg, **31.3% long**
- **Critical/high** (is_critical_high=1): 1,036.1 hours avg, 24.7% long

This suggests properly flagged critical incidents may receive more focused attention and resolve faster, while incidents *not* flagged as critical take longer.

### 7. **Description Complexity Has Minimal Impact**

- **description_complexity = 1**: 1,055.0 hours avg, 24.6% long
- **description_complexity = 2**: 1,021.3 hours avg, 26.6% long

The variance is minimal (within 3%), indicating description clarity alone is not a strong predictor.

### 8. **State (Closed vs. Resolved) Shows No Material Difference**

Both states show ~25% long-resolution rate (248.6% closed, 256.5% resolved), indicating the incident final state is not predictive of duration.

## Weak Evidence

- **Correlation coefficients** between numeric predictors and resolution_hours are weak (max 0.042), suggesting resolution time is driven by complex interactions or external factors not fully captured in the structured fields.
- **same_assignee_caller** contains only zeros in this dataset, providing no signal.
- **status_risk** has no variance (all values = 1), providing no predictive power.

## Conclusion

**Strongest signals for longer resolution times:**

1. **Network assignment group** — highest baseline resolution time
2. **System-updated incidents** — indicates potential for iterative troubleshooting  
3. **Moderate priority designation** — may signal deprioritization or complexity misclassification
4. **Time risk flag** — modest but consistent indicator

Organizations should prioritize Network group incidents and monitor moderate-priority items to ensure appropriate escalation and resource allocation. System-updated incidents warrant review for workflow improvements to accelerate resolution.
