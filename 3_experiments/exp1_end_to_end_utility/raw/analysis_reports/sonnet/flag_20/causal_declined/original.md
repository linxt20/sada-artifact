---
dataset: flag_20
scenario: causal_declined
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: causal_attribution
focus_variable: "state_declined"
query: "Why do some travel expenses get declined, and which factors contribute the most?"
source_table: augment_table/flag_20/causal_declined/original.csv
generated_at: 2026-07-26T13:29:21.201234+00:00
wall_seconds: 78.05
---

# Analysis Report: Why Travel Expenses Get Declined

**Dataset:** `flag_20/causal_declined/original.csv` | **Variant:** original | **Records:** 500

---

## Executive Summary

84 of 500 expenses (16.8%) are Declined. The dominant driver is **expense category**: Travel expenses are declined at a dramatically higher rate than any other category. Secondary factors include the absence of a `source_id`, specific departments, and item type (hardware-like travel assets vs. legitimate travel goods).

---

## Key Findings

### 1. Category Is the Strongest Predictor of Decline

| Category | Declined | Total | Decline Rate |
|---|---|---|---|
| **Travel** | **61** | **146** | **41.8%** |
| Services | 5 | 47 | 10.6% |
| Assets | 17 | 281 | 6.0% |
| Miscellaneous | 1 | 26 | 3.8% |

Travel accounts for **73% of all declined records** despite being only 29% of total records. This is the single most impactful factor.

### 2. Missing `source_id` Is Structurally Linked to Decline

- Every Travel and Miscellaneous record lacks a `source_id` (172 records total with no `source_id`).
- Among no-`source_id` records: **62 of 172 are Declined (36%)**, vs. only **22 of 328 with a `source_id` (6.7%)**.
- All 61 declined Travel records have no `source_id`.
- This is partially a structural artifact (Travel/Miscellaneous never carry source IDs), but it still serves as a reliable proxy: **an absent `source_id` multiplies decline risk ~5×**.

### 3. Declined Expenses Have No Processed Date

All 84 declined records have an empty `processed_date`, consistent with expenses that were rejected and never completed the processing workflow.

### 4. Department Has Limited Independent Effect

| Department | Declined | Total | Decline Rate |
|---|---|---|---|
| Customer Support | 48 | 272 | 17.6% |
| Sales | 26 | 141 | 18.4% |
| IT | 7 | 42 | 16.7% |
| HR | 1 | 5 | 20.0% |
| Finance | 1 | 16 | 6.3% |

Decline rates across departments are broadly similar (6–20%), suggesting department is a **weak independent factor**. Finance shows notably lower declines, but sample sizes are small. The Customer Support and Sales departments have the highest raw counts simply because they dominate the dataset.

### 5. Amount Is Not a Strong Driver

- Declined expenses: mean = **$3,912**, median = **$3,722**
- Non-declined expenses: mean = **$4,486**, median = **$4,367**

Declined amounts are slightly lower on average, but the difference is modest. Both high-value (>$5,000: 27 declined) and low-value (≤$2,000: 23 declined) items appear in declined records, with no clear threshold effect.

### 6. `type` Field Is Uniformly Blank for Declined Records

All 84 declined records have an empty `type` field. Whether this is a cause or a consequence of decline status is unclear, but it may indicate these expenses were submitted without proper categorization/coding.

### 7. Nature of Declined Travel Items

Declined travel CIs include items such as GPS devices, business suitcases, VPN devices, satellite phones, corporate jets, and laptop-labeled "travel assets." Many appear to be **hardware assets mis-classified under Travel** (e.g., "Dell Latitude E7470", "Global Positioning System Device") or expenses on items outside policy (e.g., "Aircraft Airbus A320", "Corporate Jet A320"), suggesting item-level policy violations as a contributing reason.

---

## Contributing Factors (Ranked by Strength of Evidence)

| Rank | Factor | Evidence Strength |
|---|---|---|
| 1 | **Category = Travel** | Strong – 42% decline rate vs. ~6% elsewhere |
| 2 | **Absent `source_id`** | Strong – but confounded with category |
| 3 | **Blank `type` field** | Moderate – present for all declines, likely a data quality flag |
| 4 | **Nature of CI** (hardware-like or out-of-policy items) | Moderate – qualitative, visible in descriptions |
| 5 | **Department** | Weak – no meaningful spread across departments |
| 6 | **Amount** | Weak – no threshold or directional pattern |

---

## Caveats and Exceptions

- **17 Asset records are declined** despite Assets having a low overall rate. These lack a clear shared pattern beyond having a `source_id` and blank `type`; they may represent duplicate entries or unauthorized purchases.
- The correlation between `source_id`-absent and Travel/Miscellaneous is 100%, making it impossible to fully disentangle structural data rules from causal factors.
- Small subgroups (HR, Finance, Product Management) limit statistical confidence for department-level conclusions.
- The dataset covers a ~12-month period (Jun 2023–Apr 2024) with no obvious temporal spike in declines.
