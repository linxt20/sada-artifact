---
dataset: flag_20
scenario: focus_inference
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth analyzing in these travel-expense records."
source_table: augment_table/flag_20/focus_inference/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:17:54.309879+00:00
wall_seconds: 57.7
---

# Travel-Expense Records: Analysis Report

## Dataset Overview

The dataset contains **500 expense records** across four categories: Assets (281), **Travel (146)**, Services (47), and Miscellaneous (26). The focus variable is the **Travel** category, which is structurally distinct from all other categories in several ways worth investigating.

---

## 1. Travel Records Are Systematically Missing Source IDs

**Every single Travel record (146/146) has `has_source_id = False`**, meaning none carry a traceable external source reference (e.g., a purchase order or ticket number). By contrast, 327 of the 354 non-Travel records have a source ID. This is the sharpest structural signal in the data:

| Category | has_source_id = True | has_source_id = False |
|---|---|---|
| Travel | 0 (0%) | 146 (100%) |
| Non-Travel | 327 (92%) | 27 (8%) |

This likely reflects a systemic process gap: travel expenses are submitted without tying them to a backing document/PO.

---

## 2. Travel Has a Disproportionately High Decline Rate

- **Overall decline rate:** 16.8%
- **Travel decline rate:** 41.8% (61 of 146 records)

This is 2.5× the average. The absence of a source ID is the likely driver — and the correlation is total (all declined travel records also have `has_source_id = False`). However, since all travel records lack source IDs, source ID absence alone cannot distinguish declined from approved travel claims; other factors must also be at play.

---

## 3. Processing Lag Is Lower for Travel (When Processed)

Of the 52 Travel records that were processed:
- **Median lag: 2 days** (vs. 5 days for non-Travel)
- **Mean lag: 4.6 days** (vs. 5.7 days for non-Travel)

Travel expense approvals that do go through tend to move faster than hardware/asset procurement — likely because they don't require inventory workflows.

---

## 4. Amount Patterns by State

| State | Avg Amount ($) | Count |
|---|---|---|
| Submitted | 6,167 | 15 |
| Pending | 4,498 | 18 |
| Processed | 3,928 | 52 |
| Declined | 3,793 | 61 |

**Submitted records carry the highest average amounts ($6,167)** — these are unresolved and skew large. Several submitted records exceed $7,500. This unresolved backlog is a risk worth tracking. Declined records are not concentrated in high amounts, suggesting amount is not the primary driver of declines.

---

## 5. Asset Form Factor: Travel Gear Dominates, Laptops Are an Anomaly

| Form Factor | Total | Declined | Processed |
|---|---|---|---|
| travel_gear | 89 | 38 (43%) | 32 (36%) |
| laptop | 35 | 12 (34%) | 13 (37%) |
| vehicle | 9 | 5 (56%) | 2 (22%) |
| Unknown | 9 | 3 | 4 |
| networking | 3 | 2 | 1 |

**35 travel records are classified as laptops** (e.g., "TravelMate P6 Laptop", "Dell Latitude E7470") — these appear to be hardware assets that were miscategorized under Travel. Similarly, vehicles and networking devices in Travel records look like misclassification. **Vehicles have the highest decline rate (56%).**

---

## 6. Departmental Concentration

**Customer Support (79 records, 54%)** and **Sales (44 records, 30%)** account for 84% of all Travel submissions. Customer Support also has the most declines (35) and the most submitted-but-pending high-value records.

---

## Key Exceptions and Caveats

- The `type` column is entirely empty for all records — it provides no analytical value.
- `department_group` largely mirrors `department` but contains one `Unknown` value (EXP00000032 in Development).
- The absence of source IDs in all travel records means `has_source_id` cannot differentiate within the travel cohort; it only marks a categorical boundary.
- `has_processing_lag` being `True` for processed records and `False` otherwise appears to be a derived flag rather than an independent predictor.

---

## Decision-Ready Summary

| Priority | Finding | Action |
|---|---|---|
| High | 100% of travel records lack source IDs | Mandate reference IDs for travel submissions |
| High | 41.8% of travel claims declined | Audit travel expense policy; source ID requirement likely to reduce declines |
| Medium | 15 submitted records (~$80K total exposure) unresolved | Follow up to close pending travel claims |
| Medium | ~35 laptop + vehicle records in Travel category | Review classification logic; these may be misfiled asset records |
| Low | Customer Support generates 54% of travel volume | Consider department-level travel budget controls |
