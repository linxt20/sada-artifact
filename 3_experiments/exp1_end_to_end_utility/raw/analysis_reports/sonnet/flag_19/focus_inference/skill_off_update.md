---
dataset: flag_19
scenario: focus_inference
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth analyzing and actionable in these expense records."
source_table: augment_table/flag_19/focus_inference/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:14:25.293653+00:00
wall_seconds: 52.43
---

# Expense Records Analysis Report

## Dataset Overview

- **500 expense records** across 15 columns
- Key fields: `amount`, `state`, `category`, `department`, `missing_source_id`, `processing_lag_days`, `submitter_expense_count`
- Amount range: $137–$8,987 (mean ~$4,363)

---

## 1. Missing Source IDs — A Structural Control Risk

**111 records (22%)** have `missing_source_id = Yes`. This is not random: it maps **exactly** to two categories — **Travel** (94 records) and **Miscellaneous** (17 records). Assets and Services have zero missing source IDs.

| Category | Missing Source ID |
|---|---|
| Travel | 94 (100% of Travel) |
| Miscellaneous | 17 (100% of Misc) |
| Assets | 0 |
| Services | 0 |

**Actionable:** All Travel and Miscellaneous expenses lack source IDs — this appears systematic rather than incidental, suggesting a process gap in how these categories are submitted. Mandating source IDs at submission for these categories is a clear control improvement.

---

## 2. Unresolved Pending Expenses — ~$352K in Limbo

**80 records are in `Pending` state**, concentrated in Customer Support (43) and Sales (17). Pending amounts total approximately **$351,805**, with Assets ($244K) and Travel ($90K) dominating.

- 21 Pending Travel records are **all missing source IDs**, totaling ~$90,151
- These records have no `processed_date`, meaning they are untracked in the pipeline

**Actionable:** Pending Travel expenses with no source ID and no processed date represent the highest-risk backlog. Priority review should start here.

---

## 3. Declined Rate Is Elevated in IT

**46 records (9.2%) are Declined**, with IT accounting for 19 of them — disproportionately high given IT represents only 43 total records (~44% decline rate vs. ~9% overall). Customer Support has 16 declines out of 267 records (~6%).

**Actionable:** IT's high decline rate warrants investigation — whether it's policy violations, duplicate submissions, or budget misalignment. HR also shows 2 declines on 14 records (~14%), a small but notable signal.

---

## 4. Assets Drive Volume and Cost

**Assets** are the largest category (310 records, 62%) and have the highest average amount (~$5,439 vs. ~$4,094 for Travel and ~$940 for Services). All Asset records have valid source IDs.

Services expenses average only ~$940 and carry low risk. Miscellaneous (17 records, avg ~$2,117) are all missing source IDs and warrant scrutiny given their classification.

---

## 5. High-Value Travel with Missing Source IDs

**20 records** are classified as High-tier amount (`$6,500+`) **and** missing a source ID. All fall in the Travel category. Several are in Pending or Submitted states (not yet processed), meaning they have not been reviewed.

**Actionable:** These 20 records should be individually audited before approval.

---

## 6. Processing Lag — Limited Signal

`processing_lag_days` is only populated for **106 records** and is uniformly **1 day** across all of them. This column has no discriminating power in this dataset — it cannot be used to identify slow-processing outliers.

---

## 7. Submitter Expense Count — No Anomaly Pattern

`submitter_expense_count` ranges from 3 to 17, with a mean of ~10. The distribution is nearly identical for records with and without missing source IDs (means of 10.09 vs. 10.17). High-volume submitters (e.g., Helene Iberg at 17, Felipe Mahone at 16) do not appear to concentrate in any problematic state or category.

**Weak evidence:** This field does not differentiate risk in the current dataset.

---

## Summary of Actionable Priorities

| Priority | Issue | Scope |
|---|---|---|
| 🔴 High | All Travel/Misc expenses lack source IDs | 111 records |
| 🔴 High | Pending Travel expenses missing source IDs | 21 records, ~$90K |
| 🟠 Medium | IT department high decline rate (~44%) | 19 declined records |
| 🟠 Medium | High-value Travel with no source ID, unprocessed | 20 records |
| 🟡 Low | Miscellaneous category classification clarity | 17 records |
