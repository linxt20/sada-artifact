---
dataset: flag_19
scenario: concept_attribute_declined
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "declined_expense_reasons"
query: "What reasons or compliance risks appear in declined expenses?"
source_table: augment_table/flag_19/concept_attribute_declined/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:13:39.195635+00:00
wall_seconds: 50.25
---

# Compliance Risk Analysis: Declined Expenses

## Dataset Overview

- **Total declined expenses:** 46 out of the full dataset
- **Declined expenses lack `processed_date`** in all cases — a consistent structural signal distinguishing them from Processed records
- **Average amount (declined):** $3,706 | **High-risk subset average:** $7,203

---

## Decline Reason Flags: Frequency Breakdown

| Decline Reason Flag | Count | % of Declined |
|---|---|---|
| `no_processing_record` | 46 | 100% |
| `auto_generated_missing_manual_documentation` | 15 | 33% |
| `missing_source_reference` | 13 | 28% |
| `high_value_requires_additional_approval` | 9 | 20% |
| `exceeds_standard_threshold` | 5 | 11% |
| `travel_expense_outside_policy_department` | 3 | 7% |
| `service_expense_outside_authorized_department` | 3 | 7% |
| `insufficient_categorization` | 3 | 7% |
| `potential_policy_violation_luxury_travel` | 1 | 2% |

> **Key finding:** `no_processing_record` appears on every single declined expense — it is a necessary (though not sufficient) marker of decline. It likely indicates the absence of a completed processing workflow before submission.

---

## Compliance Risk Level Distribution

| Risk Level | Count | Primary Compliance Category |
|---|---|---|
| Medium | 24 (52%) | Documentation Gap / Authorization Control |
| Low | 11 (24%) | Documentation Gap |
| High | 11 (24%) | Authorization Control |

### Compliance Categories
- **Documentation Gap** — 31 cases (67%): Missing records, auto-generated entries lacking manual review, absent source references, or insufficient categorization.
- **Authorization Control** — 14 cases (30%): High-value purchases requiring additional approval, or amounts exceeding standard thresholds. High-risk cases average **$7,203**, well above the overall declined average.
- **Policy Violation** — 1 case (2%): A luxury business-class travel claim (`potential_policy_violation_luxury_travel`).

---

## Patterns by Expense Category

| Category | Declined Count | Notes |
|---|---|---|
| Assets | 27 (59%) | Dominant category; many auto-generated entries without manual documentation |
| Travel | 10 (22%) | Frequently flagged for missing source references and out-of-policy department travel |
| Services | 6 (13%) | Often flagged for submission outside authorized departments |
| Miscellaneous | 3 (7%) | All flagged for `insufficient_categorization` |

---

## Department Concentration

IT (19 declines) and Customer Support (16 declines) together account for **76%** of all declined expenses. IT is overrepresented relative to other departments and shows the most High-risk Authorization Control cases.

---

## Notable Exceptions / Weak Evidence

- **Low-risk declines** (11 cases) carry only `no_processing_record` with no secondary flags, suggesting procedural oversights rather than intentional violations.
- The single **Policy Violation** case (luxury travel) is an outlier — the dataset does not broadly reflect luxury spend abuse.
- `auto_generated_missing_manual_documentation` co-occurs with high-value flags in several IT cases (e.g., EXP00000033, EXP00000238), suggesting auto-generation workflows may be bypassing required manual approvals for large purchases.

---

## Summary for Decision-Makers

1. **Process gap:** Every declined expense lacks a processing record — enforce workflow completion before submission.
2. **Documentation controls:** One-third of declines stem from auto-generated entries missing human review; manual sign-off requirements should be enforced on auto-generated asset lines.
3. **Value thresholds:** High-value asset purchases ($5,000+) consistently trigger authorization failures, especially in IT. Proactive pre-approval routing for high-value items is warranted.
4. **Department-based policy:** Travel and service expenses submitted from non-authorized departments are a recurring issue — department-level expense policy visibility should be improved.
