---
dataset: flag_12
scenario: eda_efficiency
variant: original
model: substrate-claude-haiku-4-5
query_subtype: exploratory_data_analysis
focus_variable: "resolution_efficiency"
query: "How does incident resolution efficiency vary across category, priority, and assignment group?"
source_table: augment_table/flag_12/eda_efficiency/original.csv
generated_at: 2026-07-26T13:13:44.138997+00:00
wall_seconds: 56.78
---

# Incident Resolution Efficiency Analysis: Original Variant

## Executive Summary

This analysis examines incident resolution efficiency (time from opening to closure) across **category**, **priority**, and **assignment group** dimensions in a dataset of 500 IT service incidents. The overall mean resolution time is **7.43 days** (median: 7.22 days), with approximately one-third of incidents resolved quickly (<5 days) and another third taking longer than 10 days.

---

## Key Findings

### 1. Category Impact on Resolution Efficiency

**Software demonstrates the fastest resolution**, with a mean of **6.40 days** and the highest proportion of fast resolutions (48.5% resolved in <5 days). This suggests category-specific handling or ticket complexity differences.

- **Software**: 6.40 days average, most efficient (48.5% fast)
- **Network**: 6.74 days average, second-fastest with 45.5% fast resolutions
- **Database**: 7.18 days average, 52.6% in moderate range (5-10 days)
- **Hardware**: 7.56 days average, the largest category (406/500 incidents, 81.2%)
- **Inquiry / Help**: 7.59 days average, 35% slow resolutions (>10 days)

**Hardware dominance**: The Hardware category represents 81% of all incidents, establishing it as the baseline for overall efficiency trends. However, its 7.56-day average is slightly above the overall mean, suggesting some drag on efficiency.

**Variability**: Network and Software categories show higher relative variability (CV of 0.71 and 0.70 respectively) compared to Database (0.59), indicating less predictable resolution times for network and software issues.

### 2. Priority Impact on Resolution Efficiency

**Critical priority incidents resolve fastest** at 6.96 days, contradicting expectations and suggesting prioritization mechanisms work effectively. However, sample size is small (27 critical incidents).

- **1 - Critical**: 6.96 days average, 40.7% fast (N=27)
- **2 - High**: 7.50 days average, 32.0% fast (N=394, dominates dataset)
- **3 - Moderate**: 7.41 days average, 36.4% fast (N=77)
- **4 - Low**: 1.36 days average (N=2, insufficient data)

**High priority is the constraint**: The majority of incidents (79%) are marked as "2 - High" priority with 7.50-day average resolution—essentially at the overall mean. This suggests either broad classification or limited differentiation in handling high-priority incidents.

**No strong priority stratification**: Moderate-priority incidents (7.41 days) resolve almost as quickly as High-priority ones (7.50 days), indicating weak enforcement of priority-based SLAs or similar underlying complexity across priority levels.

### 3. Assignment Group Impact on Resolution Efficiency

**Software and Network assignment groups are most efficient**, with means of 6.40 and 6.73 days respectively.

- **Software**: 6.40 days average, 48.5% fast (N=33)
- **Network**: 6.73 days average, 43.5% fast (N=23)
- **Hardware**: 7.56 days average, 31.6% fast (N=405, dominant)
- **Service Desk**: 7.35 days average, 36.8% fast (N=19)
- **Database**: 7.43 days average, 30.0% fast (N=20)

**Hardware team is the bottleneck**: Processing 405 of 500 incidents, the Hardware assignment group's 7.56-day average directly anchors overall efficiency. The 31.6% fast-resolution rate suggests capacity or complexity constraints.

**Smaller teams are faster**: Software (33 incidents) and Network (23 incidents) resolve issues 18-25% faster than Hardware. This may reflect:
- Lower ticket volume per team member
- More specialized expertise reducing troubleshooting time
- Potentially different SLA targets or ticket complexity distributions

### 4. Multi-Dimensional Patterns

**Top incident combination** (Hardware + 2-High priority):
- 336 incidents (67.2% of dataset)
- 7.66-day average resolution
- 27.0% slow resolutions
- This combination drives overall efficiency metrics

**Best-performing combinations**:
- **Database/2-High**: 5.99 days (N=16)
- **Hardware/1-Critical**: 6.20 days (N=16)

**Worst-performing combinations**:
- **Database/1-Critical**: 16.40 days (N=5)
- **Inquiry-Help/1-Critical**: Unresolved in sample (only 3-Moderate priority incidents)

---

## Notable Exceptions & Weak Points

1. **Critical priority paradox**: Critical incidents (6.96d) resolve faster than High (7.50d), suggesting either:
   - Aggressive SLA enforcement for critical issues, or
   - Critical incidents may have simpler root causes than high-priority incidents

2. **Low priority outlier**: Only 2 Low-priority incidents in dataset (1.0 and 1.72 days)—insufficient for meaningful analysis.

3. **Inquiry/Help category risk**: Shows highest slow-resolution rate (35%), with only 20 incidents. Service Desk team (19 incidents) shows moderate efficiency (7.35d), but sample size limits confidence.

4. **Unexplained variance**: High coefficient of variation (0.609) and wide range (1–21.4 days) suggest factors beyond category/priority/group drive resolution time (e.g., individual agent performance, ticket complexity, dependencies).

---

## Implications for Efficiency Improvement

1. **Focus on Hardware throughput**: 81% of incidents and above-average resolution time indicate potential leverage in optimizing Hardware team processes or capacity.

2. **Investigate Database/Critical delays**: 16.4-day average for Database critical issues warrants investigation into root causes and potential SLA violations.

3. **Formalize priority differentiation**: Current data shows minimal difference between High and Moderate priorities. Clear SLA targets and triage improvements could clarify handling strategies.

4. **Leverage Software/Network expertise**: These teams' faster resolution rates (6.4–6.7 days) may provide process improvement opportunities applicable to Hardware.

---

## Data Quality Notes

- **Dataset**: 500 incidents spanning 3 months (Jan–Mar 2023)
- **Completeness**: No missing resolution data; all 500 incidents have closed_at timestamps
- **Boundaries**: Median resolution time (7.22 days) near mean (7.43 days) suggests symmetric distribution with controlled outliers
