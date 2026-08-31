---
dataset: healthcare_visit_notes
scenario: predictive_long
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "visit_duration_min"
query: "What visit-note signals suggest a longer visit?"
source_table: augment_table/healthcare_visit_notes/predictive_long/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/healthcare_visit_notes__predictive_long/analyses/original/analysis.md
wall_seconds: 84.67
---

# Visit-Note Signals for Longer Visit Duration
**Dataset:** `healthcare_visit_notes__predictive_long.csv` | **Focus variable:** `visit_duration_min` | **N = 216 visits**

---

## Overview

The dataset contains six columns: `visit_id`, `department`, `urgency`, `age_group`, `visit_duration_min`, and a free-text `reason_for_visit`. Duration ranges from **15 to 60 minutes**. Three structured columns (`department`, `urgency`, `age_group`) provide the clearest, most consistent signals; the note text provides corroborating detail.

---

## 1. Department Is the Strongest Single Predictor

| Department | Typical Duration | Range Seen |
|---|---|---|
| Emergency | **45–60 min** | 30–60 min |
| Cardiology | **30 min** | 30–35 min |
| Orthopedics (Urgent) | **25–30 min** | 20–30 min |
| Orthopedics (Routine) | **25 min** | 25 min |
| GeneralPractice | **20–25 min** | 20–25 min |
| Pediatrics | **15–20 min** | 15–30 min |
| Dermatology | **15–20 min** | 15–20 min |

**Emergency** visits are the longest category without exception. Every Emergency-urgency record (STEMI, stroke, CHF exacerbation, DKA, sepsis, massive hemoptysis, GI bleed, subarachnoid hemorrhage, etc.) logs 30–60 minutes, with life-threatening presentations reaching the upper end (55–60 min). **Cardiology** is the next longest, with every Routine and Urgent cardiology note at exactly 30 minutes, rising to 35 for new paroxysmal AFib with complex medication initiation.

---

## 2. Urgency Level Shifts Duration Upward

Within departments, urgency escalates duration:

- **Pediatrics**: Routine well-child visits are almost uniformly **20 min**; simple urgent visits (roseola, hand-foot-mouth, febrile seizure, croup) land at **15 min**; complex urgent visits (Kawasaki disease, possible appendicitis) reach **25 min**.
- **GeneralPractice**: Routine visits cluster at **20 min**; Urgent visits stay at 20–25 min; Emergency-coded GP notes do not appear—these route to Emergency department.
- **Orthopedics**: Urgent fractures, ruptures, or acute radiculopathies consistently hit **30 min** vs. **25 min** for routine follow-up.

The Emergency urgency code is the single most reliable indicator of a 40+ min visit.

---

## 3. Note-Text Patterns Associated with Longer Duration

### 3a. Procedures Performed During the Visit
Notes that document an **in-visit intervention** consistently accompany longer appointments:
- `"STEMI protocol activated, cath lab notified"` → 45 min
- `"tPA administered. Mechanical thrombectomy team mobilized"` → 55 min
- `"Chest tube placed"` → 40 min
- `"Closed reduction performed under hematoma block"` → 30 min
- `"IV insulin drip and fluids initiated"` → 45 min
- `"Resuscitated with 30 mL/kg fluids"` → 50 min
- `"Wound irrigated and closed with 12 sutures"` → 30 min (short relative to severity)

By contrast, notes describing in-office **injections** or **cryotherapy** (Dermatology/Orthopedics) do not push duration past 20–25 min.

### 3b. Multi-System or Multi-Condition Complexity
Visits with multiple active problems documented in the note are longer:
- Polypharmacy review (12 medications, Beers criteria, 2 changes): **25 min**
- Diabetes with neuropathy, foot exam, gabapentin, podiatry referral: **25 min**
- Marfan syndrome with multi-specialty coordination (ophthalmology, orthopedics, annual echo): **30 min**
- Single-condition straightforward visits (tinea versicolor, seborrheic keratitis, folliculitis barbae): **15 min**

### 3c. Monitoring and Imaging Ordered Urgently
Notes that include **"ordered urgently," "stat," or specialist consultation activated immediately** correlate with ≥30 min:
- `"CT head and C-spine ordered. Trauma team evaluating"` → 60 min
- `"CT angio shows lung mass… Interventional radiology consulted"` → 60 min
- `"Echo and labs ordered, hospital admission arranged"` (Kawasaki) → 20 min (exception—note text signals complexity but duration stays 20 min because the bulk of workup will happen inpatient)

### 3d. Hemodynamic Instability or Severity Language
Phrases in notes such as **"BP 92/58," "O2 sat 86%," "GCS [low number]," "NIHSS [high number]," "lactate 4.2," "anion gap 22," "massive hemoptysis"** are all exclusive to 40–60 min Emergency visits.

### 3e. Admissions and Specialist Consults During Visit
Notes ending with **"admitted," "ICU admission," "OR booked," or "[specialty] consulted"** map to longer visits. These indicate the ED team managed the patient for an extended period before handoff.

---

## 4. Age Group

Older patients (60+) tend to have slightly longer visits in GeneralPractice (25 min vs. 20 min for 18–39), consistent with greater chronic disease burden reflected in notes (polypharmacy, multi-condition management, CKD, memory evaluation). However, age alone is not a strong predictor independent of department and clinical complexity; Pediatric urgent visits for older children can match or exceed simple adult routine visits.

---

## 5. Signals That Do NOT Reliably Extend Duration

| Signal | Observed Effect |
|---|---|
| Urgency = "Urgent" alone (outside Emergency) | +0–5 min; unreliable without procedure or complexity |
| In-office injection or biopsy | Stays at 20–25 min; does not push to 30+ |
| New diagnosis requiring new medication | Adds counseling text but duration stays at routine baseline (15–20 min in Dermatology) |
| Pediatric Urgent | Often **shorter** (15 min) for simple viral URIs than Routine (20 min) well-child visits |

---

## 6. Decision-Ready Summary

The strongest multi-signal rule for predicting a long visit (≥30 min):

1. **Department = Emergency** → expect 40–60 min (strongest signal)
2. **Department = Cardiology** (any urgency) → reliably 30 min
3. **Note contains in-visit resuscitation, intubation, thrombolytics, IV drips, or OR booking** → 45–60 min
4. **Note documents hemodynamic instability** (shock vitals, altered mental status, severe hypoxia) → 45–60 min
5. **Department = Orthopedics + note describes fracture reduction or acute rupture** → 30 min

Short visits (≤15 min) are dominated by **Dermatology Routine** notes describing a single, well-controlled dermatologic condition with minimal intervention.

**Key exception:** The Pediatric Urgent category is bimodal—simple viral presentations (roseola, hand-foot-mouth, croup) clock in at 15 min, while systemically ill or surgically urgent children (Kawasaki, possible appendicitis) reach 20–25 min. Urgency code alone is insufficient for this department.
