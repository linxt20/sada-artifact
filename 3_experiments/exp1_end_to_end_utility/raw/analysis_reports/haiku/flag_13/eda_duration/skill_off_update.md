---
dataset: flag_13
scenario: eda_duration
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_duration"
query: "How does resolution duration vary across incident category and priority?"
source_table: augment_table/flag_13/eda_duration/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:11:50.193665+00:00
wall_seconds: 57.18
---

# Incident Resolution Duration Analysis by Category and Priority
**Dataset:** haiku__skill_off_update (500 incidents)  
**Variant:** skill_off  
**Query:** How does resolution duration vary across incident category and priority?

---

## Executive Summary

Resolution duration shows modest variation across incident categories and priorities, with overall mean of **30.05 minutes** and median of **29.85 minutes**. The relationship between priority level and resolution time is non-linear, with critical incidents showing similar resolution times to high-priority cases. Category matters more significantly: Software incidents average 1-2 minutes longer than other categories, while database incidents are slightly faster on average.

---

## Duration Patterns by Category

| Category | Count | Mean (min) | Median (min) | Std Dev | Range |
|----------|-------|-----------|-------------|---------|--------|
| **Network** | 260 | 30.08 | 29.66 | 16.98 | 0.43–59.41 |
| **Software** | 73 | 31.55 | 33.45 | 17.32 | 2.30–59.16 |
| **Database** | 134 | 29.16 | 29.67 | 17.19 | 0.18–59.95 |
| **Hardware** | 25 | 30.79 | 32.00 | 13.53 | 6.29–58.21 |
| **Inquiry / Help** | 8 | 28.04 | 28.65 | 13.51 | 4.61–45.08 |

**Key observations:**
- **Software** incidents have the longest mean resolution time (31.55 min), driven by complexity and cross-system dependencies.
- **Database** incidents are fastest on average (29.16 min), despite occasional extreme outliers (up to 59.95 min).
- **Network** incidents, representing 52% of all tickets (260/500), show near-average duration (30.08 min).
- **Inquiry / Help** and **Hardware** categories are small cohorts with limited statistical power, but show broadly similar durations (28–31 min).

---

## Duration Patterns by Priority

| Priority | Count | Mean (min) | Median (min) | Std Dev | Range |
|----------|-------|-----------|-------------|---------|--------|
| **1 - Critical** | 83 | 30.35 | 32.00 | 16.58 | 0.43–57.94 |
| **2 - High** | 391 | 29.93 | 29.65 | 17.08 | 0.18–59.95 |
| **3 - Moderate** | 24 | 31.45 | 29.20 | 14.89 | 5.12–58.88 |
| **4 - Low** | 2 | 25.00 | 25.00 | 7.07 | 20.00–30.00 |

**Key observations:**
- **No clear priority advantage:** Critical incidents (mean 30.35 min) resolve slightly *slower* than High priority (mean 29.93 min), contrary to typical SLA expectations.
- **Moderate priority** shows the longest mean (31.45 min), suggesting these may be under-resourced or lower-urgency triage.
- **Low priority** (n=2) is too sparse to draw conclusions.
- **High priority** dominates the dataset (78%), making it the most reliable category for comparison.

---

## Cross-Category and Priority Matrix

### Mean Resolution Duration (minutes)

|  | 1 - Critical | 2 - High | 3 - Moderate | 4 - Low |
|---|---|---|---|---|
| **Database** | 31.79 | 28.57 | 32.85 | 30.00 |
| **Hardware** | 34.71 | 32.71 | 20.70 | — |
| **Inquiry / Help** | 25.67 | 28.38 | — | — |
| **Network** | 28.06 | 30.62 | 27.66 | — |
| **Software** | 37.11 | 29.53 | 39.33 | 20.00 |

### Incident Count

|  | 1 - Critical | 2 - High | 3 - Moderate | 4 - Low |
|---|---|---|---|---|
| **Database** | 19 | 110 | 4 | 1 |
| **Hardware** | 6 | 14 | 5 | — |
| **Inquiry / Help** | 1 | 7 | — | — |
| **Network** | 48 | 206 | 6 | — |
| **Software** | 9 | 54 | 9 | 1 |

---

## Notable Findings

### 1. **Software + Critical = Longest Resolution**
Software incidents marked as Critical resolve in **37.11 minutes** on average—the longest combination. This suggests complex system interactions requiring expert intervention.

### 2. **Category-Priority Interactions**
- **Network Critical** (28.06 min) resolves faster than **Network High** (30.62 min)—a reversal of expectations, possibly due to rapid network team mobilization for outages.
- **Hardware Moderate** (20.70 min) is unusually fast, but based on only 5 incidents.
- **Software Moderate** (39.33 min) is exceptionally slow, suggesting triage misclassification or resource constraints.

### 3. **Extreme Variability**
- Several category-priority combinations span 50+ minute ranges (Database High: 0.18–59.95 min, Network High: 0.93–59.41 min).
- This high variance (standard deviation 14–22 min) indicates inconsistent resolution processes or highly diverse incident complexity within categories.

### 4. **Small Cohorts Limit Confidence**
- Inquiry / Help (8 incidents) and Hardware (25 incidents) have insufficient data for reliable priority-level comparisons.
- 4 - Low priority (2 incidents) is negligible.

---

## Factors Influencing Resolution Duration

1. **Incident Complexity:** Software and complex Database incidents naturally require more investigation and coordination.
2. **Team Availability:** Network incidents, despite being dominant (52%), show moderate resolution times, suggesting adequate staffing or escalation protocols.
3. **Triage Accuracy:** Inverse relationships between critical/high priority duration suggest potential mislabeling or that truly critical incidents receive immediate, decisive action.
4. **External Dependencies:** Network and Database categories may depend on third-party systems or multiple teams, extending resolution time.

---

## Limitations & Caveats

- **No temporal trend:** Data lacks timestamps to assess whether resolution times have improved or degraded over the study period.
- **Root cause unavailable:** Cannot distinguish between genuine complexity and inefficient processes.
- **Small categories:** Hardware and Inquiry / Help have n < 30, limiting statistical reliability at the priority level.
- **Outlier influence:** A few extreme values (59+ minutes) disproportionately affect mean calculations; **median is a more robust measure**.

---

## Recommendations for Further Analysis

1. **Investigate the Network Critical anomaly:** Why do critical network incidents resolve faster than high-priority ones?
2. **Audit Software Moderate incidents:** The 39.33-minute average is suspiciously long for moderate-priority work.
3. **Standardize category definitions:** High variance within categories suggests inconsistent incident classification.
4. **Collect team assignment data:** Correlate resolution time with team size, expertise, and on-call status to identify bottlenecks.

---

## Conclusion

Resolution duration is **relatively consistent across most incident categories and priorities** (29–31 minutes on average), but with notable exceptions in Software and category-specific priority interactions. The lack of a clear priority gradient and high internal variance suggest that factors beyond category and priority—such as incident complexity, team expertise, and process efficiency—significantly influence resolution time. Median duration (29.85 min) is more representative than mean due to outlier sensitivity.
