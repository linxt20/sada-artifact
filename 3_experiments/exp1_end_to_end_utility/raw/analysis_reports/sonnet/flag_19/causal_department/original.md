---
dataset: flag_19
scenario: causal_department
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: causal_attribution
focus_variable: "departmental_declined_rate_variation"
query: "Why do expense decline rates differ across departments?"
source_table: augment_table/flag_19/causal_department/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_19__causal_department/analyses/original/analysis.md
wall_seconds: 85.07
---

# Why expense decline rates differ across departments

Decline rate is computed as $\text{Declined} / \text{all expenses}$ from `state` by `department`.

## Department pattern

| Department | Expenses | Declined | Decline rate |
|---|---:|---:|---:|
| IT | 43 | 19 | 44.2% |
| HR | 14 | 2 | 14.3% |
| Finance | 22 | 2 | 9.1% |
| Customer Support | 267 | 16 | 6.0% |
| Development | 20 | 1 | 5.0% |
| Sales | 122 | 6 | 4.9% |
| Product Management | 12 | 0 | 0.0% |

## Main findings

- **IT is the clear outlier.** Its decline rate is **44.2%**, far above every other department. This is not explained by volume alone: Customer Support has the most rows (267) but only a **6.0%** decline rate.
- **Category mix matters somewhat, but it does not explain the gap.** Overall decline rates by `category` are:
  - `Miscellaneous`: **17.6%**
  - `Travel`: **10.6%**
  - `Assets`: **8.7%**
  - `Services`: **7.6%**

  Departments with more `Travel` or `Miscellaneous` rows can be expected to decline somewhat more. However, IT remains high **within** categories:
  - IT `Assets`: **13/23 declined = 56.5%**
  - IT `Travel`: **3/10 = 30.0%**
  - IT `Services`: **2/7 = 28.6%**

  By comparison:
  - Sales `Assets`: **4.0%**
  - Customer Support `Assets`: **4.8%**
  - Sales `Travel`: **0.0%**

  A simple category-mix benchmark would predict about **9.6%** declines for IT, versus the actual **44.2%**. This points to a department-specific difference, not just a different expense mix.

- **Amount is not a strong explanation.** IT average `amount` is about **4.3k**, which is similar to other departments. Finance (**4.7k**) and Product Management (**5.2k**) have higher average amounts but much lower decline rates.

- **`source_id` missingness is only a partial clue.** Rows without `source_id` decline somewhat more often (**11.7%** vs **8.5%**), but this mostly tracks category structure: all `Travel` and `Miscellaneous` rows lack `source_id`, while `Assets` and `Services` usually have one. IT is still unusually high on rows **with** `source_id`, especially in `Assets`, so missing IDs do not explain the department gap.

- **Submission/workflow differences are a plausible factor, but evidence is weaker.** Many declined IT rows have hardware-heavy and auto-generated `short_description` values such as Dell/HP asset records and “Automatically generated...” text. Auto-generated descriptions appear in **47.4%** of declined IT rows versus **37.5%** of non-declined IT rows. This suggests stricter review or lower-quality intake for IT asset entries, but the evidence is directional rather than definitive.

## Important exceptions

- Product Management shows **0 declines**, but it has only **12** rows.
- HR (**14 rows**), Development (**20**), and Finance (**22**) are also small, so their rates are less stable.
- Customer Support has many `Travel` rows, which are relatively decline-prone overall, yet its total decline rate stays low because most `Assets` and `Services` are processed rather than declined.

## Bottom line

The department differences are driven mainly by **IT’s unusually high decline behavior across all major categories**, especially `Assets`. Category mix contributes at the margins, but it does **not** account for the size of the gap. The visible row patterns are more consistent with **department-specific submission or approval behavior**—particularly around IT asset creation and automated entries—than with expense size alone.
