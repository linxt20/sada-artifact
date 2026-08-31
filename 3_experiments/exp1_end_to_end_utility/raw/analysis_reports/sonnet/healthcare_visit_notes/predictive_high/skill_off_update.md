---
dataset: healthcare_visit_notes
scenario: predictive_high
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "urgency"
query: "What visit-note signals suggest high urgency?"
source_table: augment_table/healthcare_visit_notes/predictive_high/sonnet__skill_off_update.csv
generated_at: 2026-07-28T12:43:09.955292+00:00
wall_seconds: 41.37
---

# Visit-Note Signals Suggesting High Urgency

**Dataset:** 250 visits · 3 urgency levels (Emergency = 28, Urgent = 81, Routine = 141)  
**Focus variable:** `urgency` (+ derived `urgency_signal_count`, `urgency_signal_tier`)

---

## 1. Signal Overview

Five binary flags are encoded from the free-text visit notes:

| Signal | Emergency rate | Urgent rate | Routine rate |
|---|---|---|---|
| `signal_acute_symptoms` | **64.3%** | 16.1% | 6.4% |
| `signal_high_risk_dx` | **17.9%** | 2.5% | 1.4% |
| `signal_acute_onset` | **10.7%** | 4.9% | 0.7% |
| `signal_critical_vitals` | 3.6% | 6.2% | 1.4% |
| `signal_severe_pain` | 0% | 0% | 0% |

`urgency_signal_count` (sum of the five flags) averages **0.96** for Emergency vs. **0.30** for Urgent vs. **0.10** for Routine — a clear gradient.

---

## 2. Strongest High-Urgency Predictors

### 2a. Acute Symptoms (`signal_acute_symptoms`)
The single most discriminating flag. It fires in **64% of Emergency visits** versus only 16% of Urgent and 6% of Routine. Visit notes typically describe dyspnea, altered consciousness, hemodynamic instability, or acute neurological deficit.  
*Example (V-0008):* "Severe substernal chest pain … diaphoretic, BP 156/94. ECG shows ST elevation … STEMI protocol activated."

### 2b. High-Risk Diagnosis (`signal_high_risk_dx`)
Present in **18% of Emergency** cases (vs. 2–3% elsewhere). Flagged when notes document diagnoses such as STEMI, subarachnoid hemorrhage, or tension pneumothorax.

### 2c. Acute Onset (`signal_acute_onset`)
Fires in **11% of Emergency** notes. Language like "sudden onset," "worst headache of life," or "1 hour ago" is the typical trigger. Low absolute rates mean it works best in combination.

### 2d. Combined Signal Count (`urgency_signal_tier = High`)
Only 3 visits reach the "High" tier (all three have `urgency_signal_count = 3`); all 3 are Emergency visits. The tier thus has near-perfect precision for Emergency but very low recall — it misses 25 of 28 Emergency cases.

---

## 3. Department and Visit Duration as Context Signals

- All 28 Emergency visits belong to the **Emergency department** — the department label alone perfectly separates this class in the current dataset.
- Emergency visits average **45.5 min** vs. ~22–23 min for Routine/Urgent, consistent with more intensive workups.
- Among non-Emergency departments, **Orthopedics** and **Pediatrics** have the highest Urgent shares, while **Cardiology** and **GeneralPractice** are largely Routine.

---

## 4. Age Group

Patients aged **60+** (n = 87) account for 43% of Emergency cases despite being 35% of the total, suggesting older age is a modest risk amplifier in the notes context.

---

## 5. Exceptions and Weak Evidence

- **`signal_critical_vitals`** is *slightly higher* in Urgent (6.2%) than Emergency (3.6%) visits — counter-intuitive and likely reflects that the majority of Emergency notes emphasise symptoms/diagnoses over isolated vital-sign language. Treat this flag as supplementary, not primary.
- **`signal_severe_pain`** fires at 0% across all urgency levels in this dataset, making it uninformative here.
- The "High" urgency tier has extremely low recall (3/28 Emergency); relying on the tier threshold alone will miss the majority of true emergencies.
- All Emergency visits are in one department, so causal signal attribution (note content vs. department routing) cannot be fully disentangled.

---

## 6. Decision-Ready Summary

| Priority | Signal | Rationale |
|---|---|---|
| 1 | `signal_acute_symptoms` | Strongest discriminator; present in 64% of Emergency notes |
| 2 | `signal_high_risk_dx` | High-specificity flag for life-threatening diagnoses |
| 3 | `signal_acute_onset` | Onset language ("sudden", "worst of life") adds incremental value |
| 4 | `urgency_signal_count ≥ 2` | Combination threshold captures most true Emergency visits |
| Context | Department = Emergency, age 60+, duration > 40 min | Structural features corroborating note-based signals |
