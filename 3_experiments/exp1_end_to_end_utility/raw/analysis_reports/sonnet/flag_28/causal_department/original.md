---
dataset: flag_28
scenario: causal_department
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: causal_attribution
focus_variable: "department_goal_achievement"
query: "Why do goal achievement rates differ across departments?"
source_table: augment_table/flag_28/causal_department/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_28__causal_department/analyses/original/analysis.md
wall_seconds: 72.24
---

# Why goal achievement rates differ across departments

**Definition used:** a goal is treated as achieved when `percent_complete >= target_percentage`.

## Department pattern

| Department | Achieved rate | Achieved count | Completed share | Avg. % complete | Avg. target |
|---|---:|---:|---:|---:|---:|
| IT | 48.8% | 63/129 | 65.1% | 70.4 | 74.6 |
| HR | 23.4% | 34/145 | 44.1% | 44.8 | 74.7 |
| Finance | 15.6% | 20/128 | 40.6% | 47.8 | 75.7 |
| Marketing | 14.9% | 22/148 | 44.6% | 42.4 | 74.2 |

## Main drivers visible in the data

- **IT closes more work, and closed work is far more likely to hit target.**  
  `state` is a major driver because **no `In Progress`, `Planned`, or `Cancelled` rows meet target** in this table; only `Completed` rows do. IT has the highest `Completed` share at **65%** vs **41%–45%** elsewhere.

- **IT also performs better even after controlling for completion status.**  
  Among `Completed` goals, achieved rates are:
  - **IT:** 75.0%
  - **HR:** 53.1%
  - **Finance:** 38.5%
  - **Marketing:** 33.3%  
  This suggests the gap is **not only** about having fewer open items.

- **Target difficulty looks similar across departments; progress differs more than targets.**  
  Average `target_percentage` is tightly grouped at **74–76** for all departments. The bigger difference is `percent_complete`: **70.4 in IT** vs **42.4–47.8** in the other departments. The lower-achieving departments are mostly missing because progress is lower, not because targets are clearly harder.

- **Priority mix likely contributes strongly.**  
  IT has a very different `priority` profile:
  - **IT:** 110/129 goals are `High` or `Critical` (**85%**)
  - **HR:** 31/145 (**21%**)
  - **Finance:** 20/128 (**16%**)
  - **Marketing:** 24/148 (**16%**)  
  Across the full dataset, `High` and `Critical` goals achieve much more often (**52.7%** and **58.5%**) than `Low` and `Medium` goals (**8.7%** and **10.9%**). This makes work mix a plausible contributor to the department gap.

- **Category and metric mix also matter, but they do not fully explain IT’s lead.**  
  IT is stronger across **all** `category` groups (roughly **30%–61%** achieved), while the other departments are mostly below **31%** in each category.  
  Notable weak spots:
  - **Marketing:** very low on `Sales Increase` (**4.9%**)
  - **Finance:** very low on `Efficiency` (**4.5%**) and `Employee Satisfaction` (**8.7%**)  
  HR is mixed rather than uniformly weak; for example, `Sales Increase` is relatively better at **32.4%**.

## Bottom line

The department differences appear to come mostly from a combination of:

1. **Different workflow status mix** (`Completed` vs open work),
2. **Different priority mix** (IT has far more `High`/`Critical` goals),
3. **Different realized progress levels** (`percent_complete`), not clearly different target difficulty.

## Important cautions

- This table supports **association**, not a clean causal claim about department effects.
- Some fields are weak for explanation here. In particular, `start_date` and `end_date` contain many cases where `end_date < start_date`, so schedule length is not reliable enough to interpret.
- IT’s advantage is concentrated in urgent work: its `Low` and `Medium` priority items are still weak (**10%** and **0%** achieved), so the pattern is not simply “IT is better at everything.”
