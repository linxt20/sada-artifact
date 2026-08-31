---
dataset: flag_20
scenario: concept_attribute_travel
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "travel_policy_risk"
query: "What travel policy risks appear in expense descriptions?"
source_table: augment_table/flag_20/concept_attribute_travel/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:17:25.391900+00:00
wall_seconds: 45.3
---

# Travel Policy Risk Analysis
**Dataset:** `sonnet__skill_off_update.csv` | **Variant:** skill_off | **Rows:** 500

---

## Overview

The dataset contains 500 expense records across categories including Assets, Travel, Services, and Miscellaneous. Travel policy risk flags are **exclusively present in `category = Travel` rows** (146 records); no non-travel category carries any risk flag. Of the 146 travel rows, **72 (49%)** carry at least one policy risk flag.

---

## Risk Level Distribution (Travel Rows)

| Risk Level | Count | % of Travel Rows |
|------------|-------|-----------------|
| None       | 74    | 51%             |
| Low        | 60    | 41%             |
| Medium     | 9     | 6%              |
| High       | 3     | 2%              |

---

## Identified Risk Flag Types

### 1. High-Value Expense (>$5,000) — Most Prevalent
- **45 occurrences** as standalone flag (Low risk); appears in compound flags for Medium/High rows too.
- Average amount for flagged travel rows: **~$5,458** vs **~$2,920** for unflagged rows — a clear monetary threshold effect.
- Trigger: any travel item (luggage, GPS devices, suitcases, flight tickets) exceeding $5,000 requires manager approval.

### 2. Air Travel Compliance Flags — Highest Severity Driver
- **"Business class air travel (requires VP approval)"** — triggers VP-level approval; appears in all 3 **High**-risk records.
- **"Air travel (requires advance booking compliance check)"** — co-occurs with business class or high-value flags.
- High-risk examples: `Business Class Flight Ticket` ($6,784), `Business Class Airline Ticket` ($5,874, $6,361) — all flagged with 3 simultaneous risk conditions.

### 3. Luxury/Premium Items
- **4–5 occurrences**, e.g., `Premium Luggage Case` ($7,260), `Travel Suitcase Deluxe` ($1,912).
- Risk: may exceed policy spend limits; typically Low–Medium level.

### 4. International Travel
- **3–4 occurrences** — requires additional approvals; one combined with passport/travel document reimbursability concern (`Passport Controller`, $2,970).

### 5. Company Vehicle / Rental Car
- **3–4 occurrences** — company vehicles require fleet management review; rental cars require pre-approval.
- Example: `Rental Car` ($4,374), `Company Car Model X` ($7,078).

### 6. Unusual/Edge-Case Items
- `Satellite phone` — flagged as unusual equipment requiring justification.
- `Private/corporate jet` — flagged as likely policy violation (single occurrence, most severe individual flag type).

---

## Approval Status of Flagged Expenses

| State     | Count (Flagged) |
|-----------|-----------------|
| Declined  | 29 (40%)        |
| Processed | 21 (29%)        |
| Submitted | 12 (17%)        |
| Pending   | 10 (14%)        |

A notable portion of flagged expenses were **Processed** (29%), suggesting policy risks do not automatically block reimbursement — indicating a gap between detection and enforcement.

---

## Key Observations & Caveats

- **Short descriptions** are largely auto-generated boilerplate ("Automatically generated expense line for creation of travel equipment") and do not encode the risk directly — risk is determined by the **CI (configuration item/asset name)** rather than the description text.
- The `skill_off` variant may reflect a model without risk-classification skill, yet risk flags are present and consistent — suggesting the flags were injected or rule-based rather than model-predicted.
- Evidence for the private jet violation is weak (single row); the satellite phone flag is also isolated.
- The $5,000 threshold is a hard rule, creating a clear cluster of Low-risk flags near that boundary.

---

## Decision-Ready Summary

| Risk Type | Frequency | Severity | Primary Trigger |
|---|---|---|---|
| High-value (>$5,000) | High (45+) | Low–High | Amount threshold |
| Business class air travel | Low (6) | High | CI name contains "Business Class" |
| Air travel booking compliance | Low (8) | Medium–High | Airline ticket items |
| Luxury/premium items | Low (5) | Low–Medium | Premium product keywords |
| International travel | Low (4) | Medium | International/passport CI keywords |
| Company vehicle / rental car | Low (4) | Medium | Vehicle-related CI names |
| Private jet / unusual equipment | Very Low (2) | High | Specific CI patterns |
