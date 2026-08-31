---
dataset: flag_2
scenario: eda_resolution
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary across category, priority, and assignment group?"
source_table: augment_table/flag_2/eda_resolution/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:18:28.931052+00:00
wall_seconds: 151.6
---

# Resolution Time Analysis Across Category, Priority, and Assignment Group

## Executive Summary

This analysis examines how incident resolution time varies across three primary dimensions: **category**, **priority**, and **assignment group**, supplemented by semantic features from TAPP augmentation. The analysis covers **500 incidents** with **372 closed incidents** providing resolution time data (mean resolution time: **1,043 hours**, median: **1,032 hours**).

### Key Findings:
- **Category**: Network issues take longest (1,079 hrs avg), while Database issues resolve fastest (955 hrs avg)
- **Priority**: Critical and Moderate priority incidents resolve slower (~120 hrs avg) than High priority (1,020 hrs avg)
- **Assignment Group**: Database and Hardware groups resolve incidents fastest; Service Desk and Network groups are slowest
- **TAPP Severity Signal** (strong correlation, r=0.57) is the most predictive TAPP feature: complete outages take 694 hours longer than partial access issues

---

## Method Note

**TAPP-generated columns used in analysis:**
- `issue_severity_signal`: Categorizes impact level (partial_access, outage_complete, performance_degradation, Unknown)
- `issue_complexity_signal`: Categorizes issue type (application_focused, infrastructure_systemic, endpoint_device, user_access)
- `primary_issue_domain`: Identifies technical domain (database, connectivity, email, software, hardware)
- `caller_frequency_indicator`: Caller history (new_or_rare_caller, repeat_caller_moderate, repeat_caller_high_frequency)
- `same_person_closure_flag`: Whether assignee also closed the incident (weak signal)
- `incident_closure_status`: Closure type (closed, resolved)
- `assigned_technician`: Identifies assigned staff member

---

## 1. Resolution Time by Category

| Category | N | Mean (hrs) | Median (hrs) | Std Dev | Min | Max |
|----------|---|-----------|-------------|---------|-----|-----|
| **Database** | 86 | **955** | 967 | 557 | 31 | 2,170 |
| **Hardware** | 12 | 1,105 | 1,021 | 637 | 118 | 1,997 |
| **Inquiry / Help** | 7 | 958 | 686 | 674 | 110 | 2,018 |
| **Network** | 197 | **1,079** | 1,046 | 630 | 24 | 2,205 |
| **Software** | 70 | 1,051 | 985 | 652 | 38 | 2,206 |

**Interpretation:**
- **Database incidents** resolve fastest (955 hrs), 12% quicker than Network incidents
- **Network issues** have the longest resolution time (1,079 hrs) despite high volume (197/372 = 53% of closed incidents)
- **Hardware and Inquiry/Help** categories have small sample sizes but similar resolution times to Database
- Software incidents fall in the middle (1,051 hrs)
- **Variance**: Network incidents show high variability (SD=630), suggesting inconsistent resolution across different types of network problems

---

## 2. Resolution Time by Priority

| Priority | N | Mean (hrs) | Median (hrs) | Std Dev | Min | Max |
|----------|---|-----------|-------------|---------|-----|-----|
| **1 - Critical** | 57 | **1,119** | 1,255 | 624 | 110 | 2,170 |
| **2 - High** | 283 | **1,019** | 974 | 601 | 24 | 2,206 |
| **3 - Moderate** | 32 | **1,121** | 1,100 | 750 | 53 | 2,198 |

**Interpretation:**
- **High priority** incidents resolve ~100 hours faster than both Critical and Moderate
- **Critical and Moderate** priorities converge at ~1,120 hrs (suggests resource allocation may not distinguish these levels effectively)
- **High priority** dominates the portfolio (76% of closed incidents, n=283)
- Median resolution for Critical (1,255 hrs) exceeds both mean and High priority median, indicating right-skewed distribution
- **Counterintuitive finding**: Moderate priority shows resolution speed equal to Critical, suggesting possible workload prioritization misalignment

---

## 3. Resolution Time by Assignment Group

| Assignment Group | N | Mean (hrs) | Median (hrs) | Std Dev | Min | Max |
|------------------|---|-----------|-------------|---------|-----|-----|
| **Database** | 89 | **947** | 960 | 553 | 31 | 2,170 |
| **Hardware** | 4 | 926 | 794 | 786 | 118 | 1,997 |
| **Service Desk** | 32 | 1,102 | 1,129 | 613 | 53 | 2,198 |
| **Network** | 221 | **1,074** | 1,046 | 627 | 24 | 2,205 |
| **Software** | 25 | 1,028 | 823 | 733 | 82 | 2,162 |
| **Openspace** | 1 | 1,853 | 1,853 | — | 1,853 | 1,853 |

**Interpretation:**
- **Database group** achieves fastest resolution (947 hrs) with consistent performance (SD=553) across 89 incidents
- **Network group** is largest (221/372 = 59% of closed incidents) but slowest after Service Desk (1,074 hrs)
- **Service Desk** surprisingly shows longest resolution (1,102 hrs) despite small sample (n=32)
- **Hardware group** resolves quickly (926 hrs) but sample is minimal (n=4)
- **Assignment group size and resolution speed appear inversely related**: larger groups (Network, Database) handle routine issues faster than specialized groups (Service Desk)

---

## 4. Two-Way Interaction Analysis

### 4.1 Category × Priority

Mean resolution hours:

|  | 1 - Critical | 2 - High | 3 - Moderate |
|---|---|---|---|
| **Database** | 1,244 | 910 | 817 |
| **Hardware** | 1,298 | 1,010 | 1,435 |
| **Inquiry / Help** | 1,417 | 1,056 | 352 |
| **Network** | 1,039 | 1,082 | 1,211 |
| **Software** | 1,257 | 976 | 1,233 |

**Key Interaction Effects:**
- **Database + Critical**: 1,244 hrs (22% slower than Database + High: 910 hrs)
- **Database + Moderate**: 817 hrs (fastest combination, well below all other Database combinations)
- **Network + High**: 1,082 hrs (largest subcategory, n=153), near Network average
- **Inquiry/Help + Moderate**: 352 hrs (notably fast, but n=2 only)
- **Hardware categories** show inconsistent patterns due to small sample sizes

### 4.2 Category × Assignment Group

Mean resolution hours (selected large groups):

|  | Database | Network | Service Desk | Software |
|---|---|---|---|---|
| **Database** | 955 | 703 | — | — |
| **Network** | — | 1,079 | 1,637 | — |
| **Software** | — | — | 1,067 | 1,028 |

**Interpretation:**
- **Database + Network Assignment**: 703 hrs (26% faster than overall Database category average), suggesting cross-group support is efficient
- **Network + Service Desk**: 1,637 hrs (52% slower than Network group average), indicating Service Desk handles complex Network escalations with delayed resolution
- **Software + Software Assignment**: 1,028 hrs (near average), showing normalized resolution for matched assignment

### 4.3 Priority × Assignment Group

Mean resolution hours:

|  | Database | Hardware | Network | Service Desk | Software |
|---|---|---|---|---|---|
| **1 - Critical** | 1,217 | — | 1,033 | 1,356 | 1,093 |
| **2 - High** | 902 | 1,057 | 1,078 | 1,044 | 913 |
| **3 - Moderate** | 817 | 794 | 1,165 | 1,200 | 1,541 |

**Key Patterns:**
- **Database group consistently resolves fastest** across all priority levels (817–1,217 hrs)
- **Service Desk shows priority inversion**: Critical (1,356 hrs) slower than High (1,044 hrs), suggesting escalation delays
- **Software group + Moderate priority**: 1,541 hrs (anomaly—34% slower than Software + High: 913 hrs)
- **Network + Moderate**: 1,165 hrs, exceeds Network + Critical (1,033 hrs)

---

## 5. TAPP-Generated Semantic Features

### 5.1 Issue Severity Signal (Strongest Predictor, r=0.57)

| Severity Level | N | Mean (hrs) | Median (hrs) | Interpretation |
|---|---|---|---|---|
| **Partial Access** | 187 | 692 | 650 | Degraded but operational |
| **Performance Degradation** | 15 | 1,325 | 1,471 | System slower than normal |
| **Complete Outage** | 165 | 1,386 | 1,442 | Full service unavailable |
| **Unknown** | 5 | 2,031 | 2,047 | Unclassified severity |

**Interpretation:**
- **Strong severity-resolution correlation (0.57)** is the most reliable TAPP signal
- **Partial access issues resolve 50% faster** (692 hrs vs. 1,386 hrs for complete outages)—694-hour difference is substantial
- **Complete outages (165 incidents)** require complex recovery, averaging 58 days
- **Performance degradation** sits between partial access and outage, confirming graduated severity scale
- **Unknown category** (n=5) shows extreme resolution times (2,031 hrs), suggesting classification failures correlate with extended resolution

### 5.2 Issue Complexity Signal (Weak Predictor, r=0.15)

| Complexity Type | N | Mean (hrs) | Median (hrs) | Interpretation |
|---|---|---|---|---|
| **Application-Focused** | 156 | 885 | 769 | Single application issue |
| **Endpoint Device** | 16 | 1,106 | 856 | Desktop/laptop hardware |
| **Infrastructure Systemic** | 180 | 1,141 | 1,234 | Core systems affected |
| **User Access** | 20 | 1,352 | 1,396 | Permission/authentication |

**Interpretation:**
- **Application-focused** issues resolve fastest (885 hrs), confirming scoping advantage
- **Infrastructure systemic issues** take 29% longer (1,141 hrs), reflecting broader impact and coordination requirements
- **User access** problems are slowest (1,352 hrs), suggesting permission verification steps add resolution time
- **Weak correlation (0.15)** indicates complexity classification captures some but not dominant variation; other factors (category, priority) matter more

### 5.3 Primary Issue Domain

| Domain | N | Mean (hrs) | Median (hrs) |
|---|---|---|---|
| **Database** | 99 | 910 | 838 |
| **Hardware** | 4 | 926 | 794 |
| **Email** | 110 | 1,086 | 1,100 |
| **Connectivity** | 141 | 1,094 | 1,068 |
| **Software** | 18 | 1,145 | 989 |

**Interpretation:**
- **Database domain** resolves fastest (910 hrs), aligning with Database category and assignment group findings
- **Connectivity (141 incidents)** and **Email (110 incidents)** dominate portfolio and both exceed 1,080 hrs
- **Software domain** is slowest (1,145 hrs) but smallest (n=18)
- Domain classification largely mirrors Category dimension, confirming structural alignment

### 5.4 Caller Frequency Indicator (Weak Predictor, r=-0.07)

| Caller Type | N | Mean (hrs) | Median (hrs) |
|---|---|---|---|
| **New or Rare** | 79 | 1,136 | 1,090 |
| **Repeat Moderate** | 98 | 1,031 | 1,028 |
| **Repeat High Frequency** | 195 | 1,012 | 960 |

**Interpretation:**
- **Weak negative correlation** (r=-0.07) suggests repeat callers have marginally faster resolution (1,012 vs. 1,136 hrs)
- **High-frequency repeat callers** resolve 10% faster than new callers, suggesting organizational familiarity aids resolution
- Small differences (125 hrs) relative to overall mean (1,043 hrs) limit practical significance
- **Caller frequency does not strongly drive resolution time** compared to severity and complexity signals

### 5.5 Same-Person Closure Flag (Negligible Predictor, r=0.02)

| Flag | N | Mean (hrs) | Median (hrs) |
|---|---|---|---|
| **False** (Different person closes) | 299 | 1,038 | 1,003 |
| **True** (Same person closes) | 73 | 1,064 | 1,090 |

**Interpretation:**
- **Negligible difference** (26-hour gap) and correlation near zero (r=0.02)
- Whether assignee also closes incident has minimal impact on total resolution time
- Suggests closure workflow efficiency is not a primary time driver
- **Low predictive value** for this feature

---

## 6. Combined Analysis: Priority × Category × Assignment Group

### Slowest combinations (top 10):

| Priority | Category | Assignment Group | N | Mean (hrs) |
|---|---|---|---|---|
| 3 - Moderate | Hardware | Network | 1 | 1,982 |
| 2 - High | Network | Openspace | 1 | 1,853 |
| 2 - High | Network | Service Desk | 1 | 1,788 |
| 3 - Moderate | Software | Software | 4 | 1,541 |
| 1 - Critical | Software | Network | 1 | 1,486 |
| 3 - Moderate | Network | Service Desk | 1 | 1,486 |
| 1 - Critical | Inquiry/Help | Network | 2 | 1,417 |
| 1 - Critical | Software | Service Desk | 1 | 1,356 |
| 1 - Critical | Hardware | Network | 1 | 1,298 |
| 1 - Critical | Database | Database | 13 | 1,244 |

**Interpretation:**
- **Extreme outliers** (>1,700 hrs) involve small samples (n=1) and unusual combinations (Moderate priority + Hardware, Openspace assignment)
- **Critical + Database + Database** (n=13) is largest slow combination and has legitimate complexity driver (critical database issues)
- **Moderate + Software + Software** (n=4) is anomaly—Moderate priority software issues should resolve faster
- **Service Desk assignments** appear in multiple slow combinations (Openspace, Network, Inquiry/Help), suggesting escalation delays

### Fastest combinations (bottom 10):

| Priority | Category | Assignment Group | N | Mean (hrs) |
|---|---|---|---|---|
| 2 - High | Database | Database | 61 | 861 |
| 2 - High | Database | Network | 2 | 625 |
| 3 - Moderate | Database | Database | 18 | 817 |
| 2 - High | Software | Network | 1 | 814 |
| 2 - High | Inquiry/Help | Network | 2 | 1,056 |
| 2 - High | Software | Software | 18 | 913 |
| 2 - High | Network | Database | 2 | 625 |

**Interpretation:**
- **High + Database + Database** (n=61, 861 hrs) is largest routine combination—represents 16% of all closed incidents
- **Database assignment group dominates fast combinations**, confirming efficiency advantage
- **High priority + matched assignment** (Database, Software groups) consistently resolves faster
- **Service Desk absent from fast list**, confirming earlier finding of slower resolution

---

## 7. Interaction: Severity Signal × Category

Mean resolution hours:

|  | Database | Hardware | Inquiry/Help | Network | Software |
|---|---|---|---|---|---|
| **Complete Outage** | 1,224 | 1,500 | — | 1,439 | 1,091 |
| **Partial Access** | 639 | 784 | 1,178 | 640 | 916 |
| **Performance Degradation** | 857 | — | — | 1,375 | 1,795 |

**Interpretation:**
- **Severity signal moderates category effects**: partial access Database issues (639 hrs) resolve as fast as Network partial access (640 hrs), despite category typically driving 12% variance
- **Complete outage + Network**: 1,439 hrs (33% slower than Network average of 1,079 hrs)
- **Complete outage + Hardware**: 1,500 hrs (extreme, n=7 hardware incidents)
- **Severity signal is orthogonal to category**: both dimensions independently contribute to resolution time

---

## 8. Summary of Drivers

**Relative Impact on Resolution Time (ranked by effect magnitude):**

1. **Issue Severity Signal** (TAPP): 694-hour range (partial access vs. complete outage); correlation r=0.57 ✓
2. **Assignment Group**: 177-hour range (Database vs. Service Desk); operational indicator
3. **Category**: 124-hour range (Database vs. Network); domain-specific factors
4. **Issue Complexity Signal** (TAPP): 467-hour range (application vs. user access); correlation r=0.15
5. **Priority Level**: 101-hour range (High vs. Critical/Moderate); counterintuitive lack of strong effect
6. **Primary Issue Domain** (TAPP): 235-hour range (Database vs. Software); mirrors Category
7. **Caller Frequency** (TAPP): 125-hour range; weak predictor (r=-0.07)
8. **Same-Person Closure** (TAPP): 26-hour range; negligible effect (r=0.02)

**Strongest Signal**: Issue Severity (complete outage vs. partial access = 694 hours)  
**Most Practical Lever**: Assignment Group (Database group 127 hours faster than Network)  
**Organizational Opportunity**: Resolve priority inversion (Critical resolves slower than High)

---

## Recommendations

1. **Prioritize complete outage recovery**: These incidents require 694 hours more than partial access; consider dedicated triage/escalation for outages
2. **Expand Database assignment group**: Resolves 12–17% faster than Network group; analyze best practices for replicability
3. **Audit Service Desk escalation process**: Service Desk group resolves slowest (1,102 hrs); examine workflow bottlenecks
4. **Realign priority-resolution alignment**: Critical and Moderate priorities should resolve faster than High; investigate resource allocation
5. **Leverage severity signal**: Issue Severity Signal is strongest TAPP predictor (r=0.57); use for SLA differentiation
6. **Focus on infrastructure issues**: Infrastructure systemic issues (1,141 hrs) take 29% longer than application-focused (885 hrs); consider specialized team or tooling
