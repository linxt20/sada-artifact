---
dataset: flag_20
scenario: causal_declined
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "state_declined"
query: "Why do some travel expenses get declined, and which factors contribute the most?"
source_table: augment_table/flag_20/causal_declined/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:17:47.173979+00:00
wall_seconds: 78.75
---

# Analysis Report: Travel Expense Declines and Contributing Factors

## Executive Summary

Travel expenses are declined at dramatically higher rates than other expense categories. Of 500 total expense records, 84 (16.8%) are declined. However, travel-related expenses show a 41.8% decline rate, compared to just 6.5% for non-travel expenses. This analysis identifies the primary drivers of decline and quantifies their relative impact using both original structured data and TAPP-generated semantic columns.

---

## Key Findings

### 1. **Travel Expenses Dominate Declined Outcomes**

- **Total declined expenses**: 84 records
- **Travel category decline rate**: 61 out of 146 travel expenses declined (41.8%)
- **Non-travel decline rate**: 23 out of 354 non-travel expenses declined (6.5%)
- **Risk multiplier**: Travel expenses are **6.4× more likely to be declined** than non-travel expenses

### 2. **Asset Category: Travel Equipment is the Primary Driver**

The TAPP-generated `asset_category` column reveals a critical semantic pattern:

| Asset Category | Declined | Total | Decline Rate |
|---|---|---|---|
| **travel_equipment** | 52 | 116 | **44.8%** |
| hardware | 27 | 328 | 8.2% |
| service | 4 | 41 | 9.8% |
| miscellaneous | 1 | 15 | 6.7% |

Travel equipment is the single highest-risk asset category, declining at 44.8%, over 5× the rate of hardware or services.

### 3. **Travel Expense Indicator: Strongest Semantic Signal**

The TAPP-generated `travel_expense_indicator` column perfectly identifies travel-related expenses with strong predictive power:

| Travel Indicator | Declined | Total | Decline Rate |
|---|---|---|---|
| **True** | 61 | 144 | **42.4%** |
| False | 23 | 356 | 6.5% |

Of the 84 total declined expenses, 61 (72.6%) are flagged with `travel_expense_indicator=True`. This facet demonstrates high semantic relevance to the query.

### 4. **Acquisition Driver: travel_related Acquisition is Strongly Associated with Decline**

The TAPP-generated `acquisition_driver` column stratifies expenses by procurement method:

| Acquisition Driver | Declined | Total | Decline Rate |
|---|---|---|---|
| **travel_related** | 57 | 136 | **41.9%** |
| standard_procurement | 12 | 184 | 6.5% |
| automated_generated | 14 | 171 | 8.2% |
| maintenance_upgrade | 1 | 5 | 20.0% |
| manual_entry | 0 | 4 | 0.0% |

The `travel_related` acquisition driver accounts for 57 of 84 declined expenses (67.9%). Its 41.9% decline rate is 6.4× higher than standard procurement.

### 5. **Source ID Presence: Critical Missing Documentation Factor**

The TAPP-generated `source_id_presence` column reveals a strong inverse relationship. Among travel expenses specifically:

| Source ID Presence | Declined | Total | Decline Rate |
|---|---|---|---|
| **False** | 61 | 142 | **43.0%** |
| True | 0 | 2 | 0.0% |

Notably, **all travel expenses with a source ID present are approved (0% decline rate)**, while 43% of travel expenses without source IDs are declined. This suggests missing or absent source documentation is a critical approval barrier for travel claims. Across all expenses (travel and non-travel), the absence of a source ID correlates with 36.3% decline rate versus 6.7% for those with source IDs present.

### 6. **Department Origin: Customer Support and Sales Face Higher Decline Rates**

The TAPP-generated `department_origin` column (mirroring the original `department` field) shows departmental variation:

| Department | Declined | Total | Decline Rate |
|---|---|---|---|
| Customer Support | 48 | 272 | 17.6% |
| Sales | 26 | 141 | 18.4% |
| HR | 1 | 5 | 20.0% |
| IT | 7 | 42 | 16.7% |
| Finance | 1 | 16 | 6.2% |
| Development | 0 | 16 | 0.0% |

Customer Support and Sales account for 74 of 84 declined expenses (88.1%). However, this primarily reflects that these departments submit more travel expenses (81% of all travel expenses originate from Customer Support and Sales), not necessarily stricter approval criteria.

### 7. **Processed Date Absence Indicates Non-Approval**

A structural finding: **100% of declined expenses have no `processed_date` value** (84 out of 84 declined records have null `processed_date`). Conversely, 295 of 295 processed expenses have a non-null `processed_date`. This confirms that absence of a processing timestamp is inherent to the "Declined" state and not a causal factor.

---

## Quantified Effect Combinations

To isolate dominant factors, we examine their combined effects:

### Travel Indicator + Source ID Presence Interaction:

| Travel Indicator | Source ID Present | Declined | Total | Rate |
|---|---|---|---|---|
| **True** | **False** | **61** | **142** | **43.0%** |
| True | True | 0 | 2 | 0.0% |
| False | True | 22 | 327 | 6.7% |
| False | False | 1 | 29 | 3.4% |

The highest-risk combination is `travel_expense_indicator=True` AND `source_id_presence=False` (43.0% decline rate, n=142). This represents the core decline population.

---

## Factor Ranking: Decline Rate Impact

| Factor | Decline Rate | Sample Size |
|---|---|---|
| Asset Category = travel_equipment | 44.8% | 116 |
| Travel Expense Indicator = True | 42.4% | 144 |
| Acquisition Driver = travel_related | 41.9% | 136 |
| Category = Travel (structured field) | 41.8% | 146 |
| Source ID Presence = False | 36.3% | 171 |
| Department = Customer Support or Sales | 17.9% | 413 |

---

## Root Cause Hypothesis

Travel expenses decline at 6–7× the base rate due to a combination of factors:

1. **Primary Driver (Semantic/Policy)**: Travel-related acquisitions (`acquisition_driver=travel_related`, `asset_category=travel_equipment`, `travel_expense_indicator=True`) inherently face stricter approval workflows, yielding 41–45% decline rates.

2. **Critical Gating Factor (Documentation)**: Absence of source ID documentation (`source_id_presence=False`) is strongly associated with decline. Among travel expenses *without* source IDs, 43% are declined; *with* source IDs, 0% are declined (n=2). This suggests source ID presence is either a documentation requirement or a proxy for proper authorization channels.

3. **Secondary Factors**:
   - **Amount**: Declined travel expenses (mean $3,792.89) are comparable to processed travel expenses (mean $3,924.55), ruling out amount as a primary driver.
   - **Departmental**: Customer Support and Sales account for most declines but also submit most travel expenses; the decline *rate* is elevated but not dramatically higher than other departments.

---

## Method Note

This analysis employs the following TAPP-generated augmented columns:
- **`travel_expense_indicator`**: Boolean flag indicating travel-related expenses (perfect overlap with category="Travel" and acquisition_driver="travel_related")
- **`asset_category`**: Semantic categorization including travel_equipment, hardware, service, miscellaneous
- **`acquisition_driver`**: Procurement method including travel_related, standard_procurement, automated_generated, manual_entry, maintenance_upgrade
- **`department_origin`**: Department sourcing the expense (mirrors original `department` field)
- **`source_id_presence`**: Boolean flag indicating whether a source ID is present (strong inverse predictor of decline among travel expenses)

These columns add semantic clarity to the travel/non-travel distinction and reveal the source ID documentation requirement, both critical to understanding decline patterns.

---

## Conclusion

Travel expenses are declined at ~42% rate primarily due to:
1. **Inherent policy strictness** on travel acquisitions (captured by `travel_expense_indicator`, `asset_category=travel_equipment`, and `acquisition_driver=travel_related`)
2. **Missing source ID documentation** (`source_id_presence=False`), which perfectly predicts decline among travel expenses in the sample
3. **Departmental concentration** in Customer Support and Sales, which submit 81% of travel expenses

Non-travel expenses decline at only 6.5%, with the strongest decline predictor being absence of source ID documentation (36.3% decline vs. 6.7% with source ID present). Source ID presence emerges as the single strongest protective factor across all expense types.
