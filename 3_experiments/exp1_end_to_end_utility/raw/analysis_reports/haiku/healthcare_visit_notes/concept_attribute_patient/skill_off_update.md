---
dataset: healthcare_visit_notes
scenario: concept_attribute_patient
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "patient_needs"
query: "What patient needs appear in visit notes?"
source_table: augment_table/healthcare_visit_notes/concept_attribute_patient/haiku__skill_off_update.csv
generated_at: 2026-07-28T12:41:56.666426+00:00
wall_seconds: 59.88
---

# Analysis Report: Patient Needs in Healthcare Visit Notes

**Dataset:** `haiku__skill_off_update.csv`  
**Variant Label:** skill_off  
**Query:** What patient needs appear in visit notes?

---

## Executive Summary

This analysis examines 250 healthcare visit records to identify patient needs as documented in clinical visit notes. The dataset reveals six primary patient need categories spanning preventive, acute, chronic, and emergency care contexts. Patient needs are highly diverse (232 unique specific needs) and stratified by visit urgency, clinical department, and patient age group.

---

## Patient Need Categories: Distribution and Characteristics

### Overall Distribution

The dataset includes **6 broad patient need categories**:

| Category | Count | Percentage | Avg Visit Duration (min) |
|----------|-------|-----------|----------------------|
| Chronic disease management | 77 | 30.8% | 23.1 |
| Urgent care | 60 | 24.0% | 23.4 |
| Preventive care | 58 | 23.2% | 21.4 |
| Emergency/critical care | 28 | 11.2% | 45.5 |
| Acute care | 20 | 8.0% | 22.8 |
| Surgical referral | 7 | 2.8% | 26.4 |

**Key finding:** Chronic disease management and urgent/preventive care account for 78% of all visits, reflecting a healthcare system focused on ongoing disease management and preventive/episodic care alongside emergency services.

---

## Specific Patient Needs: Thematic Analysis

Patient needs were classified into **8 thematic domains** based on content patterns in the `primary_patient_need` column:

### 1. **Disease/Condition Management** (83 unique needs)
The largest thematic category. Includes management of:
- Chronic conditions: diabetes, hypertension, heart failure, atrial fibrillation, COPD
- Dermatologic conditions: psoriasis, acne, eczema, rosacea, tinea
- Neurologic/pain conditions: migraines, neuropathy, chronic pain syndromes

*Evidence:* Examples include "Diabetes monitoring and control," "Chronic pain management," "Rosacea management"

### 2. **Emergency/Acute/Critical Care** (26 unique needs)
High-acuity scenarios requiring immediate intervention:
- Cardiovascular emergencies: myocardial infarction, stroke, sepsis
- Trauma and acute injuries: MVA, open fractures, penetrating wounds
- Metabolic crises: diabetic ketoacidosis, hypoglycemia
- Respiratory emergencies: acute respiratory failure, anaphylaxis

*Evidence:* Examples include "Acute myocardial infarction emergency care," "Septic shock emergency resuscitation," "Acute stroke thrombolytic intervention"

### 3. **Treatment/Therapy** (39 unique needs)
Active treatment delivery for acute or chronic conditions:
- Infection management: bacterial, viral, fungal treatments
- Inflammatory/dermatologic treatments: acne, eczema, dermatitis
- Pain/symptom management: medication escalation, behavioral interventions
- Procedural treatments: injections, cryotherapy, cautery

*Evidence:* Examples include "Acute bacterial skin infection treatment," "Severe acne treatment escalation," "Acute asthma exacerbation treatment"

### 4. **Monitoring/Follow-up/Recovery** (24 unique needs)
Longitudinal care tracking and post-intervention oversight:
- Post-surgical recovery: orthopedic, cardiac, dermatologic procedures
- Post-acute event recovery: cardiac rehabilitation, stroke follow-up
- Medication/device monitoring: pacemaker interrogation, medication effectiveness
- Disease progression tracking: cardiac valve disease, osteoarthritis

*Evidence:* Examples include "Post-surgical knee replacement recovery," "Cardiac recovery monitoring post-MI," "Pacemaker function monitoring"

### 5. **Preventive/Screening/Wellness** (22 unique needs)
Proactive health maintenance and disease prevention:
- Well-child care and immunizations: the largest subcategory
- Cancer screening: skin, colorectal, breast, prostate
- Cardiovascular risk reduction
- Preconception/prenatal counseling

*Evidence:* Examples include "Preventive well-child care and immunization" (16 visits), "Preventive skin cancer screening," "Cardiovascular risk reduction"

### 6. **Evaluation/Diagnosis/Assessment** (4 unique needs)
Diagnostic evaluation for uncertain conditions:
- Fracture evaluation, developmental delay assessment
- Preoperative cardiac clearance
- Benign vascular lesion evaluation

### 7. **Surgical/Procedural Planning** (10 unique needs)
Coordination of surgical or advanced procedural interventions:
- Joint replacement planning (hip, knee)
- Advanced wound/dermatologic surgery
- Cardiac interventions (catheter ablation, valve repair/replacement)

*Evidence:* Examples include "Total hip arthroplasty planning," "Cardiac catheter ablation planning," "Mohs surgery planning"

### 8. **Other/Mixed Needs** (24 unique needs)
Heterogeneous needs including surveillance, optimization, and specialized management

---

## Patient Needs by Clinical Context

### By Department
Department specialization clearly shapes patient needs:

- **Cardiology (n=42):** Dominated by chronic disease management (19) and urgent care (12) — cardiovascular risk management and arrhythmia control
- **Dermatology (n=42):** Mixed chronic disease (20) and urgent skin infections (16) — ranging from rosacea maintenance to melanoma surveillance
- **Orthopedics (n=39):** Chronic disease (18) and urgent care (12) — fracture management, ligament repair, pain control
- **GeneralPractice (n=54):** Most diverse; preventive (18), chronic disease (19), acute (13) — reflects broad scope of primary care
- **Pediatrics (n=45):** Overwhelmingly preventive (26) and urgent (18) — preventive well-child care dominates with immunizations
- **Emergency (n=28):** All emergency/critical care by definition (28)

### By Visit Urgency
Urgency level shows strong correlation with need category (100% alignment):
- **Emergency visits (n=28):** 100% Emergency/critical care needs
- **Urgent visits (n=81):** 74% Urgent care, 25% Acute care
- **Routine visits (n=141):** 55% Chronic disease management, 40% Preventive care

### By Patient Age Group
Age demonstrates differential care patterns:

- **Pediatric (0-17, n=46):** Preventive-focused (57% preventive care); primary needs are well-child visits and immunizations
- **Young adults (18-39, n=57):** Mixed acute and chronic needs; trauma/injury common
- **Middle-age (40-59, n=60):** Beginning of chronic disease management; hypertension, diabetes, cancer screening
- **Older adults (60+, n=87):** Predominantly chronic disease management (41%); cardiovascular and metabolic conditions dominate

---

## Notable Patterns and Exceptions

### High Diversity of Specific Needs
With **232 unique specific patient needs** across 250 visits, the data reflects clinical heterogeneity. Only 1 need ("Preventive well-child care and immunization") appears in >5 visits (n=16), suggesting:
- Rich, context-specific documentation in visit notes
- Variation in how clinicians characterize the same clinical scenario
- The "skill_off" variant may involve less structured or more narrative-driven need categorization

### Visit Duration Alignment
Emergency/critical care visits average 45.5 minutes (nearly 2x routine visits at 21.4 min), validating that need category correlates with resource intensity. This supports using patient needs for scheduling and triage.

### Strong Age-Need Association
Pediatric preventive needs and geriatric chronic disease management show clear developmental/degenerative progression, suggesting patient needs evolve predictably across the lifespan.

### Limited Surgical Referral Representation
Only 7 visits (2.8%) are categorized as "Surgical referral," despite orthopedics representing 15.6% of visits. This suggests many orthopedic visits are management of existing surgical candidates rather than initial referrals.

---

## Focus on Query: Evidence Quality

The **focus variable is "patient_needs"**, operationalized through two columns:
- **`patient_need_category`** (6 levels): Provides clear stratification
- **`primary_patient_need`** (232 unique values): Offers rich clinical specificity

The evidence column is **`reason_for_visit`**, which consistently contains clinical details justifying the categorized patient needs. Examples:
- "Annual physical exam. Patient reports mild fatigue..." → "Preventive health screening and fatigue evaluation"
- "Severe substernal chest pain... ECG shows ST elevation..." → "Acute myocardial infarction emergency care"
- "Well-child visit at 4 years... Immunizations updated..." → "Preventive well-child care and immunization"

All 250 records have complete data for both categorized needs and supporting reason_for_visit text, indicating reliable evidence for this analysis.

---

## Conclusions

Patient needs in healthcare visit notes span a broad spectrum from preventive well-child care and immunization (most frequent specific need) to life-threatening emergencies (myocardial infarction, septic shock). Three main patterns emerge:

1. **Chronic disease dominates** (31% of visits), reflecting aging populations and chronic disease prevalence
2. **Preventive and urgent care are equally important** (~47% combined), supporting dual-focus healthcare delivery
3. **Needs are highly contextualized**, with 232 unique specific needs reflecting both clinical complexity and documentation variability

The "skill_off" variant appears to preserve granular clinical detail in need categorization, supporting detailed triage, scheduling, and care coordination workflows.
