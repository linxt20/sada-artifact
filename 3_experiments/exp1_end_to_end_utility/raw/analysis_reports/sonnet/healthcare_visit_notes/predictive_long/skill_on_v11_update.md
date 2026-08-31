---
dataset: healthcare_visit_notes
scenario: predictive_long
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "visit_duration_min"
query: "What visit-note signals suggest a longer visit?"
source_table: augment_table/healthcare_visit_notes/predictive_long/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:22:15.621584+00:00
wall_seconds: 54.37
---

# Visit-Note Signals for Longer Visit Duration

**Dataset:** 250 healthcare visit notes | **Focus variable:** `visit_duration_min`  
**Long-visit threshold:** ≥ 30 min (top quartile; mean = 25.4 min, range 15–60 min)

---

## Key Signals (Ranked by Strength)

### 1. Department — Strongest Discriminator
| Department | Mean Duration (min) | Long-Visit Rate |
|---|---|---|
| Emergency | 45.5 | **100%** |
| Cardiology | 30.1 | **100%** |
| Orthopedics | 25.9 | 23% |
| GeneralPractice | 21.9 | 0% |
| Pediatrics | 19.9 | 2% |
| Dermatology | 17.0 | 0% |

Emergency and Cardiology visits are **always** long in this dataset. Pediatrics and Dermatology visits are essentially never long.

---

### 2. Clinical Severity — Near-Perfect Predictor for Extremes
| Severity | Mean Duration | Long-Visit Rate |
|---|---|---|
| Life-threatening | 47.8 min | 94% |
| High acuity | 32.1 min | 77% |
| Moderate | 23.8 min | 28% |
| Low/stable | 21.7 min | 14% |

A `life_threatening` or `high_acuity` note is a very strong signal. Each step down in severity reduces both mean duration and long-visit rate substantially.

---

### 3. Critical Stabilizing Action Documented
| Action | Mean Duration | Long-Visit Rate |
|---|---|---|
| Resuscitation/ICU-level | 51.4 min | **100%** |
| Emergent procedure/OR | 35.6 min | 89% |
| Monitoring & observation | 33.0 min | 60% |
| Acute treatment in visit | 26.4 min | 38% |
| Not present | 22.9 min | 23% |

Any mention of a critical stabilizing action—especially resuscitation or emergent procedure—is a strong predictor of longer visits.

---

### 4. Urgency Level
| Urgency | Mean Duration | Long-Visit Rate |
|---|---|---|
| Emergency | 45.5 min | **100%** |
| Urgent | 23.2 min | 26% |
| Routine | 22.6 min | 22% |

Emergency-tagged visits are universally long. However, **Urgent vs. Routine urgency shows almost no separation** (26% vs. 22%), making urgency alone a weak signal outside the Emergency category.

---

### 5. Specialist Consult Urgency / Referral
- `emergent_bedside_consult` → mean **45.8–47.0 min**, long-visit rate **100%**
- `urgent_same_day_referral` → modest elevation (~25 min, 33–44%)
- `routine_outpatient_referral` / `not_present` → ~23–25 min, low rates

An emergent bedside consult documented in the note is a definitive signal; routine referrals are not meaningfully predictive.

---

### 6. Imaging / Diagnostics Ordered
| Imaging Type | Mean Duration | Long-Visit Rate |
|---|---|---|
| Advanced imaging (MRI/CT) | 37.8 min | 65% |
| ECG/Holter/Echo | 30.4 min | **96%** |
| Plain X-ray / US | 27.9 min | 50% |
| Point-of-care only | 26.4 min | 14% |
| None | 23.2 min | 20% |

ECG/Holter/Echo orders are almost perfectly correlated with long visits (likely reflecting Cardiology department concentration). Advanced imaging is also a strong signal.

---

### 7. Age Group
| Age Group | Mean Duration | Long-Visit Rate |
|---|---|---|
| 60+ | 29.5 min | 51% |
| 40–59 | 25.3 min | 40% |
| 18–39 | 23.5 min | 19% |
| 0–17 | 19.9 min | 2% |

Older patients trend toward longer visits. Pediatric visits (0–17) are nearly always short—but this likely co-varies with department (Pediatrics).

---

### 8. Visit Type
| Visit Type | Mean Duration | Long-Visit Rate |
|---|---|---|
| Pre-op / clearance | 30.0 min | **100%** |
| New acute problem | 27.0 min | 35% |
| Follow-up chronic | 25.5 min | 43% |
| Preventive / wellness | 20.0 min | 0% |

Preventive/wellness visits are always short; pre-op/clearance visits are always long (small subgroup). Chronic follow-ups slightly outpace new acute problems in long-visit rate.

---

### 9. Medication Change Type
- `multiple_changes` → 30 min mean, **100%** long-visit rate (small subgroup — treat with caution)
- `medication_discontinued` → 26 min, 50%
- `new_medication_started` and `dose_adjusted` are modest elevators

---

### 10. Counseling Topic
- `safety_or_return_precautions` counseling → 33.9 min mean, 63% long-visit rate (suggests higher acuity discharge planning)
- `lifestyle_or_preventive` → 20.3 min, 7% (low acuity confirmatory signal)

---

### 11. Active Problem Count (Weak Signal)
- Mean duration: 1 problem = 22.6 min vs. 2 problems = 26.6 min
- Correlation with duration: **r = 0.21** — statistically positive but modest. Only two values exist in this dataset, limiting power.

---

### 12. Laboratory Test Ordered and Shared Decision-Making (Weak / Negative)
- Lab ordered: 28 min vs. not ordered: 24 min — **modest** effect.
- `shared_decision_making_documented = True` is associated with **shorter** visits (23 min vs. 26 min). This is counterintuitive and may reflect structured wellness visits where SDM is protocol-driven.

---

## Summary Table

| Signal | Strength | Notes |
|---|---|---|
| Department = Emergency or Cardiology | ⬛⬛⬛⬛⬛ Very strong | 100% long-visit rate |
| Clinical severity = life-threatening / high | ⬛⬛⬛⬛⬛ Very strong | 77–94% long-visit rate |
| Critical stabilizing action present | ⬛⬛⬛⬛⬜ Strong | Resuscitation → 100% |
| Emergent bedside consult documented | ⬛⬛⬛⬛⬜ Strong | 100% long-visit rate |
| ECG/Echo/Advanced imaging ordered | ⬛⬛⬛⬛⬜ Strong | 65–96% long-visit rate |
| Urgency = Emergency | ⬛⬛⬛⬜⬜ Moderate | Only Emergency tag; Urgent ≈ Routine |
| Age 60+ | ⬛⬛⬛⬜⬜ Moderate | Likely co-varies with acuity |
| Safety/return-precautions counseling | ⬛⬛⬛⬜⬜ Moderate | High-acuity discharge marker |
| Active problem count | ⬛⬜⬜⬜⬜ Weak | r = 0.21, only two levels |
| Lab test ordered | ⬛⬜⬜⬜⬜ Weak | Small mean difference |
| SDM documented | ⬜⬜⬜⬜⬜ Negative/noise | Inverse association |

---

## Caveats
- **Confounding:** Department is the dominant driver; severity, imaging, and consult signals partly inherit it (e.g., ECG/Echo → Cardiology → always long).
- **Small subgroups:** `pre_op_or_clearance`, `multiple_changes`, and `resuscitation_or_icu_level` each have very few rows — treat 100% rates with caution.
- **Urgency (non-Emergency):** "Urgent" vs. "Routine" labels are nearly indistinguishable in duration, suggesting the label is not reliable for within-outpatient differentiation.
- **Duration ceiling:** Max is 60 min — extreme outliers may not be fully captured.
