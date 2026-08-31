---
dataset: healthcare_visit_notes
scenario: concept_attribute_patient
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "patient_needs"
query: "What patient needs appear in visit notes?"
source_table: augment_table/healthcare_visit_notes/concept_attribute_patient/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:21:35.194988+00:00
wall_seconds: 42.78
---

# Patient Needs in Visit Notes — Analysis Report

**Dataset:** `sonnet__skill_on_v11_update.csv` | **Records:** 250 visits | **Date:** 2026-07-30

---

## Overview

Patient needs are captured across four structured dimensions in this dataset: **intervention type**, **specialist referral**, **diagnostic workup**, and **preventive/screening needs**. Together these columns paint a comprehensive picture of what patients require at each visit.

---

## 1. Intervention Needs

The `intervention_need_type` column is the primary indicator of active patient need:

| Intervention Type | Count | % of Visits |
|---|---|---|
| Procedure performed | 91 | 36.4% |
| Medication initiated | 62 | 24.8% |
| Observation only | 54 | 21.6% |
| Conservative management | 32 | 12.8% |
| Medication adjusted | 11 | 4.4% |

- **Procedural need** is the most common, driven heavily by emergency stabilization visits (all 30 emergency visits required a procedure) and preventive wellness visits (23/36 involved procedures, likely immunizations or screenings).
- **Medication initiation** is most frequent in acute complaints and chronic disease management.
- **Observation-only** needs (21.6%) represent lower-acuity monitoring visits; these cluster in ongoing follow-up and surveillance stages.

---

## 2. Specialist Referral Needs

The majority of visits (189/250, **75.6%**) did not require specialist referral. Among those that did:

| Referral Type | Count |
|---|---|
| Surgical | 20 |
| Other specialist | 16 |
| Cardiology/EP | 8 |
| Orthopedics | 5 |
| Neurology/Neurosurgery | 4 |
| Mental health | 4 |
| Addiction services | 2 |
| Pain management | 1 |
| Dermatology specialist | 1 |

Surgical referral is the most common specialty need (8% of all visits), consistent with the dataset's high prevalence of musculoskeletal (44 visits) and orthopedic cases. Mental health and addiction services referrals are present but underrepresented (6 combined), suggesting possible documentation gaps rather than true low prevalence.

---

## 3. Diagnostic Workup Needs

Most visits (147/250, **58.8%**) required no additional diagnostics. Among those with workup needs:

| Workup Type | Count |
|---|---|
| Imaging ordered | 36 |
| Lab ordered | 31 |
| Multiple modalities | 22 |
| ECG/Holter | 6 |
| Functional test | 4 |
| Pathology/Biopsy | 4 |

Imaging and lab orders are roughly equal, together accounting for ~27% of visits. Multi-modality workup (22 visits) aligns with higher acuity cases. The 14 records with `Unknown` clinical problem type may affect workup coding accuracy.

---

## 4. Preventive and Screening Needs

Most visits (197/250, **78.8%**) had no preventive need coded. Where present:

| Preventive Need | Count |
|---|---|
| Immunization | 18 |
| Cancer screening | 13 |
| Lifestyle counseling | 12 |
| Metabolic screening | 6 |
| Preconception/family planning | 3 |
| Travel medicine | 1 |

Immunization is the leading preventive need, concentrated in the Pediatrics department (45 visits). Lifestyle counseling and metabolic screening are underrepresented given the dataset's 87 acute and 76 chronic disease visits — these may be undercoded.

---

## 5. Need Intensity by Acuity and Visit Purpose

- **High-acuity visits (levels 4–5, n=42):** 38/42 required a procedure; 28/42 needed specialist referral — predominantly surgical or other specialist. These represent the highest-burden patients.
- **New problems (n=134, 53.6%):** Dominate the dataset, with the widest mix of intervention types — medication initiation, conservative management, and procedures all represented.
- **Chronic disease management (n=76):** Predominantly observation or medication adjustment, with moderate diagnostic needs (lab and imaging).
- **Emergency stabilization (n=30):** Exclusively procedural intervention; highest concentration of complex multi-modal workup.

---

## 6. Key Exceptions and Caveats

- **14 records have `Unknown` clinical problem type**, potentially suppressing diagnostic and specialist coding for those visits.
- **Mental health and addiction needs are likely undercoded** — only 6 referrals combined despite a psychiatric/behavioral problem type of 4 and no standalone mental health visit purpose category.
- **`preventive_or_screening_need` is absent in 78.8% of visits**, even among chronic disease and routine wellness encounters where lifestyle counseling would be expected — suggesting conservative annotation rather than true absence.

---

## Summary

The dominant patient needs in these visit notes are **procedural intervention** (36%), **medication initiation** (25%), and **diagnostic workup** (41% of visits). Specialist referral is needed in ~25% of cases, led by surgical needs. Preventive needs are present but likely underdocumented. High-acuity and emergency visits concentrate the most complex, multi-dimensional needs.
