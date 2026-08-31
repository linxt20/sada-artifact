---
dataset: flag_20
scenario: causal_declined
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "state_declined"
query: "Why do some travel expenses get declined, and which factors contribute the most?"
source_table: augment_table/flag_20/causal_declined/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:17:22.247257+00:00
wall_seconds: 62.8
---

# Travel Expense Decline Analysis

## Overview

The dataset contains **500 expense records**, of which **146 (29.2%) are travel-related** (`is_travel_related = True`). Travel-related expenses are declined at a dramatically higher rate than non-travel ones:

| Segment | Total | Declined | Decline Rate |
|---|---|---|---|
| Travel-related | 146 | 61 | **41.8%** |
| Non-travel | 354 | 23 | 6.5% |

Being travel-related is itself the dominant predictor of decline. The analysis below identifies which factors within the travel segment drive outcomes.

---

## Key Factors Contributing to Declines

### 1. Processing Lag Band — Strongest Single Predictor

Travel rows that are **`not_processed`** (no `processed_date`) are declined at a rate of **64.9%** (61 of 94 not-processed travel rows are declined). Every travel row that was actually processed (same-day, 1–3 days, 4–7 days, 8–30 days, or 30+ days) has a **0% decline rate**.

> **Implication:** Decline and non-processing are tightly coupled — expenses that lack a processed timestamp are almost certainly declined or stalled. The causal direction is likely that declined records are never assigned a processed date, making this a near-perfect proxy for rejection.

### 2. CI Specificity — Poor Item Description Increases Risk

Among travel rows, vaguely described configuration items are declined far more often:

| `ci_specificity` | Travel Rows | Decline Rate |
|---|---|---|
| `generic_placeholder` | 4 | **75.0%** |
| `service_descriptor` | 8 | **50.0%** |
| `travel_label_only` | 99 | **46.5%** |
| `specific_model` | 35 | **22.9%** |

Expenses with a **specific model** named (e.g., a concrete product) are declined at roughly half the rate of those using generic or label-only descriptions. This strongly suggests that insufficient item specificity is a material driver of rejection.

### 3. Entry Method — Manual Procurement Riskiest

| `entry_method` | Decline Rate (travel) |
|---|---|
| `manual_procurement` | **58.3%** |
| `automated_generated` | 44.4% |
| `manual_registration` | 38.2% |

Manually procured travel entries are declined most often, possibly because they lack the structured metadata that automated entries generate.

### 4. Asset Class — Vehicle and Travel Items Rejected Most

| `asset_class` | Decline Rate (travel) |
|---|---|
| `vehicle` | **55.6%** |
| `travel_item` | 43.0% |
| `laptop` | 35.3% |
| `peripheral` | 33.3% |

Vehicle-class travel expenses face the highest scrutiny. This may reflect policy limits or approval thresholds for vehicle-related travel costs.

### 5. Department — IT and HR Most Affected

| `department` | Decline Rate (travel) |
|---|---|
| IT | **54.5%** |
| HR | **50.0%** |
| Customer Support | 44.3% |
| Sales | 40.9% |
| Finance | 25.0% |
| Development | 0% |
| Product Management | 0% |

Development and Product Management show zero declined travel expenses, but both have very small sample sizes — weak evidence. Finance's lower rate may reflect tighter pre-submission controls.

### 6. Amount — Weak or No Effect

Declined travel expenses have a **lower** average amount (≈$3,793) than non-declined travel expenses (≈$4,444). This counter-intuitive direction suggests amount alone is not a driver of decline; higher-value claims are not disproportionately rejected.

---

## Notable Structural Finding

All travel-related rows in this dataset have **`has_source_id = False`** (no source ID attached), meaning this field cannot differentiate declined from approved within the travel segment — though it may explain why travel expenses as a whole face elevated scrutiny compared to non-travel records (which have mixed source ID presence and a 6.5% decline rate).

---

## Summary of Contributing Factors

| Factor | Strength | Direction |
|---|---|---|
| `processing_lag_band = not_processed` | **Very Strong** | Unprocessed → Declined |
| `ci_specificity` (generic/vague) | **Strong** | Vague description → Higher decline |
| `entry_method = manual_procurement` | **Moderate** | Manual → Higher decline |
| `asset_class = vehicle` | **Moderate** | Vehicle expenses → Higher decline |
| Department (IT, HR) | **Moderate** | Certain depts → Higher decline |
| `amount` | **Weak/None** | No clear positive relationship |
