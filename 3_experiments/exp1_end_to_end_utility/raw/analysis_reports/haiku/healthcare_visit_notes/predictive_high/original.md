---
dataset: healthcare_visit_notes
scenario: predictive_high
variant: original
model: substrate-claude-haiku-4-5
query_subtype: predictive_feature_engineering
focus_variable: "urgency"
query: "What visit-note signals suggest high urgency?"
source_table: augment_table/healthcare_visit_notes/predictive_high/original.csv
source_report: dataset_portion_2/substrate-claude-haiku-4-5/healthcare_visit_notes__predictive_high/analyses/original/analysis.md
wall_seconds: 73.01
---

# Healthcare Visit Notes: Signals of High Urgency

## Overview

Analysis of 250 clinical visit notes identifies specific textual signals that distinguish **Urgent** visits (67 cases) from Routine visits (153 cases) and Emergency visits (30 cases). This report examines visit-note patterns associated with urgency classifications in the dataset.

## Key Urgency Signals

### 1. **Acute Onset with Specific Time Markers**

High-urgency notes consistently reference recent symptom onset with precise temporal markers:
- **Recent acute events**: "x3 days," "yesterday," "x1 week," "48 hours"
- **New-onset conditions**: "new-onset palpitations," "new-onset bedwetting," "new tics"
- **Change from baseline**: "worsening exertional angina past 2 weeks," "recent change"

**Evidence**: Urgent cases (V-0002, V-0011, V-0016) emphasize symptom duration in days. Routine visits often lack temporal specificity or reference months-old stable conditions.

### 2. **Fever with Specific Temperature Documentation**

Fever is a strong urgency signal when recorded with specific values:
- **Temperature thresholds**: 38.1°C, 38.2°C, 39°C in urgent notes
- **Associated systemic symptoms**: fever + other findings (cough, throat erythema, ear findings)
- **Pediatric febrile conditions**: fever in infants/children flagged as urgent (V-0012, V-0031, V-0052)

**Pattern**: Routine visits rarely mention fever; urgent visits use specific temperature values combined with clinical findings.

### 3. **Positive Physical Exam Findings with Test Names**

Diagnostic examination maneuvers performed and documented suggest urgency:
- **Orthopedic tests**: McMurray positive (V-0005), Thompson test positive (V-0034), Tinel sign, Phalen sign
- **Abdominal exam findings**: "Tender at McBurney point" (V-0022), "Murphy sign positive" (V-0062)
- **Neurologic signs**: Weakness, sensory changes, abnormal reflexes
- **Local inflammation**: "Erythematous," "swelling," "tenderness over specific anatomic landmarks"

**Evidence**: (V-0022) states "Tender at McBurney point. Concern for appendicitis," directly linking exam findings to urgency. Routine visits note "normal exam" or stable findings.

### 4. **Functional Impairment or Inability to Perform ADLs**

Urgent visits describe loss of normal function:
- **Weight-bearing status**: "Unable to bear weight" (V-0019)
- **Symptom severity limiting activity**: "Locking and giving way" (V-0206), "missing school" (V-0216)
- **Pain severity impact**: "Significant scarring developing" (V-0065), "affecting clothing and social interactions" (V-0239)

**Pattern**: Routine visits mention stable chronic pain; urgent visits describe acute functional loss.

### 5. **Acute Infection Indicators**

Specific infectious disease markers appear in urgent notes:
- **Organism identification**: "Rapid strep positive," "KOH positive," "RPR and HIV testing sent"
- **Purulent findings**: "Tonsillar exudates," "mucopurulent discharge," "Purulent nasal discharge"
- **Inflammatory markers**: "WBC elevated," "pyuria," "positive cultures"
- **Contagious condition awareness**: "Excluded from school," "hand hygiene emphasized"

**Evidence**: (V-0011) "Rapid strep positive" confirms bacterial infection; (V-0012) "TM erythematous and bulging" confirms acute otitis media diagnosis.

### 6. **Specific Abnormal Lab/Imaging Findings**

When labs or imaging are mentioned, urgent notes reference specific abnormal results:
- **Imaging findings named**: "ST elevation in V2-V4," "intertrochanteric femur fracture," "cloudy urine"
- **Elevated counts**: "WBC 14.2" (V-0062), elevated ESR, pyuria on urinalysis
- **Critical values**: Blood glucose 38 mg/dL (hypoglycemia), bilirubin 16.2
- **Equivocal findings requiring follow-up**: "Xray equivocal for scaphoid fracture" (V-0048)

**Pattern**: Emergency notes show more extreme values (ST elevation, GCS 14-15); urgent notes show moderately abnormal findings requiring intervention.

### 7. **Specialist Consultation or Urgent Referral**

Disposition language indicates urgency:
- **Immediate specialist consultation**: "Ortho surgery consulted," "General surgery consulted," "sent to ED for surgical evaluation"
- **Urgent imaging/procedures**: "MRI ordered to rule out..." (suggesting concern for serious condition), "Sent for urgent ortho referral"
- **Same-day or next-visit procedures**: "Steroid injection performed today," "Biopsy performed"
- **Repeat imaging for confirmation**: "Repeat film in 2 weeks" (V-0048)

**Evidence**: (V-0022) states "sent to ED for surgical evaluation" indicating urgency; (V-0206) mentions "urgent ortho referral for arthroscopic repair."

### 8. **Chief Complaint Descriptors Indicating Severity**

Language intensity varies with urgency:
- **Acute pain descriptors**: "Severe," "sharp," "significant" in urgent notes
- **Acute symptom onset phrases**: "Sudden," "acute," "acute exacerbation"
- **Loss of prior control**: "unresponsive to topicals," "failing treatment," "previously controlled, now worsening"

### 9. **Pediatric and Age-Related Red Flags**

Pediatric urgent notes emphasize:
- **Developmental concerns**: Unusual symptoms in specific age groups
- **Dehydration risk**: "Mild dehydration concern" (V-0074)
- **Medication dosing by weight**: Age/size-specific treatment indicates acute pediatric illness
- **School exclusion criteria**: Conditions requiring immediate removal (impetigo, conjunctivitis)

### 10. **Acute Psychiatric and Neurologic Emergencies**

Specific language flags mental health urgency:
- **Suicidal ideation**: "Suicidal ideation and plan" (V-0133)
- **Altered mental status**: "Lethargy," "confusion," "GCS < 15"
- **Neurologic deficits**: "Weakness," "slurred speech," "seizure"

## Weak or Contextual Evidence

**Not reliable urgency signals**:
- Visit duration alone (urgent visits range 15-35 minutes; routine visits also in this range)
- Department type (though Emergency department visits are always emergency-classified)
- Age group alone (urgent visits span all ages)

**Exception**: Absence of concerning features does NOT guarantee routine classification—some routine visits mention significant pathology (e.g., post-operative follow-up, stable chronic disease requiring management).

## Summary of Visit-Note Signal Hierarchy

**Strongest urgency signals** (most specific):
1. New-onset symptoms with specific acute timeline (days, not months)
2. Fever with documented temperature values (≥38°C)
3. Positive diagnostic test results or pathognomonic exam findings
4. Functional impairment (unable to perform basic activities)
5. Acute infection with specific organism or inflammatory evidence

**Moderate urgency signals**:
6. Specialist consultation or urgent referral language
7. Specific abnormal lab/imaging findings requiring intervention
8. Loss of prior treatment control or acute exacerbation

**Contextual signals** (department, age, comorbidity-dependent):
9. Pediatric red flags and age-specific presentations
10. Psychiatric or acute neurologic deficits

## Clinical Decision Relevance

Healthcare providers and triage systems can use these textual patterns to:
- **Triage intake notes**: Flag notes with acute onset + fever + exam findings for higher urgency
- **Risk stratification**: Notes lacking temporal specificity and acute findings suggest routine care
- **Quality assurance**: Ensure urgent diagnoses (appendicitis, fractures, infections) have appropriate documentation of exam findings and lab confirmation
- **Alert logic**: Combine fever (specific temperature) + positive exam findings + acute timeline as a compound urgency indicator

## Data Limitations

- Dataset contains 250 structured visit notes with pre-classified urgency; no external validation against alternative classification systems
- Limited contextual information on why notes were classified as Urgent vs. Routine (outcome-based classification assumed)
- Some urgent visits (e.g., V-0029 acute back strain) involve mild-moderate urgency; true emergency visits are in the separate Emergency category
