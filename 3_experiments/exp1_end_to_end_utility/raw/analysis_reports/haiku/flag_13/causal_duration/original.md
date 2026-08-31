---
dataset: flag_13
scenario: causal_duration
variant: original
model: substrate-claude-haiku-4-5
query_subtype: causal_attribution
focus_variable: "resolution_duration_variation"
query: "Why do resolution duration values vary across tickets?"
source_table: augment_table/flag_13/causal_duration/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_13__causal_duration/analyses/original/analysis.md
wall_seconds: 209.35
---

# Why resolution duration values vary across tickets

## Bottom line

Resolution duration varies primarily with **issue type/subtype** and **how the ticket is routed/handled**, while visible fields like **priority** and **final state** explain relatively little on their own.

## Data note

This file does **not** contain a normal close timestamp. The visible duration-like field is `closed_at`, and it is identical to `sys_updated_on` in every row, formatted like `mm:ss.s`. The analysis below treats that field as the duration proxy. Because of that schema issue, causal claims should be kept conservative.

## What the data shows

### 1. Durations are widely spread
Across 500 tickets, the duration proxy ranges from **10.9 sec** to **3597.2 sec**; median is **1790.9 sec** ($\approx 29.8$ min), with an interquartile range of **956.0 to 2703.8 sec** ($\approx 15.9$ to $45.1$ min).  
So the variation is not minor noise; tickets differ by nearly the full 0–60 minute range.

### 2. Ticket content matters more than status or priority
By `category`, average durations differ, but only moderately:

| Category | Count | Mean duration |
|---|---:|---:|
| `Software` | 73 | 1892.7 sec |
| `Hardware` | 25 | 1847.4 sec |
| `Network` | 260 | 1804.7 sec |
| `Database` | 134 | 1749.9 sec |
| `Inquiry / Help` | 8 | 1682.6 sec |

The stronger signal is in `short_description`:

- Frequent VPN tickets differ a lot by subtype:
  - `Unable to connect to VPN` ($n=28$): **1787.4 sec**
  - `Cannot connect to VPN` ($n=18$): **1401.0 sec**
  - `Cannot connect to office VPN` ($n=6$): **2124.4 sec**
- Database access problems also vary sharply:
  - `Unable to access database` ($n=12$): **1125.5 sec**
  - `Database connection issue` ($n=8$): **2451.2 sec**
  - `Unable to access the database server` ($n=5$): **2252.7 sec**
- Email/server wording shows similar spread:
  - `Email server down` ($n=5$): **822.0 sec**
  - `Email server not responding` ($n=20$): **1590.8 sec**
  - `Email server outage` ($n=5$): **1908.5 sec**

This suggests duration differences are driven less by broad category labels and more by the **specific failure mode** described in the ticket.

### 3. Routing/ownership is a plausible driver
Average duration also shifts by handling fields:

| Field | Highest visible group | Mean | Lowest visible group | Mean |
|---|---|---:|---|---:|
| `assignment_group` | `Service Desk` | 1968.6 sec | `Software` | 1707.3 sec |
| `assigned_to` | `Charlie Whitherspoon` | 1865.9 sec | `Howard Johnson` | 1726.9 sec |
| `closed_by` | `Beth Anglin` | 1924.9 sec | `Charlie Whitherspoon` | 1683.5 sec |

More importantly, within the same `category`, mismatched routing is often slower:

- `Software` tickets handled by:
  - `Database` group ($n=3$): **3015.6 sec**
  - `Service Desk` ($n=28$): **2154.3 sec**
  - `Software` ($n=29$): **1700.7 sec**
  - `Network` ($n=13$): **1498.5 sec**

That pattern is consistent with **escalation or less direct ownership** increasing duration. Evidence is weaker for tiny groups, but the direction is consistent enough to matter operationally.

### 4. Time-of-opening has a secondary effect
The `opened_at` timestamp shows some timing differences:

- By month:
  - higher means in **January** (**2074.0 sec**) and **May** (**2079.8 sec**)
  - lower means in **June** (**1429.0 sec**) and **April** (**1548.4 sec**)
- By day of week:
  - **Saturday/Sunday**: about **1875–1877 sec**
  - **Monday/Thursday**: about **1724–1743 sec**

This is consistent with a **staffing or workload effect**, but it is not clean evidence. Month-level results may partly reflect changing ticket mix, and some months have small counts.

### 5. Priority and final state are weak explanations
If duration were mainly driven by declared urgency, `priority` should separate clearly. It does not:

- `3 - Moderate`: **1887.1 sec** ($n=24$)
- `1 - Critical`: **1820.7 sec** ($n=83$)
- `2 - High`: **1795.7 sec** ($n=391$)

`state` is also very similar:

- `Closed`: **1817.4 sec**
- `Resolved`: **1787.4 sec**

So the visible evidence does **not** support a simple story that higher-priority or resolved-vs-closed tickets systematically take longer.

## Important exceptions

- Even near-identical tickets can have extreme spread:
  - `Unable to access company database` ($n=13$) ranges from **10.9 sec** to **3377.8 sec**
  - `Email server not responding` ($n=20$) ranges from **25.7 sec** to **3552.0 sec**
- Some apparent patterns rely on small groups:
  - `Inquiry / Help` ($n=8$)
  - `Hardware` assignment group ($n=10$)
  - `Software` tickets routed to `Database` ($n=3$)
  - `Network` tickets routed to `Service Desk` ($n=4$)

These exceptions imply that **unobserved factors** also matter, such as severity within a description, hidden escalation steps, dependencies, or data-generation artifacts.

## Decision-ready conclusion

The best-supported explanation is:

1. **Specific problem subtype** in `short_description` is the main visible source of duration variation.
2. **Routing/ownership path** (`assignment_group`, `assigned_to`, `closed_by`) likely adds delay, especially when tickets are handled outside their most natural group.
3. **Timing effects** from `opened_at` may contribute, but evidence is secondary.
4. **Priority** and **state** are poor standalone explanations in this dataset.

Given the schema caveat around `closed_at`, the safest operational takeaway is to focus first on **ticket routing quality** and **high-variance issue subtypes**, not on priority labels alone.
