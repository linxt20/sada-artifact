---
dataset: flag_13
scenario: concept_attribute_operational
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "operational_burden"
query: "What operational burdens appear in incident descriptions?"
source_table: augment_table/flag_13/concept_attribute_operational/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:14:19.407521+00:00
wall_seconds: 52.57
---

# Operational Burdens in Incident Descriptions

## Executive Summary

Analysis of 500 IT incidents reveals five distinct operational burden aspects affecting the organization. **Connectivity loss** dominates (35% of incidents), followed by **data access blockages** (26%) and **service degradation** (26%). Together, these three categories account for 87% of operational impact, with acute infrastructure challenges in VPN/WiFi, email systems, and database access forming the operational backbone of this dataset.

## Burden Distribution

| Operational Burden Aspect | Count | % of Total | Priority Profile |
|---------------------------|-------|-----------|------------------|
| Connectivity loss | 177 | 35.4% | 161 High, 11 Critical |
| Data access blocked | 132 | 26.4% | 110 High, 16 Critical |
| Service degradation | 131 | 26.2% | 73 High, 55 Critical |
| Client malfunction | 37 | 7.4% | 27 High, 9 Moderate |
| Performance issue | 23 | 4.6% | 20 High, 3 Moderate |

## Key Operational Burden Patterns

### 1. Connectivity Loss (177 incidents, 35%)

**Infrastructure Impact:**
- **VPN Access (108 incidents)**: Chronic inability to connect to office VPN is the single largest operational burden, predominantly affecting individual users but with company-wide implications for remote workers
- **WiFi Connectivity (14 incidents)**: Office WiFi connectivity gaps create localized friction
- **Network Connectivity (26+ incidents)**: Departmental and building-wide network disruptions

**Severity Profile:**
- 161 High-priority / 11 Critical-priority incidents
- Recurrence Rate: 74% recurring (131/177 True flag)

**Business Impact:** Remote access disruptions cascade across the workforce, blocking VPN-dependent workflows and isolating individual contributors.

### 2. Data Access Blocked (132 incidents, 26%)

**Infrastructure Impact:**
- **Database Access (120+ incidents)**: The dominant cause—inability to access company databases (both single-user and company-wide scopes)
- **Email Account Access (5+ incidents)**: Email authentication barriers
- **Network Drive Access**: Data repository connectivity failures

**Severity Profile:**
- 110 High-priority / 16 Critical-priority incidents
- Company-wide scope dominates (65 incidents affecting entire organization)
- Recurrence Rate: 76% recurring (100/132 True flag)

**Business Impact:** Production data unavailability halts critical business operations; company-wide database outages represent systemic risk with scope spanning entire departments and business lines.

### 3. Service Degradation (131 incidents, 26%)

**Infrastructure Impact:**
- **Email System Failures (83 incidents)**: The largest sub-category—email server outages, connectivity issues, and system crashes affecting company-wide communication
- **Database Service Issues (8 incidents)**: Slow queries and performance constraints limiting data operations
- **Server Outages (9+ incidents)**: General server unavailability affecting multiple user scopes

**Severity Profile:**
- 73 High-priority / 55 Critical-priority (highest critical rate among burdens)
- Company-wide scope in 83 email-related incidents
- Recurrence Rate: 85% recurring (111/131 True flag)

**Business Impact:** Email system instability represents single-point-of-failure risk; nearly 6 in 10 service degradation incidents escalate to critical priority, indicating organizational dependency on these systems.

### 4. Client Malfunction (37 incidents, 7%)

**Infrastructure Impact:**
- **Email Client Issues (22 incidents)**: Outlook synchronization failures, client crashes, installation problems
- **Application Failures (5 incidents)**: Software crashes and installation failures
- **Hardware Issues (6 incidents)**: Printer malfunctions

**Severity Profile:**
- 27 High-priority / 9 Moderate-priority (lower severity than system-wide failures)
- Individual scope predominant
- Recurrence Rate: 62% recurring (23/37 True flag)

**Business Impact:** Client-side incidents isolate individual contributors but rarely cascade; often self-resolved or handled without escalation.

### 5. Performance Issues (23 incidents, 5%)

**Infrastructure Impact:**
- **Server Performance (6 incidents)**: High CPU/latency, slow response times
- **Application Performance (6 incidents)**: Software update-related degradation, slow execution
- **Database Performance (3 incidents)**: Query optimization and throughput constraints
- **Network Performance (4 incidents)**: Bandwidth/latency issues affecting user experience

**Severity Profile:**
- 20 High-priority / 1 Critical-priority
- Distributed individual and company-wide scopes
- Recurrence Rate: 26% recurring (6/23 True flag)—lowest recurrence among all burdens

**Business Impact:** Performance degradation creates friction rather than complete blockage; majority are non-recurring, suggesting one-time environmental stressors or workload spikes.

## Operational Risk Factors

### High-Recurrence Burdens (>75% recurring)
- **Connectivity loss** (74% recurring): Suggests persistent VPN/WiFi infrastructure issues requiring architectural remediation
- **Data access blocked** (76% recurring): Indicates systemic database availability or authentication problems
- **Service degradation** (85% recurring): Email system stability is chronically unstable; highest recurrence rate signals fundamental infrastructure instability

### Critical-Severity Concentration
- **Service degradation** shows disproportionately high critical rate (42% of incidents marked "1 - Critical")
- **Data access blocking** produces 16 critical incidents, primarily affecting company-wide database access
- Together, connectivity and data access represent 22 critical incidents but span broader user base

### Scope Concentration
- **Company-wide impact**: Email (83 incidents) and database (65 incidents) dominate; these represent organizational single points of failure
- **Individual/Localized**: VPN (108), WiFi (14), and client issues (37) primarily affect isolated users
- **Systemic dependency**: 83 email service degradations affecting company-wide operations indicate platform criticality

## Evidence and Caveats

**Strong Evidence:**
- Operational burden categorization is explicitly tagged in the dataset's `operational_burden_aspect` column
- Infrastructure components and scope data are consistently populated across all 500 incidents
- Burden distribution is clear with no ambiguity in the top three categories

**Weak Evidence / Limitations:**
- Performance issues show lower recurrence (26%), suggesting either better resilience or underreporting of non-critical performance incidents
- Client malfunction categorization may undercount user experience issues that don't formally escalate
- No data on incident duration or business revenue impact per burden type; severity levels are proxy indicators only
- Recurrence flags rely on incident reporter classification; some genuinely new issues may be mislabeled as recurring

## Recommendations

**Immediate Priorities:**
1. **VPN/Connectivity infrastructure audit**: 35% of all incidents stem from connectivity loss; infrastructure refresh required
2. **Email system stabilization**: 83 service degradation incidents on email alone; consider redundancy or platform upgrade
3. **Database access resilience**: 120+ data access incidents; review authentication, failover, and availability architecture

**Operational Improvements:**
- Reduce non-recurring performance incidents (26% recurrence suggests environmental tuning, not systemic problems)
- Investigate why client malfunction incidents (62% recurrence) persist; patch management and user training gaps likely exist
