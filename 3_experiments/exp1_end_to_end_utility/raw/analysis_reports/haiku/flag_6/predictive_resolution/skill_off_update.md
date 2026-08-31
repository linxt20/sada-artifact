---
dataset: flag_6
scenario: predictive_resolution
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary by agent and issue type?"
source_table: augment_table/flag_6/predictive_resolution/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:21:37.109837+00:00
wall_seconds: 45.47
---

# Resolution Time Analysis by Agent and Issue Type
**Variant:** skill_off | **Dataset:** 500 incidents

## Executive Summary

This analysis examines how incident resolution times vary by assigned agent and issue type using a dataset with 500 service incidents. Among valid cases (436 with positive resolution times), significant performance disparities emerge both across agents and by issue category, suggesting opportunities for targeted operational improvements.

## Key Findings

### Agent Performance Variation

Resolution times vary dramatically by assigned agent, with a **5-fold performance range**:

| Agent | Mean Resolution (hrs) | Median (hrs) | Count | Performance |
|---|---|---|---|---|
| Beth Anglin | 136.3 | 124.0 | 85 | **Best** |
| Charlie Whitherspoon | 150.1 | 150.0 | 89 | ✓ Good |
| Howard Johnson | 158.2 | 139.2 | 89 | ✓ Good |
| Luke Wilson | 159.2 | 150.1 | 91 | ✓ Good |
| Fred Luddy | 698.6 | 631.2 | 82 | **Problematic** |

**Key observation:** Fred Luddy's mean resolution time (698.6 hours) is **4.3-5.1 times longer** than all other agents. This stark differential warrants investigation into potential skill gaps, assignment patterns, or systemic constraints affecting this agent.

### Issue Type Complexity

Different issue categories exhibit varying resolution difficulty:

| Issue Type | Mean Resolution (hrs) | Median (hrs) | Count | Variability |
|---|---|---|---|---|
| Network | 260.3 | 175.8 | 249 | High (σ=313.1) |
| Software | 257.7 | 150.4 | 83 | High (σ=333.1) |
| Database | 242.6 | 140.3 | 93 | High (σ=311.4) |
| Hardware | 185.0 | 147.9 | 11 | Moderate (σ=108.6) |

Network and Software issues take 40% longer on average than Hardware issues. However, **high standard deviations** (ranging from 108–333 hours) indicate inconsistent performance within each category, suggesting factors beyond issue type affect resolution outcomes.

## Agent × Issue Type Cross-Analysis

Performance patterns diverge significantly when examining agent handling by issue type:

### Mean Resolution Time (hours) by Agent and Issue Type

|  | Database | Hardware | Network | Software |
|---|---|---|---|---|
| **Beth Anglin** | 130.9 | 232.9 | 130.4 | 146.4 |
| **Charlie Whitherspoon** | 154.1 | 277.6 | 146.7 | 126.6 |
| **Howard Johnson** | 130.5 | 113.7 | 173.8 | 150.6 |
| **Luke Wilson** | 123.6 | 78.3 | 177.5 | 156.1 |
| **Fred Luddy** | 639.6 | 76.8 | 716.2 | 813.9 |

**Critical insights:**

1. **Fred Luddy's spike:** Takes **639–813 hours** for most issue types (400% above peers), but performs well on Hardware (76.8 hours, tied for fastest). This suggests potential skill specialization rather than general capability issues, or problematic assignment allocation.

2. **Consistent performers:** Beth Anglin and Luke Wilson consistently deliver the shortest times across most issue types—128–177 hours for their core categories.

3. **Software issues:** Highest variance in resolution; Fred Luddy's 813.9 hours contrasts sharply with Charlie Whitherspoon's 126.6 hours.

4. **Volume consideration:** The sample size for Hardware is very small (11 total), limiting confidence in hardware-related conclusions.

## Data Quality Observations

- **Invalid resolution times:** 64 incidents (12.8%) had negative or zero resolution times, excluded from this analysis
- **Data anomalies:** Some incidents show timestamps where closure occurs before opening (negative resolution times), suggesting data entry or system logging errors
- **Outliers:** Maximum resolution time of 1,579 hours (~66 days) for a Software issue suggests either very complex cases or extended hold times not attributable to active resolution

## Interpretation and Context

The "skill_off" variant label suggests this analysis reflects performance **without specialized skill assignment or routing optimizations**. The data shows:

1. **Agent capability gap:** A clear tier of performance exists. Fred Luddy's 5× slowness is the most actionable finding.
2. **Issue complexity:** Network and Software issues inherently consume more time, though execution quality varies.
3. **Inconsistency within type:** High standard deviations within issue categories indicate that factors beyond issue type (agent skill, complexity variance, priority handling) drive outcomes.

## Recommendations for Investigation

1. **Fred Luddy's assignment patterns:** Examine whether this agent receives systematically harder tickets or lacks necessary tools/knowledge for non-Hardware issues.
2. **Best practices capture:** Document methods used by Beth Anglin and Luke Wilson for database/network issues.
3. **Data integrity:** Investigate negative resolution time entries to improve data quality.
4. **Sample expansion:** Gather more Hardware issue data (n=11 insufficient) for reliable cross-agent comparison.

---
**Report basis:** 436 valid incidents (positive resolution times); 64 excluded due to data anomalies
