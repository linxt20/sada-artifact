---
dataset: healthcare_visit_notes
scenario: eda_duration
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: exploratory_data_analysis
focus_variable: "visit_duration_min"
query: "How do reasons for visit relate to urgency and visit duration across department and age group?"
source_table: augment_table/healthcare_visit_notes/eda_duration/original.csv
generated_at: 2026-07-26T13:49:53.343904+00:00
wall_seconds: 113.24
---

# Healthcare Visit Notes: Reasons for Visit, Urgency, and Duration Across Department and Age Group

## Dataset Overview

- **250 visits** across 6 departments, 3 urgency levels, and 4 age groups.
- Focus variable: **`visit_duration_min`** (range: 15–60 min; mean: 25.4 min).
- Visit reasons are free-text notes; urgency and department are categorical.

---

## 1. Urgency Level and Visit Duration

| Urgency | Count | Mean Duration (min) | Median |
|-----------|-------|---------------------|--------|
| Emergency | 28 | **45.5** | 45 |
| Urgent | 81 | 23.2 | 20 |
| Routine | 141 | 22.6 | 20 |

**Emergency visits are dramatically longer** (~2× urgent/routine). Urgent and Routine visits are nearly indistinguishable in duration (median both 20 min), suggesting that within non-emergency contexts, urgency alone does not meaningfully predict visit length.

---

## 2. Reason for Visit Patterns by Urgency

Text content of visit notes aligns well with urgency labels:

- **Emergency**: Acute, life-threatening presentations — chest pain with ST-elevation, MVA with possible LOC, stroke alerts. These drive the extended duration.
- **Urgent**: Sub-acute complaints — fever/cough (viral URI), acute musculoskeletal injuries, suspicious skin lesions. These are addressed efficiently despite higher acuity.
- **Routine**: Preventive care ("annual physical", n=27) and chronic disease management ("follow-up", n=31). These dominate the dataset (141 visits, 56%) and anchor the lower end of duration.

---

## 3. Duration and Urgency by Department

| Department | Count | Mean Duration (min) | Urgency Mix |
|----------------|-------|---------------------|------------------------|
| Emergency | 28 | **45.5** | 100% Emergency |
| Cardiology | 42 | **30.1** | 71% Routine, 29% Urgent |
| Orthopedics | 39 | 25.9 | 56% Routine, 44% Urgent |
| GeneralPractice| 54 | 21.9 | 72% Routine, 28% Urgent |
| Pediatrics | 45 | 19.9 | 53% Routine, 47% Urgent |
| Dermatology | 42 | **17.0** | 62% Routine, 38% Urgent |

Key observations:
- **Emergency** is a department, not just a label here — all 28 emergency-urgency visits route there; no other department sees Emergency-level visits.
- **Cardiology** has the longest non-emergency duration (30.1 min), consistent with complex chronic disease follow-ups (post-MI, heart failure, EF monitoring). Urgency mix has minimal effect: Routine (30.0 min) ≈ Urgent (30.4 min).
- **Dermatology** is the shortest department (17.0 min), even though 38% of visits are Urgent. Urgent dermatology visits (suspicious lesions) average 20 min vs. 15.2 min for Routine — a small but real difference.
- **Pediatrics** urgent visits are slightly *shorter* than routine (19.0 vs. 20.6 min), possibly reflecting fast viral illness assessments.

---

## 4. Duration and Urgency by Age Group

| Age Group | Mean Duration (min) | Emergency | Urgent | Routine |
|-----------|---------------------|-----------|--------|---------|
| 0–17 | 19.9 | 0 | 22 | 24 |
| 18–39 | 23.5 | 38.2 | 21.8 | 19.0 |
| 40–59 | 25.3 | 44.0 | 25.6 | 22.8 |
| 60+ | **29.5** | **52.9** | 26.2 | 25.5 |

- **Duration increases steadily with age** across all urgency categories.
- The 60+ group has the highest mean duration in every urgency band. Emergency visits for 60+ average **52.9 min** vs. 38.2 min for 18–39, likely reflecting greater complexity and comorbidities (e.g., stroke workup, cardiac events).
- **Children (0–17) have zero Emergency visits** in this dataset — all urgent pediatric cases were classified as Urgent, not Emergency. This limits cross-group Emergency comparisons.
- Within Routine visits, duration for 60+ (25.5 min) is notably higher than for 18–39 (19.0 min), consistent with more chronic conditions requiring more time.

---

## 5. Interaction: Department × Age Group

- **Cardiology** skews heavily toward 60+ (per clinical norms), explaining its high mean duration.
- **Pediatrics** is exclusively 0–17, with shorter visit durations and no Emergency-class visits.
- **GeneralPractice** spans all ages; higher older-adult volume pulls its mean slightly upward.

---

## 6. Exceptions and Weak Evidence

- The Emergency urgency–department boundary is **perfectly confounded**: all Emergency-urgency visits are in the Emergency department. It is impossible to separate department effect from urgency effect for this level.
- Urgent vs. Routine duration difference is **negligible** (0.6 min mean), raising questions about whether this distinction is clinically meaningful for scheduling in non-emergency settings.
- Sample size for Emergency visits (n=28) is small; age-group means within Emergency (especially 18–39, n=11; 40–59, n=5) should be interpreted cautiously.
- Reasons for visit are free-text notes, not coded diagnoses; keyword analysis is illustrative, not exhaustive.

---

## Summary

| Driver | Effect on Duration |
|--------|-------------------|
| Emergency urgency | Strong positive (+20 min vs. routine) |
| Cardiology department | Moderate positive (+7.5 min vs. GP) |
| Older age (60+) | Moderate positive (+5–10 min across all urgency levels) |
| Urgent vs. Routine | Negligible in non-emergency settings |
| Pediatric/Dermatology | Negative (shorter visits, simpler presentations) |

The **primary determinants of longer visit duration are Emergency-level presentations and older patient age**, with department (Cardiology) serving as a proxy for condition complexity. Urgency level (Urgent vs. Routine) by itself contributes minimally to duration differences outside the Emergency context.
