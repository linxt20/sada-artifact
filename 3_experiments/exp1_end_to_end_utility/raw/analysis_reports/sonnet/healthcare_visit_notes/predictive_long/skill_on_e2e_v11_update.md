---
dataset: healthcare_visit_notes
scenario: predictive_long
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "visit_duration_min"
query: "What visit-note signals suggest a longer visit?"
source_table: augment_table/healthcare_visit_notes/predictive_long/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:23:00.614693+00:00
wall_seconds: 92.16
---

# Visit-Note Signals Suggesting a Longer Visit
**Dataset:** `sonnet__skill_on_e2e_v11_update.csv` · N = 250 visits  
**Outcome variable:** `visit_duration_min` (mean 25.4 min, SD 9.1, range 15–60)  
**"Long visit" threshold:** ≥ 30 min (top quartile; 80/250 = 32% of visits)

---

## Method Note

TAPP-generated columns used in this analysis: `visit_type`, `clinical_severity_level`, `new_diagnosis_flag`, `chronic_disease_count`, `diagnostic_test_ordered`, `specialist_consult_triggered`, `outbound_referral_count`. The columns `new_medication_initiated` and `counseling_topic` were examined but showed weak or secondary associations and are noted accordingly.

---

## 1. Strongest Predictors of Visit Length

### 1.1 Urgency & Department (Structural Signals)

| Urgency | Mean Duration (min) | Long-Visit Rate |
|---------|-------------------|----------------|
| Emergency | 45.5 | **100%** (28/28) |
| Urgent | 23.2 | 25.9% (21/81) |
| Routine | 22.6 | 22.0% (31/141) |

| Department | Mean Duration (min) | Long-Visit Rate |
|------------|-------------------|----------------|
| Emergency | 45.5 | **100%** (28/28) |
| Cardiology | 30.1 | **100%** (42/42) |
| Orthopedics | 25.9 | 23.1% (9/39) |
| GeneralPractice | 21.9 | 0% (0/54) |
| Pediatrics | 19.9 | 2.2% (1/45) |
| Dermatology | 17.0 | **0%** (0/42) |

Emergency and Cardiology visits are the highest-duration departments, each averaging 30+ minutes with 100% long-visit rates.

### 1.2 `visit_type` (TAPP) — Strongest TAPP Signal

| visit_type | Mean Duration (min) | Long-Visit Rate |
|-----------|-------------------|----------------|
| emergency_or_urgent_care | 44.5 | **100%** (30/30) |
| chronic_disease_followup | 25.2 | **42.4%** (36/85) |
| counseling_or_planning | 23.0 | 20.0% (1/5) |
| post_procedure_followup | 23.3 | 16.7% (1/6) |
| acute_complaint | 21.5 | 14.0% (12/86) |
| well_child_or_preventive | 19.9 | **0%** (0/38) |

`visit_type` is the highest-discriminating TAPP column. Notes describing **emergency/urgent care** or **chronic disease follow-up** reliably predict longer visits; preventive/well-child notes predict the shortest visits.

### 1.3 `clinical_severity_level` (TAPP) — Strong Dose-Response

| Severity | Mean Duration (min) | Long-Visit Rate |
|---------|-------------------|----------------|
| 5 (highest) | 47.1 | **94.1%** (16/17) |
| 4 | 34.3 | **87.0%** (20/23) |
| 3 | 24.9 | 36.6% (15/41) |
| 2 | 22.7 | 17.8% (18/101) |
| 1 (lowest) | 21.1 | 16.2% (11/68) |

Clear monotonic relationship: severity levels 4–5 drive long visits nearly universally. This complements the raw `urgency` field—high clinical severity in the note text is an independent signal beyond triage category.

---

## 2. Clinical Complexity Signals

### 2.1 `diagnostic_test_ordered` (TAPP)

| Test Type | Mean Duration (min) | Long-Visit Rate |
|-----------|-------------------|----------------|
| electrodiagnostic_or_monitor | 31.7 | **88.9%** (8/9) |
| imaging_ordered | 31.9 | **65.7%** (23/35) |
| both_imaging_and_lab | 33.1 | **62.5%** (5/8) |
| lab_ordered | 25.3 | 24.1% (7/29) |
| not_present | 23.3 | 21.9% (37/169) |

Notes mentioning imaging or electrodiagnostic testing are strong predictors of longer visits. Lab-only orders show only a modest effect. This is cross-validated by the Cardiology and Orthopedics departments (which order imaging and ECG monitoring most frequently).

### 2.2 `specialist_consult_triggered` (TAPP)

| Consult Type | Mean Duration (min) | Long-Visit Rate |
|-------------|-------------------|----------------|
| emergent_intravisit_consult | 43.9 | **94.4%** (17/18) |
| multiple_referrals | 30.0 | 50.0% (2/4) |
| single_referral | 24.2 | 25.8% (8/31) |
| not_present | 23.8 | 26.9% (53/197) |

Emergent intra-visit consultation — documented in the note as an urgent specialist call during the visit — is the single clearest process-level signal (94.4% long-visit rate, mean 43.9 min). Planned single referrals show no duration premium over visits with no referral.

### 2.3 `chronic_disease_count` & `outbound_referral_count` (TAPP, Numeric)

- **`chronic_disease_count`** correlates with duration at $r = 0.37$; visits with 2 chronic conditions average 32.5 min vs. 24.3 min for 1 condition (n = 32 vs. 53).  
- **`outbound_referral_count`** correlates at $r = 0.26$; visits generating 2+ referrals average 32.1 min (n = 24) vs. 27.4 min for 1 referral and 23.3 min for none.

### 2.4 `new_diagnosis_flag` (TAPP)

| Flag | Mean Duration (min) |
|------|-------------------|
| new_diagnosis | 28.0 (n = 119) |
| ongoing_followup | 25.1 (n = 72) |
| not_present | 20.4 (n = 37) |
| new_initiation_of_treatment | 18.8 (n = 16) |

A new diagnosis mentioned in the note (+7.6 min vs. no flag) is a moderate signal, but is partly colinear with `clinical_severity_level` and `visit_type`.

---

## 3. Weak or Secondary Signals

| Column | Finding |
|--------|---------|
| `new_medication_initiated` | Multiple medication changes: 29.3 min mean vs. 25.4 overall — weak effect, limited sample (n = 21). |
| `counseling_topic` | Visits coded `not_present` (no documented counseling topic) actually average **35.3 min** — these are predominantly high-severity emergency visits where counseling was not the focus. Not a reliable independent signal. |
| `age_group` | Patients 60+ average 29.5 min vs. 19.9 min for 0–17, but effect is largely mediated by `chronic_disease_count` and `clinical_severity_level`. |

---

## 4. Summary: Visit-Note Signals Ranked by Strength

| Rank | Signal | Type | Effect Size |
|------|--------|------|------------|
| 1 | `urgency = Emergency` | Structured | +22 min vs. Routine; 100% long-visit rate |
| 2 | `visit_type = emergency_or_urgent_care` | TAPP | 100% long-visit rate, mean 44.5 min |
| 3 | `clinical_severity_level ≥ 4` | TAPP | 87–94% long-visit rate |
| 4 | `specialist_consult_triggered = emergent_intravisit_consult` | TAPP | 94.4% long-visit rate, mean 43.9 min |
| 5 | Department = Cardiology or Emergency | Structured | 100% long-visit rate |
| 6 | `diagnostic_test_ordered = imaging or electrodiagnostic` | TAPP | 66–89% long-visit rate |
| 7 | `visit_type = chronic_disease_followup` | TAPP | 42.4% long-visit rate |
| 8 | `chronic_disease_count ≥ 2` | TAPP | $r = 0.37$; +8 min vs. 1 condition |
| 9 | `new_diagnosis_flag = new_diagnosis` | TAPP | +7.6 min vs. not_present |
| 10 | `outbound_referral_count ≥ 2` | TAPP | $r = 0.26$; mean 32.1 min |

**Key takeaway:** The strongest visit-note signals for longer duration are (a) emergency/urgent acuity language in the note (`clinical_severity_level` 4–5, `visit_type = emergency_or_urgent_care`), (b) an emergent intra-visit specialist consultation, and (c) notes documenting imaging or electrodiagnostic workup. Chronic disease burden (`chronic_disease_count`, `visit_type = chronic_disease_followup`) represents a secondary but consistent driver. Preventive and well-child notes are uniformly short (0% long-visit rate).
