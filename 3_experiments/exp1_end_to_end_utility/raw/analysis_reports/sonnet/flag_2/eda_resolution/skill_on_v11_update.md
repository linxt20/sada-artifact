---
dataset: flag_2
scenario: eda_resolution
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary across category, priority, and assignment group?"
source_table: augment_table/flag_2/eda_resolution/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:16:37.516596+00:00
wall_seconds: 42.1
---

# Resolution Time Analysis: Category, Priority, and Assignment Group

**Dataset:** 500 incidents | **Resolved/Closed with timestamps:** 372 (128 records lack a `closed_at` value and are excluded from timing calculations)

---

## Key Metric

Resolution time is derived from `closed_at − opened_at` (hours).

| Statistic | Value (hours) |
|-----------|--------------|
| Mean | 1,043 |
| Median | 1,032 |
| Min | 24 |
| Max | 2,206 |
| Std Dev | 618 |

The distribution is broad (~1–92 days), suggesting meaningful variation across the grouping factors.

---

## 1. Resolution Time by Category

| Category | Mean (hrs) | Median (hrs) | Count |
|---|---|---|---|
| Hardware | 1,105 | 1,021 | 12 |
| Network | 1,079 | 1,046 | 197 |
| Software | 1,051 | 985 | 70 |
| Database | 955 | 967 | 86 |
| Inquiry / Help | 958 | 686 | 7 |

**Findings:**
- **Hardware** and **Network** incidents take the longest on average (~1,080–1,105 hrs).
- **Database** and **Inquiry / Help** resolve fastest (mean ~955–958 hrs), with Inquiry / Help showing the lowest median (686 hrs), suggesting a subset resolves quickly.
- The absolute spread across categories is ~150 hrs mean-to-mean — moderate but not dramatic.
- **Caution:** Hardware (n=12) and Inquiry / Help (n=7) have very small sample sizes; conclusions for these categories are weak.

---

## 2. Resolution Time by Priority

| Priority | Mean (hrs) | Median (hrs) | Count |
|---|---|---|---|
| 2 - High | 1,019 | 974 | 283 |
| 1 - Critical | 1,119 | 1,255 | 57 |
| 3 - Moderate | 1,121 | 1,100 | 32 |

**Findings:**
- Counterintuitively, **1 - Critical** and **3 - Moderate** incidents take *longer* on average than **2 - High** tickets.
- Critical incidents have a high median (1,255 hrs) vs. High's 974 hrs — suggesting critical tickets are not expedited faster in practice.
- This may reflect that "Critical" incidents are harder or more complex, or that priority labeling is not strictly tied to SLA enforcement in this dataset.
- **2 - High** dominates the volume (283 of 372 resolved incidents), making it the most reliable estimate.

---

## 3. Resolution Time by Assignment Group

| Assignment Group | Mean (hrs) | Median (hrs) | Count |
|---|---|---|---|
| Openspace | 1,853 | 1,853 | 1 |
| Service Desk | 1,102 | 1,129 | 32 |
| Network | 1,074 | 1,046 | 221 |
| Software | 1,028 | 823 | 25 |
| Database | 946 | 960 | 89 |
| Hardware | 926 | 794 | 4 |

**Findings:**
- **Database** and **Hardware** groups resolve incidents fastest (mean ~926–946 hrs, medians ~794–960 hrs).
- **Network** group handles the bulk of incidents (221) and sits at a mid-tier resolution speed (mean 1,074 hrs).
- **Service Desk** is notably slower (mean 1,102 hrs, median 1,129 hrs) despite presumably handling routed/escalated tickets.
- **Openspace** (n=1) shows the highest value at 1,853 hrs — treat as an outlier with no statistical weight.

---

## 4. Category × Priority Interaction

| Category | 1 - Critical | 2 - High | 3 - Moderate |
|---|---|---|---|
| Database | 1,244 | 910 | 817 |
| Hardware | 1,298 | 1,010 | 1,435 |
| Inquiry / Help | 1,417 | 1,056 | 352 |
| Network | 1,039 | 1,082 | 1,211 |
| Software | 1,257 | 976 | 1,233 |

**Findings:**
- Within **Database** and **Software**, Critical incidents take substantially longer than High (~300+ hrs difference), consistent with complexity driving up both priority and time.
- **Network** Critical incidents (1,039 hrs) are actually *faster* than Moderate ones (1,211 hrs) — an exception worth noting.
- **Inquiry / Help + Moderate** resolves very quickly (352 hrs median equivalent), suggesting routine requests close swiftly when not critical.

---

## Summary

| Factor | Effect on Resolution Time |
|---|---|
| Category | Hardware/Network slowest; Database fastest — ~150 hr spread |
| Priority | No monotonic SLA enforcement; Critical ≠ fastest; High resolves quickest |
| Assignment Group | Database/Hardware teams fastest; Service Desk slowest among staffed groups |

**Key decision insight:** The absence of a priority-speed relationship (Critical not faster than High) is the most actionable finding — it suggests SLA policies for Critical tickets may need reinforcement. Database and Hardware assignment groups demonstrate best practice resolution speed and could serve as benchmarks.
