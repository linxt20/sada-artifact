---
dataset: flag_13
scenario: eda_duration
variant: original
model: substrate-claude-haiku-4-5
query_subtype: exploratory_data_analysis
focus_variable: "resolution_duration"
query: "How does resolution duration vary across incident category and priority?"
source_table: augment_table/flag_13/eda_duration/original.csv
generated_at: 2026-07-26T13:17:30.144877+00:00
wall_seconds: 61.77
---

# Resolution Duration Analysis by Incident Category and Priority

## Overview

This analysis examines how resolution duration varies across incident categories and priority levels in a dataset of 500 service desk incidents. Resolution duration is measured in minutes, ranging from approximately 0.2 to 60 minutes, with a mean of **30.05 minutes** and median of **29.85 minutes**.

## Duration by Incident Category

Incident categories show modest variation in average resolution duration:

| Category | Count | Mean Duration (min) | Median | Std Dev |
|----------|-------|---------------------|--------|---------|
| **Software** | 73 | **31.55** | 33.45 | 17.32 |
| **Hardware** | 25 | 30.79 | 32.00 | 13.53 |
| **Network** | 260 | 30.08 | 29.66 | 16.98 |
| **Database** | 134 | 29.16 | 29.67 | 17.19 |
| **Inquiry / Help** | 8 | 28.04 | 28.65 | 13.51 |

**Key Findings:**
- Software incidents take longest to resolve (31.55 min average), approximately 11% longer than Inquiry/Help tickets (28.04 min).
- Network incidents represent the largest category (52% of dataset, n=260), with average resolution duration of 30.08 minutes—close to the overall mean.
- Inquiry/Help tickets (n=8) resolve fastest, though this category has minimal representation.
- The differences between categories are relatively small (~3.5 minutes across the range), suggesting category alone is not a strong duration predictor.

## Duration by Priority Level

Priority levels show clearer patterns, though with uneven distribution:

| Priority | Count | Mean Duration (min) | Median | Std Dev |
|----------|-------|---------------------|--------|---------|
| **3 - Moderate** | 24 | **31.45** | 29.20 | 14.89 |
| **1 - Critical** | 83 | 30.35 | 32.00 | 16.58 |
| **2 - High** | 391 | 29.93 | 29.65 | 17.08 |
| **4 - Low** | 2 | 25.00 | 25.00 | 7.07 |

**Key Findings:**
- Moderate priority incidents resolve **slowest** (31.45 min), contrary to typical expectations.
- Critical priority incidents (1 - Critical) resolve slightly faster (30.35 min) but not dramatically so.
- High priority incidents (2 - High) dominate the dataset (78.2%, n=391) and average 29.93 minutes.
- Low priority incidents (n=2) have lowest duration, though sample size is negligible.
- The difference between fastest and slowest categories is ~6.5 minutes, modest in absolute terms.

## Combined Category × Priority Analysis

The cross-tabulation reveals interaction patterns:

**Mean Resolution Duration by Category and Priority (minutes):**

| Category | 1 - Critical | 2 - High | 3 - Moderate | 4 - Low |
|----------|-------------|----------|--------------|---------|
| **Software** | 37.11 | 29.53 | 39.33 | 20.0 |
| **Database** | 31.79 | 28.57 | 32.85 | 30.0 |
| **Hardware** | 34.71 | 32.71 | 20.70 | — |
| **Network** | 28.06 | 30.62 | 27.66 | — |
| **Inquiry / Help** | 25.67 | 28.38 | — | — |

**Notable Patterns:**
- **Software + 3-Moderate** shows longest durations (39.33 min), suggesting complex software issues at moderate priority may have lower resolution priority in workqueues.
- **Hardware + 3-Moderate** resolves fastest (20.70 min), indicating straightforward hardware problems.
- **Network incidents** consistently resolve faster across priorities (27.66–30.62 min range), suggesting more standardized troubleshooting procedures.
- **Critical software incidents** (37.11 min) take notably longer than critical incidents in other categories, suggesting inherent complexity.

## Data Limitations

- **Severe class imbalance**: High priority incidents represent 78% of cases; Low priority only 0.4% (n=2)
- **Small categories**: Inquiry/Help (1.6%) and Hardware (5%) have limited sample sizes
- **Weak priority signal**: Moderate priority paradoxically shows highest duration, potentially reflecting workload prioritization rather than intrinsic difficulty
- **Moderate effect sizes**: Category differences (~3.5 min) and priority differences (~6.5 min) are small relative to overall standard deviation (~17 min)

## Conclusions

1. **Resolution duration is relatively stable across categories** (28–32 min range), with Software incidents taking marginally longer. Category is not a strong predictor alone.

2. **Priority level shows counterintuitive patterns**: Moderate priority tickets resolve slower than Critical, likely reflecting actual ticket queue management rather than inherent complexity.

3. **Software complexity drives duration variance**: Software incidents combined with Critical or Moderate priority show longest durations (37–39 min), while Network and Inquiry/Help tickets resolve predictably faster.

4. **Practical insight**: Duration variation is driven more by incident complexity (visible in Software outliers) than formal priority classification. The dataset may benefit from subclassifying incidents by technical area rather than relying on self-assigned priority.
