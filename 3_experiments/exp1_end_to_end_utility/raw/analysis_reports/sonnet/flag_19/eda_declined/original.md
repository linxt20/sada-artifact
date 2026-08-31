---
dataset: flag_19
scenario: eda_declined
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: exploratory_data_analysis
focus_variable: "state_declined"
query: "What kinds of expenses tend to get declined, and does it differ by department?"
source_table: augment_table/flag_19/eda_declined/original.csv
generated_at: 2026-07-26T13:23:30.582556+00:00
wall_seconds: 58.23
---

# Expense Decline Analysis — `original` Dataset

## Overview

The dataset contains **500 expense records** across 4 states: Processed (333), Pending (80), Declined (46), and Submitted (41). The **46 declined records** (9.2% overall decline rate) are the focus of this analysis.

---

## What Kinds of Expenses Get Declined?

### Decline Rate by Category

| Category | Total Records | Declined | Decline Rate |
|---|---|---|---|
| Miscellaneous | 17 | 3 | **17.6%** |
| Travel | 94 | 10 | **10.6%** |
| Assets | 310 | 27 | 8.7% |
| Services | 79 | 6 | 7.6% |

**Miscellaneous** has the highest decline rate (17.6%), though its small sample size (n=17) makes this estimate noisy. **Travel** is the next most likely to be declined (10.6%) and has a meaningful sample size. **Assets** is the most common declined category in absolute terms (27 declines), simply because it dominates the dataset (310 records).

### Declined Amounts

Declined expenses have a **lower average amount ($3,706)** than Processed ($4,436) or Pending ($4,398). Within declined records, **Assets** have the highest average amount ($5,270), suggesting that high-value asset purchases are flagged but not necessarily the primary driver of declines by rate.

---

## Does It Differ by Department?

### Decline Rate by Department

| Department | Total Records | Declined | Decline Rate |
|---|---|---|---|
| **IT** | 43 | 19 | **44.2%** |
| HR | 14 | 2 | 14.3% |
| Finance | 22 | 2 | 9.1% |
| Customer Support | 267 | 16 | 6.0% |
| Development | 20 | 1 | 5.0% |
| Sales | 122 | 6 | 4.9% |
| Product Management | 12 | 0 | 0.0% |

**IT stands out dramatically** with a 44.2% decline rate — nearly half of all IT expense submissions are declined. This is the single strongest pattern in the data.

### Category Breakdown Within Declined by Department

| Department | Assets | Miscellaneous | Services | Travel |
|---|---|---|---|---|
| IT | **13** | 1 | 2 | 3 |
| Customer Support | 8 | 1 | 1 | **6** |
| Sales | 3 | 1 | 2 | 0 |
| Finance | 2 | 0 | 0 | 0 |
| HR | 1 | 0 | 0 | 1 |
| Development | 0 | 0 | 1 | 0 |

- **IT's high decline rate is driven predominantly by Asset declines** (13 out of 19 IT declines). This may reflect policy around hardware/software procurement in IT.
- **Customer Support's declines are more balanced**, with a notable Travel component (6 of 16 declines), suggesting travel reimbursements face more scrutiny in that department.
- **Sales and Finance** have low decline rates overall, with no dominant category.

---

## Key Findings & Caveats

1. **IT is the highest-risk department** for declines (44.2%), largely due to Asset expense rejections — a pattern strong enough to drive decisions.
2. **Miscellaneous has the highest per-category decline rate** (17.6%), but the sample is very small (n=17); treat this with caution.
3. **Travel declines** are spread across departments (Customer Support, IT, HR) but Travel as a category has a 10.6% decline rate — a moderate signal.
4. **Product Management** had zero declines (n=12) — weak evidence given small sample, but notable.
5. The data does not include a reason-for-decline column, so causal attribution (policy, amount, documentation) cannot be confirmed from this table alone.
