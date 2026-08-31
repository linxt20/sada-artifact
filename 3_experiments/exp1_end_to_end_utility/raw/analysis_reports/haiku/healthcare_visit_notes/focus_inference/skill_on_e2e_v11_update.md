---
dataset: healthcare_visit_notes
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What are the main types of concerns patients come in with in these visit notes?"
source_table: augment_table/healthcare_visit_notes/focus_inference/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:22:31.148902+00:00
wall_seconds: 82.34
---

# Analysis Report: Main Types of Patient Concerns in Healthcare Visit Notes

## Executive Summary

Analysis of 250 healthcare visit records reveals a clear distribution of patient concerns that prioritizes acute diagnosis and new presentations, complemented by ongoing chronic disease management and preventive care. The augmented dataset identifies **seven primary concern types** using the TAPP-generated column `concern_type`, with **acute diagnosis** dominating at 46% of all visits, followed by chronic management and routine monitoring concerns.

## Methods

**TAPP-Generated Columns Used:**
- `concern_type` – semantic classification of patient's primary visit concern
- `clinical_domain` – healthcare specialty/department  
- `visit_stage_in_continuum` – position in clinical care pathway

All three columns achieved 100% coverage across the augmented table (250/250 records). The analysis combines TAPP-generated semantic facets with original structured variables (department, urgency, age_group, visit_duration_min) to answer the query comprehensively.

---

## Findings

### 1. Main Types of Patient Concerns

The **concern_type** column identifies seven distinct categories of patient concerns:

| Concern Type | Count | Percentage | Key Characteristics |
|---|---|---|---|
| **Acute Diagnosis** | 115 | 46.0% | New symptoms, active illness, diagnostic workup |
| **Chronic Management** | 37 | 14.8% | Ongoing disease monitoring, medication adjustment |
| **Routine Monitoring** | 34 | 13.6% | Preventive check-ups, well-visits, stable condition surveillance |
| **Follow-up Stable** | 29 | 11.6% | Post-intervention recovery, stable disease progression |
| **Injury/Trauma** | 16 | 6.4% | Acute physical injuries requiring evaluation/treatment |
| **Preventive Screening** | 15 | 6.0% | Cancer screening, preconception, health risk assessment |
| **Infectious Process** | 4 | 1.6% | Active infection requiring antimicrobial intervention |

**Dominant Pattern:** Nearly 3 in 5 visits (46%) involve acute diagnosis—patients presenting with new or active clinical concerns requiring immediate evaluation and management.

### 2. Acute Diagnosis: The Largest Concern Category (46%)

**Acute diagnosis** represents the largest concern type at 115 visits. These range in severity and urgency:

**Severity Distribution (by urgency level):**
- **Emergency** visits: 25 cases (acute_diagnosis at 89% of all emergency visits)
  - Examples: STEMI (ST-elevation MI), subarachnoid hemorrhage, acute respiratory failure, anaphylaxis
- **Urgent** visits: 63 cases  
  - Examples: new-onset palpitations/AFib, acute dermatologic flares, appendicitis concern, ankle fractures
- **Routine** visits: 27 cases  
  - Examples: acne, eczema flares, new-onset infections (pharyngitis, otitis media)

**Clinical Domains Affected:** Acute diagnosis spans all six specialty domains:
- Dermatology: 29 acute diagnoses (69% of Dermatology visits)
- Emergency: 25 acute diagnoses (89% of Emergency visits)  
- Cardiology: 15 acute diagnoses  
- GeneralPractice: 20 acute diagnoses
- Pediatrics: 18 acute diagnoses
- Orthopedics: 8 acute diagnoses

**Visit Stage Context:** 65 acute diagnosis visits represent **new_presentation** in the care continuum (TAPP column `visit_stage_in_continuum`), while 27 are **acute_exacerbation** of existing conditions and 23 represent **initial_management** of new diagnoses.

**Illustrative Examples:**
- "Severe substernal chest pain radiating to left arm, onset 1 hour ago... ECG shows ST elevation in V2-V4. STEMI protocol activated, cath lab notified" [Emergency, V-0008]
- "8-year-old with abdominal pain and vomiting x12 hours... Tender at McBurney point. Concern for appendicitis, sent to ED for surgical evaluation" [Pediatrics urgent, V-0022]
- "Acute eczema flare on hands, painful fissures and erythema. Likely contact dermatitis from new soap" [Dermatology, V-0025]

---

### 3. Chronic Disease Management: The Secondary Concern (14.8%)

**Chronic management** (37 visits, 14.8%) focuses on ongoing treatment and medication optimization:

**Key Clinical Domains:**
- Orthopedics: 15 visits (38.5% of Orthopedics visits; chronic low back pain, knee/hip arthritis, epicondylitis)
- GeneralPractice: 12 visits (hypertension, diabetes, GERD, smoking cessation, hypothyroidism)
- Cardiology: 7 visits (atrial fibrillation, heart failure, hypertensive cardiomyopathy)
- Dermatology: 3 visits (plaque psoriasis, rosacea, atopic dermatitis maintenance)

**Visit Stage:** 25 represent **chronic_maintenance** and 12 represent **follow_up_post_intervention**.

**Urgency Profile:** All 37 chronic management visits are **Routine** urgency—reflecting stable conditions being monitored during office visits.

**Examples:**
- "Diabetes follow-up. HbA1c 7.4, down from 8.1... Feet exam normal, no neuropathy. Continue plan, recheck in 3 months" [GeneralPractice, V-0006]
- "Chronic low back pain, 6 months duration. No radicular symptoms. Failed PT and NSAIDs... Referral to pain management" [Orthopedics, V-0013]

---

### 4. Routine Monitoring & Well-Visits: Health Surveillance (13.6%)

**Routine monitoring** (34 visits, 13.6%) emphasizes preventive surveillance and health maintenance:

**Primary Domain:**
- Pediatrics: 25 visits (55.6% of all Pediatrics visits; well-child visits at 2-month, 4-month, 6-month, 12-month, 4-year, school readiness intervals)
- GeneralPractice: 7 visits (annual physical exams, medication management for stable conditions)
- Cardiology: 2 visits (pacemaker checks, stable chronic disease surveillance)

**Visit Stage:** 33 visits classified as **preventive_wellness**; represents proactive health oversight rather than acute response.

**Urgency:** Nearly all (33 of 34) are **Routine** urgency; only one is **Urgent**.

**Examples:**
- "Well-child visit at 4 years. Growth on track at 50th percentile. Immunizations updated with DTaP and MMR booster" [Pediatrics, V-0007]
- "Annual physical exam... BP 128/82, BMI 27. Labs ordered including lipid panel and HbA1c" [GeneralPractice, V-0001]

---

### 5. Injury and Trauma: Acute Mechanical Concerns (6.4%)

**Injury/trauma** (16 visits, 6.4%) encompasses acute physical injuries requiring orthopedic or emergency intervention:

**Distribution by Urgency:**
- Urgent: 12 cases (acute ligament injuries, fractures, tendon ruptures)  
- Emergency: 3 cases (open fractures, MVAs with LOC concern, lacerations)
- Routine: 1 case (chronic wart)

**Mechanism Examples:**
- Sports injuries: ankle sprains, shoulder dislocations, Achilles rupture, hamstring tear
- Falls: hip fractures (intertrochanteric), wrist fractures, compression fractures
- Motor vehicle accidents: lacerations, possible LOC
- Occupational: wrist injuries

**Clinical Domain:** Orthopedics accounts for 12 of 16 injury cases (75%); Emergency accounts for 3.

**Age Distribution:** Injury cases span 18-39 age group (10 cases), 40-59 (3 cases), 60+ (2 cases), and 0-17 (1 case).

---

### 6. Preventive Screening: Proactive Disease Detection (6.0%)

**Preventive screening** (15 visits, 6.0%) targets asymptomatic disease detection and risk assessment:

**Modalities:**
- Dermatology screening: 5 visits (skin cancer, actinic keratosis surveillance)  
- GeneralPractice screening: 9 visits (cancer screening, preconception counseling, colonoscopy scheduling, mammography)
- Cardiology screening: 1 visit (coronary artery disease risk stratification)

**All visits are Routine urgency** and classified as **preventive_wellness** or **screening** visit stages.

**Examples:**
- "Routine skin cancer screening. Multiple seborrheic keratoses noted, no concerning lesions. Annual follow-up recommended" [Dermatology, V-0020]
- "Preconception counseling. Folic acid 400mcg daily started. Reviewed avoidance of teratogens" [GeneralPractice, V-0033]

---

### 7. Infectious Processes: Uncommon but Urgent (1.6%)

**Infectious process** (4 visits, 1.6%) represents active infections requiring antimicrobial therapy:

**Cases:**
- Streptococcal pharyngitis [GeneralPractice, V-0011, Urgent]
- Acute otitis media [Pediatrics, V-0012, Urgent]
- Impetigo [Pediatrics, V-0204, Urgent]
- Erysipelas [Dermatology, V-0208, Urgent]

**All four are Urgent visits.** Despite small sample size, they represent a distinct clinical phenotype warranting targeted intervention.

---

### 8. Follow-up Stable: Post-Intervention Surveillance (11.6%)

**Follow-up stable** (29 visits, 11.6%) addresses recovery and disease stability after major interventions:

**Primary Domain:** Cardiology dominates with 17 visits (40.5% of Cardiology visits)
- Post-MI follow-up (month 6)
- Pacemaker checks (1-year interrogation)
- Post-CABG surveillance
- Hypertensive cardiomyopathy monitoring

**Other Domains:**
- Orthopedics: 4 visits (post-TKR, post-fracture repair)
- GeneralPractice: 5 visits (post-bariatric surgery, osteoporosis post-DEXA)
- Dermatology: 3 visits (post-surgical skin cancer excision)

**Visit Stage:** 37 classified as **follow_up_post_intervention**.

**Urgency:** 28 Routine, 1 Urgent—reflects stable clinical course.

---

## Cross-Cutting Patterns

### Pattern 1: Department-Specific Concern Profiles

Each clinical domain shows distinct concern distributions:

| Department | Top 3 Concerns | Clinical Implications |
|---|---|---|
| **Emergency (n=28)** | Acute diagnosis 89%, injury 11% | Crisis management orientation |
| **Dermatology (n=42)** | Acute diagnosis 69%, preventive screen 12%, chronic mgmt 7% | Mix of acute flares and proactive surveillance |
| **Orthopedics (n=39)** | Chronic mgmt 38%, acute diagnosis 21%, injury 31% | High injury acuity; chronic joint disease |
| **Pediatrics (n=45)** | Routine monitoring 56%, acute diagnosis 40% | Preventive emphasis; limited chronic disease |
| **Cardiology (n=42)** | Follow-up stable 40%, acute diagnosis 36%, chronic mgmt 17% | High post-intervention follow-up burden |
| **GeneralPractice (n=54)** | Acute diagnosis 37%, chronic mgmt 22%, preventive screen 17% | Generalist scope; diverse concerns |

### Pattern 2: Age-Related Concern Shifts

- **0-17 years (n=46):** Routine monitoring dominates (54% of pediatric visits); acute diagnosis 39%; minimal chronic management
- **18-39 years (n=57):** Injury/trauma emerges (18% of this cohort); acute diagnosis peaks at 47%; minimal chronic disease
- **40-59 years (n=60):** Balanced acute (48%) and chronic (22%); emerging preventive screening (12%)
- **60+ years (n=87):** Follow-up stable becomes significant (23%); acute diagnosis remains high (47%); chronic management 21%

### Pattern 3: Urgency-Concern Alignment

- **Acute diagnosis** spans all urgency levels (Emergency 22%, Urgent 55%, Routine 23%)
- **Injury/trauma** concentrated in Urgent (75%) and Emergency (19%)
- **Chronic management, preventive screening, routine monitoring** restricted to Routine urgency
- **Infectious process** entirely Urgent (100%)

---

## Quantified Summary of Visit Characteristics

**By Concern Type (median visit duration and age group concentration):**

| Concern Type | Median Duration (min) | Predominant Age Group | Urgency Profile |
|---|---|---|---|
| Acute diagnosis | 20 | 60+ (36% of acute visits) | Urgent 55% |
| Injury/trauma | 25 | 18-39 (63% of trauma visits) | Urgent 75% |
| Chronic management | 25 | 60+ (49% of chronic visits) | Routine 100% |
| Follow-up stable | 30 | 60+ (69% of follow-up visits) | Routine 97% |
| Routine monitoring | 20 | 0-17 (74% of routine visits) | Routine 97% |
| Preventive screening | 20 | 18-39 (40% of screening visits) | Routine 100% |
| Infectious process | 20 | Varied | Urgent 100% |

---

## Data Quality

All TAPP-generated columns achieved complete coverage:
- `concern_type`: 250/250 (100%)
- `clinical_domain`: 250/250 (100%)
- `visit_stage_in_continuum`: 250/250 (100%)

The augmented dataset provides unambiguous, actionable semantic labeling that complements the original structured fields.

---

## Conclusion

Patients come to these healthcare settings with **seven distinct types of concerns**, with **acute diagnosis (46%)** as the overwhelming focus—representing new or active illness requiring diagnostic and therapeutic response. This is followed by chronic disease management (15%) and routine preventive surveillance (14%), together representing the full spectrum of medical care. Injury and trauma (6%), preventive screening (6%), post-intervention follow-up (12%), and infectious processes (2%) complete the profile. The distribution varies significantly by clinical specialty and patient age, reflecting appropriate clinical differentiation across the healthcare system.
