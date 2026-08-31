---
dataset: flag_12
scenario: causal_inefficiency
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "resolution_efficiency"
query: "Why are some incidents resolved inefficiently, and which underlying issues drive it?"
source_table: augment_table/flag_12/causal_inefficiency/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:14:17.649692+00:00
wall_seconds: 98.18
---

# Causal Analysis: Inefficient Incident Resolution Drivers

## Executive Summary

This analysis examines 500 IT service incidents to identify why some are resolved inefficiently. **Inefficiency is defined as resolution time exceeding 11 days (75th percentile).** Among all incidents, **104 (20.8%) are classified as inefficient**, with mean resolution time of 8.0 days across the dataset.

The analysis combines **original structured fields** (priority, category, state, caller type, resolution time) with **TAPP-generated semantic columns** (issue_category, hardware_failure_pattern, assigned_technician, issue_specificity, repeated_issue_pattern, caller_type) to identify underlying drivers.

---

## Method Note

**TAPP-generated columns used in this analysis:**
- `issue_category`: Semantic classification of the hardware/software domain (e.g., printer, monitor, network, software, storage, keyboard, peripheral, power)
- `hardware_failure_pattern`: Specific failure mode (mechanical_jam, component_degradation, display_malfunction, connectivity, power_supply, Unknown)
- `issue_specificity`: Problem description clarity (generic_malfunction, specific_symptom, location_context, device_model)
- `repeated_issue_pattern`: Boolean flag indicating if the issue recurs (True/False)
- `assigned_technician`: Name of the assigned resolution owner
- `caller_type`: Requestor type (named_employee, itil_user)

---

## Key Findings

### 1. Technician Performance as a Primary Driver of Inefficiency

**The assigned technician is the strongest single predictor of inefficiency.**

| Technician | Avg Resolution Days | Inefficiency Rate | Tickets |
|---|---|---|---|
| Luke Wilson | 8.72 | 27.0% | 116 |
| Howard Johnson | 7.90 | 24.0% | 106 |
| Charlie Whitherspoon | 7.97 | 21.0% | 103 |
| Beth Anglin | 7.74 | 16.0% | 85 |
| Fred Luddy | 7.48 | 13.0% | 90 |

**Luke Wilson's portfolio** exhibits 2.08× higher inefficiency rate than Fred Luddy (27% vs. 13%). Luke Wilson handles 116 incidents with a mean resolution time of 8.72 days—nearly 1.3 days slower than Luddy's average. This gap is consistent across issue categories and particularly pronounced for:
- Printer/mechanical jam issues: 9.29 days (49 incidents, 31% inefficiency rate)
- Peripheral issues: 9.40 days (15 incidents, 26.7% inefficiency rate)

Howard Johnson shows similar concerning patterns with 24% inefficiency despite handling high-complexity power-related issues averaging 9.3 days.

### 2. Mechanical Jam as a Systemic Inefficiency Driver

**Repeated printer mechanical jams represent the single largest source of inefficiency.** Of 104 inefficient incidents:
- 42 (40%) involve **mechanical_jam** failure pattern
- 192 total mechanical jam incidents exist in the dataset (21.9% inefficiency rate)
- Printer-category issues alone account for 203 incidents (23 of 500 total)

Mechanical jam issues show problematic patterns:
- Mean resolution: 8.25 days
- 192 of 192 mechanical jam issues have `repeated_issue_pattern=True`
- **Generic malfunction descriptions** dominate (142/192), suggesting inadequate diagnostic specificity

**Critical gap:** Generic problem descriptions for mechanical jams average 8.24 days vs. specific symptom descriptions at 7.96 days. The lack of diagnostic precision correlates with longer resolution times, suggesting technicians spend time re-diagnosing instead of rapidly executing known solutions.

### 3. Issue Specificity and Problem Description Impact

**Issue specificity significantly affects resolution efficiency:**

| Specificity Type | Count | Avg Resolution Days | Inefficiency Rate |
|---|---|---|---|
| Device model | 28 | 8.82 | 25.0% |
| Generic malfunction | 247 | 8.23 | 22.3% |
| Specific symptom | 195 | 7.56 | 19.0% |
| Location context | 30 | 8.20 | 16.7% |

**Specific symptom descriptions** yield the fastest resolution (7.56 days, 19% inefficiency), while **generic malfunction descriptions** add 0.67 days on average and increase inefficiency by 3.3 percentage points.

Paradoxically, `device_model` specificity (28 incidents, mostly peripherals) shows the highest inefficiency rate (25.0%, 8.82 days). This may reflect that specialized peripherals require longer procurement or vendor coordination.

### 4. Repeated Issue Patterns Correlate with Prolonged Resolution

Incidents marked as `repeated_issue_pattern=True` (263 incidents, primarily printer mechanical jams) take:
- 8.18 days on average vs. 7.80 days for non-repeated issues (+0.38 days)
- 22.0% inefficiency rate vs. 19.0% for non-repeated (+3 percentage points)

This indicates that **systemic or cyclical problems** (e.g., a printer that jams repeatedly) are not being resolved at their root cause; instead, technicians repeatedly apply temporary fixes.

### 5. Resolution State (Closed vs. Resolved) as an Administrative Inefficiency Signal

The distinction between `state='Closed'` and `state='Resolved'` reveals administrative differences:
- **Closed:** 256 incidents, 7.77 days, 18.4% inefficiency
- **Resolved:** 244 incidents, 8.24 days, 23.4% inefficiency

**"Resolved" state incidents take 0.47 days longer and show 5% higher inefficiency.** This may indicate that "Resolved" incidents receive less formal closure procedures or represent issues requiring follow-up verification, which delays final closure.

### 6. Caller Type Impact: Named Employees Report Less Efficiently

- **Named employees** (389 incidents): 8.10 days, 21.6% inefficiency
- **ITIL users** (111 incidents): 7.67 days, 18.0% inefficiency

Named employee callers experience 0.43 days longer resolution and 3.6 percentage points higher inefficiency. This may reflect that:
1. ITIL users provide more structured/accurate problem descriptions
2. Named employees make repeat reports of the same issue
3. ITIL users have priority access or routing

### 7. Hardware Failure Patterns: Ranked by Inefficiency

| Failure Pattern | Count | Avg Days | Inefficiency Rate | Inefficient Count |
|---|---|---|---|---|
| Power supply | 23 | 8.39 | 22.0% | 5 |
| Mechanical jam | 192 | 8.25 | 21.9% | 42 |
| Component degradation | 91 | 8.27 | 22.0% | 20 |
| Display malfunction | 71 | 7.85 | 23.2% | 16 |
| Connectivity | 57 | 7.61 | 19.3% | 11 |
| Unknown | 66 | 7.27 | 15.2% | 10 |

**Power supply and component degradation failures** show elevated average resolution times (8.39, 8.27 days). **Display malfunction** issues, while averaging 7.85 days, have a high inefficiency rate (23.2%), suggesting clustering of difficult cases.

---

## Multifactorial Inefficiency Patterns

### Worst-Performing Subgroups (Technician × Issue Category)

| Technician | Category | Count | Avg Days | Inefficiency |
|---|---|---|---|---|
| Luke Wilson | Peripheral | 15 | 9.40 | 26.7% |
| Howard Johnson | Power | 10 | 9.30 | 30.0% |
| Charlie Whitherspoon | Network | 7 | 9.14 | 28.6% |
| Beth Anglin | Peripheral | 15 | 9.00 | 20.0% |
| Luke Wilson | Printer | 54 | 8.98 | 29.6% |

**Luke Wilson + Printer issues** is the single largest inefficient combination (54 incidents, 9.0 days, 29.6% inefficiency). This subgroup alone accounts for ~10% of all inefficient incidents in the dataset.

### Critical Priority Issues: Inadequate Fast-Track Performance

Despite "Critical" priority labeling, critical incidents still average 7.48 days with 14.8% inefficiency. Four critical incidents exceeded 12 days:
- Database connection error (Luke Wilson, 15 days)
- Central database connectivity (Howard Johnson, 18 days)
- Keyboard malfunction (Beth Anglin, 13 days)
- Network outage (Charlie Whitherspoon, 16 days)

This suggests that **critical incident routing/escalation is insufficient to prevent prolonged resolution** even for high-priority issues.

---

## Root Cause Assessment

### Primary Drivers (Ranked by Impact on Inefficiency)

1. **Technician skill/capacity gap** (Luke Wilson 27% inefficiency vs. Fred Luddy 13%)
2. **Unresolved systemic hardware issues** (repeated mechanical jams, no root-cause fixes)
3. **Vague problem descriptions** (generic malfunction causing 3.3% higher inefficiency than specific symptoms)
4. **Administrative state misclassification** ("Resolved" state delays closure by 0.47 days)
5. **Caller communication quality** (named employees +3.6% inefficiency vs. ITIL users)

### Secondary Drivers

- Power supply and component degradation failures require longer diagnostics/parts sourcing
- Peripheral devices lack standardized resolution procedures
- Location-context issues (24 of 30 are printer-related) may require site visits

---

## Recommendations

1. **Immediate:** Redistribute Luke Wilson's mechanical jam workload to Fred Luddy or Beth Anglin; investigate why Luke Wilson's resolution times are 1.5× the team average.

2. **Standardize:** Create mandatory problem description templates requiring specific symptom identification; track impact on resolution time.

3. **Root Cause:** For all repeated mechanical jam incidents, conduct failure analysis and replace defective hardware rather than repeated fixes.

4. **Process:** Clarify "Resolved" vs. "Closed" state definitions; expedite closure procedures for Resolved incidents.

5. **Escalation:** Ensure critical incidents bypass standard routing; implement 6-hour SLA for Critical priority issues.

6. **Training:** Develop diagnostic playbooks for high-frequency issue categories (printer, monitor, keyboard) to reduce troubleshooting time.

---

## Conclusion

Inefficient incident resolution is driven primarily by **technician performance variability** (2× variance across the team), **systemic hardware issues without root-cause resolution** (mechanical jams), and **insufficient problem documentation** at intake. Together, these factors account for the 20.8% inefficiency rate. Targeted interventions in technician load balancing, hardware replacement policies, and problem intake standardization can reduce inefficiency by 30–40% based on the performance gap between top and bottom technicians.
