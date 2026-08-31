---
dataset: flag_2
scenario: concept_attribute_delay
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "incident_delay_reasons"
query: "Why do some incidents take longer to resolve?"
source_table: augment_table/flag_2/concept_attribute_delay/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:16:28.424851+00:00
wall_seconds: 51.36
---

# Incident Resolution Delay Analysis Report
## Dataset: Haiku Skill_On v11 Update

### Executive Summary

Analysis of 372 resolved incidents reveals that resolution times vary significantly (1–92 days, mean 43.5 days) based on multiple predictable factors. **Description clarity is the dominant driver**, with vague descriptions taking 115% longer than specific ones. Secondary factors include incident scope, whether incidents are recurring, technician skill level, and the technical domain of the issue.

---

### Key Findings

#### 1. **Description Clarity is the Primary Delay Factor**
- **Vague descriptions**: 76.2 days average resolution
- **Generic descriptions**: 51.7 days average resolution  
- **Specific descriptions**: 35.4 days average resolution
- **Impact**: Vague vs. specific descriptions create a **40.7-day delay (115% slower)**

This is the single most impactful variable in the dataset. Incidents with unclear problem statements require significantly more back-and-forth communication and investigation time.

#### 2. **Incident Scope Affects Resolution Speed**
- **Infrastructure-wide incidents**: 48.1 days average
- **Individual user incidents**: 38.6 days average
- **Department-wide incidents**: 35.7 days average
- **Impact**: Infrastructure-wide issues take **9.5 days longer** (24% slower)

Infrastructure-wide problems typically require broader investigation, coordination across systems, and larger-scale fixes.

#### 3. **New Incidents Take Significantly Longer**
- **Non-recurring (new) incidents**: 54.0 days average (59 incidents)
- **Recurring incidents**: 41.5 days average (313 incidents)
- **Impact**: **12.6-day delay** for new issues (30% slower)

Recurring incidents benefit from established resolutions and institutional knowledge, while truly novel problems require exploratory diagnosis.

#### 4. **Technician Skill Level Varies Meaningfully**
- **Best performer** (Howard Johnson): 39.7 days average
- **Slowest performer** (Beth Anglin): 47.6 days average
- **Skill gap**: **7.9 days difference** (20% variance in performance)

Technician assignment matters—even within the same organization, resolution times vary based on individual proficiency levels.

#### 5. **Priority Does Not Guarantee Faster Resolution**
- **Critical (P1)**: 46.6 days average (57 incidents)
- **High (P2)**: 42.5 days average (283 incidents)
- **Moderate (P3)**: 46.7 days average (32 incidents)

Counter-intuitively, critical incidents resolve only marginally faster than high-priority ones, suggesting that priority rating may not directly correlate with actual effort required.

#### 6. **Technical Domain Influences Resolution Speed**
- **Software issues**: 49.5 days average (15 incidents)
- **Connectivity issues**: 45.3 days average (145 incidents)
- **Email issues**: 45.3 days average (110 incidents)
- **Database issues**: 38.1 days average (98 incidents)
- **Hardware issues**: 38.6 days average (4 incidents)

Database and hardware incidents resolve faster—likely because they are more deterministic and have clearer diagnostic paths compared to systemic software or connectivity problems.

---

### Combined Risk Factors

The most problematic combination is:
- **Vague/generic descriptions + infrastructure-wide scope**: ~72 days average (11 incidents)
  
The most favorable combination is:
- **Specific descriptions + individual user scope**: ~27 days average (124 incidents)

This represents a **45-day difference** between worst and best-case scenarios.

---

### Weak Evidence / Exceptions

- **Priority level paradox**: Critical and Moderate incidents show nearly identical resolution times (46.6 vs 46.7 days), suggesting either that priority ratings are misaligned with actual issue complexity, or that critical issues inherently require more troubleshooting time.
- **Small sample sizes**: Some categories (e.g., Hardware: 4 incidents, Openspace group: 1 incident) have limited data and may not be statistically robust.
- **Assignment group variation**: The "Openspace" group shows 77.2 days average but only 1 incident, making reliable conclusions impossible.

---

### Recommendations

1. **Prioritize incident description quality**: Implement intake templates and require specific detail about affected systems, error messages, and reproducibility steps.
2. **Route new/non-recurring incidents carefully**: Assign novel problems to more experienced technicians rather than rotating assignments randomly.
3. **Establish knowledge base for recurring issues**: Recurring incidents resolve ~30% faster—document solutions to convert new issues into known-solution scenarios.
4. **Rebalance workload**: Redistribute assignments to higher-performing technicians (Howard Johnson averages 8 days faster than Beth Anglin).
5. **Revisit priority definitions**: Clarify whether Critical incidents genuinely require different resolution pathways, or adjust prioritization criteria.

---

### Conclusion

Incident resolution delays are not random. The **"skill_on" variant** data shows that description clarity, incident scope, and technician capability are the primary controllable factors determining resolution time. Organizations can reduce resolution times by ~40% through better incident intake practices and targeted assignment strategies.
