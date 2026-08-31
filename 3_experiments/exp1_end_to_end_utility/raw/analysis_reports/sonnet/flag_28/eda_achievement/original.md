---
dataset: flag_28
scenario: eda_achievement
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: exploratory_data_analysis
focus_variable: "goal_achievement"
query: "How does goal achievement vary across department, metric, and the management practices described?"
source_table: augment_table/flag_28/eda_achievement/original.csv
generated_at: 2026-07-26T13:35:26.460247+00:00
wall_seconds: 78.6
---

# Goal Achievement Analysis: Department, Metric, and Management Practice

## Dataset Overview

The dataset contains **550 goal records** across four departments (Finance, HR, IT, Marketing), four performance metrics, and five management-practice categories. The key outcome variable is **achievement**, defined as `percent_complete ≥ target_percentage`.

---

## 1. Achievement by Department

| Department | N | Avg % Complete | Avg Target | Achievement Rate |
|---|---|---|---|---|
| IT | 129 | 70.4 | 74.6 | **48.8%** |
| HR | 145 | 44.8 | 74.7 | 23.4% |
| Finance | 128 | 47.8 | 75.7 | 15.6% |
| Marketing | 148 | 42.4 | 74.2 | **14.9%** |

**IT dominates across all dimensions.** With nearly half of its goals met, IT outperforms the next-best department (HR) by more than 25 percentage points. Marketing and Finance are near parity at the bottom (~15%). All departments face similar average targets (~74–76%), so the gap reflects true execution differences, not target-setting leniency.

---

## 2. Achievement by Metric

| Metric | N | Avg % Complete | Achievement Rate |
|---|---|---|---|
| Survey Score | 126 | 50.8 | **27.8%** |
| Expense Ratio | 138 | 52.6 | **27.5%** |
| Employee Turnover Rate | 153 | 50.5 | 23.5% |
| Sales Increase | 133 | 49.5 | 22.6% |

Differences across metrics are modest (22–28%). **Survey Score** and **Expense Ratio** are marginally easier to achieve, while **Sales Increase** is the hardest. The narrow spread (≈5 pp) suggests metric type is a weaker predictor than department.

---

## 3. Achievement by Management Practice (Category)

| Category | N | Avg % Complete | Avg Target | Achievement Rate |
|---|---|---|---|---|
| Customer Satisfaction | 112 | 52.4 | 74.3 | **30.4%** |
| Employee Satisfaction | 118 | 50.1 | 72.5 | **28.8%** |
| Revenue Growth | 118 | 50.8 | 74.9 | 24.6% |
| Cost Reduction | 98 | 50.7 | 74.6 | 23.5% |
| Efficiency | 104 | 50.1 | 77.8 | **18.3%** |

**Efficiency** goals have the lowest achievement rate and the highest average target (77.8%), creating a compounded challenge. **Customer Satisfaction** and **Employee Satisfaction** lead, though the spread (18–30%) is moderate. Goals categorized as people-facing practices slightly outperform process/cost goals.

---

## 4. Department × Metric Interaction

| Department | Employee Turnover | Expense Ratio | Sales Increase | Survey Score |
|---|---|---|---|---|
| IT | 47% | 48% | 42% | **58%** |
| HR | 17% | 26% | **32%** | 19% |
| Finance | 12% | 19% | 15% | 16% |
| Marketing | 18% | 22% | **5%** | 16% |

IT leads in every metric combination. IT's Survey Score goals are the single highest-performing cell (58%). Marketing's Sales Increase goals are the weakest cell (5%), suggesting Marketing struggles most with revenue-generation execution despite having sales-related targets.

---

## 5. Department × Management Practice Interaction

| Department | Cost Reduction | Customer Satisfaction | Efficiency | Employee Satisfaction | Revenue Growth |
|---|---|---|---|---|---|
| IT | 50% | 52% | 30% | **61%** | 47% |
| HR | 24% | 24% | 24% | 26% | 19% |
| Finance | 17% | **31%** | **5%** | 9% | 15% |
| Marketing | 14% | 15% | 15% | 14% | 17% |

- **IT × Employee Satisfaction** is the strongest cell (61%), suggesting IT's people programs are most effective.
- **Finance × Efficiency** is the weakest cell (5%), indicating that Finance's operational efficiency goals are rarely completed.
- HR shows relative uniformity across categories (~19–26%), hinting at consistent but modest execution.
- Marketing underperforms uniformly (14–17%) across all practice areas.

---

## 6. Goal State and Priority Context

Goal state strongly predicts achievement: **Completed** goals reach 52.3% achievement, while **In Progress**, **Planned**, and **Cancelled** goals register 0% (by definition, not yet met). Only 48% of all goals are Completed.

Priority also matters: **Critical** (58.5%) and **High** (52.7%) priority goals are far more likely to be achieved than **Low** (8.7%) or **Medium** (10.9%) goals — likely driven by greater resource allocation and oversight.

---

## Key Findings

1. **Department is the strongest single predictor** of achievement. IT (48.8%) outperforms Marketing (14.9%) by ~34 pp.
2. **Management practice type has moderate influence**: Customer Satisfaction and Employee Satisfaction goals achieve ~30%, while Efficiency goals lag at 18%.
3. **Metric type is the weakest differentiator** (~22–28% range), though Sales Increase is consistently the hardest across departments.
4. **IT excels regardless of metric or practice category**, pointing to superior execution capability or more achievable internal goal-setting.
5. **Marketing's Sales Increase goals (5%)** represent a critical failure point deserving intervention.
6. **Finance's Efficiency goals (5%)** similarly signal a structural gap between target-setting and delivery.
7. **Priority level strongly moderates outcomes** — low-priority goals are rarely completed, raising questions about resource triage.
