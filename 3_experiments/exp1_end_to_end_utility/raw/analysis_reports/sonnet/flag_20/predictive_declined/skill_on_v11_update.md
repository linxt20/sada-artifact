---
dataset: flag_20
scenario: predictive_declined
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "state_declined"
query: "What signals suggest a travel expense will be declined?"
source_table: augment_table/flag_20/predictive_declined/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:17:58.281741+00:00
wall_seconds: 58.3
---

# Travel Expense Decline Signals — Analysis Report

**Dataset:** `sonnet__skill_on_v11_update.csv` (500 rows, 22 columns)  
**Focus:** Travel category expenses (`category == Travel`), n = 146 rows  
**Outcome variable:** `state` (Declined, Processed, Pending, Submitted)

---

## Executive Summary

Within travel expenses, **61 of 146 records (42%)** are Declined — the single most common outcome. Several columns are strongly or perfectly predictive of decline. The signals below are ranked by strength.

---

## Signal 1: `processing_lag_bucket == not_processed` — Near-Perfect Predictor

Every single declined travel expense has `processing_lag_bucket = not_processed`. Conversely, **no processed travel expense is unprocessed** — all processed records carry a non-trivial lag bucket (same_day, one_to_three_days, etc.).

| processing_lag_bucket | Declined | Processed |
|---|---|---|
| not_processed | **61 (100%)** | 0 |
| same_day / 1–3 / 4–7 / 7+ days | 0 | **52 (100%)** |

> **This is the strongest single signal.** A travel expense that remains unprocessed is either declined, pending, or submitted — never resolved successfully.

---

## Signal 2: `source_id_present == False` — Universal for Travel Declined

All 61 declined travel records have `source_id_present = False`. However, so do all processed and pending travel records — travel expenses universally lack a source ID. This column **cannot discriminate** within travel but confirms travel is structurally different from Assets/Services.

---

## Signal 3: `expense_origin_method == procurement_request` — 100% Decline Rate

All 4 travel expense rows where `expense_origin_method = procurement_request` were **Declined** (100%). This is a small sample (n=4) but a clean signal. Automated and manual methods show mixed outcomes (~40% decline each), so method alone is weak except for this edge case.

| Method | Declined Rate |
|---|---|
| procurement_request | **100%** (4/4) |
| automated | 40% (17/42) |
| manual | 40% (40/100) |

---

## Signal 4: `description_specificity == generic_or_placeholder` — Elevated Decline Rate

Travel expenses with generic/placeholder descriptions decline at **51.5%** vs 29.3% for those with `specific_model_named`.

| description_specificity | Declined Rate |
|---|---|
| generic_or_placeholder | **51.5%** |
| auto_generated_template | 38.5% |
| specific_model_named | 29.3% |

---

## Signal 5: `is_non_standard_item == False` — Slightly Higher Decline Rate

Somewhat counterintuitively, travel expenses with `is_non_standard_item = False` have a **52.6%** decline rate vs 40.2% for non-standard items. This is a weak signal and may reflect data artifacts; it should not be overweighted.

---

## Signal 6: Department — IT and HR Show Elevated Rates

| Department | Declined Rate |
|---|---|
| IT | **54.5%** |
| HR | 50.0% |
| Customer Support | 44.3% |
| Sales | 40.9% |
| Finance | 25.0% |
| Development | 0% (n=5) |

IT and HR travel expenses decline more frequently. Development has 0% but is a very small sample (n=5).

---

## Signal 7: `amount` — Weak Differentiator

Declined travel expenses have a mean amount of **$3,793** vs $3,928 for processed — no meaningful difference. Amount is not a useful predictor of travel expense decline in this dataset.

---

## Combined Decline Profile

A travel expense is most likely to be **Declined** when:
1. `processing_lag_bucket = not_processed` ✔ (necessary condition in the data)
2. `description_specificity = generic_or_placeholder`
3. `expense_origin_method = procurement_request`
4. Submitted from IT or HR department

---

## Caveats & Weak Evidence

- **`source_id_present`** is False for *all* travel rows, making it category-level noise rather than a within-travel signal.
- The `procurement_request` signal is based on only 4 rows — interpret with caution.
- `amount` shows no meaningful pattern and should be excluded from any predictive rule.
- Pending and Submitted outcomes share the `not_processed` bucket with Declined, so further time-based observation is needed to distinguish eventual outcomes.
