---
dataset: flag_28
scenario: eda_achievement
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "goal_achievement"
query: "How does goal achievement vary across department, metric, and the management practices described?"
source_table: augment_table/flag_28/eda_achievement/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:19:10.553704+00:00
wall_seconds: 49.32
---

# Goal Achievement Analysis: Department, Metric, and Management Practice

## Overview

The dataset contains **550 goal records** across four departments, four performance metrics, and six management practices. The focus variable is `achievement_status`, which takes six values: Achieved, Missed, On Track, At Risk, Not Started, and Cancelled. For completed goals the effective success rate is measured as **Achieved / (Achieved + Missed)**.

---

## 1. Achievement by Department

| Department | Achieved | Missed | Achievement Rate | Avg Completion Gap |
|------------|----------|--------|------------------|--------------------|
| IT | 63 | 21 | **75.0%** | −4.2 |
| HR | 34 | 30 | 53.1% | −29.9 |
| Finance | 20 | 32 | 38.5% | −28.0 |
| Marketing | 22 | 44 | **33.3%** | −31.8 |

**IT stands out sharply** with a 75% achievement rate and a near-zero completion gap (−4.2), while Marketing and Finance trail badly (33–39%). HR sits in the middle. IT also has the fewest At-Risk goals (only 6), suggesting better execution discipline across the board.

---

## 2. Achievement by Metric

| Metric | Achievement Rate (Achieved/Completed) | Avg Completion Gap |
|--------|---------------------------------------|---------------------|
| Expense Ratio | **55.1%** | −22.2 |
| Survey Score | 54.7% | −24.3 |
| Employee Turnover Rate | 50.7% | −23.4 |
| Sales Increase | **48.4%** | −25.9 |

Differences across metrics are **modest** (≈7 percentage points range). Expense Ratio goals succeed slightly more often, and Sales Increase goals have the lowest success rate and widest completion gap. No metric shows a decisive structural advantage, suggesting that the type of KPI being tracked is a weaker predictor than department or management practice.

---

## 3. Achievement by Management Practice

| Management Practice | Achievement Rate | At-Risk Rate | Avg Completion Gap |
|---------------------|------------------|--------------|--------------------|
| Customer-Focused | **63.2%** | 12.1% | −21.2 |
| People-Centric | 56.7% | 14.0% | −21.8 |
| Financial Control | 48.0% | 15.6% | −24.1 |
| Other | 47.2% | 11.5% | −24.1 |
| Process Improvement | 46.7% | **17.8%** | −28.0 |
| Automation-Driven | **43.2%** | **18.7%** | −27.7 |

**Customer-Focused** practices produce the best outcomes: highest achievement rate (63.2%) and smallest completion gap. **People-Centric** is second. **Automation-Driven** and **Process Improvement** both underperform—they have the highest At-Risk rates (≈18%) and the widest completion gaps, suggesting these approaches face greater execution challenges.

---

## 4. Combined Patterns and Notable Exceptions

- **IT's dominance** is consistent regardless of metric or management practice. Its low At-Risk count (6 vs. 23–25 for other departments) indicates organizational capability, not just favorable metrics.
- **Marketing** has the most Missed goals (44) and the most At-Risk goals (25), making it the highest-concern department.
- **Finance** has the most At-Risk goals (24) despite having only 128 total records, suggesting many in-progress goals are struggling.
- **Automation-Driven** goals appear frequently in Marketing and Finance, where outcomes are weakest—this co-occurrence may partly explain why automation-driven practices show poor results overall (rather than the practice itself being inherently weak).
- **Financial Control** has a small sample (45 records), so its 48% rate carries higher uncertainty.
- Metric-level differences are small enough that **metric type alone should not drive management intervention decisions**.

---

## Key Takeaways

1. **Department is the strongest differentiator**: IT achieves goals at 2× the rate of Marketing.
2. **Customer-Focused and People-Centric practices** correlate with better achievement and lower completion gaps.
3. **Automation-Driven and Process Improvement practices** show elevated At-Risk rates and wider gaps—flag for closer monitoring.
4. **Metric choice has limited impact** on success rates; interventions should focus on department capability and management approach rather than metric selection.
