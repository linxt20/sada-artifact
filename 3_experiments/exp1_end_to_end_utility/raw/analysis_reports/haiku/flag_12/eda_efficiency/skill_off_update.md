---
dataset: flag_12
scenario: eda_efficiency
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_efficiency"
query: "How does incident resolution efficiency vary across category, priority, and assignment group?"
source_table: augment_table/flag_12/eda_efficiency/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:10:33.744016+00:00
wall_seconds: 74.6
---

# Incident Resolution Efficiency Analysis Report
**Variant:** skill_off | **Date:** 2026-07-28

## Executive Summary

This analysis examines how incident resolution efficiency varies across **category**, **priority**, and **assignment group** using 500 incidents from the "skill_off" variant of the EDA efficiency augmentation. The efficiency score (0-100, where higher is better) is inversely correlated with resolution hours, indicating that faster resolutions yield better efficiency ratings.

**Key Finding:** Efficiency patterns are most strongly driven by **priority level** and **resolution duration**, with secondary effects from category and assignment group. Software issues and Network incidents achieve the highest average efficiency, while Database incidents show substantial variability.

---

## 1. Overall Efficiency Profile

- **Mean Efficiency Score:** 65.29 (SD ± 21.15)
- **Median Resolution Hours:** 173.2 hours (~7.2 days)
- **Dataset Composition:** 500 incidents, 393 classified as "Slow," 107 as "Normal"
- **Efficiency Inverse Relationship:** Efficiency score and resolution hours exhibit a perfect negative correlation (r = -1.000), confirming that longer resolution times directly diminish efficiency ratings.

---

## 2. Efficiency by Category

| Category | Avg Efficiency | Median Hours | Count | Variance |
|----------|---|---|---|---|
| **Software** | **70.11** ⭐ | 148.0 | 33 | 21.00 |
| **Network** | **68.55** ⭐ | 186.4 | 22 | 22.32 |
| **Database** | 66.46 | 177.5 | 19 | 19.78 |
| **Inquiry/Help** | 64.58 | 182.7 | 20 | 20.85 |
| **Hardware** | 64.70 | 175.4 | 406 | 21.21 |

**Key Observations:**

1. **Software & Network Outperform:** Software incidents average 70.11 efficiency with shortest median resolution (148 hours), followed closely by Network (68.55 efficiency, 186-hour median). These categories resolve faster due to potentially clearer diagnostic pathways.

2. **Hardware Dominance but Lower Efficiency:** Hardware incidents represent 81% of all incidents (406/500) but exhibit below-average efficiency (64.70), likely because they often require physical repairs, parts procurement, or on-site interventions that extend resolution times.

3. **Database Shows Volatility:** Database incidents display the lowest standard deviation (19.78), suggesting more consistent outcomes, but one outlier (1 Critical incident with efficiency 23.42, resolution 393.64 hours) significantly impacts group statistics.

4. **Service Categorization (Inquiry/Help):** Categorized in dataset as "Service Desk" in assignment_group, these 20 incidents maintain moderate efficiency (64.58) despite higher-than-average resolution hours.

---

## 3. Efficiency by Priority Level

| Priority | Avg Efficiency | Median Hours | Count | Sample Size |
|----------|---|---|---|---|
| **1 - Critical** | 67.51 | 164.7 | 27 | 5.4% |
| **2 - High** | 64.97 | 176.6 | 394 | **78.8%** |
| **3 - Moderate** | 65.40 | 164.2 | 77 | 15.4% |
| **4 - Low** | 93.65 | 32.7 | 2 | 0.4% |

**Key Observations:**

1. **Critical Incidents Perform Better:** Despite handling severity, Critical incidents (n=27) achieve 67.51 efficiency—higher than High priority—with slightly shorter median resolution (164.7 vs. 176.6 hours). This suggests prioritization mechanisms work: critical issues receive faster escalation and resource allocation.

2. **High Priority is the Baseline:** The vast majority of incidents (78.8%) are High priority with 64.97 efficiency, effectively anchoring the overall efficiency mean. This is the operational norm.

3. **Moderate Priority Surprisingly Consistent:** Moderate incidents (77 cases, 15.4%) perform comparably to High priority (65.40 vs. 64.97), though with similar median resolution hours. This suggests workload distribution does not heavily favor higher-priority tickets.

4. **Low Priority is Outlier:** Only 2 Low-priority incidents exist, averaging exceptional efficiency (93.65), but this is not statistically meaningful given the sample size.

---

## 4. Efficiency by Assignment Group

| Assignment Group | Avg Efficiency | Median Hours | Count | Variation |
|---|---|---|---|---|
| **Software** | **70.11** | 148.0 | 33 | 21.00 |
| **Network** | **68.56** | 161.1 | 23 | 21.80 |
| **Service Desk** | 65.69 | 179.5 | 19 | 20.81 |
| **Database** | 65.32 | 178.9 | 20 | 19.92 |
| **Hardware** | 64.69 | 175.6 | 405 | 21.23 |

**Key Observations:**

1. **Specialist Teams Excel:** Software and Network assignment groups (serving specialized domains) maintain higher efficiency (70.11 and 68.56 respectively), with Software resolving incidents ~25 hours faster than Hardware median.

2. **Hardware Team Workload Challenge:** The Hardware group manages 405 incidents (81% of total)—far exceeding other teams—yet achieves the lowest average efficiency (64.69). This suggests resource constraints or inherent complexity of hardware resolutions at scale.

3. **Service Desk Consistency:** The Service Desk group (typically Inquiry/Help category) maintains moderate efficiency (65.69) with above-average resolution hours, reflecting the nature of support queries that often require back-and-forth communication.

4. **No Radical Outliers:** Assignment group efficiencies range narrowly from 64.69 to 70.11 (5.4-point spread), indicating consistent organizational performance despite group specialization.

---

## 5. Three-Way Interaction Analysis

### 5.1 Category × Priority

**Notable Patterns:**

- **Database + Critical:** Critically low efficiency (23.42) with longest resolution (393.64 hours). Only 2 incidents, but this represents a severe outlier—likely production database failures with extensive investigation/recovery requirements.

- **Database + High:** Strong recovery (72.05 efficiency, 143.69 hours). High-priority database issues receive focused attention, resulting in faster resolutions than their Critical counterparts.

- **Hardware + Critical:** Reasonable efficiency (70.92, 149.47 hours). Critical hardware issues resolve faster than High-priority Hardware (64.23 efficiency, 183.88 hours), confirming prioritization advantage.

- **Network + Critical:** Efficient (67.86, 165.22 hours). Network outages at Critical level receive swift remediation, consistent with SLA expectations.

- **Software:** Across all priorities Software maintains 68-79 efficiency, suggesting the category's inherent advantage and clear diagnostic pathways.

---

### 5.2 Category × Assignment Group

**Notable Patterns:**

- **Perfect Alignment:** Category and assignment_group nearly match (e.g., Hardware category routed to Hardware group, Software to Software group). This validates data consistency.

- **Outlier - Inquiry/Help Misrouting:** One Inquiry/Help incident assigned to Database group shows very low efficiency (43.56, 290.10 hours), indicating potential misclassification or assignment error.

- **Network Consistency:** All 22 Network incidents assigned to Network group, maintaining 68.55 efficiency—cleanest categorical alignment.

---

### 5.3 Priority × Assignment Group

**Critical Insights:**

- **Database + Critical:** Severe performance degradation (23.42 efficiency). This specific pairing represents the worst-performing cell in the entire three-way analysis, warranting investigation into whether specialized Database expertise or tools are insufficient for Critical incidents.

- **Hardware + Critical:** Despite high volume baseline, Hardware team resolves Critical incidents at 71.06 efficiency (16 incidents), better than their overall 64.69 average, confirming prioritization mechanisms work.

- **Software + Critical:** Single incident at 95.33 efficiency (24 hours), suggesting Software team can handle Critical issues rapidly when they occur.

---

## 6. Weak Evidence and Caveats

1. **Imbalanced Dataset:** Hardware dominates with 405 incidents (81%), limiting statistical power for other categories. Results for Network (n=22), Database (n=19), and Inquiry/Help (n=20) should be interpreted cautiously.

2. **Outlier Influence:** Database + Critical incidents (n=2, mean efficiency 23.42) strongly skew Database group statistics. Removing this outlier would improve Database average efficiency.

3. **Low Priority Underpopulated:** Only 2 Low-priority incidents provide insufficient basis for conclusions about that priority tier.

4. **Perfect Correlation Artifact:** The -1.000 correlation between efficiency_score and resolution_hours indicates efficiency is a direct mathematical transformation of resolution duration, not an independent metric.

5. **Temporal Patterns Absent:** Analysis lacks day-of-week or time-of-day effects, which may influence efficiency patterns.

---

## 7. Recommendations for Decision-Making

1. **Database Incident Escalation:** Investigate why Database + Critical incidents resolve poorly (23.42 efficiency). Consider specialized DBA on-call procedures or pre-incident preparation for production scenarios.

2. **Resource Rebalancing for Hardware:** With 405 incidents managed by Hardware group (81% of volume), consider workload distribution strategies or vendor partnerships to improve baseline efficiency from 64.69.

3. **Data Quality Review:** Verify categorization and assignment_group mapping, particularly the Inquiry/Help → Database outlier.

4. **Priority Calibration:** Monitor whether Moderate-priority incidents (15.4% of volume) are appropriately classified; their efficiency parity with High priority suggests possible tier misalignment.

---

## Conclusion

Incident resolution efficiency varies primarily by **resolution duration** and secondarily by **category and priority**. Software and Network incidents achieve the highest efficiency (~70), while Hardware incidents—comprising 81% of the workload—maintain moderate efficiency (64.7) due to inherent complexity and volume. Critical incidents generally perform better than High-priority ones (67.51 vs. 64.97 efficiency), confirming prioritization mechanisms function effectively. The Database + Critical pairing represents the critical performance gap requiring targeted intervention. The "skill_off" designation represents a baseline without specialized skill-based enhancements; comparison with skill-on data would reveal improvement opportunities through skill-aware routing.
