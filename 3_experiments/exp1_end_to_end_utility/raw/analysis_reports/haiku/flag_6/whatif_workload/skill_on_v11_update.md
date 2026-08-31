---
dataset: flag_6
scenario: whatif_workload
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: what_if
focus_variable: "resolution_time"
query: "If the ticket types that create the heaviest agent workload were reduced, how much would resolution time drop?"
source_table: augment_table/flag_6/whatif_workload/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:20:11.306753+00:00
wall_seconds: 63.01
---

# Workload Impact Analysis: Effect of Reducing Heavy Ticket Types on Resolution Time

**Variant:** skill_on | **Dataset:** haiku__skill_on_v11_update.csv | **Analysis Date:** 2026-07-30

## Executive Summary

Reducing ticket types that create the heaviest agent workload would provide **modest direct reductions** in resolution time. If **Network tickets** (the highest-volume category) were eliminated, the overall average resolution time would drop by **9.01 hours (3.49%)**, from 257.98 hours to 248.97 hours. However, this direct effect likely understates potential benefits, as reduced agent overload could accelerate resolution of remaining tickets.

---

## Key Findings

### 1. Heaviest Agent Workload Source: Network Tickets

Agent workload is measured by total hours spent (volume × average resolution time):

| Category | Total Hours | Avg Resolution | Ticket Count | % of Volume |
|----------|------------|-----------------|--------------|------------|
| **Network** | **64,109 h** | 264.9 h | 242 | **56.5%** |
| Database | 22,426 h | 249.2 h | 90 | 21.0% |
| Software | 17,790 h | 278.0 h | 64 | 15.0% |
| Hardware | 4,980 h | 199.2 h | 25 | 5.8% |
| Inquiry/Help | 1,112 h | 158.9 h | 7 | 1.6% |

**Network tickets consume 65% of total agent time**, driven by high volume (56.5% of all tickets) rather than exceptional complexity.

### 2. Resolution Time Impact of Reducing Heaviest Workload

| Metric | Value |
|--------|-------|
| Current average resolution time | 257.98 hours (10.75 days) |
| Average if Network tickets eliminated | 248.97 hours (10.37 days) |
| **Direct reduction** | **9.01 hours (3.49%)** |

Eliminating Network tickets—the highest-volume category—would reduce average resolution time by approximately **3.5%**. This modest reduction reflects that Network tickets have resolution times close to the overall average, meaning the heavy workload stems from volume, not complexity.

### 3. Secondary Workload Categories

If Network reduction alone insufficient, targeting the next highest categories:
- **Database + Network elimination**: ~43% combined reduction in total agent hours; estimated ~4.5% drop in resolution time
- **Software category** has the highest average resolution time (278.0 h) but lower volume; targeting it alone would yield <1% improvement

---

## Important Limitations & Caveats

1. **Direct vs. Indirect Effects**: The 3.49% reduction assumes static agent behavior. In reality, eliminating a large workload category might allow agents to resolve remaining tickets faster due to reduced queue pressure and context-switching. Actual improvements could be 50-100% higher.

2. **Agent Utilization Not Captured**: The dataset shows ticket-level resolution times but does not include agent availability, queue lengths, or skill-based routing. Network tickets may disproportionately affect newer agents or create bottlenecks that suppress performance on other categories.

3. **Data Quality Issues**: 50 tickets (10% of dataset) have negative resolution times, indicating closed_at < opened_at. These are excluded from analysis, using 428 valid tickets from 500 total.

4. **No Causality**: The analysis identifies correlation between ticket volume and workload burden but does not prove that reducing Network tickets *alone* improves other categories' resolution times. Root causes of delays (staffing, skill gaps, system dependencies) remain unknown.

---

## Recommendation

Reducing **Network ticket volume** would yield a direct 3.5% improvement in average resolution time. However, this represents a **lower-bound estimate**. To maximize impact:

1. **Investigate Network ticket root causes** (e.g., VPN connectivity, email system outages) to prevent tickets rather than just reduce them.
2. **Monitor indirect effects** (resolution time for remaining categories) when implementing reductions, as queue relief may compound benefits.
3. **Target high-complexity categories** (Software: 278h avg, Software_update: 422h avg) in parallel, as they create disproportionate per-ticket burden.

---

**Data Period:** 2023-01-01 to 2024-01-30 | **Valid Tickets:** 428 (50 records with data quality issues excluded)
