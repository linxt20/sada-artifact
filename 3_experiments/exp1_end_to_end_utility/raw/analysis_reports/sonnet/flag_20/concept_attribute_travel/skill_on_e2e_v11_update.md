---
dataset: flag_20
scenario: concept_attribute_travel
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "travel_policy_risk"
query: "What travel policy risks appear in expense descriptions?"
source_table: augment_table/flag_20/concept_attribute_travel/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:18:01.044112+00:00
wall_seconds: 76.37
---

# Travel Policy Risks in Expense Descriptions
**Query:** What travel policy risks appear in expense descriptions?
**Dataset:** 500 records | Travel category: 146 records | Analysis date: 2026-07-30

---

## Executive Summary

Travel expenses represent the highest-risk category in the dataset, with a **41.78% decline rate** — more than four times the rate of Assets (6.1%) or Miscellaneous (3.9%). Three overlapping risk patterns emerge from expense descriptions and TAPP-augmented columns: (1) transport/airfare expenses mis-routed as asset procurement, (2) hardware items mislabeled as travel items, and (3) vague or automated descriptions that obscure actual spend. All 146 travel records share a missing source ID (`missing_source_id_flag = True` for 100%), compounding auditability risk.

---

## 1. Overall Risk Profile by Category

| Category | N | Declined | Decline Rate |
|---|---|---|---|
| **Travel** | 146 | 61 | **41.78%** |
| Services | 47 | 5 | 10.64% |
| Assets | 281 | 17 | 6.05% |
| Miscellaneous | 26 | 1 | 3.85% |

Travel is the dominant risk exposure in this dataset.

---

## 2. Key Policy Risk: Transport Expenses Misclassified as Asset Procurement

TAPP column `transport_expense_misclassified` flagged **14 of 146 travel records (9.6%)** as containing transport expense descriptions (airfare, flights, vehicle) filed under asset-creation workflows.

**Examples of misclassified descriptions:**
- *"Airline Expense for Travel Category"* — state: Submitted, amount: $7,682
- *"Flight Booking for Official Travel"* — state: **Declined**, amount: $5,656
- *"Travel expense for procuring vehicle asset"* — state: Pending, amount: $4,134
- *"Automatically generated expense line for creation of travel asset"* (×9 instances) — auto-generated wording masking actual transport costs

| `transport_expense_misclassified` | N | Declined | Decline Rate | Mean Amount |
|---|---|---|---|---|
| True | 14 | 7 | **50.0%** | $3,875 |
| False | 132 | 54 | 40.9% | $4,203 |

Misclassified entries have a 9-point higher decline rate (50% vs. 41%) and frequently involve airline or vehicle spend disguised within asset-creation boilerplate language — a direct policy violation risk.

---

## 3. Hardware Assets Mislabeled as Travel Items

`asset_category` reveals a secondary risk: **9 travel-category records are tagged as `hardware_endpoint`** (laptops, computers) rather than `travel_item`. Their descriptions include:

- *"Business-class travel laptop for remote work"* — Processed, $3,142
- *"Procurement of new laptops for travel purpose"* — **Declined**, $2,701
- *"Hardware Asset for Travel Use"* — **Declined**, $6,026

Of these 9 hardware-in-travel entries, **4 (44%)** were declined. The ambiguous routing of hardware purchases through the travel category can circumvent standard asset-procurement controls.

---

## 4. Description Quality and Automated Entry Risks

`asset_description_quality` shows that **93.2% of travel records (136/146)** carry only a `travel_descriptor_only` rating — generic wording that provides no meaningful audit trail:

| Description Quality | N | Decline Rate |
|---|---|---|
| travel_descriptor_only | 136 | 42.65% |
| specific_model | 8 | 25.00% |
| vague_generic | 2 | 50.00% |

`entry_method` shows manual procurement dominates (105/146 = 71.9%) but does not substantially differentiate decline rates (manual: 44/105 = 41.9%; automated: 17/41 = 41.5%). However, **automated entries** frequently generate repetitive boilerplate descriptions (e.g., *"Automatically generated expense line for creation of travel asset"* appeared 15 times), which mask the true nature of the expense.

---

## 5. Processing Lag and Source ID Gaps

- **`missing_source_id_flag`**: All 146 travel records lack a valid source ID — 100% coverage, making this a systemic rather than case-level risk. Without source IDs, no expense can be traced back to a booking system or approver.
- **`processing_lag_flag`**: 23 travel records (15.8%) have a processing lag. Counterintuitively, lagged records had a **0% decline rate** vs. 49.6% for non-lagged records, suggesting lagged entries may receive additional manual review that clears them — but the lag itself signals workflow failure.

---

## 6. Repeat-User Risk

`repeat_user_flag` is True for 25 travel records (17.1%), with a slightly elevated decline rate (48% vs. 40.5% for non-repeat users), indicating some users repeatedly submit borderline or non-compliant travel expenses.

---

## 7. Department Concentration

Travel policy violations are concentrated in two departments:

| Department | Travel Records | Declined | Decline Rate |
|---|---|---|---|
| Customer Support | 79 | 35 | **44.3%** |
| Sales | 44 | 18 | **40.9%** |
| IT | 11 | 6 | **54.5%** |
| Finance | 4 | 1 | 25.0% |
| Development | 5 | 0 | 0.0% |

Customer Support and Sales together account for 86% of travel records and 87% of travel declines.

---

## 8. Combined Risk Summary

| Risk Pattern | N Affected | Decline Rate | Primary Evidence |
|---|---|---|---|
| Transport/airfare in asset workflow | 14 | 50.0% | `transport_expense_misclassified=True` + descriptions |
| Hardware mislabeled as travel | 9 | 44.4% | `asset_category=hardware_endpoint` in Travel |
| Vague/generic descriptions | 136 | 42.7% | `asset_description_quality=travel_descriptor_only` |
| Missing source ID | 146 (all) | 41.8% | `missing_source_id_flag=True` |
| Repeat-user submissions | 25 | 48.0% | `repeat_user_flag=True` |

---

## Method Note

TAPP-generated columns used in this report: `transport_expense_misclassified`, `asset_category`, `asset_description_quality`, `entry_method`, `missing_source_id_flag`, `processing_lag_flag`, `repeat_user_flag`.

`transport_expense_misclassified` provided the strongest incremental semantic signal, identifying specific descriptions (airline, flight, vehicle) that would be indistinguishable from generic asset entries without NLP analysis. `asset_description_quality` confirmed the breadth of vague-description risk. `processing_lag_flag` and `repeat_user_flag` were lower-signal but corroborated by structured `state` outcome data.
