---
dataset: flag_13
scenario: eda_duration
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: exploratory_data_analysis
focus_variable: "resolution_duration"
query: "How does resolution duration vary across incident category and priority?"
source_table: augment_table/flag_13/eda_duration/original.csv
generated_at: 2026-07-26T13:17:50.556903+00:00
wall_seconds: 69.84
---

# Resolution Duration Analysis by Incident Category and Priority

## Dataset Overview

- **Total incidents:** 500
- **Duration metric:** `sys_updated_on` field encodes resolution duration in `MM:SS.s` format (minutes and seconds)
- **Incident categories:** Database, Hardware, Inquiry / Help, Network, Software
- **Priority levels:** 1 - Critical, 2 - High, 3 - Moderate, 4 - Low

---

## Duration by Incident Category

| Category       | Count | Mean (min) | Median (min) | Min (min) | Max (min) |
|----------------|-------|-----------|--------------|-----------|-----------|
| Database       | 134   | 29.2      | 29.7         | 0.2       | 60.0      |
| Hardware       | 25    | 30.8      | 32.0         | 6.3       | 58.2      |
| Inquiry / Help | 8     | 28.0      | 28.6         | 4.6       | 45.1      |
| Network        | 260   | 30.1      | 29.7         | 0.4       | 59.4      |
| Software       | 73    | 31.5      | 33.5         | 2.3       | 59.2      |

**Key observation:** Category means are tightly clustered between ~28–32 minutes. Software incidents have the highest mean (31.5 min) and median (33.5 min), while Inquiry / Help is slightly fastest (28.0 min mean). Differences across categories are modest; no single category stands out as dramatically faster or slower. Database and Network dominate volume (53% and 26% of all tickets, respectively).

---

## Duration by Priority

| Priority     | Count | Mean (min) | Median (min) | Min (min) | Max (min) |
|--------------|-------|-----------|--------------|-----------|-----------|
| 1 - Critical | 83    | 30.3      | 32.0         | 0.4       | 57.9      |
| 2 - High     | 391   | 29.9      | 29.6         | 0.2       | 60.0      |
| 3 - Moderate | 24    | 31.5      | 29.2         | 5.1       | 58.9      |
| 4 - Low      | 2     | 25.0      | 25.0         | 20.0      | 30.0      |

**Key observation:** Priority has negligible effect on mean resolution duration (~30 min across all levels). Critically, 1 - Critical incidents are **not resolved faster** than lower-priority ones (mean 30.3 min vs. 29.9 min for High). Priority 4 - Low shows the shortest mean (25.0 min), but with only 2 records, this is statistically unreliable.

---

## Duration by Category × Priority (Mean Minutes)

| Category       | 1 - Critical (n) | 2 - High (n) | 3 - Moderate (n) | 4 - Low (n) |
|----------------|------------------|--------------|------------------|-------------|
| Database       | 31.8 (19)        | 28.6 (110)   | 32.8 (4)         | 30.0 (1)    |
| Hardware       | 34.7 (6)         | 32.7 (14)    | 20.7 (5)         | —           |
| Inquiry / Help | 25.7 (1)         | 28.4 (7)     | —                | —           |
| Network        | 28.1 (48)        | 30.6 (206)   | 27.7 (6)         | —           |
| Software       | 37.1 (9)         | 29.5 (54)    | 39.3 (9)         | 20.0 (1)    |

**Notable cross-tab patterns:**

- **Software × Critical (37.1 min)** and **Software × Moderate (39.3 min)** are among the longest durations, suggesting software issues at non-High priority consume more resolution time — though sample sizes are small (n=9 each).
- **Hardware × Critical (34.7 min)** is notably longer than **Hardware × Moderate (20.7 min)**, indicating more severe hardware incidents may require more effort, though again small samples limit confidence.
- **Network × Critical (28.1 min)** is *shorter* than **Network × High (30.6 min)**, a counter-intuitive pattern that may indicate Critical network outages receive faster response (or the difference is noise).
- **Database × High (28.6 min)** is slightly lower than other Database priority cells, driven by the large volume (n=110) stabilizing the mean.

---

## Summary & Caveats

1. **Overall, resolution durations are broadly uniform (~29–32 min)** across both category and priority dimensions, suggesting that neither category nor priority is a strong differentiator of resolution speed in this dataset.
2. **Priority escalation does not reduce resolution time** — Critical incidents resolve at essentially the same rate as High ones.
3. **Software incidents trend slightly longer** across multiple priority levels, potentially indicating inherently more complex resolution steps.
4. **Most cross-tab cells for Moderate and Low priorities are small (n < 10)**, so observed differences there should be treated with caution and not used for firm decisions without more data.
5. The duration field is encoded in `MM:SS.s` format in `sys_updated_on`; this interpretation assumes that field represents elapsed resolution time. The `closed_at` field contains identical values, supporting this interpretation.
