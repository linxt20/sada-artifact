---
dataset: flag_13
scenario: causal_duration
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "resolution_duration_variation"
query: "Why do resolution duration values vary across tickets?"
source_table: augment_table/flag_13/causal_duration/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:14:08.520085+00:00
wall_seconds: 53.15
---

# Resolution Duration Variance Analysis — Skill-On Variant

## Dataset Overview
- **500 tickets** with resolution durations ranging from **~0.2 to ~60 minutes** (mean: 30.1 min, std: 16.8 min).
- The duration distribution is strikingly **near-uniform** across six 10-minute bins (73–91 tickets each), suggesting broad natural spread rather than tight clustering around a single driver.

---

## Factors and Their Observed Effects

### 1. Incident Category / Failure Mode
Mean durations by `incident_category` range from **28.5 min** (generic "other") to **32.9 min** (server infrastructure). Differences are modest (~4 min spread). `failure_mode` shows a wider gap: **performance_degradation** resolves fastest at ~23.7 min, while **connectivity_failure** averages ~31.3 min. This suggests that failure type has a weak but visible influence—connectivity issues tend to take longer, possibly due to multi-step diagnosis.

| Failure Mode | Mean Duration (min) | Count |
|---|---|---|
| performance_degradation | 23.7 | 11 |
| other | 27.7 | 46 |
| no_response | 28.6 | 44 |
| access_denied_login | 29.7 | 116 |
| full_outage | 30.0 | 43 |
| connectivity_failure | 31.3 | 229 |

### 2. Affected Scope
`location_specific` tickets average **33.6 min** vs. **29.6 min** for individual-scope and **30.1 min** for system-wide. The "printing" subcategory within location-specific is notable—mostly on-site hardware issues (avg. ~44.6 min for `location_specific` printing) that likely require physical dispatch, explaining elevated duration.

### 3. Priority
Priority shows **negligible impact** on duration: 1-Critical (~30.4 min) vs. 2-High (~29.9 min) vs. 3-Moderate (~31.5 min). Priority alone does not predict how long resolution takes in this dataset.

### 4. Assigned Agent (Skill)
This variant focuses on agent/skill assignment (`resolver_match`). Agent-level means are tightly clustered: Howard Johnson (28.8 min) through Charlie Whitherspoon (31.1 min)—only a **~2.3 min spread** across all agents with similar standard deviations (~16–17 min). `resolver_match` (True vs. False) shows essentially no difference (30.0 vs. 30.2 min). **Skill/agent matching does not meaningfully differentiate resolution speed** in this dataset.

### 5. Time of Day
`open_hour_of_day` contributes marginally: afternoon tickets resolve slightly faster (~29.3 min) versus early morning (~30.7 min). The effect is small and unlikely to be practically significant.

### 6. Caller Type & Repeat Incidents
`itil_user` callers average 29.5 min vs. 30.2 min for named users—minimal difference. Repeat/cluster incidents (True: 30.0 min) vs. non-repeat (False: 30.7 min) also show negligible variation.

---

## Primary Explanation of Duration Variance

The near-uniform distribution and consistently high within-group standard deviations (~16–17 min regardless of grouping) indicate that **resolution duration is largely driven by case-specific complexity and idiosyncratic circumstances not fully captured by the available categorical columns**. The strongest observable structural factors are:

1. **Failure mode type** — connectivity failures take longer than performance issues.
2. **Affected scope** — location-specific (often hardware/printing) incidents are slower.
3. **Incident category** — server infrastructure tickets trend longer.

All other factors (agent skill match, priority, caller type, time of day) contribute at most 1–3 minutes of mean difference—well within noise given the ~17-minute standard deviation.

---

## Exceptions and Caveats
- The `resolver_match = True` group with `3 - Moderate` priority shows a mean of ~38.9 min, but this cell contains only **a small number of tickets** and is likely an outlier artifact.
- `4 - Low` priority has only 2 tickets—too sparse for conclusions.
- Duration values appear to be capped/truncated at 60 minutes; the near-uniform spread may partly reflect data generation constraints rather than purely operational patterns.
- No single factor explains more than a few percentage points of variance; multi-factor interaction effects or unmeasured variables (e.g., ticket complexity, queue depth) are likely the primary drivers.
