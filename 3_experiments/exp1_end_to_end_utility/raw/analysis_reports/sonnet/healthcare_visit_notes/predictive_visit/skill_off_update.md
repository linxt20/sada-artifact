---
dataset: healthcare_visit_notes
scenario: predictive_visit
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "department"
query: "What visit reasons point to different departments?"
source_table: augment_table/healthcare_visit_notes/predictive_visit/sonnet__skill_off_update.csv
generated_at: 2026-07-28T12:44:04.315783+00:00
wall_seconds: 39.59
---

# Visit Reasons as Predictors of Department

**Dataset:** 250 healthcare visit notes across 6 departments (Cardiology, Dermatology, Emergency, GeneralPractice, Orthopedics, Pediatrics)  
**Focus variable:** `department`  
**Evidence column:** `reason_for_visit` → derived `reason_category`

---

## 1. Reason Categories with Strong Departmental Signal

These categories concentrate most visits in one or two departments, making them reliable predictors:

| Reason Category | Dominant Department | Key Distribution | Dept Count |
|---|---|---|---|
| **Musculoskeletal** | Orthopedics | 12/14 (86%) | 3 |
| **Preventive/Wellness** | Pediatrics + GeneralPractice | 18+5 / 23 (100%) | 2 |
| **Skin/Dermatology** | Dermatology | 18/24 (75%) | 4 |
| **Cardiovascular** | Cardiology | 13/16 (81%) | 3 |
| **Gastrointestinal** | GeneralPractice | 2/3 (67%) | 2 |
| **Neurological** | Emergency | 3/4 (75%) | 2 |
| **Chronic Disease Management** | Cardiology + GeneralPractice | 2+2 / 4 (100%) | 2 |

**Musculoskeletal** is the strongest single-department predictor → Orthopedics.  
**Preventive/Wellness** splits exclusively between Pediatrics (18) and GeneralPractice (5) — age_group further resolves this split (0-17 → Pediatrics, adult → GeneralPractice).  
**Cardiovascular** strongly routes to Cardiology; minority cases in Emergency (likely acute presentations) and Pediatrics (congenital/structural).

---

## 2. Reason Categories Spanning Many Departments (Weak Signal)

These categories appear across all 6 departments and offer little routing power on their own:

| Reason Category | Dept Spread | Notes |
|---|---|---|
| **Follow-Up** | All 6 | n=35; GeneralPractice (15) leads but Cardiology (8) is significant. Secondary signals (urgency, age_group) needed. |
| **Injury/Trauma** | All 6 | Orthopedics (10) and Emergency (4) dominate but Dermatology (4) adds noise. |
| **ENT/Ophthalmology** | All 6 | Pediatrics (6) leads slightly; spread is nearly flat. |
| **Other** | All 6 | Catch-all; n=39, highest count. Dermatology (10) and GeneralPractice (8) are slight leaders. |
| **Respiratory/Infection** | 5 depts | Emergency (9) > GeneralPractice (8) > Pediatrics (6); urgency level disambiguates. |
| **Mental Health** | 5 depts | GeneralPractice (5) > Pediatrics (4) > Emergency (2). |

---

## 3. Prediction Tree Summary

```
reason_category
├── Musculoskeletal           → Orthopedics (strong)
├── Preventive/Wellness       → age_group=0-17 → Pediatrics; adult → GeneralPractice
├── Skin/Dermatology          → Dermatology (strong; minor GP/Peds)
├── Cardiovascular            → Cardiology (strong; urgency=Emergency → Emergency dept)
├── Neurological              → Emergency (small n, treat with caution)
├── Gastrointestinal          → GeneralPractice / Pediatrics (small n)
├── Chronic Disease Mgmt      → Cardiology or GeneralPractice (tie; needs secondary feature)
├── Respiratory/Infection     → urgency=Emergency → Emergency; else GP/Pediatrics
├── Injury/Trauma             → Orthopedics (fractures/sprains); Emergency (acute/severe)
├── Mental Health             → GeneralPractice / Pediatrics / Emergency (spread)
├── Follow-Up                 → GeneralPractice (most common); specialty context needed
└── ENT/Ophthalmology, Other  → low predictive value from reason alone
```

---

## 4. Key Exceptions and Caveats

- **Pediatric** reason category (n=2) is too small to generalize; currently split between Cardiology and Orthopedics — possibly mislabeled or edge cases.
- **Urinary/Renal** (n=5) routes to Cardiology (3), GeneralPractice (1), Orthopedics (1) — the Cardiology and Orthopedics routing is unexpected and may reflect comorbidities or coding variation rather than a true pattern.
- Categories with `reason_category_dept_count = 6` (all departments eligible) confirm that reason alone is insufficient for those categories; **urgency**, **age_group**, and free-text signals from `reason_for_visit` should supplement the tree.
- The augmented columns `BodySystemFocus` and `TriageComplexityLevel` align closely with `reason_category` and can serve as confirmatory features rather than independent predictors.
