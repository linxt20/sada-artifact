---
dataset: flag_2
scenario: causal_delay
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "resolution_time"
query: "Controlling for priority and category, which underlying causes explain longer resolution times?"
source_table: augment_table/flag_2/causal_delay/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:15:05.689236+00:00
wall_seconds: 71.15
---

# Analysis Report: Causal Factors in Resolution Time Delays

## Dataset Overview
- **Total records analyzed:** 372 incidents with complete resolution time data
- **Variant:** skill_off
- **Focus:** Identifying underlying causes that explain longer resolution times, controlling for priority and category

## Key Findings

### 1. Infrastructure Involvement: Mixed Impact

**Infrastructure-related issues do NOT consistently extend resolution time:**

- **Priority 2 (High)** [283 incidents]: 
  - WITH infrastructure: mean 1,076.5 hours
  - WITHOUT infrastructure: mean 957.0 hours
  - **Impact: +119.5 hours (+12.5%)**
  
- **Priority 1 (Critical)** [57 incidents]:
  - WITH infrastructure: mean 1,099.3 hours  
  - WITHOUT infrastructure: mean 1,131.7 hours
  - **Impact: -32.4 hours (-2.9%) — inverse relationship**

**Interpretation:** For High priority incidents, infrastructure involvement adds delay. However, for Critical incidents, the relationship reverses, suggesting that Critical infrastructure issues may receive priority handling.

### 2. Database Issues: Category-Dependent Effect

**Database involvement shows contradictory patterns by priority level:**

- **Priority 2 (High)** [283 incidents]:
  - WITH database: mean 901.7 hours
  - WITHOUT database: mean 1,058.2 hours
  - **Impact: -156.5 hours (-14.8%) — shorter resolution**
  
- **Priority 1 (Critical)** [57 incidents]:
  - WITH database: mean 1,216.6 hours
  - WITHOUT database: mean 1,086.8 hours
  - **Impact: +129.8 hours (+11.9%) — longer resolution**

**Interpretation:** Database issues in Critical incidents take substantially longer, suggesting complexity or resource constraints. In High priority incidents, database issues may be more straightforward to resolve.

### 3. Access Issues: Weak Evidence for Direct Impact

**Access issues show inconsistent effects:**

- **Priority 2 (High)**: WITH vs WITHOUT access issues show nearly identical means (1,034.8 vs 1,002.9 hours)
- **Priority 1 (Critical)**: Access issues slightly reduce time (994.7 vs 1,148.3 hours)
- **Priority 3 (Moderate)**: Access issues increase time (1,230.9 vs 1,083.9 hours)

**Note:** Access issues have weak explanatory power across priority levels, suggesting they are not a primary driver of extended resolution times.

### 4. Performance Issues: Rare, Insufficient Evidence

**Performance issues are uncommon (51 of 500 incidents) and show unclear patterns:**

- **Priority 2 (High)** [24 incidents with performance issues]:
  - WITH performance: mean 882.3 hours
  - WITHOUT performance: mean 1,032.2 hours
  - **Impact: -149.9 hours (-14.5%)**

- **Priority 3 (Moderate)**: No incidents with performance issues recorded

**Interpretation:** Performance issues, when present, appear associated with shorter resolution in High priority incidents. However, the small sample size (51 total) limits confidence in this finding.

### 5. Critical Factors by Incident Category (High Priority)

**Network incidents (153 records, 54% of High priority):**
- Mean resolution: 1,082.3 hours
- Infrastructure involvement adds ~negligible impact in this category
- With access issue + infrastructure: mean 1,107.2 hours

**Database incidents (68 records, 24% of High priority):**
- Mean resolution: 909.8 hours
- Infrastructure involvement: +170.5 hours (1,017.6 vs 847.1)
- **Database + Infrastructure combination is the most time-consuming scenario**

**Software incidents (50 records, 18% of High priority):**
- Mean resolution: 975.8 hours
- NO infrastructure involvement observed (all 50 are infrastructure=0)
- Consistent timing regardless of database or access involvement

### 6. Longest Resolution Incidents Analysis

**Top 20 longest-running incidents (over 1,975 hours):**
- 14/20 are Network category incidents
- 9/20 involved infrastructure
- 9/20 involved access issues
- **Notable:** Software and Network incidents with email/connectivity themes dominate the longest delays
- **Exception:** One Inquiry/Help incident (2,018.4 hours) with infrastructure involvement

**Pattern:** Persistent infrastructure connectivity issues (VPN, WiFi, network access) are the dominant factor in extremely long resolution times.

## Underlying Causes Summary

### Primary Delays Identified:

1. **Infrastructure complexity in Database issues** — When database problems also involve infrastructure (mean 1,017.9 hours for combined), resolution extends significantly, suggesting coordinated infrastructure and database team involvement is required.

2. **Network infrastructure with access issues** — The combination of infrastructure involvement + access issues in Network category shows mean resolution of 1,107.2 hours, indicating multi-layered troubleshooting requirements.

3. **Unresolved connectivity patterns** — The longest-running incidents cluster around persistent email and network connectivity issues with infrastructure involvement, suggesting these problems recur or resist standard resolution procedures.

### Weak or Contradictory Causes:

1. **Access issues alone** — Minimal independent effect on resolution time (mean differences ≤150 hours and inconsistent direction)

2. **Performance issues** — Insufficient sample size and conflicting direction of effect; likely confounded with other factors

3. **Infrastructure in Critical priority** — Counterintuitively associated with *shorter* resolution, suggesting Critical incidents receive expedited handling regardless of infrastructure involvement

## Recommendations

- **Prioritize:** Database incidents combined with infrastructure involvement (add specialized diagnostic capabilities)
- **Investigate:** Why Network + Access Issue + Infrastructure combinations take 1,100+ hours (20%+ longer than average)
- **Review:** Persistent email/connectivity issue escalation procedures; these dominate the longest delays
- **Note:** Database-only issues in High priority incidents resolve faster (avg 901.7 hours) — consider this model for optimization

---
**Analysis Methodology:** Stratified comparison of resolution times by priority level and category, examining underlying cause flags (involves_infrastructure, involves_database, involves_access_issue, involves_performance) to identify independent and interactive effects on resolution delays.
