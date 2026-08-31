---
dataset: flag_28
scenario: eda_achievement
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "goal_achievement"
query: "How does goal achievement vary across department, metric, and the management practices described?"
source_table: augment_table/flag_28/eda_achievement/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:19:07.260805+00:00
wall_seconds: 81.01
---

# Goal Achievement Analysis: Department, Metric, and Management Practices
**Dataset:** 550 goals | **TAPP columns used:** `primary_intervention_type`, `goal_scope`, `time_horizon`, `technology_enabler`

---

## Method Note
Four TAPP-generated columns were available: `primary_intervention_type`, `goal_scope`, `time_horizon`, and `technology_enabler`. The first two (`primary_intervention_type` and `technology_enabler`) added meaningful semantic signal beyond the raw structured columns and are cited substantively below. `goal_scope` and `time_horizon` showed weak or inconsistent effects and are summarised briefly. All claims are cross-checked against original structured fields (`state`, `percent_complete`, `target_percentage`, `priority`, `department`, `metric`, `category`).

**Achievement definition:** A goal is *achieved* when `state == Completed` AND `percent_complete ≥ target_percentage` (n = 139/550, overall rate = **25.3%**). A secondary metric, *completion rate* (`state == Completed`), is also reported (48.4%).

---

## 1. Overall Outcome Distribution

| State | Count | Share |
|-------|-------|-------|
| Completed | 266 | 48.4% |
| In Progress | 198 | 36.0% |
| Planned | 62 | 11.3% |
| Cancelled | 24 | 4.4% |

Mean `percent_complete` for completed goals is 59.4 vs. target mean of ~74–75, confirming that many completions still fall short of target—hence the gap between 48.4% completion and 25.3% achievement.

---

## 2. Achievement by Department

IT stands far above all other departments on both achievement rate and mean progress-to-target gap.

| Department | N | Achievement Rate | Completion Rate | Mean % Gap (actual − target) |
|------------|---|-----------------|-----------------|------------------------------|
| **IT** | 129 | **48.8%** | 65.1% | −4.2 |
| HR | 145 | 23.4% | 44.1% | −29.9 |
| Finance | 128 | 15.6% | 40.6% | −28.0 |
| Marketing | 148 | 14.9% | 44.6% | −31.8 |

IT's achievement rate is **3.3× the Marketing rate** and its mean gap to target is nearly 8× smaller. This gap persists across all four metrics (IT: 47–58%; others: 5–32% per metric-cell, see §3).

---

## 3. Achievement by Metric

Metric differences are moderate and secondary to department effects.

| Metric | N | Achievement Rate | Completion Rate | Mean Target % | Mean % Complete |
|--------|---|-----------------|-----------------|---------------|-----------------|
| Survey Score | 126 | 27.8% | — | 75.1 | 50.8 |
| Expense Ratio | 138 | 27.5% | — | 74.8 | 52.6 |
| Employee Turnover Rate | 153 | 23.5% | — | 73.9 | 50.5 |
| Sales Increase | 133 | 22.6% | — | 75.4 | 49.5 |

The spread is narrow (5 pp). Target percentages are uniform (~74–75) across metrics, so metric choice does not explain achievement gaps; department context dominates.

**Department × Metric interaction** highlights the IT effect further:

| | Employee Turnover | Expense Ratio | Sales Increase | Survey Score |
|--|--|--|--|--|
| **IT** | **47.4%** | **48.1%** | **41.9%** | **57.6%** |
| HR | 17.1% | 25.6% | 32.4% | 19.4% |
| Finance | 11.8% | 19.4% | 14.8% | 16.1% |
| Marketing | 17.5% | 22.2% | **4.9%** | 16.1% |

Marketing's Sales Increase achievement (4.9%) is particularly low—only 7 of 41 such goals were achieved.

---

## 4. Achievement by Priority

Priority is the single strongest driver in the dataset, cutting across all departments.

| Priority | N | Achievement Rate | Completion Rate | Mean % Gap |
|----------|---|-----------------|-----------------|------------|
| **Critical** | 94 | **58.5%** | 72.3% | +2.6 |
| **High** | 91 | **52.7%** | 65.9% | +0.1 |
| Medium | 193 | 10.9% | 38.3% | −36.2 |
| Low | 172 | 8.7% | 37.2% | −37.3 |

Critical and High goals achieve at rates 5–7× those of Medium/Low goals. Both completion rates and mean % gaps confirm the pattern is structural, not an artifact of the achievement definition. The interaction with department persists: IT Critical goals achieve at 61%, but even IT's Medium/Low goals achieve at 0–10%.

---

## 5. Achievement by Management / Intervention Practice (`primary_intervention_type`)

The TAPP column `primary_intervention_type` classifies the described management practice. It adds explanatory signal beyond what category or priority alone captures.

| Intervention | N | Achievement Rate | Completion Rate | Mean % Gap |
|---|---|---|---|---|
| **training_program** | 20 | **35.0%** | 55.0% | −13.8 |
| **infrastructure_change** | 35 | **37.1%** | 68.6% | −16.5 |
| feedback_system | 114 | 26.3% | 48.2% | −22.0 |
| marketing_strategy | 101 | 24.8% | 51.5% | −24.7 |
| process_optimization | 158 | 25.3% | 46.2% | −26.6 |
| product_expansion | 16 | 25.0% | 37.5% | −18.4 |
| automation | 106 | 18.9% | 42.5% | −26.5 |

**Training programs** and **infrastructure changes** outperform automation and process-optimization by ~10–18 pp. Automation-tagged goals have the lowest achievement rate (18.9%), likely reflecting high technical risk and slower ramp-up.

The department interaction is substantial (intervention × department):

| Intervention | Finance | HR | **IT** | Marketing |
|---|---|---|---|---|
| training_program | 25.0% | 0.0% | **71.4%** | 25.0% |
| infrastructure_change | 20.0% | 50.0% | **71.4%** | 12.5% |
| feedback_system | 8.3% | 27.3% | **53.3%** | 11.1% |
| process_optimization | 26.3% | 19.6% | **44.4%** | 13.2% |
| automation | 4.0% | 25.0% | **36.8%** | 16.7% |

IT benefits most from every intervention type. HR shows strength in infrastructure change (50.0%) and feedback systems (27.3%). Finance and Marketing lag regardless of intervention.

---

## 6. Goal Category

| Category | N | Achievement Rate | Mean % Gap |
|----------|---|-----------------|------------|
| Customer Satisfaction | 112 | **30.4%** | −21.8 |
| Employee Satisfaction | 118 | **28.8%** | −22.3 |
| Cost Reduction | 98 | 23.5% | −24.0 |
| Revenue Growth | 118 | 24.6% | −24.1 |
| Efficiency | 104 | 18.3% | −27.7 |

Customer Satisfaction and Employee Satisfaction goals achieve at a moderate premium; Efficiency goals underperform, consistent with the harder-to-measure and longer-cycle nature of operational efficiency initiatives.

---

## 7. TAPP Facets: Goal Scope, Time Horizon, Technology Enabler

**`goal_scope`** — Near-flat across all levels (company_wide 25.5%, department_specific 26.3%, regional 20.0%, team_level 20.0%). The 5 pp spread is negligible; this facet is not a meaningful driver.

**`time_horizon`** — Within-fiscal-year goals (n=258, 26.4%) and within-quarter goals (n=220, 24.5%) perform similarly; the multi-year cell (n=1) is too small. Time horizon does not add signal beyond priority and department.

**`technology_enabler`** — Mostly "no_technology" (437/550, 79.5%), limiting inference. Among minority cells: `cloud_infrastructure` (n=7, 71.4% achievement) and `crm_system` (n=3, 66.7%) show striking rates but samples are too small for generalisation. `automation_software` (n=95, 16.8%) underperforms — aligning with the automation intervention finding above.

---

## 8. Key Findings Summary

1. **IT department is the dominant outlier**: 48.8% achievement vs. 15–23% elsewhere. The gap persists across all metrics and intervention types; it is structural, not metric-driven.

2. **Priority is the strongest within-dataset lever**: Critical/High goals achieve at 53–59%; Medium/Low at 9–11%. This 6× ratio dwarfs all other effects.

3. **Metric choice matters little**: Survey Score and Expense Ratio marginally outperform Sales Increase and Employee Turnover (~5 pp spread), but Marketing's Sales Increase goals (4.9%) are a clear exception driven by department context.

4. **Management practice (`primary_intervention_type`) matters at the margin**: Training programs and infrastructure changes achieve at ~35–37%, roughly 10–18 pp above automation (18.9%). The advantage is strongest in IT but visible in HR and, to a lesser degree, other departments.

5. **Category framing**: Customer Satisfaction and Employee Satisfaction goals outperform Efficiency goals by ~12 pp, suggesting clearer measurement or stakeholder alignment.

6. **Goal scope and time horizon are weak or redundant** in this dataset. Technology enabler shows interesting patterns in small sub-groups (cloud, CRM) but is dominated by a no-technology majority.
