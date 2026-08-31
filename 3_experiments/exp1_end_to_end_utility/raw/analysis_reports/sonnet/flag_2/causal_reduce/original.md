---
dataset: flag_2
scenario: causal_reduce
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: what_if
focus_variable: "resolution_time"
query: "How can we reduce incident resolution time?"
source_table: augment_table/flag_2/causal_reduce/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_2__causal_reduce/analyses/original/analysis.md
wall_seconds: 134.91
---

# How to reduce incident resolution time

## Bottom line
The strongest lever is **backlog control plus better first routing**.

Using `closed_at - opened_at` as resolution time, the 372 resolved tickets have a median of **1,032 hours** (~43 days). Resolution time rises almost steadily by `opened_at` month, from **136h in Jan** to **2,105h in Oct**. That pattern is much larger than any single priority or team effect, so queue aging appears to be the main issue.

## What the data shows

| Pattern | Evidence from columns | Implication |
| --- | --- | --- |
| Backlog/aging dominates | Median resolution time by `opened_at` month: Jan **136h**, Apr **773h**, Jul **1,439h**, Oct **2,105h** | Reduce queue age first; small workflow tweaks alone will not offset a growing backlog |
| Network is the biggest slow area | `category = Network` is **269/500** tickets; resolved network median is **1,046h** vs **967h** for Database | Improvements in Network handling should move overall time most |
| Correct routing helps | When `category` matches `assignment_group`, median is **1,003h**; when mismatched, **1,061h** | Fewer handoffs should reduce delay |
| Software tickets do better in Software | For `category = Software`, median by `assignment_group`: **Software 823h**, **Service Desk 1,079h**, **Network 1,118h** | Route software incidents directly to the Software team |
| Overnight intake is slower | `opened_at` 00:00-05:59 median is **1,277h** vs **838h** for 06:00-11:59 | Add overnight triage or a strict morning sweep |
| Open queue is material | **128/500** tickets have no `closed_at`; all are `state = New` or `In Progress` | Faster closure also requires tighter follow-up on open work |

## Recommended actions

1. **Cut backlog age in each queue**
   - Manage by oldest `opened_at` first within each `assignment_group`.
   - Add aging thresholds and escalations before tickets sit for weeks.
   - Monitor median age of open tickets, not only ticket volume.

2. **Improve first assignment**
   - Route by `category` to the matching `assignment_group` by default.
   - Highest-confidence rule from this dataset: send `Software` tickets to **Software**, not **Service Desk** or **Network**.
   - Audit misrouted Network tickets and handoffs.

3. **Focus on the Network queue first**
   - It is both the **largest** category and a **slower-than-average** one.
   - This is the best place to improve total resolution time fastest.

4. **Add early-day triage coverage**
   - Tickets opened overnight resolve slower than morning-created tickets.
   - A practical step is a dedicated next-morning sweep for overnight incidents.

5. **Do not rely on priority changes alone**
   - Resolved `1 - Critical` tickets have a higher median (**1,255h**) than `2 - High` (**974h**).
   - That suggests labels alone are not fixing delay; routing and queue age are stronger levers here.

## Important cautions
- The month trend is unusually strong and may reflect backlog buildup, a reporting cutoff, or synthetic-data behavior. It is still the clearest visible pattern.
- Staff-level differences in `assigned_to` exist, but they are weaker once the strong month trend is considered. Use them for workload review, not blame.
- `Hardware` and `Inquiry / Help` have small sample sizes, so those patterns are weak evidence.

## Decision-ready takeaway
To reduce incident resolution time, **prioritize backlog reduction and correct first assignment**, starting with the **Network** queue and direct routing of **Software** incidents to the **Software** group. Add **overnight-to-morning triage** as a secondary improvement. The data supports **process and queue fixes** more strongly than personnel or priority-label changes.
