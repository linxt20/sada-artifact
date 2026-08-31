---
dataset: flag_19
scenario: causal_reduce
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: what_if
focus_variable: "state_declined"
query: "How can we reduce declined expense submissions?"
source_table: augment_table/flag_19/causal_reduce/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:15:50.388038+00:00
wall_seconds: 78.94
---

# Reducing Declined Expense Submissions

## Executive Summary

Of 500 expense submissions in the dataset, **46 were declined (9.2% overall rate)**. Declines are heavily concentrated in the **IT department** (44.2% decline rate — nearly 5× the average) and in submissions lacking proper CI/asset identification. Targeted interventions in IT workflows and documentation completeness could realistically eliminate **~35 of the 46 declines (76%)**.

---

## 1. Outcome Overview

| State | Count | Share |
|-------|-------|-------|
| Processed | 333 | 66.6% |
| Pending | 80 | 16.0% |
| Declined | **46** | **9.2%** |
| Submitted | 41 | 8.2% |

Declined submissions have a lower mean amount ($3,706) vs. processed ($4,436), suggesting cost is **not** a primary driver of declines — procedural/documentation issues are more likely causes.

---

## 2. Primary Driver: Department

Department is the strongest predictor of decline.

| Department | Total | Declined | Decline Rate |
|---|---|---|---|
| **IT** | 43 | **19** | **44.2%** |
| HR | 14 | 2 | 14.3% |
| Finance | 22 | 2 | 9.1% |
| Customer Support | 267 | 16 | 6.0% |
| Development | 20 | 1 | 5.0% |
| Sales | 122 | 6 | 4.9% |
| Product Management | 12 | 0 | 0.0% |

IT accounts for **41% of all declines** (19/46) despite representing only 8.6% of total submissions. Within IT, every category shows elevated decline rates: Assets (56.5%), Travel (30.0%), Services (28.6%), and Miscellaneous (33.3%).

---

## 3. Category-Level Evidence

| Category | Total | Declined | Decline Rate |
|---|---|---|---|
| Miscellaneous | 17 | 3 | 17.6% |
| Travel | 94 | 10 | 10.6% |
| Assets | 310 | 27 | 8.7% |
| Services | 79 | 6 | 7.6% |

Assets and Travel together account for 80% of all declines (37/46). Travel submissions lack `source_id` entirely (100% missing) and carry a 10.6% decline rate.

---

## 4. Documentation Quality: `source_id_present` and `ci_specificity`

### Source ID Presence
| source_id_present | Total | Declined | Decline Rate |
|---|---|---|---|
| False | 112 | 14 | **12.5%** |
| True | 388 | 32 | 8.2% |

Submissions missing a source ID decline at **52% higher rate** than those with one. All 94 Travel submissions lack a source ID, driving their elevated decline rate.

### CI Specificity (TAPP column: `ci_specificity`)
The `ci_specificity` column classifies how precisely the CI field identifies an asset.

| ci_specificity | Total | Declined | Decline Rate |
|---|---|---|---|
| generic_label | 73 | 11 | **15.1%** |
| asset_code_only | 68 | 10 | **14.7%** |
| specific_model | 287 | 21 | 7.3% |
| service_name | 72 | 4 | 5.6% |

Submissions with vague CI descriptions (`generic_label` or `asset_code_only`) decline at **~2× the rate** of those with specific model identification. This effect is independent of source_id presence:

| Missing source_id | Vague CI | Declined/Total | Decline Rate |
|---|---|---|---|
| No | No | 21/313 | 6.7% |
| No | Yes | 11/75 | 14.7% |
| Yes | No | 4/46 | 8.7% |
| Yes | Yes | 10/66 | **15.2%** |

The combination of missing source ID **and** vague CI is the highest-risk profile (15.2%).

---

## 5. Submission Mechanics

### `submission_action_type` (TAPP column)
| Action Type | Total | Declined | Decline Rate |
|---|---|---|---|
| acquisition | 39 | 5 | 12.8% |
| configuration | 7 | 1 | 14.3% |
| auto_creation | 168 | 16 | 9.5% |
| registration | 245 | 22 | 9.0% |
| allocation | 15 | 1 | 6.7% |
| provisioning | 26 | 1 | 3.8% |

Within IT specifically, `auto_creation` submissions have a 50% decline rate (9/18), suggesting automated IT workflows are not populating required fields correctly before submission.

### `submission_origin` (TAPP column)
| Origin | Total | Declined | Decline Rate |
|---|---|---|---|
| auto_generated | 164 | 18 | 11.0% |
| manual_acquisition | 313 | 26 | 8.3% |
| provision_service | 23 | 2 | 8.7% |

Auto-generated submissions decline at a modestly higher rate, consistent with incomplete metadata in automated flows.

---

## 6. Asset Type and Cost

### `asset_category_type` (TAPP column)
| Asset Category | Total | Declined | Decline Rate |
|---|---|---|---|
| miscellaneous | 14 | 3 | 21.4% |
| travel | 93 | 10 | 10.8% |
| hardware | 318 | 27 | 8.5% |
| software_service | 75 | 6 | 8.0% |

### `is_high_cost_asset_type` (TAPP column)
| High Cost | Total | Declined | Decline Rate |
|---|---|---|---|
| False | 189 | 20 | 10.6% |
| True | 311 | 26 | 8.4% |

High-cost assets are **not** more likely to be declined — cost-based scrutiny does not appear to be a driver.

### Amount Quartiles
| Quartile | Range | Decline Rate |
|---|---|---|
| Q1 (lowest) | ~$50–$2,200 | 13.5% |
| Q2 | ~$2,200–$4,300 | 10.5% |
| Q3 | ~$4,300–$6,500 | 5.6% |
| Q4 (highest) | ~$6,500+ | 7.2% |

Lower-value submissions decline at higher rates, further ruling out cost as the primary cause and pointing toward documentation quality (low-value submissions may receive less scrutiny in preparation).

---

## 7. Recommendations

| Priority | Action | Expected Impact |
|---|---|---|
| **1 — High** | Audit IT department submission workflows end-to-end; require mandatory validation before submission | ~19 declines (41% of all) |
| **2 — High** | Enforce `source_id` linking for all categories, especially Travel (currently 0% compliance) | ~14 declines |
| **3 — Medium** | Require specific model/product identification in CI field; reject `generic_label` entries at submission time (`ci_specificity` signal) | ~11 declines |
| **4 — Medium** | Fix auto-generated submission pipelines (`submission_origin = auto_generated`, `submission_action_type = auto_creation`) to populate required metadata fields before submission | ~9 declines |
| **5 — Low** | Add validation guidance for `miscellaneous` category submissions (17.6% decline, 21.4% for miscellaneous asset type) | ~3 declines |

---

## Method Note

**TAPP-generated columns used in this analysis:** `ci_specificity`, `submission_action_type`, `submission_origin`, `asset_category_type`, `is_high_cost_asset_type`.

Columns `asset_brand_family` and `submitting_department` were reviewed but found to be largely redundant with `department` or low-signal for the query. The `source_id_present` TAPP column was used as a key driver alongside the raw `source_id` field, where missing values in the original column confirm the same pattern (n=112 missing, 12.5% decline rate).
