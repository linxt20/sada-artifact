---
dataset: healthcare_visit_notes
scenario: concept_attribute_patient
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "patient_needs"
query: "What patient needs appear in visit notes?"
source_table: augment_table/healthcare_visit_notes/concept_attribute_patient/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:21:58.892709+00:00
wall_seconds: 65.59
---

# Patient Needs in Healthcare Visit Notes — Analysis Report

**Query:** What patient needs appear in visit notes?  
**Dataset:** 250 visit notes across 6 departments  
**Date:** 2026-07-30

---

## Method Note

TAPP-generated columns used: `clinical_problem_type`, `acuity_complexity`, `care_action_required`, `diagnostic_workup_need`, `medication_need_type`, `preventive_or_wellness_need`. The columns `specialist_involvement` and `specialist_or_ancillary_involvement` were identical to the original `department` field and provided no additional signal; they are noted but not centered in the analysis.

---

## 1. Overview of Patient Need Categories

The 250 visit notes span four primary need types identified via `clinical_problem_type`:

| Clinical Problem Type | Count | % of Visits | Median Duration (min) |
|---|---|---|---|
| Chronic disease management | 94 | 37.6% | 25 |
| Acute illness | 81 | 32.4% | 30 |
| Preventive / wellness | 40 | 16.0% | 20 |
| Injury or trauma | 19 | 7.6% | 30 |
| Screening / surveillance | 8 | 3.2% | 15 |
| Surgical/procedural follow-up | 8 | 3.2% | 25 |

**Chronic disease management** is the most prevalent need (94/250, 38%), concentrated in Routine-urgency visits (84/94). **Acute illness** is the second largest need (81/250, 32%) and drives most Urgent visits (53/81) and nearly all Emergency visits (25/28 Emergency-flagged notes).

---

## 2. Acuity and Complexity of Needs

Using `acuity_complexity`, most visits are low-to-moderate complexity:

| Acuity Level | Count | % |
|---|---|---|
| Low acuity / routine | 103 | 41% |
| Moderate acuity | 96 | 38% |
| High acuity / urgent | 33 | 13% |
| Life-threatening | 18 | 7% |

High-acuity and life-threatening visits (51 combined) align strongly with Emergency department visits (28) and urgent Cardiology cases (10 high-acuity in Cardiology). The 18 life-threatening visits generated 19 hospital admissions (with 1 cross-department admission), confirming strong internal consistency between `acuity_complexity` and original `urgency`.

---

## 3. Care Actions Required

`care_action_required` identifies what the patient concretely needed from the encounter:

| Care Action | Count | Routine | Urgent | Emergency |
|---|---|---|---|---|
| Monitoring / counseling only | 81 | 60 | 19 | 2 |
| Medication initiation or change | 69 | 29 | 40 | 0 |
| Procedure or intervention | 46 | 36 | 9 | 1 |
| Hospital admission / transfer | 25 | 1 | 5 | 19 |
| Surgical consultation / referral | 21 | 10 | 6 | 5 |
| Imaging or labs ordered | 8 | 5 | 2 | 1 |

**Medication change** (69 visits, 28%) is the most action-intensive non-emergency need—driven largely by urgent chronic/acute illness cases. **Monitoring and counseling** (81 visits, 32%) is the most common action overall and dominates Routine visits. **Hospital admission** (25 visits) is almost exclusively an Emergency-department need (19/25 = 76%).

---

## 4. Medication Needs

`medication_need_type` was populated for 139/250 visits (56%); 111 visits had no medication need. Among those with a medication need:

| Medication Need | Count | Primary Age Group |
|---|---|---|
| New prescription | 51 | 18–39 (17), 40–59 (16), 60+ (16) |
| Procedural/emergency medication | 34 | 60+ (15), 18–39 (9), 40–59 (9) |
| Chronic disease medication | 28 | 60+ (17) |
| Antibiotic | 13 | Evenly distributed |
| Dose adjustment / switch | 9 | 60+ (6) |
| Medication discontinued | 4 | 60+ (3) |

Older patients (60+) show the heaviest medication burden: 17/28 chronic disease medications, 15/34 procedural/emergency medications, and 6/9 dose adjustments. New prescriptions are distributed across working-age adults (18–59).

---

## 5. Diagnostic Workup Needs

`diagnostic_workup_need` shows that 152/250 visits (61%) required **no diagnostic workup**. For the 98 visits requiring workup:

| Workup Type | Count | Key Department |
|---|---|---|
| Multi-modal | 32 | Orthopedics (10), Cardiology (5) |
| Laboratory | 26 | Cardiology (10 combined with imaging) |
| Imaging | 25 | Cardiology (10), Orthopedics (7) |
| Functional/procedural test | 11 | Cardiology (9) |
| Biopsy / pathology | 4 | Dermatology (4) |

Cardiology and Orthopedics drive the majority of diagnostic workup needs. Dermatology's diagnostic need is almost entirely biopsy/pathology. General Practice, Pediatrics, and Dermatology dominate the "none ordered" group.

---

## 6. Preventive and Wellness Needs

`preventive_or_wellness_need` is present in only 54/250 visits (22%). Most visits (196/250, 78%) have no preventive component. Among those with a need:

| Preventive Need | Count | Age Group Concentration |
|---|---|---|
| Immunization | 20 | 0–17 (16/20) |
| Cancer screening | 12 | 40–59 (7), 60+ (4) |
| Lifestyle counseling | 11 | 18–39 (5), 60+ (4) |
| Anticipatory guidance | 6 | 0–17 (6/6) |
| Chronic disease prevention | 2 | 40–59 |
| Reproductive/preconception | 3 | 18–39 (3/3) |

Preventive needs are strongly age-stratified: **immunizations and anticipatory guidance** concentrate in children (0–17); **cancer screening** peaks in middle-age and older adults (40–59, 60+); **reproductive counseling** is exclusive to 18–39.

---

## 7. Summary: Patient Need Profile

| Need Dimension | Dominant Pattern |
|---|---|
| Problem type | Chronic disease management (38%) and acute illness (32%) account for 70% of visits |
| Acuity | 79% low-to-moderate; high/life-threatening concentrated in Emergency and Cardiology |
| Care action | Monitoring/counseling (32%) and medication change (28%) are the most common responses |
| Medication | 56% of visits involve a medication need; 60+ patients have the highest chronic medication burden |
| Diagnostics | 39% of visits require workup; Cardiology and Orthopedics are primary consumers |
| Prevention | Present in 22% of visits; age-stratified (immunizations in children, screening in adults 40+) |
| Visit duration | Acute illness and trauma require the most time (≈29 min avg); screening is shortest (≈18 min) |
