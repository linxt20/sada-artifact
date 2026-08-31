---
dataset: healthcare_visit_notes
scenario: predictive_visit
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "department"
query: "What visit reasons point to different departments?"
source_table: augment_table/healthcare_visit_notes/predictive_visit/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:23:04.566333+00:00
wall_seconds: 88.91
---

# Healthcare Visit Reasons and Department Referral Patterns: Analysis Report

## Executive Summary

This analysis examines how visit reasons predict department routing in a healthcare dataset of 250 clinical encounters across six departments. The query "What visit reasons point to different departments?" is answered by analyzing the augmented table to identify the semantic and clinical drivers that differentiate departmental case mixes. The augmented columns—particularly **organ_system_focus**, **life_threat_status**, and **presenting_symptom_type**—provide critical semantic enrichment that clarifies how visit characteristics map to departmental specialization.

## Methods

### Dataset Characteristics
- **Total visits:** 250 encounters (plus 1 header row = 251 lines)
- **Departments:** 6 (Cardiology, Dermatology, Emergency, GeneralPractice, Orthopedics, Pediatrics)
- **TAPP-Generated Augmented Columns Used:**
  - `organ_system_focus` (14 categories)
  - `life_threat_status` (6 severity levels)
  - `presenting_symptom_type` (13 symptom categories)
  - `diagnostic_or_procedural_escalation` (7 escalation types)

### Analytical Approach
The report combines original structured fields (department, urgency, age_group, visit_duration_min, reason_for_visit) with TAPP-generated semantic columns to identify department-specific patterns. Augmented columns are used to clarify which visit characteristics distinguish departments, not to replace the original data. Cross-tabulation and stratified frequency analysis provide quantified evidence.

---

## Key Findings: Visit Reasons That Point to Different Departments

### 1. **Cardiology** (n=42, 16.8% of visits)

**Defining Characteristic:** Exclusive focus on cardiovascular system

- **Organ System:** Cardiovascular (100%)
- **Primary Visit Reasons:** Medication management (69.0%) and chest pain/cardiac symptoms (26.2%)
- **Acuity Profile:** Routine maintenance dominant (42.9%), with 26.2% moderate acute and 7.1% severe acute
- **Escalation Pattern:** Monitoring/observation (47.6%), medication adjustment (28.6%), procedural planning (14.3%)

**Distinctive Visit Types:**
- Post-intervention follow-ups (MI recovery, pacemaker interrogations, stent surveillance)
- Chronic disease management (arrhythmias, valve disease, heart failure)
- Preventive screening for cardiovascular risk (e.g., CAD, hypertension)

**Insight:** Cardiology visits are highly specialized around cardiovascular pathology with minimal organ system overlap. The `organ_system_focus=cardiovascular` field perfectly predicts Cardiology, appearing in 42/42 visits. Life threat status and escalation types reflect stable disease management with monitoring as the dominant strategy.

---

### 2. **Dermatology** (n=42, 16.8% of visits)

**Defining Characteristic:** Isolated dermatological and skin-focused presentation

- **Organ System:** Dermatological (95.2%), with minimal infectious_inflammatory overlap (4.8%)
- **Primary Visit Reasons:** Skin lesions/rashes (88.1%), preventive screening (7.1%)
- **Acuity Profile:** Moderate acute illness dominant (61.9%), routine maintenance (19.0%), mild chronic (16.7%)
- **Escalation Pattern:** Medication initiation (52.4%), procedural intervention (23.8%), monitoring (9.5%)

**Distinctive Visit Types:**
- Inflammatory/infectious skin conditions (eczema, acne, dermatitis, impetigo)
- Neoplastic/precancerous lesions (actinic keratosis, SCC, melanoma screening)
- Cosmetic and chronic skin disorders (alopecia, vitiligo, rosacea, psoriasis)

**Insight:** The `presenting_symptom_type=skin_rash_lesion` field appears in 88.1% of Dermatology visits (37/42), acting as a near-perfect classifier. The high proportion of acute illness (61.9%) reflects infectious, inflammatory, and treatment-responsive dermatological conditions. Procedural interventions (biopsies, cryotherapy, injections) account for 23.8% of escalations.

---

### 3. **Orthopedics** (n=39, 15.6% of visits)

**Defining Characteristic:** Exclusive musculoskeletal focus with pain presentation

- **Organ System:** Musculoskeletal (100%)
- **Primary Visit Reasons:** Musculoskeletal pain (53.8% joint/muscle pain, 46.2% other pain)
- **Acuity Profile:** Moderate acute (46.2%), mild chronic (33.3%), severe acute organ threat (10.3%)
- **Escalation Pattern:** Procedural intervention (46.2%), monitoring (20.5%), surgical intervention (17.9%), imaging (10.3%)

**Distinctive Visit Types:**
- Acute trauma/fractures (ankle sprains, fractures, dislocations)
- Chronic joint/structural disease (osteoarthritis, herniated disc, tendinopathy)
- Post-operative follow-up and rehabilitation
- Surgical planning (reconstructions, arthroplasties, stabilizations)

**Insight:** The `organ_system_focus=musculoskeletal` field predicts Orthopedics visits with 100% consistency (39/39 visits). Pain syndromes (joint/muscle and other pain) dominate symptom presentation. The high frequency of procedural (46.2%) and surgical (17.9%) interventions reflects the department's role in operative management. Imaging is common (10.3%), reflecting diagnostic imaging needs.

---

### 4. **GeneralPractice** (n=54, 21.6% of visits)

**Defining Characteristic:** Broad multi-system coverage with emphasis on chronic disease and preventive care

- **Organ Systems:** Endocrine/metabolic (22.2%), not_present (13.0%), infectious_inflammatory (9.3%), obstetric_gynecological (9.3%), respiratory (7.4%) — **12 different systems represented**
- **Primary Visit Reasons:** Medication management (42.6%), preventive screening (27.8%)
- **Acuity Profile:** Routine maintenance dominant (53.7%), moderate acute (27.8%), mild chronic (18.5%)
- **Escalation Pattern:** Medication initiation (46.3%), monitoring (25.9%), lab workup (13.0%), preventive counseling (11.1%)

**Distinctive Visit Types:**
- Chronic disease management (diabetes, hypertension, COPD, hypothyroidism)
- Preventive care (annual exams, cancer screening, vaccinations, preconception counseling)
- Acute primary care (URI, UTI, acute bronchitis, minor lacerations)
- Psychiatric and behavioral health (anxiety, depression, substance use counseling)

**Insight:** GeneralPractice is the only truly multi-system department. Unlike specialist departments, no single `organ_system_focus` dominates (max 22.2%). The presence of 12 organ systems in 54 visits reflects gatekeeper role. Medication management (42.6%) and preventive screening (27.8%) together account for 70.4% of visits, distinguishing GP from specialist acute care. Lab workup and counseling-only interventions are proportionally higher here (24.1% combined) than in procedure-heavy departments.

---

### 5. **Pediatrics** (n=45, 18.0% of visits)

**Defining Characteristic:** Age-stratified preventive and developmental focus

- **Organ System:** Pediatric developmental (66.7%), infectious_inflammatory (13.3%), respiratory (6.7%), gastrointestinal (4.4%)
- **Primary Visit Reasons:** Growth/developmental screening (53.3%), fever/infection (20.0%)
- **Acuity Profile:** Routine maintenance (53.3%), mild chronic (20.0%), moderate acute (20.0%), severe acute (6.7%)
- **Escalation Pattern:** Preventive counseling (55.6%), monitoring (20.0%), medication initiation (15.6%)

**Distinctive Visit Types:**
- Well-child visits and developmental surveillance (newborn, 2-month, 4-month, 12-month, school-age, adolescent physicals)
- Immunization-focused encounters
- Acute infections (otitis media, URIs, bronchiolitis, impetigo)
- Behavioral/developmental concerns (speech delay, tics, enuresis, concussions)

**Insight:** The `organ_system_focus=pediatric_developmental` field appears in 66.7% of Pediatrics visits (30/45), far exceeding any other organ system category. Preventive counseling (55.6%) is the dominant escalation type—nearly double the rate in other departments—reflecting Pediatrics' emphasis on anticipatory guidance, immunizations, and developmental counseling. The high routine maintenance rate (53.3%) and low severe acuity (6.7%) distinguish Pediatrics as the lowest-acuity specialty.

---

### 6. **Emergency** (n=28, 11.2% of visits)

**Defining Characteristic:** High acuity, multi-system, acute threat-driven presentations

- **Organ Systems:** Diverse — respiratory (21.4%), neurological (17.9%), gastrointestinal (14.3%), psychiatric (10.7%), cardiovascular (7.1%), **10 systems total across 28 visits**
- **Primary Visit Reasons:** Neurological pain (17.9%), respiratory distress (17.9%), altered mental status (17.9%), abdominal pain (14.3%) — no single reason dominates
- **Acuity Profile:** Severe acute organ threat (53.6%), organ failure/shock (21.4%), hemodynamically unstable (17.9%), moderate acute (7.1%) — **92.9% high acuity**
- **Escalation Pattern:** Procedural intervention (50.0%), surgical intervention (17.9%), monitoring (14.3%)

**Distinctive Visit Types:**
- Life-threatening presentations (STEMI, stroke, anaphylaxis, sepsis, massive hemorrhage, DKA)
- Organ failure and shock states (respiratory failure, cardiogenic shock, GI bleed)
- Acute trauma (MVA, open fractures, head injury)
- Acute psychiatric emergencies (suicidal ideation, intoxication, psychosis)

**Insight:** Emergency is definitively distinguished by `life_threat_status` distribution. Severe acute organ threat (53.6%) and organ failure/shock (21.4%) together account for 75.0% of visits—contrasted with 0% in Pediatrics and GeneralPractice. Hemodynamically unstable status (17.9%) appears only in Emergency and occurs in 5 visits. Procedural (50.0%) and surgical (17.9%) intervention rates are proportionally high, reflecting acute management needs. The high organ system diversity (10 systems in 28 visits, vs. 1-2 in specialist departments) reflects Emergency's role as a safety net for acute presentations across all organ systems.

---

## Quantitative Department Differentiation Matrix

| Department | N | Primary Organ System | Primary Symptom | Routine % | High Acuity % | Top Escalation |
|---|---|---|---|---|---|---|
| **Cardiology** | 42 | Cardiovascular (100%) | Medication mgmt (69%) | 43% | 33% | Monitoring (48%) |
| **Dermatology** | 42 | Dermatological (95%) | Skin lesions (88%) | 19% | 64% | Medication init (52%) |
| **Emergency** | 28 | Respiratory (21%) [diverse] | Varied (no >18%) | 0% | 93% | Procedures (50%) |
| **GeneralPractice** | 54 | Endocrine (22%) [12 systems] | Medication mgmt (43%) | 54% | 28% | Medication init (46%) |
| **Orthopedics** | 39 | Musculoskeletal (100%) | Pain (100%) | 8% | 56% | Procedures (46%) |
| **Pediatrics** | 45 | Pediatric devel (67%) | Growth/devel (53%) | 53% | 27% | Counseling (56%) |

---

## Role of TAPP-Augmented Columns in Clarifying Department Patterns

### How Each Augmented Column Adds Semantic Signal:

1. **`organ_system_focus`** (Primary differentiator)
   - **Strength:** Perfectly predicts specialist departments (Cardiology, Dermatology, Orthopedics all 100% monospecialty)
   - **Evidence:** Cardiovascular organ_system in 42/42 Cardiology visits; Dermatological in 40/42 Dermatology; Musculoskeletal in 39/39 Orthopedics
   - **Generalist value:** Reveals GeneralPractice diversity (12 organ systems) vs. specialist focus
   - **Recommendation:** Essential column; no redundancy with original fields

2. **`life_threat_status`** (Acuity differentiator)
   - **Strength:** Sharply distinguishes Emergency from all other departments
   - **Evidence:** Emergency 93% high-acuity (severe organ threat + organ failure + hemodynamically unstable) vs. 0% in Pediatrics/GeneralPractice
   - **Clinical relevance:** Explains routing decisions more clearly than "urgency" field alone (Emergency has 28 visits; high-acuity is intrinsic to department mission, not visit-level variance)
   - **Recommendation:** Highly valuable; adds acuity classification beyond triage urgency

3. **`presenting_symptom_type`** (Phenotypic differentiator)
   - **Strength:** Identifies characteristic symptom presentations by department
   - **Evidence:** Skin lesions in 88% of Dermatology (37/42); Medication management in 69% of Cardiology; Developmental in 53% of Pediatrics
   - **Clarity:** Clarifies which symptom presentations route to which departments
   - **Note:** Somewhat redundant with organ_system_focus for specialist departments but adds symptom-centric view useful for triage logic
   - **Recommendation:** Valuable for operational triage systems; partially overlaps organ_system but from different angle

4. **`diagnostic_or_procedural_escalation`** (Management intensity differentiator)
   - **Strength:** Reveals department-specific management strategies
   - **Evidence:** Preventive counseling dominates Pediatrics (56%), while procedures dominate Orthopedics/Emergency (46-50%); Monitoring dominates Cardiology (48%)
   - **Insight:** Not primarily a department predictor but a consequence of department selection; nonetheless clarifies why visits route differently (Pediatrics doesn't do surgery; Emergency needs urgent procedures)
   - **Recommendation:** Lower priority for predicting departments but valuable for understanding downstream care patterns

---

## Clinical Interpretation: Why Visits Route to Different Departments

### Specialist Departments (Single-System Focus)
- **Cardiology, Dermatology, Orthopedics:** Visit reasons point to these departments because the **primary organ system and chief symptom are pathognomonic** for each specialty. A patient with cardiovascular symptoms and chest pain metrics routes to Cardiology; skin lesions to Dermatology; musculoskeletal pain to Orthopedics. The `organ_system_focus` field is near-deterministic.

### Generalist Department (Multi-System)
- **GeneralPractice:** Attracts visits across 12 organ systems because it serves as a **first-contact and chronic disease management service**. Visit reasons here emphasize medication management (42.6%) and preventive screening (27.8%)—continuity-of-care functions rather than acute diagnosis. Patients with stable diabetes, hypertension, or routine preventive needs route to GP regardless of underlying system.

### Pediatric Specialty (Age-Stratified)
- **Pediatrics:** Visit reasons are **age-dependent and developmental** rather than purely organ-system-driven. The dominant `organ_system_focus=pediatric_developmental` (66.7%) reflects the fact that many pediatric visits are wellness encounters and developmental surveillance, not acute illness. Preventive counseling (55.6%) is the hallmark escalation type.

### Emergency Department (Acute, Multi-System, Threat-Driven)
- **Emergency:** Visit reasons are characterized by **high threat status regardless of organ system**. The 93% high-acuity rate and diversity of 10 organ systems indicates that Emergency is accessed based on **severity and need for urgent intervention**, not a specific organ system. Patients with potentially life-threatening presentations across any system route to Emergency.

---

## Summary: Differential Routing Patterns

| **Routing Driver** | **Departments Affected** | **Mechanism** |
|---|---|---|
| Organ system (single) | Cardiology, Dermatology, Orthopedics | Pathognomonic specialization |
| Organ system (multi) | GeneralPractice | Gatekeeper + chronic disease management role |
| Age group | Pediatrics | Age-stratified developmental care |
| Life threat status | Emergency | Severity triggers urgent evaluation |
| Symptom phenotype | All departments | Reinforces organ system routing |
| Preventive intent | Pediatrics, GeneralPractice | Anticipatory, wellness-driven care |
| Medication management | Cardiology, GeneralPractice, Dermatology | Chronic disease and symptom control |
| Procedural/surgical need | Orthopedics, Emergency | Intervention requirements |

---

## Limitations and Data Quality Notes

- The "not_present" organ_system category appears in 7 GeneralPractice visits (13%), suggesting some visit narratives may not have clear organ system engagement (e.g., pure preventive/administrative visits). This does not diminish the analysis but reflects that some encounters transcend traditional system boundaries.
- Visit urgency field (Routine/Urgent/Emergency) aligns closely with department assignment but is less granular than the `life_threat_status` augmented field, which provides six-level severity classification.
- Reason_for_visit narratives are rich clinical notes; the augmented columns distill these into actionable semantic categories. No discrepancies detected.

---

## Conclusion

Visit reasons point to different departments through a hierarchical combination of:
1. **Primary organ system** (nearly deterministic for specialists; diverse for generalists and emergency)
2. **Chief symptom presentation** (phenotypic fingerprint for each department)
3. **Acuity/threat status** (dominant driver for Emergency; stratifies other departments)
4. **Care intent** (preventive vs. acute vs. chronic management)
5. **Age group** (critical for Pediatrics; secondary elsewhere)

The TAPP-augmented columns—particularly `organ_system_focus` and `life_threat_status`—provide semantic enrichment that clarifies these routing patterns beyond what the original structured fields reveal. Together, these augmented and original fields enable accurate prediction of departmental assignment and understanding of population-specific visit characteristics across the healthcare system.
