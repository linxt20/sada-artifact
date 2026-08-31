---
dataset: flag_12
scenario: eda_efficiency
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_efficiency"
query: "How does incident resolution efficiency vary across category, priority, and assignment group?"
source_table: augment_table/flag_12/eda_efficiency/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:13:32.545258+00:00
wall_seconds: 43.19
---

# Incident Resolution Efficiency Analysis

**Dataset:** 500 incidents | **Date range:** 2023 | **Focus variable:** Resolution time (hours from `opened_at` to `closed_at`)

---

## Overview

The overall mean resolution time is **178 hours (~7.4 days)**, with a median of **173 hours**. Resolution times range from 24 h to 514 h (std ≈ 109 h), indicating meaningful dispersion driven by category, priority, and assignment group.

---

## 1. By Category

| Category | Mean (h) | Median (h) | Count |
|---|---|---|---|
| Software | **153.6** | 148.0 | 33 |
| Network | 161.6 | 186.4 | 22 |
| Database | 172.4 | 177.6 | 19 |
| Hardware | 181.4 | 175.4 | **406** |
| Inquiry / Help | 182.1 | 182.7 | 20 |

**Key finding:** Software incidents resolve ~18% faster than the dataset average and ~28 hours faster than Hardware. Hardware dominates volume (81% of tickets), so its slow mean pulls the overall average. Network's mean (161.6 h) is deceptively close to Software but its median (186.4 h) signals right-skewed outliers. Inquiry/Help is consistently the slowest category by both mean and median.

> ⚠️ **Weak evidence caveat:** Non-Hardware categories each have ≤33 incidents, making category-level comparisons statistically fragile.

---

## 2. By Priority

| Priority | Mean (h) | Median (h) | Count |
|---|---|---|---|
| 4 - Low | **32.6** | 32.6 | 2 |
| 1 - Critical | 167.0 | 164.7 | 27 |
| 3 - Moderate | 177.8 | 164.2 | 77 |
| 2 - High | 180.0 | 176.6 | 394 |

**Key finding:** Priority does not reliably predict faster resolution in this dataset. Counter-intuitively, **Critical incidents resolve faster than High or Moderate** (167 h vs. 180 h mean). Low-priority has only 2 records and should be treated as anecdotal. The bulk of volume sits at High priority (394 tickets), which also posts the slowest mean among the three significant tiers.

**Cross-tab insight (Priority × Category):** The anomaly is partly explained by composition—Critical incidents in Software resolve in just 24 hours, while Critical Database incidents average 393.6 hours, suggesting Database escalations are unusually protracted. Network at Moderate priority resolves fastest (136.8 h mean).

---

## 3. By Assignment Group

| Assignment Group | Mean (h) | Median (h) | Count |
|---|---|---|---|
| Software | **153.6** | 148.0 | 33 |
| Network | 161.6 | 161.1 | 23 |
| Service Desk | 176.4 | 179.5 | 19 |
| Database | 178.3 | 178.9 | 20 |
| Hardware | 181.5 | 175.6 | 405 |

Assignment groups closely mirror category distributions (likely because tickets are routed by category). The **Software group is the most efficient** (~28 hours faster than Hardware). The **Hardware group handles 81% of volume** at the slowest mean resolution time, representing the single largest efficiency bottleneck in the system.

---

## 4. Reassignment & Resolution Action Type

**Reassignment:** Reassigned incidents take marginally longer on average (180.9 h vs. 174.9 h for non-reassigned), but the medians are reversed (169.6 h vs. 180.2 h), suggesting reassignment does not systematically worsen outcomes and the effect is not decisive.

**Resolution action type:**

| Action | Mean (h) | Count |
|---|---|---|
| update_install | **158.2** | 38 |
| investigation | 167.0 | 67 |
| replacement | 170.5 | 19 |
| repair | 182.7 | 356 |
| configuration | 186.2 | 20 |

Repair (the most common action at 71% of tickets) is among the slowest resolution types. Update/install and investigation resolve ~15–25 hours faster, reinforcing that Hardware-heavy repair workflows drive the overall slow mean.

---

## Summary & Decision Signals

| Dimension | Fastest | Slowest | Gap |
|---|---|---|---|
| Category | Software (154 h) | Inquiry/Help (182 h) | ~28 h |
| Priority | Critical (167 h) | High (180 h) | ~13 h |
| Assignment Group | Software (154 h) | Hardware (182 h) | ~28 h |

1. **Hardware/repair backlog is the primary efficiency gap** — it represents 80%+ of volume and resolves slowest.
2. **Priority escalation is not working as expected** — Critical tickets resolve faster than High/Moderate, but this may reflect selection bias (Critical incidents get immediate attention or are simpler in non-Database categories).
3. **Database Critical incidents are a major outlier** (393.6 h mean), warranting targeted investigation.
4. Cross-category sample sizes are small; findings outside Hardware should be interpreted directionally rather than conclusively.
