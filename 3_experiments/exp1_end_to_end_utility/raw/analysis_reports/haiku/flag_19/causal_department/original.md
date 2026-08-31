---
dataset: flag_19
scenario: causal_department
variant: original
model: substrate-claude-haiku-4-5
query_subtype: causal_attribution
focus_variable: "departmental_declined_rate_variation"
query: "Why do expense decline rates differ across departments?"
source_table: augment_table/flag_19/causal_department/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_19__causal_department/analyses/original/analysis.md
wall_seconds: 114.29
---

# Expense decline rates by department

## Bottom line

Department differences are **real in the observed data**, and the largest gap is concentrated in **IT**. The strongest visible explanation is not expense size; it is a **department-specific rejection pattern, especially for Asset requests**.

## Key evidence

| Department | Rows | Declined | Decline rate | Decline rate among decided only* |
|---|---:|---:|---:|---:|
| IT | 43 | 19 | 44.2% | 54.3% |
| HR | 14 | 2 | 14.3% | 18.2% |
| Finance | 22 | 2 | 9.1% | 15.4% |
| Customer Support | 267 | 16 | 6.0% | 7.9% |
| Development | 20 | 1 | 5.0% | 6.7% |
| Sales | 122 | 6 | 4.9% | 6.5% |
| Product Management | 12 | 0 | 0.0% | 0.0% |

\*Decided only = `Processed` or `Declined`, excluding `Pending` and `Submitted`.

## Why the rates differ

### 1. IT is unusually decline-heavy across multiple categories
IT is the main outlier, and this is not just because it handles one niche category.

- **Assets:** 13 declines out of 23 IT asset records = **56.5%**
- **Travel:** 3/10 = **30.0%**
- **Services:** 2/7 = **28.6%**

This is much higher than other departments in the same categories. For example:

- Asset decline rate is **4.0% in Sales** and **4.8% in Customer Support**
- Product Management has **0 declines in 10 asset records**

So category mix contributes somewhat, but **IT remains high even within category**.

### 2. Asset-heavy departments do not all behave the same
Most departments are asset-heavy:

- Product Management: **83.3% Assets**
- HR: **78.6% Assets**
- Finance: **63.6% Assets**
- Customer Support: **61.8% Assets**
- Sales: **61.5% Assets**
- IT: **53.5% Assets**

If category mix alone explained the pattern, other asset-heavy departments would also show high decline rates. They do not. This points to **department-specific approval behavior or request quality differences** rather than just different work types.

### 3. Undecided backlogs affect headline rates, but do not explain the main gap
Some departments have many `Pending` or `Submitted` records:

- Finance: **40.9%** pending/submitted
- Customer Support: **24.0%**
- Sales: **23.8%**
- Product Management: **25.0%**

That means all-record decline rates slightly understate the eventual rate. But even after limiting to decided cases, the pattern holds:

- IT: **54.3%**
- Customer Support: **7.9%**
- Sales: **6.5%**

So backlog differences are **not** the main reason IT stands apart.

### 4. Expense amount is weak evidence
Amounts do not show a clean “higher amount = more declines” pattern.

- **IT:** declined mean = **4,473.6**, processed mean = **4,266.7**
- **Customer Support:** declined mean = **3,055.4**, processed mean = **4,360.9**
- **Sales:** declined mean = **3,191.3**, processed mean = **4,599.8**

In Sales and Customer Support, declined requests are actually **smaller on average** than processed ones. This weakens a “cost control” explanation.

### 5. Data-quality/process signals may matter in some departments, but evidence is mixed
Two visible signals were checked:

- `source_id` missing
- `short_description` marked as “Automatically ...”

Overall, both are only **slightly** more decline-prone:

- Missing `source_id`: **11.7%** declined vs **8.5%** when present
- Auto-generated description: **11.8%** declined vs **8.1%** otherwise

But this is **not consistent by department**. Example:

- In **Customer Support**, missing `source_id` is more common in declines than in processed records
- In **IT**, missing `source_id` is **not** the main driver

So these fields may reflect process quality in places, but they do **not** explain the full cross-department gap.

## Important exceptions and weak spots

- **Small samples** make some department rates unstable:
  - Product Management: 12 rows
  - HR: 14
  - Development: 20
  - Finance: 22
- Some category results are especially thin:
  - HR Travel: 2 rows
  - Finance Services: 1 row
  - IT Miscellaneous: 3 rows
- There is also a **time-cluster effect** in IT: declines rise sharply in late 2023 to early 2024, including **5 declines in 6 IT records in 2024-02**. That suggests timing or policy/process changes may be involved, but the dataset has no policy or approver fields to confirm this.

## Decision-ready conclusion

The department gap is driven mainly by **IT’s unusually high rejection rate**, especially for **Asset** requests. This pattern persists even when comparing the same category across departments, so the difference is **not explained by category mix alone**. `amount` provides little support as a driver, and data-quality signals such as missing `source_id` are only weak and inconsistent. The most defensible interpretation from the visible columns is:

1. **Department-specific review behavior or request quality differs**, with IT much stricter or receiving more rejectable requests.
2. **Category mix contributes somewhat**, but cannot explain the gap by itself.
3. **Pending/submitted backlog differences** affect headline rates modestly, but do not change the ranking.

If action is needed, the first place to investigate is **IT asset-request workflow**: request standards, approval rules, and any policy change around late 2023 to early 2024.
