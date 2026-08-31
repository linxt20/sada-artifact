---
dataset: flag_2
scenario: predictive_long
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "resolution_time"
query: "What signals suggest an incident will take longer to resolve?"
source_table: augment_table/flag_2/predictive_long/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_2__predictive_long/analyses/original/analysis.md
wall_seconds: 91.49
---

# Signals linked to longer resolution

**Scope.** Resolution time was measured as `closed_at - opened_at` for the **372** incidents with both timestamps. Median resolved time is **1032.0 hours** (~43 days). The top quartile starts at **1557.6 hours** (~65 days). Another **128/500** incidents have no `closed_at`; all are still in `state` **New** or **In Progress**.

## Strongest visible signals

- **Open date / aging effect dominates the table.**  
  By `opened_at` month, median resolution time rises almost monotonically from **135.6h** in **2023-01** to **2104.8h** in **2023-10**. All incidents opened in **2023-11 to 2024-01** are still unresolved. This is the strongest signal in the data, but it likely reflects dataset timing/censoring more than a true operational cause.

- **Network work tends to run longer.**  
  - `category = Network`: median **1046.4h**, long-case rate **27.9%**  
  - `category = Database`: median **967.2h**, long-case rate **20.9%**  
  - `assignment_group = Network`: median **1046.4h**  
  - `assignment_group = Database`: median **960.0h**

- **Overnight openings are slower.**  
  - `opened_at` bucket **overnight (00:00-05:59)**: median **1276.8h**, long-case rate **29.2%**  
  - `morning`: median **837.6h**, long-case rate **19.3%**  
  This is strongest inside network incidents: `category = Network` has median **1428.0h** overnight vs **801.6h** in the morning.

- **Some routing patterns align with longer times.**  
  - `assigned_to = Beth Anglin`: median **1298.4h**, long-case rate **32.9%**  
  - `assigned_to = Fred Luddy`: median **1100.4h**, long-case rate **27.0%**  
  - `assigned_to = Luke Wilson`: median **816.0h**  
  This is operationally useful, but it may reflect ticket mix rather than individual effect.

## Text patterns in `short_description`

Repeated **VPN/connectivity** wording appears in slower tickets:

- `Cannot connect to VPN`: median **1435.2h** (`n = 15`)
- `Cannot connect to office VPN`: median **1370.4h** (`n = 6`)
- `Unable to connect to VPN`: median **1104.0h** (`n = 18`)
- `Email server connectivity issue`: median **1485.6h** (`n = 4`)

Evidence is mixed outside that cluster:

- `Email server not responding`: median **945.6h** (`n = 12`)
- `Unable to access database`: median **816.0h** (`n = 7`)

So the slowest recurring descriptions are more **connectivity/VPN** oriented than broadly **email** or **database**.

## Weaker or mixed signals

- **Priority is not a clean driver.**  
  `1 - Critical` and `3 - Moderate` are somewhat longer than `2 - High` (medians **1255.2h**, **1100.4h**, **974.4h**), but the separation is modest.

- **Day of week is suggestive, not decisive.**  
  Sunday openings are slower (median **1233.6h**) than Thursday openings (**859.2h**), but the pattern is weaker than month or time-of-day.

- **`state` and `sys_updated_by` should be treated cautiously.**  
  They correlate with longer or unresolved cases, but they are lifecycle fields, not stable intake features.

## Decision-ready takeaway

The clearest signals that an incident will take longer to resolve are:

1. **It opens overnight**, especially if it is a **network** issue.
2. **It is a network/VPN/connectivity case**, based on both structured fields and repeated description text.
3. **It follows certain routing patterns** (`assigned_to` differences), though that is likely partly workload/case-mix.

The main caveat is that **`opened_at` month overwhelms this dataset**. Any prediction or operational rule should control for that timing effect first, or it will overstate the importance of the other signals.
