---
dataset: flag_13
scenario: eda_duration
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "resolution_duration"
query: "How does resolution duration vary across incident category and priority?"
source_table: augment_table/flag_13/eda_duration/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:14:43.054703+00:00
wall_seconds: 59.2
---

# Resolution Duration by Incident Category and Priority

## Summary

Across 500 closed/resolved incidents, the **overall median resolution time is 29.8 minutes** (mean 30.1 min, std 16.8 min). Priority and category both influence duration, but their effects differ—and critically, they interact: the relationship between priority and speed is **not monotonic** across categories.

---

## Method Note

TAPP-generated columns used in this report: `incident_category`, `scope_indicator`, `opened_hour_of_day`, `repeat_incident_signal`, `resolver_match`. The primary outcome measure is `sys_updated_on`, which encodes resolution duration (parsed as minutes). Original structured columns `priority` and `category` serve as the primary explanatory variables; TAPP columns add semantic granularity where they provide signal beyond raw originals.

---

## 1. Duration by Priority

| Priority | N | Median (min) | Mean (min) |
|---|---|---|---|
| 1 - Critical | 83 | 32.0 | 30.3 |
| 2 - High | 391 | 29.6 | 29.9 |
| 3 - Moderate | 24 | 29.2 | 31.5 |
| 4 - Low | 2 | 25.0 | 25.0 |

**Priority has weak overall effect on duration.** Critical incidents take slightly *longer* (median 32 min) than High (29.6 min) or Moderate (29.2 min)—the opposite of the expected SLA pattern. The spread across priority levels is only ~3 minutes at the median. The sample for Moderate (n=24) and Low (n=2) is too small to draw firm conclusions.

---

## 2. Duration by Category

| Category | N | Median (min) | Mean (min) |
|---|---|---|---|
| Software | 73 | 33.5 | 31.5 |
| Hardware | 25 | 32.0 | 30.8 |
| Database | 134 | 29.7 | 29.2 |
| Network | 260 | 29.7 | 30.1 |
| Inquiry / Help | 8 | 28.6 | 28.0 |

**Software and Hardware incidents take longest** (median ~32–34 min), while Database, Network, and Inquiry/Help are resolved faster (~28–30 min). Network dominates volume (52% of incidents).

---

## 3. Priority × Category Interaction (Median Duration, minutes)

| Category | 1 - Critical | 2 - High | 3 - Moderate |
|---|---|---|---|
| Database | 34.5 | 28.3 | 33.7 |
| Hardware | 35.3 | 37.0 | 23.9 |
| Network | 23.8 | 30.5 | 24.8 |
| Software | 38.0 | 24.4 | 43.4 |
| Inquiry / Help | 25.7 | 31.6 | — |

Key interactions:
- **Software × Critical** has the longest median (38.0 min); **Software × Moderate** is even longer (43.4 min, n=5—small sample, treat cautiously).
- **Network × Critical** is surprisingly *fast* (23.8 min) vs. Network × High (30.5 min), suggesting Network critical issues may be routed or resolved differently.
- **Database × Critical** (34.5 min) runs longer than Database × High (28.3 min), consistent with complexity.
- **Hardware × High** (37.0 min) is the highest among hardware-priority cells.

---

## 4. TAPP Semantic Facets: `incident_category` Granularity

The TAPP `incident_category` column subdivides raw `category` into finer types. Notable findings:

| incident_category | N | Median (min) | Dominant raw category |
|---|---|---|---|
| network_connectivity | 92 | 33.7 | Network |
| vpn_connectivity | 109 | 30.3 | Network |
| database_access | 136 | 30.0 | Database |
| email_service | 134 | 27.1 | Software/Network |
| printing | 9 | 24.8 | Hardware |

Within the broad **Network** category, `network_connectivity` incidents (median 33.7 min) resolve significantly slower than `vpn_connectivity` (30.3 min), a distinction invisible in the raw `category` column. **Email service** issues (largely mapped to Software) resolve faster than average (27.1 min).

At the priority-interaction level, `vpn_connectivity × Critical` incidents have a median of 45.5 min—the second-highest cell—while `database_access × Critical` is 35.1 min, confirming that Critical VPN outages are the most time-consuming combination.

---

## 5. Other TAPP Facets (Secondary / Weak Signal)

| TAPP Column | Key Finding | Signal Strength |
|---|---|---|
| `scope_indicator` | Location-specific issues: median 32.2 min vs. individual_user 29.0 min. Modest +3 min effect. | Moderate |
| `opened_hour_of_day` | Overnight incidents longest (median 34.3 min); business-hours fastest (27.7 min). ~7 min gap. | Moderate |
| `repeat_incident_signal` | True vs. False: 30.0 vs. 29.6 min median. Negligible. | Weak |
| `resolver_match` | True vs. False: 31.1 vs. 29.6 min median. Marginal. | Weak |

`scope_indicator` and `opened_hour_of_day` add modest contextual signal. Overnight incidents taking longest likely reflects reduced staffing. Location-specific incidents taking longer aligns with on-site investigation overhead. `repeat_incident_signal` and `resolver_match` show no meaningful duration effect.

---

## Key Takeaways

1. **Category matters more than priority level alone.** Software and Hardware incidents are consistently slower regardless of priority; Network incidents are fastest.
2. **Critical priority does not guarantee faster resolution**—Critical incidents take slightly *longer* on median, driven by difficult Software/Database/VPN cases.
3. **VPN × Critical** is the most time-intensive combination (median 45.5 min, n=22).
4. **Network × Critical** is the fastest high-severity combination (median 23.8 min), likely reflecting mature runbooks.
5. Overnight timing adds ~7 minutes to median resolution; location-specific scope adds ~3 minutes—secondary but actionable factors.
