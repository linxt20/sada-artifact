---
dataset: healthcare_visit_notes
scenario: causal_triage
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "triage_and_scheduling_efficiency"
query: "How can clinics improve triage and scheduling?"
source_table: augment_table/healthcare_visit_notes/causal_triage/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:21:55.541801+00:00
wall_seconds: 70.79
---

# Improving Clinic Triage and Scheduling: Evidence from Visit-Note Data

**Dataset:** 250 healthcare visits across 6 departments  
**Focus variables:** `urgency`, `clinical_urgency_signal`, `presentation_acuity_type`, `diagnostic_workup_required`, `referral_or_consult_required`, `follow_up_interval_signal`, `comorbidity_complexity_flag`

---

## 1. Overall Urgency Distribution

| Urgency Tier | Count | % |
|---|---|---|
| Routine | 141 | 56% |
| Urgent | 81 | 32% |
| Emergency | 28 | 11% |

The majority of visits are routine, yet 43% carry an `urgent` or `emergency` tag — indicating the scheduling pipeline must reliably distinguish time-sensitive from deferrable cases.

---

## 2. Key Finding: Urgency Signal–Slot Misalignment

The `clinical_urgency_signal` column provides finer granularity than the three-tier `urgency` label, and reveals two actionable patterns:

### 2a. Semi-urgent cases booked as Routine (n = 49)
Forty-nine visits were assigned a `clinical_urgency_signal` of `semi_urgent` but placed in a **Routine** scheduling slot. These are concentrated in:
- **Dermatology** (18 cases, e.g., actinic keratoses, suspicious lesions)
- **Orthopedics** (17 cases, e.g., disc pathology, recurrent dislocations)
- **Cardiology** (7 cases, e.g., elevated coronary calcium scores)

**Recommendation:** Intake protocols should map `semi_urgent` signals to a distinct "priority routine" queue (e.g., ≤5 business days) rather than standard routine waits, particularly in Dermatology and Orthopedics.

### 2b. Urgent-same-day cases absorbed by non-Emergency departments (n = 23)
Twenty-three visits flagged `urgent_same_day` occurred outside the ED — in Cardiology, Orthopedics, Pediatrics, and Dermatology. Of these, **11 had no documented follow-up interval**, meaning same-day urgency was handled without a structured handoff plan.

**Recommendation:** Non-ED departments need a dedicated same-day urgent access pathway and a mandatory follow-up scheduling trigger at discharge.

---

## 3. Follow-up Scheduling Gaps

Among all non-routine visits, **52 (64% of Urgent, ~18% of Emergency)** had `follow_up_interval_signal = not_present`. Common examples:
- Cardiology paroxysmal AFib (V-0016): same-day urgent, no follow-up scheduled
- Dermatology acute MRSA folliculitis (V-0045): urgent, cultures pending, no return visit set
- Infectious disease cases across Pediatrics and GeneralPractice (multiple)

**Recommendation:** Embed automated follow-up prompts triggered by `urgent_same_day` or `urgent_next_available` signals at note-close, with default intervals matched to chief complaint category (e.g., infectious disease = 48–72 h re-check).

---

## 4. Diagnostic Workup as a Scheduling Complexity Driver

| Workup Type | Total | Urgent | Emergency |
|---|---|---|---|
| `no_workup` | 146 | 54 | 9 |
| `imaging_ordered` | 47 | 16 | 9 |
| `imaging_and_lab` | 14 | 3 | 9 |
| `lab_ordered` | 28 | 5 | 1 |

Emergency visits are disproportionately workup-intensive (`imaging_ordered` or `imaging_and_lab` in 64% of ED cases vs. 26% of urgent cases). Scheduling systems should flag imaging-and-lab combinations at triage to pre-reserve diagnostic slots and avoid visit elongation (Emergency avg: **45.5 min** vs. Routine **22.6 min**).

---

## 5. Comorbidity Complexity and Triage Risk

`high_comorbidity` patients are underrepresented in the Urgent tier (4 cases, 15% of high-comorbidity visits) relative to their clinical risk — 18 high-comorbidity patients were seen in Routine slots. In contrast, 66 `single_condition` patients occupied Urgent slots.

**Recommendation:** Intake questionnaires should capture active comorbidity burden; a comorbidity flag (≥2 active conditions) should auto-elevate scheduling priority even for nominally stable complaints (`chronic_stable_followup`).

---

## 6. Referral Pathways Require Pre-coordination

61 visits (24%) required a referral or consult. The heaviest referral loads are in:
- **Emergency** (17 referrals, mostly emergency and surgical consults)
- **Orthopedics** (17 referrals, mostly surgical and specialist)
- **Cardiology** and **GeneralPractice** (8 each)

Most of these are currently managed reactively at visit time. Pre-visit triage screening using `chief_complaint_category` and `presentation_acuity_type` could anticipate surgical consult likelihood (e.g., trauma + imaging = high probability) and notify downstream teams before the patient arrives.

---

## 7. Acute-on-Chronic: A High-Risk Scheduling Gap

The 12 `acute_on_chronic` presentations were classified as Urgent in 8/12 cases — higher urgency rate than new-acute cases (51%). These patients have existing disease plus an acute deterioration event. Only 4 received same-day access; the remainder were funneled through `urgent_next_available` queues.

**Recommendation:** Add `acute_on_chronic` as an explicit intake category to trigger same-day or 24-h scheduling, distinct from purely new-acute or chronic-stable pathways.

---

## 8. Summary of Actionable Recommendations

| Priority | Action | Supporting Evidence |
|---|---|---|
| **High** | Create "priority routine" tier for `semi_urgent` signals | 49 semi-urgent cases in routine slots; Dermatology, Orthopedics, Cardiology most affected |
| **High** | Mandate follow-up scheduling for all `urgent_same_day`/`urgent_next_available` visits | 52 non-routine visits with no follow-up signal |
| **High** | Pre-reserve imaging/lab for Emergency and complex Urgent visits | Imaging + labs in 64% of ED cases; avg duration 45.5 min vs. 22.6 min |
| **Medium** | Incorporate comorbidity screening at intake | 18 high-comorbidity patients in routine slots |
| **Medium** | Anticipate referral needs from chief complaint and acuity type | 61 reactive referrals across departments |
| **Medium** | Recognize `acute_on_chronic` as a same-day/24-h category | 8/12 acute-on-chronic cases ultimately urgent; currently under-triaged |

---

## Caveats and Weak Evidence

- **Visit duration** differences (Routine ~23 min vs. Emergency ~46 min) are meaningful but may partly reflect documentation practices rather than true workload.
- The 52 non-routine visits with `follow_up_interval_signal = not_present` may include cases where follow-up was arranged verbally or through other channels not captured in these notes.
- The dataset contains 250 visits; department-level subgroup counts (e.g., 7 Cardiology semi-urgent cases) are small and should be validated against larger operational data before protocol changes.
