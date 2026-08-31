---
dataset: flag_20
scenario: predictive_declined
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "state_declined"
query: "What signals suggest a travel expense will be declined?"
source_table: augment_table/flag_20/predictive_declined/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:18:33.470814+00:00
wall_seconds: 82.25
---

# Signals That Predict a Declined Travel Expense

**Query:** What signals suggest a travel expense will be declined?  
**Dataset:** 500 expense records; 146 are Travel category; 61 Travel expenses declined (41.8% decline rate vs. 16.8% overall).

---

## Method Note

TAPP-generated columns used in this analysis: `has_processed_date`, `entry_origin`, `expense_action_type`, `ci_asset_type`, `expense_category`, `department_group`. Columns `is_miscellaneous_ci` and `ci_asset_type` provided limited signal for Travel (all 146 travel rows have `is_miscellaneous_ci = False`); `ci_asset_type` offered minor supplemental signal. `expense_category` confirmed all but 5 travel rows are `travel_expense` type with negligible incremental signal.

---

## 1. Baseline: Travel Is the Highest-Risk Category

| Category | Declined | Total | Decline Rate |
|---|---|---|---|
| **Travel** | **61** | **146** | **41.8%** |
| Services | 5 | 47 | 10.6% |
| Assets | 17 | 281 | 6.0% |
| Miscellaneous | 1 | 26 | 3.8% |

Being a **Travel** expense is itself the dominant risk signal — it is ~7× more likely to be declined than an Assets expense.

---

## 2. Signal 1 (Strongest): Missing `processed_date` / `has_processed_date = False`

This is the single most predictive individual signal in the dataset.

| `has_processed_date` | Declined | Total Travel | Decline Rate |
|---|---|---|---|
| **False** | **61** | **94** | **64.9%** |
| True | 0 | 52 | 0.0% |

**No travel expense with a processed date was declined.** Every declined travel expense lacked a `processed_date` in the original structured column, confirmed by the TAPP-derived `has_processed_date` flag. This is a near-perfect discriminator within Travel.

---

## 3. Signal 2: Low Amount (especially < $2,000)

Among travel expenses with no processed date (the at-risk pool), small amounts sharply elevate decline probability:

| Amount Range | Declined | Total | Decline Rate |
|---|---|---|---|
| < $2,000 | 16 | 28 | **57.1%** |
| $2,000–$4,000 | 15 | 37 | 40.5% |
| $4,000–$6,000 | 21 | 48 | 43.8% |
| $6,000–$8,000 | 9 | 33 | 27.3% |

- Median amount, **Declined**: $3,699  
- Median amount, **Not Declined** (travel): $4,482  
- Combined filter — no `processed_date` **and** amount < $2,000: **88.9% decline rate** (16/18)

Higher-value expenses are relatively less likely to be declined, possibly indicating legitimate large travel costs receive more scrutiny before approval but clear review.

---

## 4. Signal 3: Department / `department_group`

Department adds meaningful stratification within Travel:

| Department (`department_group`) | Declined | Total | Decline Rate |
|---|---|---|---|
| IT | 6 | 11 | **54.5%** |
| HR | 1 | 2 | **50.0%** |
| Customer Support | 35 | 79 | **44.3%** |
| Sales | 18 | 44 | 40.9% |
| Finance | 1 | 4 | 25.0% |
| Development | 0 | 5 | **0.0%** |
| Product Management | 0 | 1 | 0.0% |

IT and Customer Support account for the majority of declined travel expenses (41/61 = 67%). Development shows zero declines in travel (small sample, n=5). The TAPP-derived `department_group` column mirrors the raw `department` field exactly here and adds no independent signal.

---

## 5. Signal 4: `entry_origin` (TAPP-derived)

Among travel expenses with no processed date (the at-risk pool):

| `entry_origin` | Decline Rate | Declined / Total |
|---|---|---|
| travel_expense_report | **66.2%** | 43/65 |
| automated_system | **63.0%** | 17/27 |
| manual_procurement | 50.0% | 1/2 |

Entries submitted as `travel_expense_report` form the largest share (65/94 = 69%) of unprocessed travel expenses. The decline rates across origins are similar once conditioned on missing `processed_date`, so `entry_origin` adds limited incremental lift beyond that primary signal.

---

## 6. Signal 5: `ci_asset_type` — Vehicle Expenses (TAPP-derived)

Within Travel, the `ci_asset_type = vehicle` subcategory shows the highest decline rate:

| `ci_asset_type` | Declined | Total | Decline Rate |
|---|---|---|---|
| vehicle | 5 | 9 | **55.6%** |
| travel_item | 38 | 90 | 42.2% |
| laptop | 12 | 35 | 34.3% |
| mobile_device | 3 | 9 | 33.3% |

Vehicle-category travel CIs (n=9) decline at 55.6%, predominantly from Customer Support via `travel_expense_report`.

---

## 7. `expense_action_type` (TAPP-derived) — Limited Additional Signal

| `expense_action_type` | Decline Rate | n |
|---|---|---|
| configuration | 100% | 1 |
| allocation | 50.0% | 4 |
| new_procurement | 42.3% | 26 |
| registration | 43.1% | 102 |
| tracking | 23.1% | 13 |

With the small sample sizes for non-`registration` types, these rates are not reliable. `registration` (n=102) is the dominant type and its 43.1% decline rate is consistent with the overall travel decline rate.

---

## 8. Summary: Ranked Decline Signals

| Rank | Signal | Source | Effect |
|---|---|---|---|
| 1 | **Missing `processed_date`** (`has_processed_date = False`) | Original + TAPP | 64.9% decline rate; 0% decline rate when present |
| 2 | **Amount < $2,000** (with no processed date) | Original | 88.9% combined decline rate |
| 3 | **Department = IT or Customer Support** | Original + TAPP `department_group` | 44–55% decline rate |
| 4 | **`ci_asset_type = vehicle`** | TAPP | 55.6% decline rate |
| 5 | **`entry_origin = travel_expense_report`** | TAPP | Largest share of declines (70%), similar rate to other origins |

**Decision rule:** A travel expense is very likely to be declined if it has no `processed_date` recorded — especially when the amount is low (< $2,000), it originates from the IT or Customer Support departments, and/or its CI is classified as a vehicle asset type.
