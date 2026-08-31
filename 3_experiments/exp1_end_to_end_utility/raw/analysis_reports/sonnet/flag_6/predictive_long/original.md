---
dataset: flag_6
scenario: predictive_long
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "resolution_time"
query: "What signals suggest an agent's tickets will take longer to resolve?"
source_table: augment_table/flag_6/predictive_long/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_6__predictive_long/analyses/original/analysis.md
wall_seconds: 157.92
---

# Longer-resolution signals in `flag_6__predictive_long.csv`

**Focus variable:** resolution time, calculated as `closed_at - opened_at`.

**Usable data:** 428 of 500 tickets.  
22 rows have missing `closed_at`, and 50 produce negative durations (`closed_at < opened_at`), so findings are directional rather than definitive.

**Baseline:** median resolution time is **6.8 days**.  
The longest quartile starts at **10.8 days**.  
The top decile starts at **24.8 days**.

## Strongest signal

| Signal | Evidence from the table | Readout |
|---|---|---|
| `assigned_to = Fred Luddy` | median **28.8 days**; **80%** of his tickets are in the longest quartile; **all 44** top-decile tickets are his | Strongest visible signal |
| Other `assigned_to` values | Luke Wilson **6.3d**, Charlie Whitherspoon **6.3d**, Howard Johnson **5.9d**, Beth Anglin **5.2d** median | No comparable slowdown |

This assignee effect is not limited to one issue type. Within Fred Luddy’s own tickets, median times stay very high across `Network` (**28.4d**), `Database` (**26.9d**), and `Software` (**34.7d**). That points more to an assignee/backlog workflow effect than to a single category.

## Secondary signals

- **`category` / `assignment_group`**
  - Overall, `Software` tickets are slowest (median **7.8d**), followed by `Network` (**7.4d**).
  - `Database` (**6.0d**) and `Hardware` (**5.1d**) are shorter.
  - `assignment_group = Software` has the highest median (**8.8d**, `n=23`).

- **But this evidence is weaker than it looks.**  
  After excluding Fred Luddy’s tickets, category gaps narrow:
  - `Network`: **6.4d**
  - `Software`: **5.4d**
  - `Database`: **5.2d**
  - `Hardware`: **5.2d**

  So category/group seems secondary and partly driven by assignee mix.

- **`caller_id`**
  - `Bud Richman` tickets are somewhat slower: median **7.9d**, with **31%** in the longest quartile.
  - `David Loo` is lower: median **6.2d**, **22%** long.
  
  This is a modest signal and may reflect issue mix rather than ticket handling.

- **`sys_updated_by`**
  - `admin`: median **7.6d**
  - `system`: **6.8d**
  - `employee`: **6.3d**
  
  This looks more like an operational marker than a clean early predictor.

## Important exceptions

- **`priority` does not signal longer resolution.**
  - `1 - Critical`: **6.2d**
  - `2 - High`: **7.2d**
  - `3 - Moderate`: **7.0d** (`n=28`)
  
  If anything, critical tickets are resolved faster.

- **`state` is not useful for distinguishing long tickets.**
  - `Resolved`: median **7.0d**
  - `Closed`: median **6.8d**

- **`short_description` wording is weak evidence on its own.**  
  Similar issue text can resolve very differently:
  - `Unable to connect to VPN` (22 tickets): median **10.4d**
  - `Cannot connect to VPN` (15 tickets): median **6.7d**

## Decision-ready conclusion

The clearest signal that a ticket will take longer is **which agent it is assigned to**, especially **Fred Luddy** in this dataset. Category and assignment group add some signal, with **Software** and **Network** tending slower overall, but much of that appears to be explained by **assignee mix**. `Priority` is not a delay signal here, and description text is inconsistent.

**Practical takeaway:** treat **assignee** as the primary flag for long resolution time in this table; use **category/group** only as secondary context, and avoid overinterpreting the result because one assignee accounts for all extreme-duration tickets and 72 rows are unusable for duration analysis.
