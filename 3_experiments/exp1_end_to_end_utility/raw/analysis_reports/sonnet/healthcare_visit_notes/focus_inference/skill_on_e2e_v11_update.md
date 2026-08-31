---
dataset: healthcare_visit_notes
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What are the main types of concerns patients come in with in these visit notes?"
source_table: augment_table/healthcare_visit_notes/focus_inference/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:22:13.715184+00:00
wall_seconds: 62.26
---

# Patient Concern Types in Healthcare Visit Notes
**Dataset:** 250 visit notes across 6 departments | **Query:** What are the main types of concerns patients come in with?

---

## Method Note
TAPP-generated columns used in this analysis: `clinical_category`, `visit_purpose`, `problem_acuity`, `chronicity`, `body_system`, `symptom_mechanism`, `care_action_type`, `referral_or_escalation`, `preventive_flag`. Original structured columns `department`, `urgency`, `age_group`, `visit_duration_min`, and `reason_for_visit` serve as primary cross-checks throughout.

---

## 1. Overview: Distribution of Visit Concerns

The 250 visits span 12 `clinical_category` groups. Five categories account for 88% of all visits:

| Clinical Category (`clinical_category`) | N | % | Median Acuity (`problem_acuity` 1–5) | Avg Duration (min) |
|---|---|---|---|---|
| Cardiovascular | 47 | 18.8% | 3 | 30.9 |
| Dermatologic | 42 | 16.8% | 3 | 17.3 |
| Musculoskeletal / Orthopedic | 40 | 16.0% | 3 | 25.5 |
| Preventive / Wellness | 38 | 15.2% | 2 | 20.3 |
| Infectious / Inflammatory | 18 | 7.2% | 2 | 23.6 |
| Metabolic / Endocrine | 13 | 5.2% | 3 | 28.1 |
| Respiratory | 11 | 4.4% | 3 | 31.4 |
| Neurologic | 11 | 4.4% | 3 | 32.3 |
| Gastrointestinal | 10 | 4.0% | 3 | 33.5 |
| Trauma / Injury | 9 | 3.6% | 4 | 32.2 |
| Psychiatric / Behavioral | 7 | 2.8% | 3 | 25.0 |
| Obstetric / Gynecologic | 4 | 1.6% | 2 | 21.3 |

---

## 2. Main Concern Types in Detail

### A. Cardiovascular Concerns (n=47, 18.8%) — Most Common Category
Nearly all cardiovascular visits are concentrated in the Cardiology department (41/47). Two-thirds are **Routine urgency** (32/47), consistent with chronic disease management: 28 of 47 visits fall under `visit_purpose = chronic_disease_management` or `post_procedure_or_post_hospitalization_followup`. The dominant `symptom_mechanism` is `ischemic_or_vascular` (25 visits across the dataset, heavily cardiovascular). Referral/escalation is relatively low (21% referred), confirming stable ongoing management as the typical pattern.

### B. Dermatologic Concerns (n=42, 16.8%)
Dermatology is evenly split between Routine (25) and Urgent (17) visits. `visit_purpose` is predominantly `acute_complaint` (18) or `chronic_disease_management` (18). `symptom_mechanism` is dominated by `inflammatory_or_autoimmune` (32 across the dataset, heavily dermatologic). Visits are shorter on average (17.3 min) — consistent with focused skin examinations. Only 14% are referred elsewhere.

### C. Musculoskeletal / Orthopedic Concerns (n=40, 16.0%)
Mostly seen in Orthopedics (35/40). Split between Routine (23) and Urgent (17). `visit_purpose` spans `acute_complaint` (18), `chronic_disease_management` (12), and surgical evaluation (2). `symptom_mechanism` aligns with `structural_or_mechanical` and `traumatic` patterns. Referral rate is 28%, consistent with surgical consult scheduling.

### D. Preventive / Wellness Visits (n=38, 15.2%)
Almost entirely Routine urgency (37/38) and concentrated in Pediatrics (24) and General Practice (13). `visit_purpose = routine_wellness_or_screening` (38/40 dataset total). Mean `problem_acuity` is low (1.2), `preventive_flag` is active (`screening_or_surveillance` or `immunization`) for most of these visits — these are the 54 visits with non-`not_present` preventive flags. The concern here is absence of disease rather than a presenting complaint.

### E. Infectious / Inflammatory Concerns (n=18, 7.2%)
Nearly all are **Urgent** (15/18) with `visit_purpose = acute_complaint` (18/18). Pediatrics and General Practice dominate. `symptom_mechanism = infectious` (36 dataset total, heavily concentrated here). Referral rate is low (17%), consistent with self-limited illness managed in primary care or pediatrics.

---

## 3. Visit Purpose Cross-Cut

`visit_purpose` provides a complementary lens that cuts across `clinical_category`:

| Visit Purpose | N | Mean Acuity | Avg Urgency Profile |
|---|---|---|---|
| Acute complaint | 107 | 3.4 | Mostly Urgent/Emergency |
| Chronic disease management | 82 | 2.6 | Mostly Routine |
| Routine wellness / screening | 40 | 1.2 | Routine only |
| Post-procedure / post-hospitalization follow-up | 11 | 1.5 | Routine |
| Surgical evaluation / clearance | 5 | 3.2 | Routine |
| Preventive counseling | 4 | 1.3 | Routine |

**Acute complaints** (107/250, 43%) are the single largest purpose group and carry the highest average acuity (3.4/5). **Chronic disease management** (82/250, 33%) is the second-largest cluster, concentrated in cardiovascular, dermatologic, and musculoskeletal categories.

---

## 4. Urgency and Acuity Patterns

- **Routine** visits: 141/250 (56%) — dominated by cardiovascular follow-up, dermatology, orthopedics, and preventive care.  
- **Urgent** visits: 81/250 (32%) — concentrated in infectious/inflammatory, dermatology (acute flares), and musculoskeletal.  
- **Emergency** visits: 28/250 (11%) — highest in trauma/injury (4), neurologic (5), gastrointestinal (5), and respiratory (4). Trauma/injury and neurologic categories have the highest referral/escalation rates (67% and 64% respectively), consistent with emergency transfer or surgical consult needs.

---

## 5. Summary: Main Types of Patient Concerns

| Rank | Concern Type | Key Evidence |
|---|---|---|
| 1 | **Cardiovascular disease management** | 47 visits (19%); mostly routine chronic follow-up; Cardiology dept |
| 2 | **Skin/dermatologic conditions** | 42 visits (17%); mix of acute and chronic; inflammatory mechanism |
| 3 | **Musculoskeletal pain & injuries** | 40 visits (16%); acute and chronic; structural/traumatic mechanisms |
| 4 | **Preventive & wellness** | 38 visits (15%); low acuity; screening/immunization focus |
| 5 | **Acute infectious illness** | 18 visits (7%); all acute complaints; predominantly Urgent urgency |
| 6 | **Metabolic/endocrine disorders** | 13 visits (5%); General Practice; moderate acuity |
| 7 | **Respiratory complaints** | 11 visits (4%); split Emergency/Urgent/Routine |
| 8 | **Neurologic complaints** | 11 visits (4%); high referral rate (64%); longest visits |

> **Key takeaway:** Nearly half of all visits are acute complaints (107/250), but chronic disease management (82/250) represents a substantial second stream. Together, these two `visit_purpose` categories account for 76% of visits. Cardiovascular, dermatologic, and musculoskeletal concerns dominate the volume, while preventive/wellness represents a distinct low-acuity segment largely driven by Pediatrics and General Practice.
