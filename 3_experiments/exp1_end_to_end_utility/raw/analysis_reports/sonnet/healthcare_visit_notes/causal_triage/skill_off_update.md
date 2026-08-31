---
dataset: healthcare_visit_notes
scenario: causal_triage
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "triage_and_scheduling_efficiency"
query: "How can clinics improve triage and scheduling?"
source_table: augment_table/healthcare_visit_notes/causal_triage/sonnet__skill_off_update.csv
generated_at: 2026-07-28T12:41:01.502928+00:00
wall_seconds: 61.85
---

# Triage & Scheduling Improvement Analysis
**Dataset:** `sonnet__skill_off_update.csv` | 250 visits across 6 departments

---

## Key Finding: Slot Allocation Is Systematically Misaligned

The dataset records `recommended_slot_length_min`, `visit_duration_min`, and `duration_deviation_min` alongside `triage_priority` and `clinical_complexity_score`. Together these expose concrete scheduling inefficiencies.

### 1. Duration Overruns Are Common but Unevenly Distributed

- **46% of visits (115/250)** ran over their allocated slot (positive `duration_deviation_min`).
- Mean overrun across all visits: **+4.1 minutes**; mean overrun *only among over-running visits*: **+8.9 minutes**.
- Emergency department visits show the worst mean deviation (**+20.5 min**), followed by Pediatrics (+4.9 min). Cardiology (+0.1 min) and Orthopedics (+0.9 min) run nearly on time.

### 2. Medium-Priority Visits Are the Scheduling Weak Spot

Counter-intuitively, **Medium-priority visits have the highest mean overrun** among those that ran long (+11.2 min), surpassing High-priority (+5.0 min) and Low-priority (+7.7 min). Medium-priority slots are uniformly set at 30 minutes, but this category is heterogeneous—it mixes mostly **Urgent** cases (60/79) with some Emergency (14/79), which carry higher realized complexity.

> **Action:** Differentiate Medium-priority slots by urgency sub-label (Urgent vs. Emergency origin) rather than using a flat 30-minute default.

### 3. Slot Length Is Tightly Coupled to Clinical Complexity Score

Correlation between `clinical_complexity_score` and `recommended_slot_length_min` is **r = 0.92**, confirming the scoring model drives slot assignment well. However, the correlation with *actual* `duration_deviation_min` is only **r = 0.22**, meaning complexity is captured in the schedule but execution still drifts—pointing to workflow or handoff issues rather than planning errors alone.

### 4. High-Priority Visits Are Under-Scheduled in Terms of Actual Time Used

High-priority visits have a **slot mismatch of −17.1 minutes** (actual duration shorter than recommended slot). This may reflect efficient care protocols, but it also suggests over-allocation of 45-minute High slots, leaving idle capacity while other queues overflow.

> **Action:** Review whether High-priority 45-minute slots can be shortened, freeing buffer time for Medium/Emergency overflow.

### 5. Telehealth Eligibility Aligns with Lower Complexity and Better Adherence

Telehealth-eligible visits have mean complexity **1.0 vs. 3.4** for in-person, and mean duration deviation **+1.5 min vs. +4.7 min**. Routing low-complexity, telehealth-eligible cases (predominantly Routine, Preventive) out of physical queues would reduce in-clinic pressure.

> **Action:** Proactively triage Routine and Preventive visit types (complexity ≤ 2) to telehealth, which make up the majority of Low-priority visits.

### 6. Recommended Slot Lengths Map Cleanly to Priority Tiers — But the Middle Tier Is Too Coarse

| Triage Priority | Recommended Slot | Count | Mean Deviation (over-runners) |
|---|---|---|---|
| Low | 15 min | 150 | +7.7 min |
| Medium | 30 min | 79 | +11.2 min |
| High | 45 min | 21 | +5.0 min |

Low-priority visits also show meaningful overruns (+7.7 min when they run long), likely because 15-minute slots leave no buffer. A 20-minute default for Low-priority with moderate complexity (score 2–3) would reduce cascade delays.

---

## Summary Recommendations

| Issue | Evidence | Recommendation |
|---|---|---|
| Medium-priority heterogeneity | Urgent + Emergency mixed in one 30-min slot tier; highest overruns | Split Medium into Urgent-30 and Urgent-Complex-40 sub-slots |
| Low-priority under-slotted | 15-min slots run over 46% of the time by avg +7.7 min | Increase low-complexity chronic/routine to 20 min |
| High-priority over-slotted | −17 min actual vs. recommended | Trial 35-min High slots; reallocate saved time as flex buffer |
| Telehealth underutilized | Low complexity, lower deviations | Mandatory telehealth routing for complexity ≤ 2, telehealth-eligible |
| Emergency department overflow | +20.5 min mean deviation, highest in dataset | Dedicated flex slots or fast-track pathway for ED triage |

### Caveats
- `duration_deviation_min` has 133/250 zero values — it is unclear whether these are true zero deviations or missing/imputed values; conclusions about over-running visits may undercount the true rate.
- The dataset has only 21 High-priority visits, making estimates for that tier less reliable.
- No wait-time or no-show data is available; scheduling improvements should be validated against those metrics.
