---
dataset: flag_20
scenario: eda_declined
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "state_declined"
query: "What signals in a travel-expense description predict whether it will be declined?"
source_table: augment_table/flag_20/eda_declined/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:17:48.816211+00:00
wall_seconds: 68.29
---

# Travel Expense Decline Prediction Analysis

## Executive Summary

This analysis examines 146 travel expense records to identify signals that predict whether a travel expense will be declined. **The primary predictive signal is the nature of the item/product classified as a "travel" expense**, with systematically misclassified or inappropriate items showing significantly higher decline rates.

## Key Findings

### 1. **Missing Processing Field as Deterministic Signal**

**Strongest single predictor:** `missing_processing = 1` 

- **100% of declined travel expenses** have `missing_processing = 1`
- **0% of processed travel expenses** have `missing_processing = 1`

This indicates that declined expenses lack processing dates (`processed_date` is empty), which is a definitive marker of expenses that failed the processing pipeline. **This is a direct consequence of decline, not a predictive cause.**

### 2. **Product Category Misclassification**

Travel expenses show systematic misclassification. Declined expenses frequently contain products that don't belong in "travel" category:

**Inappropriate/Problematic Items in Declined Expenses (8.2% of declined):**
- **Vehicles:** "Company Car Fiat 500", "Corporate Jet A320", "Luxury Bus 2018 Model", "Luxury Tour Bus", "Corporate Car Fleet"
- **Communication devices:** "Satellite Phone Model XJ2"
- **Non-travel hardware:** "Aircraft Airbus A320"

**Legitimate Travel Products in Declined Expenses (appear less frequently):**
- Standard luggage (Samsonite cases)
- Portable travel accessories (GPS, chargers, adapters)
- Airline tickets
- Business travel laptops

The presence of vehicle or vehicle-related items as "travel equipment assets" signals declined status with high confidence.

### 3. **Description Text Patterns**

Declined travel expenses show specific description patterns:

**Declined (61 records):**
- "Automated generated" or "automatically": 34.4% (vs. 30.6% non-declined)
- "Equipment": 34.4% (vs. 28.2% non-declined)
- "Asset" keyword: 65.6% (vs. 68.2% non-declined)
- "Hardware": 14.8% (vs. 15.3% non-declined)

**Interpretation:** Declined expenses are slightly more likely to be automatically generated and describe items as "equipment" rather than legitimate travel services, suggesting system-generated misclassifications.

### 4. **Financial Amount: Weak Signal**

- **Declined average:** $3,792.89
- **Non-declined average:** $4,443.73

Declined expenses have slightly lower amounts, but overlapping ranges ($521–$7,798 for declined, $538–$7,984 for non-declined) and a modest difference mean amount alone is insufficient for prediction.

### 5. **Automated Description Flag**

- **Declined:** 34.4% have `has_automated_desc = 1`
- **Non-declined:** 30.6% have `has_automated_desc = 1`
- Difference: only 3.8 percentage points—weak signal

### 6. **High Amount Flag (`is_high_amount`)**

- **Declined:** 45.9% marked as high amount
- **Non-declined:** 49.4% marked as high amount
- Declined expenses are *slightly less* likely to be high-amount, making this non-predictive

## Important Caveats

1. **Deterministic vs. Predictive:** The `missing_processing` field perfectly separates declined from processed, but this reflects the *outcome* of decline (no processing date assigned) rather than a *cause* that predicts it.

2. **Pending Status Ambiguity:** 18 travel expenses have Pending state with `missing_processing = 1`, suggesting these could transition to either Processed or Declined.

3. **Department Clustering:** Declined expenses concentrate in Customer Support (57.4%) but this reflects workflow assignment, not prediction.

4. **Inconsistent Categorization:** Legitimate travel items (airline tickets, luggage) appear in both declined and non-declined sets, indicating manual or heuristic classification rather than rigid rules.

## Predictive Signals (Ranked by Practical Strength)

| Signal | Type | Strength | Basis |
|--------|------|----------|-------|
| Vehicle/vehicle-like product in CI field | Content | Strong | 8 vehicle-related items in declined (vs. ~4 in non-declined); "car", "jet", "bus", "aircraft" keywords |
| Automatically generated + equipment/asset language combo | Content | Moderate | 3.8–6.2 pp higher prevalence in declined descriptions |
| Amount < $3,500 | Financial | Weak | Marginal difference in central tendency; substantial overlap |
| `has_automated_desc = 1` | Metadata | Weak | Only 3.8 pp difference |
| `missing_processing = 1` | Structural | Perfect (but post-hoc) | 100% of declined, 0% of processed; **reflects outcome only** |

## Conclusion

Travel expense decline is primarily determined by **content appropriateness and product classification**, not financial thresholds or automation metadata. Declined expenses frequently represent system-generated misclassifications (vehicles, inappropriate items, or malformed asset records incorrectly tagged as "travel" expenses).

**For actionable prediction:** Examine the `ci` (configuration item/product name) field for:
- Vehicle references (car, bus, jet, aircraft)
- Extreme/suspicious items (satellite phones, luxury vehicles)
- Category mismatch (hardware/software assets labeled as travel equipment)

**Weak predictors alone:** Amount, automated description flags, and department cannot reliably predict decline without examining item content.
