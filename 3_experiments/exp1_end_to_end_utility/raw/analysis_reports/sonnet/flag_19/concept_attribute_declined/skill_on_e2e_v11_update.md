---
dataset: flag_19
scenario: concept_attribute_declined
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "declined_expense_reasons"
query: "What reasons or compliance risks appear in declined expenses?"
source_table: augment_table/flag_19/concept_attribute_declined/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:16:03.638960+00:00
wall_seconds: 75.15
---

# Compliance Risk Analysis: Declined Expense Entries

**Query:** What reasons or compliance risks appear in declined expenses?

---

## 1. Overview

Of 500 expense records, **46 (9.2%) are in `Declined` state**. All 46 declined entries have a missing `processed_date`, confirming they were never successfully processed — a necessary cross-check that the `state` label is consistent with the data. The remaining states are Processed (333), Pending (80), and Submitted (41).

---

## 2. Primary Compliance Risk Signals

### 2.1 Missing Source ID (`source_id_present`)

| source_id_present | Declined (n=46) | All other states (n=454) |
|---|---|---|
| False (missing) | **14 (30.4%)** | 98 (21.6%) |
| True (present) | 32 (69.6%) | 356 (78.4%) |

Declined expenses are **~1.4× more likely to be missing a source ID** than non-declined expenses. Critically, the missing-source-ID pattern is concentrated in the **Travel** and **Miscellaneous** categories: all 10 declined Travel entries and all 3 declined Miscellaneous entries lack a `source_id`, while only 1 of 27 declined Assets entries lacks one. Missing source ID is a primary documentation compliance gap.

### 2.2 Category Breakdown of Declined Entries

| Category | Declined (n) | Declined Rate (of category total) |
|---|---|---|
| Assets | 27 (58.7%) | 27/227 = **11.9%** |
| Travel | 10 (21.7%) | 10/94 = **10.6%** |
| Services | 6 (13.0%) | 6/91 = **6.6%** |
| Miscellaneous | 3 (6.5%) | 3/88 = **3.4%** |

Assets and Travel categories carry the highest absolute and relative decline burden.

### 2.3 Low Asset Amount vs. Peers

Declined expenses have a notably **lower mean amount ($3,706)** compared to Processed ($4,436), Pending ($4,398), and Submitted ($4,433). This suggests declined entries are not simply large-ticket items being flagged for cost control — the compliance issues are more likely process/documentation failures rather than amount-based thresholds.

---

## 3. TAPP-Augmented Column Analysis

*TAPP-generated columns used: `asset_category`, `entry_origin`, `asset_lifecycle_action`, `source_id_present`, `ci_id_quality`, `travel_related`.*

### 3.1 CI/Asset Identifier Quality (`ci_id_quality`)

| ci_id_quality | Declined (n) | Risk signal |
|---|---|---|
| named_model | 25 (54.3%) | Baseline |
| opaque_code | **10 (21.7%)** | High — non-descriptive CI reference |
| travel_label | 7 (15.2%) | All Travel category |
| service_label | 3 (6.5%) | Services |
| generic_placeholder | 1 (2.2%) | "Automatically generated" CI |

**`opaque_code` CI quality is a meaningful compliance risk signal.** Entries with `ci_id_quality = opaque_code` include auto-generated records like "Automatically generated asset entry for Dell Optiplex 3080 Desktop" (EXP00000238, $8,084) and non-traceable CI codes on high-value laptops and desktops. These 10 entries span Assets and Miscellaneous categories and include 3 of the 14 highest-value declined entries (>$7,000).

### 3.2 Asset Lifecycle Action (`asset_lifecycle_action`)

| action | Declined (n) | Compliance note |
|---|---|---|
| registration | 15 (32.6%) | Largest group; 13/15 are IT/Customer Support Assets |
| auto_generated_action | **13 (28.3%)** | Fully auto-generated records — no human validation |
| travel_expense | 8 (17.4%) | All from Travel category; 8/10 Travel declines |
| new_acquisition | 5 (10.9%) | Mix of Assets and Travel |
| provisioning | 3 (6.5%) | All Services |
| allocation | 1 | — |
| configuration | 1 | — |

`auto_generated_action` entries (13 declined) come from `entry_origin = auto_generated` (n=18 total declined), meaning **39% of declined records were system-generated without manual review**. These auto-generated declined entries include high-value Assets ($8,301; $7,990; $7,316; $5,525) and Services records with `generic_placeholder` CI quality — clear indicators that automated pipelines are submitting incomplete or unverifiable expense records.

### 3.3 Entry Origin (`entry_origin`)

Auto-generated entries represent **39.1% of declined** vs. 29.7% of Processed — a modestly elevated rate, but the concern is that auto-generated entries disproportionately appear in **high-value, opaque-CI declined records** (see §3.1–3.2).

### 3.4 Asset Category (`asset_category`)

Among declined entries, `hardware_laptop` (23/46, 50%) dominates, followed by `hardware_desktop_workstation` (6), `travel_accessory` (6), and `software_service` (5). Laptop and desktop assets together account for **63%** of declined entries. The high representation of `hardware_laptop` in `registration` lifecycle actions suggests that bulk laptop registrations — possibly auto-generated batches — are a systemic source of declined records.

### 3.5 Travel-Related Flag (`travel_related`)

`travel_related = True` for 10/46 declined entries (21.7%), matching the Travel category count exactly. The travel decline rate (10/94 = 10.6%) is comparable to Assets (11.9%), but the compliance risk is distinct: **all 10 declined travel entries lack a source_id**, pointing to missing receipts or booking references as the primary cause.

---

## 4. Department Risk Profile

| Department | Declined (n) | Top category declined |
|---|---|---|
| IT | **19 (41.3%)** | Assets (13) |
| Customer Support | 16 (34.8%) | Assets (8) |
| Sales | 6 (13.0%) | Assets (3), Services (2) |
| Finance | 2 | Assets |
| HR | 2 | Assets (1), Travel (1) |
| Development | 1 | Services |

IT and Customer Support together account for **76%** of all declined records, driven by asset registration and auto-generated actions. This likely reflects bulk hardware procurement or asset management workflows that generate incomplete records.

---

## 5. High-Value Declined Entries (>$5,000)

There are **14 declined entries above $5,000** (30% of all declined), all in the **Assets** category, split between IT (7) and Customer Support (4). Of these, 3 carry `ci_id_quality = opaque_code` — meaning the CI identifier is non-transparent for records exceeding $7,000–$8,800. These represent the highest financial exposure in the declined pool.

---

## 6. Summary of Compliance Risks

| Risk | Evidence | Affected Records |
|---|---|---|
| **Missing source ID** | 30.4% of declined lack `source_id`; 100% of Travel/Misc declined | 14 records |
| **Auto-generated records without validation** | `asset_lifecycle_action = auto_generated_action`; `entry_origin = auto_generated` | 13–18 records |
| **Opaque CI references** | `ci_id_quality = opaque_code` in 10 declined, incl. high-value assets | 10 records |
| **Travel documentation gap** | All 10 declined Travel entries: no source_id, `travel_label` CI quality | 10 records |
| **Bulk asset registration failures** | 15 `registration` actions declined, dominated by IT/Customer Support laptops | 15 records |

**Primary conclusions:** Declined expenses cluster around two distinct compliance failure modes — (1) **documentation gaps** (missing `source_id`, opaque CIs, travel receipts) and (2) **process failures** in automated asset pipelines that generate unverifiable records. Neither is primarily amount-driven; declined entries are actually *lower-value* on average than processed ones, ruling out a simple high-amount rejection policy.
