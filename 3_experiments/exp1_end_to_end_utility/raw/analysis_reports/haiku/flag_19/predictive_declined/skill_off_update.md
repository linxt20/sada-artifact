---
dataset: flag_19
scenario: predictive_declined
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "state_declined"
query: "What signals suggest an expense will be declined?"
source_table: augment_table/flag_19/predictive_declined/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:14:22.973782+00:00
wall_seconds: 43.78
---

# Expense Decline Prediction Signals Analysis

## Executive Summary

The dataset contains 500 expense records, of which **46 (9.2%) were declined**. A clear and dominant pattern emerges: **all declined expenses lack a processed date** (100% vs. 26.7% in non-declined records), indicating these expenses never completed processing. Beyond this structural signal, elevated risk scores and IT department concentration provide secondary predictive value.

## Primary Signal: Missing Processed Date (100% Predictive)

The most critical decline indicator is a **missing `processed_date`** value:

- **100% of declined expenses** have `missing_processed_date = 1`
- Only **26.7% of non-declined expenses** have this missing value
- This creates a **3.74x difference in likelihood** of decline

### Interpretation

A missing processed date suggests the expense was entered into the system but **never successfully processed to completion**. This is a near-perfect differentiator between declined and successfully handled expenses.

## Secondary Signal: Elevated Risk Score

Declined expenses carry substantially higher risk scores:

- **Declined expenses**: mean risk score = 6.5 (range: 5–9, median: 6)
- **Non-declined expenses**: mean risk score = 2.9 (range: 0–12, median: 1)

The typical declined expense carries a **2.3x higher risk score**, suggesting systematic flagging of problematic records.

## Department and Category Patterns

### IT Department Concentration
- **41.3% of declined expenses** originate from the IT department
- Of all IT department expenses (n=43), **44.2% are declined**—the highest decline rate by department
- In contrast, other departments show much lower decline rates

### Asset Category Dominance
- **58.7% of declined expenses** are in the "Assets" category
- This reflects the dataset's focus on hardware asset management and procurement

## Missing Source ID (Secondary Indicator)

- **28.3% of declined expenses** have a missing `source_id`
- Only **21.6% of non-declined expenses** are missing `source_id`
- Notably, **71.7% of declined expenses have only the processed date missing**, suggesting data collection issues are not the root cause of all declines

## Temporal Patterns

All declined expenses show `processing_delay_days = 999` (encoding missing or stalled processing):
- **100% of declined expenses** have this value
- Only **26.7% of non-declined expenses** show this pattern
- This aligns perfectly with the missing processed date signal

## Status Indicators

A notable distinction is that **0% of declined expenses** have `is_pending = 1` or `is_submitted = 1`. All declined records show:
- `is_pending = 0`
- `is_submitted = 0`

This indicates declined expenses are **not in transient states**—they are finalized as declined.

## Amount and Categorical Attributes

- **No significant difference** in `amount_is_low` or `amount_is_high` flags between declined and non-declined expenses
- **No strong correlation** between travel category (`is_travel_category`) and decline rates
- Average amounts are slightly lower for declined expenses ($3,706 vs. $4,429), but the overlap is substantial

## Summary of Decline Signals (Ranked by Strength)

| Signal | Declined Rate | Non-Declined Rate | Strength |
|--------|---------------|-------------------|----------|
| **Missing processed_date** | 100% | 26.7% | **Dominant** |
| **Risk score ≥ 5** | ~95% | ~30% | **Very Strong** |
| **IT department** | 41.3% | 10.5% | Strong |
| **Processing delay = 999** | 100% | 26.7% | **Dominant** |

## Conclusion

An expense is likely to be declined if it exhibits **a missing processed date combined with elevated risk scoring (≥5)**. The IT department context increases this risk. Notably, declined expenses are **not in-flight statuses** (Pending/Submitted)—they represent final, failed resolution states. The absence of a processed date is nearly a perfect indicator and suggests systemic processing failures, system errors, or policy violations that prevent completion.
