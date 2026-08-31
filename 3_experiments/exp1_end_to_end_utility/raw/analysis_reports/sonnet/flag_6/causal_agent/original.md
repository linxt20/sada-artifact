---
dataset: flag_6
scenario: causal_agent
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: causal_attribution
focus_variable: "agent_resolution_discrepancy"
query: "Why do some agents have longer resolution times?"
source_table: augment_table/flag_6/causal_agent/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_6__causal_agent/analyses/original/analysis.md
wall_seconds: 94.42
---

# Why do some agents have longer resolution times?

Resolution time was derived as `closed_at - opened_at`. Because the table contains **50 negative durations** and **22 missing close times**, the comparison below uses the **428 non-negative rows**.

## Main finding

Longer resolution times are concentrated in **one assignee: `Fred Luddy`**. The other agents are relatively similar, so the table does **not** suggest that all slower agents simply received much harder tickets.

Usable-ticket resolution times by `assigned_to`:

- `Fred Luddy`: **mean 750h**, **median 691h**, `n=76`
- `Luke Wilson`: **mean 160h**, **median 151h**, `n=90`
- `Howard Johnson`: **mean 160h**, **median 143h**, `n=88`
- `Charlie Whitherspoon`: **mean 150h**, **median 150h**, `n=89`
- `Beth Anglin`: **mean 136h**, **median 124h**, `n=85`

## What seems to drive the difference

### 1. Visible case mix does not explain most of it

Workload mix is fairly similar across agents.

By `category`, every agent is still mostly handling `Network` work:

- `Network`: about **54%–59%** of tickets for each agent
- `Database`: about **17%–24%**
- `Software`: about **10%–20%**

Despite that similar mix, `Fred Luddy` is slower **within the same categories**:

- `Network`: **762h** mean for Fred vs **128–177h** for others
- `Database`: **707h** vs **126–154h**
- `Software`: **851h** vs **108–168h**

The same pattern appears in `assignment_group`:

- `Network` group: Fred **742h** vs others **132–171h**
- `Database` group: Fred **715h** vs others **128–158h**
- `Software` group: Fred **1024h** vs others **70–236h**

This points to an **assignee-specific pattern**, not just ticket-type mix.

### 2. Extreme long-tail tickets are concentrated under one agent

The gap is driven by very long cases.

For `Fred Luddy`:

- **89%** of tickets exceed **7 days**
- **71%** exceed **14 days**
- **46%** exceed **30 days**

For every other agent:

- **35%–47%** exceed **7 days**
- **0%–9%** exceed **14 days**
- **0%** exceed **30 days**

A concrete pattern: the **top 20 longest tickets** are all assigned to `Fred Luddy`, across `Network`, `Database`, and `Software` issues such as VPN, intranet, database server, and operating-system problems.

### 3. Calendar timing may contribute, but it is secondary

Overall mean resolution time rises in **Sep–Nov 2023** (roughly **378h–462h** by opened month), which is consistent with a backlog period. But Fred’s tickets are much slower in nearly every month, and that gap remains large even after controlling for:

- `category`
- `priority`
- `state`
- `opened_month`

In a simple controlled log-time model, `Fred Luddy` still has a large positive effect (**about +1.69 log-hours**), while the other agents are not meaningfully different from the baseline.

## Factors with weaker evidence

- `Software` and `Network` tickets are somewhat slower overall than `Hardware` or `Inquiry / Help`, but those differences are weak once assignee is considered.
- `Resolved` tickets are somewhat slower than `Closed` tickets, but the gap is modest.
- `Priority` does **not** explain longer times here; `1 - Critical` tickets are not slower than `2 - High` or `3 - Moderate`.

## Caveats

- Data quality is important: **50 negative durations** and **22 missing close times**. Negative durations are concentrated in non-Fred agents, so raw averages on all 500 rows would understate the true gap.
- The table has no direct fields for backlog, escalations, reopenings, dependencies, or true technical complexity. So the data supports an **agent-linked delay pattern**, not a definitive root cause.

## Decision-ready answer

In this table, longer resolution times are mainly associated with a **persistent assignee effect centered on `Fred Luddy`**, not with visible differences in `category`, `assignment_group`, `priority`, or `state`. The most plausible interpretation from the available columns is **queue/backlog or process differences attached to that assignee**, because the slowdown appears across issue types, across months, and in nearly all extreme-duration cases. Secondary factors such as `Network`/`Software` work and late-2023 timing may contribute, but they are weaker than the assignee-specific pattern.
