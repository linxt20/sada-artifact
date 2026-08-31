---
dataset: flag_28
scenario: predictive_high
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "high_goal_achievement"
query: "What signals suggest a goal will be highly achieved?"
source_table: augment_table/flag_28/predictive_high/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_28__predictive_high/analyses/original/analysis.md
wall_seconds: 91.72
---

# Signals of high goal achievement

Using `percent_complete` as the visible achievement measure, the top quartile begins at **74%** complete ($141/550$ goals).

## Strongest signals

| Signal | Concrete pattern | Assessment |
|---|---:|---|
| `priority` | Mean `percent_complete`: `High` **76.0%**, `Critical` **75.0%**, vs `Low` **38.4%** and `Medium` **38.3%**. Top-quartile rates: `High` **61.5%**, `Critical` **59.6%**, `Medium` **8.8%**, `Low` **7.0%**. | Strongest signal in the table. Highly achieved goals are concentrated in `High` and `Critical` items. |
| `department` | `IT` has mean `percent_complete` **70.4%** and top-quartile rate **51.9%**. Other departments are much lower: `HR` **44.8%** / **20.7%**, `Finance` **47.8%** / **18.8%**, `Marketing` **42.4%** / **13.5%**. | Strong signal. IT goals are much more likely to be highly achieved. |

## Why those signals look credible

- The `priority` pattern is not only a byproduct of more `Completed` rows. Even within `Completed`, mean completion stays much higher for `High` and `Critical` goals (**79.5%** and **78.1%**) than for `Low` and `Medium` goals (both about **41%**).
- The `department` pattern also persists within status groups. For example, among `Completed` rows, `IT` averages **75.8%** complete, versus **52.5%** in `Finance`, **55.2%** in `HR`, and **47.9%** in `Marketing`.

## Useful but outcome-adjacent signal

- `state` is strongly associated with achievement: `Completed` goals average **59.4%** complete, versus `In Progress` **43.3%** and `Planned` **40.7%**.
- Top-quartile rates are `Completed` **42.5%**, `Cancelled` **16.7%**, `Planned` **9.7%**, and `In Progress` **9.1%**.
- This is informative, but it is partly a status marker rather than a clean early predictor.

## Weak or inconsistent signals

- `target_percentage` does **not** predict achievement here. Its correlation with `percent_complete` is essentially zero at **-0.04**.
- `metric` differences are small: mean completion ranges only from **49.5%** (`Sales Increase`) to **52.6%** (`Expense Ratio`).
- `category` differences are also small: top-quartile rates range from **21.2%** (`Efficiency`) to **28.6%** (`Customer Satisfaction`).
- Planned duration is not useful in this sample: correlation between `duration_days` and `percent_complete` is **-0.04**.

## Text in `description`

Textual wording shows only mild patterns, not strong evidence.

- Goals mentioning words like **“improve”**, **“optimize”**, or **“enhance”** average about **52%–53%** complete, only slightly above the dataset mean (**50.8%**).
- Goals mentioning **“develop”** or **“implement”** average lower, at **46.4%** and **45.7%**.
- These are weak signals and may simply reflect different goal types.

## Important exceptions and limits

- High priority is a strong signal, but not a guarantee: about **38%–40%** of `High`/`Critical` goals still fall below the top-quartile threshold.
- Some `Low` and `Medium` goals are still highly achieved, so priority should not be used deterministically.
- The date fields have quality issues: **82** rows have `end_date` earlier than `start_date`, so schedule-based conclusions are less reliable.

## Decision-ready takeaway

The clearest signals that a goal will be highly achieved are:

1. **`High` or `Critical` priority**
2. **Belonging to the `IT` department**

`state = Completed` is also strongly associated with high achievement, but it functions more as a current-status marker than as an early planning signal. By contrast, target stretch (`target_percentage`), duration, metric, category, and description wording show weak or inconsistent relationships.
