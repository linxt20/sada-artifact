---
dataset: healthcare_visit_notes
scenario: predictive_high
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "urgency"
query: "What visit-note signals suggest high urgency?"
source_table: augment_table/healthcare_visit_notes/predictive_high/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:22:41.306562+00:00
wall_seconds: 86.54
---

# Visit-Note Signals Suggesting High Urgency
**Dataset:** `sonnet__skill_on_e2e_v11_update.csv` | N = 250 visits | High urgency (Urgent + Emergency) = 109 (43.6%)

---

## Method Note

TAPP-generated columns used in this analysis: `symptom_severity`, `onset_acuity`, `presentation_type`, `organ_system_involved`, `visit_purpose`, `diagnostic_workup_urgency`. These were cross-checked against original structured columns (`urgency`, `department`, `visit_duration_min`, `age_group`) and free-text `reason_for_visit` notes.

---

## 1. Outcome Distribution

| Urgency Class | N | % |
|---|---|---|
| Routine | 141 | 56.4% |
| Urgent | 81 | 32.4% |
| Emergency | 28 | 11.2% |

All Emergency cases originate exclusively from the **Emergency department** (n=28, 100%).

---

## 2. Strongest Single Predictors of High Urgency

### 2a. `symptom_severity` (TAPP) — Strongest discriminator

| symptom_severity | Emergency | Urgent | Routine | N | High-Urgency Rate |
|---|---|---|---|---|---|
| critical | 13 | 1 | 0 | 14 | **100%** |
| severe | 11 | 19 | 3 | 33 | **91%** |
| moderate | 4 | 41 | 34 | 79 | 57% |
| mild | 0 | 19 | 57 | 76 | 25% |
| not_present | 0 | 1 | 47 | 48 | 2% |

Notes coded `critical` or `severe` in the visit text are high-urgency in 93–100% of cases. Notes with no symptom presence (`not_present`) are high-urgency only 2% of the time.

### 2b. `onset_acuity` (TAPP) — Perfect separator for acute presentations

| onset_acuity | Emergency | Urgent | Routine | N | High-Urgency Rate |
|---|---|---|---|---|---|
| sudden_minutes | 6 | 0 | 0 | 6 | **100%** |
| acute_hours | 22 | 29 | 0 | 51 | **100%** |
| subacute_days | 0 | 26 | 0 | 26 | **100%** |
| chronic_weeks_or_more | 0 | 25 | 103 | 128 | 20% |
| not_present | 0 | 1 | 38 | 39 | 3% |

Any acute or sudden onset in the visit note predicts high urgency with 100% precision. Chronic/longstanding symptoms are low-urgency 80% of the time.

### 2c. Combined signal: severe/critical severity + acute onset

All 38 visits with both `symptom_severity` ∈ {critical, severe} **and** `onset_acuity` ∈ {sudden_minutes, acute_hours, subacute_days} were high-urgency (**100%, n=38**). This combination is the single most reliable composite signal in the notes.

---

## 3. Presentation Type and Visit Purpose

### `presentation_type` (TAPP)

| presentation_type | N | High-Urgency Rate |
|---|---|---|
| trauma_injury | 17 | **100%** |
| acute_illness | 82 | **94%** |
| mental_health | 5 | 60% |
| procedural_only | 12 | 25% |
| chronic_disease_followup | 93 | 9% |
| preventive_wellness | 41 | 2% |

Visit notes framed as acute illness or trauma are overwhelmingly high-urgency. Chronic follow-up and preventive wellness notes carry <10% urgency rates. This facet is highly informative and largely independent of structured `department` (chronic follow-up occurs across all non-ED departments).

### `visit_purpose` (TAPP)

| visit_purpose | N | High-Urgency Rate |
|---|---|---|
| emergency_evaluation | 30 | **100%** |
| urgent_sick_visit | 77 | **90%** |
| procedure_or_injection | 12 | 17% |
| scheduled_followup | 86 | 8% |
| preventive_screening | 38 | 3% |
| counseling_only | 7 | 0% |

The `visit_purpose` facet closely mirrors the official `urgency` label, confirming it captures true clinical intent from note language.

---

## 4. Organ System Involved

### `organ_system_involved` (TAPP)

| organ_system_involved | N | High-Urgency Rate |
|---|---|---|
| multi_system | 2 | **100%** |
| infectious | 13 | **92%** |
| neurological | 15 | **80%** |
| gastrointestinal | 9 | 78% |
| respiratory | 13 | 69% |
| musculoskeletal | 48 | 52% |
| psychiatric | 4 | 50% |
| dermatologic | 46 | 43% |
| cardiovascular | 49 | 33% |
| endocrine_metabolic | 14 | 21% |
| not_present | 37 | 3% |

Neurological, infectious, GI, and respiratory organ systems are disproportionately high-urgency. Cardiovascular appears moderate (33%) partly because many visits are scheduled cardiology follow-ups post-MI. Dermatologic and endocrine notes are mostly routine.

---

## 5. Diagnostic Workup Urgency

### `diagnostic_workup_urgency` (TAPP)

| diagnostic_workup_urgency | Emergency | Urgent | Routine | N | High-Urgency Rate |
|---|---|---|---|---|---|
| emergent_imaging_or_labs | 23 | 5 | 0 | 28 | **100%** |
| urgent_imaging_or_labs | 0 | 22 | 16 | 38 | 58% |
| no_workup | 5 | 53 | 95 | 153 | 38% |
| routine_labs_ordered | 0 | 1 | 30 | 31 | 3% |

Notes describing emergent imaging or labs (e.g., stat CT, ECG, troponin) are 100% high-urgency. Routine lab orders are near-exclusively routine visits.

---

## 6. Structured Column Cross-Checks

**Visit duration:** Emergency visits are notably longer (mean 45.5 min) vs. Urgent (23.2 min) and Routine (22.6 min), suggesting resource-intensive workup is reflected in the note complexity and `diagnostic_workup_urgency`.

**Department:** The Emergency department is the sole source of Emergency-class visits. Among non-ED departments, Pediatrics has the highest Urgent rate (21/45 = 47%), followed by Orthopedics (17/39 = 44%). Cardiology is dominated by routine follow-ups despite cardiovascular system involvement.

**Age group:** No age group has dramatically different urgency rates (range 37–49%), meaning age alone is not a reliable signal, and symptom/acuity features from the notes are more discriminative.

**Free-text keywords in `reason_for_visit`:** Trauma/injury language (93% high urgency, n=15), seizure/syncope (100%, n=3), and fever (92%, n=12) are specific high-urgency signals in raw note text, consistent with `presentation_type` and `onset_acuity` TAPP encodings.

---

## 7. Summary: Ranked Signals for High Urgency

| Rank | Signal | Type | High-Urgency Rate When Present |
|---|---|---|---|
| 1 | `onset_acuity` = acute_hours / sudden_minutes / subacute_days | TAPP | **100%** (n=83) |
| 2 | `symptom_severity` = critical | TAPP | **100%** (n=14) |
| 3 | `presentation_type` = trauma_injury | TAPP | **100%** (n=17) |
| 4 | `visit_purpose` = emergency_evaluation | TAPP | **100%** (n=30) |
| 5 | `diagnostic_workup_urgency` = emergent_imaging_or_labs | TAPP | **100%** (n=28) |
| 6 | `symptom_severity` = severe | TAPP | 91% (n=33) |
| 7 | `presentation_type` = acute_illness | TAPP | 94% (n=82) |
| 8 | `organ_system_involved` = neurological / infectious | TAPP | 80–92% (n=15, 13) |
| 9 | Trauma/fever/seizure keywords in `reason_for_visit` | Original text | 92–100% |
| 10 | `department` = Emergency | Original structured | 100% (n=28) |

**Key finding:** The most reliable high-urgency signals in visit notes are (a) acute or sudden symptom onset, (b) severe or critical symptom intensity, and (c) framing as acute illness or trauma—all detectable from note language via the TAPP `onset_acuity`, `symptom_severity`, and `presentation_type` facets. When these three facets co-occur with critical severity, urgency is 100% in this dataset. Chronic/follow-up and preventive notes are low-urgency with >90% reliability.
