---
dataset: flag_13
scenario: eda_duration
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_duration"
query: "How does resolution duration vary across incident category and priority?"
source_table: augment_table/flag_13/eda_duration/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:11:40.310557+00:00
wall_seconds: 43.04
---

# Resolution Duration Analysis: Incident Category × Priority

**Dataset:** 500 incidents | **Focus variable:** `resolution_hours`

---

## 1. Overall Summary

| Dimension | Range of Medians (hrs) | Key observation |
|---|---|---|
| By Category | 28.6 – 33.5 | Moderate spread; Software highest |
| By Priority | 25.0 – 32.0 | Critical slightly longer than High |

Differences across both dimensions are present but modest — no category or priority tier shows dramatically faster or slower resolution in isolation.

---

## 2. Resolution Duration by Category

| Category | Median (hrs) | Mean (hrs) | Count |
|---|---|---|---|
| Software | **33.45** | 31.55 | 73 |
| Hardware | 32.00 | 30.79 | 25 |
| Database | 29.67 | 29.16 | 134 |
| Network | 29.66 | 30.08 | 260 |
| Inquiry / Help | **28.65** | 28.04 | 8 |

- **Software** takes the longest (median ~33 hrs), likely reflecting diagnostic complexity.
- **Network** and **Database** are close to the dataset average (~29–30 hrs) and together account for ~79% of tickets.
- **Inquiry / Help** resolves fastest, but its sample (n=8) is too small for reliable conclusions.

---

## 3. Resolution Duration by Priority

| Priority | Median (hrs) | Mean (hrs) | Count |
|---|---|---|---|
| 1 - Critical | 32.00 | 30.35 | 83 |
| 2 - High | 29.65 | 29.93 | 391 |
| 3 - Moderate | 29.20 | 31.45 | 24 |
| 4 - Low | 25.00 | 25.00 | 2 |

- Counterintuitively, **Critical** incidents have a *longer* median duration than **High**, not shorter — suggesting urgency does not translate to faster closure in this dataset.
- **4 - Low** appears fastest (median 25 hrs), but n=2 makes this unreliable.
- Duration bands (short / medium / long) distribute similarly across priority tiers, confirming no strong priority-driven compression of resolution time.

---

## 4. Interaction: Category × Priority (Median Resolution Hours)

| Category | 1 - Critical | 2 - High | 3 - Moderate |
|---|---|---|---|
| Software | **38.00** | 24.37 | **43.39** |
| Hardware | 35.25 | **37.01** | 23.92 |
| Database | 34.49 | 28.28 | 33.70 |
| Network | 23.81 | 30.53 | 24.84 |
| Inquiry / Help | 25.67 | 31.63 | — |

Key patterns:
- **Software × Critical** (38.0 hrs) and **Software × Moderate** (43.4 hrs) are the slowest combinations, pointing to Software as the main duration risk regardless of priority label.
- **Hardware × High** (37.0 hrs) is also notably elevated.
- **Network × Critical** (23.8 hrs) is one of the *fastest* critical combinations — opposite of what urgency scaling would predict.
- The interaction effect between category and priority is more meaningful than either variable alone.

---

## 5. Conclusions & Caveats

- **Category drives duration more than priority**: Software and Hardware incidents consistently show longer resolution times.
- **Priority escalation does not reliably reduce resolution hours** — Critical tickets are not resolved faster than High tickets.
- The `duration_vs_category_median` and `duration_vs_priority_median` engineered columns confirm within-group deviation but do not change the overall ordering.
- Several cells in the cross-tab have small or missing counts (Hardware × Low, Inquiry / Help × Moderate), so those figures should be treated with caution.
