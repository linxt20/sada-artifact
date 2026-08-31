---
dataset: healthcare_visit_notes
scenario: focus_inference
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What are the main types of concerns patients come in with in these visit notes?"
source_table: augment_table/healthcare_visit_notes/focus_inference/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:21:40.212605+00:00
wall_seconds: 34.27
---

# Patient Concern Types in Healthcare Visit Notes

## Dataset Overview
- **250 visit records** across departments including General Practice, Cardiology, Pediatrics, Dermatology, and others.
- Key structured columns: `clinical_category`, `chief_complaint_type`, `body_system`, `visit_purpose`, and `condition_chronicity`.

---

## 1. Clinical Categories (Broadest Grouping)

| Clinical Category | Count | % |
|---|---|---|
| Chronic disease management | 88 | 35.2% |
| Acute illness / infection | 71 | 28.4% |
| Preventive & wellness | 38 | 15.2% |
| Injury or trauma | 21 | 8.4% |
| Procedural / surgical | 15 | 6.0% |
| Screening & surveillance | 10 | 4.0% |
| Mental health / behavioral | 6 | 2.4% |
| Medication management | 1 | 0.4% |

**Chronic disease management** and **acute illness/infection** together account for nearly two-thirds of all visits, making them the dominant concern types. Preventive care is a meaningful third category (~15%).

---

## 2. Chief Complaint Type (Symptom-Level Detail)

| Chief Complaint | Count |
|---|---|
| No complaint / asymptomatic | 67 |
| Pain | 64 |
| Skin or wound/lesion | 46 |
| Dyspnea / respiratory | 18 |
| Cardiovascular symptom | 16 |
| Lab result / screening finding | 14 |
| Neurological symptom | 10 |
| Systemic infection / fever | 6 |
| Behavioral / psychiatric | 5 |
| Gastrointestinal symptom | 4 |

- **Pain** is the single most common active complaint (64 visits), spanning musculoskeletal, cardiovascular, and other causes.
- **Asymptomatic / no complaint** visits (67) reflect the large preventive, screening, and stable-chronic-disease cohort.
- **Skin/wound/lesion** concerns (46) are notably prominent, driven by the dermatology and wound-care visits.

---

## 3. Body Systems Involved

Cardiovascular (48), musculoskeletal (46), and dermatologic (45) are the three most represented systems, together accounting for ~56% of visits. Pediatric general, respiratory, neurological, and endocrine/metabolic systems are secondary clusters.

---

## 4. Visit Purpose & Chronicity Context

- **New problems** make up the largest single visit-purpose group (103/250), indicating a high proportion of first-presentation concerns.
- **Follow-up** visits (74) reinforce the chronic disease management theme — patients returning for ongoing conditions.
- Condition chronicity confirms this split: **acute new onset** (100) vs. **chronic stable** (68) vs. **preventive/asymptomatic** (39).

---

## Summary of Main Concern Types

1. **Chronic disease follow-up** (cardiovascular, metabolic, musculoskeletal) — the largest single category, often asymptomatic at visit time.
2. **Acute illness / infection** (pain, fever, respiratory) — nearly as common, often new-onset presentations.
3. **Preventive & wellness** (screenings, physicals, labs) — a clear third tier.
4. **Injury / trauma and procedural needs** — moderate presence (~14% combined).
5. **Mental health / behavioral concerns** — a small but distinct group (6 visits); likely underrepresented relative to real-world burden.

### Caveats
- The `body_system = Unknown` category (13 records) introduces minor uncertainty in system-level counts.
- Mental health visits (n=6) are few enough that conclusions about that category are weak.
- The single `medication_management` record is an outlier and not a reliable category.
