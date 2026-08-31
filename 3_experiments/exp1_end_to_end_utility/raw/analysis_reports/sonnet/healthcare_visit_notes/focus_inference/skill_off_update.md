---
dataset: healthcare_visit_notes
scenario: focus_inference
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What are the main types of concerns patients come in with in these visit notes?"
source_table: augment_table/healthcare_visit_notes/focus_inference/sonnet__skill_off_update.csv
generated_at: 2026-07-28T12:42:31.306819+00:00
wall_seconds: 34.64
---

# Patient Concern Types in Healthcare Visit Notes

## Overview

The dataset contains **250 visit notes** across 6 departments (General Practice, Pediatrics, Cardiology, Dermatology, Orthopedics, Emergency). The `concern_category` column directly encodes the type of concern, grounded in the free-text `reason_for_visit` and `chief_complaint` fields. Visits skew routine (141 / 56%) over urgent (81 / 32%) and emergency (28 / 11%).

---

## Main Concern Categories

| Rank | Concern Category | Count | % of Visits |
|------|-----------------|-------|-------------|
| 1 | **Musculoskeletal / Pain** | 44 | 17.6% |
| 2 | **General / Other** | 39 | 15.6% |
| 3 | **Cardiovascular** | 34 | 13.6% |
| 4 | **Preventive Care / Wellness** | 26 | 10.4% |
| 5 | **Mental Health** | 21 | 8.4% |
| 6 | **Dermatology** | 20 | 8.0% |
| 7 | **Infectious Disease** | 13 | 5.2% |
| 8 | **Endocrine / Metabolic** | 11 | 4.4% |
| 9 | **Respiratory** | 11 | 4.4% |
| 10 | **Ophthalmology / ENT** | 11 | 4.4% |
| 11 | **Gastrointestinal** | 8 | 3.2% |
| 12 | **Neurological** | 7 | 2.8% |
| 13 | **Genitourinary / Reproductive** | 3 | 1.2% |
| 14 | **Oncology** | 2 | 0.8% |

---

## Key Findings

### Dominant Concerns (top 3 account for ~47%)
- **Musculoskeletal / Pain** is the single largest category (17.6%), consistent with the Orthopedics department being one of the larger cohorts (39 visits). Complaints include joint pain, back pain, fractures, and sports injuries.
- **General / Other** (15.6%) captures undifferentiated presentations seen mainly in General Practice — fatigue, multi-system complaints, and follow-ups that don't map neatly to a specialty.
- **Cardiovascular** (13.6%) is driven largely by the Cardiology cohort (42 visits); chief complaints include chest pain, arrhythmias, hypertension management, and post-MI follow-ups.

### Mid-Tier Concerns (~27% combined)
- **Preventive Care / Wellness** (10.4%): annual physicals, immunizations, and screening labs — almost exclusively routine visits.
- **Mental Health** (8.4%): anxiety, depression, and stress-related presentations, appearing across General Practice and Pediatrics notes.
- **Dermatology** (8.0%): acne, eczema, rashes, and skin lesion evaluations, tightly aligned with the Dermatology department cohort.

### Smaller but Clinically Meaningful Categories
- Infectious Disease (5.2%), Respiratory (4.4%), and Ophthalmology/ENT (4.4%) cluster around acute/urgent visits (cough, URI, ear infections, eye complaints).
- Endocrine/Metabolic (4.4%) covers diabetes management and thyroid issues, often surfacing as secondary findings during annual exams.

---

## Caveats & Weak Evidence

- **"General / Other" (15.6%)** is a catch-all that may mask more specific sub-patterns; the `reason_for_visit` text shows heterogeneous complaints with no single dominant thread.
- **Oncology (0.8%, n=2)** and **Genitourinary / Reproductive (1.2%, n=3)** are too sparse for reliable pattern inference.
- The dataset's department composition (no Psychiatry, Gastroenterology, or Neurology departments) likely suppresses the true prevalence of Mental Health, GI, and Neurological concerns relative to a real-world population.
- `concern_category` appears to be an augmented/derived column rather than a raw EHR field; classification accuracy may vary for ambiguous multi-complaint notes.

---

## Summary

The **most prevalent concern types** are musculoskeletal/pain, cardiovascular, and preventive care/wellness — reflecting a mix of specialty follow-up care and primary care demand. Mental health concerns represent a notable 8.4% of visits. Acute infectious/respiratory complaints are present but underrepresented relative to their expected population burden, likely due to the routine-visit skew of this dataset.
