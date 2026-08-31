---
dataset: healthcare_visit_notes
scenario: causal_long_visit
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "visit_duration_min"
query: "Which clinical factors best explain longer visit durations?"
source_table: augment_table/healthcare_visit_notes/causal_long_visit/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:21:21.251674+00:00
wall_seconds: 50.15
---

# Clinical Factors Explaining Longer Visit Durations

**Dataset:** 250 healthcare visit notes | **Focus variable:** `visit_duration_min` (range: 15–60 min, mean: 25.4 min, median: 25 min)

---

## Key Findings

### 1. Clinical Severity — Strongest Predictor

Clinical severity is the single strongest explanatory factor (Pearson *r* = **0.71**).

| Severity | Mean Duration (min) | % Visits > 35 min |
|---|---|---|
| Critical | 48.5 | 94.1% |
| High | 31.2 | 17.6% |
| Moderate | 23.9 | 0.0% |
| Low | 21.1 | 0.0% |

> **Practically all visits exceeding 35 minutes involve critical or high severity.** No moderate or low severity visit crossed the 35-minute threshold.

---

### 2. Disposition Complexity — Strong Co-factor

Disposition complexity is closely tied to duration and likely mediates much of the severity effect.

| Disposition | Mean Duration (min) | % Visits > 35 min |
|---|---|---|
| ICU admission | 50.0 | 100% |
| Inpatient admission | 39.4 | 58.3% |
| Observation/monitoring | 42.9 | 57.1% |
| Discharge with follow-up | 23.5 | 0.0% |
| Discharge routine | 20.5 | 0.0% |

Visits ending in admission or observation are consistently long; those ending in straightforward discharge are consistently short.

---

### 3. Condition Category — Acuity Drives Duration

Acute high-acuity conditions dominate the long-visit tail:

| Condition | Mean (min) | % Visits > 35 min |
|---|---|---|
| Acute cardiovascular | 47.3 | 81.8% |
| Acute neurological | 42.5 | 83.3% |
| Acute surgical abdomen | 40.8 | 66.7% |
| Acute injury/trauma | 30.3 | 13.3% |
| Chronic disease management | 27.5 | 0.0% |
| Dermatologic | 17.3 | 0.0% |

Chronic disease management visits are moderately long on average (27.5 min) but **never exceed 35 minutes**, indicating a different mechanism (complexity without urgency).

---

### 4. Department & Urgency — Structural Reflections of Severity

- **Emergency** department: mean 45.5 min (n=28), closely mirrors the Emergency urgency tier.
- **Cardiology**: mean 30.1 min, driven by both chronic follow-ups and acute cardiac events.
- **Pediatrics** and **Dermatology**: shortest mean durations (≤20 min).
- **Urgency** alone adds limited predictive value beyond department (Emergency urgency = Emergency department in this dataset).

---

### 5. Diagnostic Workup and Procedures — Moderate Contributors

| Diagnostic Workup | Mean (min) |
|---|---|
| Multiple modalities | 39.2 |
| ECG/Holter/Echo | 30.3 |
| Advanced imaging (CT/MRI) | 29.5 |
| Labs only | 27.9 |
| Not present | 22.2 |

| Procedure | Mean (min) |
|---|---|
| IV/IM medication administration | 33.0 |
| Cast/splint immobilization | 25.8 |
| Not present | 23.9 |

Extensive workup and IV procedures add time, but their effect is likely downstream of severity rather than an independent cause.

---

### 6. Multisystem Involvement — Weak-to-Moderate Effect

Multisystem involvement correlates modestly with duration (*r* = 0.35). Mean duration rises from 22.2 min (single system) to 27.8 min (two systems) to 37.0 min (three or more systems), but the three-or-more group is very small (n=5), so this finding is **weak evidence**.

---

### 7. Age Group — Modest Confound

Older patients (60+) have the longest mean duration (29.5 min), likely reflecting higher rates of chronic disease management and comorbidity rather than age itself.

---

## Summary

The evidence points to a clear hierarchy of explanatory factors:

1. **Clinical severity** (dominant; *r* = 0.71) — critical/high severity nearly guarantees a long visit.
2. **Disposition complexity** (strong; co-varies with severity) — admission vs. discharge is the sharpest binary divider.
3. **Condition category** — acute cardiovascular, neurological, and surgical conditions drive the longest visits.
4. **Diagnostic and procedural intensity** — multiple imaging modalities and IV medication administration extend visits but appear downstream of severity.
5. **Multisystem involvement** — directionally consistent but limited by sparse data at the high end.

**Exceptions / Weak evidence:** Chronic disease management visits are moderately long without ever being very long, suggesting a separate "complexity without urgency" pathway. Mental/behavioral health visits (n=5) show high variability and should not be over-interpreted. Multisystem involvement ≥3 systems has only 5 cases.
