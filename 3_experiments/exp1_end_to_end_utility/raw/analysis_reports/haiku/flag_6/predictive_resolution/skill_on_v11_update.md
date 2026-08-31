---
dataset: flag_6
scenario: predictive_resolution
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary by agent and issue type?"
source_table: augment_table/flag_6/predictive_resolution/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:19:48.307767+00:00
wall_seconds: 56.04
---

# Resolution Time Analysis by Agent and Issue Type

## Overview

This analysis examines how resolution time varies across assigned agents and issue categories in the predictive resolution dataset. The dataset contains 500 incident records; 428 records (85.6%) have valid positive resolution times suitable for analysis.

## Key Findings

### Resolution Time by Agent

**Dramatic variance exists across agents**, with Fred Luddy as a significant outlier:

| Agent | Tickets (n) | Mean (hours) | Median (hours) | Std Dev |
|-------|-------------|--------------|----------------|---------|
| Fred Luddy | 76 | 750.0 | 691.2 | 470.9 |
| Luke Wilson | 90 | 160.2 | 151.3 | 97.0 |
| Howard Johnson | 88 | 159.7 | 142.8 | 99.5 |
| Charlie Whitherspoon | 89 | 150.1 | 150.0 | 100.2 |
| Beth Anglin | 85 | 136.3 | 124.0 | 81.3 |

**Fred Luddy's Performance Issue**: Fred Luddy's mean resolution time is ~4.7× higher than the next-slowest agent (Luke Wilson). Of Fred's 76 tickets, 47 (62%) took longer than 500 hours—extreme outliers. Excluding these outliers, Fred's mean drops to 266 hours, suggesting systematic issues with specific ticket types or a backlog of extremely delayed cases in the dataset.

**Other Agents**: Beth Anglin, Charlie Whitherspoon, Howard Johnson, and Luke Wilson show comparable performance, clustering around 136–160 hours mean resolution time with similar standard deviations (~80–100 hours). These agents resolve tickets in roughly 6–7 days on average.

### Resolution Time by Issue Category

**Issue complexity varies significantly by type**:

| Issue Category | Tickets (n) | Mean (hours) | Median (hours) |
|---|---|---|---|
| Software | 16 | 435.1 | 218.5 |
| Authentication | 8 | 315.1 | 79.3 |
| VPN Connectivity | 99 | 289.5 | 186.1 |
| Database Access | 87 | 247.6 | 140.4 |
| Network Connectivity | 95 | 240.6 | 178.5 |
| Email Server | 115 | 229.8 | 150.1 |
| Hardware | 8 | 180.7 | 186.6 |

**Software and Authentication issues** take longest to resolve (435 and 315 hours respectively), though sample sizes are small (16 and 8 tickets). **Email Server issues** dominate the volume (115 tickets) but resolve faster than network and database issues. Median times are substantially lower than means across categories, indicating right-skewed distributions with occasional long-tail resolutions.

### Agent Performance by Issue Type

**Critical insight**: **Fred Luddy is exceptionally slow across all issue categories**, with mean times typically 5–15 times higher than peers:

- **VPN Connectivity**: Fred (851 hrs) vs. Luke Wilson (147 hrs) – 5.8× difference
- **Database Access**: Fred (716 hrs) vs. Luke Wilson (129 hrs) – 5.5× difference
- **Software**: Fred (1093 hrs) vs. Luke Wilson (316 hrs) – 3.5× difference
- **Authentication**: Fred (1010 hrs) vs. Charlie Whitherspoon (44 hrs) – 23× difference

**Other agents** show reasonable consistency:
- **Beth Anglin** is fastest on authentication (126 hrs) and database access (131 hrs)
- **Luke Wilson** handles VPN and database issues efficiently (147 and 129 hrs respectively)
- **Charlie Whitherspoon** excels on authentication (44 hrs) but takes longer on software issues (192 hrs)
- **Howard Johnson** performs near-peers on most categories except authentication (no tickets recorded)

### Data Quality Issues

**Negative resolution times** (50 records, 10%) suggest data entry errors (closed timestamps before opened timestamps). These are excluded from analysis. **Missing closed/opened times** (22 records) further reduce the analyzable dataset. Fred Luddy's extreme delays warrant investigation—they may represent genuinely complex cases, long wait times due to capacity constraints, or data quality anomalies (e.g., stale tickets).

## Recommendations

1. **Investigate Fred Luddy's backlog**: 47 tickets exceeded 500 hours. Review whether these represent system delays, resource constraints, or data artifacts.
2. **Focus on high-complexity types**: Software and authentication issues show elevated resolution times. Root-cause analysis and targeted training may improve outcomes.
3. **Distribute load strategically**: Beth Anglin and Charlie Whitherspoon demonstrate faster resolution on certain issue types; consider skill-based routing.
4. **Data validation**: Address negative and missing resolution timestamps to improve analysis reliability.

## Limitations

- Small sample sizes for some issue categories (authentication: 8, hardware: 8, software: 16) reduce confidence in category-level conclusions.
- Dataset timeframe (Jan–Mar 2023) is not specified; trends may be temporal.
- Agent skill, issue complexity, and process factors cannot be fully disentangled from this data alone.
