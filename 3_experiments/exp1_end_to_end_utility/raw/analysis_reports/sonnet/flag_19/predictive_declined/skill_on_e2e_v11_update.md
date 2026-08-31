---
dataset: flag_19
scenario: predictive_declined
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "state_declined"
query: "What signals suggest an expense will be declined?"
source_table: augment_table/flag_19/predictive_declined/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:16:30.392741+00:00
wall_seconds: 72.17
---

# Signals Predicting Expense Declination
**Dataset:** 500 expense records | **Declined:** 46 (9.2% base rate)  
**Method note:** TAPP-generated columns used in this analysis: `has_processed_date`, `has_source_id`, `is_travel_related`, `description_specificity`, `asset_form_factor`, `asset_vendor`. Columns `is_premium_or_nonstandard_asset`, `ci_identifier_quality`, and `submitting_department` were evaluated but showed weak or redundant signal and are not featured in primary claims.

---

## 1. Strongest Signal: Absence of a Processed Date

The single most discriminating signal is whether a processed date exists (`has_processed_date`). This is a perfect separator in the data:

| `has_processed_date` | Declined | Pending | Submitted | Processed | Total | **Decline Rate** |
|---|---|---|---|---|---|---|
| False | 46 | 80 | 41 | 0 | 167 | **27.5%** |
| True | 0 | 0 | 0 | 333 | 333 | **0.0%** |

All 46 declined expenses lack a processed date. No expense with a processed date was ever declined. While this partly reflects workflow mechanics (a declined expense never reaches processing), it means **an unprocessed expense carries a 27.5% risk of declination** versus zero for processed ones.

---

## 2. Submitting Department

The IT department is a major concentration of risk, with a decline rate nearly 5× the baseline:

| Department | Declined | Total | Decline Rate |
|---|---|---|---|
| IT | 19 | 43 | **44.2%** |
| HR | 2 | 14 | 14.3% |
| Finance | 2 | 22 | 9.1% |
| Customer Support | 16 | 267 | 6.0% |
| Sales | 6 | 122 | 4.9% |
| Development | 1 | 20 | 5.0% |
| Product Management | 0 | 12 | 0.0% |

IT expenses account for 41% of all declines (19/46) while comprising only 8.6% of submissions. Within IT, 70.4% of unprocessed IT expenses (19/27) are declined.

---

## 3. Expense Amount — Lower Amounts Declined More

Declined expenses have a noticeably lower median amount ($3,471) compared to non-declined ($4,434), opposite to an intuitive "too expensive" model.

| Amount Quartile | Approximate Range | Declined | Total | Decline Rate |
|---|---|---|---|---|
| Q1 (lowest) | < ~$2,500 | 17 | 126 | **13.5%** |
| Q2 | ~$2,500–$4,200 | 13 | 124 | 10.5% |
| Q3 | ~$4,200–$6,000 | 7 | 125 | 5.6% |
| Q4 (highest) | > ~$6,000 | 9 | 125 | 7.2% |

Lower-value expenses (Q1) are declined at 13.5%, nearly double the rate of mid-to-high values. This may reflect that small discretionary or miscellaneous purchases receive less justification.

---

## 4. Expense Category

| Category | Declined | Total | Decline Rate |
|---|---|---|---|
| Miscellaneous | 3 | 17 | **17.6%** |
| Travel | 10 | 94 | **10.6%** |
| Assets | 27 | 310 | 8.7% |
| Services | 6 | 79 | 7.6% |

Miscellaneous is the highest-risk category. Travel expenses (`is_travel_related = True`, n=94) decline at 10.6% vs. 8.9% for non-travel—a modest but real elevation.

---

## 5. Missing Source ID

Expenses missing a source reference ID (`has_source_id = False`) decline at a higher rate:

| `has_source_id` | Declined | Total | Decline Rate |
|---|---|---|---|
| False | 14 | 112 | **12.5%** |
| True | 32 | 388 | 8.2% |

The combination of missing source ID **and** missing processed date yields 30.4% decline rate (14/46 declined among 46 such records).

---

## 6. Asset Form Factor (TAPP)

The `asset_form_factor` column adds semantic granularity beyond `category`:

| `asset_form_factor` | Declined | Total | Decline Rate |
|---|---|---|---|
| software_license | 2 | 11 | **18.2%** |
| Unknown | 4 | 24 | **16.7%** |
| travel_accessory | 8 | 57 | **14.0%** |
| laptop | 23 | 225 | 10.2% |
| desktop | 6 | 98 | 6.1% |
| cloud_service | 3 | 59 | 5.1% |
| server | 0 | 15 | 0.0% |
| network_device | 0 | 11 | 0.0% |

Software licenses, unknown/unclassified assets, and travel accessories carry the highest per-form-factor decline risk. Server and network device expenses were never declined (though small samples).

---

## 7. Description Specificity (TAPP)

Vague or auto-generated descriptions (`description_specificity`) are associated with modestly higher decline rates:

| `description_specificity` | Declined | Total | Decline Rate |
|---|---|---|---|
| auto_generated_template | 18 | 159 | **11.3%** |
| generic_or_vague | 12 | 119 | **10.1%** |
| specific_model_identified | 16 | 222 | 7.2% |

Expenses with a specifically identified model decline ~36% less often than those with auto-generated or vague descriptions.

---

## Summary: Decline Risk Profile

An expense is most likely to be declined when it exhibits multiple of the following signals:

| Signal | Decline Rate | Source |
|---|---|---|
| IT department | 44.2% | `department` (original) |
| No processed date | 27.5% | `has_processed_date` (TAPP) |
| No source ID + no processed date | 30.4% | `has_source_id` + `has_processed_date` (TAPP) |
| Miscellaneous category | 17.6% | `category` (original) |
| Software license / unknown asset | 16–18% | `asset_form_factor` (TAPP) |
| Low amount (Q1) | 13.5% | `amount` (original) |
| Missing source ID alone | 12.5% | `has_source_id` (TAPP) |
| Travel category | 10.6% | `category` + `is_travel_related` (TAPP) |
| Vague/auto-generated description | 10–11% | `description_specificity` (TAPP) |

The absence of a processed date is a necessary (but partially definitional) condition for declination. Independently, department (IT), lower amounts, Miscellaneous/Travel category, missing source IDs, and vague descriptions are the most actionable predictive signals available pre-decision.
