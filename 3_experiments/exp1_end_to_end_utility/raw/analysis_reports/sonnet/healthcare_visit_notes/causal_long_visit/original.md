---
dataset: healthcare_visit_notes
scenario: causal_long_visit
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: causal_attribution
focus_variable: "visit_duration_min"
query: "Which clinical factors best explain longer visit durations?"
source_table: augment_table/healthcare_visit_notes/causal_long_visit/original.csv
generated_at: 2026-07-26T13:47:41.770317+00:00
wall_seconds: 75.36
---

# Clinical Factors Explaining Longer Visit Durations
**Dataset:** `healthcare_visit_notes / causal_long_visit / original`  
**N = 250 visits | Duration range: 15–60 min | Mean: 25.4 min | Median: 25 min**

---

## Key Finding Summary

| Factor | Effect on Duration | Strength of Evidence |
|---|---|---|
| Department (Emergency) | +20 min vs. overall mean | Strong |
| Department (Cardiology) | +4.7 min vs. overall mean | Strong |
| Age group (60+) | +4.1 min vs. overall mean | Moderate |
| Urgency (Emergency) | +20 min vs. Routine/Urgent | Strong (confounded with dept) |

---

## 1. Department — Strongest Predictor

Department is the single clearest structural predictor of visit duration.

| Department | Mean Duration (min) | N |
|---|---|---|
| **Emergency** | **45.5** | 28 |
| **Cardiology** | **30.1** | 42 |
| Orthopedics | 25.9 | 39 |
| General Practice | 21.9 | 54 |
| Pediatrics | 19.9 | 45 |
| Dermatology | 17.0 | 42 |

- **Emergency** visits average 45.5 min — nearly double the overall mean, accounting for all 28 visits at the extreme upper range.
- **Cardiology** accounts for 42 of 80 long visits (≥30 min), making it the dominant contributor by volume.
- **Dermatology** consistently logs the shortest visits (mean 17 min), regardless of urgency.

## 2. Urgency Level — Largely Mediated by Department

| Urgency | Mean Duration (min) | N |
|---|---|---|
| **Emergency** | **45.5** | 28 |
| Urgent | 23.2 | 81 |
| Routine | 22.6 | 141 |

- The "Emergency" urgency level maps 1:1 with the Emergency department in this dataset, so the urgency effect is largely **collinear with department** rather than an independent driver.
- Within non-emergency departments (Routine vs. Urgent), the urgency difference is minimal (~0.6 min), suggesting **urgency label alone does not strongly predict duration** outside the Emergency setting.

## 3. Age Group — Moderate Independent Signal

| Age Group | Mean Duration (min) | N |
|---|---|---|
| **60+** | **29.5** | 87 |
| 40–59 | 25.3 | 60 |
| 18–39 | 23.5 | 57 |
| 0–17 | 19.9 | 46 |

- Older patients (60+) have consistently longer visits across departments. Within Emergency, the 60+ group averages 52.9 min vs. 38.2 min for 18–39, suggesting age compounds complexity in acute settings.
- Pediatric visits (0–17) are the shortest, reflecting focused, single-issue encounters per the visit notes.

## 4. Cross-Factor Interactions

The department × urgency cross-tab reveals the dominant combinations:

| Department / Urgency | Mean (min) | N |
|---|---|---|
| Emergency / Emergency | 45.5 | 28 |
| Cardiology / Urgent | 30.4 | 12 |
| Cardiology / Routine | 30.0 | 30 |
| Orthopedics / Urgent | 27.4 | 17 |
| Dermatology / Routine | 15.2 | 26 |

- **Cardiology is uniformly long regardless of urgency** (30.0 vs. 30.4 min), suggesting the clinical complexity of cardiac patients — not urgency classification — drives duration.
- **Orthopedics Urgent** visits run longer than Orthopedics Routine, one of the few cases where urgency adds meaningful time (~2.6 min).

## 5. Visit Notes — Qualitative Corroboration

Inspection of `reason_for_visit` notes supports the quantitative patterns:
- Long Cardiology visits involve post-MI follow-ups, echo reviews, and multi-drug management.
- Emergency notes describe multi-step evaluations (imaging, labs, monitoring).
- Short Dermatology visits are single-condition, prescription-based encounters.

---

## Caveats and Weak Evidence

- **Urgency as an independent variable is weak** — its apparent effect is almost entirely explained by the Emergency department mapping.
- **Age group is a correlate**, not a confirmed causal factor; it may proxy for comorbidity burden not directly measured.
- With only 250 records and no continuous clinical severity score, regression-based isolation of independent effects is not feasible from this data alone.
- No procedure codes, lab orders, or comorbidity counts are available; these unmeasured factors likely mediate the department and age effects observed.

---

## Decision-Ready Summary

> **Department is the primary driver of long visits.** Emergency and Cardiology departments consistently produce the longest encounters. Age ≥60 amplifies duration, especially in Emergency. Urgency level adds little independent predictive value outside the Emergency department. Interventions aimed at reducing visit length should prioritize workflow design within Emergency and Cardiology rather than targeting urgency triage alone.
