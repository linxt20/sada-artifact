---
dataset: flag_19
scenario: predictive_declined
variant: original
model: substrate-claude-haiku-4-5
query_subtype: predictive_feature_engineering
focus_variable: "state_declined"
query: "What signals suggest an expense will be declined?"
source_table: augment_table/flag_19/predictive_declined/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_19__predictive_declined/analyses/original/analysis.md
wall_seconds: 48.3
---

# Expense decline signals

## Scope
This dataset has **500 expenses** with `state` as the focus variable. **46 rows are `Declined`** ($9.2\%$), compared with `Processed` (333), `Pending` (80), and `Submitted` (41).

## Stronger signals associated with decline

### 1. `department = IT` is the clearest visible signal
Decline rates by `department`:

- **IT:** 19 of 43 declined (**44.2%**)
- HR: 2 of 14 (**14.3%**)
- Finance: 2 of 22 (**9.1%**)
- Customer Support: 16 of 267 (**6.0%**)
- Development: 1 of 20 (**5.0%**)
- Sales: 6 of 122 (**4.9%**)
- Product Management: 0 of 12

This is the strongest pattern in the table. Declines are heavily concentrated in **IT**.

### 2. Some `category` values are somewhat more decline-prone
Decline rates by `category`:

- **Miscellaneous:** 3 of 17 (**17.6%**)
- **Travel:** 10 of 94 (**10.6%**)
- Assets: 27 of 310 (**8.7%**)
- Services: 6 of 79 (**7.6%**)

`Travel` and `Miscellaneous` look somewhat more exposed than average, but the `Miscellaneous` sample is small.

### 3. Certain request descriptions recur in declined rows
Declined rows often include:

- **auto-generated / automatically generated** requests
- **hardware / asset** creation language
- **travel equipment** purchases
- repeated laptop/device names such as **Dell Latitude**, **OptiPlex**, and related hardware references in `short_description` or `ci`

Examples visible in declined rows include:

- “Automatically generated asset line for creation of hardware”
- “Travel-related hardware assets acquisition”
- “Dell Latitude 7390 Laptop Asset”
- “Automatically generated service asset”

This suggests declines are common among **system-generated hardware/asset requests**, especially in IT-related workflows.

## Weaker or mixed signals

### 4. Lower-to-mid `amount` values are not safer
Decline rates by `amount` band:

- $\leq \$1k$: **12.5%**
- \$1k–\$2k: **12.5%**
- \$2k–\$5k: **9.9%**
- \$5k–\$10k: **6.7%**

In this table, **smaller expenses are not less likely to be declined**. If anything, declines skew slightly lower than processed items. Still, the gradient is not large enough to treat amount as a primary signal.

### 5. Missing `source_id` is only a weak signal
- `source_id` present: 33 of 389 declined (**8.5%**)
- `source_id` missing: 13 of 111 declined (**11.7%**)

Missing `source_id` may indicate slightly higher decline likelihood, but the difference is modest.

## Important exception: avoid overusing `processed_date`
All declined rows have missing `processed_date`, but so do all `Pending` and `Submitted` rows. That means:

- `processed_date` missing is **not a useful early warning signal for decline specifically**
- it mainly indicates the expense was **not processed**

So this field separates `Processed` from everything else, not `Declined` from other unresolved states.

## Decision-ready takeaways
The most credible signals that an expense will be declined are:

1. **IT department ownership**
2. **Travel or miscellaneous request category**
3. **Auto-generated hardware/asset request language** in `short_description`
4. **Recurring hardware/device references** in `ci` and descriptions, especially laptop/desktop asset records

## Confidence and limits
Evidence is strongest for **`department`**. Evidence for `category`, `amount`, and text patterns is **directional but weaker**. Also, many declined rows are in `Assets`, but that alone is **not** a strong discriminator because `Assets` is also the dominant category overall.
