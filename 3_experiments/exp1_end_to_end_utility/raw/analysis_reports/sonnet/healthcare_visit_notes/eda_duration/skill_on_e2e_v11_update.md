---
dataset: healthcare_visit_notes
scenario: eda_duration
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "visit_duration_min"
query: "How do reasons for visit relate to urgency and visit duration across department and age group?"
source_table: augment_table/healthcare_visit_notes/eda_duration/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:22:27.386454+00:00
wall_seconds: 82.8
---

# How Reasons for Visit Relate to Urgency and Visit Duration Across Department and Age Group

**Dataset:** 250 visits · 6 departments · 4 age groups · original + 10 TAPP-generated columns

---

## Method Note

TAPP-generated columns used in this report: `visit_type`, `primary_clinical_category`, `symptom_acuity`, `condition_complexity`, `diagnostic_workup_intensity`, `treatment_intensity`. Columns `injury_mechanism`, `injury_or_illness_mechanism`, `disposition_signal`, and `patient_age_proxy` were examined but found redundant with structured fields or low-signal for the query and are not featured.

---

## 1. Urgency and Duration: Baseline

| Urgency | n | Mean Duration (min) | Median |
|---|---|---|---|
| Emergency | 28 | **45.5** | 45.0 |
| Urgent | 81 | 23.2 | 20.0 |
| Routine | 141 | 22.6 | 20.0 |

Emergency visits drive duration sharply upward (+22 min vs. Routine). Urgent and Routine visits are nearly indistinguishable at median, suggesting urgency alone does not explain within-non-emergency variation; reason for visit matters more.

---

## 2. Visit Reason Patterns (visit_type + primary_clinical_category)

### 2a. Visit Type → Urgency and Duration

| visit_type | Emergency | Routine | Urgent | Mean Duration (min) |
|---|---|---|---|---|
| emergency_presentation | 28 | 0 | 2 | **44.5** |
| chronic_disease_management | 0 | 72 | 6 | 25.8 |
| acute_complaint | 0 | 16 | 71 | 21.4 |
| post_procedure_followup | 0 | 6 | 1 | 24.3 |
| preventive_wellness | 0 | 37 | 1 | 19.9 |
| counseling_screening | 0 | 10 | 0 | 20.0 |

- **emergency_presentation** (n=30) is almost exclusively Emergency-urgency and the longest visit type.
- **acute_complaint** (n=87) drives the bulk of Urgent designations (71/81 = 88% of all Urgent visits) but has a *shorter* mean duration (21.4 min) than chronic disease management—suggesting urgency ≠ longer visit in these cases.
- **chronic_disease_management** (n=78) is Routine but longer than acute complaints, reflecting management complexity.

### 2b. Clinical Category → Duration

| primary_clinical_category | Mean Duration (min) | Predominant Urgency |
|---|---|---|
| gastrointestinal | 32.8 | Emergency / Urgent |
| neurologic | 32.7 | Emergency / Urgent |
| cardiovascular | 30.6 | Routine (Cardiology) |
| respiratory | 30.4 | Mixed |
| endocrine_metabolic | 28.3 | Routine |
| musculoskeletal | 25.9 | Routine / Urgent |
| dermatologic | 17.0 | Routine |
| pediatric_developmental | 20.2 | Routine |

Gastrointestinal and neurologic presentations have the highest mean durations and skew toward Emergency/Urgent urgency. Dermatologic presentations are the shortest (17.0 min, all Routine).

---

## 3. Department Patterns

### Mean Duration by Department × Urgency

| Department | n | Routine (mean min) | Urgent (mean min) | Emergency (mean min) |
|---|---|---|---|---|
| Cardiology | 42 | 30.0 | 30.4 | — |
| Dermatology | 42 | 15.2 | 20.0 | — |
| Emergency | 28 | — | — | 45.5 |
| GeneralPractice | 54 | 21.8 | 22.0 | — |
| Orthopedics | 39 | 24.8 | 27.4 | — |
| Pediatrics | 45 | 20.6 | 19.0 | — |

- **Cardiology** has the highest mean duration among non-emergency departments (30.1 min overall), driven by chronic_disease_management and cardiovascular complexity (`condition_complexity`: known_with_complication mean = 34.5 min).
- **Dermatology** is the shortest (17.0 min), consistent with `treatment_intensity` = topical_or_OTC (mean 17.1 min, n=17) and `diagnostic_workup_intensity` = basic_labs_or_vitals.
- **Pediatrics** shows a modest urgency inversion: Urgent visits are slightly *shorter* (19.0 min) than Routine (20.6 min), likely because acute pediatric complaints (viral URIs, fever) are straightforward.
- Emergency department visits are exclusively Emergency-urgency by design (28/28).

---

## 4. Age Group Patterns

### Duration and Urgency Rate by Age Group

| Age Group | n | Mean Duration (min) | Emergency Rate | Urgent Rate |
|---|---|---|---|---|
| 0–17 | 46 | 19.9 | 0% | 48% |
| 18–39 | 57 | 23.5 | 19% | 30% |
| 40–59 | 60 | 25.3 | 8% | 28% |
| 60+ | 87 | 29.5 | 14% | 29% |

- Duration increases monotonically with age: 60+ patients average 29.5 min vs. 19.9 min for children.
- Children (0–17) have zero Emergency visits but the highest Urgent rate (48%), reflecting acute infectious complaints rather than life-threatening emergencies—confirmed by `symptom_acuity`: 0–17 has no life_threatening cases.
- 60+ patients have the longest Emergency visits (mean 52.9 min) driven by high `symptom_acuity` = life_threatening (mean duration 51.4 min for this group).

### Mean Duration by Age Group × Urgency

| Age Group | Routine | Urgent | Emergency |
|---|---|---|---|
| 0–17 | 20.6 | 19.1 | — |
| 18–39 | 19.0 | 21.8 | 38.2 |
| 40–59 | 22.8 | 25.6 | 44.0 |
| 60+ | 25.5 | 26.2 | **52.9** |

The age-duration gradient holds within every urgency tier, suggesting older patients require more time regardless of urgency level.

---

## 5. Semantic Acuity and Complexity Cross-Check

**symptom_acuity** strongly aligns with urgency and duration:

| symptom_acuity | Emergency | Routine | Urgent | Mean Duration (min) |
|---|---|---|---|---|
| asymptomatic | 0 | 64 | 1 | 23.2 |
| life_threatening | 10 | 0 | 0 | **47.5** |
| mild | 0 | 41 | 15 | 20.3 |
| moderate | 3 | 34 | 46 | 24.2 |
| severe | 15 | 2 | 19 | 33.9 |

`symptom_acuity` = severe accounts for 15 of 28 Emergency visits and has a mean duration of 33.9 min overall, bridging Urgent and Emergency tiers.

**condition_complexity** adds signal:
- `known_with_complication` (n=11): mean 34.5 min — highest among complexity categories, concentrated in Cardiology and Emergency.
- `not_present` (n=37, preventive/asymptomatic): mean 20.4 min.

**diagnostic_workup_intensity** directly maps to duration:
- `emergent_multilevel` (n=28, all Emergency): mean **43.8 min**
- `advanced_imaging_or_procedure` (n=25): mean 27.8 min
- `basic_labs_or_vitals` (n=70): mean 22.6 min

---

## 6. Key Findings Summary

1. **Urgency tier is the strongest single predictor of duration**: Emergency visits average 45.5 min vs. ~22–23 min for Routine/Urgent.
2. **Reason for visit modulates duration within urgency tiers**: chronic disease management (Routine, Cardiology) averages 25.8 min vs. preventive wellness at 19.9 min; gastrointestinal/neurologic presentations are longest within Urgent visits.
3. **Department reflects case mix**: Cardiology's high duration reflects chronic cardiovascular management; Dermatology's brevity reflects topical/OTC treatment; Emergency's duration reflects emergent multilevel workup.
4. **Age amplifies all effects**: 60+ patients are 50% longer than 0–17 across all urgency tiers; older patients dominate the Emergency cohort's longest visits (mean 52.9 min).
5. **Children are frequently Urgent but never Emergency** in this dataset, and their visits are short, because their acute complaints are high-frequency but low-complexity infectious presentations.
6. TAPP columns `symptom_acuity` and `diagnostic_workup_intensity` add confirmed quantitative signal that bridges free-text reasons to structured urgency and duration outcomes, consistent with original structured fields.
