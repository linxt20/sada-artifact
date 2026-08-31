---
dataset: flag_20
scenario: predictive_declined
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "state_declined"
query: "What signals suggest a travel expense will be declined?"
source_table: augment_table/flag_20/predictive_declined/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:17:46.248130+00:00
wall_seconds: 47.11
---

# Travel Expense Decline Prediction Analysis
**Dataset:** haiku__skill_on_v11_update.csv  
**Variant:** skill_on  
**Date:** 2026-07-30

## Executive Summary

This analysis identifies strong predictive signals that distinguish declined travel expenses from processed ones. A single dominant pattern emerges: **missing or unresolved processing status** is the critical signal for decline. The dataset shows 100% of declined travel expenses lack processing lag information and have no recorded processing completion date.

## Dataset Overview

- **Total Travel Expenses:** 146
  - Declined: 61 (41.8%)
  - Processed: 52 (35.6%)
  - Pending: 18 (12.3%)
  - Submitted: 15 (10.3%)

## Key Signals of Decline

### 1. **Processing Lag Signal = "Unknown" (100% of declined cases)**

This is the **strongest predictor** of decline:

| State | Unknown | Delayed/Same-day | Long Delay |
|-------|---------|------------------|-----------|
| **Declined** | 61 (100.0%) | 0 (0.0%) | 0 (0.0%) |
| **Processed** | 0 (0.0%) | 51 (98.1%) | 1 (1.9%) |
| **Pending** | 18 (100.0%) | 0 (0.0%) | 0 (0.0%) |

**Interpretation:** Expenses flagged with "Unknown" processing lag invariably fail to reach "Processed" status. Processed expenses exclusively show concrete processing timelines (delayed_processing or same_day_processing). This suggests that declined expenses fail before processing lag data is captured.

### 2. **Missing Processed Date (100% of declined cases)**

All 61 declined travel expenses lack a `processed_date` entry, while all 52 processed expenses have a recorded date.

**Interpretation:** The absence of a completion timestamp is definitive—declined expenses never reach the processing completion stage. This reflects the workflow: expenses cannot be marked "Processed" without a processing date recorded.

### 3. **No Source ID (100% pattern, minimal differentiation)**

All travel expenses (both declined and processed) lack a `source_id`, making this non-discriminative for decline prediction.

### 4. **Automation Mode: Marginal Difference**

- Declined: 63.9% automated_generated, 36.1% manual_procurement
- Processed: 78.8% automated_generated, 21.2% manual_procurement

**Interpretation:** While manual procurement is slightly overrepresented in declined cases (36.1% vs 21.2%), this is a weak signal. Both automation modes produce both outcomes.

### 5. **Asset Class Composition (Travel Equipment Dominant)**

Declined travel expenses break down as:
- travel_equipment: 37 (60.7%)
- hardware_computing: 12 (19.7%)
- vehicle: 7 (11.5%)
- services: 4 (6.6%)
- miscellaneous: 1 (1.6%)

**Note:** Declined travel expenses skew slightly toward tangible travel_equipment (60.7%) vs processed (71.2%), but both are travel-focused, limiting predictive value.

### 6. **CI Specificity (Weak Signal)**

- Declined: 55.7% generic_category, 37.7% specific_model_identifier, 6.6% service_descriptor
- Processed: 59.6% generic_category, 38.5% specific_model_identifier, 1.9% service_descriptor

**Interpretation:** Generic descriptors (e.g., "Travel Equipment," "Business Travel Kit") are present in both groups at similar rates. This is not a strong predictor.

## Financial Metrics (Non-Discriminative)

Amount does not differentiate decline:
- **Declined:** Mean $3,793, Median $3,699 (range: $521–$7,798)
- **Processed:** Mean $3,928, Median $3,619 (range: $538–$7,648)

## Important Exceptions & Limitations

1. **Pending and Submitted Status:** Travel expenses in "Pending" or "Submitted" states also show `processing_lag_signal = "Unknown"` and missing processed_date. These may be candidates for future decline or eventual processing; they are unresolved, not yet finalized.

2. **Marginal Differences:** Except for processing completion signals, most feature differences between declined and processed are modest (±15–20 percentage points). Decline prediction benefits most from **processing workflow signals** rather than asset characteristics alone.

3. **No Strong Department or User Signal:** Customer Support departments dominate both declined (57.4%) and processed (65.4%) travel expenses; no department is protective.

## Conclusion

**The primary signal of travel expense decline is the absence of processing completion evidence:**

- Declined expenses are consistently marked with `processing_lag_signal = "Unknown"` and lack a `processed_date`
- Processed expenses always have concrete processing lag signals and recorded completion dates
- This pattern suggests declined expenses fail at the processing stage before workflow data is finalized

**Secondary, weak signals** include slight overrepresentation of manual procurement and travel-equipment class among declined expenses, but these are insufficient alone for robust prediction.

**Recommendation:** Predict decline based on absence of processing lag data and missing processed_date; investigate the workflow logic that prevents these signals from being captured for declined expenses to enable early intervention.
