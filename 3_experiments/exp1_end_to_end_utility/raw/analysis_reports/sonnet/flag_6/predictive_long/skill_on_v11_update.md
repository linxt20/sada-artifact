---
dataset: flag_6
scenario: predictive_long
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "resolution_time"
query: "What signals suggest an agent's tickets will take longer to resolve?"
source_table: augment_table/flag_6/predictive_long/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:19:49.792579+00:00
wall_seconds: 64.22
---

# Signals of Longer Ticket Resolution Time
**Dataset:** `sonnet__skill_on_v11_update.csv` | 500 records, 23 columns  
**Focus variable:** Resolution time (derived: `closed_at` − `opened_at`)  
**Baseline (median, valid tickets):** ~164 hours (~6.8 days)

---

## 1. Assigned Agent (Strongest Signal)

Agent assignment is the single clearest predictor of resolution time:

| Agent | Mean (hrs) | Median (hrs) | Tickets |
|---|---|---|---|
| Fred Luddy | **750** | **691** | 76 |
| Luke Wilson | 160 | 151 | 90 |
| Howard Johnson | 160 | 143 | 88 |
| Charlie Whitherspoon | 150 | 150 | 89 |
| Beth Anglin | 136 | 124 | 85 |

**Fred Luddy's tickets take ~5× longer than any other agent's.** This is consistent across both mean and median, indicating a structural pattern (workload, skill gap, or ticket routing bias) rather than outlier distortion.

---

## 2. Remote Access Context

Tickets with `remote_access_context = True` resolve significantly slower:

| Remote Access | Mean (hrs) | Median (hrs) | n |
|---|---|---|---|
| True | **263** | **176** | 109 |
| False | 212 | 140 | 369 |

The combination of **remote access + reassignment** is the worst scenario (mean ~347 hrs for remote/not-reassigned group likely reflects escalation delays).

---

## 3. Incident Category

| Incident Category | Mean (hrs) | Median (hrs) | n |
|---|---|---|---|
| software_application | **451** | 225 | 15 |
| authentication | 315 | 79 | 8 |
| vpn | **289** | 186 | 99 |
| server | 272 | 198 | 24 |
| database | 248 | 140 | 87 |

**VPN and software_application categories** are high-volume or high-mean risk factors. Authentication has a very high mean but very low median — indicating occasional extreme outliers rather than a consistent pattern (weak evidence, small n=8).

---

## 4. Symptom Type

| Symptom | Mean (hrs) | Median (hrs) | n |
|---|---|---|---|
| slow_performance | **402** | 152 | 13 |
| error_message | **327** | 128 | 27 |
| connection_failure | 236 | 163 | 199 |
| complete_outage | 196 | 143 | 101 |
| access_denied | 183 | 114 | 99 |
| crash | 51 | 42 | 6 |

`slow_performance` and `error_message` symptoms show elevated means but the median for both is moderate — the mean is skewed by a subset of long-tail tickets. These are moderate-confidence signals.

---

## 5. Priority (Weak / Counterintuitive Signal)

| Priority | Mean (hrs) | Median (hrs) | n |
|---|---|---|---|
| 1 - Critical | 188 | 131 | 84 |
| 2 - High | 230 | 152 | 364 |
| 3 - Moderate | 247 | 155 | 30 |

Lower priority tickets trend slightly longer, but differences are small. Priority is **not a reliable standalone predictor** here.

---

## 6. Ticket Opening Context (Day/Time)

- **Friday-opened tickets** have the highest median (~181 hrs), likely due to weekend delays.
- **Business-hours vs. after-hours** shows minimal median difference (158 vs. 146 hrs) — weak signal.
- **Tuesday** has the highest mean (279 hrs) but this appears driven by outliers (median: 135 hrs).

---

## Summary: Decision-Ready Signals

| Signal | Strength | Direction |
|---|---|---|
| **Assigned to Fred Luddy** | 🔴 Strong | ~5× longer |
| **Remote access = True** | 🟠 Moderate | +25–35% longer |
| **VPN / software_application category** | 🟠 Moderate | +75–175% mean increase |
| **slow_performance / error_message symptom** | 🟡 Moderate (mean-skewed) | High mean, moderate median |
| **Friday opened** | 🟡 Weak–Moderate | Slightly longer |
| **Priority (lower)** | 🟡 Weak | Marginal difference |
| **Reassignment alone** | ⚪ Negligible | Near-zero effect in isolation |

> **Key caveat:** 22 tickets had negative resolution times (data quality issue) and were excluded. The `ticket_open_status` column had no variation in valid records (all `False`), so it provides no predictive value.
