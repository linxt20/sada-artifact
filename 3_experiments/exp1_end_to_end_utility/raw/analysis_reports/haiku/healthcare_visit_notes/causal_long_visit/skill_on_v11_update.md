---
dataset: healthcare_visit_notes
scenario: causal_long_visit
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "visit_duration_min"
query: "Which clinical factors best explain longer visit durations?"
source_table: augment_table/healthcare_visit_notes/causal_long_visit/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:21:11.455537+00:00
wall_seconds: 42.67
---

# Analysis Report: Clinical Factors Explaining Longer Visit Durations

## Executive Summary

This analysis examined 250 healthcare visits to identify clinical factors associated with longer visit durations. The median visit duration is 25 minutes, with visits ranging from 15 to 60 minutes. **Emergency acuity level and emergency department settings are the dominant drivers of longer visits**, accounting for over 96% of all visits exceeding 30 minutes.

---

## Key Clinical Factors Driving Longer Visits

### 1. **Emergency Acuity Level (Strongest Driver)**
- **96% of long visits (>30 min) classified as "emergency_critical"**
- Mean duration for emergency_critical visits: **41.8 minutes** (SD: 12.0)
- Mean duration for routine_stable visits: **22.3 minutes** (SD: 5.0)
- Mean duration for urgent_acute visits: **24.2 minutes** (SD: 5.4)

**Clinical Context**: Emergency-critical presentations involve life-threatening conditions requiring rapid assessment, multiple concurrent interventions, and specialist coordination, naturally extending visit duration.

### 2. **Emergency Department Setting (Near-Perfect Association)**
- **96% of long visits (26 of 27 >30 min) occurred in the Emergency Department**
- Mean ED duration: **45.5 minutes**
- Cardiology mean: 30.1 minutes, Orthopedics: 25.9 minutes, Dermatology: 17.0 minutes
- Emergency visits show highest variability (SD: 9.2 min), indicating diverse case severity

**Constraint Note**: This strong departmental effect may reflect data structure rather than pure clinical causality, as emergency departments inherently handle acute conditions with longer processing times.

### 3. **Acute Clinical Complexity**
- Long visits predominantly involve **acute single-issue cases (96%)** rather than chronic disease management
- Mean duration for acute_single_issue: **27.2 minutes** (SD: 12.0)
- Mean duration for chronic_disease_management: **25.6 minutes** (SD: 5.0)
- Preventive_wellness cases average only **20.1 minutes**

**Clinical Rationale**: Acute emergencies (MI, stroke, trauma, sepsis, anaphylaxis) require rapid diagnostic workup and time-critical interventions versus routine chronic follow-ups.

### 4. **Diagnostic Workload (Imaging/Labs Requirement)**
- Long visits show **66.7% require imaging or labs** vs. 37.2% in short visits
- Mean duration with imaging/labs ordered: **28.9 minutes**
- Mean duration with clinical assessment only: **22.3 minutes**
- Procedure-based visits: **24.0 minutes** (lower than imaging/labs due to emergency mix)

**Clinical Pattern**: Emergency CT scanning, ECG, labs for troponin/glucose/coagulation, and imaging interpretation add 5-7 minutes to core clinical assessment time.

### 5. **Specialist Referral Interventions**
- **63% of long visits resulted in surgical or specialist referrals**
- Mean duration for surgical_or_specialist_referral interventions: **31.9 minutes**
- Mean duration for medication_adjustment_or_initiation: **24.3 minutes**
- Long visits are **4.3× more likely** to involve specialist referrals (63% vs. 15%)

**Clinical Significance**: Cases like STEMI, stroke, femur fracture, or acute sepsis require real-time communication with cardiology, neurology, orthopedic surgery, or ICU teams.

---

## Secondary Factors (Weaker Evidence)

### Age and Urgency Categorization
- Urgency field shows 96.3% of long visits are "Emergency" (vs. 0.9% in short visits), but this overlaps substantially with acuity_level
- Age groups show relatively uniform distribution across visit durations (not a primary driver)

### Department Specialization
- Cardiology routine visits average 30.1 minutes (longest non-emergency specialty)
- Dermatology averages 17.0 minutes (shortest specialty)
- Pattern reflects **disease complexity inherent to specialty** rather than a causal department effect

---

## Quantified Duration Drivers

| Factor | Short Visits ≤30 min | Long Visits >30 min | Duration Difference |
|--------|----------------------|-------------------|------------------|
| Emergency Acuity | 4.0% | 96.0% | +19.5 min |
| Emergency Dept | 0.4% | 96.3% | +23.7 min |
| Imaging/Labs Ordered | 37.2% | 66.7% | +6.6 min |
| Specialist Referral | 14.8% | 63.0% | +7.6 min |
| Acute Complexity | 39.9% | 96.3% | +6.9 min |

---

## Important Limitations and Caveats

1. **Data Structure Confounding**: Emergency department visits naturally cluster longer durations due to operational protocols (triage, documentation, monitoring) independent of pure clinical complexity.

2. **Modest Sample Size for Long Visits**: Only 27 visits >30 minutes provide limited statistical power for isolating independent causal effects; many longest visits (45-60 min) represent single cases (n=1).

3. **Reverse Causality Possibility**: Longer visits may sometimes *enable* rather than result from clinical complexity—for example, more time available allows detailed consultation.

4. **Unmeasured Confounders**: Comorbidity burden, patient acuity trajectories during visit, and provider experience are not captured but likely influence duration.

---

## Clinical Conclusions

**The strongest evidence supports that longer visit durations are primarily explained by:**

1. **Emergency-critical acuity level** (41.8 min mean)—life-threatening conditions requiring concurrent diagnostics and intervention
2. **Emergency department context** (45.5 min mean)—operational and safety requirements
3. **Diagnostic workload intensity** (imaging/labs ordered)—adds 6–7 minutes to assessment time
4. **Specialist coordination** (surgical/specialist referral)—consultation and arrangement time

**Causality inference**: Emergency acuity and diagnostic demands are most likely *causal* drivers; department setting may be a consequence rather than cause. Chronic disease management, preventive wellness, and behavioral counseling visits are reliably shorter (~20–21 min), consistent with lower acuity and lower procedural demand.
