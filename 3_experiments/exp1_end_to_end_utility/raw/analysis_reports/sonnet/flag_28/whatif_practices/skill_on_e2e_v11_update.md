---
dataset: flag_28
scenario: whatif_practices
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: what_if
focus_variable: "percent_complete"
query: "If teams adopted the goal-management practices described by top performers, how much would achievement improve?"
source_table: augment_table/flag_28/whatif_practices/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:20:53.302096+00:00
wall_seconds: 149.93
---

# What-If Analysis: Goal-Management Practices and Achievement Improvement
**Dataset:** 550 goals (526 non-cancelled) | **Date:** 2026-07-30

---

## Executive Summary

Adopting top-performer goal-management practices yields **modest but real marginal gains of ~2–5 percentage points** in `percent_complete`. However, the single largest driver of achievement in this dataset is **goal priority** (High/Critical vs. Low/Medium), which alone explains a ~37-point gap. Practice improvements are most impactful within the same priority tier and when combined: the best-documented practice bundle (`training_development` lever + `multi_step_detailed` action plan) shows a **+22.5 pt advantage** over single-action alternatives, though at small sample size (n=10 vs. n=6).

---

## 1. Outcome Variable and Dominant Driver

| Priority Tier | Mean `percent_complete` | Median | n |
|---|---|---|---|
| Critical | 75.2 | 79.0 | 93 |
| High | 76.5 | 78.0 | 86 |
| Low | 39.1 | 42.0 | 161 |
| Medium | 37.8 | 36.0 | 186 |

**High/Critical goals average 75.8% complete; Low/Medium goals average 38.4%** — a **37.4-point gap** that dwarfs any single practice effect. This is corroborated by department-level data: IT (84.8% of goals High/Critical) averages **70.5%** complete, while Marketing (17.1% High/Critical) averages **42.6%**.

---

## 2. Practice Effects from TAPP-Augmented Columns

*TAPP columns used: `action_plan_detail`, `feedback_loop_present`, `goal_specificity`, `target_ambition_level`, `time_horizon`, `primary_lever`.*

### 2a. `action_plan_detail`: Largest Consistent Practice Signal

| | Multi-step Detailed | Single Action | Difference |
|---|---|---|---|
| Mean `percent_complete` (all) | 52.2 | 50.4 | **+1.8 pts** |
| Completion rate | 53.4% | 48.8% | **+4.6 pp** |
| Within Critical | 75.7 | 74.9 | +0.8 |
| Within High | 78.4 | 75.4 | **+3.0** |
| Within Low | 40.4 | 38.2 | +2.2 |
| Within Medium | 38.7 | 37.3 | +1.4 |

Effect is **consistent across all priority tiers** (always positive). Currently **60.8% of goals (n=320)** use single_action only. If these adopted multi_step_detailed, the weighted uplift in Low/Medium tiers would be approximately **+1.1 pts** in average `percent_complete` for those 347 goals — or **+1.8 pts** overall.

### 2b. `primary_lever`: Largest Effect with `training_development`

| `primary_lever` | `action_plan_detail` | Mean `percent_complete` | Completion Rate | n |
|---|---|---|---|---|
| training_development | multi_step_detailed | **62.2** | — | 10 |
| training_development | single_action | 39.7 | — | 6 |
| feedback_system | multi_step_detailed | 54.2 | 54.7% | 42 |
| feedback_system | single_action | 53.6 | — | 22 |
| automation | multi_step_detailed | 51.1 | 43.0% | — | 

`feedback_system` has the **highest completion rate (54.7%)** among all levers. `training_development` + `multi_step_detailed` shows the largest gap (+22.5 pts vs. single_action), but the sample is small (n=16 total for this lever) and should be treated as directional.

### 2c. `feedback_loop_present`: Weak and Inconsistent Signal

| Priority | Feedback=True | Feedback=False | Difference |
|---|---|---|---|
| Critical | 73.9 | 75.5 | −1.6 |
| High | 77.4 | 76.3 | +1.0 |
| Low | 36.4 | 39.6 | −3.2 |
| Medium | 42.1 | 36.9 | +5.2 |

`feedback_loop_present` is inconsistent across priority tiers and **not a reliable practice lever** for a universal recommendation (only 17.5% of goals have it; effect direction flips).

### 2d. `goal_specificity`: Counterintuitive Result

| `goal_specificity` | Mean `percent_complete` | Completion Rate | n |
|---|---|---|---|
| quantified_target_only | 52.1 | 53.4% | 380 |
| quantified_baseline_and_target | 48.7 | 43.2% | 146 |

More specific goals (baseline + target) do **not** outperform simpler quantified targets here. This may reflect that harder goals with baselines are harder to complete. **`goal_specificity` is not a recommended lever.**

### 2e. `target_ambition_level`: Incremental Targets Slightly Outperform

| Level | Mean `percent_complete` | n |
|---|---|---|
| incremental_under_15pct | **59.1** | 31 |
| moderate_15_to_25pct | 50.9 | 400 |
| ambitious_over_25pct | 49.3 | 91 |

Higher ambition is **associated with lower achievement rates**, consistent with stretch-goal literature. Teams adopting moderate targets show slightly better completion than ambitious ones, though the effect is modest.

### 2f. `time_horizon`: Marginal Difference

| `time_horizon` | Mean `percent_complete` | n |
|---|---|---|
| within_quarter | 52.0 | 212 |
| within_year | 51.2 | 246 |
| unspecified | 48.6 | 58 |

Quarterly time horizons marginally outperform annual (+0.8 pts). The absence of a specified horizon (`unspecified`) reduces achievement by ~2.6 pts versus quarterly goals.

---

## 3. What-If Scenarios

### Scenario A: Universal Adoption of `multi_step_detailed` Action Plans
- **Who benefits:** 320 goals currently using `single_action`
- **Expected lift:** +1.8 pts in mean `percent_complete`; completion rate rises ~4.6 pp
- **Population-level impact:** Weighted across all 526 active goals, mean achievement rises from **51.1% → ~52.2%**

### Scenario B: Shift Low/Medium Priority Goals to Best Practices Bundle
(multi_step_detailed + feedback_system lever + within_quarter)
- Targets the 347 Low/Medium priority goals (66% of active portfolio)
- Current mean: **38.4%**; best-practice Low/Medium subset mean: **~41–43%**
- Estimated uplift: **+2–5 pts** within this tier

### Scenario C: Rebalance Priority Distribution (Non-Practice But Structural)
- If Marketing and Finance matched IT's priority mix (84.8% High/Critical), their mean `percent_complete` would shift toward the **74–76% range** seen for High/Critical goals in those departments (Marketing H/C goals already average **74.8%**)
- This is a structural/management decision, not a practice change, but is the **single highest-leverage intervention**

---

## 4. Summary Table: Practice Lever Effectiveness

| Practice Lever | Effect Size | Consistency | Coverage Gap | Recommend? |
|---|---|---|---|---|
| `action_plan_detail`: multi_step | +1.8 pts, +4.6 pp completion | Consistent across tiers | 60.8% still single_action | ✅ Yes |
| `primary_lever`: feedback_system | +5.5 pp completion rate | High | Well-covered (12%) | ✅ Yes |
| `primary_lever`: training_development + multi_step | +22.5 pts | Small sample (n=10) | Most goals don't use it | ⚠️ Directional |
| `time_horizon`: within_quarter | +0.8–3.4 pts | Moderate | 41% unspecified/annual | ✅ Marginal |
| `feedback_loop_present` | Mixed (−3 to +5) | Inconsistent | 82.5% no feedback | ❌ Weak |
| `goal_specificity`: baseline+target | −3.4 pts | Unfavorable | — | ❌ Not recommended |

---

## 5. Conclusions

1. **Priority assignment is the dominant factor** (37.4 pt gap): ensuring adequate staffing, leadership attention, and resources for High/Critical goals yields far greater improvement than any practice change alone.

2. **The highest-ROI practice change is adopting multi-step detailed action plans** (`action_plan_detail = multi_step_detailed`): it shows a consistent +1.8 pt average and +4.6 pp completion rate lift across all priority tiers, and 61% of current goals have not adopted it.

3. **Using `feedback_system` as the primary lever** is associated with the best completion rate (54.7%) and is the second-strongest practice recommendation.

4. **Estimated total achievement improvement from practice adoption alone:** ~**2–5 percentage points** in mean `percent_complete` for teams shifting from the modal (single_action, non-feedback-system) profile to the top-performer profile — equivalent to raising the portfolio average from ~51% to ~53–56%.

5. **`feedback_loop_present`, `goal_specificity`, and `target_ambition_level`** (TAPP columns) do not show reliable positive effects in this dataset and should not be prioritized as levers.

---

**Method Note:** TAPP-generated columns used in this analysis: `action_plan_detail`, `feedback_loop_present`, `goal_specificity`, `target_ambition_level`, `time_horizon`, `primary_lever`. The column `measurement_mechanism` was reviewed but found to be largely colinear with `category` and not independently analyzed. All TAPP column effects were cross-checked against original structured columns (`priority`, `state`, `percent_complete`, `department`).
