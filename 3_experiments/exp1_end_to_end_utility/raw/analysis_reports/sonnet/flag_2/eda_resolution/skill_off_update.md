---
dataset: flag_2
scenario: eda_resolution
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary across category, priority, and assignment group?"
source_table: augment_table/flag_2/eda_resolution/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:15:54.370679+00:00
wall_seconds: 46.98
---

# Resolution Time Analysis: Category, Priority, and Assignment Group

## Dataset Overview

- **Total tickets:** 500
- **Resolved tickets:** 372 (74.4%); 128 tickets have `is_resolved = 0` and carry a sentinel value of −1 for `resolution_time_hours`
- **All resolution-time statistics below are computed on resolved tickets only** to avoid distortion from the −1 sentinel

---

## 1. Resolution Time by Category

| Category | Mean (hrs) | Median (hrs) | Count |
|---|---|---|---|
| Hardware | 1,105.2 | 1,021.2 | 12 |
| Network | 1,078.7 | 1,046.4 | 197 |
| Software | 1,050.6 | 985.2 | 70 |
| Inquiry / Help | 957.9 | 686.4 | 7 |
| Database | 955.0 | 967.2 | 86 |

**Key findings:**
- **Hardware** tickets take the longest on average (~1,105 hrs ≈ 46 days), though the sample is small (n = 12), making this estimate weak evidence.
- **Network** is the dominant category by volume (n = 197) and has the second-highest mean (~1,079 hrs), pulling the overall average significantly.
- **Database** and **Inquiry / Help** resolve ~13–14% faster than Network/Hardware on average.
- Mean–median gaps for all categories are modest except **Inquiry / Help** (mean 958 hrs vs. median 686 hrs), suggesting a right-skewed tail in that small group.

---

## 2. Resolution Time by Priority

| Priority | Mean (hrs) | Median (hrs) | Count |
|---|---|---|---|
| 3 - Moderate | 1,120.7 | 1,100.4 | 32 |
| 1 - Critical | 1,118.7 | 1,255.2 | 57 |
| 2 - High | 1,019.5 | 974.4 | 283 |

**Key findings:**
- **Counter-intuitively, Critical (P1) tickets do not resolve faster than Moderate (P3) tickets**; both average ~1,119–1,121 hrs. This is a notable anomaly.
- **High (P2)** priority tickets resolve meaningfully faster (~1,019 hrs mean, ~974 hrs median), roughly 9–12% quicker than either P1 or P3.
- The median for Critical is **1,255 hrs** — higher than its mean — indicating a left-skewed or heavy-right-tail distribution, meaning a subset of Critical tickets are held open for very long periods.
- The bulk of tickets (n = 283) are classified as High priority, which anchors the overall mean.

> **Caveat:** The absence of a monotonic Priority → Resolution Time relationship is a red flag; it may reflect escalation handling, data quality issues, or SLA policies not captured in the table.

---

## 3. Resolution Time by Assignment Group

| Assignment Group | Mean (hrs) | Median (hrs) | Count |
|---|---|---|---|
| Openspace | 1,852.8 | 1,852.8 | 1 |
| Service Desk | 1,102.4 | 1,129.2 | 32 |
| Network | 1,074.0 | 1,046.4 | 221 |
| Software | 1,028.3 | 823.2 | 25 |
| Database | 946.5 | 960.0 | 89 |
| Hardware | 925.8 | 794.4 | 4 |

**Key findings:**
- **Openspace** has the longest resolution time (~1,853 hrs), but with only 1 ticket it is an outlier, not a reliable group-level signal.
- **Service Desk** is the second-slowest group (~1,102 hrs), potentially because it handles escalated or unrouted tickets before specialist assignment.
- **Network** group (n = 221, largest) resolves at ~1,074 hrs — consistent with the Network category average, as most tickets are co-assigned.
- **Database** and **Hardware** groups are the fastest (~946 and ~926 hrs respectively), though Hardware's n = 4 limits confidence.
- The **Software** group shows a notable mean–median gap (1,028 vs. 823 hrs), suggesting a few long-tail tickets inflate the mean.

---

## 4. Summary and Decision-Ready Takeaways

| Factor | Direction | Strength of Evidence |
|---|---|---|
| Hardware category slowest | ~15% above average | Weak (n = 12) |
| Network category high volume + high time | Dominant cost driver | Strong (n = 197) |
| P1 Critical NOT faster than P3 Moderate | Anomalous — warrants investigation | Moderate (n = 57 vs. 32) |
| P2 High resolves fastest | ~9% below P1/P3 | Strong (n = 283) |
| Service Desk group slower than specialist groups | ~10–16% slower | Moderate (n = 32) |
| Database group resolves faster | ~12% below Network | Strong (n = 89) |

**Priority inversion** (Critical ≈ Moderate > High) is the most actionable finding: it suggests SLA enforcement or routing rules for Critical tickets may need review.
