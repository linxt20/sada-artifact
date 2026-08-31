---
dataset: flag_2
scenario: causal_reduce
variant: original
model: substrate-claude-haiku-4-5
query_subtype: what_if
focus_variable: "resolution_time"
query: "How can we reduce incident resolution time?"
source_table: augment_table/flag_2/causal_reduce/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_2__causal_reduce/analyses/original/analysis.md
wall_seconds: 70.88
---

# Reduce incident resolution time

## Decision summary

The focus variable is **resolution time**, computed from `closed_at - opened_at` for completed incidents. In this dataset, **372 of 500 incidents are completed** and their **median resolution time is 1,032 hours** (about **43 days**). The largest practical levers are:

1. **Reduce the open backlog earlier**, especially tickets still in `New` or `In Progress`.
2. **Improve routing in the `Network` and `Database` queues**, which carry most volume.
3. **Route by assignee-topic fit**, because some assignees are consistently faster within the same work type.
4. **Expedite `1 - Critical` incidents**, which are currently slower than `2 - High`.

## What the data shows

### 1) Backlog is the clearest drag on resolution time
- **128 of 500 incidents are still unresolved**.
- All unresolved tickets are in `state = New` (**65**) or `In Progress` (**63**).
- **65 unresolved tickets have no `assigned_to` value**, indicating a large unassigned backlog.
- Open volume is concentrated in:
  - `assignment_group = Network`: **79 open**
  - `assignment_group = Database`: **32 open**
  - `priority = 2 - High`: **97 open**
  - `category = Network`: **72 open**

**Implication:** the fastest way to reduce end-to-end resolution time is to shorten time-to-assignment and time spent sitting in `New`.

### 2) Network incidents are the biggest improvement opportunity
- `assignment_group = Network` handles **300 of 500 incidents**.
- Its completed-ticket median is **1,046.4 hours**, slower than `Database` (**960.0**) and `Software` (**823.2**).
- It also has the largest unresolved backlog: **79 open**.

At the category level:
- `category = Network`: **269 incidents**, median **1,046.4 hours**, **72 open**
- `category = Database`: **116 incidents**, median **967.2 hours**, **30 open**

**Implication:** even a modest improvement in the Network queue should produce the largest overall reduction.

### 3) Assignee-topic fit appears to matter
Overall completed-ticket medians by `assigned_to`:
- `Luke Wilson`: **816.0 hours**, **85.0%** completed
- `Howard Johnson`: **909.6 hours**, **85.2%** completed
- `Charlie Whitherspoon`: **1,060.8 hours**, **84.5%** completed
- `Fred Luddy`: **1,100.4 hours**, **87.1%** completed
- `Beth Anglin`: **1,298.4 hours**, **85.9%** completed

Within the highest-volume `Network` group, the gaps are large:
- `Luke Wilson`: **736.8 hours**
- `Howard Johnson`: **816.0 hours**
- `Charlie Whitherspoon`: **988.8 hours**
- `Fred Luddy`: **1,334.4 hours**
- `Beth Anglin`: **1,363.2 hours**

Within `Database`:
- `Beth Anglin`: **744.0 hours**
- `Fred Luddy`: **790.8 hours**
- `Luke Wilson`: **812.4 hours**
- `Howard Johnson`: **1,053.6 hours**
- `Charlie Whitherspoon`: **1,334.4 hours**

**Implication:** routing should not be generic. Match incident type to the fastest assignee for that queue.

### 4) Critical incidents are not being resolved faster
Completed-ticket medians by `priority`:
- `2 - High`: **974.4 hours**
- `3 - Moderate`: **1,100.4 hours**
- `1 - Critical`: **1,255.2 hours**

Completion rates are also not better for critical work:
- `1 - Critical`: **72.2%**
- `2 - High`: **74.5%**

**Implication:** the current process does not show effective fast-tracking for critical incidents.

## Recommended actions

### A. Enforce rapid assignment
- Set an SLA for moving tickets out of `New` quickly.
- Auto-assign or triage unassigned work first, since **65 open tickets have no assignee**.
- Start with `Network` and `Database`, where most open work sits.

### B. Rebalance Network work by observed speed
- Send more `Network` incidents to the faster assignees in this dataset, especially `Luke Wilson` and `Howard Johnson`.
- Review why `Network` tickets assigned to `Beth Anglin` and `Fred Luddy` have much longer medians.

### C. Use skills-based routing for Database work
- Prefer `Beth Anglin`, `Fred Luddy`, or `Luke Wilson` for `Database` incidents based on observed medians.
- Review whether slower pairings reflect harder case mix or avoidable routing inefficiency.

### D. Create a true critical-incident fast path
- `1 - Critical` tickets should have tighter triage, assignment, and escalation rules.
- Monitor whether critical tickets are waiting unassigned or sitting in `In Progress`.

### E. Follow up on employee-updated tickets
- Tickets with `sys_updated_by = employee` have a much lower completion rate: **57.9%** vs about **85%** for `admin` and `system`.
- This may indicate requester-dependent delays, missing information, or stalled communication.
- Use reminder workflows and closure/follow-up rules for these cases.

## Important caveats

- The dataset is **right-censored by time**: incidents opened in **2023-11 to 2024-01** are all still open, so later months cannot be used to claim the process definitely worsened.
- Resolution times rise sharply by opening month for completed tickets, but part of that pattern is likely due to the dataset cutoff rather than only operational decline.
- Assignee comparisons are useful, but some differences may reflect unobserved case difficulty because the dataset lacks effort, reopen, transfer, or full workflow-history fields.

## Bottom line

To reduce incident resolution time, prioritize **faster assignment**, especially for the **65 unassigned open tickets**; focus process improvement on the **Network** queue; and apply **skills-based routing** because assignee performance differs materially within the same work type. The evidence is strongest for backlog control and queue/assignee routing, and weaker for any claim that time trends alone reflect worsening operations.
