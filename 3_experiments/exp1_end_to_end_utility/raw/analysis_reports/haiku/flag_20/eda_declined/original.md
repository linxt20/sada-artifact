---
dataset: flag_20
scenario: eda_declined
variant: original
model: substrate-claude-haiku-4-5
query_subtype: exploratory_data_analysis
focus_variable: "state_declined"
query: "What signals in a travel-expense description predict whether it will be declined?"
source_table: augment_table/flag_20/eda_declined/original.csv
generated_at: 2026-07-26T13:31:56.888514+00:00
wall_seconds: 138.56
---

# Travel Expense Decline Prediction Analysis

## Executive Summary

This analysis examines 146 travel expenses to identify signals predicting whether a travel-expense description will be declined. The dataset reveals a **41.8% decline rate** for travel expenses, with several clear predictive signals based on description content and processing metadata.

## Key Findings

### 1. **Critical Signal: Missing Processing Date (Highest Predictor)**

The most distinctive signal is the **absence of a `processed_date` field**:

- **100% of Processed expenses** have a `processed_date` populated
- **0% of Declined expenses** have a `processed_date` populated (0/61)

**Interpretation**: The `processed_date` field is systematically populated only after an expense is approved, making its absence a definitive indicator of decline. This is not a description-based signal but a critical metadata indicator.

### 2. **Description Language: Specificity vs. Generic System Language**

Travel expense descriptions exhibit a notable pattern in decline likelihood based on their specificity:

**Specific Travel Item Language** (mentions of flights, luggage, laptops, devices, etc.):
- **Declined descriptions**: 4.9% (3/61)
- **Accepted descriptions**: 17.3% (9/52)

**Interpretation**: Descriptions that mention concrete travel items (e.g., "luggage tracking device," "office laptop purchased for business travel") are **more likely to be accepted**, while generic asset-focused descriptions tend toward decline.

**Generic System Language** ("automatically generated," "for creation"):
- **Declined descriptions**: 27.9% (17/61)
- **Accepted descriptions**: 25.0% (13/52)

This shows marginal difference, suggesting generic language alone is not strongly predictive.

### 3. **Asset-Centric Framing**

Both declined and accepted descriptions frequently use asset-focused language:
- **Declined**: 65.6% mention "asset"
- **Accepted**: 67.3% mention "asset"

**Interpretation**: Asset framing is ubiquitous and not a strong differentiator. However, descriptions emphasizing travel items (specific equipment) rather than generic assets show better acceptance.

### 4. **Department-Level Risk**

Decline rates vary meaningfully by department:

| Department | Declined | Total | Decline Rate |
|---|---|---|---|
| IT | 6 | 11 | 54.5% |
| HR | 1 | 2 | 50.0% |
| Customer Support | 35 | 79 | 44.3% |
| Sales | 18 | 44 | 40.9% |
| Finance | 1 | 4 | 25.0% |
| Development | 0 | 5 | 0.0% |

**Interpretation**: IT department expenses show the highest decline risk (54.5%), while Development has no declines. Customer Support, which generates the majority of travel expenses (79/146), maintains a moderate 44.3% decline rate.

### 5. **Amount Analysis: Weak Predictor**

Amount distributions are remarkably similar between declined and accepted expenses:

- **Declined mean**: $3,793 (median: $3,699)
- **Accepted mean**: $3,928 (median: $3,618)
- **Range**: Both span from ~$500 to ~$7,800

**Interpretation**: Expense amount is **not a strong predictor** of decline. The distributions nearly overlap, suggesting decline decisions are driven by other factors (description quality, legitimacy, department) rather than cost thresholds.

### 6. **Identical Descriptions with Mixed Outcomes**

Seven descriptions appear in both declined and accepted datasets, with varying outcomes:

- "Automatically generated expense line for creation of travel asset": **5 declined, 6 accepted**
- "Travel-related hardware asset": **1 declined, 2 accepted**

**Interpretation**: Description text alone does not deterministically predict outcome. This suggests approval decisions depend on context beyond the description itself (date submitted, reviewer, department policy, or sequential processing rules).

## Weak or Absent Signals

- **No significant seasonal pattern** in opened_at dates
- **Source ID**: Uniformly absent for all travel expenses (cannot be used for prediction)
- **User name**: No discernible pattern by submitter
- **High vs. low amounts**: Similar distribution across states (both ~30% below Q1, ~20% above Q3)

## Decision-Ready Insights

**Primary Predictive Indicators (in order of strength):**

1. **Metadata presence** (processed_date = declined indicator) — definitive but post-hoc
2. **Description specificity** — mentions of concrete travel items increase acceptance likelihood
3. **Department** — IT shows elevated decline risk; Development shows zero declines
4. **Generic system language** — marginal predictor; weak evidence of slight decline association

**Actionable patterns for description improvement:**
- Replace generic "asset" and "for creation" language with specific travel item references
- Consider department-specific review policies, particularly for IT and HR
- Amount-based approval thresholds are **not evident** in the data

## Limitations

- Description patterns show only modest predictive strength; identical descriptions receive different outcomes
- The `processed_date` field represents post-decision metadata, not a pre-decision signal
- The dataset is imbalanced toward declined expenses (41.8% vs. expected operational norms)
- Cannot determine if decline is due to expense legitimacy, policy violation, or system error
