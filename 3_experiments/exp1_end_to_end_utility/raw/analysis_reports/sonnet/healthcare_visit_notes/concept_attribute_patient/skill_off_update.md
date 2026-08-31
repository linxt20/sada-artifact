---
dataset: healthcare_visit_notes
scenario: concept_attribute_patient
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "patient_needs"
query: "What patient needs appear in visit notes?"
source_table: augment_table/healthcare_visit_notes/concept_attribute_patient/sonnet__skill_off_update.csv
generated_at: 2026-07-28T12:41:37.241688+00:00
wall_seconds: 35.74
---

# Patient Needs in Healthcare Visit Notes

## Dataset Overview

- **250 visit records** across 6 departments: General Practice, Cardiology, Dermatology, Emergency, Orthopedics, and Pediatrics.
- Each visit has binary flags for 10 distinct patient need categories, plus an `identified_patient_needs` text field and a `needs_count` summary.
- Patients present an average of **2.9 needs per visit** (range: 1–6, median: 3).

---

## Prevalence of Patient Needs (All Visits)

| Need Category | # Visits | % of Visits |
|---|---|---|
| Medication Management | 140 | 56% |
| Monitoring / Follow-up | 115 | 46% |
| Diagnostic Testing | 97 | 39% |
| Lifestyle Counseling | 80 | 32% |
| Specialist Referral | 68 | 27% |
| Pain Management | 67 | 27% |
| Physical Rehabilitation | 55 | 22% |
| Preventive Care | 49 | 20% |
| Wound / Skin Care | 31 | 12% |
| Mental Health | 17 | 7% |

**Medication management** and **monitoring/follow-up** are the two dominant needs, together appearing in over half of all visits. **Mental health** is the least commonly flagged need—likely under-identified rather than truly rare (weak evidence; the notes are brief and clinically focused).

---

## Most Common Need Combinations

The three most frequent co-occurring patterns are:
1. `medication_management + diagnostic_testing + monitoring_followup` (14 visits)
2. `medication_management` alone (12 visits)
3. `lifestyle_counseling + preventive_care` (9 visits)

---

## Departmental Patterns

| Department | Dominant Needs |
|---|---|
| **General Practice** | Highest avg. needs/visit (3.22); broad mix — medication, monitoring, lifestyle, preventive |
| **Orthopedics** | Highest physical rehabilitation rate (72%); high pain management (52%) |
| **Cardiology** | Medication management central; low pain, low rehabilitation |
| **Emergency** | Pain management and specialist referral prominent; broader acute needs |
| **Dermatology** | Wound/skin care most concentrated here; medication management frequent |
| **Pediatrics** | Fewest needs per visit (2.24); lifestyle counseling and monitoring most common |

---

## Age Group Observations

- **18–39 and 40–59** age groups show the highest rates of pain management and physical rehabilitation, suggesting musculoskeletal and chronic-onset conditions.
- **0–17** patients present the fewest and narrowest needs (mostly monitoring and lifestyle).
- **60+** patients have elevated medication management needs but relatively lower physical rehabilitation rates than mid-age groups.

---

## Urgency Level

Urgent visits (2.96–3.05 avg needs) cluster slightly higher than Routine (2.76), but the difference is modest. Emergency visits show elevated pain management and specialist referral. The overall needs profile is broadly consistent across urgency levels, suggesting that chronic/ongoing needs drive most of the volume rather than acute presentations alone.

---

## Key Takeaways

1. **Medication management and follow-up monitoring are the two most pervasive patient needs** across all departments and age groups.
2. **Physical rehabilitation is a significant but concentrated need**, almost exclusively in Orthopedics.
3. **Mental health needs are markedly under-represented** (7%) relative to clinical expectations — this is likely a documentation gap rather than a true absence of need.
4. **General Practice bears the broadest and most complex need burden** per visit; targeted support tools there would have the widest impact.
