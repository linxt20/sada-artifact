---
dataset: flag_20
scenario: causal_reduce
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: what_if
focus_variable: "travel_expense_declined_status"
query: "How can we reduce declined travel expenses?"
source_table: augment_table/flag_20/causal_reduce/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:17:59.538948+00:00
wall_seconds: 85.88
---

# Reducing Declined Travel Expenses: Analysis Report

## Executive Summary

Travel expenses have a **41.8% decline rate** (61/146 records in `category == Travel`; 60/141 in `expense_category == travel_expense`), compared to 6.0% for Assets, 10.6% for Services, and 3.8% for Miscellaneous. This is the dominant quality problem in the expense dataset and is driven by a combination of missing documentation, vague item specification, and department-level submission practices.

---

## Method Note

TAPP-generated columns used in this report: **`is_travel_related`**, **`expense_category`**, **`entry_origin`**, **`has_source_id`**, **`ci_specificity`**, **`expense_action_type`**, **`submitting_department`**. Columns `processing_lag_category` and `asset_brand` were evaluated but found redundant or not meaningfully predictive of travel declines and are not centered in the analysis.

---

## 1. Scale of the Problem

| Category | Total | Declined | Decline Rate |
|---|---|---|---|
| Travel | 146 | 61 | **41.8%** |
| Services | 47 | 5 | 10.6% |
| Assets | 281 | 17 | 6.0% |
| Miscellaneous | 26 | 1 | 3.8% |
| **All** | **500** | **84** | **16.8%** |

Of the 84 total declined expenses, **73% (61/84) are travel-related**, making travel the single largest lever for reducing overall declines.

---

## 2. Missing Source ID: A Universal Travel Problem

Every single travel expense record (141/141 with `expense_category == travel_expense`) has **`has_source_id = False`**. In contrast, non-travel categories show no meaningful difference in decline rate between records with and without a source ID (6.2% vs 6.7%). This suggests that the source-ID gap is structural to the travel submission workflow, not a documentation hygiene issue unique to declined claims. Fixing the upstream system to attach a source reference ID to all travel claims at submission time is the highest-leverage single intervention.

---

## 3. Vague Item Description Drives Higher Decline Rates

The TAPP column **`ci_specificity`** captures how precisely the configuration item (CI) field names the claimed item:

| `ci_specificity` | Total Travel Claims | Declined | Decline Rate |
|---|---|---|---|
| `category_label_only` | 73 | 36 | **49.3%** |
| `generic_placeholder` | 21 | 9 | 42.9% |
| `specific_named_model` | 47 | 15 | **31.9%** |

Claims with only a vague category label (e.g., "Travel Equipment") are declined at a rate **17 percentage points higher** than those with a specific named item. This pattern holds across all departments. Requiring submitters to name the specific item/vendor in the CI field is a concrete process fix.

---

## 4. Department-Level Concentration

| Department | Total Travel Claims | Declined | Decline Rate |
|---|---|---|---|
| IT | 11 | 6 | **54.5%** |
| HR | 2 | 1 | 50.0% |
| Customer Support | 77 | 34 | **44.2%** |
| Sales | 43 | 18 | 41.9% |
| Finance | 3 | 1 | 33.3% |
| Development | 4 | 0 | 0.0% |
| Product Management | 1 | 0 | 0.0% |

**Customer Support** drives the most declined travel claims in absolute terms (34), while **IT** has the highest decline rate (54.5%). Development and Product Management have zero travel declines, suggesting their submission practices can serve as an internal benchmark.

The `submitting_department` TAPP column aligns with the raw `department` column and confirms no routing mismatch between submitting and recorded departments.

---

## 5. Entry Origin: Automated vs. Manual Submissions

The **`entry_origin`** TAPP column breaks down how travel expenses entered the system:

| `entry_origin` | Total | Declined | Decline Rate |
|---|---|---|---|
| `travel_expense_claim` | 94 | 41 | 43.6% |
| `automated_system` | 41 | 17 | 41.5% |
| `manual_procurement` | 6 | 2 | 33.3% |

Decline rates are nearly identical across entry origins (~41–44%), indicating the problem is not input channel–specific. Automated system entries are nearly as likely to be declined as manual claims, pointing to a data quality issue upstream of the submission channel.

---

## 6. Amount and Processing Lag

| Amount Range | Declined | Processed |
|---|---|---|
| $0–$2,000 | 16 | 10 |
| $2,001–$4,000 | 15 | 17 |
| $4,001–$6,000 | 21 | 11 |
| $6,001–$8,000 | 8 | 12 |

Higher-amount claims ($4,001–$6,000) show a higher rate of declines relative to approvals. The **`processing_lag_category`** column shows that all 60 declined travel expenses fall in `not_processed`, which is expected (declined = no processed date), so lag is not an independent driver.

---

## 7. Recommendations

1. **Mandate source IDs on all travel submissions.** All 141 travel claims lack `has_source_id`. Linking each claim to a booking reference, PO number, or approval ticket is the most systemic fix.

2. **Require specific item/vendor naming in the CI field** (`ci_specificity`). Moving from category-label-only to specific-named-model claims cuts the decline rate from 49% to 32%. Enforce this with form validation.

3. **Target Customer Support and IT with corrective training.** These departments account for 40 of 60 declined travel claims. Reviewing Development's zero-decline practices and sharing them as a template is recommended.

4. **Audit high-value claims ($4,001–$6,000) proactively.** This band shows the worst declined-to-processed ratio and warrants a pre-submission review step.

5. **Fix automated system submissions.** A 41.5% decline rate for `entry_origin == automated_system` means the automated pipeline is generating non-compliant entries; the schema or approval logic feeding it needs correction.
