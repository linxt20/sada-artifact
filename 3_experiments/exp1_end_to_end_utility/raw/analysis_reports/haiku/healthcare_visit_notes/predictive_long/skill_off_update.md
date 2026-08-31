---
dataset: healthcare_visit_notes
scenario: predictive_long
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "visit_duration_min"
query: "What visit-note signals suggest a longer visit?"
source_table: augment_table/healthcare_visit_notes/predictive_long/haiku__skill_off_update.csv
generated_at: 2026-07-28T12:43:35.601187+00:00
wall_seconds: 64.29
---

# Visit-Note Signals Suggesting Longer Visits: Analysis Report

**Dataset:** healthcare_visit_notes/predictive_long  
**Variant:** skill_off_update  
**Query:** What visit-note signals suggest a longer visit?  
**Focus Variable:** visit_duration_min  
**Analysis Date:** 2026-07-28

---

## Executive Summary

Visit duration is predominantly driven by **department context, clinical complexity, and procedural requirements**. Visits >25 min (median) show distinct patterns: Emergency Department visits are 80% longer on average, visits with procedures/diagnostics are 10-12% longer, and older patients (60+) spend 16% more time. Multiple conditions and urgent clinical markers further extend visit time.

---

## Key Findings

### 1. **Emergency Department Context** (Strongest Signal)
- **Effect Size:** +80% longer than mean (45.5 min vs. 25.4 min overall)
- **Consistency:** 100% of Emergency visits exceed median duration (25 min)
- **Evidence:** All 28 Emergency Department visits are longer visits; 17/17 visits ≥45 min are Emergency cases
- **Interpretation:** Emergency visits inherently require extended time for triage, stabilization, diagnostic evaluation, and treatment initiation

### 2. **Procedures and Interventions**
- **Duration Impact:** +2.8 min mean difference (27.2 min with procedure vs. 24.4 min without)
- **Prevalence in Longer Visits:** 36% of visits with procedures exceed median
- **Strongest Combination:** Emergency + Procedure = 45.3 min mean (n=16)
- **Note Signal:** Words like "procedure," "biopsy," "injection," "splint," and "cryotherapy" in visit notes correlate with extended time

### 3. **Diagnostic Testing Signals**
- **Duration Impact:** +2.9 min mean difference (26.7 min vs. 23.8 min without diagnostics)
- **Prevalence in Longer Visits:** 39% of diagnostic visits exceed median
- **Content Pattern:** Longer visits are 38% more likely to mention diagnostics ("labs," "imaging," "CT," "MRI," "echo," "biopsy")
- **Note Quality:** The presence of specific diagnostic references (not just note length) matters—correlation between visit duration and note length is weak (-0.106)

### 4. **Urgent Clinical Complexity**
- **Duration Impact:** +6.8 min mean difference (30.8 min for urgent notes vs. 24.0 min routine)
- **Prevalence in Longer Visits:** 52% of urgent-flagged visits exceed median
- **Markers:** Acute symptoms, vital sign abnormalities, immediate diagnostic ordering, and clinical uncertainty flags extend visits
- **Note Indicators:** "Acute," "urgent," "concern for," "immediately," and "stat" appear more frequently in longer visits

### 5. **Multiple Conditions**
- **Duration Impact:** +2.6 min mean difference (26.6 min for 3+ conditions vs. 24.0 min for <3)
- **Prevalence in Longer Visits:** 37% of multi-condition visits exceed median (130/250 visits have 3+ conditions)
- **Distribution:** Visits with 4-6 conditions average 30.8 min (30% longer than single-condition visits)
- **Clinical Reasoning:** Complexity compounds with each additional diagnosis requiring assessment and management planning

### 6. **Specialty Department Effects**
- **Cardiology Baseline:** 30.1 min mean (18% above overall average)
  - Highest-complexity specialty in dataset
  - Follow-up visits still require comprehensive cardiovascular assessment
  - 42/42 Cardiology visits average 30 min
- **Orthopedics:** 25.9 min mean (2% above overall average)
  - Moderate complexity; physical examination is time-intensive
- **Pediatrics:** 19.9 min mean (21% below average)
  - Shorter visits due to simpler presenting issues and faster examination
- **Dermatology:** 17.0 min mean (33% below average)
  - Visual inspection-based; typically straightforward assessment

### 7. **Age Effects**
- **Age 60+:** 29.5 min mean (16% above average)
  - 51% of older visits exceed median
  - Likely reflects polypharmacy review, multiple chronic conditions, and comorbidity complexity
- **Age 0-17 (Pediatrics):** 19.9 min mean (22% below average)
- **Age 40-59:** 25.3 min mean (baseline)
- **Age 18-39:** 23.5 min mean (8% below average)

---

## Note-Content Patterns

Analysis of visit-note text reveals these content signals in longer visits:

| Signal | Longer Visits | Shorter Visits | Lift |
|--------|---------------|----------------|------|
| Diagnostic language | 63.8% | 45.9% | +39% |
| Multiple concerns/conditions | 86.2% | 79.4% | +8% |
| Procedure mentions | 26.2% | 11.2% | +134% |
| Clinical history reference | 11.2% | 3.5% | +220% |
| Complex/complicated language | 10.0% | 7.6% | +32% |

**Interpretation:** Longer visits contain richer clinical detail, more procedure references, and greater discussion of patient history—suggesting deeper evaluation and planning.

---

## Quantified Impact Hierarchy

1. **Emergency Department Status** → +80% duration (strongest)
2. **Urgent Clinical Complexity Flag** → +28% duration
3. **Procedure Presence** → +11% duration
4. **Diagnostic Testing** → +12% duration
5. **Multiple Conditions (3+)** → +11% duration
6. **Age 60+** → +16% duration
7. **Cardiology Specialty** → +18% duration

---

## Weak Evidence / Exceptions

- **Note Length Alone:** Word count shows negligible correlation with visit duration (-0.106). A longer note does not reliably predict longer visits. Clinical content quality matters more than verbosity.
- **Multiple Medications:** Only 6% of dataset has `has_multiple_meds=1`, and mean difference is minimal (+1.1 min). Not a strong predictor in isolation.
- **Follow-up Status:** Presence of follow-up language ("follow-up," "recheck," "annual") appears equally in both longer and shorter visits (~13% each). Routine follow-ups can be quick.

---

## Decision-Ready Insights

**To predict or schedule for longer visits, prioritize:**

1. **Automatically flag Emergency Department visits** for 45-60 min slots (100% longer visits)
2. **Identify Cardiology appointments** for 30 min minimum slots (18% baseline extension)
3. **When procedures are planned**, allocate +3-5 min buffer
4. **Detect urgent clinical language** (acute onset, acute symptoms, "concern for") and extend time
5. **Count documented conditions** — visits with 3+ conditions warrant extended slots
6. **Consider age context:** patients 60+ need ~5 min additional buffer

**Note text features are useful but secondary:** focus on structured fields (department, urgency, condition count, procedure flag) for most reliable prediction.

---

## Limitations

- The dataset contains 250 visit records with median duration of 25 min and range 15-60 min. Effect sizes are moderate; statistical significance beyond descriptive patterns requires formal testing.
- The `skill_off` variant reflects a specific augmentation or evaluation scenario and may not generalize to all healthcare systems.
- Visit notes are brief structured summaries; patterns may differ in verbose clinical note systems.

EOF
