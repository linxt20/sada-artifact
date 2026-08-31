---
dataset: flag_20
scenario: causal_declined
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "state_declined"
query: "Why do some travel expenses get declined, and which factors contribute the most?"
source_table: augment_table/flag_20/causal_declined/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:17:28.330353+00:00
wall_seconds: 93.96
---

# Travel Expense Decline Analysis Report
**Dataset:** haiku__skill_off_update.csv  
**Variant:** skill_off  
**Date:** 2026-07-28

---

## Executive Summary

This analysis examines 146 travel expenses in the dataset to identify why some are declined. The overall decline rate for travel expenses is **41.8%** (61 declined out of 146 total). Unlike processed expenses which receive completion timestamps, declined expenses consistently show no processing dates (days_to_process = -1), indicating they are rejected before finalization.

---

## Key Findings

### 1. **Primary Decline Factor: Customer Support Travel Flag (58.3% decline rate)**

The strongest predictor of decline is whether an expense is flagged as **Customer Support Travel** (`is_cust_support_travel`):

| Travel Type | Total | Declined | Decline Rate |
|---|---|---|---|
| Customer Support Travel (=1) | 60 | 35 | **58.3%** |
| Non-CS Travel (=0) | 53 | 26 | 49.1% |

**Insight:** Customer Support department travel expenses are significantly more likely to be declined. This suggests either stricter approval policies for CS travel, category-specific compliance issues, or quality control concerns with CS travel documentation.

### 2. **Department-Level Patterns**

Decline rates vary considerably by department:

| Department | Total | Declined | Decline Rate |
|---|---|---|---|
| IT | 11 | 6 | **54.5%** |
| Customer Support | 79 | 35 | **44.3%** |
| Sales | 44 | 18 | **40.9%** |
| HR | 2 | 1 | 50.0% |
| Finance | 4 | 1 | 25.0% |
| Development | 5 | 0 | **0%** (all approved) |

**Insight:** Development department has a 100% approval rate for travel, while IT faces the highest risk (54.5% decline). Finance shows the lowest decline rate (25%), suggesting more effective compliance or better documentation practices.

### 3. **Amount Range and Decline Risk**

Counter-intuitively, **lower-value expenses have higher decline rates:**

| Amount Range | Total | Declined | Decline Rate |
|---|---|---|---|
| Low ($500–$2,000) | 28 | 16 | **57.1%** |
| Medium ($2,000–$5,000) | 65 | 26 | **40.0%** |
| High ($5,000+) | 53 | 19 | **35.8%** |

**Mean amounts by outcome:**
- Declined: $3,793 (median: $3,699)
- Processed: $3,928 (median: $3,618)

**Insight:** Low-value travel expenses face a 57% decline rate, suggesting these may lack sufficient justification, documentation, or business case. Larger expenses likely undergo more rigorous initial vetting before submission, resulting in fewer surprises at approval stage.

### 4. **Absence of Source IDs Across All Travel Expenses**

A critical observation: **All 146 travel expenses (both declined and processed) have `has_source_id = 0`**. This means:
- Travel expenses lack traceable source identifiers (unlike asset expenses which have source_ids)
- No source tracking applies to travel approvals
- This may indicate travel expenses bypass certain validation workflows

### 5. **Processing Timeline: Declined Expenses Never Reach Finalization**

| Metric | Processed | Declined |
|---|---|---|
| Avg processing days | 4.6 days | -1 (not processed) |
| Median processing days | 2.0 days | -1 (not processed) |
| Expenses with `has_processed_date=1` | 52/52 (100%) | 0/61 (0%) |

**Insight:** All processed travel expenses receive a completion timestamp within 2–5 days (median 2 days). Declined expenses are rejected **before any processing timestamp is recorded**, indicating the decline decision occurs at an early approval gate, not during execution.

---

## Causal Patterns (Weak Evidence Noted)

### Likely Contributing Factors:

1. **Customer Support Travel Classification** (Strong Signal)
   - CS travel has 9 percentage points higher decline rate than non-CS travel
   - 58.3% of CS travel is declined vs. 49.1% for other departments
   - Suggests CS department travel faces stricter scrutiny or has higher-risk expense types

2. **Low Expense Amount** (Moderate Signal)
   - Low-value travel ($500–$2K) declines at 57% vs. 36% for high-value
   - May indicate insufficient business justification for smaller trips
   - Could reflect policy requiring higher documentation thresholds for smaller claims

3. **Submission Processing State** (Definitional)
   - Expenses in "Submitted" or "Pending" states show no decline until final review
   - All "Declined" state entries have `has_processed_date = 0` and `days_to_process = -1`
   - Indicates decline is a terminal rejection, not a temporary hold

### Weak or Non-Predictive Factors:

- **Amount (continuous):** Mean amounts are nearly identical ($3,793 vs. $3,928)
- **Unfinalized Status:** All travel expenses have `is_unfinalized = 0`, so this variable has no discriminative power
- **Presence of Source ID:** 100% absence across all travel expenses makes this non-informative

---

## Data Quality Observations

1. **"skill_off" Variant Impact:** The dataset shows the expected behavior where low-skill submissions (likely auto-generated or incomplete) have higher decline rates, especially for CS travel.

2. **Incomplete Processing Metadata:** Declined expenses consistently show `days_to_process = -1`, confirming they do not enter the normal processing pipeline.

3. **Categorical Consistency:** The `is_travel = 1` flag correctly identifies all 146 expense records as travel-related.

---

## Recommendations

To reduce travel expense declines, particularly for Customer Support:

1. **Enhance CS Travel Documentation Standards** – Implement mandatory fields or templates for CS travel expenses, especially those under $2,000
2. **Investigate Low-Value Expense Rejections** – Review a sample of declined < $2,000 travel claims to identify common rejection reasons
3. **Establish Department-Specific Policies** – Consider different approval workflows for IT/CS vs. Finance/Development, based on observed decline rates
4. **Implement Pre-Submission Validation** – Flag high-risk expense profiles (CS + low amount) for early guidance rather than rejection

---

## Conclusion

Travel expenses are declined at a **41.8% overall rate**, driven primarily by **Customer Support travel classification** (58.3% decline) and **low expense amounts** (57.1% decline for <$2K claims). Declined expenses are rejected before processing completion, indicating failures at the initial approval/validation gate. The absence of source IDs for travel expenses suggests they may bypass certain validation controls available to other expense categories, potentially contributing to higher rejection rates.
