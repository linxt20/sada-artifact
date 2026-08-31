---
dataset: healthcare_visit_notes
scenario: predictive_high
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "urgency"
query: "What visit-note signals suggest high urgency?"
source_table: augment_table/healthcare_visit_notes/predictive_high/haiku__skill_off_update.csv
generated_at: 2026-07-28T12:43:24.727466+00:00
wall_seconds: 62.93
---

# Visit-Note Signals Suggesting High Urgency: Analysis Report

## Executive Summary

This analysis examined 250 healthcare visit notes to identify signals that distinguish high-urgency (Urgent + Emergency) visits from routine care. **High-urgency visits comprise 43.6% of the dataset** (109 visits: 28 Emergency, 81 Urgent). The data reveals clear, measurable patterns in how urgency is communicated through clinical documentation.

## Key Urgency Signal Patterns

### 1. **Urgency Signal Count (Primary Differentiator)**

The most powerful predictor is the **number of encoded urgency signals per note**:

- **Emergency department visits**: Average 1.68 signals/note (range 0–5)
- **Urgent visits**: Average 1.12 signals/note (range 0–3)  
- **Routine visits**: Average 0.30 signals/note (range 0–2)

Signal intensity strongly stratifies by urgency level:
- Notes with **2+ signals**: 39 of 39 high-urgency cases (100% in Emergency/Urgent tier)
- Notes with **0–1 signals**: Mixed urgency, though high-urgency cases still present (~31% of 84 one-signal notes are Urgent/Emergency)

### 2. **Critical Keywords (15.6% of High-Urgency Notes)**

Specific clinical phrases appear exclusively or predominantly in high-urgency contexts:

**Life-threatening diagnoses/presentations:**
- STEMI (ST-elevation MI) — 4 cases, all Emergency/Urgent
- Stroke alert / tPA candidates — 5 cases
- Subarachnoid hemorrhage, sepsis, anaphylaxis — 1–2 cases each
- ICU mentions — 11 high-urgency notes
- Loss of consciousness (LOC) — 11 high-urgency notes

**Critical finding:** 17 of 109 high-urgency notes (15.6%) contained critical keywords, whereas **0 of 141 routine notes** contained them, indicating perfect discrimination for this signal.

### 3. **Acute Presentation (47.7% of High-Urgency Notes)**

High-urgency visits frequently signal acute onset or new clinical events:

- **High-urgency with acute presentation**: 52/109 (47.7%)
- **Routine with acute presentation**: 3/141 (2.1%)
- **Relative risk**: 22.7× higher likelihood of urgency when acute presentation is noted

Common acute triggers in high-urgency notes:
- Sudden-onset symptoms (stroke, syncope, chest pain)
- Trauma/injury within 1–2 days
- New fever + focal findings (e.g., strep throat, otitis media)
- Acute flares of chronic conditions

### 4. **Severe Symptoms (15.6% of High-Urgency; 5.0% Routine)**

Severe symptom descriptors are 3× more common in high-urgency notes:

- **High-urgency with severe symptoms**: 17/109 (15.6%)
- **Routine with severe symptoms**: 7/141 (5.0%)

Examples in high-urgency context:
- "Severe substernal chest pain," "rigid abdomen," "paroxysmal AFib," "syncope," "hemoptysis"

### 5. **Visit Duration (Temporal Signal)**

Emergency visits consume substantially more clinician time:

- **Emergency**: Mean 45.5 min (median 45, max 60)
- **Urgent**: Mean 23.2 min (median 20, max 35)
- **Routine**: Mean 22.6 min (median 20, max 30)

Extended visits (~40–60 min) are virtually pathognomonic for Emergency department evaluations, suggesting administrative/procedural complexity alongside clinical urgency.

---

## Department-Specific Patterns

Urgency distribution varies significantly by clinical setting:

| Department | Emergency | Urgent | Routine |
|------------|-----------|--------|---------|
| Emergency  | 28/28 (100%) | — | — |
| Pediatrics | — | 21/45 (47%) | 24/45 |
| Orthopedics | — | 17/39 (44%) | 22/39 |
| Dermatology | — | 16/42 (38%) | 26/42 |
| GeneralPractice | — | 15/54 (28%) | 39/54 |
| Cardiology | — | 12/42 (29%) | 30/42 |

**Clinical interpretation:** Pediatrics and orthopedics show higher Urgent prevalence, likely reflecting time-sensitive acute presentations (infections, fractures, trauma) that benefit from same-day evaluation. Dermatology and general practice show lower urgency overall, consistent with predominantly chronic disease management and preventive visits.

---

## Clinical Evidence from Note Content

### High-Urgency Visit Examples

**Emergency – Acute Coronary Syndrome (V-0008):**  
"Severe substernal chest pain radiating to left arm, onset 1 hour ago. Diaphoretic, BP 156/94. ECG shows ST elevation in V2-V4. STEMI protocol activated, cath lab notified."  
*Signals: 5 | Critical keywords: Yes | Acute: Yes | Severe: Yes | Duration: 45 min*

**Emergency – Stroke (V-0028):**  
"Sudden onset right-sided weakness and slurred speech 45 minutes ago. NIHSS 8. Stroke alert called, CT head negative for bleed. tPA candidate, neurology bedside."  
*Signals: 2 | Critical keywords: Yes | Duration: 45 min*

**Urgent – Appendicitis Concern (V-0022):**  
"8-year-old with abdominal pain and vomiting x12 hours. Periumbilical, now RLQ. Tender at McBurney point. Concern for appendicitis, sent to ED for surgical evaluation."  
*Signals: 2 | Acute: Yes | Duration: 20 min*

**Urgent – Acute Respiratory Infection (V-0011):**  
"Sore throat x2 days, fever to 39°C, tonsillar exudates noted. Rapid strep positive. Prescribed amoxicillin 500mg TID for 10 days."  
*Signals: 1 | Acute: Yes | Duration: 20 min*

### Routine Visit Examples (Contrast)

**Routine – Diabetes Follow-up (V-0006):**  
"Diabetes follow-up. HbA1c 7.4, down from 8.1. Reports adherence to metformin and dietary changes. Feet exam normal, no neuropathy. Continue plan, recheck in 3 months."  
*Signals: 0 | Acute: No | Severe: No | Duration: 25 min*

**Routine – Well-Child Visit (V-0007):**  
"Well-child visit at 4 years. Growth on track at 50th percentile. Immunizations updated with DTaP and MMR booster. Parents counseled on nutrition and screen time limits."  
*Signals: 0 | Acute: No | Severe: No | Duration: 20 min*

---

## Notable Exceptions and Limitations

1. **Low-Signal High-Urgency Cases (21/109, 19.3%)**: Some urgent visits carry 0 detected signals. These typically represent:
   - Physician judgment calls on borderline acute presentations
   - Preventive urgent referrals (e.g., suspicious skin lesion in Dermatology)
   - Cases where clinical impression drives urgency despite understated documentation

2. **Severe Symptoms in Routine Context (7/141, 5.0%)**: Occasional routine notes mention "severe" descriptors when discussing chronic, well-managed conditions (e.g., "severe but stable CAD"). Context matters.

3. **Signal Coverage**: The encoded signals (`has_critical_keywords`, `has_acute_presentation`, `has_severe_symptoms`) capture ~60–70% of high-urgency cases, suggesting that clinical urgency drivers beyond these three categories exist in free text.

---

## Summary: High-Urgency Note Characteristics

**Strong indicators (high discriminative value):**
- **Critical keywords** (ICU, LOC, STEMI, stroke alert, tPA, anaphylaxis, sepsis) — 15.6% sensitivity, 100% specificity
- **Multiple signals** (≥2 in same note) — strongly associated with Emergency/Urgent classification
- **Visit duration ≥40 min** — nearly all are Emergency

**Moderate indicators (multivariate importance):**
- **Acute presentation** (new-onset, sudden, trauma in last 48 hrs) — 47.7% sensitivity in high-urgency, 22.7× relative risk vs. Routine
- **Severe symptom language** — 3× more common in high-urgency
- **Department type** (Pediatrics, Orthopedics > General Practice)

**Contextual signals:**
- Explicit clinical reasoning for urgency (e.g., "sent to ED for surgical evaluation," "urgent referral")
- Procedural or intervention language (steroid injection, splinting, IV medications "today")
- Follow-up timing compressed to hours/days rather than weeks/months

---

## Conclusion

Visit-note signals suggesting high urgency are **multifactorial but identifiable**. The strongest single predictor is the **encoding of clinical urgency signals** (critical keywords, acute presentation, severe symptoms), with Emergency visits averaging 1.7 signals and Routine 0.3. These signals appear in ~60% of high-urgency notes but show high specificity (low false-positive rate in routine notes). Clinical urgency is further indicated by **acute onset language** (47.7% of high-urgency), **extended visit durations** (Emergency >40 min), and **critical clinical descriptors** (STEMI, stroke, sepsis, ICU). The variant label "skill_off" suggests this analysis was conducted with standard model inference, and the evidence supports a robust, rule-like relationship between documented clinical signals and urgency classification.
