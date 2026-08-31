---
dataset: healthcare_visit_notes
scenario: predictive_visit
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "department"
query: "What visit reasons point to different departments?"
source_table: augment_table/healthcare_visit_notes/predictive_visit/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/healthcare_visit_notes__predictive_visit/analyses/original/analysis.md
wall_seconds: 89.58
---

# Visit Reasons and Department Routing: Cross-Department Analysis

## Dataset Overview

- **Total records:** 250 visits (V-0001 to V-0250)
- **Departments:** GeneralPractice, Pediatrics, Cardiology, Dermatology, Orthopedics, Emergency
- **Key variable:** `reason_for_visit` (free-text clinical narrative)
- **Supporting variables:** `department`, `urgency`, `age_group`, `visit_duration_min`

---

## 1. Core Department–Reason Mapping

Each department owns a clear primary cluster of visit reasons:

| Department | Primary Visit Reasons (representative examples) |
|---|---|
| **GeneralPractice** | Annual physical exam, hypertension follow-up, diabetes follow-up, COPD follow-up, hypothyroidism, UTI, GERD, depression/anxiety, tobacco cessation, preconception, osteoporosis, polypharmacy review, travel medicine |
| **Pediatrics** | Well-child visits (all ages 0–17), immunizations, viral URI, otitis media, eczema, ADHD follow-up, febrile seizure, bronchiolitis, Kawasaki disease, developmental concerns |
| **Cardiology** | MI follow-up, atrial fibrillation, heart failure (HFrEF, HFpEF), stable/unstable angina, arrhythmias (SVT, VT, bradycardia), valvular disease, pacemaker/ICD checks, CAD, aortic aneurysm |
| **Dermatology** | Acne, psoriasis, eczema/atopic dermatitis, melanoma/SCC/BCC surveillance, rosacea, tinea, shingles, bullous disease, hidradenitis suppurativa, alopecia |
| **Orthopedics** | Fractures, sprains/strains, osteoarthritis, post-op follow-up, tendinopathy, herniated disc, carpal tunnel, meniscal tear, joint dislocation |
| **Emergency** | STEMI, stroke, anaphylaxis, sepsis, DKA, acute abdomen, trauma, overdose, pulmonary embolism, psychiatric crisis |

---

## 2. Visit Reasons That Span Multiple Departments

These are the most analytically important findings—reasons whose chief complaint overlaps across departments:

### 2.1 Pain (Chest, Back, Abdominal, Joint)

| Reason type | Department(s) |
|---|---|
| Chest pain / STEMI (acute, ST-elevation) | **Emergency** (V-0008) |
| Chest pain / pericarditis (pleuritic, positional) | **Cardiology** (V-0129) |
| Chest pain / stable angina follow-up | **Cardiology** (V-0100, V-0218) |
| Low back pain, acute strain | **GeneralPractice** (V-0029, V-0200) |
| Low back pain, acute after gardening (sciatica) | **GeneralPractice** (V-0165) |
| Low back pain, herniated disc with radiculopathy | **Orthopedics** (V-0142) |
| Low back pain, chronic / disc bulge | **Orthopedics** (V-0013) |
| Abdominal pain / acute cholecystitis | **Emergency** (V-0062) |
| Abdominal pain / appendicitis suspicion | **Pediatrics** → ED (V-0022); confirmed appendicitis → **Emergency** (V-0230) |
| Abdominal pain / diverticulitis | **GeneralPractice** (V-0183) |

**Key insight:** *Pain* is the clearest multi-department signal. The routing depends on acuity (Emergency vs. Orthopedics vs. GeneralPractice), chronicity, and anatomical specificity.

---

### 2.2 Skin / Rash Presentations

| Reason type | Department(s) |
|---|---|
| Shingles / herpes zoster (thoracic dermatome) | **GeneralPractice** (V-0219), also **Dermatology** (V-0108) |
| Herpes zoster ophthalmicus (forehead, Hutchinson sign) | **GeneralPractice** → Ophthalmology (V-0136) |
| Cellulitis (leg) | **Dermatology** (V-0138) |
| Cellulitis from insect bites | **Pediatrics** (V-0041) |
| Eczema flare / secondary infection | **Pediatrics** (V-0086), **Dermatology** (V-0250) |
| Erysipelas (facial) | **Dermatology** (V-0208) |
| Rash + fever (roseola) | **Pediatrics** (V-0031) |
| Drug reaction / Stevens-Johnson | **Dermatology** → burn unit transfer (V-0170) |
| Sunburn with blistering | **Dermatology** (V-0221) |

**Key insight:** Skin infections involving children route to **Pediatrics**; the same conditions in adults route to **Dermatology** or **GeneralPractice**. Age_group is the implicit separator.

---

### 2.3 Respiratory Complaints

| Reason type | Department(s) |
|---|---|
| Cough + fever (viral URI) | **Pediatrics** (V-0002) |
| Acute bronchitis, productive cough | **GeneralPractice** (V-0084) |
| COPD exacerbation (severe, respiratory failure) | **Emergency** (V-0087) |
| COPD follow-up stable | **GeneralPractice** (V-0042) |
| Asthma exacerbation (severe) | **Emergency** (V-0044) |
| Asthma / new wheeze in child | **Pediatrics** (V-0098) |
| Bronchiolitis (infant, RSV) | **Pediatrics** (V-0192) |

**Key insight:** Acuity, age, and diagnosis severity jointly determine whether respiratory complaints go to **Pediatrics**, **GeneralPractice**, or **Emergency**.

---

### 2.4 Cardiac Symptoms (Palpitations, Dyspnea, Syncope)

| Reason type | Department(s) |
|---|---|
| New palpitations / paroxysmal AFib | **Cardiology** (V-0016) |
| Recurrent palpitations / SVT | **Cardiology** (V-0213) |
| Dyspnea / CHF exacerbation | **Emergency** (V-0035, V-0035), **Cardiology** (V-0082, V-0146) |
| Worsening dyspnea / EF drop | **Cardiology** (V-0082) |
| Syncope / bradycardia | **Cardiology** (V-0112, V-0229) |

**Key insight:** The Emergency department handles acute hemodynamic instability (O₂ sat 86%, bilateral crackles); Cardiology manages sub-acute or known cardiac disease with worsening course.

---

### 2.5 Headache

| Reason type | Department(s) |
|---|---|
| Subarachnoid hemorrhage ("worst headache of life") | **Emergency** (V-0070) |
| Migraine with aura, severe (unresponsive) | **GeneralPractice** (V-0149) |
| Migraine prophylaxis follow-up | **GeneralPractice** (V-0038) |
| Adolescent tension-type headache | **Pediatrics** (V-0227) |

**Key insight:** Headache severity and red-flag features (sudden onset, "thunderclap") segregate Emergency from GeneralPractice/Pediatrics.

---

### 2.6 Infection / Fever

| Reason type | Department(s) |
|---|---|
| UTI / acute cystitis (elderly female) | **GeneralPractice** (V-0050) |
| UTI / pyelonephritis (acute, flank pain) | **GeneralPractice** (V-0242) |
| Sepsis from urinary source | **Emergency** (V-0175) |
| Strep throat | **GeneralPractice** (V-0011) |
| Acute sinusitis | **GeneralPractice** (V-0067) |
| Conjunctivitis (bacterial) | **GeneralPractice** (V-0127) |
| Conjunctivitis (viral, watery) | **GeneralPractice** (V-0093) |
| Septic arthritis of knee | **Orthopedics** (V-0237) |

**Key insight:** Site-specific infections (joint → Orthopedics) route differently from systemic/systemic-risk infections (Sepsis → Emergency).

---

### 2.7 Hyperlipidemia / Metabolic Conditions

| Reason type | Department(s) |
|---|---|
| Hyperlipidemia follow-up | **GeneralPractice** (V-0024, V-0235) |
| Hyperlipidemia with strong CAD family history, coronary calcium scoring | **Cardiology** (V-0043) |

**Key insight:** Risk-stratification level determines whether hyperlipidemia is managed in GeneralPractice or escalated to Cardiology.

---

### 2.8 Fractures

| Reason type | Department(s) |
|---|---|
| Open ankle fracture (MVC) | **Emergency** (V-0166) |
| Intertrochanteric hip fracture (fall) | **Orthopedics** (V-0019) |
| Non-displaced supracondylar fracture (child) | **Orthopedics** (V-0105) |
| Compression vertebral fracture (osteoporosis) | **Orthopedics** (V-0092) |
| Distal radius fracture, closed reduction | **Orthopedics** (V-0174) |

**Key insight:** Open/trauma fractures (MVA) go to Emergency; closed fractures with stable mechanics route to Orthopedics directly.

---

## 3. Visit Reasons That Are Essentially Department-Exclusive

Some reason patterns are highly predictive of a single department with no observed overlap in this dataset:

| Visit Reason | Exclusive Department |
|---|---|
| Well-child visits, immunization schedules, developmental milestones | **Pediatrics** |
| Pacemaker/ICD interrogation, TAVR evaluation, EP ablation | **Cardiology** |
| Mohs surgery follow-up, total-body photography for nevi | **Dermatology** |
| Post-surgical orthopedic follow-up (TKR, THA, ACL reconstruction) | **Orthopedics** |
| Resuscitation / STEMI protocol / stroke thrombolysis | **Emergency** |
| Preconception counseling, tobacco cessation, polypharmacy review | **GeneralPractice** |

---

## 4. Exceptions and Weak Evidence

- **Acute angle closure glaucoma** (V-0245) landed in **Emergency**, not Ophthalmology—this reflects the dataset's department scope (no Ophthalmology department exists).
- **Pediatric appendicitis** (V-0022) was *recognized* in Pediatrics and transferred to ED; the confirmed appendicitis visit (V-0230) is logged under Emergency. This is a two-step routing pattern not captured by a single record's department field.
- **Shingles** appears in both **GeneralPractice** (V-0219) and **Dermatology** (V-0108) with no clear distinguishing feature in the text; this may represent true practice variation or initial-presenting-provider availability rather than a principled rule.
- **Hyperlipidemia** managed at two levels (GP vs. Cardiology) suggests a **risk-based escalation pattern**, but the sample is small (2 vs. many GP-managed hyperlipidemia cases), so the threshold is inferred, not precisely quantified.
- The dataset has no Neurology, Gastroenterology, or Pulmonology departments, so conditions that would realistically route there (stroke follow-up, IBD, asthma maintenance) appear in Cardiology, Emergency, or GeneralPractice, which may skew apparent mappings.

---

## 5. Summary Decision Rules

$$
\text{Department} = f(\text{acuity}, \text{age}, \text{anatomy}, \text{chronicity})
$$

| Factor | Effect |
|---|---|
| **Acuity = Emergency** | Routes to Emergency regardless of cause |
| **Patient age 0–17** | Routes child-appropriate version of common complaints to Pediatrics |
| **Organ-specific condition** | Routes to organ specialty (Cardiology, Dermatology, Orthopedics) |
| **Preventive / chronic management** | Routes to GeneralPractice |
| **Musculoskeletal, traumatic but stable** | Routes to Orthopedics |
| **Same diagnosis, higher severity** | Escalates from GP → Cardiology → Emergency |

---

## Conclusion

The clearest multi-department visit reasons are **pain** (chest, back, abdominal), **skin infections and rashes**, **respiratory complaints**, and **headaches**—all of which can plausibly present in two to four departments depending on acuity, age, and diagnostic certainty. Department routing in this dataset is driven primarily by **severity/urgency** (the `urgency` column aligns closely: Emergency visits always have urgency = "Emergency"), **age** (segregates Pediatrics), and **anatomical specificity** (segregates organ specialties). The most ambiguous routing involves shingles (GP vs. Dermatology) and hyperlipidemia (GP vs. Cardiology), where practice-level variation rather than a hard clinical rule appears to govern assignment.
