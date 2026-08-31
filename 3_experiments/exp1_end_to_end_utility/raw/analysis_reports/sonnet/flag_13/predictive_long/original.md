---
dataset: flag_13
scenario: predictive_long
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "duration_like_resolution_value"
query: "What signals are linked to longer resolution duration values?"
source_table: augment_table/flag_13/predictive_long/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_13__predictive_long/analyses/original/analysis.md
wall_seconds: 102.65
---

# Resolution-duration signals

## Scope
- The duration field appears to be `closed_at`, which is formatted as `mm:ss.s`. `sys_updated_on` is identical to it in all 500 rows, so the analysis uses `closed_at` as the resolution-duration measure.
- Overall resolution duration is centered around **29.9 min median** and **30.1 min mean**. The **top quartile** starts at **45.1 min** and the **top decile** at **52.6 min**.

## Signals linked to longer durations

### 1. Time opened shows the clearest pattern, though still modest
- **Month opened**
  - **May** and **January** have the longest averages: **34.7 min** and **34.6 min**.
  - **December** is also elevated at **32.6 min**.
  - By contrast, **June** averages **23.8 min** and **August/October** are around **27 min**.
- **Hour opened**
  - Tickets opened around **02:00** and **17:00-20:00** average about **35-36 min**.
  - This is directionally useful, but each hour bucket only has about **17-25 tickets**, so evidence is limited.

### 2. Software and service-desk routing trend longer
- `category = Software` has the longest category average at **31.6 min**, with **33.5 min median**.
- `assignment_group = Service Desk` is the longest group at **32.8 min** mean, with **29.4%** of its tickets in the top quartile.
- This is not a broad “all software handling” effect: `assignment_group = Software` averages only **28.5 min**. The stronger signal is **software-like issues reaching the service desk**.

### 3. Some workflow/reporter fields tilt longer, but weakly
- `sys_updated_by = employee` averages **31.4 min**, versus **29.5 min** for `system` and **29.1 min** for `admin`.
- `caller_id = Bud Richman` averages **31.6 min**, the highest among callers.
- Assignee/closer differences exist, but they are small and likely reflect workflow mix more than intrinsic ticket difficulty.

### 4. Certain issue descriptions are associated with longer cases
Repeated descriptions with higher average durations include:
- **Cannot connect to database**: **49.4 min** (\(n = 4\))
- **Database connection issue**: **40.9 min** (\(n = 8\))
- **Cannot connect to the VPN**: **40.9 min** (\(n = 4\))
- **Unable to access company VPN**: **38.7 min** (\(n = 4\))
- **Internet connection unstable**: **38.1 min** (\(n = 4\))

Keyword-level patterns are weaker but similar:
- `account`: **39.7 min** (\(n = 8\))
- `network`: **33.4 min** (\(n = 36\))
- `vpn`: **30.2 min** (\(n = 108\))

## Weak or inconsistent signals
- `priority` is not a strong separator:
  - **Critical**: **30.4 min**
  - **High**: **29.9 min**
  - **Moderate**: **31.5 min**
- `state` is also nearly flat:
  - **Closed**: **30.3 min**
  - **Resolved**: **29.8 min**
- Broad category differences are small outside the software lift:
  - **Network**: **30.1 min**
  - **Database**: **29.2 min**
  - **Hardware**: **30.8 min**
- Several of the highest-duration text patterns have very small sample sizes, so they should be treated as leads, not stable rules.

## Bottom line
Longer resolution durations are linked most clearly to **when the ticket was opened**, with a smaller but consistent pattern around **software/service-desk cases** and **database/VPN/network connectivity issues**. Most other visible fields show only **weak separation**, so these signals are better used for **triage support** than as strong standalone predictors.
