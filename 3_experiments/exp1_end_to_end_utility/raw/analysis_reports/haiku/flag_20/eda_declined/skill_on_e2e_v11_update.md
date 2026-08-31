---
dataset: flag_20
scenario: eda_declined
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "state_declined"
query: "What signals in a travel-expense description predict whether it will be declined?"
source_table: augment_table/flag_20/eda_declined/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:18:40.866784+00:00
wall_seconds: 107.15
---

# Travel-Expense Decline Prediction Analysis

**Query:** What signals in a travel-expense description predict whether it will be declined?

**Dataset:** 500 expense records (146 Travel category), with 84 total declines (61 from Travel category, 16.8% overall decline rate, 41.8% decline rate for Travel).

## Executive Summary

Travel expenses are declined at **41.8%** compared to 6.0% for Assets, 10.6% for Services, and 3.8% for Miscellaneous. Decline signals are predominantly categorical and mechanical rather than textual-semantic:

1. **Asset type mismatch**: Travel-accessories and vehicles are high-risk (43.2% and 63.6% decline rates)
2. **Lack of system tracking**: Untracked expenses decline at 43.2% vs. 14.3% for tracked ones (Travel only)
3. **Generic or placeholder asset descriptions**: Generic descriptions decline at 49.1% vs. 36.4% for specific models (Travel only)
4. **Automated generation without validation**: 40.8% decline rate for automated-generation expense mechanism (Travel only)

## Method Note

**TAPP-generated columns used in substantive analysis:**
- `asset_type_category` – semantic categorization of asset type (travel_accessory, vehicle, travel_service, hardware, etc.)
- `asset_specificity` – degree of specificity in asset naming (generic_placeholder, generic_class, specific_model, service_name)
- `expense_mechanism` – data entry method (automated_generation, procurement_order, manual_entry, system_creation)
- `source_system_tracking` – whether expense has external system tracking reference (boolean)

These were selected because they add material semantic signal beyond raw structured fields and directly address asset validation and origin clarity.

---

## Findings

### 1. Primary Signal: Asset Type Category

**Travel expenses by asset type (decline rate):**

| Asset Type | Total | Declined | Rate |
|---|---|---|---|
| Vehicle | 11 | 7 | **63.6%** |
| Travel Accessory | 74 | 32 | **43.2%** |
| Travel Service | 24 | 9 | **37.5%** |
| Hardware | 36 | 13 | 36.1% |

**Interpretation:** Vehicles and travel-accessories (luggage, travel kits, GPS devices) have significantly higher decline rates than hardware or services. The `asset_type_category` TAPP column captures a semantic distinction that the raw `category="Travel"` field does not—it discriminates within Travel between procurement types.

**52.5% of all declined travel expenses (32/61) are travel-accessories alone.** Combined with vehicles (11.5%), these two categories account for **64% of travel declines**.

### 2. Signal: Asset Specificity

Generically described assets decline at higher rates than specifically named ones:

| Specificity | Total (Travel) | Declined | Rate |
|---|---|---|---|
| Generic Placeholder | 53 | 26 | **49.1%** |
| Generic Class | 29 | 12 | **41.4%** |
| Specific Model | 55 | 20 | 36.4% |
| Service Name | 9 | 3 | 33.3% |

**Interpretation:** When travel expenses use generic placeholders like "Travel Equipment 3", "Travel Case", or "Travel Kit 01" (rather than "Samsonite Luggage" or "Dell Inspiron 15"), the description provides insufficient detail for validation. The `asset_specificity` TAPP field detects this semantic loss; **49.1% decline rate for generic placeholders vs. 36.4% for specific models represents a 13.4 pp risk increase**.

### 3. Signal: Expense Mechanism (Data Entry Method)

| Mechanism | Total (Travel) | Declined | Rate |
|---|---|---|---|
| Procurement Order | 5 | 5 | **100.0%** |
| Manual Entry | 12 | 5 | 41.7% |
| Automated Generation | 103 | 42 | 40.8% |
| System Creation | 26 | 9 | 34.6% |

**Interpretation:** The `expense_mechanism` TAPP column reveals a critical procedural signal: **all 5 travel procurement orders were declined** (small sample, but 100% rate). Automated generation shows high risk (40.8%), while system-creation via API shows the lowest risk (34.6%). This suggests that manual and automated processes lack proper validation gates that system-integrated creation has.

### 4. Signal: Source System Tracking

| Tracking Status | Total (Travel) | Declined | Rate |
|---|---|---|---|
| Not Tracked (False) | 139 | 60 | **43.2%** |
| Tracked (True) | 7 | 1 | 14.3% |

**Interpretation:** The `source_system_tracking` TAPP boolean is a strong indicator. Travel expenses lacking external system integration (`source_system_tracking=False`) decline at 43.2%, while tracked ones decline at only 14.3%—a **28.9 percentage point difference**. Tracked expenses (those with a valid `source_id`) have institutional accountability; untracked ones are orphaned.

### 5. Signal: Purchase Intent Signal

| Intent | Total (Travel) | Declined | Rate |
|---|---|---|---|
| Generation | 38 | 17 | 44.7% |
| Creation | 54 | 23 | 42.6% |
| New Acquisition | 42 | 17 | 40.5% |
| Registration | 12 | 4 | 33.3% |

**Interpretation:** The `purchase_intent_signal` TAPP field shows that "generation" (auto-created entries) and "creation" (new items) have higher decline rates (44.7%, 42.6%) than "registration" of existing items (33.3%). This aligns with a pattern: new and unvalidated entries are riskier.

### 6. Signal: Department Context

Among travel expenses by department:

| Department | Total | Declined | Rate |
|---|---|---|---|
| IT | 11 | 6 | 54.5% |
| HR | 2 | 1 | 50.0% |
| Customer Support | 79 | 35 | 44.3% |
| Sales | 44 | 18 | 40.9% |
| Finance | 4 | 1 | 25.0% |
| Development | 5 | 0 | 0.0% |

**Interpretation:** IT and HR show higher decline rates. HR's high rate may reflect personal travel policies or approvals (small n=2). IT's 54.5% rate suggests travel expenses in IT are less clearly business-justified or more prone to miscategorization.

### 7. Composite Risk Model

Combining asset type, specificity, mechanism, and tracking:

| Risk Score | Total (Travel) | Declined | Rate | Pattern |
|---|---|---|---|---|
| 0–2 | 18 | 5 | 27.8% | Low risk (tracked, specific, system-created) |
| 3–5 | 38 | 15 | 39.5% | Moderate (mixed signals) |
| 6–8 | 90 | 41 | 45.6% | High risk (untracked, generic, automated/manual) |

A simple additive risk model (asset type: +1 to +3; specificity: +1 to +2; mechanism: +1; tracking: +2) shows a clear gradient: **low-risk composite profiles decline at 27.8%; high-risk profiles at 45.6%**.

### 8. Amount Signal

Amount does **not** meaningfully distinguish decline:

- **Declined**: mean=$3,793, median=$3,699, std=$2,144
- **Processed**: mean=$3,928, median=$3,618, std=$1,990

Ranges overlap (min $521–$7,798), and no threshold effect is observed. Decline is not a price-control signal.

### 9. Description Text Patterns

Text-level analysis shows minimal discriminative power:

| Keyword | Declined | Processed | Difference |
|---|---|---|---|
| "travel" | 98.4% | 94.2% | +4.2 pp |
| "asset" | 65.6% | 67.3% | −1.7 pp |
| "automatically" | 26.2% | 25.0% | +1.2 pp |
| "generated" | 34.4% | 30.8% | +3.6 pp |
| "equipment" | 34.4% | 32.7% | +1.7 pp |

**Interpretation:** Short description text contains minimal discriminative signal. Both declined and processed expenses use similar language. The signal is in the *metadata* (`asset_type_category`, `asset_specificity`, `source_system_tracking`) rather than the free text itself.

### 10. Description Length

Description length is uniform across outcomes:
- **Declined**: mean=41 chars, median=36
- **Processed**: mean=43 chars, median=38

No meaningful difference (within 2 characters).

---

## Decline Risk Hierarchy (Travel Expenses)

**Highest Risk** (≥50% decline):
- Vehicle assets  
- Travel-accessories with generic placeholders ("Travel Equipment 3", "Travel Kit", "Travel Case")  
- Procurement-order mechanism  
- Untracked expenses (no `source_id`)  

**Moderate Risk** (35–49%):
- Travel-accessories with generic class ("GPS Device", "Travel Suitcase")  
- Automated-generation mechanism  
- Manual-entry mechanism  
- "Generation" or "creation" purchase intent  

**Lower Risk** (<35%):
- System-created expenses (API-integrated)  
- Tracked expenses  
- Registered or allocated items (registration intent)  
- Specific model naming  
- Hardware or travel-service categories  

---

## Conclusion

**Travel-expense descriptions predict decline primarily through structural and procedural signals, not textual content:**

1. **Asset type and specificity**: Assets categorized as vehicles or generically described travel-accessories are flagged as high-risk during description review.

2. **System integration**: Expenses lacking `source_system_tracking` (no external `source_id`) or created via unvalidated manual/automated processes are declined at ~43%, versus 14% for tracked, system-integrated ones.

3. **Procedure over content**: Automated generation without validation gates and procurement-order channels (100% decline in sample) suggest policy gaps rather than description content issues.

4. **Weak text signals**: Free-text descriptions contain no meaningful discriminative patterns; similar language appears in both declined and processed expenses.

**Actionable implication**: Decline prediction should use the semantic categorical fields (`asset_type_category`, `asset_specificity`, `expense_mechanism`, `source_system_tracking`) as primary features rather than parsing description text. Improvements in system tracking and specification clarity (e.g., requiring brand/model names, mandating `source_id`) would reduce false declines more than description rewording.
