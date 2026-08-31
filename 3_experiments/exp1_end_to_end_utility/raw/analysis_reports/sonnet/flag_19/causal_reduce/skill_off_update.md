---
dataset: flag_19
scenario: causal_reduce
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "state_declined"
query: "How can we reduce declined expense submissions?"
source_table: augment_table/flag_19/causal_reduce/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:13:20.305654+00:00
wall_seconds: 42.46
---

# Reducing Declined Expense Submissions

## Dataset Overview
- **Total records:** 500 expense submissions
- **Declined:** 46 (9.2%), Processed: 333 (66.6%), Pending: 80, Submitted: 41

---

## Key Findings

### 1. IT Department Is the Primary Problem Area
The IT department has a **44.2% decline rate** (19 of 43 submissions), far exceeding any other department:

| Department | Total | Declined | Decline Rate |
|---|---|---|---|
| IT | 43 | 19 | **44.2%** |
| HR | 14 | 2 | 14.3% |
| Finance | 22 | 2 | 9.1% |
| Customer Support | 267 | 16 | 6.0% |
| Sales | 122 | 6 | 4.9% |
| Development | 20 | 1 | 5.0% |
| Product Management | 12 | 0 | 0.0% |

The `department_decline_rate` column confirms this: declined submissions average **0.221** vs. **0.079** for non-declined ones, driven almost entirely by IT.

### 2. High-Risk Individual Users Concentrate in IT
The top-declined users are concentrated in IT and exhibit persistently high `user_decline_rate` values:

| User | Declined Submissions | User Decline Rate | Department |
|---|---|---|---|
| Vernon Engelman | 7 | 0.54 | IT |
| Helene Iberg | 7 | 0.41 | IT |
| Sadie Rowlett | 2 | 0.40 | IT |
| Virgil Chinni | 2 | 0.40 | IT |

Average `user_decline_rate` for declined submissions: **0.273** vs. **0.074** for non-declined — a ~3.7× difference, making this the strongest individual-level predictor.

### 3. Missing Source IDs Slightly Elevate Decline Risk
Declined submissions have a higher rate of missing `source_id` (**28.3%** missing) compared to non-declined (**21.6%** missing). While not the primary driver, incomplete documentation contributes.

### 4. Expense Category Has Minimal Impact
The category mix between Declined and Processed submissions is nearly identical (Assets ~58–64%, Travel ~17–22%), so category alone does not drive declines. `category_decline_rate` shows negligible difference (0.096 declined vs. 0.092 not declined).

### 5. Amount Bracket Is Not a Strong Predictor
Declined submissions are slightly skewed toward Low and Medium amounts, but the difference is modest and inconsistent with a clear causal pattern.

---

## Recommendations

1. **Audit IT department submission processes** — With a 44% decline rate, IT likely has systemic policy, approval-chain, or documentation issues. Targeted training or process review for IT is the highest-ROI intervention.
2. **Focus on repeat-decline users** — Users with `user_decline_rate > 0.30` (Vernon Engelman, Helene Iberg, Sadie Rowlett, Virgil Chinni) account for a disproportionate share of declines. Direct coaching or pre-submission review for these individuals could immediately reduce declined volume.
3. **Enforce source ID completeness** — Making `source_id` mandatory at submission time would reduce a known gap, though this is a secondary factor.
4. **No action needed on category or amount** — These factors show weak or no independent effect on decline probability.

---

## Caveats
- The dataset does not include decline reasons, so the exact cause of IT's elevated rate (policy violations, budget overruns, missing approvals) cannot be confirmed from this data alone.
- `user_decline_rate` and `department_decline_rate` appear to be pre-computed features, which may encode historical patterns rather than strictly causal relationships.
