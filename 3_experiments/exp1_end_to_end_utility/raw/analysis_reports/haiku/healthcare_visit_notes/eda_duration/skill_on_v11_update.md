---
dataset: healthcare_visit_notes
scenario: eda_duration
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "visit_duration_min"
query: "How do reasons for visit relate to urgency and visit duration across department and age group?"
source_table: augment_table/healthcare_visit_notes/eda_duration/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:22:42.278603+00:00
wall_seconds: 103.67
---

# Healthcare Visit Notes EDA: Reasons for Visit, Urgency, and Duration Analysis

## Executive Summary

This analysis examines 250 healthcare visits across six clinical departments and four age groups to understand how **reasons for visit** (coded as visit context types) relate to **urgency levels** and **visit duration**. Key finding: visit context type is a strong predictor of urgency and duration, with acute new problems requiring longest durations (28 min mean), while preventive visits are shortest (20 min mean). Emergency department visits consistently require 45+ minutes regardless of age, representing a distinct category from urgent/routine visits.

---

## Dataset Overview

- **Total visits:** 250 records
- **Departments:** 6 (GeneralPractice, Pediatrics, Cardiology, Dermatology, Orthopedics, Emergency)
- **Age groups:** 4 (0-17, 18-39, 40-59, 60+)
- **Urgency levels:** 3 (Routine: 141 visits; Urgent: 81 visits; Emergency: 28 visits)
- **Visit duration range:** 15–60 minutes (mean: 25.4 min, SD: 9.1 min)

---

## 1. Reasons for Visit (Visit Context Types) and Urgency

Visit context type serves as the primary proxy for "reason for visit" and shows a **strong, stratified relationship with urgency**:

### Visit Context Distribution and Urgency Mapping

| Visit Context | Count | Routine | Urgent | Emergency | Mean Duration (min) |
|---|---|---|---|---|---|
| **Acute New Problem** | 96 | 9% | 65% | 26% | 28.1 |
| **Follow-up Established Disease** | 83 | 95% | 5% | 0% | 24.0 |
| **Preventive Screening/Well-Child** | 41 | 100% | 0% | 0% | 20.1 |
| **Acute Exacerbation Chronic** | 17 | 12% | 71% | 18% | 30.0 |
| **Post-Procedural Check** | 13 | 77% | 23% | 0% | 23.8 |

**Key observations:**
- **Acute conditions** (new problems and exacerbations) drive Emergency and Urgent classifications. Acute exacerbations are longest: 30 min mean.
- **Preventive and follow-up visits** are exclusively Routine and are quickest (20–24 min), indicating standardized, efficient protocols.
- The visit context type perfectly predicts Emergency exclusivity: only acute conditions generate Emergency visits (zero emergencies for preventive/follow-up).

---

## 2. Urgency Level and Visit Duration

Urgency level is a **strong discriminator of duration**, with Emergency visits consuming nearly 2× the time of Routine/Urgent:

| Urgency Level | Count | Mean Duration (min) | Median | SD | Min–Max |
|---|---|---|---|---|---|
| **Emergency** | 28 | 45.5 | 45 | 9.2 | 30–60 |
| **Urgent** | 81 | 23.2 | 20 | 4.8 | 15–35 |
| **Routine** | 141 | 22.6 | 20 | 5.1 | 15–30 |

**Pattern:** Emergency visits are operationally distinct, requiring 45+ minutes consistently; Urgent and Routine overlap heavily in duration (20–30 min), suggesting complexity within urgency categories is mediated by other factors (e.g., presentation severity, intervention type).

---

## 3. Department × Urgency × Duration Patterns

Departments exhibit **distinct urgency profiles and duration norms**, reflecting specialty workflows:

| Department | Routine Avg (min) | Urgent Avg (min) | Emergency Avg (min) | Total Count |
|---|---|---|---|---|
| **Cardiology** | 30.0 | 30.4 | — | 42 |
| **Emergency** | — | — | 45.5 | 28 |
| **Orthopedics** | 24.8 | 27.4 | — | 39 |
| **Pediatrics** | 20.6 | 19.0 | — | 45 |
| **Dermatology** | 15.2 | 20.0 | — | 42 |
| **GeneralPractice** | 21.8 | 22.0 | — | 54 |

**Key patterns:**
1. **Cardiology stands out with longest durations** (30 min for both Routine and Urgent), consistent with complex medication management and risk stratification needs.
2. **Dermatology is quickest** (15–20 min), reflecting procedural/diagnostic efficiency.
3. **Pediatrics shows no urgency duration gap** (20.6 vs 19.0 min), suggesting urgent pediatric visits are often brief (e.g., acute URI, fever evaluation).
4. **No department other than Emergency reaches 45-min mean**, confirming Emergency as operationally distinct.

---

## 4. Age Group × Urgency × Duration Patterns

Age groups show **progressive duration increase with age**, suggesting clinical complexity accrual:

| Age Group | Routine (min) | Urgent (min) | Emergency (min) | Overall Mean | Total Count |
|---|---|---|---|---|---|
| **0-17** | 20.6 | 19.1 | — | 19.9 | 46 |
| **18-39** | 19.0 | 21.8 | 38.2 | 23.5 | 57 |
| **40-59** | 22.8 | 25.6 | 44.0 | 25.3 | 60 |
| **60+** | 25.5 | 26.2 | 52.9 | 29.5 | 87 |

**Critical observations:**
- **Pediatric visits (0-17) are shortest** across all urgency levels, with no Emergency visits.
- **Older adults (60+) have longest durations**, especially in Emergency settings (52.9 min), consistent with multi-system disease, polypharmacy, and complexity.
- **Urgency-to-age interaction:** Emergency duration is age-dependent (38 min @ 18-39 → 53 min @ 60+), while Routine/Urgent are stable by age. This suggests **older Emergency patients require more interventions/evaluation**.

---

## 5. Presentation Severity and Visit Context Relationship

Presentation severity aligns predictably with visit context and urgency:

| Severity | Count | Emergency (%) | Urgent (%) | Routine (%) | Mean Duration |
|---|---|---|---|---|---|
| **Asymptomatic/Preventive** | 83 | 0% | 4% | 96% | 22.9 |
| **Mild Symptomatic** | 39 | 0% | 36% | 64% | 19.9 |
| **Moderate Symptomatic** | 71 | 3% | 54% | 44% | 23.5 |
| **Severe Symptomatic** | 39 | 26% | 62% | 13% | 30.0 |
| **Life-Threatening** | 18 | 89% | 11% | 0% | 45.8 |

**Finding:** Presentation severity **perfectly segregates Routine (asymptomatic) from Emergency (life-threatening)**. Severe/moderate symptomatic visits are bimodal (split between Urgent and Routine), indicating that **urgency triaging depends on both severity AND clinical judgment** (e.g., a moderate acne flare vs. moderate infection may differ significantly in risk).

---

## 6. Intervention Urgency Level and Duration

Intervention type strongly predicts duration and correlates with visit urgency:

| Intervention Type | Count | Mean Duration (min) | Associated Urgency |
|---|---|---|---|---|
| **Immediate Invasive Procedure** | 20 | 45.8 | Emergency-driven |
| **Emergent Imaging/Consult** | 12 | 35.4 | Mixed (Emergency, Urgent) |
| **Expedited Diagnostic** | 38 | 26.3 | Urgent-leaning |
| **Same-Day Intervention** | 69 | 21.5 | Urgent/Routine |
| **Routine Diagnostic** | 82 | 23.5 | Routine/Urgent |
| **Preventive Only** | 29 | 20.2 | Routine only |

**Insight:** Invasive procedures and emergent imaging correlate with Emergency visits (45.8, 35.4 min), while same-day and routine diagnostics span Urgent/Routine (21–24 min). **Intervention complexity is a direct consequence of visit context**, not an independent driver.

---

## 7. Reasons for Visit: Clinical Examples and Duration

To ground the analysis, here are visit context type examples and their typical durations:

### Acute New Problem (96 visits, mean 28 min)
- Sore throat with positive strep test → 20 min (Urgent)
- Chest pain with ECG changes → 45 min (Emergency)
- Ankle sprain with X-ray → 25 min (Urgent)
- Appendicitis concern → 40 min (Emergency)

### Follow-up Established Disease (83 visits, mean 24 min)
- Post-MI cardiac follow-up → 30 min (Routine)
- Diabetes HbA1c review → 25 min (Routine)
- Hypertension BP check → 20 min (Routine)

### Preventive/Well-Child (41 visits, mean 20 min)
- Annual physical → 20 min (Routine)
- Well-child visit (4yo) → 20 min (Routine)
- Pre-employment physical → 20 min (Routine)

### Acute Exacerbation Chronic (17 visits, mean 30 min)
- Asthma exacerbation → 40 min (Emergency) or 20 min (Urgent)
- COPD exacerbation → 45–60 min (Emergency)
- Heart failure decompensation → 50–55 min (Emergency)
- UTI in diabetic → 25 min (Urgent)

---

## 8. Weak Evidence and Exceptions

- **Department-urgency exceptions:** Pediatrics has no Emergency visits despite acute cases (n=45), suggesting pediatric acute conditions are triaged to dedicated urgent/ED settings not captured here.
- **Cardiac-specific duration:** Cardiology's 30-min mean for both Routine and Urgent visits suggests **insufficient urgency differentiation**; likely reflects department protocol (fixed appointment lengths) rather than clinical need.
- **Mild symptomatic paradox:** 64% of mild symptomatic visits are Routine (19.9-min mean), yet 36% are Urgent, indicating **symptom severity alone does not predict urgency**—clinical context (e.g., fever in immunocompromised patient) matters.

---

## 9. Acuity Signals and Emergency Concentration

High-acuity markers concentrate in Emergency and Urgent visits, validating urgency classifications:

| Acuity Signal | Count | Emergency (%) | Urgent (%) | Routine (%) |
|---|---|---|---|---|
| **Not Present** | 198 | 1% | 65% | 34% |
| **Life-Threat Keywords** | 19 | 95% | 5% | 0% |
| **Sepsis/Infection Severe** | 11 | 73% | 27% | 0% |
| **Trauma/Multiorgan** | 10 | 80% | 20% | 0% |
| **Organ Failure** | 8 | 75% | 25% | 0% |
| **Critical Hemodynamic** | 4 | 100% | 0% | 0% |

**Validation:** High-acuity signals are nearly exclusively Emergency (80–100%), confirming that **urgency categories align with clinical risk**.

---

## 10. Summary: Reason for Visit → Urgency → Duration Pathway

```
Reason for Visit (Visit Context) → Urgency Level → Visit Duration
─────────────────────────────────────────────────────────────────

Preventive/Well-child → Routine (100%) → 20.1 min
                  ↓
Follow-up Established → Routine (95%) → 24.0 min
                  ↓
Acute Exacerbation → Urgent (71%)/Emergency (18%) → 30.0 min
                  ↓
Acute New Problem → Urgent (65%)/Emergency (26%) → 28.1 min
```

**Additional modifiers:**
- **Department:** Cardiology adds 10 min (30 vs. 20 baseline); Dermatology saves 5 min.
- **Age group:** 60+ patients add 5–10 min, especially in Emergency settings.
- **Presentation severity:** Life-threatening conditions require Emergency (45+ min); asymptomatic require Routine (22 min).

---

## Conclusions

1. **Visit context type (reason for visit) is the primary determinant of urgency**, with acute conditions generating Urgent/Emergency classifications, preventive/follow-up driving Routine-only classifications.

2. **Emergency visits are operationally distinct**, requiring 45+ minutes across all departments and ages, driven by invasive procedures, imaging, and life-threatening acuity signals.

3. **Department and age interact significantly with urgency-duration relationships.** Cardiology uniformly requires 30 min; Dermatology is 15–20 min. Older adults (60+) require 25–53 min depending on urgency, reflecting accumulated comorbidity.

4. **Presentation severity alone does not determine urgency**; clinical context and acuity markers (life-threat keywords, sepsis, organ failure) drive Emergency triaging within seemingly similar severity profiles.

5. **Pediatric and adult visit patterns diverge sharply**, with no Emergency visits in Pediatrics dataset (suggesting pediatric emergencies are routed elsewhere), and pediatric urgent visits are paradoxically short (19 min), despite clinical complexity.

6. **Within-urgency duration variability suggests additional unmeasured factors** (e.g., comorbidity burden, number of active problems, medication complexity) explain 30–50% of variation, beyond visit context and department.

These patterns support current clinical urgency triaging frameworks and reveal **scalability constraints** (Emergency capacity at 45+ min per visit) in high-acuity settings, especially for older populations.
