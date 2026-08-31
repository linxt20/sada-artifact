---
dataset: flag_28
scenario: focus_inference
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth attention in these goal records."
source_table: augment_table/flag_28/focus_inference/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:18:36.303920+00:00
wall_seconds: 48.64
---

# Goal Records Analysis — `skill_on` Variant

## Dataset Overview

| Attribute | Value |
|---|---|
| Total goals | 550 |
| Departments | HR, IT, Marketing, Finance (roughly even: 125–148 each) |
| State breakdown | Completed 266 (48%), In Progress 198 (36%), Planned 62 (11%), Cancelled 24 (4%) |
| Priority breakdown | Medium 193 (35%), Low 172 (31%), High 91 (17%), Critical 94 (17%) |

---

## 1. Completion vs. Progress Quality

- **Completed goals** average only **59% `percent_complete`** (median 67%), and **50 Completed goals sit below 30%** — a data quality flag suggesting the `state` field may not reliably reflect true completion.
- **In Progress** goals average **43% complete**, with **46 In Progress goals below 20%** — these are effectively stalled and warrant review.
- **Planned** goals average **41% complete** despite not having started, which is another consistency concern.

> ⚠️ The `percent_complete` and `state` columns are frequently misaligned. Downstream prioritization should not rely on either field alone.

---

## 2. High-Urgency Goals Needing Attention

**22 goals are both Critical priority and In Progress**, with an average `percent_complete` of ~67% — most are moderately progressed but not done. Notable examples by category:

| sys_id | Category | % Complete | Metric |
|---|---|---|---|
| G000052 | Efficiency | 94 | Sales Increase |
| G000149 | Revenue Growth | 81 | Sales Increase |
| G000448 | Cost Reduction | 81 | Expense Ratio |
| G000015 | Employee Satisfaction | 53 | Sales Increase |
| G000179 | Cost Reduction | 54 | Sales Increase |

The near-complete Critical goals (≥80%) are the lowest-effort wins. The lower-progress Critical goals (≤55%) deserve resource checks.

---

## 3. Improvement Magnitude Distribution

| Band | Count |
|---|---|
| `standard_20pct` | 421 (77%) |
| `high_25_30pct` | 70 (13%) |
| `absolute_target_only` | 30 (5%) |
| `low_under_15pct` | 28 (5%) |
| Unknown | 1 |

The overwhelming reliance on **20% improvement targets** suggests templated goal-setting rather than context-specific targets. The **70 `high_25_30pct` goals** represent more ambitious commitments — worth tracking separately for feasibility.

---

## 4. Baseline & Alignment Gaps

- Only **127 of 550 goals (23%) have a baseline value** (`has_baseline_value = True`), making it impossible to measure actual improvement for the majority.
- Only **74 goals (13%) show `metric_category_alignment = True`** — meaning the tracked metric (e.g., `Expense Ratio`, `Survey Score`) actually aligns with the stated goal category for only a small minority. This is evenly distributed across categories, suggesting a systemic labeling or metric-assignment problem rather than a category-specific issue.

---

## 5. Scope & Action Lever Patterns

- **53% of goals are `company_wide`** in scope — a large proportion for goals sitting in individual departments.
- Top action levers: `process_improvement` (123), `feedback_survey` (112), `marketing_sales` (101), `automation` (95). `cost_negotiation` (9) and `product_expansion` (14) are rare.
- `Employee Satisfaction` and `Revenue Growth` are the most common categories (118 each), followed by `Efficiency` (104), `Customer Satisfaction` (112), and `Cost Reduction` (98).

---

## 6. Cancellation Pattern

- Only **24 goals cancelled (4%)** — mostly Low and Medium priority. Just **1 Critical goal was cancelled**, which is healthy.
- Cancelled goals have an average `percent_complete` of **44.5%**, suggesting some were abandoned midway rather than early.

---

## Key Takeaways

1. **Focus immediate attention on the 22 Critical + In Progress goals** — especially the ~6 below 60% completion.
2. **State/percent_complete inconsistency is systemic** — validate before reporting progress externally.
3. **Lack of baselines (77% of goals)** makes success measurement weak; prioritize baseline capture on active High/Critical goals.
4. **Metric-category misalignment (87%)** is the most actionable structural problem in the dataset — goals are largely being tracked on metrics that don't correspond to their stated objective.
5. **Templated 20% targets** dominate; consider whether goals reflect genuine strategic intent or administrative box-checking.
