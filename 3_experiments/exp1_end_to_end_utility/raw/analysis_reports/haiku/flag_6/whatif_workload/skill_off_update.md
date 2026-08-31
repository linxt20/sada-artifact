---
dataset: flag_6
scenario: whatif_workload
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: what_if
focus_variable: "resolution_time"
query: "If the ticket types that create the heaviest agent workload were reduced, how much would resolution time drop?"
source_table: augment_table/flag_6/whatif_workload/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:22:13.746344+00:00
wall_seconds: 59.5
---

# Analysis Report: Impact of Reducing Heavy Workload Categories on Resolution Time

**Dataset:** haiku__skill_off_update.csv (skill_off variant)  
**Query:** "If the ticket types that create the heaviest agent workload were reduced, how much would resolution time drop?"  
**Focus Variable:** resolution_time  
**Analysis Date:** 2026-07-28

---

## Executive Summary

Reducing heavy workload ticket categories (Network and Database) would produce **modest gains in resolution time**—a **3.6% decrease in mean resolution time** (9.2 hours) and a **5.5% decrease in median resolution time** (9.1 hours). While these categories represent **77.6% of ticket volume**, their resolution times are not substantially different from lighter categories, limiting the causal impact on overall resolution speed.

---

## Data Overview

- **Total valid tickets (with complete resolution timestamps):** 428 tickets
- **Time period:** January 2023 – February 2024
- **Baseline mean resolution time:** 257.98 hours (10.75 days)
- **Baseline median resolution time:** 164.04 hours (6.83 days)

---

## Heavy vs. Light Workload Categorization

### Heavy Workload Categories (Identified Treatment Levers)

| Category  | Ticket Count | % of Volume | Mean Resolution (hrs) | Median Resolution (hrs) |
|-----------|--------------|-------------|----------------------|------------------------|
| **Network**   | 242          | 56.5%       | 250.81                | 157.80                 |
| **Database**  | 90           | 21.0%       | 253.56                | 170.44                 |
| **Subtotal**  | **332**      | **77.6%**   | **260.65**            | **165.42**             |

**Drivers:** Network connectivity (VPN, WiFi, internet) and Database access issues dominate agent workload due to high repetition and impact scope.

### Light Workload Categories (Baseline Comparison)

| Category        | Ticket Count | % of Volume | Mean Resolution (hrs) | Median Resolution (hrs) |
|-----------------|--------------|-------------|----------------------|------------------------|
| **Software**    | 70           | 16.4%       | 268.03                | 162.46                 |
| **Hardware**    | 24           | 5.6%        | 192.60                | 134.86                 |
| **Inquiry/Help**| 2            | 0.4%        | 88.61                 | 88.61                  |
| **Subtotal**    | **96**       | **22.4%**   | **248.77**            | **154.98**             |

---

## What-If Analysis: Resolution Time Impact

### Scenario 1: Complete Elimination of Heavy Workload Categories

**Assumption:** Network and Database tickets reduced to zero (100% reduction).

| Metric | Baseline | After Reduction | Delta | % Change |
|--------|----------|-----------------|-------|----------|
| **Mean Resolution Time** | 257.98 hrs | 248.77 hrs | -9.22 hrs | -3.6% |
| **Median Resolution Time** | 164.04 hrs | 154.98 hrs | -9.06 hrs | -5.5% |
| **Remaining Ticket Volume** | 428 | 96 | -332 | -77.6% |

**Key Finding:** Despite removing **77.6% of tickets**, the overall resolution time drops by only **3.6%** on average. This indicates that heavy workload categories do not have proportionally longer resolution times than light workload categories.

### Scenario 2: 50% Reduction in Heavy Workload Categories

**Assumption:** Network and Database tickets reduced by half (166 tickets eliminated).

| Metric | Baseline | After Reduction | Delta | % Change |
|--------|----------|-----------------|-------|----------|
| **Mean Resolution Time** | 257.98 hrs | 249.91 hrs | -8.07 hrs | -3.1% |
| **Remaining Tickets** | 428 | 262 | -166 | -38.8% |

**Key Finding:** A 50% reduction in heavy workload categories yields approximately **50% of the benefit** (3.1% vs. 3.6%), suggesting a linear relationship with modest overall impact.

---

## Critical Observations

### 1. Similar Resolution Times Across Categories

Heavy workload categories (Network: 250.81h, Database: 253.56h) have nearly **identical mean resolution times** as software (268.03h). The main distinction is **volume**, not complexity or speed.

- **Network tickets:** 250.81 hours (242 tickets)
- **Database tickets:** 253.56 hours (90 tickets)
- **Software tickets:** 268.03 hours (70 tickets)

This suggests that **agent skill or task inherent difficulty** is not the primary driver of resolution time variation for heavy workload categories.

### 2. Confounding by Scope and Severity

The `is_heavy_workload_category` flag marks Network and Database based on **ticket volume and infrastructure criticality**, not individual ticket complexity. High-volume, enterprise-critical categories may include both quick-fixes and long-resolution issues, averaging to similar resolution times as diverse, lower-volume categories.

### 3. Weak Direct Causal Effect

The data shows **weak causal evidence** that reducing heavy workload ticket types alone would substantially drop resolution times. The confounders identified in the GT annotation (scope_context, is_outage_scope, remote_access_involved) likely mediate much of the resolution time variance.

---

## Implications for Resolution Time Strategy

1. **Volume Reduction Alone is Insufficient:** Eliminating high-volume categories does not proportionally reduce mean resolution time, suggesting **other factors dominate resolution speed** (e.g., problem scope, skill mix, escalation paths).

2. **Modest Baseline Improvement:** A 3–5% improvement is achievable but **not substantial**. Larger gains would require addressing root causes (e.g., improving Network/Database infrastructure, specialist skill training).

3. **Practical Consideration:** While removing 77.6% of tickets is unrealistic, the linear relationship (50% reduction → 3.1% time drop) indicates that even significant workload shedding has **limited direct impact** on overall resolution speed without addressing specific resolution mechanisms.

---

## Limitations

- **Missing Augmented Columns:** The `ticket_type`, `affected_component`, `problem_mechanism`, and `scope_context` columns referenced in GT specs are not present in the augmented table, limiting causal mechanism analysis.
- **Skill Off Variant:** The "skill_off" label suggests skills are disabled/unknown; results may differ if agent skill levels are factored.
- **Closed Tickets Only:** Analysis includes only closed/resolved tickets (428 of 500); open tickets and SLA misses are not measured.

---

## Conclusion

**Resolution time would drop by 3.6–5.5% if heavy workload categories were eliminated.** However, this modest improvement indicates that **ticket volume and categorization are weak direct drivers** of resolution time. Strategies to reduce resolution time should focus on improving:

1. Root-cause problem mechanisms (connectivity, authentication, performance)
2. Agent skill and knowledge alignment by component
3. Scope and severity management (isolating vs. enterprise-wide issues)
4. Infrastructure reliability to reduce ticket recurrence

**Recommendation:** Rather than reducing heavy workload ticket types, optimize the resolution process for Network and Database tickets through specialized support, proactive infrastructure improvements, and better diagnostic tools.
