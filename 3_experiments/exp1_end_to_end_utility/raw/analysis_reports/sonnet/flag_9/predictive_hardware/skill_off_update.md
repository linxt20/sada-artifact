---
dataset: flag_9
scenario: predictive_hardware
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "is_hardware_anomaly_window"
query: "What signals indicate a hardware incident is in the anomaly window?"
source_table: augment_table/flag_9/predictive_hardware/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:23:17.948932+00:00
wall_seconds: 42.85
---

# Hardware Anomaly Window Signal Analysis

**Dataset:** `sonnet__skill_off_update.csv` | 600 total incidents, 182 hardware incidents, **12 in the anomaly window** (`hw_anomaly_window = 1`)

---

## Key Finding: The Dominant Signal

The single strongest indicator of an anomaly window incident is **`hw_incidents_last_7d`** — the count of hardware incidents in the preceding 7 days.

| Metric | Anomaly Window (n=12) | Non-Anomaly (n=170) |
|---|---|---|
| `hw_incidents_last_7d` mean | **26.5** | 10.6 |
| `hw_incidents_last_7d` min | **26** | 1 |
| `hw_incidents_last_7d` max | **28** | 25 |

All 12 anomaly-window incidents fall in a tight band of **26–28 hardware incidents in the prior 7 days**, while no non-anomaly incident exceeds 25. This creates a clean, near-perfect threshold: **`hw_incidents_last_7d ≥ 26` → anomaly window**.

All 12 anomaly incidents cluster in a single burst period: **2023-08-06 to 2023-08-11**, confirming temporal concentration.

---

## Supporting Signals

### `hw_resolution_zscore`
The anomaly-window incidents show a narrower Z-score distribution (mean ≈ 0.01, std ≈ 0.72) compared to non-anomaly incidents (std ≈ 1.02), but the distributions overlap substantially. This column is **not a reliable standalone discriminator** — it captures relative resolution time deviation within hardware incidents, not the surge itself.

### `resolution_hours`
- Anomaly mean: **175 hrs** | Non-anomaly mean: **174 hrs**
- Essentially identical. Resolution time alone does **not** signal anomaly window membership.

### `priority_score` / `priority`
- Anomaly incidents: all priority 2–3 (no 1-Critical)
- Non-anomaly: includes 16 priority-1 incidents
- The absence of Critical-priority tickets during the anomaly window is notable but likely reflects the specific incident types (monitor flicker, keyboard, printer) rather than a causal rule. **Priority is not a useful signal.**

---

## Anomaly Window Incident Profile

The 12 anomaly incidents are characterized by:
- **Category:** Hardware (required — `is_hardware = 1`)
- **Device types:** Monitors, printers, keyboards, desktop computers, hard drives, laptops
- **Timing:** All opened 2023-08-06 to 2023-08-11 (a 5-day cluster)
- **Priority:** 2-High (9) or 3-Moderate (3)
- **`hw_incidents_last_7d`:** 26–28

---

## Exceptions and Caveats

- The anomaly window is **extremely rare** (12/600 = 2% of all rows; 6.6% of hardware rows), making any pattern susceptible to small-sample noise.
- `hw_resolution_zscore` is blank for non-hardware incidents and shows no discriminating power within the anomaly set.
- The threshold of 26 appears sharp in this dataset, but its generalizability depends on baseline hardware incident volume — it may represent a dataset-specific artifact rather than a universal rule.
- No categorical column (assigned agent, caller, assignment group) shows consistent anomaly-window association.

---

## Decision Rule (Data-Grounded)

> A hardware incident (`is_hardware = 1`) is in the anomaly window when **`hw_incidents_last_7d ≥ 26`**.

This threshold achieves perfect separation in the observed data. All other available signals (resolution time, priority, Z-score) do not materially add discriminating power.
