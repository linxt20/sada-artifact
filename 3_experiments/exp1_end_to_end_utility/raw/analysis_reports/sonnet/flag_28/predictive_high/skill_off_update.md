---
dataset: flag_28
scenario: predictive_high
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "high_goal_achievement"
query: "What signals suggest a goal will be highly achieved?"
source_table: augment_table/flag_28/predictive_high/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:20:07.097421+00:00
wall_seconds: 57.86
---

# Signals of High Goal Achievement — Analysis Report

**Dataset:** `sonnet__skill_off_update.csv` | **Rows:** 550 | **Focus Variable:** `high_achievement_score`

---

## How `high_achievement_score` Is Constructed

The focus variable is the product of two columns:

$$\text{high\_achievement\_score} = \text{progress\_ratio} \times \text{priority\_score}$$

where `progress_ratio = percent_complete / target_percentage` and `priority_score` maps Low→1, Medium→2, High→3, Critical→4. This means both *actual progress* and *declared priority* must be high for a goal to score highly.

**Score distribution:** mean ≈ 1.80, median ≈ 1.19, 75th-percentile threshold ≈ 2.87, max ≈ 7.12.

---

## Key Signals — Ranked by Correlation with `high_achievement_score`

| Signal | Correlation | Direction |
|---|---|---|
| `priority_score` (Low→Critical) | **0.861** | Higher priority → higher score |
| `progress_ratio` | **0.851** | More complete relative to target → higher score |
| `completion_gap` (actual − target %) | **0.818** | Positive gap (over-delivery) strongly predictive |
| `percent_complete` | **0.792** | Raw completion percentage |
| `is_on_track` | **0.721** | On-track flag strongly associated |
| `target_percentage` | **−0.283** | Lower target → easier to exceed → higher score |
| `duration_days` | **−0.083** | Weak / negligible effect |

---

## Profile of Highly Achieved Goals (Top 25%, score ≥ 2.87, n = 138)

### 1. Priority Is the Dominant Gate
- **Critical** priority: 83/138 goals (60%) in the top group, yet Critical makes up only 94/550 (17%) of all goals.
- **High** priority: 52/138 (38%).
- **Medium or Low**: only 3 goals in the top group combined — virtually absent.
- *Conclusion:* A Critical or High priority rating is a near-necessary condition for a high score.

### 2. Substantial Over-Delivery on Progress
- 99/138 top-group goals have a **positive `completion_gap`** (percent_complete > target_percentage), versus only 29/412 in the rest.
- Mean `progress_ratio` in the top group is well above 1.0; 106/138 (77%) have `progress_ratio ≥ 1.0`.
- Mean `percent_complete`: **79%** (top group) vs. **41%** (bottom group).

### 3. `is_on_track = 1` Is Near-Universal
- 131/138 top-group goals (95%) are flagged on-track, versus only 100/412 (24%) in the lower group.

### 4. State: Predominantly Completed
- 115/138 top-group goals (83%) have state = **Completed**.
- In the lower group, "In Progress" (178) and "Completed" (151) are roughly equal — many open goals have not yet accumulated progress.

### 5. Lower Target Percentages
- Top-group mean target: **69.4%** vs. all-goals mean: **74.8%**.
- Goals with more modest targets are proportionally easier to exceed, boosting `progress_ratio`.

### 6. Department & Category Patterns
- **IT department** dominates the top group (81/138 = 59%), suggesting either better execution culture or more Critical/High-priority goals routed there.
- Categories are relatively balanced (Employee Satisfaction, Customer Satisfaction, Revenue Growth each ~24–25%), so category alone is not a strong differentiator.

---

## Exceptions and Weak Evidence

- **Duration has negligible effect** (r = −0.08): short and long goals both appear in the top tier; some top-group goals have negative `duration_days` (end date before start), indicating data anomalies.
- **A few low-priority goals score moderately** if progress_ratio is very high, but they cannot reach the top quartile due to the multiplicative formula.
- **Cancelled and Planned goals** are almost entirely absent from the top group but not entirely — one Cancelled and two Planned goals appear, likely because they had high percent_complete logged before cancellation.
- The IT department dominance may reflect **assignment bias** (Critical goals routed to IT) rather than IT-specific execution quality.

---

## Decision-Ready Summary

> **A goal is most likely to be highly achieved when it carries Critical or High priority AND already shows percent_complete exceeding its target percentage (completion_gap > 0, progress_ratio ≥ 1.0), with `is_on_track = 1` and state = Completed.** Priority is the single strongest lever — no Low/Medium priority goal practically reaches the top quartile regardless of completion level. Goals with lower initial target percentages are also over-represented, suggesting ambitious but moderately scoped goals outperform aggressive targets.
