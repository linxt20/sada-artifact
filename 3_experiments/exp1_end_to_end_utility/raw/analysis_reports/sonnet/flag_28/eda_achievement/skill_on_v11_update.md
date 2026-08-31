---
dataset: flag_28
scenario: eda_achievement
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "goal_achievement"
query: "How does goal achievement vary across department, metric, and the management practices described?"
source_table: augment_table/flag_28/eda_achievement/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:18:26.110490+00:00
wall_seconds: 48.54
---

# Goal Achievement Analysis — `skill_on_v11_update`

**Dataset:** 550 goals across four departments | **Overall completion rate:** 48.4% (`state == Completed`)

---

## 1. Achievement by Department

| Department | Completion Rate | N |
|---|---|---|
| **IT** | **65.1%** | 129 |
| Marketing | 44.6% | 148 |
| HR | 44.1% | 145 |
| Finance | 40.6% | 128 |

IT stands out as a clear leader — roughly 20 percentage points above the other three departments, which cluster closely together. Finance is the weakest performer overall.

---

## 2. Achievement by Metric

| Metric | Completion Rate | N |
|---|---|---|
| Survey Score | 50.8% | 126 |
| Expense Ratio | 50.0% | 138 |
| Sales Increase | 46.6% | 133 |
| Employee Turnover Rate | 46.4% | 153 |

Differences across metrics are modest (< 5 pp), suggesting metric type is a weaker driver of achievement than department. The Employee Turnover Rate metric has the most goals and the lowest rate — worth monitoring.

**Department × Metric interactions** reveal sharper contrasts:
- IT achieves strongly on every metric (61–68%).
- Finance's Sales Increase goals complete at only 33.3%, its worst category.
- HR underperforms on Employee Turnover Rate (31.7%) but overperforms on Survey Score (51.6%) and Sales Increase (52.9%).

---

## 3. Achievement by Management Practices

### 3a. Primary Intervention Type

| Intervention | Rate | N |
|---|---|---|
| **technology_upgrade** | **73.3%** | 30 |
| work_environment | 55.8% | 43 |
| marketing_sales | 51.5% | 103 |
| resource_optimization | 50.0% | 32 |
| feedback_survey / cost_cutting / training_development | ~47.8% | 23–90 |
| process_redesign | 43.8% | 96 |
| automation | 40.2% | 97 |
| product_launch | 38.5% | 13 |

`technology_upgrade` has the highest rate (73.3%), though its sample size is small (n=30). `automation` and `product_launch` underperform relative to the mean — possibly reflecting higher complexity or longer lead times.

### 3b. Improvement Lever

| Lever | Rate | N |
|---|---|---|
| feedback_system | 55.2% | 58 |
| cost_cutting | 52.6% | 97 |
| market_expansion | 49.6% | 117 |
| employee_engagement | 48.9% | 88 |
| response_time | 46.2% | 80 |
| **workflow_efficiency** | **40.0%** | 105 |

`workflow_efficiency` is the weakest lever, completing at only 40% despite a large sample — a meaningful finding. `feedback_system` and `cost_cutting` levers outperform the average.

### 3c. Priority

| Priority | Rate | N |
|---|---|---|
| **Critical** | **72.3%** | 94 |
| **High** | **65.9%** | 91 |
| Medium | 38.3% | 193 |
| Low | 37.2% | 172 |

Priority is among the strongest predictors: Critical/High goals complete at nearly double the rate of Medium/Low goals. This likely reflects resource allocation and attention bias.

### 3d. Other Practice Flags

| Factor | Aligned/True | Misaligned/False |
|---|---|---|
| `target_metric_alignment` | 49.0% | 47.8% |
| `involves_people_program` | 50.8% (True) | 47.7% (False) |
| `involves_technology_investment` | 49.1% (True) | 48.1% (False) |
| `has_quantified_baseline` | 44.6% (True) | 49.5% (False) |

These four flags show **negligible or counterintuitive differences**. Notably, `has_quantified_baseline = True` is associated with *lower* completion (44.6% vs 49.5%) — possibly because harder or more rigorously scoped goals are more often tracked with baselines. Metric alignment adds almost no predictive power (< 1.5 pp gap).

### 3e. Initiative Scope

| Scope | Rate | N |
|---|---|---|
| external_market | 51.8% | 83 |
| company_wide | 48.4% | 308 |
| department_wide | 46.7% | 150 |
| individual_team | 44.4% | 9 |

Scope differences are small; `external_market` slightly leads but the sample is modest.

---

## 4. Key Takeaways

1. **Department is the dominant differentiator.** IT's 65% rate vs. Finance's 41% suggests structural or capability differences, not metric-level effects.
2. **Priority drives completion far more than management practice flags.** Critical/High goals achieve at ~2× the rate of Low/Medium goals.
3. **Intervention type matters at the extremes.** `technology_upgrade` outperforms; `automation` and `product_launch` lag — possibly due to scope or dependency complexity.
4. **`workflow_efficiency` as a lever is a weak spot** (40% completion, n=105 — high confidence).
5. **Alignment flags and baseline tracking show weak or reversed relationships** with achievement, indicating these governance practices are not yet meaningfully predictive in this dataset.
