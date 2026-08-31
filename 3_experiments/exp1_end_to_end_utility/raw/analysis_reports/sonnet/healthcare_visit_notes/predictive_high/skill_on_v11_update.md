---
dataset: healthcare_visit_notes
scenario: predictive_high
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "urgency"
query: "What visit-note signals suggest high urgency?"
source_table: augment_table/healthcare_visit_notes/predictive_high/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:22:17.093542+00:00
wall_seconds: 65.44
---

# Visit-Note Signals Suggesting High Urgency

**Dataset:** 250 healthcare visit notes | **Focus variable:** `urgency` (Routine: 141, Urgent: 81, Emergency: 28)

---

## 1. Strongest Predictive Signals (100% precision)

The following column values are **perfectly associated** with high urgency (Urgent or Emergency) across all observed cases:

| Signal | Column | Count (high-urgency / total) | Notes |
|---|---|---|---|
| `sudden_acute` onset | `symptom_onset_acuity` | 49 / 49 | All sudden-onset visits are non-routine |
| `emergency_activation` | `visit_type_context` | 28 / 28 | Exclusive to Emergency tier |
| `True` | `hemodynamic_instability` | 8 / 8 | Small count but perfect discriminator |
| `emergent_labs_cultures` | `diagnostic_urgency_proxy` | 12 / 12 | Ordered only for Urgent/Emergency |
| `neurological_acute` | `chief_complaint_category` | 7 / 7 | All high-urgency |
| `trauma_injury` | `chief_complaint_category` | 15 / 15 | All high-urgency |
| `respiratory_distress` | `chief_complaint_category` | 7 / 7 | All high-urgency |
| Visit duration ≥ 40 min | `visit_duration_min` | 22 / 22 | Entirely Emergency-tier visits |

---

## 2. Near-Perfect Signals (>85% precision)

| Signal | Column | High-urgency rate | Count |
|---|---|---|---|
| `severe` pain | `pain_severity_indicator` | 96% | 51 total |
| `bedside_procedure_diagnostic` | `diagnostic_urgency_proxy` | 88% | 16 total |
| `stat_imaging_ordered` | `diagnostic_urgency_proxy` | 77% | 22 total |

**Severe pain** is the most common near-perfect signal (51 visits) and nearly exclusive to non-routine cases. Stat imaging, while strongly associated, does appear in 5 Routine visits—a notable exception.

---

## 3. Emergency vs. Urgent Differentiators

Within high-urgency visits, **Emergency** cases show a distinct fingerprint:

- **`symptom_onset_acuity`**: 27/28 Emergency visits are `sudden_acute` (vs. 22/81 Urgent). Sudden onset is near-sufficient for Emergency classification.
- **`pain_severity_indicator`**: 25/28 Emergency visits report `severe` pain (vs. 24/81 Urgent).
- **`hemodynamic_instability = True`**: All 8 positive cases are in Emergency.
- **`chief_complaint_category`**: Emergency cases concentrate on `neurological_acute` (5), `respiratory_distress` (4), `abdominal_acute` (4), `trauma_injury` (4), `hemorrhage_vascular` (3), and `metabolic_crisis` (3)—categories absent or rare at Routine level.
- **`organ_system_involved`**: Neurological (7), multi-system (3), and respiratory (4) are disproportionately Emergency.
- **`visit_duration_min`**: Emergency mean = 45.5 min vs. Urgent = 23.2 min vs. Routine = 22.6 min—a large gap.

---

## 4. Weak or Ambiguous Signals

- **`chief_complaint_category = skin_dermatologic`** and **`musculoskeletal_pain`**: Both appear frequently across all urgency tiers—these categories have limited discriminatory power on their own.
- **`symptom_onset_acuity = days`** or **`weeks_to_chronic`**: Found across Urgent and Routine; insufficient alone.
- **`diagnostic_urgency_proxy = no_workup`**: Predominates even in Urgent visits (57/109 high-urgency), meaning absence of diagnostic orders does **not** rule out urgency.
- **`moderate` pain**: Appears in 33 high-urgency and 24 Routine visits—moderate predictive value only.
- **Department**: All Emergency visits are concentrated in the Emergency department (no Emergency cases in Cardiology, Dermatology, Orthopedics, or Pediatrics in this dataset), but this likely reflects triage routing rather than a note-level predictive signal.

---

## 5. Summary Decision Rules

For clinical decision support from visit-note structured fields, the following hierarchy applies:

1. **Immediate high urgency (Emergency):** `sudden_acute` onset + `severe` pain + `emergency_activation` visit context → 100% precision individually; co-occurrence is near-definitive for Emergency.
2. **High urgency (Urgent or Emergency):** Any of `trauma_injury`, `neurological_acute`, `respiratory_distress` complaint categories; `emergent_labs_cultures`; `hemodynamic_instability = True`; visit duration ≥ 40 min.
3. **Supportive signals:** Severe pain alone (~96%), bedside diagnostic procedures (~88%), stat imaging (~77%).
4. **Caution:** No single weak signal (moderate pain, days-onset, skin/musculoskeletal category, no workup ordered) reliably distinguishes urgency levels. Combinations should be evaluated.
