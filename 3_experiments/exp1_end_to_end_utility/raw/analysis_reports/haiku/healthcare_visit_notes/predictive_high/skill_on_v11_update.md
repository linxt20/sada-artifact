---
dataset: healthcare_visit_notes
scenario: predictive_high
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "urgency"
query: "What visit-note signals suggest high urgency?"
source_table: augment_table/healthcare_visit_notes/predictive_high/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:22:34.770514+00:00
wall_seconds: 83.24
---

# Visit-Note Signals for High Urgency: Analysis Report

## Executive Summary

This analysis identifies the key signals in healthcare visit notes that predict high urgency (Emergency and Urgent designations). Across 250 visit records, we identify five distinct signal categories that strongly correlate with urgency classification. **Emergency visits (n=28, 11%)** are characterized by immediate threat signals, while **Urgent visits (n=81, 32%)** show varied but distinct patterns from Routine visits (n=141, 56%).

## Key Urgency Signals

### 1. **Acute Symptom Timeline** — Critical Differentiator

The symptom onset timeline is the strongest single predictor of urgency:

| Timeline | Emergency | Urgent | Routine |
|----------|-----------|--------|---------|
| Minutes-to-hours onset | 12 (43%) | 5 (6%) | 0 (0%) |
| Hours-to-one day | 1 (4%) | 19 (23%) | 0 (0%) |
| One-to-three days | 0 (0%) | 7 (9%) | 0 (0%) |
| Three-plus days | 0 (0%) | 10 (12%) | 8 (6%) |
| Not specified | 15 (53%) | 40 (50%) | 133 (94%) |

**Finding**: 43% of Emergency visits involve symptom onset within minutes-to-hours. In contrast, 94% of Routine visits show "not_specified" timeline (predominantly preventive or chronic follow-up). Urgent visits cluster in the hours-to-one-day window (23%), suggesting acute but not immediately life-threatening presentations.

### 2. **Clinical Intervention Triggers** — Escalation Markers

The presence and type of diagnostic or therapeutic triggers strongly indicate urgency:

**Emergency visits** (most common triggers):
- Protocol/alert activation (39%): STEMI protocols, stroke alerts, trauma team activation
- Transfer to higher acuity (29%): ICU admission, specialized acute care needed
- Procedural interventions (14%): Emergency procedures, imaging-guided interventions

**Urgent visits** (mixed triggers):
- Procedural intervention same visit (26%): Minor office procedures, biopsies, injections
- Lab findings critical (19%): Positive rapid tests, confirmatory labs
- No specific trigger present (28%): Clinical judgment sufficient

**Routine visits**:
- No trigger present (52%): Standard follow-up or preventive care
- Procedural interventions (24%): Elective procedures, routine counseling

**Finding**: Emergency visits show protocol activation and system-level escalation signals absent from Routine visits. Urgent visits show intermediate complexity with procedural or critical lab findings requiring same-visit action.

### 3. **Treatment Intensity and Escalation** — Response Level Indicator

Treatment patterns reflect urgency classification:

| Treatment Escalation | Emergency | Urgent | Routine |
|----------------------|-----------|--------|---------|
| Hospitalization/ICU admission | 15 (54%) | 1 (1%) | 0 (0%) |
| IV medications/fluids emergent | 6 (21%) | 0 (0%) | 0 (0%) |
| Medication escalation/change | 4 (14%) | 36 (44%) | 36 (26%) |
| Routine care/monitoring | 2 (7%) | 21 (26%) | 80 (57%) |
| Multiple specialist consults (acute) | 1 (4%) | 14 (17%) | 19 (13%) |

**Finding**: 75% of Emergency visits require hospitalization or emergent IV support. Urgent visits predominantly involve medication changes (44%) and multiple specialist consults (17%), while Routine visits emphasize monitoring and continuity (57%).

### 4. **Department and Visit Disposition** — Contextual Urgency

Urgency clustering by department:

**Emergency Department** accounts for:
- All (27/28, 96%) Emergency visits
- Zero Urgent/Routine visits routed there

**High-Urgency Departments** (Urgent concentration):
- Pediatrics (21 Urgent): Acute infections (URI, otitis media), rashes, breathing issues
- General Practice (13 Urgent): Acute infections, injuries, acute pain
- Dermatology (13 Urgent): Suspicious lesions, infections, immunological conditions
- Cardiology (11 Urgent): New-onset arrhythmias, worsening symptoms, syncope

**Routine-Heavy Departments**:
- Cardiology (30 Routine): Stable follow-ups, device checks
- Dermatology (26 Routine): Cosmetic/chronic conditions, maintenance

**Finding**: Emergency cases concentrate entirely in the ED, while Urgent cases scatter across multiple departments, requiring clinical judgment at point-of-care.

### 5. **Specific Clinical Patterns in Visit Notes** — Content Signals

Content analysis of the `reason_for_visit` field reveals distinct linguistic and clinical markers:

**Emergency Visit Markers** (Examples: V-0008, V-0028, V-0070):
- Acute, severe symptoms with vital sign abnormalities (e.g., "Severe substernal chest pain radiating to left arm, diaphoretic, BP 156/94")
- Time-stamped acute onsets (e.g., "onset 1 hour ago", "45 minutes ago")
- Diagnostic urgency indicators (e.g., "ST elevation on ECG", "subarachnoid hemorrhage on CT")
- Immediate intervention language (e.g., "protocol activated", "tPA candidate", "cath lab notified")
- System-level responses (e.g., "Trauma team evaluating", "Neurosurgery consulted")

**Urgent Visit Markers** (Examples: V-0002, V-0005, V-0011):
- Recent symptom onset (e.g., "x3 days", "yesterday", "x2 days")
- Positive objective findings (e.g., "Rapid strep positive", "McMurray positive", "TM erythematous and bulging")
- Need for same-visit intervention (e.g., "MRI ordered", "Biopsy performed", "Started antibiotics")
- Moderate symptom intensity (e.g., "low-grade fever", "swelling and tenderness", "tonsillar exudates")
- Single system focus with clear etiology

**Routine Visit Markers** (Examples: V-0001, V-0003, V-0006):
- Preventive or maintenance language (e.g., "Annual physical exam", "Follow-up after MI 6 months ago", "Well-child visit")
- Absence of acute symptom descriptors
- Stable objective findings or improvements (e.g., "BP well-controlled", "no angina", "tolerating well")
- Chronic disease management focus
- Preventive counseling and standard testing

## Quantitative Signal Strength

Cross-tabulation of key signals with urgency classification reveals:

**Most Specific for Emergency (Lift > 10x from baseline):**
1. Minutes-to-hours symptom onset: 43% of Emergency vs. 0% of Routine (43x lift)
2. Protocol/alert activation: 39% of Emergency vs. 0% of Routine (∞ lift)
3. Hospitalization/ICU treatment: 54% of Emergency vs. 0% of Routine (∞ lift)
4. Emergency Department disposition: 96% of Emergency vs. 0% of Routine (∞ lift)

**Most Specific for Urgent (Lift 2-4x):**
1. Hours-to-one-day symptom onset: 23% of Urgent vs. 0% of Routine (∞ lift)
2. Procedural intervention same visit: 26% of Urgent vs. 24% of Routine (1.1x, weak)
3. Critical lab findings trigger: 19% of Urgent vs. 0% of Routine (∞ lift)

**Weaknesses and Edge Cases:**
- Overlapping triggers: 28% of Urgent visits show "not_present" for intervention triggers, requiring clinical judgment from visit note text
- Routine follow-ups with acute issues: 30 Routine visits are in Cardiology "with_acute_issue" disposition, suggesting secondary complexity
- Timeline ambiguity: 50% of Urgent and 94% of Routine visits show "not_specified" timeline, forcing reliance on clinical descriptors

## Conclusion

High urgency in visit notes is signaled by a **hierarchical combination** of factors:

1. **Immediate threat signals** (Emergency): Symptom onset < 1 hour + vital abnormalities + protocol activation → Hospitalization/ICU
2. **Acute illness requiring prompt intervention** (Urgent): Symptom onset < 3 days + objective positive findings + same-visit procedure/labs → Medication or specialist escalation
3. **Stable/preventive** (Routine): No specified onset (preventive context) + stable findings + monitoring or education focus

The evidence is strongest for **Emergency classification** (protocol/alert activation, hospitalization, ED disposition are quasi-deterministic), and most challenging for **Urgent classification** (heterogeneous presentations require integration of onset timing, objective findings, and intervention triggers). Visit-note content analysis is essential for cases where structured fields are indeterminate.

**Practical application**: Triage systems should prioritize (1) acute symptom timeline, (2) vital sign abnormalities and alert language in the text, and (3) type of intervention trigger (protocol vs. routine) as the primary decision tree for urgency classification.
