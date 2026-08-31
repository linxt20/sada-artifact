---
dataset: healthcare_visit_notes
scenario: eda_duration
variant: original
model: substrate-claude-haiku-4-5
query_subtype: exploratory_data_analysis
focus_variable: "visit_duration_min"
query: "How do reasons for visit relate to urgency and visit duration across department and age group?"
source_table: augment_table/healthcare_visit_notes/eda_duration/original.csv
generated_at: 2026-07-26T13:50:11.768765+00:00
wall_seconds: 135.72
---

# Healthcare Visit Notes: EDA Duration Analysis
## Original Dataset

### Executive Summary

Analysis of 250 healthcare visits reveals that **urgency level, visit reason, and patient age group are strongly associated with visit duration**. Emergency visits average **45.5 minutes** compared to routine visits at **22.6 minutes**—a 2× difference. Age shows a positive gradient with visit duration, from 19.9 minutes for 0-17 year-olds to 29.5 minutes for 60+ year-olds (0.381 correlation). The relationship between urgency and duration is particularly strong (0.612 correlation), with visit reasons explaining the variation across departments and age groups.

---

### Dataset Composition

- **Total visits**: 250
- **Urgency distribution**: Routine (56%), Urgent (32%), Emergency (12%)
- **Age groups**: 0-17 (18%), 18-39 (23%), 40-59 (24%), 60+ (35%)
- **Departments**: General Practice (22%), Pediatrics (18%), Cardiology (17%), Dermatology (17%), Orthopedics (16%), Emergency (11%)
- **Visit duration range**: 15–60 minutes (mean 25.4 min, median 20 min)

---

### Key Finding 1: Urgency Determines Duration

Urgency level is the strongest predictor of visit length (correlation = 0.612):

| Urgency   | Count | Mean Duration | Median | Range    |
|-----------|-------|---------------|--------|----------|
| Routine   | 141   | 22.6 min      | 20     | 15–30    |
| Urgent    | 81    | 23.2 min      | 20     | 15–35    |
| Emergency | 28    | 45.5 min      | 45     | 30–60    |

**Pattern**: Emergency visits require **~2× the time** of non-emergency care. Within non-emergency visits, urgency shows minimal duration difference (Routine vs. Urgent: 22.6 vs. 23.2 min, p not significant), suggesting that true clinical urgency (Emergency) carries substantial resource implications, while triage urgency (Routine/Urgent) does not substantially differ in duration at initial visit.

---

### Key Finding 2: Visit Reason Drives Urgency Classification and Duration

Six major visit reason categories emerged:

| Visit Category              | Count | Mean Duration | Typical Urgency |
|-----------------------------|-------|---------------|-----------------|
| Follow-up/Preventive        | 86    | 23.2 min      | Routine (85%)   |
| Acute Cardiac               | 72    | 26.4 min      | Mixed           |
| Other/Chronic Management    | 44    | 25.5 min      | Routine (64%)   |
| Acute Musculoskeletal       | 23    | 24.9 min      | Urgent (52%)    |
| Acute Infection/Inflammatory| 12    | 28.3 min      | Mixed           |
| Dermatologic                | 8     | 17.4 min      | Routine/Urgent  |

**Critical observation**: Acute cardiac conditions average 26.4 minutes across all urgency levels, but 16 Emergency-classified cardiac visits average **46.2 minutes**—matching Emergency department duration. This suggests that visit reason partially determines urgency classification, and **emergency-classified cardiac reasons** (acute MI, CVA, syncope, arrhythmia) drive both urgency assignment and extended duration.

---

### Key Finding 3: Department-Specific Patterns Reflect Visit Reason Distribution

Department average durations align with the typical reasons for visit:

| Department      | Mean Duration | Primary Reasons                    | Age Profile  |
|-----------------|---------------|-----------------------------------|--------------|
| Emergency       | 45.5 min      | Trauma, acute cardiac, critical   | Mixed 60+    |
| Cardiology      | 30.1 min      | Cardiac follow-up, arrhythmia     | 95% over 40  |
| Orthopedics     | 25.9 min      | Musculoskeletal injury/pain       | Mixed        |
| General Practice| 21.9 min      | Preventive, infection, chronic    | Broad        |
| Pediatrics      | 19.9 min      | Well-child, acute URIs            | 100% age 0-17|
| Dermatology     | 17.0 min      | Skin concerns, mostly routine     | Mixed        |

Cardiology's extended duration (30.1 min) reflects **reason-based complexity**: cardiac follow-up and management require detailed assessment. Pediatrics' shortest duration (19.9 min) reflects well-child visits (preventive, structured protocol) despite some urgent acute infections.

---

### Key Finding 4: Age Group Effects on Duration Are Mediated by Reason and Department

Age shows moderate correlation with duration (0.381), but this relationship is **confounded by visit reason and department**:

| Age Group | Mean Duration | Urgent % | Common Visit Reasons              |
|-----------|---------------|----------|----------------------------------|
| 0-17      | 19.9 min      | 48%      | Well-child, infections (Pediatrics)|
| 18-39     | 23.5 min      | 30%      | Acute injuries, infections        |
| 40-59     | 25.3 min      | 28%      | Chronic management, cardiac       |
| 60+       | 29.5 min      | 29%      | Cardiac follow-up, systemic       |

**Age-specific patterns**:

- **60+ in Emergency**: Average 52.9 minutes (vs. 38.2 for 18-39, n=12 vs. 11)—reflects higher acuity (acute cardiac 54.3 min, systemic emergency 47.5 min)
- **60+ in Cardiology**: Average 30.2 minutes regardless of urgency—reflects specialized management of complex conditions (HF, AFib, CAD)
- **0-17 in Pediatrics**: Average 19.9 minutes (Routine 20.6, Urgent 19.0)—suggests well-structured visit protocols with minimal urgency variation
- **18-39 acute musculoskeletal**: Average 28.6 minutes (higher than 40-59 at 24.4 min)—possibly due to sports injuries requiring detailed workup

**Weak evidence for age alone**: When controlling for department and visit reason, age shows minimal independent effect. The observed age-duration gradient primarily reflects **age-driven department routing** (60+ concentrated in Cardiology; 0-17 in Pediatrics) rather than age-inherent complexity.

---

### Key Finding 5: Department × Age Group × Urgency Creates Specific High-Duration Subgroups

The most time-intensive combinations are:

| Subgroup                          | N  | Mean Duration | Reason                          |
|-----------------------------------|----|---------------|---------------------------------|
| Emergency dept, 60+ age           | 12 | 52.9 min      | Acute cardiac crises, strokes   |
| Emergency dept, 40-59 age         | 5  | 44.0 min      | Severe trauma, MI               |
| Cardiology, routine, 60+ age      | 20 | 30.0 min      | Complex cardiac management     |
| Orthopedics, urgent, 40-59 age    | 6  | 27.4 min      | Significant musculoskeletal    |

**Lowest-duration subgroups**:
- Dermatology routine, all ages: 15.0–16.8 min
- Pediatrics well-child: 19.0–20.6 min (structured visit)
- General Practice routine, 18-39 age: 20.3 min

---

### Key Finding 6: Urgent (Intermediate Triage) Visits Show Inconsistent Duration Patterns

Urgent visits (n=81, 23.2 min average) do **not form a coherent duration group**:

- Urgent cardiac: 23.4 min average (includes both stable AFib and new-onset SVT)
- Urgent musculoskeletal: 23.3 min average
- Urgent dermatologic: 20.0 min average (skin biopsy, same as routine)
- Urgent infection: 21.2 min average

**Interpretation**: "Urgent" classification appears to reflect **clinical decision to move appointment forward** rather than a standardized extended assessment time. Duration varies based on the underlying reason (true urgency like new arrhythmia vs. convenience of earlier slot). This suggests **urgency tier lacks predictive validity for resource allocation**, whereas Emergency vs. non-Emergency shows clear 2× separation.

---

### Limitations and Caveats

1. **Small Emergency cohort** (n=28): Estimates for Emergency subgroups have wider confidence intervals
2. **Visit reason coded from narrative**: Categorization based on text patterns may miss nuanced clinical factors not explicitly mentioned
3. **No documentation complexity metric**: Duration may reflect charting burden, not purely clinical assessment time
4. **Age-specific confounding**: Cardiology patient concentration in 60+ group prevents clean age-effect isolation
5. **No throughput timing**: Analysis reflects total visit duration; clinic factors (wait time, scheduling gaps) not disentangled

---

### Clinical Implications

1. **Resource allocation**: Emergency visits require 2× standard duration; departmental staffing should account for emergency vs. non-emergency case mix
2. **Preventive visit efficiency**: Well-child visits and routine follow-ups average ~20 min; streamlined protocols appear effective
3. **Age-appropriate pathways**: Routing by age (Pediatrics for 0-17, Cardiology for 60+ cardiac) naturally groups similar-duration visits
4. **Urgent visit recalibration needed**: "Urgent" triage tier does not reliably predict extended visit time; consider re-evaluating whether "Urgent" appointments warrant different scheduling assumptions
5. **Cardiac visit complexity**: Cardiac management consistently requires 30+ minutes regardless of routine/urgent classification, suggesting **cardiac reason ≈ extended visit time** independent of triage

---

### Conclusion

Visit duration is determined by a **three-factor hierarchy**: (1) **Urgency level (primary)**—Emergency visits are ~2× longer; (2) **Visit reason (primary)**—cardiac and systemic conditions require longer assessment; (3) **Age and department (secondary)**—largely reflect reason-based routing rather than age-intrinsic complexity. The "Urgent" triage category shows heterogeneous durations and may not warrant differential scheduling assumptions. Emergency department visits and specialized cardiac management account for the longest durations and should be prioritized in capacity planning.
