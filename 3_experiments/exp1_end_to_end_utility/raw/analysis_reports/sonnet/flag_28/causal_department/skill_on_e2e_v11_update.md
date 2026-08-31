---
dataset: flag_28
scenario: causal_department
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "department_goal_achievement"
query: "Why do goal achievement rates differ across departments?"
source_table: augment_table/flag_28/causal_department/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:18:43.473439+00:00
wall_seconds: 82.81
---

# Goal Achievement Rates by Department: Causal Analysis

## Executive Summary

IT achieves goals at **48.8%** — more than 3× the rate of Marketing (14.9%) and Finance (15.6%) and about 2× that of HR (23.4%). The dominant driver is **priority composition**: IT assigns 85% of its goals to High or Critical priority, versus only 18% for the other three departments. Priority is strongly causal — High/Critical goals achieve at ~55–58% regardless of department — and IT's unusually high-priority portfolio almost entirely explains its lead.

---

## 1. Achievement Rates by Department

| Department | N | Completed | Achieved (≥ target) | Achievement Rate | Avg % Complete | Cancelled |
|---|---|---|---|---|---|---|
| IT | 129 | 84 | 63 | **48.8%** | 70.4 | 4 |
| HR | 145 | 64 | 34 | **23.4%** | 44.8 | 9 |
| Finance | 128 | 52 | 20 | **15.6%** | 47.8 | 3 |
| Marketing | 148 | 66 | 22 | **14.9%** | 42.4 | 8 |

**Definition:** A goal is "achieved" if `state = Completed` AND `percent_complete ≥ target_percentage`. Targets are similar across all departments (avg 74–76%).

---

## 2. Primary Driver: Priority Composition

High/Critical goals achieve at 45–58% across every department; Low/Medium goals achieve at only 5–14%. IT's portfolio is 85% High/Critical, while Finance, HR, and Marketing are each only 18–21% High/Critical.

| Department | High+Critical Share | Achievement (High/Crit) | Achievement (Low/Med) | Overall Rate |
|---|---|---|---|---|
| IT | **85%** | 56.4% | 5.3% | **48.8%** |
| HR | 21% | 58.1% | 14.0% | 23.4% |
| Finance | 16% | 45.0% | 10.2% | 15.6% |
| Marketing | 16% | 58.3% | 6.5% | 14.9% |

**Counterfactual:** If Finance, HR, and Marketing were given IT's 85% high-priority mix (using their own within-priority achievement rates), their simulated achievement rates would be 39.8%, 51.5%, and 50.5% respectively — compared to their actual 15.6%, 23.4%, and 14.9%. Priority mix alone closes most of the gap.

---

## 3. TAPP-Generated Facets: Additional Signal

*TAPP columns used: `primary_lever`, `initiative_complexity`, `goal_specificity`, `time_horizon`, `measurement_mechanism`, `metric_goal_alignment`, `scope_breadth`.*

### 3a. initiative_complexity
`multi_action` goals achieve at 28.6% vs. `single_action` at 21.6% and `program_level` at 22.6% — a modest positive signal for more structured multi-step goals. Department distributions are similar (40–54% multi_action across all four), so this does not explain inter-department differences.

### 3b. goal_specificity
`quantified_no_baseline` goals achieve at 27.6% vs. `quantified_with_baseline` at 19.7%. Department distributions are broadly similar (~72% vs. ~28%), contributing little to the cross-department gap.

### 3c. time_horizon
Distributions are nearly identical across departments (within_year ~45–50%, within_quarter ~33–41%). Achievement rates vary mildly (within_year 26.4%, within_quarter 24.9%), but this facet is **not a departmental differentiator**.

### 3d. measurement_mechanism
IT and HR have a slightly higher share of `survey_based` measures (36–39%) relative to Finance (30%) and Marketing (33%). Survey-based goals achieve at 28.4% — above the global mean of 25.5% — but the difference is too small and distributions too similar to explain the large IT lead.

### 3e. primary_lever
`automation` goals achieve at only 17.0%, while `customer_service` (30.4%) and `people_programs` (28.8%) perform best. Marketing has the highest automation share (24%) and lowest achievement rate, which is a contributing factor. IT's automation share (12%) is the lowest among departments. However, the effect magnitude is secondary to priority.

| Primary Lever | Achievement Rate | N |
|---|---|---|
| customer_service | 30.4% | 112 |
| people_programs | 28.8% | 118 |
| cost_optimization | 27.5% | 80 |
| marketing_sales | 25.0% | 104 |
| automation | 17.0% | 94 |
| process_improvement | 13.8% | 29 |

### 3f. metric_goal_alignment, scope_breadth
`metric_goal_alignment` (True/False) shows nearly identical distributions across departments (~22–24% True) and very similar achievement rates (True: 23.6%, False: 25.8%). **Weak signal.** `scope_breadth` is dominated by `company_wide` (76–82%) in all departments with minimal differential effect.

---

## 4. Synthesis

| Driver | Strength | Cross-Dept Differentiator? |
|---|---|---|
| **Priority (High/Critical share)** | Very strong (~55% vs ~10% achievement) | **Yes — IT: 85%, others: ~18%** |
| **primary_lever** (`automation` drag) | Moderate | Partial — Marketing highest automation |
| `initiative_complexity` | Weak | No |
| `goal_specificity` | Weak | No |
| `time_horizon` | Negligible | No |
| `measurement_mechanism` | Weak | No |
| `metric_goal_alignment` | Negligible | No |
| `scope_breadth` | Negligible | No |

**Conclusion:** Goal achievement rates differ across departments primarily because **IT concentrates ~85% of goals at High or Critical priority**, while Finance, HR, and Marketing assign ~80% of goals to Low or Medium priority — where achievement rates fall below 15% universally. This priority allocation pattern likely reflects IT's operational urgency and escalation culture. Among TAPP facets, `primary_lever` adds marginal explanatory value: Marketing's heavy reliance on `automation`-type initiatives (24%) suppresses its rate further, while `process_improvement`-heavy portfolios (Finance, HR) also underperform. Other TAPP facets (time_horizon, metric_goal_alignment, scope_breadth, goal_specificity) are either uniformly distributed or show weak effects and do not meaningfully explain the cross-department pattern.

---

## Method Note

TAPP-generated columns analyzed: `primary_lever`, `goal_mechanism`, `goal_specificity`, `initiative_complexity`, `time_horizon`, `measurement_mechanism`, `metric_goal_alignment`, `scope_breadth`. Of these, `primary_lever` contributed marginal explanatory signal; the remaining six were assessed but found to be either uniformly distributed across departments or weakly correlated with achievement, and are not centered in the report.
