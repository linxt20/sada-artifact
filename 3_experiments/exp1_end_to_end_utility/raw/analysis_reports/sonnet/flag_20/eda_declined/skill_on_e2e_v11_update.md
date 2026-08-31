---
dataset: flag_20
scenario: eda_declined
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "state_declined"
query: "What signals in a travel-expense description predict whether it will be declined?"
source_table: augment_table/flag_20/eda_declined/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:18:13.663729+00:00
wall_seconds: 78.56
---

# Signals Predicting Travel-Expense Description Declines

## Overview

The dataset contains **500 expense records** across four categories: Assets, Travel, Services, and Miscellaneous. Of these, **84 are Declined (16.8% overall decline rate)**. The Travel category is the dominant driver of declines: it accounts for **61 of 84 declined records (73%)** at a category decline rate of **41.8%**, versus 6.0% for Assets and 10.6% for Services.

---

## 1. Primary Signal: Missing `processed_date`

The single strongest predictor is whether a `processed_date` exists:

| `processed_date` present | Declined | Total | Decline Rate |
|--------------------------|----------|-------|--------------|
| Yes | 0 | 295 | **0.0%** |
| No | 84 | 205 | **41.0%** |

**No record with a processed_date was ever declined.** Among Travel-only rows, the effect is even sharper:

| `processed_date` present (Travel) | Declined | Total | Decline Rate |
|-----------------------------------|----------|-------|--------------|
| Yes | 0 | 52 | **0.0%** |
| No | 61 | 94 | **64.9%** |

This is the clearest structural signal in the data: absence of a processing timestamp is a necessary condition for decline.

---

## 2. Category: Travel Is the Dominant Risk Group

| Category | Declined | Total | Decline Rate |
|----------|----------|-------|--------------|
| Travel | 61 | 146 | **41.8%** |
| Services | 5 | 47 | 10.6% |
| Assets | 17 | 281 | 6.0% |
| Miscellaneous | 1 | 26 | 3.8% |

TAPP-augmented column `asset_category` confirms this — rows tagged `travel` have a 41.4% decline rate vs. 6.6% for `hardware` and 11.1% for `cloud_service`.

---

## 3. Missing Source ID (`has_source_id`)

TAPP-generated column `has_source_id` is a strong predictor:

| `has_source_id` | Declined | Total | Decline Rate |
|-----------------|----------|-------|--------------|
| True | 22 | 327 | **6.7%** |
| False | 62 | 173 | **35.8%** |

Critically, **all 146 Travel records have `has_source_id = False`** — so missing source IDs are a necessary but not sufficient condition for Travel declines. Within non-Travel categories, the decline rate for missing source IDs is much lower, confirming that missing source ID is structurally coupled with the Travel category rather than being an independent causal factor.

---

## 4. TAPP `action_type`: Travel-Expense vs. Other Action Types

TAPP-generated `action_type` cleanly separates records:

| `action_type` | Declined | Total | Decline Rate |
|---------------|----------|-------|--------------|
| travel_expense | 58 | 141 | **41.1%** |
| procurement | 5 | 65 | 7.7% |
| allocation_registration | 16 | 242 | 6.6% |
| service_provision | 4 | 43 | 9.3% |

The `travel_expense` action type is a reliable proxy for Travel category records and independently confirms the risk concentration.

---

## 5. TAPP `description_specificity`: Weak Signal Within Travel

TAPP-generated `description_specificity` categories across all records:

| `description_specificity` | Declined | Total | Decline Rate |
|---------------------------|----------|-------|--------------|
| generic_category_label | 51 | 254 | **20.1%** |
| auto_generated_template | 24 | 132 | 18.2% |
| specific_asset_named | 9 | 114 | **7.9%** |

Specificity does differentiate: records with a named asset have a much lower decline rate (7.9%). However, **within the Travel category alone**, the signal collapses — all three specificity types have 25–43% decline rates, showing that specificity alone cannot rescue a travel expense from decline.

---

## 6. Amount: Modest Inverse Relationship

Declined travel expenses have a lower mean amount ($3,793) than non-declined travel expenses ($4,444). Across all records:

| State | Mean Amount | Median Amount |
|-------|-------------|---------------|
| Declined | $3,912 | $3,722 |
| Processed | $4,284 | $4,087 |
| Submitted | $5,712 | $5,884 |

Within Travel, low-amount records (<$2,000) are declined at 57.1%, compared to 27.3% for amounts $6,000–$8,000. However, this effect is modest compared to the category and processing-status signals.

---

## 7. TAPP `is_luxury_or_premium`: Marginal Signal

TAPP-generated `is_luxury_or_premium`:

| `is_luxury_or_premium` | Declined | Total | Decline Rate |
|------------------------|----------|-------|--------------|
| True | 4 | 12 | **33.3%** |
| False | 80 | 488 | 16.4% |

The luxury flag elevates decline risk, but coverage is low (only 12 records flagged True), limiting its practical utility.

---

## 8. Department: Secondary Differentiator

| Department | Declined | Total | Decline Rate |
|------------|----------|-------|--------------|
| HR | 1 | 5 | 20.0% |
| Sales | 26 | 141 | **18.4%** |
| Customer Support | 48 | 272 | **17.6%** |
| IT | 7 | 42 | 16.7% |
| Finance | 1 | 16 | 6.3% |
| Development | 0 | 16 | **0.0%** |

TAPP `department_group` mirrors these rankings. The Sales and Customer Support elevation is driven primarily by their heavy Travel category usage, not an independent departmental policy.

---

## Summary: Ranked Predictive Signals

| Rank | Signal | Source | Strength |
|------|--------|--------|----------|
| 1 | `processed_date` absent | Original | Necessary condition; 41% → 65% (Travel) decline rate |
| 2 | `category` = Travel | Original | 41.8% decline rate vs. ≤10.6% elsewhere |
| 3 | `action_type` = travel_expense | TAPP | 41.1% decline rate; mirrors category |
| 4 | `has_source_id` = False | TAPP | 35.8% overall; fully overlaps Travel category |
| 5 | Low amount (<$2,000, Travel) | Original | 57.1% vs. 27.3% at higher amounts |
| 6 | `description_specificity` = specific_asset_named | TAPP | 7.9% vs. 18–20% for generic/template — effective outside Travel |
| 7 | `is_luxury_or_premium` = True | TAPP | 33.3% but very low coverage (n=12) |

---

## Method Note

TAPP-generated columns used in this report: `asset_category`, `action_type`, `description_specificity`, `has_source_id`, `is_luxury_or_premium`, `department_group`. Columns `asset_brand_vendor`, `creation_method`, and `hardware_subtype` were examined but found weak or redundant — `creation_method` (manual vs. automated) showed a 17.8% vs. 15.0% decline rate, not meaningfully predictive.
