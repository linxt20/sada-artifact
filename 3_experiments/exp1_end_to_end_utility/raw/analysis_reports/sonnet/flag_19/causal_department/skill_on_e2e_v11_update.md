---
dataset: flag_19
scenario: causal_department
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "departmental_declined_rate_variation"
query: "Why do expense decline rates differ across departments?"
source_table: augment_table/flag_19/causal_department/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:16:06.171125+00:00
wall_seconds: 106.21
---

# Expense Decline Rates Across Departments

## Executive Summary

Decline rates vary dramatically across departments — from **44.2% (IT)** down to **0% (Product Management)** — driven primarily by three structural factors: category mix (especially high-risk Miscellaneous and Travel expenses), absence of a recurring submitter relationship, and missing source IDs. TAPP-generated columns `recurring_submitter`, `has_source_id`, and `asset_category_type` add material explanatory signal beyond the raw structured fields.

---

## Department Decline Rates Overview

| Department | N | Declined | Decline Rate | Travel % | Misc % | No Source ID % | Recurring Submitter % | Median Amount |
|---|---|---|---|---|---|---|---|---|
| IT | 43 | 19 | **44.2%** | 23.3 | 7.0 | 32.6 | 0.0 | $4,132 |
| HR | 14 | 2 | **14.3%** | 14.3 | 0.0 | 14.3 | 0.0 | $3,615 |
| Finance | 22 | 2 | **9.1%** | 31.8 | 0.0 | 31.8 | 45.5 | $4,883 |
| Customer Support | 267 | 16 | **6.0%** | 20.6 | 2.6 | 23.2 | 6.0 | $4,256 |
| Development | 20 | 1 | **5.0%** | 10.0 | 0.0 | 10.0 | 0.0 | $3,381 |
| Sales | 122 | 6 | **4.9%** | 14.8 | 5.7 | 20.5 | 3.3 | $4,580 |
| Product Management | 12 | 0 | **0.0%** | 0.0 | 0.0 | 0.0 | 75.0 | $5,865 |

---

## Key Causal Drivers

### 1. IT Is a Structural Outlier — High-Risk Category Mix + Zero Recurring Submitters

IT's 44.2% decline rate is nearly 3× the next-highest department (HR, 14.3%). The primary drivers:

- **Category composition**: 23% of IT expenses are Travel (decline rate: 30.0% within IT) and 7% are Miscellaneous (decline rate: 33.3% within IT). Across all departments, Miscellaneous has the highest decline rate (17.6%) and Travel the second-highest (10.6%).
- **Asset decline anomaly**: IT's Assets category has a **56.5% decline rate** (13 of 23 declined), compared to 4.8% for Customer Support and 4.0% for Sales on the same category. This is the single largest driver of IT's elevated overall rate.
- **No recurring submitters**: IT has 0% `recurring_submitter=True`. Globally, recurring submitters have a decline rate of only **2.6%** vs. **9.8%** for non-recurring — a 3.8× difference. Product Management (75% recurring) has 0 declines; Finance (45.5% recurring) has only 9.1% despite having the highest travel share (31.8%).

### 2. `recurring_submitter` Is the Strongest TAPP-Generated Protective Factor

| recurring_submitter | N | Decline Rate |
|---|---|---|
| True | 39 | 2.6% |
| False | 461 | 9.8% |

This is consistent with the department-level pattern: departments with high recurring submitter shares (Product Management 75%, Finance 45.5%) have the lowest decline rates despite having substantial travel and missing source IDs.

### 3. `has_source_id` Correlates With Decline Risk

| has_source_id | N | Decline Rate |
|---|---|---|
| False | 112 | 12.5% |
| True | 388 | 8.2% |

IT and Finance have the two highest `has_source_id=False` rates (32.6% and 31.8% respectively). However, Finance's elevated recurring submitter share offsets this risk. IT has neither mitigating factor.

### 4. `asset_category_type` Differentiates Within-Category Risk

| asset_category_type | Decline Rate |
|---|---|
| miscellaneous | 23.1% |
| travel | 10.8% |
| hardware | 8.5% |
| software_service | 8.0% |

IT's portfolio is heavily skewed toward hardware (24/43 = 56%) and travel (10/43 = 23%), both higher-risk categories. The `asset_category_type` column (`hardware`, `travel`, `miscellaneous`) largely mirrors the original `category` field and is confirmatory rather than independently explanatory.

### 5. `ci_identifier_quality` Adds Modest Signal

| ci_identifier_quality | Decline Rate |
|---|---|
| opaque_asset_tag | 13.5% |
| generic_label | 11.3% |
| standard_model_name | 8.0% |

Within IT, expenses with `opaque_asset_tag` or `generic_label` have decline rates of 55.6% and 60.0% respectively vs. 37.9% for `standard_model_name`. This suggests poor CI identification quality is a secondary amplifier within IT, but does not explain cross-department differences substantially.

### 6. Amount Is Not a Primary Driver

Median amounts are broadly similar across departments ($3,381–$5,865). Within IT's Assets, declined expenses have a mean of $5,620 vs. $6,337 for processed — if anything, higher amounts are *processed* more often, ruling out simple dollar-threshold policies as the explanation.

---

## Synthesized Explanation

The cross-department variance in decline rates is explained by three interacting factors:

1. **Category mix**: Departments with more Miscellaneous and Travel expenses face higher baseline decline rates.
2. **Recurring submitter absence (TAPP: `recurring_submitter`)**: IT and HR have 0% recurring submitters, leaving all expenses subject to standard scrutiny. Product Management and Finance offset structural risks through established submitter relationships.
3. **IT-specific anomaly in Assets**: IT's 56.5% Asset decline rate (vs. ~5% elsewhere) is the dominant single contributor. This likely reflects institutional policy differences for IT hardware procurement — possibly separate approval workflows, budget caps, or duplicate-purchase controls — not just mix effects. Poor `ci_identifier_quality` (opaque/generic tags on 40% of IT assets) may flag these as unresolvable.

Finance demonstrates the clearest protective mechanism: 31.8% travel exposure and 31.8% missing source IDs, yet only 9.1% decline rate, fully attributable to 45.5% recurring submitters.

---

## Method Note

**TAPP-generated columns used**: `recurring_submitter`, `has_source_id`, `ci_identifier_quality`, `asset_category_type`.

Columns `device_form_factor`, `entry_origin`, `vendor_brand`, and `is_travel_related` were evaluated but showed weak or redundant effects relative to the original `category` and `department` structured fields and are not centered in the analysis.
