---
dataset: flag_20
scenario: causal_reduce
variant: original
model: substrate-claude-haiku-4-5
query_subtype: what_if
focus_variable: "travel_expense_declined_status"
query: "How can we reduce declined travel expenses?"
source_table: augment_table/flag_20/causal_reduce/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_20__causal_reduce/analyses/original/analysis.md
wall_seconds: 76.49
---

# Reducing Declined Travel Expenses

## Bottom line

Travel is the main decline problem in this dataset. Although **Travel is 146 of 500 records (29.2%)**, it accounts for **61 of 84 declined records (72.6%)**. The fastest way to reduce declines is to **stop sending asset-like and poorly specified requests through the Travel category**, then target the highest-volume departments first.

## What the data shows

| Metric | Value |
|---|---:|
| Travel records | 146 |
| Declined travel records | 61 |
| Travel decline rate | 41.8% |
| Overall dataset decline rate | 16.8% |

### 1. Declines are concentrated in a few departments
Travel declines by department:

- **Customer Support:** 35 declines out of 79 travel records (**44.3%**)
- **Sales:** 18 of 44 (**40.9%**)
- **IT:** 6 of 11 (**54.5%**, highest rate but small sample)
- **Development:** 0 of 5
- **Finance:** 1 of 4

**Implication:** Start with **Customer Support** and **Sales** for volume, and review **IT** for policy/routing issues.

### 2. Many declined “travel” items do not look like normal travel spend
Visible columns `short_description` and `ci` show many declined travel entries that resemble **assets, hardware, vehicles, or systems**, for example:

- “**Automatically generated expense line for creation of travel asset**” — top declined description, **5 records**
- “**Travel equipment asset registration**” — **3 records**
- `ci`: **Global Positioning System Device**, **Dell XPS 15 Travel Laptop**, **Travel Management System V2**, **Aircraft Airbus A320**, **Company Car Fiat 500**, **Luxury Tour Bus**, **Company SUV Model X**

This pattern suggests a large share of declines come from **misclassified requests** or **auto-generated asset-style records** being submitted as travel expenses.

### 3. Amount alone does not explain declines
Travel `amount` is not clearly higher for declines than approvals:

- **Declined mean:** 3792.89
- **Processed mean:** 3927.87
- **Declined median:** 3699
- **Processed median:** 3618.5

Declined travel amounts range from **521 to 7798**, so both low- and high-value items are declined.

**Implication:** A simple spend cap will not solve most declines.

### 4. Evidence of inconsistent outcomes for similar items
Some items that look similar are processed, not declined:

- `ci` **Samsonite Luggage** appears **3 times, all Processed**
- `ci` **Portable GPS Navigator** appears **2 times, both Processed**
- `ci` **Business Class Airline Ticket** is mixed: **Processed, Declined, and Pending**
- `ci` **Dell Latitude 7400/7420/7490** appears across multiple states

**Implication:** The problem is not just the item type. It likely includes **request quality, category selection, approval rules, or required justification**.

### 5. Timing may matter, but evidence is weaker
Travel decline rate is higher in:

- **2023-11:** 57.1%
- **2024-03:** 53.8%
- **2023-07:** 50.0%
- **2024-01 to 2024-02:** about 47%

Lower months include:

- **2023-09:** 21.4%
- **2024-04:** 27.3%

This may indicate seasonal process strain or policy enforcement changes, but monthly travel counts are small (**8 to 17 per month**), so this is **weak evidence**.

## Actions most likely to reduce declines

1. **Block misclassified requests before submission**
   - Add routing rules so items mentioning `asset`, `hardware`, `laptop`, `GPS`, `vehicle`, `booking system`, or similar do **not** default to `category = Travel`.
   - Redirect them to **Assets**, **Services**, or procurement review.

2. **Require better travel-specific information**
   - For Travel submissions, require fields tied to real travel spend: trip purpose, traveler, dates, destination, expense type, and policy exception reason.
   - Reject vague descriptions like “travel asset” or “travel equipment” at intake.

3. **Review auto-generated travel records**
   - Many declines contain phrases like “automatically generated expense line.”
   - Audit the automation creating Travel records, because it appears to be producing low-quality or wrong-category submissions.

4. **Target Customer Support and Sales first**
   - These two departments create **53 of 61** travel declines.
   - Training, approval checklists, and routing fixes there should have the biggest effect fastest.

5. **Standardize approval rules for recurring travel items**
   - Similar items currently land in different states.
   - Define approved vs non-approved travel items clearly, especially for laptops, luggage, GPS devices, and business-class airfare.

## Recommended interpretation

The strongest data-backed explanation is **not overspending**, but **poor fit between submitted travel records and what travel expense approval expects**. Reducing declines should focus on **category cleanup, automation fixes, and better submission requirements**, not just tighter cost controls.

## Important caution

This dataset shows `state`, `amount`, `department`, timing, and free-text item descriptions, but it does **not** show explicit decline reasons or policy codes. That means the evidence supports **likely operational causes**, especially misclassification, but not a definitive causal claim for every declined record.
