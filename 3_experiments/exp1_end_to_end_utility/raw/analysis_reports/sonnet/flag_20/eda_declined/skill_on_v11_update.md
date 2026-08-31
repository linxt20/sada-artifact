---
dataset: flag_20
scenario: eda_declined
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "state_declined"
query: "What signals in a travel-expense description predict whether it will be declined?"
source_table: augment_table/flag_20/eda_declined/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:17:47.662303+00:00
wall_seconds: 55.12
---

# Travel-Expense Description Decline Signals
**Dataset:** `sonnet__skill_on_v11_update.csv` | 500 rows, 84 Declined (16.8% overall)

---

## 1. Strongest Predictors of Decline

### 1a. `processed_date_present` — Most Decisive Signal
| processed_date present | source_id present | Decline Rate | n |
|---|---|---|---|
| **No** | **No** | **61.4%** | 101 |
| No | Yes | 21.2% | 104 |
| Yes | No | 0.0% | 72 |
| Yes | Yes | 0.0% | 223 |

A missing `processed_date` combined with a missing `source_id` produces the highest decline rate in the dataset (61%). **Every declined record lacks a processed date.** This is a near-perfect necessary condition for decline.

### 1b. `expense_purpose = travel_expense`
| expense_purpose | Decline Rate | n |
|---|---|---|
| **travel_expense** | **41.5%** | 142 |
| maintenance_upgrade | 12.5% | 8 |
| service_provisioning | 9.3% | 43 |
| asset_procurement | 7.4% | 68 |
| asset_registration | 6.5% | 216 |
| miscellaneous | 4.3% | 23 |

Travel expenses are declined at 6× the rate of standard asset registrations. The word **"travel"** in `short_description` yields a 42.3% decline rate (n=142).

### 1c. `description_specificity`
| Specificity | Decline Rate | n |
|---|---|---|
| **vague_miscellaneous** | **38.9%** | 95 |
| generic_template | 29.0% | 93 |
| specific_named_asset | **6.4%** | 312 |

Vague or generic descriptions decline at ~5–6× the rate of specific ones. Among travel expenses specifically: vague travel = **44.9%** decline vs. specific travel = **25.8%** decline.

### 1d. `source_id_present`
| source_id present | Decline Rate | n |
|---|---|---|
| **False** | **35.8%** | 173 |
| True | 6.7% | 327 |

Missing source IDs (no audit trail reference) associate strongly with decline.

---

## 2. Secondary Signals

| Signal | Decline Rate | Notes |
|---|---|---|
| `category = Travel` | 41.8% (n=146) | vs. Assets 6.0%, Services 10.6% |
| `asset_category = travel` | 41.4% (n=145) | Closely mirrors category |
| `ci_hardware_class = Unknown` | 32.2% (n=152) | Unclassified CI items raise risk |
| `department_group = sales` | 18.4% (n=141) | Modestly elevated vs. finance (6.2%) |

---

## 3. Amount Has Minimal Predictive Power

| Outcome | Mean Amount | Median Amount |
|---|---|---|
| Not Declined | $4,486 | $4,367 |
| Declined | $3,912 | $3,722 |

Declined expenses are slightly lower in value, but the overlap is large. **Dollar amount alone is not a reliable signal.**

---

## 4. Combined Risk Profile (High-Risk Pattern)

A travel expense is most likely to be declined when it exhibits **all** of the following:
1. `expense_purpose = travel_expense`
2. `description_specificity = vague_miscellaneous` or `generic_template`
3. `processed_date_present = False`
4. `source_id_present = False`

This cluster accounts for the majority of the 84 declined records.

---

## 5. Exceptions and Weak Evidence

- **`entry_origin`** (auto-generated vs. manual) shows minimal differentiation (15–18% across all groups) — not a reliable signal on its own.
- **Some specific-named travel expenses are still declined** (25.8%), indicating that description specificity alone cannot guarantee approval for travel claims.
- **`ci_hardware_class = server`** shows 23.1% decline, but n=26 — limited evidence.
- Department effects (sales, HR) are weak and may be confounded with travel-heavy roles.

---

## 6. Decision-Ready Summary

| Priority | Signal | Action |
|---|---|---|
| 🔴 Critical | `processed_date` missing | Flag immediately; require date before processing |
| 🔴 Critical | `expense_purpose = travel_expense` | Route to travel-specific approval workflow |
| 🟠 High | `description_specificity = vague/generic` | Require itemized description |
| 🟠 High | `source_id` missing | Require reference number |
| 🟡 Moderate | `category = Travel` + `ci_hardware_class = Unknown` | Request CI classification |
