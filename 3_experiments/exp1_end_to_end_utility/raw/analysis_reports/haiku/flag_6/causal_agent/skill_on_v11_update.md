---
dataset: flag_6
scenario: causal_agent
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "agent_resolution_discrepancy"
query: "Why do some agents have longer resolution times?"
source_table: augment_table/flag_6/causal_agent/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:19:22.917268+00:00
wall_seconds: 58.93
---

# Analysis: Why Some Agents Have Longer Resolution Times

## Executive Summary

A significant disparity exists in incident resolution times across agents, driven primarily by **individual agent performance** rather than incident characteristics. Fred Luddy's cases resolve in approximately **750 hours (31 days) on average**, compared to 136–160 hours for other agents—a **4.94× difference**. While incident complexity and severity show minor correlations with resolution time, the agent assigned to handle an incident is the strongest predictor of how long resolution will take.

---

## Key Findings

### 1. **Agent Performance Disparity is Dramatic**

| Agent | Cases | Mean Resolution | Median | Days |
|-------|-------|-----------------|--------|------|
| Fred Luddy | 76 | 750.0 hours | 691.2 | 31.3 |
| Luke Wilson | 90 | 160.2 hours | 151.3 | 6.7 |
| Howard Johnson | 88 | 159.6 hours | 142.8 | 6.7 |
| Charlie Whitherspoon | 89 | 150.1 hours | 150.0 | 6.3 |
| Beth Anglin | 85 | 136.3 hours | 124.0 | 5.7 |

**Interpretation:** Fred Luddy's mean resolution time is roughly **5 times longer** than Beth Anglin's (the fastest), and about **4.7 times longer** than the average of other agents (157.7 hours).

### 2. **Long-Running Cases Concentrate with One Agent**

Among the 48 incidents requiring over 500 hours to resolve:
- **47 cases (97.9%)** were assigned to Fred Luddy
- **1 case** was assigned to Charlie Whitherspoon

This extreme concentration strongly suggests **individual capacity or skill factors** rather than random variation.

### 3. **Issue Complexity Shows Counterintuitive Pattern**

Contrary to expectation, high-complexity issues resolve *faster* than low-complexity ones:
- **High complexity:** 188.4 hours (median: 229.4)
- **Medium complexity:** 295.4 hours (median: 159.8)
- **Low complexity:** 253.9 hours (median: 171.6)

This suggests that high-complexity incidents may receive more immediate attention or escalation, while low-to-medium complexity work may be subject to delays or deprioritization.

### 4. **Fred Luddy's Performance is Consistent Across Categories**

Fred's elevated resolution times persist across all incident types:

| Category | Fred's Mean | Dataset Mean |
|----------|-------------|--------------|
| Database Access | 715.5 hours | 266.4 hours |
| Email Server | 708.0 hours | 261.6 hours |
| VPN Connectivity | 850.9 hours | 333.7 hours |
| Software Issues | 1,093.2 hours | 569.2 hours |

This pattern is **not driven by case selection**; Fred is not disproportionately assigned harder cases. His complexity and severity distributions are comparable to other agents.

### 5. **Resolution Mechanism Shows Modest Impact**

Average resolution by mechanism (positive times only):
- **Server Restart Required:** 208.3 hours
- **Network Config Required:** 239.4 hours
- **Software Patch Required:** 374.7 hours
- **Credentials Reset Required:** 292.6 hours

Credential and software patch cases run longer, but this alone does not explain Fred Luddy's 5× longer mean time.

---

## Data Quality Note

The dataset contains **50 records with negative resolution times** (opened_at > closed_at), suggesting timestamping errors or system anomalies. These records are excluded from analysis. This affects ~10% of the dataset and could mask or exaggerate some patterns if concentrated with specific agents.

---

## Conclusions

**Skill and Process Factors:**
- The primary driver of longer resolution times is **agent assignment**, not incident characteristics.
- Fred Luddy's consistent performance across all incident types suggests **individual capacity constraints** (e.g., workload, prioritization, or skill gaps) rather than case complexity.
- Other agents (Beth Anglin, Charlie Whitherspoon, Luke Wilson, Howard Johnson) resolve incidents ~4–5 times faster, indicating established, efficient processes.

**Secondary Factors:**
- Issue complexity has a weak and non-intuitive relationship with resolution time.
- Incident severity shows minimal variation across priority levels.
- Resolution mechanism type has modest explanatory power.

**Recommendation:**
Further investigation should focus on Fred Luddy's workflow, resource allocation, technical capabilities, and case handling procedures to identify bottlenecks and improvement opportunities.
