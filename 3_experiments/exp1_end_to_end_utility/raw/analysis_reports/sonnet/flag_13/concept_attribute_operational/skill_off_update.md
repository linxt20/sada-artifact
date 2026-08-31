---
dataset: flag_13
scenario: concept_attribute_operational
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "operational_burden"
query: "What operational burdens appear in incident descriptions?"
source_table: augment_table/flag_13/concept_attribute_operational/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:11:50.804049+00:00
wall_seconds: 59.61
---

# Operational Burdens in Incident Descriptions

## Dataset Overview
- **500 incidents** with three augmented columns: `operational_burden_flags` (pipe-separated), `operational_burden_count`, and `primary_operational_burden`.
- Incidents span five categories: Network, Database, Software, Hardware, Inquiry/Help.

---

## Burden Types Identified

Eight distinct operational burden types appear across incident descriptions:

| Burden Type | Flag Occurrences | Primary Burden Count |
|---|---|---|
| `connectivity_issue` | 230 | 230 |
| `server_outage` | 131 | 113 |
| `database_burden` | 135 | 14 |
| `email_service_burden` | 134 | 29 |
| `access_denied` | 110 | 72 |
| `performance_degradation` | 48 | 10 |
| `software_failure` | 35 | 22 |
| `hardware_issue` | 7 | 4 |
| `other` | 6 | 6 |

> **Note:** Flag occurrences exceed primary counts for `database_burden` and `email_service_burden` because these frequently appear as secondary burdens in multi-burden incidents rather than as the primary classification.

---

## Dominant Patterns

### 1. Connectivity Issues (most prevalent)
- **230 incidents** (46%) list `connectivity_issue` as the primary burden.
- Heavily concentrated in **Network** category (181/230) and secondarily in **Database** (43).
- Almost entirely **2 - High** priority (206/230).
- Descriptions include WiFi failures, VPN access problems, and general network connectivity loss.

### 2. Server Outages (second most common)
- **113 incidents** (22.6%) primary; appears as a flag in 131.
- Uniquely skews toward **1 - Critical** priority (52/113 ≈ 46%), far higher than any other burden type — indicating outages drive the most severe incidents.
- Concentrated in **Network** (69) and **Database** (25) categories.

### 3. Access Denied
- **72 incidents** (14.4%) as primary burden, 110 as a flag.
- Predominantly **Database** (48) and **Software** (19) categories; nearly all **2 - High** priority (62/72).
- Represents authorization/permission failures rather than infrastructure issues.

### 4. Email Service Burden
- Only **29 primary** designations despite appearing in **134 flags** — the largest gap between flag count and primary count.
- Primarily a **co-occurring** burden layered onto connectivity or server incidents in the **Software** category (25 primaries).

### 5. Software Failure
- **22 primary** incidents, concentrated in **Software** category (17/22).
- Balanced across Critical and High priority.

### 6. Performance Degradation & Hardware Issue
- **Performance degradation**: 10 primary, 48 flags — frequently co-occurs with other burdens.
- **Hardware issue**: Only 4 primary, 7 flags — the rarest substantive burden type, limited to Hardware category.

---

## Multi-Burden Incidents

**273 of 500 incidents (54.6%)** carry two or more burden flags, indicating that many descriptions reflect overlapping operational failures:

- `server_outage` and `connectivity_issue` incidents are the most likely to be multi-burden (100 and 84 respectively among multi-burden primaries).
- `database_burden` and `email_service_burden` almost never lead as primary; they almost always appear as secondary flags.

---

## Exceptions and Weak Evidence

- **`other` (6 incidents)**: Near-zero presence; descriptions that don't clearly fit named burden types. These carry `operational_burden_count = 0`, suggesting the annotation model found no clear burden pattern.
- **`database_burden` as primary (14)**: Surprisingly low given 135 flag appearances — this burden is structurally secondary and may not independently drive incidents.
- **Priority 3–4 incidents** are rare across all burden types, suggesting low-priority tickets rarely escalate to flagged operational burden.

---

## Summary

The dominant operational burdens are **connectivity failures** and **server outages**, which together account for ~70% of primary-labeled incidents. **Access denied** issues form a distinct third cluster tied to authorization failures in Database and Software systems. **Email service burden**, **database burden**, and **performance degradation** function primarily as co-occurring secondary stressors. Server outages stand out as the burden most associated with **Critical priority**, making them the highest-stakes operational concern in the dataset.
