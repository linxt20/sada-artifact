---
dataset: flag_20
scenario: eda_declined
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "state_declined"
query: "What signals in a travel-expense description predict whether it will be declined?"
source_table: augment_table/flag_20/eda_declined/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:18:09.439901+00:00
wall_seconds: 83.71
---

# Travel Expense Decline Prediction: Signals Analysis

## Dataset Context
- **Total travel expenses analyzed**: 146 records
- **Declined**: 61 (41.8%)
- **Processed**: 52 (35.6%)
- **Other states** (Pending/Submitted): 33 (22.6%)

## Key Signal: Payment Processing Status

### Critical Finding
**The strongest predictor of decline is the absence of a processed date.**

- **100% of declined expenses** lack a `processed_date` field
- **100% of processed expenses** have a `processed_date` field
- **This creates a perfect separation** between declined and processed outcomes

**Interpretation**: Declined expenses are never actually processed through the payment system. This reflects their rejection during approval workflows, preventing payment authorization.

---

## Secondary Signals: Description Characteristics

### 1. Travel Equipment Category Misclassification
- **53 of 61 declined (86.9%)** are labeled as `asset_category_type = travel_equipment`
- **Contrast**: Among processed, only 39 of 52 (75%) are labeled `travel_equipment`
- **Hardware devices** in travel category have better approval rates (44.8% processed vs. 27.6% declined)

**Signal**: Pure "travel_equipment" items have a higher decline rate than mixed equipment categories.

### 2. Automated vs. Manual Description Patterns
- **Automated-sounding descriptions** ("automatically generated," "generated") appear in 21 of 61 declined (34.4%)
- **Decline rate for automated descriptions**: 56.8%
- **Decline rate for manual descriptions**: 52.6%

**Signal**: Marginally higher decline rate for system-generated vs. human-authored descriptions, but both show substantial decline rates (~53-57%).

### 3. High-Value Expenses
- **31.1% of declined** travel expenses exceed $5,000
- **30.8% of processed** travel expenses exceed $5,000
- **Mean declined amount**: $3,793; **Mean processed**: $3,928

**Finding**: No meaningful amount-based signal; distributions are nearly identical.

---

## Weak or Ambiguous Signals

### Department Context
- **Customer Support** dominates both outcomes (35 declined, 25 processed)
- **Sales** shows near parity (18 declined, 17 processed)
- **No clear departmental pattern** of decline/approval differentiation

### Source System
- **Expense system**: 34 declined, 32 processed (nearly balanced)
- **Internal ticket system**: 26 declined, 16 processed (slightly higher decline)
- **No strong source system signal** for prediction

### Specific Item Types
- **Luggage items**: Appear only in processed expenses (3 instances, 100% approved)
- **Flight/airline items**: Minimal and mixed
- **Vehicle-related items**: Rare; appear in both outcomes (e.g., "Company Car Model X" declined at $5,550)

**Finding**: Most item types have insufficient frequency for reliable pattern detection.

---

## Summary Table: Signal Strength

| Signal | Strength | Evidence |
|--------|----------|----------|
| **Missing processed_date** | Perfect (definitional) | 100% separation |
| **Travel_equipment category** | Weak | 86.9% vs. 75%; marginal differentiation |
| **Automated description** | Weak | 56.8% vs. 52.6% decline rate |
| **High amount (>$5k)** | None | 31.1% vs. 30.8% |
| **Department** | None | No significant variation |
| **Source system** | Weak | Minimal differentiation |

---

## Important Limitations

1. **Reverse causality**: The processed_date is post-decision and definitional. Declined expenses lack it by design, not as a predictive feature. This separates outcomes but cannot predict decline before approval.

2. **Description patterns are weak**: Automated vs. manual descriptions show only ~4 percentage point difference in decline rates (52.6% vs. 56.8%). This does not constitute actionable predictive power.

3. **Missing upstream signals**: The dataset lacks:
   - Approval status/timestamps prior to processing
   - Policy violation flags
   - User authority levels
   - Budget utilization data
   - Explicit decline reasons

4. **Small item-level samples**: Luggage (3 items), flights, vehicles each represent <3% of travel expenses, limiting generalizability.

---

## Conclusion

**The processed_date field perfectly separates outcomes but is not predictive**—it reflects the definitional outcome rather than signals preceding the decline decision.

**Available descriptive features show weak predictive power**: Travel equipment categorization, description automation, department, and amount all show <10 percentage point differences between declined and processed cohorts.

**For actionable decline prediction**, signals that precede the approval decision are needed: policy compliance status, manager pre-approval scores, budget constraints, cost center validation, and explicit approval workflows—none of which appear in this dataset.
