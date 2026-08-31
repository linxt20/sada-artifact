---
dataset: healthcare_visit_notes
scenario: causal_triage
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: what_if
focus_variable: "triage_and_scheduling_efficiency"
query: "How can clinics improve triage and scheduling?"
source_table: augment_table/healthcare_visit_notes/causal_triage/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/healthcare_visit_notes__causal_triage/analyses/original/analysis.md
wall_seconds: 90.1
---

# Triage and Scheduling Improvement Analysis
## Dataset: `healthcare_visit_notes__causal_triage` (N = 250 visits)

---

## 1. Dataset Overview

The dataset contains 250 clinic visit records with five structured variables:

| Variable | Values |
|---|---|
| `department` | GeneralPractice, Pediatrics, Cardiology, Dermatology, Orthopedics, Emergency |
| `urgency` | Routine, Urgent, Emergency |
| `age_group` | 0-17, 18-39, 40-59, 60+ |
| `visit_duration_min` | 15 – 60 min |
| `reason_for_visit` | Free-text clinical notes |

The **focus variable for triage is `urgency`**, which directly determines how patients should be prioritized and slotted. `visit_duration_min` is the key scheduling variable.

---

## 2. Key Patterns Relevant to Triage and Scheduling

### 2.1 Urgency Distribution

Across all 250 visits, the approximate urgency split is:
- **Routine** (~60%): Follow-ups, wellness exams, chronic disease management
- **Urgent** (~28%): Acute but non-life-threatening presentations (strains, infections, fractures)
- **Emergency** (~12%): Life-threatening events routed through the Emergency department

> **Implication**: The majority of clinic volume is schedulable in advance. However, ~28% of visits arrive as same-day urgent cases, representing the main triage challenge in non-Emergency departments.

---

### 2.2 Visit Duration by Urgency Level

From the data, a clear duration gradient exists by urgency:

| Urgency | Typical Duration | Range |
|---|---|---|
| Routine | 15–25 min | 15–30 min |
| Urgent | 20–30 min | 15–35 min |
| Emergency | 35–60 min | 30–60 min |

**Emergency visits consume 2–3× more time** than routine visits. Underestimating the duration of urgent walk-ins causes downstream scheduling bottlenecks. Clinics should reserve longer slots for urgent add-ons rather than squeezing them into standard 15-minute blocks.

---

### 2.3 Urgency and Duration by Department

| Department | Urgency Profile | Typical Duration |
|---|---|---|
| **Emergency** | 100% Emergency | 30–60 min |
| **Cardiology** | Mostly Routine; some Urgent | 30 min (consistent) |
| **Orthopedics** | ~50% Urgent | 20–30 min |
| **GeneralPractice** | ~35% Urgent | 20–25 min |
| **Pediatrics** | ~35% Urgent | 15–25 min |
| **Dermatology** | ~25% Urgent | 15–20 min |

**Key findings:**
- **Cardiology** holds 30-minute slots uniformly regardless of urgency — this is already well-calibrated but leaves little buffer for acute exacerbations (e.g., V-0082: EF drop from 45% to 30%; V-0146: acute HF exacerbation).
- **Orthopedics** has the highest urgent-to-routine ratio outside the Emergency department. Half of orthopedic visits are urgent (fractures, tendon ruptures, acute dislocations), suggesting a dedicated same-day urgent orthopedic slot is warranted.
- **GeneralPractice and Pediatrics** see frequent urgent cases (infections, acute injuries, pediatric crises like Kawasaki disease) mixed with schedulable wellness visits — a dual-track scheduling model is advisable.
- **Dermatology** has fewer urgent cases, mostly related to cellulitis, biopsy-triggering lesions, and severe drug reactions (e.g., V-0170: Stevens-Johnson syndrome requiring transfer). These rare but time-critical cases require clear escalation criteria.

---

### 2.4 Age Group and Urgency

- **60+ patients** account for a disproportionate share of both Urgent and Emergency visits — hip fractures, HF exacerbations, strokes, sepsis, and DKA appear concentrated in this group. This cohort also tends toward longer visit durations due to comorbidity complexity.
- **0-17 (Pediatrics)** urgent cases are frequent but tend to be shorter (15–20 min), suggesting efficient protocols already exist for pediatric triage.
- **18-39** Emergency visits include trauma (MVA, anaphylaxis, open fractures, psychiatric crises) — typically same-day walk-in or EMS-driven, less predictable.
- **40-59** is the most mixed group, spanning routine chronic disease management to acute musculoskeletal and cardiac events.

> **Implication**: Age-stratified triage protocols — particularly for patients 60+ — can improve efficiency. These patients may warrant pre-visit screening calls to identify potential escalations before arrival.

---

### 2.5 Distinguishing Urgent from Routine Within the Same Department

The clinical notes reveal that **urgency is not always apparent from the chief complaint alone**. Examples where misclassification risk is high:

- **Pediatrics Routine vs. Urgent**: A "rash and fever" case (V-0031) was Roseola (Routine, 15 min); a "prolonged fever" case (V-0120) was Kawasaki disease (Urgent, 20 min, hospital admission). Both could present similarly at intake.
- **GeneralPractice Urgent vs. Routine**: "Low back pain" is Routine in V-0013 (chronic, 25 min) but Urgent in V-0029 (acute strain, 20 min) and Urgent with sciatica in V-0165 (20 min). Duration is similar but triage pathways differ.
- **Orthopedics**: Routine follow-ups (post-TKR, post-ACL) consistently run 25 min; acute fractures and tendon ruptures consistently run 25–30 min. Duration alone does not separate these categories — the acuity description must.

> **Implication**: Intake questionnaires or symptom-specific triage scripts (onset acuity, functional loss, systemic symptoms) are more reliable urgency signals than visit type alone.

---

## 3. Actionable Recommendations

### 3.1 Department-Level Scheduling Adjustments

| Department | Recommendation |
|---|---|
| **Orthopedics** | Reserve 2–3 same-day urgent slots daily (fractures, tendon injuries, acute joint locks) |
| **GeneralPractice** | Implement dual-track scheduling: pre-booked Routine + same-day Urgent buffer slots |
| **Pediatrics** | Use symptom onset duration and fever flags at check-in to pre-sort Urgent cases |
| **Cardiology** | Standardize 30-min slots but add a 45-min overflow slot for urgent new exacerbations |
| **Dermatology** | Establish a clear escalation protocol for rapidly evolving lesions or rashes to avoid missed SJS/biopsy-critical cases |

### 3.2 Triage Protocol Improvements

1. **Structured intake screening**: Use symptom-onset timeline (acute <72 hr vs. chronic >4 wk) as a primary urgency signal — consistently visible in clinical notes across departments.
2. **Age-based flagging**: Automatically flag 60+ patients with acute symptoms for extended-duration slots and possible same-day escalation.
3. **Red-flag symptom lists by department**: Orthopedics (inability to bear weight, positive Thompson/McMurray), Pediatrics (prolonged fever >5 days, stridor at rest), Cardiology (new dyspnea, syncope, palpitations with hemodynamic change).
4. **Overbooking buffer calibration**: Because urgent visits average 5–10 min longer than routine visits, clinics should not backfill urgent slots with routine appointments without duration adjustment.

---

## 4. Caveats and Limitations

- **No timestamps or wait-time data**: The dataset lacks arrival time, wait time, or actual vs. scheduled duration — limiting direct measurement of triage efficiency. Duration here represents visit length, not queue delay.
- **Urgency is pre-assigned**: It is unclear whether `urgency` reflects initial patient-reported severity or a clinician's retrospective classification. If the latter, it cannot directly calibrate front-desk triage.
- **Small Emergency department sample**: Emergency visits (~30 records) are exclusively in the Emergency department, so cross-department Emergency urgency comparisons are not possible.
- **Dermatology urgent outliers are rare but severe**: V-0170 (Stevens-Johnson syndrome requiring burn unit transfer) and V-0077 (bullous pemphigoid) are single events; patterns inferred from them carry high uncertainty.
- **Causal attribution is limited**: The data shows associations between department, age, and urgency — but cannot establish whether, for example, older age *causes* longer visits independently of diagnosis mix.

---

## 5. Summary

The strongest levers for triage and scheduling improvement are:

1. **Slot duration calibration by urgency and department** — Emergency and Urgent visits consistently run longer; 15-min default slots will cause bottlenecks.
2. **Dedicated same-day urgent capacity** — especially in Orthopedics and GeneralPractice, which show ~35–50% urgent volume.
3. **Symptom-onset structured intake** — onset acuity (acute vs. chronic) is the most reliable urgency discriminator visible across the clinical notes.
4. **Age-stratified prioritization** — 60+ patients represent the highest-acuity, highest-duration subgroup in non-Emergency settings and warrant proactive scheduling buffers.
