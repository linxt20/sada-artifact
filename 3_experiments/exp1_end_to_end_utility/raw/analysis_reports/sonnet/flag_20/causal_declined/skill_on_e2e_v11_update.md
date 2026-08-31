---
dataset: flag_20
scenario: causal_declined
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "state_declined"
query: "Why do some travel expenses get declined, and which factors contribute the most?"
source_table: augment_table/flag_20/causal_declined/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:17:52.842029+00:00
wall_seconds: 84.21
---

# Why Travel Expenses Get Declined — Causal Analysis

## Executive Summary

Travel is the highest-decline expense category at **41.8% decline rate** (61/146). The dominant causal driver is the absence of a source ID (`has_source_id = False`), which is structurally tied to the `Travel` category in this dataset. Secondary factors include department affiliation and processing lag (all declined expenses are unprocessed). Expense entry origin (`travel_generated`) and asset action type (`travel_procurement`) confirm and sharpen the category-level signal provided by the raw `category` column.

---

## 1. Outcome Distribution

| State | Count | % of Total |
|---|---|---|
| Processed | 295 | 59.0% |
| Declined | 84 | 16.8% |
| Pending | 69 | 13.8% |
| Submitted | 52 | 10.4% |
| **Total** | **500** | |

---

## 2. Primary Driver: Category = Travel

Decline rate varies dramatically by expense category:

| Category | Declined | Total | Decline Rate |
|---|---|---|---|
| **Travel** | 61 | 146 | **41.8%** |
| Services | 5 | 47 | 10.6% |
| Assets | 17 | 281 | 6.1% |
| Miscellaneous | 1 | 26 | 3.8% |

Travel accounts for **72.6% of all declined expenses** (61 of 84) despite being only 29.2% of the dataset.

---

## 3. Missing Source ID: The Structural Mechanism

Every single Travel expense lacks a source ID (`has_source_id = False`, n=146, 100%). This is the strongest measurable predictor of decline:

| has_source_id | Declined | Total | Decline Rate |
|---|---|---|---|
| False | 62 | 173 | **35.8%** |
| True | 22 | 327 | 6.7% |

Rows without a source ID are **5.3× more likely** to be declined. The 62 declined expenses with no source ID represent 73.8% of all declines. The 1 non-Travel declined expense with `has_source_id=False` is Miscellaneous. Within non-Travel categories, all have source IDs (Assets/Services), and their decline rates are low (6–11%).

**Causal interpretation:** Travel expenses are created without a linked source document or booking reference. Approvers appear to decline unverifiable entries lacking a source ID.

---

## 4. Processing Lag Confirms the Pattern (TAPP: `processing_lag_category`)

The `processing_lag_category` column shows a perfect split: all 84 declined and all 69 pending and all 52 submitted expenses fall under `not_processed`, with zero declined entries in any processed lag bucket.

| processing_lag_category | Declined | Processed | Pending | Submitted |
|---|---|---|---|---|
| not_processed | 84 | 0 | 69 | 52 |
| same_day | 0 | 80 | 0 | 0 |
| next_day | 0 | 37 | 0 | 0 |
| short_delay_2–7 days | 0 | 63 | 0 | 0 |
| long_delay >7 days | 0 | 115 | 0 | 0 |

This confirms that decline is a terminal non-processing state — not a delayed processing outcome. All travel-category declines share `not_processed` status.

---

## 5. TAPP Semantic Facets: `expense_entry_origin` and `asset_action_type`

**`expense_entry_origin`** adds semantic clarity to *how* travel expenses enter the system:

| expense_entry_origin | Declined | Total | Decline Rate |
|---|---|---|---|
| `travel_generated` | 61 | 143 | **42.7%** |
| `automated_system` | 18 | 278 | 6.5% |
| `explicit_purchase` | 2 | 23 | 8.7% |
| `manual_procurement` | 3 | 56 | 5.4% |

Expenses tagged `travel_generated` account for nearly all travel-related declines. This label aligns exactly with the `Travel` category but adds a semantic signal: travel expenses seem to be auto-generated from a travel booking system that lacks the approval linkage (source ID) required for final processing.

**`asset_action_type`** mirrors this:

| asset_action_type | Declined | Total | Decline Rate |
|---|---|---|---|
| `travel_procurement` | 61 | 146 | **41.8%** |
| `new_acquisition` | 18 | 297 | 6.1% |
| `service_configuration` | 4 | 45 | 8.9% |
| `upgrade_maintenance` | 1 | 12 | 8.3% |

`travel_procurement` is essentially a restatement of the `Travel` category and does not add independent explanatory power beyond confirming the category label.

---

## 6. Department Effects Within Travel

Among the 146 travel expenses, decline rate varies by department:

| Department | Declined | Total (Travel) | Decline Rate |
|---|---|---|---|
| IT | 6 | 11 | 54.5% |
| HR | 1 | 2 | 50.0% |
| Customer Support | 35 | 79 | 44.3% |
| Sales | 18 | 44 | 40.9% |
| Finance | 1 | 4 | 25.0% |
| Development | 0 | 5 | 0.0% |

Customer Support and Sales drive the absolute count of declined travel (35 and 18 respectively). IT and HR show the highest rates but small sample sizes. Development is the only department with no declined travel expenses.

---

## 7. Amount: Not a Primary Driver

Mean expense amount for declined travel ($3,793) is similar to processed travel ($3,928), with overlapping distributions. Amount does not appear to drive declines. Submitted (pending approval) travel has a higher mean ($6,167) suggesting large outlier claims, but that does not translate to the decline state.

---

## 8. Key Findings Summary

| Factor | Effect on Decline | Evidence |
|---|---|---|
| **Category = Travel** | **Primary driver**, 41.8% decline rate vs 3–11% elsewhere | 61/84 all declines |
| **has_source_id = False** | 5.3× higher decline rate | 62/173 no-source declined vs 22/327 with source |
| **expense_entry_origin = travel_generated** | Confirms travel origin, 42.7% decline rate | 61/143 travel_generated rows |
| **processing_lag = not_processed** | Structural: all declines are unprocessed | 84/84 declined rows |
| **Department** | Modulates rate within travel (IT 55%, CS 44%, Sales 41%) | Department-level counts |
| **Amount** | Not significant | Mean $3,793 declined ≈ $3,928 processed |

---

## 9. Method Note

**TAPP-generated columns used in this report:** `is_travel_related`, `has_source_id`, `processing_lag_category`, `expense_entry_origin`, `department_group`, `asset_action_type`.

Columns `asset_category` and `is_travel_related` were reviewed but found largely redundant with the raw `category` column — `asset_category` distinguishes hardware/software/cloud within non-travel categories but adds no additional signal for the decline outcome. `department_group` was examined as a lower-cardinality proxy for `department`; the raw `department` column was used directly as it was more interpretable. All quantitative claims are grounded in the original structured columns (`category`, `state`, `source_id`, `amount`, `department`), with TAPP facets used to clarify semantic mechanisms.
