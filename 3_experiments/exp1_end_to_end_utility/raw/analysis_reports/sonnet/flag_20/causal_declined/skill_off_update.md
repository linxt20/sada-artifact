---
dataset: flag_20
scenario: causal_declined
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "state_declined"
query: "Why do some travel expenses get declined, and which factors contribute the most?"
source_table: augment_table/flag_20/causal_declined/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:16:37.749247+00:00
wall_seconds: 36.8
---

# Why Travel Expenses Get Declined: Factor Analysis

## Dataset Overview

The dataset contains 500 expense records across categories (Assets, Travel, Services, Miscellaneous). Of 146 travel expenses (`is_travel = 1`), **61 (42%)** were Declined — a far higher decline rate than for non-travel expenses (23 declined out of 354, ~6.5%).

---

## Key Finding: Missing Processed Date is the Dominant Factor

The single strongest predictor of a declined travel expense is **`missing_processed_date`**:

| State | `missing_processed_date = 0` | `missing_processed_date = 1` |
|-----------|------|------|
| Declined | **0** | **61** |
| Processed | **52** | **0** |
| Pending | 0 | 18 |
| Submitted | 0 | 15 |

This is a **perfect split** among travel records: every declined travel expense has a missing processed date, and every processed travel expense has a valid processed date. This makes `missing_processed_date` the clearest causal indicator — expenses that were never formally logged as processed are systematically declined.

---

## Secondary Factor: Amount Above Travel Median

Among declined travel expenses, 46% had `amount_above_travel_median = 1` (vs. 40% for processed), suggesting higher-cost travel expenses are *somewhat* more prone to decline. However, this difference is modest and not deterministic — many below-median travel expenses are also declined (33 out of 61 declined had `amount_above_travel_median = 0`).

> **Weak signal**: Amount alone does not explain decline outcomes; it likely amplifies risk when combined with missing documentation.

---

## Departmental Concentration

Declined travel expenses are concentrated in specific departments:

| Department | Declined Travel Count |
|---|---|
| Customer Support | 35 |
| Sales | 18 |
| IT | 6 |
| HR / Finance | 1 each |

The `dept_travel_decline_rate` for declined records averages **0.44** vs. **0.39** for processed, indicating departments like Customer Support and IT (with higher departmental decline rates ~0.44–0.55) contribute more declined travel submissions.

---

## Summary of Contributing Factors

| Factor | Strength | Direction |
|---|---|---|
| `missing_processed_date` | **Very strong (deterministic)** | Missing → Declined |
| `dept_travel_decline_rate` | Moderate | Higher rate → more declines |
| `amount_above_travel_median` | Weak | Above median → slightly more risk |

**Bottom line:** Travel expenses are declined primarily because they lack a processed date — likely reflecting missing approval, incomplete submission, or workflow failure. Departmental practices (reflected in `dept_travel_decline_rate`) and high amounts are secondary contributors. Any intervention to reduce declines should focus on ensuring the processing step is completed at submission time.
