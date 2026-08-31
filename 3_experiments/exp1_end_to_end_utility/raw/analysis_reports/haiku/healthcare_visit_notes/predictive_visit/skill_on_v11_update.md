---
dataset: healthcare_visit_notes
scenario: predictive_visit
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "department"
query: "What visit reasons point to different departments?"
source_table: augment_table/healthcare_visit_notes/predictive_visit/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:22:45.806653+00:00
wall_seconds: 70.83
---

# Analysis Report: Visit Reasons Pointing to Different Departments

**Dataset:** Healthcare Visit Notes - Predictive Visit Analysis  
**Variant Label:** skill_on  
**Focus Variable:** Department  
**Query:** What visit reasons point to different departments?

## Executive Summary

Analysis of 250 healthcare visits across six departments reveals **clear and distinct patterns of visit reasons that align with departmental specialization**. Each department exhibits characteristic presentation types, clinical focus areas, and urgency profiles that effectively define departmental routing decisions.

---

## Department Distributions

| Department | Count | % of Total | Primary Pathway |
|---|---|---|---|
| General Practice | 54 | 21.6% | Primary care hub |
| Pediatrics | 45 | 18.0% | Age-specific (0-17) |
| Cardiology | 42 | 16.8% | Cardiac/vascular specialization |
| Dermatology | 42 | 16.8% | Skin/dermatologic specialization |
| Orthopedics | 39 | 15.6% | Musculoskeletal specialization |
| Emergency | 28 | 11.2% | Urgent/acute-only |

---

## Visit Reason Patterns by Department

### **Cardiology** (n=42)
**Key Clinical Focus:** Cardiac and vascular conditions exclusively
- **Primary System:** 100% cardiac_vascular (42/42)
- **Presentation Types:** 
  - Chronic management: 66.7% (28 visits) — follow-ups, medication adjustments, ongoing condition management
  - Acute symptoms: 26.2% (11 visits) — new-onset arrhythmias, chest pain, hemodynamic changes
  - Preventive screening: 4.8% (2 visits) — pre-operative clearance
  
**Typical Visit Reasons:**
- Post-MI follow-ups with EF monitoring and medication tolerance
- Atrial fibrillation rate control on anticoagulation
- New-onset palpitations/arrhythmias requiring urgent evaluation
- Heart failure management with functional capacity assessment
- Peripheral vascular disease and stenosis surveillance

**Acuity Pattern:** 61.9% chronic stable, 19.0% acute onset  
**Evidence:** Clear cardiac-specific pathway with consistent clinical systems focus

---

### **Dermatology** (n=42)
**Key Clinical Focus:** Skin lesions, dermatologic conditions exclusively
- **Primary System:** 97.6% dermatologic (41/42)
- **Presentation Types:**
  - Acute symptoms: 50.0% (21 visits) — new rashes, infections, acute reactions
  - Chronic management: 33.3% (14 visits) — psoriasis, acne, eczema control
  - Preventive screening: 9.5% (4 visits) — skin cancer surveillance
  
**Typical Visit Reasons:**
- Acute viral exanthems, urticaria, contact dermatitis
- Suspicious pigmented lesions requiring biopsy
- Chronic inflammatory conditions (psoriasis, eczema) management
- Infectious skin conditions (impetigo, cellulitis, tinea)
- Post-treatment follow-ups (Mohs surgery, cryotherapy)

**Acuity Pattern:** 45.2% acute onset, 33.3% chronic stable, 16.7% exacerbation  
**Evidence:** Balanced acute/chronic mix, unified by dermatologic system focus

---

### **Orthopedics** (n=39)
**Key Clinical Focus:** Musculoskeletal system, injuries, structural conditions
- **Primary System:** 100% musculoskeletal (39/39)
- **Presentation Types:**
  - Chronic management: 46.2% (18 visits) — degenerative conditions, post-op rehabilitation
  - Injury/trauma: 33.3% (13 visits) — acute fractures, sprains, tears
  - Acute symptoms: 12.8% (5 visits) — tendinopathy flares, new pain syndromes
  
**Typical Visit Reasons:**
- Traumatic injuries (fractures, dislocations, joint damage from falls/MVAs)
- Chronic degenerative conditions (osteoarthritis, spinal stenosis)
- Acute musculoskeletal pain from strain, overuse, or sports injury
- Post-operative follow-ups (joint replacement, ACL reconstruction)
- Structural pathology requiring imaging and surgical consultation

**Acuity Pattern:** 46.2% acute onset, 38.5% chronic stable, 15.4% exacerbation  
**Evidence:** Strong injury/trauma component (33.3%) distinguishes Orthopedics from primary care

---

### **Pediatrics** (n=45)
**Key Clinical Focus:** Age-specific (0-17 years) across multiple systems
- **Presentation Types:**
  - Preventive screening: 51.1% (23 visits) — well-child exams, immunizations, developmental screening
  - Acute symptoms: 44.4% (20 visits) — fever, URI, rash, acute injury
  - Chronic management: 2.2% (1 visit) — minimal chronic disease
  
**Typical Visit Reasons:**
- Routine well-child visits (newborn, 2-month, 4-month, 12-month checkups)
- Acute viral illnesses (URI, otitis media, roseola, hand-foot-mouth)
- Vaccine administration and immunization catch-up
- Developmental screening (growth, motor, speech)
- Acute injuries (fractures, lacerations, concussions)
- Behavioral/developmental concerns (bedwetting, ADHD follow-up, tics)

**Acuity Pattern:** 51.1% preventive/not_present, 42.2% acute onset  
**Evidence:** Age-driven departmental routing; pediatric-specific visit types dominate

---

### **General Practice** (n=54)
**Key Clinical Focus:** Broad primary care spectrum
- **Primary Systems:** Multiple — endocrine_metabolic (35.2%), infectious_disease (13.0%), psychiatric_neurologic (13.0%)
- **Presentation Types:**
  - Chronic management: 40.7% (22 visits) — diabetes, hypertension, COPD, hypothyroidism
  - Acute symptoms: 31.5% (17 visits) — infections, acute exacerbations, new symptoms
  - Preventive screening: 25.9% (14 visits) — annual exams, health maintenance
  
**Typical Visit Reasons:**
- Chronic disease follow-ups (diabetes, hypertension, lipidemia management)
- Common acute infections (UTI, bronchitis, sinusitis, pharyngitis)
- Mental health and substance abuse screening/counseling
- Preventive care (annual exams, immunizations, cancer screening)
- Minor acute illness management (acute LBP, migraine, conjunctivitis)
- Postpartum and preconception counseling

**Acuity Pattern:** Balanced — 35.2% chronic stable, 35.2% acute onset  
**Evidence:** Intentional generalist routing; primary care acts as multi-system triage point

---

### **Emergency** (n=28)
**Key Clinical Focus:** Acute and life-threatening conditions only
- **Presentation Types:** 85.7% acute symptoms (24 visits), 10.7% injury/trauma
- **Acuity Pattern:** 100% acute onset; 53.6% life-threatening severity
- **Primary Systems:** Distributed — pulmonary_respiratory (25.0%), psychiatric_neurologic (21.4%), gastrointestinal_hepatic (17.9%)
  
**Typical Visit Reasons:**
- Acute coronary syndromes (STEMI, unstable angina)
- Acute neurological emergencies (stroke, seizure, altered mental status)
- Severe trauma (MVA with LOC, open fractures, head injury)
- Acute organ system failure (respiratory failure, severe CHF exacerbation)
- Acute abdominal pathology (peritonitis, appendicitis, ruptured AAA)
- Anaphylaxis and severe allergic reactions

**Acuity Pattern:** 100% emergency urgency; life-threatening and urgent severity only  
**Evidence:** Strict clinical gatekeeping; only conditions meeting emergency thresholds

---

## Key Patterns in Visit Reason → Department Routing

### **Pattern 1: System-Specific Specialization**
Cardiology, Dermatology, and Orthopedics show **near-perfect clinical system alignment**:
- Cardiology: 100% cardiac_vascular
- Dermatology: 97.6% dermatologic  
- Orthopedics: 100% musculoskeletal

**Implication:** These departments act as clinical system specialists with clear referral criteria.

### **Pattern 2: Age-Driven Routing**
Pediatrics receives **100% of patients aged 0-17**, regardless of clinical condition type:
- 51.1% preventive visits (unique to this department at this scale)
- 44.4% acute symptom visits
- Demonstrates **age-based triage precedence** over condition type

### **Pattern 3: Acuity-Based Gatekeeping**
Emergency exclusively receives **100% emergency-level urgency** visits:
- 53.6% life-threatening severity
- 39.3% urgent severity
- 0% routine visits
- Patterns show **emergency-specific presentation** (massive trauma, organ failure, hemodynamic instability)

### **Pattern 4: Generalist Triage**
General Practice shows **balanced mix across presentation types and systems**:
- 40.7% chronic management, 31.5% acute, 25.9% preventive
- No system dominates (endocrine 35.2%, infectious 13.0%, psychiatric 13.0%)
- Acts as **first-line evaluation and management gateway**

### **Pattern 5: Hybrid Specialist-Generalist (Pediatrics)**
Pediatrics combines **age-based specialization with broad clinical range**:
- 51.1% preventive screening (general pediatric content)
- 44.4% acute care across multiple systems
- Suggests **pediatric expertise across multiple clinical domains** rather than single-system focus

---

## Clinical Evidence of Department Differentiation

### Severity Levels Align with Departmental Scope:

| Department | Mild | Moderate | Urgent | Life-Threatening |
|---|---|---|---|---|
| Cardiology | 28.6% | 40.5% | 28.6% | 0% |
| Dermatology | 28.6% | 59.5% | 7.1% | 2.4% |
| Orthopedics | 5.1% | 76.9% | 15.4% | 2.6% |
| General Practice | 38.9% | 37.0% | 3.7% | 0% |
| Emergency | 0% | 7.1% | 39.3% | 53.6% |

**Key Finding:** Severity distribution **strongly predicts department**:
- Life-threatening cases routed almost exclusively to Emergency (53.6%)
- Orthopedic cases predominantly moderate severity (76.9%) — consistent with structural/traumatic focus
- Dermatology concentrates on moderate severity (59.5%) — appropriate for inflammatory/infectious conditions

---

## Factors Enabling Department Differentiation

1. **Primary Clinical System** (strongest predictor)
   - Cardiac → Cardiology
   - Skin → Dermatology
   - Musculoskeletal → Orthopedics

2. **Age of Patient** (categorical filter)
   - Age 0-17 → Pediatrics (except Emergency)

3. **Acuity/Urgency Level** (escalation filter)
   - Emergency urgency + critical severity → Emergency Department

4. **Presentation Type** (context modifier)
   - Chronic management, preventive, acute symptom distributed across appropriate departments

5. **Injury/Trauma Status** (specialty trigger)
   - Trauma + musculoskeletal → Orthopedics
   - Trauma + multisystem → Emergency
   - Trauma + dermatologic (laceration) → Dermatology

---

## Notable Exceptions and Weak Evidence

1. **Emergency Department System Diversity:** Unlike specialist departments, Emergency manages multiple clinical systems (respiratory 25%, neurologic 21%, GI 18%), reflecting its role as ultimate safety net rather than specialist pathway.

2. **General Practice Breadth:** While acting as multi-system generalist, some conditions (e.g., moderate cardiac symptoms) may bypass GP directly to Cardiology, suggesting referral criteria exist beyond data captured in reason text alone.

3. **Pediatric Chronic Disease Limitation:** Only 1 chronic management case in Pediatrics (ADHD follow-up) suggests pediatric chronic disease cases may be co-managed with other departments or routed to specialists early.

4. **Cardiology Preventive Screening:** Only 4.8% preventive screening (vs. 51.1% in Pediatrics) indicates cardiac risk assessment typically occurs in General Practice initially.

---

## Conclusion

Visit reasons point to departments through **complementary mechanisms**:

- **Specialist departments** (Cardiology, Dermatology, Orthopedics) act as **clinical system specialists**, concentrating on single or closely-related systems with consistent high prevalence (>97%).

- **Pediatrics** acts as an **age-segregated generalist**, managing broad presentation types within pediatric population, suggesting age-based specialization may require general clinical competence.

- **General Practice** functions as a **multi-system triage point**, managing common acute/chronic conditions across systems, likely serving as first-line evaluation.

- **Emergency** serves as an **acuity-based safety net**, exclusively accepting emergent presentations regardless of clinical system, with severity profile (53.6% life-threatening) distinct from all other departments.

**Predictive Value:** The `reason_for_visit` field strongly aligns with department assignment through its implicit encoding of clinical system, acuity, age-appropriateness, and trauma status. This enables reliable department prediction from visit reason text through feature engineering focused on clinical system recognition, acuity indicators, and age cues.

REPORT_MD_BEGIN
