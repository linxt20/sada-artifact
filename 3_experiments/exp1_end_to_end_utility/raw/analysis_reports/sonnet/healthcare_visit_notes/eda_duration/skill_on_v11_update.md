---
dataset: healthcare_visit_notes
scenario: eda_duration
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "visit_duration_min"
query: "How do reasons for visit relate to urgency and visit duration across department and age group?"
source_table: augment_table/healthcare_visit_notes/eda_duration/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:21:51.795844+00:00
wall_seconds: 49.98
---

# Reasons for Visit, Urgency, and Visit Duration — Healthcare Visit Notes EDA

**Dataset:** 250 visits across 6 departments | Focus variable: `visit_duration_min` (15–60 min, mean 25.4 min)

---

## 1. Urgency Level Drives the Largest Duration Differences

| Urgency | Mean Duration (min) | Median | N |
|---|---|---|---|
| Emergency | 45.5 | 45.0 | 28 |
| Urgent | 23.2 | 20.0 | 81 |
| Routine | 22.6 | 20.0 | 141 |

Emergency visits are roughly **twice as long** as Routine or Urgent visits. Notably, Urgent and Routine visits are nearly indistinguishable in duration (difference < 1 min), suggesting urgency level alone does not differentiate non-emergency complexity in this dataset.

---

## 2. Reason for Visit (Complaint Category) Shapes Duration Independently

| Complaint Category | Mean Duration (min) | N |
|---|---|---|
| trauma_injury | 33.8 | 8 |
| gastrointestinal | 32.8 | 9 |
| cardiovascular | 30.6 | 49 |
| neurologic | 30.5 | 11 |
| respiratory | 29.2 | 13 |
| musculoskeletal | 25.5 | 40 |
| preventive_wellness | 20.1 | 36 |
| **dermatologic** | **17.3** | **43** |

- **High-acuity complaint categories** (trauma, GI, cardiovascular, neurologic, respiratory) consistently show longer visits.
- **Dermatologic** visits are the shortest (17.3 min), well below the overall mean — consistent with their near-exclusive Routine classification and procedurally simple workup.
- **Preventive/wellness** visits cluster around 20 min despite being Routine, reflecting structured but time-bounded annual exams.

---

## 3. Department Determines Visit Profile More Than Urgency Label

| Department | Mean Duration (min) | Dominant Urgency | Key Complaint Categories |
|---|---|---|---|
| Emergency | 45.5 | Emergency (100%) | trauma, GI, respiratory, neurologic |
| Cardiology | 30.1 | Routine (71%) | cardiovascular |
| Orthopedics | 25.9 | Routine/Urgent split | musculoskeletal |
| GeneralPractice | 21.9 | Routine (72%) | preventive_wellness, mixed |
| Pediatrics | 19.9 | Routine (53%) | respiratory, infectious |
| Dermatology | 17.0 | Routine (62%) | dermatologic |

**Cardiology** stands out: despite being mostly Routine, its mean duration (30.1 min) rivals Orthopedics' Urgent visits. This is driven by cardiovascular follow-up complexity and diagnostic workup (labs + imaging), not urgency classification. Dermatology's short visits persist even among Urgent-classified patients (20.0 min vs. 15.2 min Routine — only a 5 min gap).

---

## 4. Age Group Moderates Duration — Most Prominently in Emergencies

| Age Group | Emergency Mean (min) | Routine Mean (min) | Urgent Mean (min) |
|---|---|---|---|
| 0–17 | — (no Emergency visits) | 20.6 | 19.1 |
| 18–39 | 38.2 | 19.0 | 21.8 |
| 40–59 | 44.0 | 22.8 | 25.6 |
| 60+ | **52.9** | 25.5 | 26.2 |

Age has a **clear monotonic relationship with duration**, especially in Emergency visits: patients aged 60+ average nearly 53 minutes vs. 38 minutes for 18–39 year-olds. In Routine visits, the age gradient is smaller but consistent (19 → 25.5 min from youngest to oldest adults). Pediatric patients (0–17) have no Emergency visits in this sample, limiting cross-age Emergency comparisons.

The 60+ cohort is also the largest group (87 visits, 35%) and skews toward cardiovascular and endocrine complaints — inherently longer-duration categories.

---

## 5. Urgency × Complaint Category: Clear Structural Patterns

- **Preventive/wellness** visits are almost exclusively Routine (35/36), averaging 20 min — a tightly defined category.
- **Trauma and GI** complaints concentrate in Emergency (4/8 and 4/9 respectively), pulling those categories' durations up.
- **Infectious disease** complaints are mostly Urgent (7/10), yet average only 26.5 min — shorter than cardiovascular Routine visits, indicating that diagnosis type matters more than urgency flag.
- **Musculoskeletal** visits split nearly evenly between Routine and Urgent with a modest duration difference (24.8 vs. 27.4 min), suggesting mild complexity variation by urgency within this category.

---

## Key Takeaways

1. **Urgency level** is the strongest single predictor of duration, but only because Emergency visits are structurally different (all in the Emergency department, high-acuity complaints). Among non-emergency levels, urgency adds little discriminatory power.
2. **Complaint category** is a strong secondary predictor — cardiovascular and neurologic reasons drive long visits regardless of urgency; dermatologic reasons consistently drive short visits.
3. **Department** largely encodes the complaint × urgency combination: Cardiology's Routine cardiovascular follow-ups are as long as most Urgent visits elsewhere.
4. **Older age groups** (especially 60+) consistently extend visits, most dramatically in emergencies, likely reflecting multimorbidity and greater diagnostic workup intensity.
5. **Caveats:** Small Emergency cell sizes for some age/complaint combinations (n < 5) limit confidence in those subgroup estimates. The Routine vs. Urgent duration overlap warrants caution in treating urgency as a continuous severity signal outside of Emergency classification.
