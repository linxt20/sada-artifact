---
dataset: healthcare_visit_notes
scenario: predictive_high
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "urgency"
query: "What visit-note signals suggest high urgency?"
source_table: augment_table/healthcare_visit_notes/predictive_high/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/healthcare_visit_notes__predictive_high/analyses/original/analysis.md
wall_seconds: 91.22
---

# Visit-Note Signals Suggesting High Urgency

## Dataset Overview

The dataset contains 224 clinical visit records with five visible attributes:

| Column | Description |
|---|---|
| `department` | Clinical specialty (Emergency, Cardiology, GeneralPractice, Orthopedics, Dermatology, Pediatrics) |
| `urgency` | Labelled outcome: `Routine`, `Urgent`, or `Emergency` |
| `age_group` | `0-17`, `18-39`, `40-59`, `60+` |
| `visit_duration_min` | Consultation duration in minutes |
| `reason_for_visit` | Free-text clinical note (the primary signal source) |

The focus variable is `urgency`. The analysis distinguishes between **Urgent** (elevated priority) and **Emergency** (immediate life threat), contrasted against **Routine** visits.

---

## 1. Departmental Distribution as a Structural Urgency Signal

**Emergency department = always Emergency-labelled.** Every visit assigned to `Emergency` maps to `urgency = Emergency` without exception. The clinical notes confirm true time-critical presentations.

**Other departments** carry a mix of Routine and Urgent labels. Cardiology and Orthopedics show the broadest urgency spread — from stable follow-ups (Routine) to acute decompensation (Urgent/Emergency boundary events like STEMI, stroke, GI bleed).

> **Practical implication:** Department alone is a strong predictor — Emergency visits need no further triage from note text. For non-Emergency departments, note content becomes the decisive signal.

---

## 2. Visit Duration as a Weak Proxy Signal

| Urgency Level | Typical `visit_duration_min` |
|---|---|
| Routine | 15–30 min (modal: 20 min) |
| Urgent | 15–30 min (modal: 20–25 min) |
| Emergency | 30–60 min (modal: 35–55 min) |

Emergency visits are longer (35–60 min), reflecting stabilization and procedural work. However, Urgent and Routine visits overlap substantially in duration. Duration is a **weak standalone signal** but reinforces Emergency classification when ≥ 45 min in a non-routine context.

---

## 3. Age Group and Urgency

Elderly patients (`60+`) appear disproportionately in Emergency-labelled notes: falls with fracture, sepsis, stroke, GI bleed, DKA, acute respiratory failure. The `0-17` group has Urgent (not Emergency) visits for febrile illness, bronchiolitis, and appendicitis concern — except when transferred to the ED. Age alone is insufficient but `60+` with acute onset language in the note is a strong combined signal.

---

## 4. Textual Signals in `reason_for_visit` — The Core Urgency Source

### 4a. Emergency-Class Signals (confirmed across all Emergency-labelled rows)

These linguistic and clinical patterns appear **exclusively or predominantly** in Emergency notes:

| Signal Category | Example Phrases from Notes |
|---|---|
| Hemodynamic instability | `BP 92/58`, `HR 124`, `BP 84/50`, `HR 118` |
| Oxygen saturation crisis | `O2 sat 86% on RA`, `SpO2 89% on room air`, `SpO2 96%` dropping further |
| Stroke / neuro emergency | `NIHSS 8`, `NIHSS 14`, `sudden onset right-sided weakness`, `worst of life headache` |
| STEMI / MI | `ST elevation in V2–V4`, `STEMI protocol activated`, `cath lab notified` |
| Anion gap / metabolic crisis | `anion gap 22, pH 7.21`, `glucose 38`, `glucose 480` |
| Acute abdomen | `free air`, `perforated viscus`, `rigid abdomen`, `rebound tenderness` |
| Altered mental status | `altered mental status`, `found down`, `GCS 15` with polytrauma |
| Active hemorrhage | `melena and hematemesis`, `Hgb 7.2`, `massive hemoptysis 200mL` |
| Respiratory failure | `pCO2 72, pH 7.28`, `BiPAP initiated`, `bilateral crackles`, `accessory muscle use` |
| Sepsis criteria | `lactate 4.2`, `broad-spectrum antibiotics`, `30 mL/kg fluid resuscitation` |
| Psychiatric emergency | `suicidal ideation and plan`, `voluntary admission` |
| Anaphylaxis | `angioedema`, `IM epinephrine given` |
| Traumatic injury | `open ankle fracture`, `LOC`, `C-collar`, `8cm wound` |

**Key phrase patterns:** time anchors like `"onset 1 hour ago"`, `"45 minutes ago"`, `"30 minutes ago"` consistently appear in Emergency notes, signalling acute onset. Protocol activation language (`tPA administered`, `cath lab notified`, `Stroke alert called`, `Trauma team evaluating`) is exclusive to Emergency records.

### 4b. Urgent-Class Signals (distinguishing Urgent from Routine)

These signals appear in Urgent notes but are absent or subdued in Routine notes:

| Signal Category | Example Phrases |
|---|---|
| Acute infection with fever | `fever 39C`, `fever 38.2C`, `pyuria and nitrites positive`, `WBC 14.2` |
| New-onset pathology | `new-onset palpitations`, `new-onset hypertension`, `new-onset bedwetting after dry period` |
| Trauma with structural concern | `McMurray positive`, `Thompson test positive`, `anatomic snuffbox tenderness` |
| Acute fracture | `intertrochanteric femur fracture`, `non-displaced supracondylar fracture`, `compression fracture L2` |
| Worsening trajectory | `worsening exertional angina past 2 weeks`, `EF dropped from 45% to 30%`, `weight up 6 lbs in 4 days` |
| Specialist referral urgency | `urgent ortho referral`, `urgent ophthalmology referral`, `sent to ED for surgical evaluation` |
| Short symptom duration (<14 days) with acuity markers | `x1 week`, `x3 days`, `x2 days` combined with pain, fever, or functional loss |
| Treatment escalation | `dose increased`, `prednisone 60mg daily`, `isotretinoin enrollment` |
| Unable to bear weight / functional deficit | `unable to bear weight`, `locking and giving way`, `decreased ankle reflex` |
| Medication discontinuation for safety | `discontinued offending med`, `urgent transfer to burn unit` (SJS) |

### 4c. Routine Note Signals (absence = non-urgent)

Routine visits systematically include phrases such as `"tolerating well"`, `"asymptomatic"`, `"stable"`, `"continue current regimen"`, `"follow-up in 3/6 months"`, `"within normal limits"`, and `"well-controlled"`. Their presence reliably predicts Routine classification.

---

## 5. Composite Urgency Signal Framework

The strongest combinations in the data that predict high urgency:

1. **Department = Emergency** → urgency = Emergency (deterministic in this dataset)
2. **Acute onset time anchor + hemodynamic/O₂ abnormality** → Emergency
3. **Protocol-level activation language** (tPA, cath lab, ICU, OR, Stroke alert) → Emergency
4. **Lab values at crisis thresholds** (glucose <50 or >400, pH <7.3, lactate >2, Hgb <8) → Emergency
5. **New structural finding + inability to function** (fracture, tendon rupture, disc herniation with deficit) → Urgent
6. **Worsening trend language** (EF drop, weight gain, BP escalation) + non-Emergency department → Urgent
7. **Fever + culture/lab concern + acute antibiotic start** → Urgent (vs. Routine supportive care)
8. **"Sent to ED"** or cross-specialty urgent referral within the note → Urgent

---

## 6. Exceptions and Weak Evidence

- **Urgent ≠ Emergency despite serious diagnosis:** V-0037 (worsening angina) and V-0082 (EF drop to 30%) are labelled Urgent, not Emergency, because hemodynamics are preserved and the patient is not in acute decompensation at the time of the note.
- **Pediatric mild dehydration / bronchiolitis with SpO₂ 95%** is Urgent but not Emergency — the threshold appears to be supplemental oxygen need / SpO₂ <94%.
- **Duration alone is insufficient:** Visit duration of 30 min appears in Routine Cardiology follow-ups (e.g., V-0003, V-0010) and in Urgent Orthopedics visits — it adds little discriminative power beyond department context.
- **Age group 0-17** never generates an Emergency label from non-Emergency departments in this dataset — all paediatric Emergency cases appear to be transferred to ED rather than managed in-department.
- **Psychiatric emergencies** (V-0133: suicidal ideation with plan) receive Emergency classification even without physiological instability markers.

---

## Summary

The dominant urgency signals in visit notes are:

1. **Hemodynamic, respiratory, or neurological collapse language** → Emergency
2. **Explicit protocol/transfer/ICU activation** → Emergency
3. **Crisis-threshold lab values** → Emergency
4. **New acute structural injury or functional loss** → Urgent
5. **Worsening trajectory in a known condition** → Urgent
6. **Acute infection with objective fever and positive cultures/UA** → Urgent
7. **"Stable", "asymptomatic", "continue current"** → Routine (negative predictor)

Note free-text outperforms structured fields (department, age, duration) for distinguishing Urgent from Routine; structured fields are reliable primarily for isolating Emergency visits.
