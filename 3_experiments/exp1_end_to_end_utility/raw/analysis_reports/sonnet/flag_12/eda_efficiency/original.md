---
dataset: flag_12
scenario: eda_efficiency
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: exploratory_data_analysis
focus_variable: "resolution_efficiency"
query: "How does incident resolution efficiency vary across category, priority, and assignment group?"
source_table: augment_table/flag_12/eda_efficiency/original.csv
generated_at: 2026-07-26T13:15:03.452433+00:00
wall_seconds: 93.12
---

# Incident Resolution Efficiency Analysis
**Dataset:** `original.csv` — 500 incidents (all Closed or Resolved), January 2023  
**Focus variable:** Resolution time (hours from `opened_at` to `closed_at`)

---

## Overall Distribution

| Metric | Value |
|---|---|
| Mean resolution time | **178.4 h** (~7.4 days) |
| Median resolution time | **173.2 h** (~7.2 days) |
| Std. deviation | 108.7 h |
| Min / Max | 24.0 h / 514.0 h |

Resolution times are roughly symmetric around the median but with a long right tail, indicating a subset of incidents that take significantly longer to close.

---

## By Category

| Category | Mean (h) | Median (h) | Count |
|---|---|---|---|
| Software | **153.6** | 148.0 | 33 |
| Network | 161.6 | 186.4 | 22 |
| Database | 172.4 | 177.6 | 19 |
| Hardware | 181.4 | 175.4 | **406** |
| Inquiry / Help | 182.1 | 182.7 | 20 |

- **Software** is the fastest category by both mean and median, resolving ~28 hours (≈1.2 days) quicker than the overall mean.
- **Hardware** dominates volume (81 % of incidents) and sits slightly above the overall mean, pulling the dataset average upward.
- **Network** shows a noteworthy mean–median gap (161.6 h mean vs. 186.4 h median), suggesting a few very fast resolutions skew the mean down while the typical Network case is actually slower than average.
- Differences across categories are moderate (~30 h range) rather than dramatic; category alone is not a strong differentiator given how heavily Hardware dominates.

---

## By Priority

| Priority | Mean (h) | Median (h) | Count |
|---|---|---|---|
| 1 - Critical | **167.0** | 164.7 | 27 |
| 2 - High | 180.0 | 176.6 | 394 |
| 3 - Moderate | 177.8 | 164.2 | 77 |
| 4 - Low | **32.6** | 32.6 | 2 |

- **Critical (P1)** incidents resolve faster on average than High (P2) or Moderate (P3), consistent with expected escalation behavior—though the margin is small (~13 h vs. P2).
- **High (P2)** is actually the slowest tier despite its urgency ranking, likely because it carries the largest volume (79 % of tickets) and includes complex Hardware cases.
- **Low (P4)** shows extremely fast resolution (mean 32.6 h), but with only **2 incidents** this observation is statistically unreliable and should not drive conclusions.
- The near-identical means for P2 (180 h) and P3 (178 h) suggest priority is not consistently enforced as an efficiency driver in this dataset—a potential process concern.

---

## By Assignment Group

| Assignment Group | Mean (h) | Median (h) | Count |
|---|---|---|---|
| Software | **153.6** | 148.0 | 33 |
| Network | 161.6 | 161.1 | 23 |
| Service Desk | 176.4 | 179.5 | 19 |
| Database | 178.3 | 178.9 | 20 |
| Hardware | 181.5 | 175.6 | 405 |

- **Software** and **Network** groups are the most efficient, resolving incidents ~28–20 h faster than the overall mean.
- **Hardware** group, handling the vast majority of tickets, is the least efficient on average—but because it dominates volume, its performance sets the baseline for the overall metric.
- **Service Desk** sits near the global mean, consistent with its role as a general intake/triage group.
- Assignment group results closely mirror category results because routing is largely category-aligned (e.g., Hardware category → Hardware group in nearly all cases).

---

## Cross-Dimensional Highlights

| Priority | Category | Mean (h) | Note |
|---|---|---|---|
| 1 - Critical | Software | 24.0 | Single incident — fastest observed |
| 1 - Critical | Database | 393.6 | Single incident — significant outlier |
| 4 - Low | Hardware | 41.3 | Only 2 Low-priority records total |
| 3 - Moderate | Software | 106.2 | Notably faster than P2 Software (163 h) |

- The **Critical Database** incident (393.6 h) is a clear outlier and drags the Database group's Critical-priority average substantially; it warrants individual investigation.
- **Software at P3-Moderate** resolves faster than Software at P2-High, an anomaly that may reflect ticket misclassification or batch closure behavior.

---

## Key Takeaways

1. **Software** is consistently the fastest category and assignment group regardless of priority.
2. **Priority does not reliably predict resolution speed**—P2 High is slower than P1 Critical but nearly identical to P3 Moderate, suggesting priority assignment or enforcement gaps.
3. **Hardware volume dominance** (>80 % of tickets) means organizational efficiency is essentially determined by Hardware group performance.
4. **Outliers matter**: a single Critical Database incident (≈394 h) and the very small P4-Low sample limit conclusions in those cells.
5. Cross-group variation is moderate (≈30 h range among main groups), so no single dimension fully explains resolution time differences—multi-factor investigation (agent workload, incident complexity) is warranted.
