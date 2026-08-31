---
dataset: flag_6
scenario: causal_agent
variant: original
model: substrate-claude-haiku-4-5
query_subtype: causal_attribution
focus_variable: "agent_resolution_discrepancy"
query: "Why do some agents have longer resolution times?"
source_table: augment_table/flag_6/causal_agent/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_6__causal_agent/analyses/original/analysis.md
wall_seconds: 96.93
---

# Why some agents have longer resolution times

## Bottom line

Longer resolution times are **mostly concentrated in one assignee: Fred Luddy**, and the pattern looks **more like an assignment-specific backlog or time-period effect than a pure ticket-mix effect**.

For completed incidents with valid timestamps, median resolution time by `assigned_to` is:

- **Fred Luddy:** **691.2 hours**
- Luke Wilson: 151.3 hours
- Charlie Whitherspoon: 150.0 hours
- Howard Johnson: 142.8 hours
- Beth Anglin: 124.0 hours

Fred’s median is about **4.7×** the median of the other agents.

## What appears to drive longer times

### 1. A strong assignee-specific backlog pattern
The clearest signal is in `opened_at` and `closed_at`.

For **Fred Luddy**, resolution times rise steadily by open month:

- Jan 2023 median: 117.6h
- Apr 2023: 564.0h
- Jul 2023: 1015.2h
- Sep 2023: 1276.8h
- Nov 2023: 1536.0h

Other agents stay much lower, usually around **100–200h** by month.  
This means the longest times are not random; they accumulate over time in one assignee’s queue.

Visible corroboration:
- Fred has **no valid completed tickets opened in Dec 2023 or Jan 2024**, while other agents do.
- Many of Fred’s tickets close **months after opening**, while most other agents’ tickets close in the same month or the next.

### 2. Ticket type matters, but does not explain the full gap
Some categories are slower overall:

- `category = Software`: median 188.4h
- `Network`: 176.7h
- `Database`: 143.1h
- `Hardware`: 123.1h
- `Inquiry / Help`: 176.5h, but only 7 valid cases

So agents handling more `Network`/`Software`/`Database` work can run longer.  
However, ticket mix is only a **partial** explanation because Fred is still much slower **within the same category**:

- `Network`: Fred **681.6h** vs others **152.6h**
- `Database`: Fred **645.6h** vs others **123.9h**
- `Software`: Fred **832.8h** vs others **129.3h**

His category shares are also not radically different from peers:
- Fred: 57% `Network`, 24% `Database`, 16% `Software`
- Most others are also majority `Network` with meaningful `Database`/`Software` volume

### 3. Priority is not the reason
If long times were driven by harder urgent work, `priority` would likely be higher for slower agents. That is not strongly supported.

Overall median resolution time by `priority`:
- `2 - High`: 172.0h
- `3 - Moderate`: 168.3h
- `1 - Critical`: 148.7h

Fred’s critical-ticket share (17%) is close to peers. So **higher severity does not explain the long tail**.

### 4. Some requester/update patterns are associated with longer times, but evidence is weaker
There are weaker associations in:
- `caller_id`: tickets from **Bud Richman** and **Don Goodliffe** run longer on average than those from `ITIL User`
- `sys_updated_by`: `admin`-updated tickets are slower on average than `employee`-updated tickets

These may reflect more involved workflows, but they do **not** explain the main agent gap on their own.

## Important exceptions and caveats

- The dataset has **data-quality issues**:
  - **22** rows have missing `closed_at`
  - **50** completed rows have negative `closed_at - opened_at`
- This analysis therefore uses **428 completed incidents with non-negative durations**.
- Invalid completed rows are unevenly distributed across agents: Fred has **0 invalid**, while others have **10–14** each. That can affect exact comparisons, but it is too small to explain a gap of this size.
- `assignment_group` and `category` are not always aligned, so category-based interpretation should be treated as directional.

## Decision-ready interpretation

The evidence supports this ranking of likely causes for longer resolution times:

1. **Backlog / queue aging for specific assignees**, especially Fred Luddy  
2. **Some contribution from slower ticket types** (`Network`, `Software`, `Database`)  
3. **Little evidence that priority differences are the main cause**

## Practical implication

If the goal is to reduce resolution time, the first place to investigate is **assignee-level workload management and aging patterns over time**, not priority rules. The data suggests that one agent’s queue became progressively older, and that is the main driver of the longest resolution times.
