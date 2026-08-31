---
dataset: flag_19
scenario: causal_reduce
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: what_if
focus_variable: "state_declined"
query: "How can we reduce declined expense submissions?"
source_table: augment_table/flag_19/causal_reduce/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:16:57.764400+00:00
wall_seconds: 149.0
---

# Analysis: Reducing Declined Expense Submissions

## Executive Summary

This analysis examines 500 expense submission records to identify drivers of decline and recommend interventions. **Overall decline rate: 9.2% (46 of 500 submissions)**. The primary finding is that **IT department submissions exhibit a dramatically elevated decline rate of 44.2%**—nearly 5× the baseline. Secondary risk factors include custom CI identifiers (15.9% decline rate), travel-related expenses (10.6%), and vague asset descriptions.

By targeting IT department process improvements, custom identifier standardization, and travel policy clarity, organizations can eliminate approximately **15–17 declined submissions** while improving governance.

---

## Key Findings

### 1. IT Department: Critical Decline Risk (44.2% decline rate)

The IT department is the primary driver of declined submissions:

| Department | Declined | Total | Decline Rate |
|---|---|---|---|
| **IT** | **19** | **43** | **44.2%** |
| HR | 2 | 14 | 14.3% |
| Finance | 2 | 22 | 9.1% |
| Customer Support | 16 | 267 | 6.0% |
| Development | 1 | 20 | 5.0% |
| Sales | 6 | 122 | 4.9% |
| Product Management | 0 | 12 | 0.0% |
| **Overall** | **46** | **500** | **9.2%** |

**Insight**: IT represents only 8.6% of submissions but accounts for 41% (19/46) of all declines. Reducing IT decline rate from 44.2% to the baseline of 9.2% would eliminate approximately **16 declined submissions**.

### 2. Submission Pattern + Department Interaction

The augmented column `submission_pattern` reveals that IT declines occur across both automated and manual submission modes:

| Department | Pattern | Declined | Total | Rate |
|---|---|---|---|---|
| **IT** | **user_initiated** | **6** | **10** | **60.0%** |
| **IT** | **automatically_generated** | **10** | **23** | **43.5%** |
| **IT** | **travel_related** | **3** | **10** | **30.0%** |
| Finance | user_initiated | 1 | 5 | 20.0% |
| HR | automatically_generated | 1 | 7 | 14.3% |
| Customer Support | travel_related | 6 | 53 | 11.3% |
| Sales (user_initiated) | — | 4 | 44 | 9.1% |

**Insight**: IT user-initiated submissions show the highest risk (60% decline rate, n=10), followed by automatically-generated IT submissions (43.5%, n=23). This suggests both processes—whether human-driven or system-generated—have quality or compliance issues within IT's workflow.

### 3. CI Identifier Quality: Strong Compliance Signal

The augmented column `ci_identifier_quality` reveals that custom identifiers significantly elevate decline risk:

| CI Quality | Declined | Total | Decline Rate |
|---|---|---|---|
| **custom_identifier** | **10** | **63** | **15.9%** |
| descriptive_only | 12 | 124 | 9.7% |
| standard_model_number | 23 | 286 | 8.0% |
| generic_placeholder | 1 | 27 | 3.7% |

**Insight**: Submissions with custom CI identifiers (e.g., "Desktop_30123_Dell", "Asset-DELL7490SN123456", "CPU_i7_E5470_Serial12345") have a 15.9% decline rate versus 8.0% for standard model numbers. The IT department is disproportionately affected: 5 of 10 declined IT user-initiated submissions used custom identifiers. Standardizing to industry-recognized model numbers could reduce declines by ~5 submissions.

### 4. Travel Expenses: Elevated but Secondary Risk

The augmented column `travel_expense_flag` identifies travel-related submissions:

| Travel Flag | Declined | Total | Decline Rate |
|---|---|---|---|
| **True** | **10** | **94** | **10.6%** |
| False | 36 | 406 | 8.9% |

**Insight**: Travel expenses decline at 10.6% versus 8.9% for non-travel. Asset type further stratifies this: travel equipment (e.g., GPS receivers, luggage, portable chargers) decline at 15.5% (9/58), the highest rate among equipment categories, while non-travel hardware devices decline at 8.7% (30/346).

### 5. Description Specificity: Vague Descriptions Increase Risk

The augmented column `expense_description_specificity` shows that vague or generic descriptions correlate with declines:

| Description Specificity | Declined | Total | Decline Rate |
|---|---|---|---|
| **asset_class_implied** | **7** | **53** | **13.2%** |
| generic_category_only | 1 | 8 | 12.5% |
| product_model_named | 32 | 360 | 8.9% |
| service_type_specified | 6 | 79 | 7.6% |

**Insight**: Submissions with only implied asset classes (e.g., "Miscellaneous hardware asset issued" without naming the asset) decline at 13.2%. Contrast: explicit product model names (8.9% decline) and service types (7.6%) show lower risk. Encouraging detailed descriptions—especially for travel and miscellaneous items—could reduce declines.

### 6. Category and Asset Type

Miscellaneous and travel categories show elevated decline rates:

| Category | Declined | Total | Decline Rate |
|---|---|---|---|
| Miscellaneous | 3 | 17 | **17.6%** |
| Travel | 10 | 94 | **10.6%** |
| Assets | 27 | 310 | 8.7% |
| Services | 6 | 79 | 7.6% |

By asset type (augmented), travel equipment stands out:

| Asset Type | Declined | Total | Decline Rate |
|---|---|---|---|
| travel_equipment | 9 | 58 | **15.5%** |
| miscellaneous | 1 | 7 | 14.3% |
| hardware_device | 30 | 346 | 8.7% |
| software_service | 6 | 74 | 8.1% |
| network_infrastructure | 0 | 15 | 0.0% |

**Insight**: Travel items and miscellaneous hardware lack clear governance frameworks, leading to higher rejection rates.

---

## Root Cause Assessment

### IT Department Decline Drivers

Analysis of declined IT submissions reveals:

1. **Custom CI identifiers**: 5 of 6 declined user-initiated IT submissions (83%) used non-standard identifiers.
2. **Process gaps in auto-generated submissions**: 10 automatically-generated IT submissions declined at 43.5%, suggesting validation or mapping defects in the system generation logic.
3. **Possible policy mismatch**: IT submissions (especially user-initiated) may face stricter compliance checks or lack proper pre-approval workflows.

### Secondary Drivers

- **Travel policy ambiguity**: Travel expense items lack explicit policy guidance, causing compliance uncertainty in reviewers.
- **Vague descriptions**: Miscellaneous and asset-class-only descriptions cannot be automatically validated, forcing manual review and rejection when insufficient detail is provided.
- **High expense amounts**: Declined submissions have a slightly lower mean amount ($3,706 vs. $4,436 for processed), but high-value travel and IT items likely trigger escalated approval chains.

---

## Quantified Improvement Opportunities

### Opportunity 1: IT Department Process Improvement (Est. 16 declines eliminated)
- **Current state**: 19 declined IT submissions (44.2% rate) from 43 submissions
- **Target**: Reduce IT rate from 44.2% to 12% (midpoint between IT baseline and Finance/HR)
- **Impact**: ~9 fewer declines
- **Actions**:
  - Audit IT submission workflows (both user-initiated and auto-generated)
  - Implement pre-submission validation (CI identifier format, description standards)
  - Clarify IT asset procurement policies; establish approval SLAs
  - Separate manual and auto-generated review pathways

### Opportunity 2: CI Identifier Standardization (Est. 5 declines eliminated)
- **Current state**: Custom identifiers (15.9% decline rate, 63 submissions, 10 declines)
- **Target**: Migrate all custom identifiers to standard model numbers (8.0% rate)
- **Impact**: ~5 fewer declines
- **Actions**:
  - Enforce standard format for CI identifiers in submission forms
  - Map existing custom identifiers to official model/service names
  - Flag non-standard CIs for requester correction before submission

### Opportunity 3: Travel Policy Clarification (Est. 2 declines eliminated)
- **Current state**: Travel expenses (10.6% decline rate, 94 submissions, 10 declines)
- **Target**: Reduce to non-travel level (8.9% rate)
- **Impact**: ~2 fewer declines
- **Actions**:
  - Create approved list of reimbursable travel items and categories
  - Require detailed justification (business purpose, trip dates) for travel submissions
  - Establish single-source-of-truth for travel policies by department

### Combined Impact
Implementing all three interventions could reduce total declines from 46 to approximately **29–31 (37% reduction)**.

---

## Method Note

**TAPP-augmented columns used in this analysis:**

- `submission_pattern`: Categorizes submission mode (automatically_generated, user_initiated, travel_related)
- `ci_identifier_quality`: Evaluates CI identifier format (standard_model_number, custom_identifier, descriptive_only, generic_placeholder)
- `expense_description_specificity`: Measures description detail level (product_model_named, service_type_specified, asset_class_implied, generic_category_only)
- `travel_expense_flag`: Binary flag for travel-related submissions
- `asset_type_category`: Classifies asset type (hardware_device, software_service, travel_equipment, network_infrastructure, miscellaneous)
- `requisition_source_department`: Source department for the requisition

These augmented columns add semantic clarity to expense submission quality and compliance risk. They do not replace original structured fields (department, state, category, ci, source_id, amount, processed_date) but complement them by identifying patterns not explicitly labeled in the raw data. All quantitative claims in this report integrate augmented and original columns.

---

## Recommendations

1. **Immediate (0–3 months)**:
   - Audit all declined IT submissions from the past 12 months to identify systematic issues.
   - Implement CI identifier validation in submission forms.
   - Publish travel expense policy FAQ to clarify reimbursable categories.

2. **Short-term (3–6 months)**:
   - Redesign IT expense workflow with pre-submission checklist (department, asset type, CI format, description).
   - Migrate custom CI identifiers to standard format; update CMDB mappings.
   - Establish travel expense approval gate with escalation rules.

3. **Medium-term (6–12 months)**:
   - Monitor decline rates by department monthly; set targets (e.g., IT → 15% within 6 months).
   - Extend standardization to all asset categories.
   - Consider automated pre-screening for vague descriptions and policy violations.

---

## Conclusion

Declined expense submissions are concentrated in the **IT department (44.2% decline rate)**, driven by custom CI identifiers, weak submission processes, and possible policy gaps. Secondary risks include travel expense ambiguity (10.6%) and vague asset descriptions (13.2%). By targeting IT process improvements, enforcing standard CI formats, and clarifying travel policy, organizations can reduce overall declines by 37% (from 46 to ~29 submissions) and improve operational efficiency and financial control.
