---
dataset: healthcare_visit_notes
scenario: focus_inference
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What are the main types of concerns patients come in with in these visit notes?"
source_table: augment_table/healthcare_visit_notes/focus_inference/original.csv
generated_at: 2026-07-26T13:50:23.070406+00:00
wall_seconds: 43.12
---

# Patient Visit Concerns — Healthcare Visit Notes Analysis

## Dataset Overview

- **Records:** 250 visit notes (V-0001 to V-0250)
- **Departments:** General Practice, Pediatrics, Cardiology, Dermatology, Orthopedics, Emergency
- **Urgency levels:** Routine, Urgent, Emergency
- **Age groups:** 0–17, 18–39, 40–59, 60+

---

## Main Types of Patient Concerns

### 1. Chronic Disease Management (most frequent overall)
The largest single category across departments, especially in **General Practice** and **Cardiology**:

- **Cardiovascular conditions:** Hypertension, atrial fibrillation, heart failure (reduced/preserved EF), coronary artery disease, stable angina, cardiomyopathy, valvular disease (aortic stenosis, mitral regurgitation/prolapse) — e.g., V-0003, V-0010, V-0023, V-0030, V-0100
- **Metabolic/endocrine:** Type 1 and Type 2 diabetes (HbA1c management, neuropathy, DKA), hypothyroidism, hyperlipidemia, GERD, COPD, sleep apnea — e.g., V-0006, V-0042, V-0055, V-0072, V-0080, V-0089
- **Mental health:** Anxiety/GAD, depression (PHQ-9), ADHD follow-up, memory concerns — e.g., V-0026, V-0059, V-0121, V-0169

### 2. Acute Infections & Illness (very common)
Prominent across **General Practice**, **Pediatrics**, and **Emergency**:

- **Upper respiratory:** Viral URI, strep pharyngitis, acute otitis media, sinusitis, croup, bronchiolitis (RSV), acute bronchitis — e.g., V-0002, V-0011, V-0012, V-0067, V-0109, V-0192
- **Skin/soft tissue infections:** Cellulitis, MRSA folliculitis, impetigo, erysipelas — e.g., V-0041, V-0045, V-0138, V-0208
- **Other infections:** UTI, pyelonephritis, conjunctivitis, herpes zoster, STIs, gout — e.g., V-0050, V-0108, V-0093, V-0125, V-0219, V-0242

### 3. Musculoskeletal / Orthopedic Injuries & Pain (high volume)
**Orthopedics** is one of the highest-volume departments:

- **Acute traumatic injuries:** Fractures (scaphoid, hip, distal radius, ankle, supracondylar, boxer's, metacarpal, wrist falls), ligament/tendon ruptures (ACL, Achilles, meniscal tear), sprains, dislocations — e.g., V-0005, V-0019, V-0034, V-0048, V-0061, V-0105
- **Chronic degenerative/overuse:** Osteoarthritis (knee, hip), plantar fasciitis, carpal tunnel syndrome, rotator cuff tears, lateral epicondylitis, Achilles tendinopathy, lumbar spinal stenosis — e.g., V-0013, V-0040, V-0073, V-0099, V-0128, V-0181
- **Post-operative follow-up:** TKR, THR, ACL reconstruction — e.g., V-0054, V-0135, V-0161

### 4. Skin / Dermatological Conditions
**Dermatology** visits span a wide range:

- **Acne, eczema/atopic dermatitis, psoriasis, rosacea** — routine and urgent — e.g., V-0004, V-0014, V-0025, V-0071, V-0083
- **Skin cancer & precancerous lesions:** Basal cell carcinoma, squamous cell carcinoma, melanoma surveillance, actinic keratoses, dysplastic nevi — e.g., V-0009, V-0032, V-0058, V-0090, V-0152
- **Infections:** Tinea, herpes, molluscum, folliculitis barbae — e.g., V-0039, V-0113, V-0176, V-0186
- **Less common/severe:** Bullous pemphigoid, pyoderma gangrenosum, Stevens-Johnson syndrome, hidradenitis suppurativa — e.g., V-0077, V-0095, V-0159, V-0170

### 5. Preventive Care & Wellness
A consistent pattern across **General Practice** and **Pediatrics**:

- **Well-child visits** at standard developmental milestones (2-month through 16-year), covering immunizations, growth, and developmental screening — e.g., V-0007, V-0017, V-0036, V-0057
- **Annual adult physicals and preventive screenings:** Pap smears, mammograms, colon cancer screening, lipid panels, PSA, bone density — e.g., V-0046, V-0076, V-0106, V-0154, V-0189
- **Preconception and postpartum care** — e.g., V-0033, V-0101, V-0179
- **Lifestyle/preventive counseling:** Tobacco cessation, weight management, travel medicine, STI screening — e.g., V-0021, V-0214, V-0232

### 6. Emergencies / Life-Threatening Presentations
**Emergency** visits consistently involve high-acuity conditions:

- **Cardiac emergencies:** STEMI (V-0008), stroke (V-0028, V-0211), acute CHF (V-0035), GI bleed (V-0141), DKA (V-0157), sepsis (V-0175)
- **Trauma & accidents:** MVC (V-0018, V-0166), lacerations (V-0104), open fractures
- **Toxic/overdose events:** Opioid overdose (V-0150), acute alcohol intoxication (V-0185), anaphylaxis (V-0078)
- **Surgical emergencies:** Appendicitis (V-0230), acute cholecystitis (V-0062), perforated viscus (V-0114), pneumothorax (V-0202)

---

## Cross-Cutting Observations

| Pattern | Evidence |
|---|---|
| Older adults (60+) dominate chronic disease and emergency visits | Majority of cardiology and many GP follow-ups; most severe emergency cases |
| Children (0–17) mainly present for well-child visits and acute infections | Pediatrics split roughly evenly between routine and urgent |
| Working-age adults (18–59) drive orthopedic injuries and acute GP concerns | Sports/occupational trauma, acute infections, mental health |
| Routine vs. urgent breakdown | Most GP visits are routine chronic care; orthopedics mixes routine follow-up and acute trauma; all emergency visits are high acuity |

---

## Exceptions & Weaker Evidence

- **Mental health** concerns appear but are **underrepresented** relative to real-world prevalence — only a few explicit psychiatric visits (e.g., V-0059, V-0133, V-0169); most are incidental screening findings.
- **Social determinants and behavioral health** (e.g., V-0064 bedwetting linked to parental divorce, V-0155 boxer fracture with anger counseling) appear occasionally but are not a primary category in this dataset.
- A few **rare/complex diagnoses** (Kawasaki disease V-0120, Stevens-Johnson V-0170, bullous pemphigoid V-0077) are present but are statistical outliers and should not be over-weighted.
- The dataset appears **synthetic/structured** — departments and urgency levels are evenly distributed, which may not reflect real-world visit proportions.

---

## Summary

The five dominant concern types are: **(1) chronic disease management** (cardiovascular, metabolic, neurological), **(2) acute infections and illness**, **(3) musculoskeletal injuries and pain**, **(4) dermatological conditions**, and **(5) preventive/wellness care**. Emergency cases represent a distinct sixth category defined by life-threatening acuity. Concern type correlates strongly with department, urgency level, and patient age group.
