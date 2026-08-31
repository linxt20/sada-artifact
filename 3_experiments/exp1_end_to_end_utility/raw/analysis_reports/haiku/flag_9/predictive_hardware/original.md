---
dataset: flag_9
scenario: predictive_hardware
variant: original
model: substrate-claude-haiku-4-5
query_subtype: predictive_feature_engineering
focus_variable: "is_hardware_anomaly_window"
query: "What signals indicate a hardware incident is in the anomaly window?"
source_table: augment_table/flag_9/predictive_hardware/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_9__predictive_hardware/analyses/original/analysis.md
wall_seconds: 88.69
---

# Hardware incident anomaly-window signals

## Bottom line

The clearest signal is **`opened_at` timing**. The data shows an inferred hardware anomaly window of **2023-07-19 to 2023-08-17**, where hardware incidents surge far above baseline.

## Strong signals

| Signal | Evidence from the table |
|---|---|
| **`opened_at` falls in late Jul to mid Aug 2023** | **90 of 182** hardware incidents occur in this **30-day** span, even though that span is only **30 of 396 days** in the dataset. Hardware runs at **3.0 incidents/day** in the window vs **0.25/day** outside, about **12x higher**. |
| **Hardware dominates incident mix during that span** | In the same window, **90 of 144** total incidents are `category = Hardware` (**62.5%**). Outside it, hardware is only **92 of 456** (**20.2%**). |
| **Sustained daily cluster, not a one-day spike** | Hardware appears on **29 of 30 days** in the window. Daily hardware counts are usually **2 to 5**, peaking at **6 on 2023-08-11**. Monthly hardware volume is **44 in 2023-07** and **52 in 2023-08**, versus only **4 to 12** in every other month. |

## Secondary signals

`short_description` suggests the window is driven by a burst of repeated end-user hardware failures, especially:

- **Printers**
- **Monitors / displays**
- **Keyboards**
- **Desktop / boot failures**
- **Drive / storage faults**

Examples inside the burst include `Printer not working properly`, `Monitor screen flickering`, `Keyboard malfunction on workstation`, `Disk drive failure on office desktop`, and `Unable to turn on the office computer`.

## Weak or non-distinguishing signals

These fields do **not** separate the anomaly window well:

- **`priority`**: mostly `2 - High` both inside and outside the window.
- **`state`**: `Resolved` and `Closed` appear in similar proportions inside and outside.
- **`assigned_to`**, **`caller_id`**, **`closed_by`**, **`sys_updated_by`**: the same small set of names appears throughout the dataset.
- **`assignment_group`**: almost always `Hardware` for hardware incidents, so it adds little.

## Important exceptions

- **Description alone is weak evidence.** Printer incidents are common both inside and outside the anomaly window, so a printer ticket by itself is not enough.
- The window boundary is **inferred from the `opened_at` spike**; there is **no explicit anomaly label** in the table.
- The cluster is strong but not perfectly continuous: **2023-08-08** has no hardware openings.

## Decision-ready rule

A hardware incident is likely in the anomaly window when:

1. **`category = Hardware`**
2. **`opened_at` is in the late-July to mid-August 2023 surge**, especially **2023-07-19 through 2023-08-17**

Use `short_description` only as supporting context. The **date pattern** is the main signal.
