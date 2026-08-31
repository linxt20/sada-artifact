---
dataset: flag_2
scenario: eda_resolution
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary across category, priority, and assignment group?"
source_table: augment_table/flag_2/eda_resolution/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:16:40.090545+00:00
wall_seconds: 94.4
---

# Resolution Time Analysis by Category, Priority, and Assignment Group
**Variant:** skill_off | **Date:** 2026-07-28

## Executive Summary

This analysis examines how IT incident resolution times vary across category, priority level, and assignment group in a dataset of 500 tickets, of which 372 have completed resolution data. The dataset shows moderate variance in resolution times (CV = 0.59), with interesting interactions between dimensions that suggest category-specific workflows.

## Data Overview

- **Total Records:** 500 incidents
- **Records with Resolution Time:** 372 (74.4%)
- **Missing Resolution Time:** 128 records (marked "New" or "In Progress")
- **Resolution Time Range:** 24.0 to 2,205.6 hours (~1 day to ~92 days)
- **Mean Resolution Time:** 1,043.4 hours (~43.5 days)
- **Median Resolution Time:** 1,032.0 hours (~43 days)

### Dimensions Analyzed
- **Categories:** Database, Hardware, Inquiry/Help, Network, Software
- **Priorities:** 1 - Critical, 2 - High, 3 - Moderate
- **Assignment Groups:** Database, Hardware, Network, Service Desk, Software, Openspace

---

## Resolution Time by Category

| Category | Count | Mean (h) | Median (h) | Std Dev | Range |
|----------|-------|----------|-----------|---------|-------|
| **Database** | 86 | 954.98 | 967.2 | 557.19 | 31.2–2,169.6 |
| **Network** | 197 | 1,078.67 | 1,046.4 | 630.00 | 24.0–2,198.4 |
| **Software** | 70 | 1,050.62 | 985.2 | 651.98 | 38.4–2,205.6 |
| **Hardware** | 12 | 1,105.20 | 1,021.2 | 637.02 | 117.6–1,996.8 |
| **Inquiry/Help** | 7 | 957.94 | 686.4 | 674.03 | 110.4–2,018.4 |

### Key Observations by Category

**Database (Fastest Overall)**
- Mean resolution: ~955 hours (~40 days)
- Most predictable category (CV = 0.58)
- Represents 23% of all incidents
- Performance is consistent across assignment groups (handled by dedicated Database teams)

**Network (Slowest Overall, Largest Volume)**
- Mean resolution: ~1,079 hours (~45 days)
- Largest assignment group with 221 incidents (59% of complete dataset)
- Higher variability in outcomes (CV = 0.58)
- Handled by Network team; shows relatively uniform timing across priority levels (~1,043–1,165 hours)
- **Weak evidence:** Priority escalation does not strongly reduce resolution time for Network category

**Software & Hardware**
- Software: ~1,051 hours (70 records)
- Hardware: ~1,105 hours (12 records, small sample)
- Both show high variability (CV = 0.62 and 0.58 respectively)

**Inquiry/Help**
- Smallest category (7 records)
- Highest variability (CV = 0.70)
- Mixed results: one critical case took 1,417 hours; moderate cases averaged only 352 hours
- **Weak evidence:** Small sample size limits confidence in patterns

---

## Resolution Time by Priority

| Priority | Count | Mean (h) | Median (h) | Std Dev |
|----------|-------|----------|-----------|---------|
| **1 - Critical** | 57 | 1,118.65 | 1,255.2 | 624.09 |
| **2 - High** | 283 | 1,019.48 | 974.4 | 600.83 |
| **3 - Moderate** | 32 | 1,120.65 | 1,100.4 | 749.93 |

### Key Observations by Priority

**Counterintuitive Finding: Priority Does Not Strongly Drive Resolution Time**
- **Critical tickets** average 1,119 hours (46.6 days) — *slightly longer* than High priority
- **High priority tickets** average 1,019 hours (42.5 days) — *shortest overall*
- **Moderate tickets** average 1,121 hours (46.7 days) — *similar to Critical*
- **Important caveat:** This may reflect *ticket classification bias* rather than true resolution performance (easier/faster issues might be marked as High priority with shorter resolution times)

**Priority Effect Within Categories**
- **Database:** Priority has clear effect: Critical (1,244h) → High (909.8h) → Moderate (817.4h)
  - Critical cases take 52% longer than Moderate cases
  - Suggests real escalation/complexity differences
- **Network:** Priority effect is *minimal* (1,044h to 1,093h difference)
  - Assignment group handling may be more important than priority
- **Software:** Mixed effect; Moderate cases unexpectedly take 1,233h vs. 976h for High priority

---

## Resolution Time by Assignment Group

| Group | Count | Mean (h) | Median (h) | Std Dev |
|-------|-------|----------|-----------|---------|
| **Database** | 89 | 946.49 | 960.0 | 553.18 |
| **Network** | 221 | 1,074.03 | 1,046.4 | 627.14 |
| **Service Desk** | 32 | 1,102.42 | 1,129.2 | 612.83 |
| **Software** | 25 | 1,028.26 | 823.2 | 733.15 |
| **Hardware** | 4 | 925.80 | 794.4 | 785.77 |
| **Openspace** | 1 | 1,852.80 | — | — |

### Key Observations by Assignment Group

**Database Team (Fastest)**
- Mean: 947 hours (~39 days)
- Most consistent performer (SD = 553)
- Handles 24% of resolved incidents
- Dedicated team focus appears to improve efficiency

**Network Team (Largest, Moderate Performance)**
- Mean: 1,074 hours (~45 days)
- Handles 59% of all resolved incidents
- High volume may contribute to longer cycle times
- No clear priority advantage

**Service Desk (Slowest Dedicated Team)**
- Mean: 1,102 hours (~46 days)
- Only 32 records (8.6% of total)
- Primarily handles Software (30 cases) and Network (2 cases)
- May represent more complex issue routing or escalation delays

**Hardware (Small Sample, Fast)**
- Only 4 records; limited confidence
- Mean: 926 hours (~39 days)
- Similar speed to Database team

**Openspace (Insufficient Data)**
- Only 1 record: 1,853 hours
- Cannot draw conclusions

---

## Cross-Dimensional Patterns

### Category × Priority Interaction

**Database by Priority (Clear hierarchy)**
- Critical: 1,244h → High: 910h → Moderate: 817h
- 52% reduction from Critical to Moderate

**Network by Priority (Flat structure)**
- Ranges only 1,044h to 1,093h (4.7% variation)
- Priority escalation ineffective for Network category

**Software by Priority (Inverted)**
- Critical: 1,257h, High: 976h, Moderate: 1,233h
- Suggests classification or complexity issues

### Category × Assignment Group Alignment

**Ideal Alignment (Single Responsible Team)**
- Database category → Database team: 955h / 946h (matched)
- Network category → Network team: 1,075h / 1,074h (matched)

**Misalignment Issues**
- Software tickets routed to Service Desk: 1,007h (median 823h)
- Software tickets stay with Software team: 913h
- Service Desk adds ~10% overhead for Software tickets

### Priority × Assignment Group Interaction

**Network Team by Priority** (221 records)
- Minimal variation: 1,044h (Critical) to 1,092h (Moderate)
- High volume homogenizes priority effects

**Database Team by Priority** (89 records)
- Strong priority effect: 1,217h (Critical) vs. 818h (Moderate)
- 49% improvement with proper prioritization

**Service Desk by Priority** (32 records)
- Critical: 1,356h
- High: 1,044h
- Moderate: 1,200h
- Service Desk shows inconsistent priority handling

---

## Important Exceptions and Data Quality Notes

### Data Completeness Issue
- **128 of 500 records (25.6%) lack resolution time**
- These are marked as "New" (68) or "In Progress" (60) status
- Analysis based on 372 closed/resolved tickets only
- Results may not reflect true organizational performance

### High Variability
- Overall CV = 0.59 indicates substantial case-by-case variation
- Inquiry/Help category shows highest variability (CV = 0.70)
  - Only 7 cases; one outlier (2,018h) inflates mean
- Software and Hardware also show high variability (CV ≥ 0.58)

### Small Sample Sizes
- Hardware: 12 cases
- Inquiry/Help: 7 cases
- Openspace: 1 case
- **Findings for these categories should be treated as exploratory only**

### Unexpected Priority Pattern
- Critical and Moderate tickets take *longer* than High priority tickets
- **Hypothesis:** Easier issues (High) resolve faster; harder issues (Critical, Moderate) take longer regardless of categorization
- Alternative explanation: priority classification may lag actual issue complexity

---

## Conclusion

Resolution time varies meaningfully across category and assignment group, but shows surprisingly weak correlation with priority level. The **Database team achieves fastest resolution** (~947 hours), while the **Network team handles the largest volume** but at longer average duration (~1,074 hours). Priority escalation is effective *only* for Database tickets (52% reduction from Critical to Moderate), but ineffective for Network category, suggesting that assignment group and issue category are stronger drivers of resolution time than priority level in this dataset.

The `skill_off` variant analysis indicates that without skill-based routing optimization, general assignment groups handle diverse issue types with moderate efficiency. Further investigation into Network team capacity and Service Desk escalation processes may identify opportunities for improvement.

---

**Report Generated:** 2026-07-28 | **Dataset:** haiku__skill_off_update.csv (n=372 complete records)
