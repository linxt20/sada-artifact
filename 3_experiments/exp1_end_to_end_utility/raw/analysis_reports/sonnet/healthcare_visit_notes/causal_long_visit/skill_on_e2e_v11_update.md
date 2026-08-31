---
dataset: healthcare_visit_notes
scenario: causal_long_visit
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "visit_duration_min"
query: "Which clinical factors best explain longer visit durations?"
source_table: augment_table/healthcare_visit_notes/causal_long_visit/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:22:03.210339+00:00
wall_seconds: 88.71
---

# Clinical Factors Explaining Longer Visit Durations
**Dataset:** 250 visits across 6 departments | **Outcome:** `visit_duration_min` (mean 25.4 min, IQR 20–30, range 15–60)

---

## Method Note

TAPP-generated columns used in this analysis: `visit_type_category`, `condition_acuity`, `procedure_performed`, `admission_or_urgent_referral`, `counseling_complexity`, `multimorbidity_or_polypharmacy`, `multimorbidity_signal`. Effect sizes (η²) are reported as variance explained by each factor in visit duration.

---

## Summary of Factor Strength (η²)

| Factor | Source | η² | Notes |
|---|---|---|---|
| `department` | Original | **0.837** | Strongest single predictor |
| `visit_type_category` | TAPP | **0.630** | Largely co-linear with dept/urgency |
| `urgency` | Original | **0.622** | Emergency class drives effect |
| `condition_acuity` | TAPP | **0.609** | Strong, adds acuity gradient within dept |
| `admission_or_urgent_referral` | TAPP | **0.539** | Captures disposition intensity |
| `counseling_complexity` | TAPP | **0.235** | Moderate; confounded by Emergency dept |
| `age_group` | Original | **0.148** | Modest independent effect |
| `multimorbidity_or_polypharmacy` | TAPP | **0.087** | Weak; partially redundant |

---

## 1. Department (Original) — Strongest Predictor (η² = 0.84)

Department explains ~84% of duration variance and is the dominant structural factor.

| Department | Mean (min) | Median | N |
|---|---|---|---|
| Emergency | **45.5** | 45.0 | 28 |
| Cardiology | 30.1 | 30.0 | 42 |
| Orthopedics | 25.9 | 25.0 | 39 |
| GeneralPractice | 21.9 | 20.0 | 54 |
| Pediatrics | 19.9 | 20.0 | 45 |
| Dermatology | **17.0** | 15.0 | 42 |

Emergency is 2.6× longer than Dermatology on average. Cardiology and Orthopedics are the longest non-emergency departments.

---

## 2. Urgency (Original) + Visit Type Category (TAPP) — Both η² ≈ 0.62

Urgency level (`Emergency` category) drives the bulk of long visits, but offers limited granularity within Routine/Urgent tiers (mean 22.6 vs 23.2 min, nearly identical).

The TAPP `visit_type_category` adds semantic gradient within that space:

| visit_type_category | Mean (min) | Median | N |
|---|---|---|---|
| emergency_critical | **43.7** | 45.0 | 31 |
| acute_injury | 26.1 | 25.0 | 14 |
| chronic_disease_followup | 24.7 | 25.0 | 101 |
| acute_illness | 20.7 | 20.0 | 49 |
| procedure_only | 20.5 | 20.0 | 10 |
| wellness_preventive | 20.1 | 20.0 | 45 |

`emergency_critical` closely mirrors the Emergency department cluster. Among non-emergency types, `chronic_disease_followup` (n=101, the largest group) runs ~4–5 min longer than `acute_illness` or `wellness_preventive`, which is meaningful at scale.

---

## 3. Condition Acuity (TAPP) — η² = 0.61, Strong Gradient

`condition_acuity` adds a monotonic dose-response that is not directly available in the original columns:

| condition_acuity | Mean (min) | Median | % Long (≥30 min) | N |
|---|---|---|---|---|
| life_threatening | **48.5** | 50.0 | **94.1%** | 17 |
| high_acuity | 31.9 | 30.0 | 82.8% | 29 |
| moderate_acuity | 24.6 | 25.0 | 33.8% | 68 |
| low_acuity | 21.9 | 20.0 | 17.2% | 99 |
| not_present | 20.1 | 20.0 | 0.0% | 37 |

Nearly all life-threatening and high-acuity visits are long (≥30 min), while only 17% of low-acuity visits exceed that threshold. This gradient holds even within the Emergency department and clarifies why some Cardiology visits (high post-MI acuity) average 30 min.

---

## 4. Admission / Referral Disposition (TAPP) — η² = 0.54

`admission_or_urgent_referral` captures the downstream intensity of a visit and independently predicts duration:

| admission_or_urgent_referral | Mean (min) | N |
|---|---|---|
| hospital_admission | **43.7** | 26 |
| urgent_surgical_referral | **36.2** | 8 |
| routine_referral | 23.6 | 21 |
| discharge_only | 22.7 | 193 |
| urgent_er_transfer | 20.0 | 2 |

Visits ending in hospital admission or urgent surgical referral are ~20 min longer than simple discharges. Cross-checking with `condition_acuity`: all 13 life-threatening hospital admissions and 6 of 8 urgent surgical referrals originated from high- or life-threatening acuity cases.

---

## 5. Age Group (Original) — η² = 0.15, Modest Effect

Older patients have longer visits, likely mediated by chronic disease burden:

| age_group | Mean (min) | N |
|---|---|---|
| 60+ | **29.5** | 87 |
| 40–59 | 25.3 | 60 |
| 18–39 | 23.5 | 57 |
| 0–17 | 19.9 | 46 |

The 10-min gap between 60+ and pediatric patients is partly explained by `chronic_disease_followup` being concentrated in older cohorts (Cardiology, GeneralPractice).

---

## 6. Counseling Complexity (TAPP) — η² = 0.24, Partially Confounded

Counter-intuitively, `low_or_none` counseling visits have the highest mean duration (32.7 min vs. 24.0 for high_counseling). This is confounded by composition: 24 of 66 `low_or_none` visits are in Emergency (mean 47.5 min), where counseling is minimal but acuity is high. After accounting for department, this TAPP column does not add an independent signal above acuity and urgency.

---

## 7. Multimorbidity / Polypharmacy (TAPP) — η² = 0.09, Weak

`multimorbidity_or_polypharmacy` shows a modest lift for `multiple_active_conditions` (mean 29.4 min, n=60 vs. 24.7 for single-condition). However, the effect is partially explained by age group (60+ concentration) and `chronic_disease_followup` visit type. With η² = 0.087, it is a minor independent contributor and should not be prioritized over acuity or department.

---

## 8. Procedure Performed (TAPP) — Counterintuitive, Low Signal

`procedure_performed` does not add visit time in this dataset; `no_procedure` visits average 26.5 min vs. 21.4 for minor procedures. This likely reflects selection: procedures occur mostly in low-acuity Dermatology and Orthopedics outpatient contexts while no-procedure visits include high-acuity Emergency cases.

---

## Key Findings

**The three strongest independent explanatory factors for longer visit duration are:**

1. **Department** (η² = 0.84): Emergency and Cardiology departments have structurally longer visits. This is the dominant predictor.
2. **Condition acuity** (`condition_acuity`, TAPP, η² = 0.61): Life-threatening and high-acuity visits are nearly universally long (83–94% exceed 30 min), adding a clinical severity gradient not captured by department or urgency alone.
3. **Disposition intensity** (`admission_or_urgent_referral`, TAPP, η² = 0.54): Visits requiring hospital admission (+21 min) or urgent surgical referral (+13 min) are substantially longer, reflecting the time required for stabilization and care planning.

Age (60+) and chronic disease follow-up (`visit_type_category`) are secondary contributing factors. Multimorbidity, counseling complexity, and procedure type add minimal incremental explanation once the primary three factors are controlled.
