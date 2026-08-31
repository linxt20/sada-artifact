---
dataset: flag_20
scenario: causal_reduce
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "travel_expense_declined_status"
query: "How can we reduce declined travel expenses?"
source_table: augment_table/flag_20/causal_reduce/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:17:23.953941+00:00
wall_seconds: 53.56
---

# Reducing Declined Travel Expenses

## Overview

The dataset contains **146 travel-category expenses**, of which **61 (41.8%) are Declined** — the highest-volume terminal-negative state. This is the primary focus variable for reduction.

---

## Key Findings

### 1. Missing Processed Date is the Strongest Predictor of Decline
All 61 declined travel expenses have **no `processed_date`**. Of the 94 travel records without a processed date, 61 (64.9%) are Declined. Conversely, every one of the 52 records with a processed date was Processed (0% decline). While absence of a processed date is partly a *consequence* of decline rather than a cause, it signals that travel expenses reaching a processor for review succeed — those that never enter proper processing do not.

> **Implication:** Travel expenses that lack a valid workflow routing or approver assignment never get processed. Ensuring every travel submission is routed to an approver would likely break the decline pattern.

### 2. `asset_action_type = registration` Drives Most Declines
| action type | declined | total | decline rate |
|---|---|---|---|
| registration | 41 | 90 | **45.6%** |
| tracking | 6 | 14 | 42.9% |
| new_procurement | 14 | 41 | 34.1% |
| allocation | 0 | 1 | 0% |

Registration-type travel expenses account for **67% of all declined travel records**. These appear to be auto-generated or loosely described entries (e.g., "Automatically generated expense line for creation of travel equipment") that may lack proper justification or a linked source.

### 3. Missing `source_id` Affects All Declined Travel Records
Every declined travel record has `has_source_id = False`. This is consistent across all 61 declined cases. In contrast, processed travel expenses also lack source IDs (the travel category never carries a source ID), so this alone is not discriminating between travel outcomes — but it does confirm that **travel expenses are structurally under-documented** compared to Assets/Services categories.

### 4. Manual Entry Method has a Higher Absolute Decline Count
| entry_method | declined | total | decline rate |
|---|---|---|---|
| manual | 42 | 95 | 44.2% |
| automated | 19 | 51 | 37.3% |

Manual entries produce more declined records overall. However, the interaction with `asset_action_type` reveals a nuance: **automated + new_procurement** has a very low decline rate (7.7%), while **manual + new_procurement** declines at 46.4%. This suggests automated procurement submissions may follow a more structured workflow.

### 5. `travel_brand` CI Brand Dominates Declined Records
43 of 61 declined records (70.5%) carry `ci_brand = travel_brand`, with an overall 43% decline rate for this group. Expenses linked to specific hardware brands (Dell, Lenovo) decline at lower rates, possibly because they are tied to real asset procurement workflows.

### 6. Customer Support and Sales Are the Top Declining Departments
| department | declined | 
|---|---|
| Customer Support | 35 |
| Sales | 18 |
| IT | 6 |

These departments submit the most travel expenses overall, so high absolute declined counts are partly volume-driven. However, IT's decline rate (6 declined out of 11 total = 54.5%) warrants attention.

---

## Actionable Recommendations

| Priority | Action | Rationale |
|---|---|---|
| **High** | Enforce approver assignment at submission time | 100% of declined records never received a `processed_date`; routing to a reviewer appears sufficient to avoid decline |
| **High** | Replace open-ended "registration" action type for travel with mandatory procurement justification | `registration` accounts for 67% of declined travel; adding required fields would filter low-quality submissions early |
| **Medium** | Automate new_procurement travel entries where possible | Automated new_procurement declines at only 7.7% vs. 46.4% for manual; structured templates reduce ambiguity |
| **Medium** | Audit "travel_brand" CI entries for completeness | 43% decline rate; vague brand classification may indicate incomplete records |
| **Low** | Targeted review of IT department travel submissions | Disproportionate decline rate (54.5%) despite low volume |

---

## Caveats
- The dataset does not include an explicit **decline reason** field, so causal links are inferred from co-occurring attributes.
- `has_source_id` is universally `False` for travel, making it non-discriminating within this category.
- Sample sizes for some subgroups (HP: 2, allocation: 1) are too small to draw firm conclusions.
