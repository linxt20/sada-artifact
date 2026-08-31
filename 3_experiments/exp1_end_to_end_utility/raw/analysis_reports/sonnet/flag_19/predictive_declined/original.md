---
dataset: flag_19
scenario: predictive_declined
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "state_declined"
query: "What signals suggest an expense will be declined?"
source_table: augment_table/flag_19/predictive_declined/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_19__predictive_declined/analyses/original/analysis.md
wall_seconds: 89.74
---

## Signals that suggest an expense will be declined

**Base rate:** $46$ of $500$ expenses are `Declined`, or $9.2\%$.

| Signal | Evidence from data | Takeaway |
|---|---:|---|
| **`department = IT`** | $19/43 = 44.2\%$ declined, versus $27/457 = 5.9\%$ for all other departments | **Strongest business signal** |
| **`department = IT` + `category = Assets`** | $13/23 = 56.5\%$ declined | Very strong concentration |
| **Missing `processed_date`** | All declined rows have no `processed_date` ($46/46$), but $121$ non-declined rows also lack it | Strong association, but likely a late-stage/status signal rather than an early predictor |
| **Lower `amount`** | Decline rates are higher for smaller expenses: $\le 1000$: $12.5\%$; $1001$-$2000$: $12.5\%$; $2001$-$4000$: $11.3\%$; $4001$-$6000$: $7.1\%$; $6001$-$9000$: $6.5\%$ | Weak-to-moderate signal; declines are **not** concentrated in the highest amounts |
| **Missing `source_id`** | Missing: $13/111 = 11.7\%$ declined; present: $33/389 = 8.5\%$ | Weak signal |

### What stands out most

- **IT expenses are the main decline cluster.**  
  The IT department is only $43/500$ rows, but it contributes $19/46$ of all declines.

- **The strongest subtype is IT asset spending.**  
  Within IT:
  - `Assets`: $13/23 = 56.5\%$ declined
  - `Travel`: $3/10 = 30.0\%$
  - `Services`: $2/7 = 28.6\%$

- **Category alone is much less useful than department.**  
  Overall category decline rates are:
  - `Miscellaneous`: $3/17 = 17.6\%$ *(small sample)*
  - `Travel`: $10/94 = 10.6\%$
  - `Assets`: $27/310 = 8.7\%$
  - `Services`: $6/79 = 7.6\%$

  So `Assets` by itself is not a decline signal; it becomes one mainly **inside IT**.

### Visible patterns in the declined rows

Declined examples in `short_description` and `ci` are often **hardware / asset records**, including Dell laptops/desktops, Surface devices, and auto-generated asset entries. That supports the quantitative pattern above: declines are concentrated in **IT-linked asset workflows**, not broadly across all expense types.

### Important exceptions and weak evidence

- **Most non-IT assets are not decline-heavy.**  
  Examples:
  - `Customer Support` + `Assets`: $8/165 = 4.8\%$
  - `Sales` + `Assets`: $3/75 = 4.0\%$

- **Some departments show few or no declines, but counts are small.**  
  - `Product Management`: $0/12$
  - `Development`: $1/20$

- **Timing is unstable.**  
  Some months are higher (for example, February 2024 is $11/58 = 19.0\%$ declined), but the month pattern is inconsistent and should not be treated as a reliable rule.

### Bottom line

If the goal is to flag expenses likely to be declined, the clearest signal in this table is:

1. **IT department**
2. **Especially IT + Assets**
3. **Secondarily, lower-dollar requests and missing `source_id`**

Use **missing `processed_date`** carefully: it is highly associated with decline, but it looks more like a workflow/status field than a clean pre-decision predictor.
