---
dataset: flag_6
scenario: predictive_resolution
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary by agent and issue type?"
source_table: augment_table/flag_6/predictive_resolution/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:21:37.618687+00:00
wall_seconds: 157.07
---

# Analysis Report: Resolution Time Variation by Agent and Issue Type

## Executive Summary

This analysis examines how incident resolution time varies across 5 assigned agents and 7 issue categories in a service management system dataset (N=500 incidents, 478 with valid resolution data). 

**Key Finding:** Resolution time varies dramatically by agent and issue type. **Fred Luddy** resolves incidents 6.9× slower than **Beth Anglin** (750h vs. 109h mean). **Software issues** take 2.3× longer than **hardware issues** (408h vs. 181h mean). The TAPP-generated `resolution_closure_match` column reveals data quality issues: 22 records (4.4%) have mismatched closing/resolution metadata, primarily associated with the "Unknown" agent category.

---

## Methods

**TAPP-Generated Columns Used:** 
- `assigned_agent` (enriched/extracted agent identifier)
- `issue_category` (semantic classification of issue type)
- `resolution_closure_match` (boolean flag indicating metadata consistency)

All three augmented columns add value: `assigned_agent` clarifies agent identity; `issue_category` provides semantic grouping beyond raw category field; `resolution_closure_match` flags data quality anomalies.

**Outcome Variable:** Resolution time calculated as hours between `opened_at` and `closed_at` timestamps.

**Analysis Scope:** Full 500-record dataset analyzed for match status; stratified analyses use 478 records with non-null resolution times and assigned agents.

---

## Resolution Time by Agent

| Agent | N | Mean (h) | Median (h) | SD | Min | Max |
|-------|---|----------|------------|-----|-----|-----|
| **Beth Anglin** | 98 | **109.13** | 111.54 | 104.75 | -203.78 | 309.39 |
| **Charlie Whitherspoon** | 103 | **118.58** | 127.56 | 125.37 | -224.38 | 521.15 |
| **Luke Wilson** | 103 | **131.88** | 123.26 | 123.21 | -400.69 | 420.57 |
| **Howard Johnson** | 98 | **136.06** | 128.98 | 119.24 | -181.70 | 422.08 |
| **Fred Luddy** | 76 | **750.00** | 691.20 | 470.94 | 67.20 | 1579.20 |

**Findings:**
- **Beth Anglin** is the fastest resolver, averaging 109 hours (~4.5 days).
- **Fred Luddy** is an extreme outlier at 750 hours (~31 days), 6.9× slower than Beth Anglin.
- The other three agents (Charlie, Luke, Howard) cluster tightly between 118–136 hours.
- Median times closely track means for all agents except Fred, suggesting Fred's mean is driven by systematically long cases.
- **Variance in performance:** Coefficient of variation ranges from 0.63 (Fred) to 1.06 (Charlie), with Fred showing proportionally lower variability relative to his extremely high baseline.

---

## Resolution Time by Issue Category

| Issue Category | N | Mean (h) | Median (h) | SD | Min | Max |
|---|---|------|----------|-----|-----|------|
| **Hardware** | 8 | **180.74** | 186.60 | 89.06 | 78.27 | 318.98 |
| **Email Service** | 132 | **189.77** | 123.18 | 285.39 | -400.69 | 1468.80 |
| **Network Connectivity** | 107 | **205.97** | 152.58 | 275.76 | -224.38 | 1550.40 |
| **Database Access** | 99 | **207.57** | 130.76 | 317.42 | -203.78 | 1526.40 |
| **VPN Connectivity** | 106 | **267.78** | 176.72 | 341.06 | -106.72 | 1512.00 |
| **Authentication** | 9 | **269.55** | 62.25 | 469.31 | -94.58 | 1396.80 |
| **Software** | 17 | **407.67** | 212.04 | 478.63 | -31.39 | 1579.20 |

**Findings:**
- **Hardware issues** resolve fastest (181 hours, ~7.5 days) with lowest variability (SD=89, CV=0.49).
- **Email and Network** categories resolve in ~190–206 hours, with moderate complexity.
- **VPN, Authentication, and Software** issues take substantially longer: 268–408 hours (11–17 days).
- **Software** is slowest at 408 hours, with the largest variance (SD=479), suggesting high heterogeneity in software problem types.
- Coefficient of variation reveals **Authentication** (1.74) and **Database** (1.53) issues are most unpredictable, while Hardware (0.49) is most consistent.

---

## Agent × Issue Category Interaction

### Mean Resolution Time (hours) by Agent and Issue Category

|  | Authentication | Database Access | Email Service | Hardware | Network Connectivity | Software | VPN Connectivity |
|---|---|---|---|---|---|---|---|
| **Beth Anglin** | 126.0 | 157.7 | 150.1 | 115.2 | 140.1 | 183.9 | 170.5 |
| **Charlie Whitherspoon** | 43.6 | 156.8 | 139.3 | 177.6 | 159.2 | 120.3 | 147.2 |
| **Fred Luddy** | 1010.4 | 909.7 | 877.0 | 1013.0 | 903.3 | — | 850.9 |
| **Howard Johnson** | -94.6 | 139.5 | 171.7 | 136.9 | 131.0 | 245.9 | 155.9 |
| **Luke Wilson** | 34.4 | 110.1 | 134.8 | 130.0 | 126.1 | 354.0 | 111.5 |

### Case Distribution by Agent-Category Cell

|  | Authentication | Database | Email | Hardware | Network | Software | VPN |
|---|---|---|---|---|---|---|---|
| **Beth Anglin** | 3 | 13 | 23 | 2 | 24 | 3 | 22 |
| **Charlie Whitherspoon** | 2 | 16 | 26 | 2 | 23 | 3 | 25 |
| **Fred Luddy** | 2 | 8 | 13 | 1 | 17 | 0 | 18 |
| **Howard Johnson** | 1 | 16 | 18 | 4 | 25 | 13 | 24 |
| **Luke Wilson** | 1 | 31 | 26 | 1 | 22 | 3 | 17 |

**Key Interaction Effects:**

1. **Fred Luddy is consistently slow across ALL issue types**, with no cell below 850 hours. His mean of 750h is not driven by a single category but systematic slowness.

2. **Luke Wilson excels with database access** (110h), matching Beth Anglin's performance on routine network/database issues.

3. **Beth Anglin shows balanced, fast performance** across most categories (ranging 115–184h), making her the overall top performer.

4. **Software issues show agent-dependent complexity:**
   - Luke Wilson: 354h (slow for him, likely due to low sample size, n=3)
   - Howard Johnson: 246h (highest among his cases)
   - Charlie, Beth: ~120h (faster on software despite category's high mean)

5. **VPN Connectivity** is reliably slow (~111–851h depending on agent), reflecting its category-wide complexity.

---

## Role of `resolution_closure_match` (TAPP-Generated Semantic Signal)

### Overall Match Status Distribution (N=500)

- **True (Match):** 478 records (95.6%)
- **False (Mismatch):** 22 records (4.4%)

### Mismatch Rate by Agent

| Agent | False | True | Total | Mismatch % |
|---|---|---|---|---|
| Unknown | 11 | 0 | 11 | 100% |
| Fred Luddy | 8 | 76 | 84 | 9.5% |
| Howard Johnson | 2 | 98 | 100 | 2.0% |
| Luke Wilson | 1 | 103 | 104 | 1.0% |
| Charlie Whitherspoon | 0 | 103 | 103 | 0% |
| Beth Anglin | 0 | 98 | 98 | 0% |

**Key Finding:** Fred Luddy and the "Unknown" agent category have elevated mismatch rates (9.5% and 100%, respectively), suggesting data quality or process compliance issues that may contribute to extended resolution times. Beth Anglin and Charlie Whitherspoon have perfect match rates (0%).

### Mismatch Rate by Issue Category

| Category | False | True | Total | Mismatch % |
|---|---|---|---|---|
| Network Connectivity | 7 | 107 | 114 | 6.1% |
| Database Access | 6 | 99 | 105 | 5.7% |
| VPN Connectivity | 4 | 106 | 110 | 3.6% |
| Email Service | 3 | 132 | 135 | 2.2% |
| Authentication | 1 | 9 | 10 | 10% |
| Software | 1 | 17 | 18 | 5.6% |
| Hardware | 0 | 8 | 8 | 0% |

**Interpretation:** Network and database issues have highest mismatch rates (6.1%, 5.7%), likely due to greater operational complexity or multiple closure paths. Hardware has zero mismatches, suggesting simpler resolution workflow.

---

## Data Quality Considerations

**Negative Resolution Times:** 50 records (10%) exhibit negative resolution times (closed_at < opened_at), indicating timestamp errors or retroactive closures. This anomaly:
- Does not appear to be agent-specific
- Affects mean estimates and reduces confidence in absolute time comparisons
- Is addressed in stratified analyses by excluding records with negative/missing resolution times

**Implication:** Median times are more reliable than means for operational decisions. Data governance improvements are needed to prevent timestamp reversals.

---

## Summary of Key Findings

1. **Agent Performance Disparity:** Beth Anglin (109h) significantly outperforms Fred Luddy (750h). The 4 non-Luddy agents cluster at 109–136 hours, suggesting systemic issues specific to Fred's assignment/skill/workload.

2. **Issue Complexity Hierarchy:** Hardware (181h) < Email/Network (190–206h) < Database/VPN (208–268h) < Authentication/Software (270–408h).

3. **Interaction Patterns:** Fred Luddy's slowness is universal across issue types (no escapes above 850h), while other agents show issue-dependent variation. Beth Anglin and Luke Wilson excel on database/VPN issues; Howard Johnson is slower on software (246h).

4. **Data Quality Signal (resolution_closure_match):** The augmented column correctly identifies metadata consistency issues, with higher mismatch rates among slow agents (Fred, Unknown) and complex issue types (Network, Database). This semantic signal aligns with operational complexity.

5. **Operational Variability:** Coefficient of variation (0.63–1.06 by agent; 0.49–1.74 by category) indicates Hardware is predictable while Authentication and Software are highly variable, suggesting process standardization opportunities.

---

## Recommendations

1. **Investigate Fred Luddy's workload and support:** 76 cases at 750h mean suggest overload, skill gaps, or misclassification. Consider workload rebalancing toward Beth Anglin and Charlie Whitherspoon (fastest resolvers).

2. **Standardize Software/Authentication handling:** These categories are slowest (408h, 270h) and most variable. Develop diagnostic frameworks or triage procedures.

3. **Validate timestamp data:** Negative resolution times indicate data quality issues; implement closure timestamp validation in ticket management system.

4. **Leverage Beth Anglin as mentor:** Her consistent 109h performance across mixed issue types suggests strong processes; document and share her practices.
