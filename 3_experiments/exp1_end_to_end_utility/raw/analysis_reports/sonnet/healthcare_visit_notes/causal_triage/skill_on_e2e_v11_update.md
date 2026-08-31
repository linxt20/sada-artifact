---
dataset: healthcare_visit_notes
scenario: causal_triage
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: what_if
focus_variable: "triage_and_scheduling_efficiency"
query: "How can clinics improve triage and scheduling?"
source_table: augment_table/healthcare_visit_notes/causal_triage/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:22:35.645463+00:00
wall_seconds: 108.45
---

# Clinic Triage and Scheduling Improvement Analysis
**Dataset:** 250 healthcare visit notes across 6 departments  
**Query:** How can clinics improve triage and scheduling?

---

## Method Note

TAPP-generated columns used in this report: `clinical_acuity_level`, `visit_type_category`, `complexity_driver`, `required_diagnostic_workup`, `specialty_routing_signal`, `care_continuity_type`, `in_visit_procedure_performed`, and `pediatric_age_vulnerability`. These were used to provide semantic signal for visit acuity, complexity, and routing patterns that the original structured columns (`urgency`, `department`, `age_group`, `visit_duration_min`) could not fully capture alone.

---

## 1. Dataset Overview

| Original Column | Distribution |
|---|---|
| Department | GeneralPractice (54), Pediatrics (45), Cardiology (42), Dermatology (42), Orthopedics (39), Emergency (28) |
| Urgency | Routine (141, 56%), Urgent (81, 32%), Emergency (28, 11%) |
| Age Group | 60+ (87), 40–59 (60), 18–39 (57), 0–17 (46) |
| Visit Duration | Mean 25.4 min, Median 25 min, Range 15–60 min |

---

## 2. Triage Accuracy: Urgency vs. Clinical Acuity Alignment

The original `urgency` field is broadly consistent with the TAPP `clinical_acuity_level` signal, but reveals important nuances:

| Urgency | life_threatening | urgent_undiff | urgent_known | semi_urgent | routine_preventive |
|---|---|---|---|---|---|
| Emergency | 17 | 4 | 6 | 1 | 0 |
| Urgent | 1 | 5 | 20 | 53 | 2 |
| Routine | 0 | 0 | 3 | 51 | 87 |

**Key finding — semi-urgent overload:** The majority of Urgent-coded visits (53/81, 65%) are tagged `semi_urgent` by `clinical_acuity_level`, and 51/141 Routine visits (36%) are also `semi_urgent`. This means a substantial grey-zone cohort (104 visits, 42% of total) spans the Routine/Urgent boundary and is the primary scheduling challenge.

**Triage mismatches are rare but present:** 2 visits labeled Urgent were tagged `routine_preventive`; 1 Urgent visit was `life_threatening` (likely in a non-ED department). These cases suggest edge-level inconsistency in clinician-assigned urgency.

**Urgent visits outside the ED (n = 81)** are predominantly `semi_urgent` (53) or `urgent_known_condition` (20). These are managed in Pediatrics (21), Orthopedics (17), Dermatology (16), General Practice (15), and Cardiology (12)—departments that would benefit the most from same-day urgent slots.

---

## 3. Visit Duration Drivers and Slot Allocation

Mean visit duration by key stratifiers:

### By Urgency
| Urgency | Mean Duration (min) | n |
|---|---|---|
| Emergency | 45.5 | 28 |
| Urgent | 23.2 | 81 |
| Routine | 22.6 | 141 |

Emergency visits are nearly **2× longer** than other visit types; they require dedicated extended slots.

### By `clinical_acuity_level`
| Acuity Level | Mean (min) | n |
|---|---|---|
| life_threatening | 46.9 | 18 |
| urgent_undifferentiated | 33.9 | 9 |
| urgent_known_condition | 30.2 | 29 |
| routine_preventive | 23.5 | 89 |
| semi_urgent | 21.1 | 105 |

`clinical_acuity_level` is a stronger predictor of duration than the raw `urgency` flag. `urgent_undifferentiated` visits average 33.9 min—longer than `urgent_known_condition`—supporting priority scheduling for patients whose diagnosis is unclear at intake.

### By `required_diagnostic_workup`
| Workup Type | Mean (min) | n |
|---|---|---|
| imaging_and_labs | 39.4 | 17 |
| imaging_ordered | 30.7 | 46 |
| labs_ordered | 23.3 | 30 |
| no_workup | 23.0 | 142 |
| procedure_only | 19.7 | 15 |

Visits requiring both imaging and labs (17 visits, 6.8%) consume on average **39 min**—the highest outside pure emergency cases. Scheduling these into longer slots and pre-ordering workups at intake could reduce same-day bottlenecks.

### By `complexity_driver`
| Complexity Driver | Mean (min) | n |
|---|---|---|
| multi_system_comorbidity | 30.9 | 29 |
| metabolic_endocrine | 28.6 | 11 |
| trauma_injury | 28.5 | 20 |
| single_acute_condition | 26.4 | 111 |
| infectious | 20.7 | 35 |
| developmental_behavioral | 20.6 | 27 |

Multi-system comorbidity visits (mostly Cardiology and General Practice) average 31 min; scheduling a 30-min default slot for this group versus a 20-min slot for `infectious` and `developmental_behavioral` visits would better match capacity to demand.

---

## 4. Visit Type and Care Continuity Patterns

### By `visit_type_category`
| Visit Type | Mean Duration (min) | n |
|---|---|---|
| acute_new_problem | 27.1 | 116 |
| chronic_disease_management | 25.6 | 75 |
| preventive_wellness | 19.9 | 40 |
| post_procedure_follow_up | 24.5 | 10 |

`acute_new_problem` is the **dominant visit type** (116/250, 46%). These visits are disproportionately Urgent-coded (72/81 Urgent visits) and exhibit the highest duration variance, making them the hardest to schedule predictably.

`preventive_wellness` visits (40 total, all Routine) average only 19.9 min and are concentrated in Pediatrics (23) and General Practice (13). These are highly schedulable and represent an opportunity for efficient block scheduling.

### By `care_continuity_type`
| Continuity Type | Mean Duration (min) | n |
|---|---|---|
| new_patient_problem | 27.1 | 132 |
| established_follow_up | 25.3 | 72 |
| protocol_surveillance | 20.0 | 40 |
| post_acute_transition | 23.3 | 6 |

`protocol_surveillance` visits (e.g., chronic disease monitoring) are the most time-efficient (20 min mean) and predictable. These are strong candidates for nurse-led or group visit scheduling to free physician slots.

---

## 5. Specialty Routing and Escalation

### Routing from General Practice
GP generates the most `cross_specialty_referral` signals of any department (7/54 visits, 13%), followed by Dermatology (2) and Orthopedics (2). These referrals add scheduling lag; pre-visit intake screening to identify likely referrals could reduce unnecessary in-person GP contacts.

### Emergency Escalation
23 visits carry a `specialty_routing_signal` of `emergency_escalation`. Of these, 20 originated in the ED itself (already escalated), but **3 escalations came from Pediatrics (2) and Dermatology (1)**—representing unexpected acuity in outpatient settings. These departments should have defined escalation pathways and on-call coverage.

### Surgical Consult Concentration
All 13 surgical consult signals are concentrated in Orthopedics (7) and Emergency (4), with minor presence in Cardiology (2). Orthopedics scheduling should reserve slots for surgical consult follow-ups.

---

## 6. Pediatric Scheduling

`pediatric_age_vulnerability` = True in 46 visits (all age 0–17). Pediatric visits are shorter on average (19.9 min vs. 26.6 min for adults) and predominantly `routine_preventive` (24/46, 52%) or `semi_urgent` (18/46, 39%). No `life_threatening` pediatric cases appear; the 2 pediatric emergency escalations involve `urgent_undifferentiated` presentations. Pediatric slots can be shorter on average, but clinics should maintain rapid-escalation protocols for undifferentiated presentations.

---

## 7. Long-Visit Burden

Only 27 visits (10.8%) exceed 30 minutes. Of these, **26 are Emergency-coded**, and 19/27 require `imaging_ordered` or `imaging_and_labs`. The `single_acute_condition` complexity tag appears in 17/27 long visits—driven by ED trauma and acute presentations rather than chronic complexity. This confirms that extended time is mostly an ED-specific operational issue, not distributed across outpatient departments.

---

## 8. Actionable Recommendations

| Recommendation | Evidence Basis |
|---|---|
| **Introduce acuity-based slot tiers** (20 / 25 / 45 min) | `clinical_acuity_level` means: semi_urgent=21 min, urgent_known=30 min, life_threatening=47 min |
| **Pre-order diagnostics at intake for imaging+labs visits** | `required_diagnostic_workup = imaging_and_labs` → mean 39 min; pre-ordering could compress to 25–30 min |
| **Reserve same-day urgent slots in Pediatrics, Ortho, Derm, GP** | 81 Urgent visits outside ED; 53 semi_urgent with avg 21 min—short slots are feasible |
| **Block-schedule protocol_surveillance and preventive_wellness** | 40+40 visits, both ~20 min mean, high predictability, concentrated in GP and Pediatrics |
| **Flag multi_system_comorbidity for 30-min default slots** | 29 visits, mean 30.9 min; often under-scheduled as Routine |
| **Triage undifferentiated-urgent visits for physician fast-track** | `urgent_undifferentiated` (n=9): longest Urgent subgroup (34 min), highest escalation risk |
| **GP referral screening at intake** | 13% of GP visits generate cross_specialty_referral; pre-visit risk stratification reduces wasted contacts |
| **Pediatric escalation protocol for undifferentiated presentations** | 2 Pediatric emergency escalations; `pediatric_age_vulnerability` + `urgent_undifferentiated` = highest risk subgroup |

---

## 9. Summary

The central scheduling challenge is the **semi-urgent grey zone** (104 visits, 42% of all encounters) spanning the Routine/Urgent boundary, where `clinical_acuity_level` adds precision that raw `urgency` flags miss. Duration is best predicted by the combination of `clinical_acuity_level` and `required_diagnostic_workup`—not by `urgency` alone. Clinics should tier slot lengths by acuity-workup profile, protect same-day slots for `semi_urgent` and `urgent_known_condition` cases in outpatient departments, and use `care_continuity_type` to batch `protocol_surveillance` visits into efficient blocks.
