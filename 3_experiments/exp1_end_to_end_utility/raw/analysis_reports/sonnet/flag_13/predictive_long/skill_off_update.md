---
dataset: flag_13
scenario: predictive_long
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "duration_like_resolution_value"
query: "What signals are linked to longer resolution duration values?"
source_table: augment_table/flag_13/predictive_long/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:12:48.945855+00:00
wall_seconds: 62.71
---

# Signals Linked to Longer Resolution Duration

## Dataset Overview

The dataset contains **500 IT incidents** with `resolution_duration_seconds` as the primary metric, binned into four tiers: `short` (n=77, mean ~318s), `medium` (n=173, mean ~1,206s), `long` (n=175, mean ~2,404s), and `very_long` (n=75, mean ~3,299s). The analysis targets signals associated with `long` + `very_long` outcomes (~50% of all tickets).

---

## Key Signals

### 1. Off-Hours Ticket Opening (`is_off_hours_open`)

The strongest single binary signal is whether a ticket was opened outside normal hours:

| `is_off_hours_open` | Long/Very Long Rate | Mean Duration (s) |
|---------------------|--------------------|--------------------|
| 0 (business hours)  | 42.6%              | 1,718              |
| 1 (off hours)       | **53.6%**          | **1,843**          |

Tickets opened off-hours are ~11 percentage points more likely to have long resolution times, and average ~125s longer. This is the most consistent signal in the data.

### 2. Assigned Agent (`assigned_to`)

Agent identity shows a notable spread in long-resolution rates:

| Assignee              | Long/Very Long Rate | Mean Duration (s) |
|-----------------------|--------------------|--------------------|
| Charlie Whitherspoon  | **56.0%**          | **1,866**          |
| Fred Luddy            | 52.7%              | 1,841              |
| Luke Wilson           | 50.0%              | 1,828              |
| Beth Anglin           | 47.0%              | 1,755              |
| Howard Johnson        | **44.6%**          | **1,727**          |

Charlie Whitherspoon and Fred Luddy are disproportionately associated with longer outcomes (~10+ pp above Howard Johnson). The `assignee_avg_resolution_seconds` engineered feature has a small but positive correlation (r = 0.052) with actual duration, consistent with this pattern.

### 3. Category (`category`)

Software and Hardware tickets tend toward longer durations:

| Category       | Long/Very Long Rate | Mean Duration (s) |
|----------------|--------------------|--------------------|
| Hardware       | **52.0%**          | **1,847**          |
| Software       | 50.7%              | 1,892              |
| Inquiry / Help | 50.0%              | 1,682              |
| Network        | 50.0%              | 1,804              |
| Database       | 49.3%              | 1,750              |

Differences across categories are modest (~3pp in long-rate). Software has the highest mean duration in seconds but is a relatively small category (n=73).

### 4. Priority (`priority`)

Counterintuitively, `1 - Critical` tickets do **not** show substantially higher long-resolution rates than `2 - High` tickets (51.8% vs. 49.9%). `3 - Moderate` tickets actually have a slightly lower long-resolution rate (45.8%). The correlation between `priority_numeric` and duration is near zero (r = –0.003), making priority a weak predictor here.

### 5. Opening Hour (Time of Day)

Afternoon-opened tickets (12–18h) have a slightly higher long rate (52.1%, mean 1,866s) compared to morning-opened tickets (44.9%, mean 1,769s). However, the differences are small and may be partially driven by the off-hours variable.

---

## Summary of Signal Strength

| Signal                    | Direction         | Long/VL Rate Gap | Correlation (r) |
|---------------------------|-------------------|-----------------|-----------------|
| `is_off_hours_open`       | Off-hours → longer | +11 pp          | 0.058           |
| `assigned_to`             | Charlie/Fred → longer | ~11 pp spread | 0.052 (avg feature) |
| `category`                | Software/Hardware → longer | ~3 pp  | 0.047 (cat avg feature) |
| `priority`                | Negligible         | ~2 pp            | –0.003          |
| `is_high_severity`        | Negligible         | ~4 pp            | –0.013          |

---

## Caveats

- **All correlations are weak** (all |r| < 0.06). No single feature strongly predicts long resolution.
- The near-uniform distribution across tiers (~50% are long/very_long) suggests the dataset may have limited discriminative variance, or that the dominant factors are unobserved (e.g., ticket complexity, customer responsiveness).
- Priority shows essentially no predictive signal — escalation classification in this dataset does not reliably translate to faster resolution.
- Category differences are small with overlapping confidence intervals given sample sizes.
