---
dataset: healthcare_visit_notes
scenario: predictive_visit
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "department"
query: "What visit reasons point to different departments?"
source_table: augment_table/healthcare_visit_notes/predictive_visit/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:23:31.673939+00:00
wall_seconds: 114.05
---

# Visit Reasons Pointing to Different Departments
**Dataset:** 250 visits × 16 columns (6 original structured + 10 TAPP-generated)  
**Departments:** Cardiology (42), GeneralPractice (54), Pediatrics (45), Dermatology (42), Orthopedics (39), Emergency (28)

---

## Method Note

TAPP-generated columns used in this analysis: `primary_clinical_domain`, `presenting_problem_category`, `body_system`, `visit_acuity_level`, `encounter_type`, `chronic_vs_acute`. These provide semantic classification of free-text `reason_for_visit` narratives and are cross-checked against original structured columns (`department`, `urgency`, `age_group`, `visit_duration_min`).

---

## Key Finding: 11 of 12 Clinical Domains Route to Multiple Departments

Using `primary_clinical_domain` as the semantic proxy for visit reason, only one domain (`pediatric_general`, n=2) is confined to a single department. All other 11 domains appear in at least two departments, with several spanning 3–4 departments.

| primary_clinical_domain | Total n | Departments spanned | Primary dept (n) | Secondary dept(s) |
|---|---|---|---|---|
| cardiovascular | 49 | 4 | Cardiology (42) | Emergency (3), GeneralPractice (3), Pediatrics (1) |
| musculoskeletal_orthopedic | 46 | 3 | Orthopedics (39) | GeneralPractice (5), Emergency (2) |
| preventive_wellness | 36 | 3 | Pediatrics (23) | GeneralPractice (12), Dermatology (1) |
| infectious_disease | 18 | 4 | GeneralPractice (9) | Pediatrics (5), Dermatology (2), Emergency (2) |
| neurological | 14 | 3 | Emergency (6) | Pediatrics (5), GeneralPractice (3) |
| respiratory | 14 | 3 | Emergency (5) / GP (5) | Pediatrics (4) |
| gastrointestinal | 10 | 3 | Emergency (5) | GeneralPractice (3), Pediatrics (2) |
| endocrine_metabolic | 11 | 2 | GeneralPractice (9) | Emergency (2) |
| psychiatric_behavioral | 6 | 3 | Emergency (3) | GeneralPractice (2), Pediatrics (1) |
| dermatology | 40 | 2 | Dermatology (39) | Pediatrics (1) |
| reproductive_womens_health | 4 | 2 | GeneralPractice (3) | Pediatrics (1) |

---

## Department-Routing Drivers Within Shared Domains

Three TAPP-generated facets — `visit_acuity_level`, `chronic_vs_acute`, and `encounter_type` — together with original `urgency` and `visit_duration_min` explain how the same `primary_clinical_domain` routes to different departments.

### Cardiovascular (n=49 across 4 departments)

| Department | n | acuity | chronic_vs_acute | encounter_type | urgency | avg duration |
|---|---|---|---|---|---|---|
| Cardiology | 42 | routine | chronic_stable | scheduled_followup | Routine | 30 min |
| GeneralPractice | 3 | routine | chronic_stable | scheduled_followup | Routine | 22 min |
| Emergency | 3 | life_threatening | acute_new | emergency_triage | Emergency | 50 min |

**Routing logic:** Chronic, stable cardiovascular conditions go to Cardiology (managed follow-up) or GP (shared-care); acute life-threatening presentations (e.g., chest pain, arrhythmia) divert to Emergency. `presenting_problem_category` confirms: Cardiology = 33 chronic disease management + 5 post-procedure follow-up vs Emergency = 3 acute illness.

### Musculoskeletal / Orthopedic (n=46 across 3 departments)

| Department | n | acuity | chronic_vs_acute | encounter_type | urgency | avg duration |
|---|---|---|---|---|---|---|
| Orthopedics | 39 | semi_urgent | acute_new | scheduled_followup | Routine | 26 min |
| GeneralPractice | 5 | semi_urgent | acute_new | acute_unscheduled | Urgent | 23 min |
| Emergency | 2 | urgent_same_day | acute_new | emergency_triage | Emergency | 35 min |

**Routing logic:** The `trauma_injury` sub-category within `presenting_problem_category` almost exclusively routes to Orthopedics (13/14 trauma visits) or Emergency (2/14); chronic/acute non-trauma MSK visits split between GP and Orthopedics depending on access and urgency.

### Respiratory (n=14 across 3 departments)

| Department | n | acuity | chronic_vs_acute | encounter_type | urgency | avg duration |
|---|---|---|---|---|---|---|
| Emergency | 5 | urgent_same_day | acute_new | emergency_triage | Emergency | 47 min |
| GeneralPractice | 5 | routine | chronic_stable | scheduled_followup | Routine | 22 min |
| Pediatrics | 4 | semi_urgent | acute_new | acute_unscheduled | Urgent | 18 min |

**Routing logic:** Severe acute respiratory presentations → Emergency; chronic respiratory management (e.g., COPD, asthma) → GP; pediatric acute respiratory illness (e.g., croup, URI) → Pediatrics. Age (`age_group` = 0–17 exclusively for Pediatrics) is the key additional splitter.

### Infectious Disease (n=18 across 4 departments)

Primarily routed by patient population and body system. Pediatrics (n=5) serves age 0–17 with `body_system` = respiratory/systemic; Dermatology (n=2) handles skin infections (`body_system` = skin_integument); Emergency (n=2) handles severe acute cases; GP (n=9) covers general community infections. `presenting_problem_category` = acute_illness across all sub-groups (n=17/18), so acuity and body system are the differentiators, not visit problem category.

---

## Presenting-Problem Categories Spanning All or Most Departments

`presenting_problem_category` provides a coarser but wide-spanning signal:

| presenting_problem_category | Depts spanned | Cardiology | Dermatology | Emergency | GeneralPractice | Orthopedics | Pediatrics |
|---|---|---|---|---|---|---|---|
| acute_illness | 6 | 3 | 16 | 14 | 13 | 5 | 16 |
| chronic_disease_management | 5 | 33 | 19 | 0 | 17 | 18 | 4 |
| preventive_screening | 4 | 1 | 6 | 0 | 12 | 0 | 24 |
| post_procedure_followup | 4 | 5 | 1 | 0 | 1 | 3 | 0 |
| trauma_injury | 3 | 0 | 0 | 2 | 0 | 13 | 1 |

- **Acute illness** is the most cross-cutting reason, appearing in all 6 departments — routing is then determined by `body_system`, `visit_acuity_level`, and `age_group`.
- **Chronic disease management** skips Emergency entirely; it concentrates in Cardiology (33), Dermatology (19), Orthopedics (18), and GP (17).
- **Preventive screening** is split between Pediatrics (24 well-child visits) and GP (12 adult screens); `encounter_type` = well_visit_preventive confirms this split.
- **Trauma/injury** routes almost entirely to Orthopedics (13/15), with overflow to Emergency for high-acuity cases.

---

## Age as a Structural Department Router

Original column `age_group` cleanly stratifies Pediatrics from adult departments:

| age_group | Cardiology | Dermatology | Emergency | GeneralPractice | Orthopedics | Pediatrics |
|---|---|---|---|---|---|---|
| 0–17 | 0 | 0 | 6 | 0 | 1 | 45 |
| 18–39 | 0 | 17 | 7 | 12 | 11 | 0 |
| 40–59 | 14 | 11 | 8 | 25 | 14 | 0 |
| 60+ | 28 | 14 | 7 | 17 | 13 | 0 |

Age alone nearly fully explains Pediatrics routing. Within adult departments, `primary_clinical_domain` and `visit_acuity_level` are the decisive splitters.

---

## Summary: Department-Routing Decision Framework

```
Visit Reason (reason_for_visit)
    │
    ├─ age_group = 0–17 ──────────────────────────────► Pediatrics
    │
    ├─ primary_clinical_domain = cardiovascular
    │       ├─ chronic_stable / routine ─────────────► Cardiology (or GP for shared care)
    │       └─ acute_new / life_threatening ─────────► Emergency
    │
    ├─ primary_clinical_domain = musculoskeletal
    │       ├─ trauma_injury ───────────────────────► Orthopedics (or Emergency if severe)
    │       └─ acute/chronic non-trauma ─────────────► GP → Orthopedics referral
    │
    ├─ primary_clinical_domain = dermatology ────────► Dermatology
    │
    ├─ primary_clinical_domain = preventive_wellness
    │       ├─ well-child visit ───────────────────► Pediatrics
    │       └─ adult screening ─────────────────────► GeneralPractice
    │
    ├─ presenting_problem_category = acute_illness
    │       └─ visit_acuity_level = urgent/life_threatening ► Emergency
    │
    └─ chronic_disease_management (all adult domains) ► Specialty (Cardiology/Ortho/Derm) or GP
```

**Decision-ready insight:** The visit reasons with the greatest inter-department ambiguity are *cardiovascular acute illness*, *respiratory acute illness*, *neurological presentations*, and *infectious disease* — all of which appear in 3–4 departments. For these, `visit_acuity_level` (routine vs. urgent_same_day vs. life_threatening), `chronic_vs_acute` (chronic_stable vs. acute_new), and `age_group` are the minimum signal required to predict the correct department.
