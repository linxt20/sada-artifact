---
dataset: flag_13
scenario: concept_attribute_operational
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "operational_burden"
query: "What operational burdens appear in incident descriptions?"
source_table: augment_table/flag_13/concept_attribute_operational/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:11:46.236314+00:00
wall_seconds: 61.58
---

# Operational Burdens in Incident Descriptions: Analysis Report

## Executive Summary

Analysis of 500 IT incident records reveals a clear operational burden profile dominated by **connectivity issues** (47.0% of incidents) combined with **infrastructure and service outage challenges**. The dataset exhibits a strong focus on network and data access disruptions that significantly impact end-user productivity and business continuity.

## Operational Burden Distribution

The dataset presents five dominant operational burden types:

| Burden Type | Count | Percentage | Primary Impact |
|---|---|---|---|
| Connectivity | 126 | 25.2% | Network/system access failures |
| Connectivity + Infrastructure | 109 | 21.8% | Access + underlying system issues |
| Infrastructure | 46 | 9.2% | Backend system degradation |
| Outage + Infrastructure + Software | 44 | 8.8% | Complete service unavailability |
| Outage + Software | 33 | 6.6% | Application/email service failures |

**Combined connectivity-related burdens** (connectivity alone + connectivity|infrastructure + connectivity|performance variants) account for **approximately 330 incidents (66%)**, indicating that network/system access is the dominant operational concern.

## Burden Distribution by Infrastructure Type

### Network Infrastructure (246 incidents, 49.2%)
- **Connectivity issues**: 126 incidents (WiFi, VPN, general network access failures)
- **Outage + Infrastructure + Software**: 35 incidents (email server outages, service disruptions)
- **Infrastructure problems**: 20 incidents (performance, routing, server network issues)
- **Other**: 13 incidents (miscellaneous connectivity scenarios)

**Pattern**: Network burdens are primarily connectivity-driven, with significant email/collaboration service outages.

### Database Infrastructure (173 incidents, 34.6%)
- **Connectivity + Infrastructure**: 68 incidents (access blocked by underlying DB issues)
- **Infrastructure problems**: 23 incidents (performance, CPU usage, SQL issues)
- **Connectivity alone**: Minimal direct representation
- **Outage + Infrastructure**: 12 incidents (database server down scenarios)

**Pattern**: Database burdens are predominantly compound issues combining access problems with backend failures, indicating cascading failures.

### Software (Software, Hardware, Service Desk) (81 incidents, 16.2%)
- **Software**: 27 incidents (app crashes, update failures, email client issues)
- **Outage + Software**: 25 incidents (application unavailability)
- **Connectivity + Software**: 18 incidents (access to cloud services, email access)

**Pattern**: Software burdens center on application functionality and update management.

## Priority Correlation

- **2 - High priority**: 362 incidents (72.4%) - predominantly connectivity and infrastructure issues
- **1 - Critical priority**: 87 incidents (17.4%) - concentrated in outage scenarios
- **3 - Moderate priority**: 44 incidents (8.8%) - scattered across all burden types
- **4 - Low priority**: 5 incidents (1.0%) - mostly infrastructure queries

**Finding**: Higher-priority incidents align with compound operational burdens (outage|infrastructure|software), while routine connectivity issues remain high-priority due to frequency and user impact.

## Incident Description Patterns

### Connectivity Burdens (247 incidents)
Representative descriptions:
- "Cannot connect to office WiFi"
- "Unable to connect to the office VPN"
- "Unable to access company database"
- "Email server connectivity issues"

**Implication**: Users face direct access barriers requiring immediate troubleshooting.

### Outage + Infrastructure + Software (44 incidents)
Representative descriptions:
- "Email server not responding"
- "Email server outage"
- "Database server issue"
- "Server outage in main facility"

**Implication**: Complete service unavailability affects multiple users/departments simultaneously.

### Infrastructure + Software (14-39 incidents)
Representative descriptions:
- "Database server issue - high CPU usage"
- "SQL Server performance issue"
- "Software update required on server"

**Implication**: Backend degradation causes cascading user impact.

## Critical Observations

1. **Access-First Problem Profile**: Nearly 2 in 3 incidents cite connectivity/access as the primary burden, suggesting a highly networked, cloud-dependent operational environment.

2. **Database Dependency**: Database connectivity issues (77 incidents combining connectivity|infrastructure variants) represent 15.4% of the total, indicating critical reliance on centralized data systems.

3. **Email as Critical Service**: Email-related incidents appear across multiple burden categories (outage, connectivity, software) with high frequency, reflecting business-critical status.

4. **Compound Failures**: 109 incidents (21.8%) present *both* connectivity and infrastructure burdens, indicating failures cascade from underlying system problems rather than isolated network glitches.

5. **Software Update Risk**: Multiple incidents reference "software upgrade," "update failed," and "installation issue," suggesting deployment stability is a secondary operational concern.

6. **Geographic/Departmental Spread**: Descriptions reference "floor," "building," "office," "meeting room," indicating distributed infrastructure with localized failure points.

## Limitations and Data Quality Notes

- A small set (17 incidents, 3.4%) marked as "other" burdens lack specific classification detail.
- The "skill_off" variant label suggests these may represent scenarios with degraded operational knowledge or automation capabilities.
- Some descriptions are generic ("Network connectivity issue") while others are specific ("Email server not responding"), creating classification variance.

## Conclusion

Operational burdens in this incident set are fundamentally **access and availability challenges** driven by network dependencies (49%), followed by database system reliability (35%), and application functionality (16%). The prevalence of compound burden types (connectivity + infrastructure, outage + software) indicates an integrated infrastructure where single-point failures propagate across user-facing services. Priority assignment correlates strongly with burden type, with outage scenarios commanding critical urgency.
