---
dataset: healthcare_visit_notes
scenario: predictive_visit
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "department"
query: "What visit reasons point to different departments?"
source_table: augment_table/healthcare_visit_notes/predictive_visit/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:22:46.458550+00:00
wall_seconds: 71.26
---

# Visit Reasons Pointing to Different Departments

## Overview

The dataset contains 250 visits across 6 departments — **Cardiology, Dermatology, Emergency, GeneralPractice, Orthopedics, and Pediatrics** — with visits categorized by `chief_complaint_category`, `visit_type`, and `primary_body_system`. Ten of eleven chief complaint categories appear in **more than one department**, revealing that clinical presentation alone does not determine routing. The analysis below maps each shared visit reason to its departmental distribution and explains the distinguishing clinical factors.

---

## Chief Complaint Categories Spanning Multiple Departments

### 1. `chronic_condition_monitoring` — 6 departments (n=53)

The most broadly distributed complaint category:

| Department | Count |
|---|---|
| Cardiology | 29 |
| GeneralPractice | 16 |
| Orthopedics | 4 |
| Dermatology | 2 |
| Pediatrics | 1 |
| Emergency | 1 |

**Distinguishing factors:** The organ system drives routing. Cardiology handles cardiac/vascular follow-up (e.g., post-MI, EF monitoring); Orthopedics manages joint/spine conditions (arthritis, disc disease); Dermatology handles skin disease; GeneralPractice covers metabolic/endocrine or multi-system conditions (e.g., diabetes, hypertension). The single Emergency case reflects acute decompensation of an underlying chronic condition.

---

### 2. `pain` — 4 departments (n=31)

| Department | Count |
|---|---|
| Orthopedics | 18 |
| Emergency | 5 |
| GeneralPractice | 5 |
| Pediatrics | 3 |

**Distinguishing factors:** Musculoskeletal/structural pain (back, knee, disc) routes to Orthopedics. Acute high-severity pain with systemic features (cholecystitis, renal colic) routes to Emergency. Mild or ambiguous pain (acute strain, gout) is handled by GeneralPractice. Pediatric pain (abdominal, dysmenorrhea) routes to Pediatrics due to age.

---

### 3. `infection` — 5 departments (n=21)

| Department | Count |
|---|---|
| Pediatrics | 8 |
| GeneralPractice | 8 |
| Dermatology | 2 |
| Emergency | 2 |
| Orthopedics | 1 |

**Distinguishing factors:** Site and severity determine routing. Pediatric URIs go to Pediatrics; bacterial throat/respiratory infections to GeneralPractice; skin/soft-tissue infections (cellulitis) to Dermatology; sepsis or hemodynamically unstable infections to Emergency; septic arthritis to Orthopedics.

---

### 4. `cardiorespiratory_symptom` — 3 departments (n=22)

| Department | Count |
|---|---|
| Cardiology | 11 |
| Emergency | 9 |
| Pediatrics | 2 |

**Distinguishing factors:** Urgency is the key discriminator. Stable arrhythmias, palpitations, or chronic dyspnea route to Cardiology. Acute chest pain with ST changes or hemodynamic instability routes to Emergency (STEMI, PE). Pediatric wheeze and new-onset asthma route to Pediatrics.

---

### 5. `injury_trauma` — 3 departments (n=22)

| Department | Count |
|---|---|
| Orthopedics | 16 |
| Emergency | 4 |
| Pediatrics | 2 |

**Distinguishing factors:** Orthopedics dominates with fractures, ligament tears, and joint injuries. Emergency handles multi-trauma or injuries requiring urgent stabilization. Pediatric trauma cases (fractures in children) go to Pediatrics.

---

### 6. `screening_preventive` — 4 departments (n=19)

| Department | Count |
|---|---|
| GeneralPractice | 15 |
| Dermatology | 2 |
| Cardiology | 1 |
| Pediatrics | 1 |

**Distinguishing factors:** Routine wellness and metabolic screening go to GeneralPractice. Skin cancer screening routes to Dermatology. Cardiac risk assessment post-event routes to Cardiology. Well-child checks route to Pediatrics.

---

### 7. `skin_lesion` — 3 departments (n=39)

| Department | Count |
|---|---|
| Dermatology | 36 |
| GeneralPractice | 2 |
| Pediatrics | 1 |

**Distinguishing factors:** Dermatology handles the overwhelming majority. GeneralPractice and Pediatrics see minor or incidental skin findings; these likely represent straightforward cases not requiring specialist referral.

---

### 8. `neurologic_symptom` — 3 departments (n=9)

| Department | Count |
|---|---|
| Emergency | 6 |
| Pediatrics | 2 |
| GeneralPractice | 1 |

**Distinguishing factors:** High-acuity neurologic presentations (stroke, severe headache) route to Emergency. Pediatric-onset seizures or developmental neurologic concerns go to Pediatrics. Mild or chronic symptoms may be handled by GeneralPractice initially.

---

### 9. `medication_adjustment` — 2 departments (n=6)

| Department | Count |
|---|---|
| GeneralPractice | 5 |
| Cardiology | 1 |

**Distinguishing factors:** GeneralPractice handles general medication titration; Cardiology manages cardiac-specific drug adjustments.

---

### 10. `psychiatric_behavioral` — 3 departments (n=4)

| Department | Count |
|---|---|
| GeneralPractice | 2 |
| Pediatrics | 1 |
| Emergency | 1 |

**Note:** Low counts (n=4 total) make patterns weak. GeneralPractice and Pediatrics handle stable mental health concerns; Emergency handles acute behavioral crises.

---

## Categories Exclusive to One Department

Only **`growth_development`** (n=24) is exclusively routed to **Pediatrics**, reflecting age-specific care that no other department handles.

---

## Visit-Type Dimension

Six of seven visit types span multiple departments, underscoring that neither visit type nor complaint category alone determines routing. `chronic_disease_management` is the most diffuse (5 departments: Cardiology 34, Dermatology 18, GeneralPractice 20, Orthopedics 17, Pediatrics 3). `acute_illness` spans all 6 departments (Emergency 25, Pediatrics 17, Dermatology 18, GeneralPractice 14, Cardiology 3, Orthopedics 4).

---

## Key Takeaways

| Routing Factor | Examples |
|---|---|
| **Organ/body system** | Pain → Orthopedics (musculoskeletal) vs Emergency (visceral) |
| **Clinical urgency/severity** | Cardiorespiratory → Cardiology (stable) vs Emergency (acute) |
| **Patient age** | Infection/pain in children → Pediatrics |
| **Anatomical site** | Infection → Dermatology (skin), Orthopedics (joint), Emergency (systemic) |
| **Chronicity** | Chronic monitoring → specialty; acute presentations → Emergency/GP |

> **Important exception:** Small cell counts for `psychiatric_behavioral` (n=4), `medication_adjustment` (n=6), and `neurologic_symptom` (n=9) provide weak evidence for departmental routing patterns and should not be generalized without additional data.
