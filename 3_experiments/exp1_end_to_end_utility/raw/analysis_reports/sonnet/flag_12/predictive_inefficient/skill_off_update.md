---
dataset: flag_12
scenario: predictive_inefficient
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "inefficient_resolution"
query: "What signals suggest an incident resolution will be inefficient?"
source_table: augment_table/flag_12/predictive_inefficient/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:10:53.008202+00:00
wall_seconds: 54.41
---

# Incident Resolution Inefficiency Signals
**Dataset:** `sonnet__skill_off_update.csv` | **Variant:** `skill_off` | **N = 500 incidents**

## Target Definition

`above_p75_resolution = 1` indicates resolution time exceeds the 75th percentile threshold. **124 of 500 incidents (24.8%)** are flagged as inefficient. Inefficient incidents take a mean of **323 hours** vs. 131 hours for efficient ones.

---

## Key Signals

### 1. Assignee Is Slow Relative to Peer Median — Dominant Predictor

`assignee_slow_relative_to_median` is by far the strongest single signal:

| Flag Value | % Inefficient | Count |
|---|---|---|
| 0 (not slow) | 4.8% | 393 |
| 1 (slow assignee) | **98.1%** | 107 |

Nearly every inefficient case involves a slow assignee. This single flag captures the vast majority of the signal in this dataset.

### 2. Accumulation of Risk Flags

When multiple risk flags co-occur (`reassigned`, `high_complexity_category`, `critical_or_high_priority`, `assignee_slow_relative_to_median`), inefficiency compounds sharply:

| # Flags Present | % Inefficient | Count |
|---|---|---|
| 0 | 15.4% | 13 |
| 1 | 7.9% | 114 |
| 2 | 14.2% | 274 |
| 3 | **73.7%** | 95 |
| 4 | **100%** | 4 |

The jump from 2 to 3+ flags is the critical threshold.

### 3. Reassignment — Weak Independent Signal

`reassigned = 1` alone adds almost no predictive power (24.9% inefficient vs. 24.5% for non-reassigned). However, when combined with a slow assignee, inefficiency remains near-total (97.6%), confirming reassignment amplifies an already-troubled ticket rather than being a standalone cause.

### 4. Category — Moderate Signal

| Category | % Inefficient | Count |
|---|---|---|
| Inquiry / Help | 35.0% | 20 |
| Hardware | 25.6% | 406 |
| Software | 21.2% | 33 |
| Network | 18.2% | 22 |
| Database | **10.5%** | 19 |

Inquiry/Help tickets show the highest inefficiency rate. Database tickets resolve most efficiently, though sample sizes for non-Hardware categories are small.

### 5. Priority — Counterintuitive Pattern

Critical priority incidents are *less* likely to be inefficient (18.5%) than High (25.1%) or Moderate (26.0%), possibly because critical tickets receive escalated resources. Low-priority tickets (n=2) had 0% inefficiency — too small to generalize.

### 6. High-Complexity Category — Suppressor Effect

`high_complexity_category = 1` is associated with *lower* inefficiency (14.6% vs. 25.7%). This is likely a **confounding artifact**: complex categories (e.g., Database) tend to be resolved by more specialized/faster assignees. The flag should not be interpreted as protective in isolation.

---

## Exceptions and Caveats

- **`assignee_slow_relative_to_median`** dominates to such a degree that other signals are largely redundant when it is absent (only ~5% inefficient in 393 cases).
- The dataset is **heavily skewed toward Hardware** (406/500 cases), limiting generalizability of category-level findings.
- Reassignment alone is not actionable — its effect is only meaningful as a co-occurring flag.
- The `skill_off` variant suggests assignee skill/speed information may be intentionally degraded or absent in operational settings; if `assignee_slow_relative_to_median` is unavailable at ticket open time, the combination of **reassignment + category (Inquiry/Help or Hardware) + 3+ flags** becomes the next-best predictor.

---

## Decision-Ready Summary

| Signal | Strength | Actionable |
|---|---|---|
| Assignee slow relative to median | ★★★★★ | Re-assign at intake |
| 3+ risk flags co-occurring | ★★★★ | Escalate proactively |
| Inquiry/Help category | ★★ | Route to specialists |
| Reassignment (standalone) | ★ | Monitor, not triage trigger |
| High-complexity category | ✗ (suppressor) | Do not use as risk signal |
