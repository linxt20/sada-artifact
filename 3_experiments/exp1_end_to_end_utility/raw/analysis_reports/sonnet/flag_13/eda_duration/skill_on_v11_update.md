---
dataset: flag_13
scenario: eda_duration
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_duration"
query: "How does resolution duration vary across incident category and priority?"
source_table: augment_table/flag_13/eda_duration/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:14:24.752464+00:00
wall_seconds: 41.78
---

# Resolution Duration by Incident Category and Priority

## Dataset Overview
- **500 closed/resolved incidents** across 6 incident categories and 4 priority levels.
- Resolution duration is encoded in the `closed_at` column as `MM:SS.s` (minutes and seconds).
- Parsed durations range from **0.2 to ~60 minutes**, with an overall mean of **30.1 min** and median of **29.8 min** — a near-uniform spread across the full hour window.

---

## By Priority

| Priority | Mean (min) | Median (min) | Count |
|---|---|---|---|
| 1 - Critical | 30.35 | 32.00 | 83 |
| 2 - High | 29.93 | 29.65 | 391 |
| 3 - Moderate | 31.45 | 29.20 | 24 |
| 4 - Low | 25.00 | 25.00 | 2 |

**Priority has minimal effect on resolution duration.** The differences between Critical, High, and Moderate are within ~1.5 minutes and not practically significant. The "4 - Low" category has only 2 records — too few for reliable inference.

---

## By Incident Category

| Category | Mean (min) | Median (min) | Count |
|---|---|---|---|
| server | 33.77 | 35.43 | 21 |
| network | 31.37 | 31.75 | 72 |
| vpn | 30.35 | 30.32 | 109 |
| database | 29.64 | 30.00 | 136 |
| other | 29.62 | 24.41 | 28 |
| email | 29.02 | 27.13 | 134 |

**Server incidents take the longest** (mean ~34 min), while **email incidents resolve fastest** (mean ~29 min). However, the spread across categories is narrow (~5 minutes mean difference), limiting operational significance.

---

## Interaction: Priority × Incident Category (Mean Duration, minutes)

| Category | 1 - Critical | 2 - High | 3 - Moderate |
|---|---|---|---|
| database | 33.1 | 28.9 | 32.9 |
| email | 25.0 | 30.2 | **39.5** |
| network | **45.2** | 30.7 | 29.1 |
| other | 38.1 | 30.3 | 23.5 |
| server | 39.1 | 32.1 | 25.2 |
| vpn | 36.3 | 30.1 | 24.2 |

**Key interaction patterns:**

- **Network × Critical** stands out most strongly: mean of **45.2 minutes**, notably higher than Network at other priorities (~30 min). However, this cell has only **4 records** — weak evidence.
- **Email × Moderate** shows an elevated mean of **39.5 min** (8 records) vs. email at Critical (25 min) — an unexpected reversal where lower-priority email takes longer. Small sample caveat applies.
- **VPN, Server, and Other** all show a consistent inverse pattern: Critical takes longer than High, which takes longer than Moderate. This could reflect escalation overhead for critical incidents in infrastructure-related categories.
- **Database** shows a more stable profile across priorities (~29–33 min), suggesting more standardized resolution procedures.

---

## Summary

> Resolution duration shows **weak differentiation by priority alone** and **modest differentiation by category** (server highest, email lowest). The most actionable signal is in **priority × category interactions**: Critical-level network and server incidents take measurably longer, but many cross-cells have small sample sizes, warranting caution before drawing firm operational conclusions. The overall duration distribution (0–60 min range, near-uniform) suggests the metric may be capped or artificially bounded in this dataset.
