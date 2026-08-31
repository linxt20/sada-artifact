---
dataset: flag_9
scenario: predictive_hardware
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "is_hardware_anomaly_window"
query: "What signals indicate a hardware incident is in the anomaly window?"
source_table: augment_table/flag_9/predictive_hardware/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_9__predictive_hardware/analyses/original/analysis.md
wall_seconds: 87.33
---

# Hardware anomaly-window signals

## Bottom line

The strongest indicator is **time**: the anomaly window is an **inferred late-July to mid-August 2023 burst**, centered roughly on **2023-07-19 to 2023-08-17**, because the table has no explicit anomaly flag.

## Signals that a hardware incident is in the anomaly window

1. **`opened_at` falls in the late-July / mid-August 2023 surge**
   - Hardware incidents jump to **44 in 2023-07** and **52 in 2023-08**.
   - Outside those months, hardware volume is only **4 to 12 per month**.
   - In the inferred window alone, there are **90 hardware incidents**, which is about **49%** of all hardware tickets in the full table (**90/182**).

2. **Hardware dominates overall incident mix during that period**
   - In the inferred window, total incidents are **144**, of which **90 are Hardware**.
   - That is **62.5% hardware share** in-window, versus much lower hardware shares in most other months:
     - **2023-07:** **55.0%**
     - **2023-08:** **53.6%**
     - Most other months: about **10.8% to 30.3%**

3. **Daily hardware counts become unusually dense**
   - Peak hardware days occur inside this period:
     - **2023-08-11:** **6**
     - **2023-07-28, 2023-08-03, 2023-08-06, 2023-08-07:** **5 each**
   - The window shows many multi-incident days close together, unlike the sparse pattern elsewhere.

## Secondary patterns

4. **Printer issues are common in-window, but not unique to it**
   - Top in-window descriptions include:
     - `Printer not working properly` (**8**)
     - `Printer is not functioning properly` (**3**)
     - `Printer not functioning properly` (**3**)
   - However, the same printer phrases are also frequent outside the window, so this is a **volume signal**, not a **distinctive signature**.

5. **Monitor and hard-drive issues are somewhat more represented in-window**
   - Inferred issue-family counts:
     - **Monitor:** **16 in-window** vs **12 outside**
     - **Hard drive:** **5 in-window** vs **3 outside**
   - This suggests some broadening beyond printers, but the evidence is **moderate**, not decisive.

## Weak or non-signals

- **`priority` is not a strong separator**
  - In-window hardware tickets are still mostly **`2 - High`** (**68/90**).
  - Critical share is only slightly higher in-window (**9/90**) than outside (**7/92**).
  - This is not strong enough to identify the window by itself.

- **`assigned_to`, `closed_by`, `state`, `caller_id`, `sys_updated_by` are not distinctive**
  - Assignee and closer distributions remain spread across the same few people both in and out of the window.
  - `Resolved` vs `Closed` is also similar in both groups.

- **Power/boot failures are not a window signal**
  - These appear **less common in-window** (**3**) than outside (**10**).

## Decision-ready interpretation

A hardware incident is most likely in the anomaly window when:

- **`category = Hardware`**, and
- **`opened_at` is in late July to mid-August 2023**, especially **2023-07-19 to 2023-08-17**, and
- it appears during a **dense cluster of same-day hardware tickets**.

## Caveats

- The dataset does **not** contain an explicit anomaly-window label, so the window is **inferred from the `opened_at` spike**.
- Description text alone is **not reliable** for identification, because the same printer-related complaints appear both inside and outside the burst.
- The anomaly is therefore best treated as a **temporal concentration of hardware incidents**, not as a unique issue type or workflow pattern.
