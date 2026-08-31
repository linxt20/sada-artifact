---
dataset: flag_20
scenario: predictive_declined
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "state_declined"
query: "What signals suggest a travel expense will be declined?"
source_table: augment_table/flag_20/predictive_declined/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:18:01.753465+00:00
wall_seconds: 36.36
---

# Analysis: Signals of Travel Expense Decline

## Overview
This analysis identifies key patterns distinguishing declined travel expenses from approved ones. The dataset contains 146 travel expenses, of which 61 (41.8%) were declined, 52 (35.6%) were processed, and 33 (22.6%) remain pending or submitted.

## Primary Decline Signals

### 1. **Absence of Processed Date (Critical Indicator)**
The strongest signal for decline is the **lack of a processed date**. All 61 declined travel expenses have `has_processed_date = 0` and empty `processed_date` fields. This suggests that declined expenses are rejected before processing can be completed, indicating failure at an early approval gate.

### 2. **Department Source**
Declined travel expenses concentrate in specific departments:
- **Customer Support**: 35 declined (44.3% of all Customer Support travel)
- **Sales**: 18 declined (40.9% of all Sales travel)
- **IT**: 6 declined (54.5% of all IT travel, highest decline rate)

Development and Product Management show no declines (0%), suggesting stronger oversight or different expense patterns in those teams.

### 3. **Smaller Average Amounts**
Declined travel expenses average **$3,792.89** (median: $3,699), compared to $4,443.73 for non-declined travel. This $650 difference suggests lower-value or peripheral travel requests are more likely to be rejected.

### 4. **Automatic Entry / Generic Descriptions**
Declined expenses predominantly feature standardized, auto-generated descriptions:
- "Automatically generated expense line for creation of travel equipment"
- "Travel equipment asset"
- "Travel-related hardware configuration asset"
- Generic equipment references (travel kits, luggage, adapters)

In contrast, processed travel often includes specific trip context or employee information, suggesting that vague or system-generated entries are flagged for decline.

### 5. **Customer Support Travel Designation**
Of 61 declined expenses, 35 (57.4%) are marked as `is_customer_support_travel = 1`, while only 18 (29.5%) are marked as `is_sales_travel = 1`. Customer Support travel has the highest absolute decline count, despite representing only 54% of all travel expenses.

## Secondary Patterns

- **No correlation with amount alone**: While declined amounts average lower, the range overlaps significantly ($521–$7,798 vs. $538–$7,648), so amount alone is not determinative.
- **Independent of expense ID**: All travel expenses show `source_id` is consistently blank, so this is not a differentiating factor.

## Conclusions

Travel expenses are most likely to be declined when they exhibit multiple signals:
1. **No completed processing date** (100% of declined cases)
2. **Auto-generated or vague descriptions** (majority pattern)
3. **Customer Support department origin** (higher decline rate)
4. **Below-average amount** (supporting but not definitive)
5. **Lack of specific travel context** (trip details, employee, business purpose)

The skill-off variant suggests these patterns hold when decision-making lacks specialized travel approval knowledge, relying instead on systemic flags and structural indicators.
