---
dataset: flag_13
scenario: causal_duration
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: causal_attribution
focus_variable: "resolution_duration_variation"
query: "Why do resolution duration values vary across tickets?"
source_table: augment_table/flag_13/causal_duration/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_13__causal_duration/analyses/original/analysis.md
wall_seconds: 118.06
---

# Resolution duration analysis

## What was measured
- The apparent duration signal is stored in `closed_at` and it exactly matches `sys_updated_on` on every row, formatted like `MM:SS.s`.
- Interpreting that field as duration yields 500 tickets with mean **30.1 min**, median **29.8 min**, and range **0.2 to 60.0 min**.
- Durations are broadly spread across the full range, so variation is real rather than concentrated in a narrow band.

## Main answer
Resolution duration varies across tickets only **weakly** by the visible operational fields. Broad metadata such as `priority`, `state`, `assignment_group`, `category`, and assignee changes average duration by only a few minutes. The clearest differences appear in **specific issue descriptions**, not in the broad labels. Even then, evidence is uneven because many descriptions have small counts.

## Evidence by factor

| Factor | Visible pattern | Strength |
|---|---|---|
| `short_description` | Repeated issue types differ more than broad categories. Examples: `Database connection issue` averages **40.9 min** (n=8), `Cannot connect to office VPN` **35.4 min** (n=6), while `Unable to access database` averages **18.8 min** (n=12) and `Email server down` **13.7 min** (n=5). | Moderate, but noisy |
| `category` | Means are close: `Software` **31.5**, `Hardware` **30.8**, `Network` **30.1**, `Database` **29.2** minutes. | Weak |
| `assignment_group` | Means are also close: `Service Desk` **32.8**, `Hardware` **30.8**, `Database` **30.0**, `Network` **29.9**, `Software` **28.5**. | Weak |
| `priority` | No clear escalation pattern: `3 - Moderate` **31.5**, `1 - Critical` **30.3**, `2 - High` **29.9**. | Weak |
| `assigned_to` / `closed_by` | Assignee means range from **28.8** to **31.1** minutes; closer means range from **28.1** to **32.1**. | Weak; likely reflects ticket mix |
| `opened_at` timing | Some month differences exist: January **34.6**, May **34.7**, June **23.8**, December **32.6**. Some after-hours opening times are also somewhat slower. | Weak-to-moderate |
| `state` | `Closed` **30.3** vs `Resolved` **29.8**. | Negligible |

## Important exceptions and limits
- Most broad-field differences are small relative to the overall spread: the overall standard deviation is **16.8 min**, much larger than most group mean gaps.
- Statistical separation across `state`, `assignment_group`, `priority`, `category`, assignee, and closer is very small, so these are not strong explanations by themselves.
- A predictive check using all visible columns still did **not** explain duration well out of sample, which suggests the main drivers are not captured well in this table.
- Broad groups hide more meaningful subtypes. For example, `Database` tickets include both relatively fast patterns and much slower connection-issue patterns.
- Some standout averages come from small subgroups, so they should be treated as hints, not stable rules.

## Bottom line
From the visible data, resolution duration varies mostly because **specific ticket types differ**, with minor timing effects and only weak evidence for strong differences by priority, group, state, or individual owner. For decisions, the most useful visible signal is the **fine-grained issue description**, but most of the duration spread appears to come from factors **not recorded in this dataset**.
