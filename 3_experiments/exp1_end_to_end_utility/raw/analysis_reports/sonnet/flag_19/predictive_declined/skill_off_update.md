---
dataset: flag_19
scenario: predictive_declined
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "state_declined"
query: "What signals suggest an expense will be declined?"
source_table: augment_table/flag_19/predictive_declined/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:14:40.629038+00:00
wall_seconds: 47.78
---

# Signals of Expense Decline: Analysis Report

**Dataset:** `sonnet__skill_off_update.csv` (500 expenses) | **Focus variable:** `state = Declined` (n=46)

---

## Key Signals

### 1. Missing `processed_date` — Perfect Discriminator
Every single Declined expense (46/46, **100%**) has `missing_processed_date = 1`, compared to 0% of Processed expenses. This is the single strongest signal of a decline. No expense lacking a processed date was ever marked Processed.

### 2. High `decline_risk_score` — Strong Predictor
Declined expenses cluster heavily at scores 3–4 (60.9% of Declined have score ≥ 3), while only 2.1% of Processed expenses reach this threshold.

| State | Mean Score | % with Score ≥ 3 |
|---|---|---|
| Declined | 2.41 | **60.9%** |
| Pending | 1.61 | 21.2% |
| Submitted | 1.61 | 24.4% |
| Processed | 0.47 | 2.1% |

Score 4 (maximum) appears **only** among Declined and Pending cases — never in Processed. All score-4 records have all four risk flags simultaneously set.

### 3. `high_risk_dept_category` — Elevated in Declined
67.4% of Declined expenses are flagged as high-risk department/category combinations, vs. 20.7% in Processed. IT department + Assets category is the most common combination among declined records (IT: 19 of 46 declined).

### 4. `high_risk_user` — Meaningful Lift
45.7% of Declined expenses involve a flagged high-risk user, compared to only 6.0% among Processed. This nearly 8× gap makes it a meaningful secondary signal.

### 5. `missing_source_id` — Weak Signal
28.3% of Declined expenses have a missing source ID, vs. 19.8% for Processed. The gap is real but modest; missing source ID alone is insufficient to predict decline.

### 6. Amount — Not a Distinguishing Factor
Mean amounts are similar across states (Declined: $3,706 vs. Processed: $4,436), indicating expense size has little predictive value.

---

## Risk Factor Combinations

The `decline_risk_score` effectively accumulates the above binary flags. The pattern is consistent:

- **Score = 4** → Almost certainly declined or still pending (never Processed)  
- **Score = 3** → 24 of 46 Declined records; 7 Processed records reached score 3 (exceptions exist)  
- **Missing processed_date alone** → Necessary but not sufficient (Pending/Submitted also lack it)

---

## Exceptions / Weak Evidence

- **13 Declined expenses have score = 1**: decline is not limited to multi-flag cases; even single-flag records (typically missing processed date only) can be declined.
- **Pending and Submitted also lack processed dates**: the `missing_processed_date` flag alone does not distinguish Declined from Pending/Submitted — the `high_risk_dept_category` and `high_risk_user` flags differentiate them further.
- **No category is immune**: Assets, Travel, and Services all appear among declined records, though Assets is most common (27/46).

---

## Decision-Ready Summary

| Signal | Strength | Notes |
|---|---|---|
| `missing_processed_date = 1` | ★★★★★ | Present in 100% of declines |
| `decline_risk_score ≥ 3` | ★★★★☆ | 61% of declines; rare in Processed |
| `high_risk_dept_category = 1` | ★★★☆☆ | 67% of declines; elevates risk |
| `high_risk_user = 1` | ★★★☆☆ | 46% of declines; strong lift |
| `missing_source_id = 1` | ★☆☆☆☆ | Weak marginal signal |
| High `amount` | ✗ | Not predictive |

**Highest-risk profile:** an expense with a missing processed date, a high-risk department/category combination, a flagged user, and a missing source ID (score = 4) is almost certain to be declined.
