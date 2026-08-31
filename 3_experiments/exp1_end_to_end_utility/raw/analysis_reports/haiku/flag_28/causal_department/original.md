---
dataset: flag_28
scenario: causal_department
variant: original
model: substrate-claude-haiku-4-5
query_subtype: causal_attribution
focus_variable: "department_goal_achievement"
query: "Why do goal achievement rates differ across departments?"
source_table: augment_table/flag_28/causal_department/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_28__causal_department/analyses/original/analysis.md
wall_seconds: 113.5
---

# Why goal achievement rates differ across departments

**How achievement was read:** the table has no explicit achievement flag, so achievement is inferred mainly from `percent_complete >= target_percentage`, with `state` used as supporting evidence. `Completed` alone is not enough because many completed goals still miss target.

## Bottom line
Goal achievement appears strongest in **IT**, weakest in **Marketing**, with **HR** and **Finance** mixed. The main drivers visible in the table are:
1. different mixes of goal types by department,
2. different shares of `Completed` vs `In Progress`/`Planned`/`Cancelled`,
3. different target difficulty, and
4. uneven execution even among completed goals.

## What the table shows

- **IT has the densest concentration of clear hits, including hard targets.** Examples: `G000001` (IT, Completed, `97/97`), `G000241` (`96/72`), `G000461` (`97/83`), `G000482` (`96/96`), `G000511` (`98/58`). Many IT rows are in `Efficiency`, `Customer Satisfaction`, `Cost Reduction`, or operational `Revenue Growth` efforts, and the descriptions often use concrete levers like automation, workflow redesign, and response-time improvements.

- **Marketing has the weakest pattern because many rows are either open/cancelled or completed far below target.** Examples: `G000103` (Planned, `1/95`), `G000278` (Completed, `3/97`), `G000310` (Completed, `7/98`), `G000391` (Completed, `21/86`), `G000529` (Completed, `19/94`). There are successes (`G000101` `84/74`, `G000390` `88/54`, `G000395` `75/73`, `G000464` `91/68`), but the spread is much wider and the low-end failures are more frequent.

- **HR is mixed, but many misses come from employee-satisfaction and revenue-growth goals with very high targets.** Examples of weak rows: `G000012` (Completed, `6/100`), `G000044` (In Progress, `14/100`), `G000119` (In Progress, `0/60`), `G000203` (In Progress, `2/85`), `G000273` (Completed, `5/100`). HR still has strong exceptions (`G000107` `92/88`, `G000352` `94/79`, `G000416` `81/80`, `G000497` `96/69`), so the issue is not universal underperformance; it is uneven execution across goal types.

- **Finance looks middle-of-the-pack because it has both strong and very weak pockets.** It does well on several `Customer Satisfaction` and `Cost Reduction` items: `G000154` (`89/56`), `G000262` (`92/85`), `G000531` (`78/63`), `G000546` (`82/63`). But `Revenue Growth` and some `Employee Satisfaction` rows lag badly: `G000140` (`13/63`), `G000271` (`0/91`), `G000290` (`22/93`), `G000524` (In Progress, `3/100`), `G000501` (`15/73`).

## Likely reasons for the department gap

1. **Goal mix differs by department.**  
   IT has many internally controlled operational goals (`Efficiency`, support response, automation, cost actions), which appear easier to push to completion. Marketing and HR carry more `Revenue Growth` and broad `Employee Satisfaction` goals, which often have higher targets and more external or cross-team dependencies.

2. **Open/cancelled work is concentrated outside IT.**  
   HR, Finance, and especially Marketing show many `In Progress`, `Planned`, and `Cancelled` rows with low `percent_complete`. That lowers apparent achievement even before checking target attainment.

3. **Completed does not mean achieved, and this hurts Marketing/HR/Finance more.**  
   The file contains many completed-but-missed records outside IT, such as Marketing `G000278` (`3/97`) and HR `G000012` (`6/100`). So the gap is not only about closure rate; it is also about weaker final attainment after closure.

4. **Target ambition matters, but it does not fully explain the gap.**  
   HR, Finance, and Marketing often set `target_percentage` in the 90-100 range and then miss badly. But IT also has ambitious targets and still converts some of them (`G000001` `97/97`, `G000482` `96/96`, `G000156` `93/91`). This points to a real execution difference, not just easier target-setting in IT.

5. **`priority` is weak evidence as an explanation.**  
   IT hits several `High`/`Critical` goals (`G000111`, `G000123`, `G000389`, `G000461`), while other departments miss even `Low`/`Medium` items (`G000103`, `G000119`, `G000529`). Priority labels alone do not explain the departmental gap.

## Exceptions and cautions

- **There are strong exceptions in every department**, so “department” should be read as a proxy for portfolio mix and execution style, not destiny.
- **The `metric` column is not very reliable for causal interpretation** because it often does not match the goal description cleanly.
- **Date-based explanations are weak** because many rows have `end_date` earlier than `start_date`, so schedule duration is not trustworthy in this file.

## Decision-ready take
The department gap is best explained by a combination of **goal portfolio** and **execution quality**. IT appears to outperform because it has more operationally controllable goals and more rows that both close and meet target. Marketing underperforms most clearly because it combines many open/cancelled goals with many completed-but-failed ones. HR and Finance sit between those extremes, with results depending heavily on category: customer satisfaction, cost reduction, and operational efficiency tend to do better than broad employee-satisfaction or revenue-growth targets.
