---
dataset: flag_13
scenario: predictive_long
variant: original
model: substrate-claude-haiku-4-5
query_subtype: predictive_feature_engineering
focus_variable: "duration_like_resolution_value"
query: "What signals are linked to longer resolution duration values?"
source_table: augment_table/flag_13/predictive_long/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_13__predictive_long/analyses/original/analysis.md
wall_seconds: 85.45
---

# Analysis: signals linked to longer resolution-duration values

## Outcome used
The visible duration-like field is `closed_at` (identical to `sys_updated_on` in all 500 rows), formatted like `59:57.2` rather than a timestamp. Interpreting that as the resolution-duration measure:

- Median duration: **29.85**
- 75th percentile: **45.06**
- 90th percentile: **52.60**

## Stronger signals

| Signal | Evidence linked to longer durations | Strength |
|---|---|---|
| `short_description` mentions **network/connectivity/internet** | Mean duration **31.63** vs overall **30.05**; **34.5%** fall in the top quartile | Strongest text-pattern signal |
| Some exact issue labels are much longer | `Database connection issue` mean **40.85**; `Unable to access the database server` **37.55**; `Cannot connect to office VPN` **35.41** | Strong, but some labels have small $n$ |
| `assignment_group = Service Desk` | Mean **32.81**; **14.7%** in top decile | Moderate, but only **34** rows |
| `category = Software` | Mean **31.55**; **15.1%** in top decile | Moderate |
| `sys_updated_by = employee` | Mean **31.40** vs `admin` **29.10** and `system` **29.50** | Moderate operational signal |
| `caller_id = Bud Richman` | Mean **31.64**; **28.3%** in top quartile | Moderate, likely routing/user-mix effect |

## Patterns worth attention

### 1. Network/connectivity wording is the clearest recurring long-duration signal
Issue text containing terms such as network, connectivity, or internet skews longer than the dataset overall.

Examples among frequent descriptions:

- `Database connection issue`: **40.85**
- `Unable to access the database server`: **37.55**
- `Cannot connect to office VPN`: **35.41**
- `Unable to access VPN`: **35.28**

This suggests that connection-oriented incidents, especially when framed as infrastructure or server access problems, are more associated with long durations than generic access tickets.

### 2. Software and Service Desk cases run somewhat longer
By structured fields:

- `category = Software`: mean **31.55**
- `assignment_group = Service Desk`: mean **32.81**
- `assignment_group/category` mismatch rows: mean **31.14** vs **29.87** for matched rows

This points to slightly longer handling when routing is less direct or when the ticket sits in software/service-desk workflows. The mismatch effect is present but not large.

### 3. Timing by `opened_at` month shows variation
Longer average durations appear in:

- January: **34.57** ($n=79$)
- May: **34.66** ($n=24$)
- December: **32.62** ($n=64$)

Shorter months include:

- June: **23.82** ($n=25$)
- April: **25.81** ($n=17$)

This is a visible pattern, but it should be treated cautiously because some month sample sizes are small.

## Weak or inconsistent signals

### Priority is not a useful separator here
Despite intuitive expectations, `priority` shows little discrimination:

- `3 - Moderate`: **31.45** mean
- `1 - Critical`: **30.35**
- `2 - High`: **29.93**

Also, **391/500** tickets are `2 - High`, so the field has limited spread.

### State is nearly neutral
- `Closed`: **30.29**
- `Resolved`: **29.79**

This is too small to treat as a meaningful signal.

### Personnel fields show modest differences, not strong effects
Examples:

- `assigned_to`: Charlie Whitherspoon **31.10**, Fred Luddy **30.69**, Howard Johnson **28.78**
- `closed_by`: Beth Anglin **32.08**, Charlie Whitherspoon **28.06**

These gaps are visible but modest and may reflect ticket mix rather than a stable duration driver.

## Important exceptions
Semantically similar issue labels can behave very differently:

- `Cannot connect to office VPN`: **35.41**
- `Cannot connect to VPN`: **23.35**

Likewise:

- `Unable to access the database server`: **37.55**
- `Unable to access database`: **18.76**

This suggests inconsistent wording or heterogeneous cases inside similar labels. Text signals are useful, but exact phrasing should not be over-interpreted without normalization.

## Bottom line
The clearest links to longer resolution-duration values are:

1. **Connection/infrastructure-style issue text**, especially network, connectivity, VPN, and database-server wording.
2. **Service Desk and Software workflows**, which are somewhat slower on average.
3. **Some month-level timing effects** from `opened_at`, though these are less reliable.

By contrast, **priority** and **state** are weak signals in this dataset. The main caution is that several text-based patterns rely on inconsistent ticket wording and some small subgroups.
