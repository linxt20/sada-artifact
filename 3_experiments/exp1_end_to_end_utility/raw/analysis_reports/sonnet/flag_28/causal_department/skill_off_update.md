---
dataset: flag_28
scenario: causal_department
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "department_goal_achievement"
query: "Why do goal achievement rates differ across departments?"
source_table: augment_table/flag_28/causal_department/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:18:32.528397+00:00
wall_seconds: 43.71
---

# Goal Achievement Rate Differences Across Departments

## Department-Level Summary

| Department | Goal Achievement Rate | Avg Completion % | Completion Rate | High-Priority Rate | Cancellation Rate | N |
|---|---|---|---|---|---|---|
| IT | **48.8%** | 70.4% | 65.1% | **85.3%** | 3.1% | 129 |
| HR | 23.5% | 44.8% | 44.1% | 21.4% | 6.2% | 145 |
| Finance | 15.6% | 47.8% | 40.6% | 15.6% | 2.3% | 128 |
| Marketing | **14.9%** | 42.4% | 44.6% | 16.2% | 5.4% | 148 |

IT far outperforms the other three departments, which cluster together in the 15–24% range.

---

## Key Driver: High-Priority Task Concentration

The strongest predictor of department-level goal achievement is the **share of high-priority and critical tasks** (`dept_high_priority_rate`, correlation ≈ **0.985** with achievement rate).

- **IT**: 85.3% of its goals are high or critical priority — by far the highest.
- **HR / Finance / Marketing**: all sit at 15–21%.

Within every department, high/critical goals succeed at materially higher rates than low/medium goals:

| Department | Critical achieve % | High achieve % | Low achieve % | Medium achieve % |
|---|---|---|---|---|
| IT | 61.1% | 51.8% | 10.0% | 0.0% |
| HR | 45.5% | 65.0% | 14.0% | 14.0% |
| Finance | 54.5% | 33.3% | 8.7% | 11.3% |
| Marketing | 61.1% | 50.0% | 3.4% | 9.2% |

Because IT has ~85% of its portfolio at high/critical priority (vs. ~16–21% elsewhere), its aggregate achievement rate is pulled up dramatically even though its per-priority achievement rates are not uniquely superior.

---

## Secondary Driver: Actual Progress / Completion

`dept_avg_completion_pct` (average `percent_complete` across goals) is strongly correlated with achievement rate (≈ **0.957**):

- IT: 70.4% average completion — substantially higher than the 42–48% range of other departments.
- `dept_completion_rate` (fraction of goals reaching "Completed" state) also tracks this: IT = 65.1% vs. ~41–45% elsewhere.

This reflects a portfolio that gets further toward its targets before closing, independently reinforcing IT's advantage.

---

## Minor Factors

- **Cancellation rate**: Finance has the lowest cancellation rate (2.3%) yet the second-worst achievement rate, suggesting cancellations are not a key lever here.
- **Average target percentage** (`dept_avg_target_pct`): Nearly identical across all departments (74–76%), so target-setting ambition does not explain the gap.
- **Category mix**: No single category clearly explains cross-department differences; all departments pursue cost reduction, customer satisfaction, and efficiency goals.

---

## Caution / Weak Evidence

- The `dept_high_priority_rate` column is a **department-level aggregate repeated for every row**, meaning causality cannot be established at the individual goal level. It is possible that IT's organizational context (e.g., clearer metrics, stronger tooling) drives both higher priority assignment and higher completion, with priority being a proxy rather than a direct cause.
- IT's near-zero achievement for medium-priority goals (0%) is anomalous and may reflect data quality issues or a small sub-sample effect.
- With only four departments the correlation analysis is descriptive; sample size limits statistical confidence.

---

## Decision-Ready Takeaway

The primary observable explanation for IT's ~3× higher goal achievement rate is that **85% of its goals are classified as high or critical priority**, compared with ≤21% in other departments. High/critical goals consistently achieve at 2–6× the rate of low/medium goals across every department. Closing the gap for HR, Finance, and Marketing likely requires either reprioritising their portfolios toward higher-stakes goals or investigating why lower-priority goals almost universally fail to reach their targets.
