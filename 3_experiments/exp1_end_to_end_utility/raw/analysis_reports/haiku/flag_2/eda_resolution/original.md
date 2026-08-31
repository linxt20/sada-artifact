---
dataset: flag_2
scenario: eda_resolution
variant: original
model: substrate-claude-haiku-4-5
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary across category, priority, and assignment group?"
source_table: augment_table/flag_2/eda_resolution/original.csv
generated_at: 2026-07-26T13:27:10.408801+00:00
wall_seconds: 61.46
---

# Resolution Time Analysis: Original Dataset

## Executive Summary

This analysis examines resolution time patterns across **category**, **priority**, and **assignment group** dimensions in a dataset of 500 IT service incidents. Mean resolution time is **1,043 hours** (~43 days), with median **1,032 hours**, indicating relatively long resolution cycles with high variability (SD: 618 hours). Resolution times vary moderately across the three dimensions, with distinct patterns by priority level and assignment group effectiveness.

## Key Findings

### 1. Category Variations

Resolution time varies modestly across the five incident categories:

| Category | Count | Mean (hours) | Median (hours) | Std Dev |
|----------|-------|--------------|----------------|---------|
| **Database** | 86 | 955 | 967 | 557 |
| **Hardware** | 12 | 1,105 | 1,021 | 637 |
| **Inquiry / Help** | 7 | 958 | 686 | 674 |
| **Network** | 197 | 1,079 | 1,046 | 630 |
| **Software** | 70 | 1,051 | 985 | 652 |

**Database** issues resolve fastest (mean: 955 hours), likely due to dedicated Database assignment group handling. **Network** incidents are slowest (mean: 1,079 hours) despite being the largest category (n=197), suggesting potential resource constraints or complexity. Hardware and Software categories fall in the middle range with similar means (~1,050–1,105 hours).

### 2. Priority Patterns

Priority significantly influences resolution speed, but not uniformly:

| Priority | Count | Mean (hours) | Median (hours) | Std Dev |
|----------|-------|--------------|----------------|---------|
| **1 - Critical** | 57 | 1,119 | 1,255 | 624 |
| **2 - High** | 283 | 1,019 | 974 | 601 |
| **3 - Moderate** | 32 | 1,121 | 1,100 | 750 |

**Counterintuitive finding**: Critical and Moderate priorities take *longer* (1,119–1,121 hours) than High priority (1,019 hours). This suggests either: (a) Critical issues are inherently more complex, (b) Moderate incidents lack urgency in assignment or handling, or (c) High-priority incidents receive preferential treatment. The High priority group (n=283, 57% of incidents) drives the overall dataset characteristics.

### 3. Assignment Group Effectiveness

Different assignment groups show substantial differences in resolution efficiency:

| Assignment Group | Count | Mean (hours) | Median (hours) | Std Dev |
|------------------|-------|--------------|----------------|---------|
| **Database** | 89 | 946 | 960 | 553 |
| **Hardware** | 4 | 926 | 794 | 786 |
| **Network** | 221 | 1,074 | 1,046 | 627 |
| **Service Desk** | 32 | 1,102 | 1,129 | 613 |
| **Software** | 25 | 1,028 | 823 | 733 |

**Database group is most efficient** (mean: 946 hours, fastest across all groups), handling 89 incidents with consistent performance (SD: 553). **Network group is slowest** (mean: 1,074 hours) despite handling 221 incidents (44% of dataset), suggesting either capacity constraints or higher intrinsic complexity in network issues. Service Desk is also slower than average (1,102 hours), which may indicate it handles lower-priority or more complex routing cases. The lone Openspace assignment (n=1) shows an outlier of 1,853 hours.

### 4. Combined Dimension Insights

Cross-tabulation reveals interaction effects:

**Database incidents by priority:**
- Critical: 1,244 hours (13 cases)
- High: 910 hours (68 cases)  
- Moderate: 817 hours (5 cases)

Database shows the clearest priority effect—Critical issues take 35% longer than High priority, which aligns with expected complexity.

**Network incidents by priority:**
- Critical: 1,044 hours (36 cases)
- High: 1,079 hours (151 cases)
- Moderate: 1,165 hours (7 cases)

Network's priority pattern is atypical: High and Moderate resolve *slower* than Critical, contradicting typical SLA-driven behavior.

**Assignment group handling by priority (High priority):**
- Database: 902 hours (fastest)
- Network: 1,071 hours (similar to overall Network average)
- Service Desk: 1,007 hours (middle ground)
- Software: 913 hours (fast, but small sample of 19)

Database group maintains its efficiency advantage even within the largest priority slice (High priority, n=283).

## Weak Evidence & Exceptions

1. **Small category/group cells**: Inquiry/Help (n=7), Hardware with groups (n=2–4), and Openspace (n=1) lack sufficient sample size for reliable inference.
2. **High variance**: Standard deviations (556–787 hours) exceed 50% of means in several groups, indicating outliers and heterogeneity within categories.
3. **Network group dominance**: With 44% of incidents, Network group's slower times may reflect composition differences rather than true group inefficiency (e.g., more inherently complex issues).

## Recommendations

1. **Investigate Network group bottlenecks**: The combination of high incident volume and slow mean resolution warrants root cause analysis.
2. **Replicate Database group practices**: Their consistent efficiency across all priorities offers a benchmark model.
3. **Verify High vs. Critical priority classification**: The counterintuitive pattern (Critical slower than High) suggests potential categorization issues or legitimate complexity differences that should be validated.
4. **Increase sample sizes** for rare category-priority-group combinations before drawing operational conclusions.
