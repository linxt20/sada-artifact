---
dataset: flag_20
scenario: eda_declined
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "state_declined"
query: "What signals in a travel-expense description predict whether it will be declined?"
source_table: augment_table/flag_20/eda_declined/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:17:46.194516+00:00
wall_seconds: 60.7
---

# Signals Predicting Declined Travel-Expense Descriptions

## Dataset Overview

- **500 records**, 84 declined (16.8% overall decline rate)
- Key engineered signals: `has_travel_keyword`, `has_expense_keyword`, `has_equipment_keyword`, `has_auto_generated_language`, `is_travel_category`, `travel_expense_signal` (composite), `amount_tier`, `desc_word_count`

---

## Strongest Predictors of Decline

### 1. `travel_expense_signal` / `has_travel_keyword` / `is_travel_category`

These three flags are closely co-linear and represent the dominant predictor:

| Signal value | Decline rate | n |
|---|---|---|
| `travel_expense_signal = 0` | **6.7%** | 359 |
| `travel_expense_signal = 1` | **42.6%** | 141 |
| `is_travel_category = 0` | 6.5% | 354 |
| `is_travel_category = 1` | 41.8% | 146 |

**Presence of travel-related language (e.g., "travel equipment," "travel-related hardware," "travel gear") in the description is the single strongest predictor of decline.** Records without any travel keyword have a ~7% decline rate; records with it face a ~43% decline rate — a 6× increase.

### 2. `has_expense_keyword`

| Value | Decline rate | n |
|---|---|---|
| 0 | 13.1% | 435 |
| 1 | **41.5%** | 65 |

Descriptions containing explicit expense terminology ("expense," "cost," "rental cost") independently elevate decline likelihood to ~42%.

### 3. `has_equipment_keyword`

| Value | Decline rate | n |
|---|---|---|
| 0 | 13.9% | 440 |
| 1 | **38.3%** | 60 |

References to equipment (especially in combination with travel keywords) are strongly associated with decline.

---

## Secondary Factors

### 4. `amount_tier` (interacts with travel signal)

| travel_expense_signal | amount_tier | Decline rate |
|---|---|---|
| 1 | low | **80.0%** |
| 1 | medium | 41.8% |
| 1 | high | 36.5% |
| 0 | any | 3–8% |

Low-dollar amounts on travel-flagged descriptions are declined at an extreme rate (80%), suggesting small travel expenses are treated with high scrutiny. Paradoxically, higher amounts without travel signals are rarely declined — the travel framing matters more than the amount alone.

### 5. `has_auto_generated_language`

| Value | Decline rate | n |
|---|---|---|
| 0 | 15.2% | 349 |
| 1 | **20.5%** | 151 |

Auto-generated language ("Automatically generated expense line for…") raises decline risk modestly (+5 pp). Among declined records, 31/84 (37%) had auto-generated phrasing, but this signal is weaker in isolation.

### 6. Category

| Category | Decline rate |
|---|---|
| Travel | **41.8%** |
| Services | 10.6% |
| Assets | 6.0% |
| Miscellaneous | 3.8% |

The **Travel category** drives nearly all declines. Non-travel categories are rarely declined.

### 7. Department

HR (20%), Sales (18%), and Customer Support (18%) have higher decline rates than Finance (6%) or Development (0%). Development had zero declined records. However, this may reflect underlying category/travel-signal distributions rather than department policy.

---

## Description Language Patterns

Reviewing declined `short_description` text reveals recurring phrases:

- "Travel-related hardware asset"
- "Automated record for travel equipment asset"
- "Travel gear – asset generation"
- "Rental cost for travel equipment"
- "Expense for business travel equipment"

Common structure: **[auto-generated / expense / rental] + [travel] + [equipment / hardware / asset]**. The combination of travel terminology with asset/equipment framing and expense language appears to trigger policy-based declines consistently.

---

## Exceptions & Weak Evidence

- **`desc_word_count`** shows negligible difference between declined (5.5 words) and non-declined (5.8 words) — description length is not predictive.
- **`amount` (raw)**: Declined records actually have a *lower* mean amount (≈$3,912) vs. processed (≈$4,284). High-amount records are not disproportionately declined; the travel signal dominates.
- **141 records with `travel_expense_signal = 1`** are not all declined (57% are not), meaning travel language alone is not sufficient — policy or case-by-case review plays a role.
- **`has_auto_generated_language`** is a weak standalone signal; its elevated decline rate mostly reflects its overlap with travel-flagged records.

---

## Summary: Decision-Ready Signals

| Priority | Signal | Effect |
|---|---|---|
| **1 (strongest)** | Travel keyword / `is_travel_category` | ~43% decline rate vs. 7% baseline |
| **2** | Expense keyword in description | ~42% decline rate |
| **3** | Equipment keyword in description | ~38% decline rate |
| **4 (interaction)** | Travel signal + low amount | 80% decline rate |
| **5 (weak)** | Auto-generated language | Modest +5 pp lift |

> **Actionable rule**: A description flagged with travel terminology (`travel_expense_signal = 1`), especially when combined with expense/equipment keywords and a low dollar amount, is at very high risk of being declined. Non-travel, non-equipment descriptions face a ~7% baseline decline rate regardless of other factors.
