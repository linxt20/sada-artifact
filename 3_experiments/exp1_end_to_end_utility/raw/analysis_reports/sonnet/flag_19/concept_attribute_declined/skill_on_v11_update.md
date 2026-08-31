---
dataset: flag_19
scenario: concept_attribute_declined
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "declined_expense_reasons"
query: "What reasons or compliance risks appear in declined expenses?"
source_table: augment_table/flag_19/concept_attribute_declined/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:15:45.296598+00:00
wall_seconds: 65.88
---

# Declined Expenses: Reasons and Compliance Risks

**Dataset:** `sonnet__skill_on_v11_update.csv` | **Declined records:** 46 of 500 (9.2%)

---

## 1. Universal Signal: Missing `processed_date`

Every single declined expense (46/46) has a blank `processed_date`, compared to 167/500 (33%) across the full dataset. While many non-declined records also lack a processed date (they are Pending/Submitted), **no declined expense ever received a completion timestamp**. This is the strongest structural marker of decline and reflects that the workflow was terminated before processing concluded.

---

## 2. Category Distribution of Declined Expenses

| Category | Count | % of Declined |
|---|---|---|
| Assets | 27 | 59% |
| Travel | 10 | 22% |
| Services | 6 | 13% |
| Miscellaneous | 3 | 7% |

Assets dominate declined records, consistent with their prevalence overall, but Travel is slightly over-represented as a risk category given the flags noted below.

---

## 3. Compliance Risk Factors

### 3a. Missing Source ID (`source_id_present = False`)
- **14 of 46 declined records (30%)** lack a source ID, vs. 22% in the overall dataset.
- Missing source IDs indicate the expense cannot be traced back to a purchase order, ticket, or upstream system record — a common rejection reason in audit-driven workflows.
- All 14 missing-source-ID declined records also lack a `processed_date`, compounding traceability gaps.

### 3b. Poor CI Name Quality
- **24 of 46 declined records (52%)** have `ci_name_quality` of `generic_label` (14) or `asset_code_only` (10).
- Only 22 records (48%) have `specific_model_name`.
- Vague or code-only CI labels reduce verifiability of the asset being expensed and are a likely trigger for manual review and rejection.

### 3c. Travel-Category Hardware Mismatches (`is_travel_category_hardware_mismatch = True`)
- **2 of 46 declined records** flag a mismatch between a Travel expense category and a hardware subtype (e.g., a laptop or GPS peripheral filed under "Travel").
- Examples: EXP00000288 ("Travel Department Laptop" — Dell Latitude 7490 filed as Travel, HR dept.) and EXP00000443 (GPS peripheral under Travel, Customer Support).
- Both also lack a source ID, suggesting compounding risk factors.

### 3d. Premium/Luxury Items (`is_premium_or_luxury_item = True`)
- **1 of 46 declined records** involves a luxury item: EXP00000240, a "Business Class Airline Ticket" auto-generated under Travel, Customer Support, with no source ID and a generic CI label.
- This is weak evidence given the single instance, but aligns with expected policy enforcement against luxury spend.

### 3e. Auto-Generated Entries
- **18 of 46 declined records (39%)** were `auto_generated`, similar to the overall rate (~36%). Auto-generation alone does not appear to be a strong independent predictor of decline.

---

## 4. Departmental Pattern

| Department | Declined Count |
|---|---|
| IT | 19 (41%) |
| Customer Support | 16 (35%) |
| Sales | 6 (13%) |
| HR | 2 |
| Finance | 2 |
| Development | 1 |

IT and Customer Support account for 76% of declined expenses, suggesting either higher volume submission or stricter review processes in those departments.

---

## 5. Summary of Key Compliance Risks

| Risk Factor | Declined Records Affected | Notes |
|---|---|---|
| Missing `processed_date` | 46/46 (100%) | Universal; definitional to declined state |
| Poor CI name quality (generic/code-only) | 24/46 (52%) | Reduces asset verifiability |
| Missing source ID | 14/46 (30%) | Breaks audit traceability |
| Travel/hardware category mismatch | 2/46 (4%) | All also missing source ID |
| Premium/luxury item | 1/46 (2%) | Weak evidence; single case |

**Most actionable finding:** Declined expenses disproportionately combine missing source IDs with generic or code-only CI labels, suggesting that incomplete or non-specific expense documentation is the primary driver of rejection. The travel-hardware mismatch and luxury item flags are real but minor signals given their low counts.
