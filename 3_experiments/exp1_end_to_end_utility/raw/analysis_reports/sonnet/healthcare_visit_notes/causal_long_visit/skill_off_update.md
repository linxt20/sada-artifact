---
dataset: healthcare_visit_notes
scenario: causal_long_visit
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "visit_duration_min"
query: "Which clinical factors best explain longer visit durations?"
source_table: augment_table/healthcare_visit_notes/causal_long_visit/sonnet__skill_off_update.csv
generated_at: 2026-07-28T12:40:56.784396+00:00
wall_seconds: 57.13
---

# Clinical Factors Explaining Longer Visit Durations

**Dataset:** 250 visit records across 6 departments  
**Focus variable:** `visit_duration_min` (range: 15–60 min; mean: 25.4 min; median: 25 min; 90th pct: 35 min)

---

## Key Findings

### 1. Emergency Urgency / Emergency Department — Strongest Driver

Emergency visits are by far the dominant predictor of long duration:

| Urgency / Department | Mean Duration (min) | N |
|---|---|---|
| Emergency | 45.5 | 28 |
| Urgent | 23.2 | 81 |
| Routine | 22.6 | 141 |

Of the 27 visits ≥ 35 min (top ~10%), **26 are Emergency department visits** and 26 are classified as Emergency urgency. The Emergency department average (45.5 min) is nearly **double** that of the next highest department (Cardiology, 30.1 min). Urgency and department are effectively co-linear here (all Emergency-urgency visits map to the Emergency department).

---

### 2. Procedure Performed — Moderate Independent Effect

| Procedure Performed | Mean Duration (min) | N |
|---|---|---|
| Yes (1) | 31.3 | 80 |
| No (0) | 22.6 | 170 |

This is the **strongest numeric-column correlation** with visit duration (r = 0.45). Visits with a procedure are ~8.7 min longer on average. Among the 27 long visits (≥35 min), 74% involved a procedure vs. 32% overall.

---

### 3. Department (Excluding Emergency) — Secondary Factor

| Department | Mean Duration (min) | N |
|---|---|---|
| Cardiology | 30.1 | 42 |
| Orthopedics | 25.9 | 39 |
| General Practice | 21.9 | 54 |
| Pediatrics | 19.9 | 45 |
| Dermatology | 17.0 | 42 |

Even within non-emergency visits, Cardiology runs ~8 min longer than Dermatology, likely reflecting complexity of follow-up and monitoring needs.

---

### 4. Patient Age Group — Modest Effect

| Age Group | Mean Duration (min) | N |
|---|---|---|
| 60+ | 29.5 | 87 |
| 40–59 | 25.3 | 60 |
| 18–39 | 23.5 | 57 |
| 0–17 | 19.9 | 46 |

Older patients (60+) average ~9.6 min longer than pediatric patients. This likely reflects greater clinical complexity (chronic conditions, polypharmacy) and is partially confounded with Cardiology/chronic condition prevalence.

---

### 5. Chronic Condition Count & Systems Involved — Weak Signals

| Factor | Pearson r with Duration |
|---|---|
| `chronic_condition_count` | 0.18 |
| `systems_involved_count` | 0.17 |

Visits with ≥1 chronic condition average ~29.7 min vs. 24.7 min for zero. `systems_involved_count` has a nonlinear edge: the two visits involving 3 systems average 42.5 min, but counts of 1–2 add only ~3 min. Both effects are real but small and dwarfed by urgency/procedure effects.

---

### 6. Factors With Negligible Effect

- **`referral_or_consult`**: r ≈ 0.00 — no discernible relationship with duration.  
- **`medication_mentions`**: r = −0.11 — slight negative association, possibly reflecting that quick prescription renewals are short visits.  
- **`note_word_count`**: r = 0.04 — essentially uncorrelated; note length does not predict visit duration in this dataset.

---

## Summary Table

| Factor | Effect Size | Confidence |
|---|---|---|
| Emergency urgency / department | +20 min vs. routine | Strong |
| Procedure performed | +8.7 min | Strong |
| Cardiology department | +8 min vs. Dermatology | Moderate |
| Age 60+ | +~5–10 min vs. pediatric | Moderate |
| Chronic condition count | +5 min | Weak |
| Systems involved count | +3–4 min | Weak |
| Referral/consult, medication mentions, note words | Negligible | Weak/None |

**Bottom line:** Visit urgency (Emergency) and whether a procedure was performed are the clearest clinical drivers of longer visits. Department specialty (Cardiology) and older patient age contribute secondarily. Chronic condition burden and multi-system involvement add marginal but real signal. All remaining variables show little or no explanatory value.
