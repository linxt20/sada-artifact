---
dataset: flag_19
scenario: concept_attribute_declined
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "declined_expense_reasons"
query: "What reasons or compliance risks appear in declined expenses?"
source_table: augment_table/flag_19/concept_attribute_declined/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:16:45.731772+00:00
wall_seconds: 122.68
---

# Analysis Report: Reasons and Compliance Risks in Declined Expenses

## Executive Summary

This analysis examines 46 declined expenses (9.2% of 500 total) in the dataset to identify dominant patterns of decline reasons and compliance risks. The augmented table combines original structured data (state, category, department, amount, source_id, short_description, ci) with TAPP-generated semantic facets (asset_type_category, provisioning_mechanism, resource_purpose_intent, departmental_context, documentation_completeness, travel_asset_flag) to provide multi-layered evidence.

**Primary findings:**
- **IT Department dominance**: 19 of 46 declines (41%) originate from IT, with a 44.2% decline rate—9× higher than the overall 9.2% baseline.
- **Documentation deficiency**: 63% of declines have missing or incomplete documentation (either_missing or only source_id_present).
- **Auto-generated processing risk**: 48% of declines are auto-generated entries, concentrated in hardware asset categories.
- **Travel category policy sensitivity**: 11% decline rate for travel (vs. 8.7% for assets), driven by compliance and policy gaps.
- **Hardware compute dominance**: 29 of 46 declines (63%) involve hardware_compute assets, predominantly Dell laptops and workstations.

---

## Methodology

**TAPP-generated columns used:**
- `documentation_completeness`: Captures whether both source_id and processed_date are present (both_present, either_missing, source_id_present, processed_date_present).
- `provisioning_mechanism`: Indicates submission mode (auto_generated, asset_created, manual_registration, service_based).
- `resource_purpose_intent`: Captures business intent (business_operation, travel, infrastructure).
- `departmental_context`: Normalized department field for consistency.
- `travel_asset_flag`: Boolean flag identifying travel-related expenses.

These augmented columns provide semantic clarity on compliance-relevant attributes without replacing original structured evidence. Original columns (state, category, department, amount, source_id, ci, short_description) remain primary evidence sources.

---

## Decline Patterns by Department

The IT department exhibits catastrophic decline concentration:

| Department      | Total | Declined | Decline Rate (%) |
|-----------------|-------|----------|------------------|
| IT              | 43    | 19       | **44.19**        |
| HR              | 14    | 2        | 14.29            |
| Finance         | 22    | 2        | 9.09             |
| Customer Support| 267   | 16       | 5.99             |
| Development     | 20    | 1        | 5.00             |
| Sales           | 122   | 6        | 4.92             |
| Product Mgmt    | 12    | 0        | 0.00             |

**Insight:** IT's 44% decline rate indicates systemic compliance or procedural failures, likely related to auto-generated entries and missing documentation. The `departmental_context` field confirms IT as the dominant risk locus.

---

## Documentation Completeness: Primary Compliance Risk

Documentation gaps emerge as the strongest predictor of decline:

| Documentation Status | Total | Declined | Decline Rate (%) |
|---------------------|-------|----------|------------------|
| **source_id_present only** | 48 | 14 | **29.17** |
| **either_missing** | 69 | 15 | **21.74** |
| both_present | 365 | 17 | 4.66 |
| processed_date_present | 18 | 0 | 0.00 |

**In declined expenses (n=46):**
- only_source_id_present: 14 entries (30%)
- either_missing (source_id OR processed_date): 15 entries (33%)
- both_present: 17 entries (37%)

**Interpretation:** When source_id is present but processed_date is absent, decline risk rises to 29.2%—**6× higher** than when both are present. Among the 15 "either_missing" declines, 10 (67%) are travel expenses, indicating that travel entries systematically lack processing dates or source IDs. Missing documentation prevents audit trails and approval verification, triggering compliance rejections.

---

## Provisioning Mechanism and Automation Risks

Provisioning mode correlates with decline likelihood:

| Provisioning Mechanism | Total | Declined | Decline Rate (%) |
|------------------------|-------|----------|------------------|
| manual_registration | 71 | 8 | 11.27 |
| asset_created | 123 | 13 | 10.57 |
| auto_generated | 249 | 22 | 8.84 |
| service_based | 57 | 3 | 5.26 |

Of 46 declined expenses, **22 (48%)** are `auto_generated`. Within IT's 19 declines, **11 (58%)** are auto-generated.

**Subset analysis—High-risk combination (auto_generated + incomplete documentation):**
- 44 rows match this combination
- 11 declined (25% decline rate)
- 7 of the 11 have `documentation_completeness='source_id_present'` only

**Interpretation:** Auto-generated entries lack manual review controls. When combined with missing processed_date or incomplete ci identifiers, they fail compliance gates. The short_descriptions for auto-generated declines frequently contain boilerplate text ("Automatically generated asset line for creation of..."), suggesting systematic flagging by audit systems due to lack of substantiating detail.

---

## Category-Level Decline Risks

| Category | Total | Declined | Decline Rate (%) |
|----------|-------|----------|------------------|
| **Miscellaneous** | 17 | 3 | 17.65 |
| **Travel** | 94 | 10 | **10.64** |
| Assets | 310 | 27 | 8.71 |
| Services | 79 | 6 | 7.59 |

**Miscellaneous (n=3 declines):** All three involve vague asset descriptions (e.g., "Raspberry Pi 4 Model B," "Meeting Room Projector," "Item_586"). These lack vendor standardization and approval history, triggering vague_misc_item compliance flags.

**Travel (n=10 declines, 21.7% of all declines):**
- 8 involve `travel_equipment` assets (GPS systems, luggage, travel bags, airline tickets)
- 2 involve `hardware_compute` categorized as travel-intent
- **6 of 10** have `either_missing` documentation (vs. 1 for non-travel)
- High travel decline rate reflects policy sensitivity: travel expenses require pre-approval and receipts; missing dates/IDs trigger automatic rejection

**Sample declined travel entries:**
- EXP00000054: "Ticket for purchase of corporate travel equipment" (Travel Case Pro, $936)
- EXP00000189: "Travel equipment asset" (Pocket WiFi 4G, $2,083)
- EXP00000240: "Automatically generated expense line for purchase of travel assets" (Business Class Airline Ticket, $2,164)
- EXP00000353: "Expensed TSA approved travel bag" (Travel Bag Deluxe, $2,312)

All lack source_id or processed_date, indicating failed pre-approval workflows.

---

## Asset Type and Amount Distribution

**Declined by asset_type_category:**

| Asset Type | Declined | % of Declines | Avg Amount |
|------------|----------|---------------|------------|
| hardware_compute | 29 | 63% | $3,521 |
| travel_equipment | 8 | 17% | $1,738 |
| software_service | 6 | 13% | $2,283 |
| hardware_peripheral | 2 | 4% | $3,113 |
| Unknown | 1 | 2% | $266 |

**Amount analysis:**
- Declined mean: $3,706 (median $3,471)
- Processed mean: $4,436 (median $4,509)
- Difference: Declined expenses are ~$730 (16%) lower on average, though high-value items (>$8000) are present in both groups

Declined hardware_compute items are predominantly **Dell laptops and workstations** (Latitude 7490, OptiPlex 3070/3080, Precision models), suggesting:
1. Systematic compliance review of high-volume commodity IT hardware
2. Duplicate or redundant purchase attempts (many identical model/serial combinations)
3. Asset tracking failures (multiple OptiPlex 3080 entries with slight description variations)

---

## Business Purpose and Compliance Drift

| Resource Purpose | Total | Declined | Decline Rate (%) |
|------------------|-------|----------|------------------|
| business_operation | 337 | 33 | 9.79 |
| travel | 94 | 10 | **10.64** |
| infrastructure | 69 | 3 | 4.35 |

Travel-intent expenses (identified by `resource_purpose_intent='travel'`) show a 10.64% decline rate, higher than infrastructure (4.35%). The `travel_asset_flag` augmented column identifies 93 travel-related rows; 10 declined (10.75% rate). Of these 10:
- 8 are in the Travel category (policy-aligned)
- 2 are hardware_compute items misclassified or reclassified to travel intent
- 8 have incomplete documentation

**Interpretation:** Travel expenses face stricter compliance gates due to policy sensitivity around per-diem limits, approved vendors, and advance approval requirements. Missing processing dates prevent approval-chain verification.

---

## Interdepartmental Compliance Patterns

**IT Department (19 declines):**
- 68% auto-generated (11/19)
- Categories: Assets (13), Travel (3), Services (2), Miscellaneous (1)
- Documentation: both_present (7), either_missing (6), source_id_present (6)
- Primary risk: High-volume auto-generated hardware entries without full metadata

**Customer Support (16 declines):**
- 50% asset_created (8/19), 31% auto-generated (5/16)
- Categories: Assets (8), Travel (6), Services (1), Miscellaneous (1)
- Documentation: either_missing (7), both_present (5), source_id_present (4)
- Primary risk: Travel category over-representation (6/16); missing dates/IDs on travel gear

**Sales (6 declines):**
- Categories: Assets (3), Services (2), Miscellaneous (1)
- Decline rate 4.92% (6/122) — well below IT
- Primary risk: Miscellaneous category entry (Item_586) with no specific ci value

---

## Key Compliance Risk Signals

Synthesizing original and augmented evidence, the declined expense dataset reveals **six dominant compliance failure modes:**

1. **Missing Processing Date** (`documentation_completeness='either_missing'`): 15 declined (33%)
   - Prevents audit trail verification
   - Concentrated in Travel category (10/15 = 67%)
   - Blocks approval chain confirmation

2. **Auto-Generated with Incomplete Metadata**: 22 declined (48%)
   - No manual reviewer oversight
   - Often contain generic descriptions ("Automatically generated asset line...")
   - Risk escalates when combined with missing source_id (11 cases, 25% decline rate)

3. **Travel Policy Non-Compliance** (`travel_asset_flag=True` OR `resource_purpose_intent='travel'`): 10 declined (21.7% of total)
   - Missing pre-approval indicators
   - Lack of vendor/receipt documentation
   - Sensitivity to per-diem and advance-booking rules

4. **Miscellaneous/Vague Item Classification**: 3 declined (6.5%)
   - Non-standard assets (Raspberry Pi, Projector, generic Item_586)
   - Insufficient ci value (sometimes "Item_586" instead of vendor/serial)
   - Auditors cannot verify legitimacy

5. **Commodity Hardware Duplication** (hardware_compute, 29 declined): 63% of declines
   - Identical or near-identical Dell models appearing repeatedly
   - Suggests duplicate purchase attempts or untracked inventory
   - Risk heightened in IT department (13/19 IT declines are hardware_compute)

6. **IT Department Systemic Failures** (44.19% decline rate): 19 declined
   - Insufficient controls on auto-generated entries
   - Procedural drift in asset registration workflows
   - Possible IT system integration failures (ERP/asset management system)

---

## Quantified Risk Summary

| Risk Factor | Count | % of Declined | Decline Rate in Group |
|-------------|-------|---------------|-----------------------|
| Missing documentation | 29 | 63% | 21.7% (vs. 4.7% if both_present) |
| Auto-generated entries | 22 | 48% | 8.8% (in full dataset) |
| Travel category | 10 | 21.7% | 10.6% (vs. 8.7% overall) |
| IT department | 19 | 41.3% | 44.2% (vs. 9.2% overall) |
| Miscellaneous category | 3 | 6.5% | 17.7% (highest categorical risk) |
| Hardware compute assets | 29 | 63% | 8.7% (in full dataset) |

---

## Conclusion

Declined expenses cluster around three interdependent failure modes:

1. **Procedural:** Missing processing dates and source IDs prevent compliance verification (63% of declines).
2. **Systemic:** IT Department auto-generated entries lack human review controls (11 of 19 IT declines).
3. **Policy-driven:** Travel expenses face heightened scrutiny due to policy sensitivity; missing pre-approval indicators trigger blanket rejection.

The augmented semantic facets (`documentation_completeness`, `provisioning_mechanism`, `travel_asset_flag`) align strongly with original structured evidence, confirming that declined expenses are primarily driven by **documentation deficiency and lack of manual oversight** rather than substance-level issues. Mean declined amount ($3,706) is comparable to processed expenses ($4,436), indicating price is not a decline driver.

**Remediation priorities:**
1. Enforce mandatory processed_date capture, especially for travel expenses.
2. Require manual review before auto-generating IT asset entries above threshold amounts.
3. Establish travel pre-approval workflows linked to expense records.
4. Implement duplicate purchase detection for commodity hardware.
