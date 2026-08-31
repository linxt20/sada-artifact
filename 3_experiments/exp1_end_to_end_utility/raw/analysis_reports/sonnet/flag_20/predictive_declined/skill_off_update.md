---
dataset: flag_20
scenario: predictive_declined
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "state_declined"
query: "What signals suggest a travel expense will be declined?"
source_table: augment_table/flag_20/predictive_declined/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:18:17.634948+00:00
wall_seconds: 49.3
---

# Signals Suggesting a Travel Expense Will Be Declined

**Dataset:** 500 expense records; 146 are Travel category (61 Declined, 52 Processed, 18 Pending, 15 Submitted).

---

## Key Signals

### 1. Missing Processed Date (`no_processed_date = 1`) — Strongest Signal
Every single declined Travel expense (61/61, **100%**) has no processed date, versus 0% of Processed travel expenses. This is the single most discriminating binary flag in the dataset.

### 2. Missing Source ID (`missing_source_id = 1`) — Near-Perfect Co-Indicator
All 61 declined travel records also carry `missing_source_id = 1`. Because this co-occurs perfectly with `no_processed_date` among declined records, the **combination of both flags missing is a near-certain decline marker** for travel expenses.

### 3. High `decline_risk_score` — Clear Separation
| State | Mean Score |
|---|---|
| Declined | **3.51** |
| Processed | **1.24** |

Declined travel scores cluster between 3.0–4.5, while processed travel scores cluster at 1.0–1.5. A score ≥ 3.0 appears to be the practical threshold for high decline risk.

### 4. Elevated `user_prior_decline_rate` — Moderate Signal
Users whose travel claims were declined had a prior decline rate of **25.1%** on average, compared to **14.9%** for processed claims. This indicates submitter history is a meaningful secondary signal.

### 5. `high_decline_dept = 1` — Weak Differentiator
60/61 (98.4%) of declined travel records flag `high_decline_dept`, but so do 45/52 (86.5%) of processed ones. This flag alone is not sufficient to predict decline for travel expenses, though its absence is a mild positive signal.

### 6. Amount — Not a Reliable Signal
Declined travel expenses averaged **$3,793** vs. **$3,928** for processed — negligible difference. Neither `amount_above_travel_median` nor `amount_below_dept_median` shows meaningful separation.

### 7. `submitted_off_hours` — Counterintuitive
Declined claims were *less* likely to have been submitted off-hours (47.5%) than processed claims (63.5%), suggesting off-hours submission does not predict decline in the travel category.

---

## Summary Decision Rules

| Signal | Declined Rate Impact |
|---|---|
| `no_processed_date = 1` | **Necessary condition** — all declines |
| `missing_source_id = 1` | Co-occurs with all declines |
| `decline_risk_score ≥ 3.0` | Present in **100%** of declines, **0%** of processed |
| `user_prior_decline_rate > 0.20` | Elevated in ~50% of declines |
| `high_decline_dept` | Weak marginal signal |

**Decision-ready rule:** A travel expense is very likely to be declined if it has **no processed date AND no source ID** (yielding a risk score ≥ 3.0). User prior decline rate above ~20% reinforces this prediction but is not independently decisive.

---

## Exceptions and Caveats
- A small number of Travel records flagged with `no_processed_date = 1` appear in Pending/Submitted states — their outcome is not yet determined, so the signal may generalize to those.
- The `high_decline_dept` flag is near-universal for travel expenses regardless of outcome, limiting its standalone utility.
- Non-travel categories (Assets, Services) show different decline patterns; these findings are specific to **category = Travel**.
