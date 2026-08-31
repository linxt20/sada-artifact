---
dataset: flag_13
scenario: causal_duration
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "resolution_duration_variation"
query: "Why do resolution duration values vary across tickets?"
source_table: augment_table/flag_13/causal_duration/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:15:18.222419+00:00
wall_seconds: 111.74
---

# Why Do Resolution Duration Values Vary Across Tickets?

## Overview

The dataset contains **500 tickets** with resolution durations encoded in the `closed_at` column (format MM:SS.s, interpreted as total minutes). Duration spans **10.9 to 3,597.2 minutes** (≈11 min to 60 hrs), with a mean of **1,803 min (~30 hrs)** and median of **1,791 min (~29.8 hrs)**. The distribution is broad and roughly uniform across six 10-hour bands, suggesting multiple concurrent drivers rather than a single dominant factor.

**Duration distribution:**

| Bucket | Count |
|--------|-------|
| < 10 hrs | 79 |
| 10–20 hrs | 85 |
| 20–30 hrs | 88 |
| 30–40 hrs | 84 |
| 40–50 hrs | 91 |
| 50–60 hrs | 73 |

---

## Method Note

TAPP-generated columns used in this analysis: `incident_category`, `failure_mode`, `affected_system_scope`, `resolver_match`, `ticket_open_hour_band`. Columns `assigned_resolver` and `caller_id_group` were reviewed but provided redundant or low-signal information relative to existing structured fields (`assigned_to`, `caller_id`).

---

## Key Drivers of Duration Variation

### 1. Assigned Resolver (Individual Agent Effect)

The strongest structured signal comes from **which agent handled the ticket** (`assigned_to`). Among the five resolvers (all with n ≥ 91):

| Resolver | n | Mean (min) | Median (min) |
|---|---|---|---|
| Howard Johnson | 101 | 1,726.9 | 1,609.4 |
| Beth Anglin | 100 | 1,755.7 | 1,740.0 |
| Luke Wilson | 98 | 1,828.3 | 1,799.0 |
| Fred Luddy | 110 | 1,841.5 | 1,926.3 |
| Charlie Whitherspoon | 91 | 1,865.9 | 2,029.9 |

The spread between fastest and slowest resolver is ~139 min mean and ~420 min median — meaningful given the overall ~1,000 min standard deviation. Charlie Whitherspoon's median (2,030 min) is 26% higher than Howard Johnson's (1,609 min).

### 2. Failure Mode (`failure_mode` — TAPP)

The `failure_mode` column reveals the most differentiated duration spread across all variables:

| Failure Mode | n | Mean (min) | Median (min) |
|---|---|---|---|
| `other` | 50 | 1,605.8 | 1,484.8 |
| `sync_failure` | 10 | 1,735.6 | 1,419.4 |
| `outage` | 39 | 1,754.3 | 1,642.4 |
| `not_responding` | 44 | 1,714.1 | 1,712.2 |
| `access_denied` | 117 | 1,789.5 | 1,852.5 |
| `connectivity_failure` | 230 | 1,876.2 | 1,863.6 |
| `installation_failure` | 10 | 1,914.8 | 1,946.1 |

`connectivity_failure` and `installation_failure` tickets take ~18–26% longer (median) than `other` or `sync_failure` tickets. This semantic facet adds meaningful signal not captured by raw `category` alone.

### 3. Incident Category (`incident_category` — TAPP)

| Incident Category | n | Mean (min) | Median (min) |
|---|---|---|---|
| `other` | 16 | 1,661.9 | 1,152.1 |
| `email` | 134 | 1,741.2 | 1,627.7 |
| `database` | 134 | 1,791.5 | 1,816.5 |
| `vpn_access` | 109 | 1,820.9 | 1,819.1 |
| `network_connectivity` | 72 | 1,882.5 | 1,905.0 |
| `software_update` | 12 | 1,951.1 | 1,864.8 |
| `server_infrastructure` | 23 | 1,919.0 | 2,116.7 |

Server/infrastructure and software-related categories cluster at the high end (median ≥1,865 min), while email/general tickets resolve faster. This is consistent with the raw `category` column (Software mean: 1,893 min vs. Database: 1,750 min).

### 4. Priority

Priority shows only a **weak effect** on duration, with no monotonic relationship:

| Priority | n | Mean (min) | Median (min) |
|---|---|---|---|
| 1 - Critical | 83 | 1,820.7 | 1,920.0 |
| 2 - High | 391 | 1,795.7 | 1,778.9 |
| 3 - Moderate | 24 | 1,887.1 | 1,752.0 |
| 4 - Low | 2 | 1,500.0 | 1,500.0 |

The narrow mean range (~387 min spread) and small sample sizes at extreme priorities limit interpretation. Critical tickets do not resolve faster than High tickets, suggesting SLA escalation does not compress resolution time in this data.

### 5. Time of Day (`ticket_open_hour_band` — TAPP)

| Band | n | Mean (min) | Median (min) |
|---|---|---|---|
| afternoon_12_18 | 118 | 1,770.4 | 1,621.2 |
| evening_18_24 | 122 | 1,792.9 | 1,838.6 |
| morning_6_12 | 132 | 1,806.4 | 1,760.0 |
| overnight_0_6 | 128 | 1,839.3 | 1,863.6 |

Tickets opened overnight show a ~69 min higher mean and ~242 min higher median vs. afternoon tickets, consistent with reduced staffing during off-hours. However, the effect is modest and within noise given the high variance.

### 6. Resolver Match (`resolver_match` — TAPP)

`resolver_match` (whether `assigned_to` matches `assigned_resolver`) shows **negligible effect**:

| resolver_match | n | Mean (min) | Median (min) |
|---|---|---|---|
| True | 97 | 1,808.9 | 1,867.1 |
| False | 403 | 1,801.6 | 1,778.9 |

Only 97/500 (19.4%) of tickets matched; the ~7 min mean difference is not practically significant. This facet is **weak and not a material driver**.

### 7. Affected System Scope (`affected_system_scope` — TAPP)

| Scope | n | Mean (min) | Median (min) |
|---|---|---|---|
| server_side | 236 | 1,771.4 | 1,780.3 |
| client_side | 78 | 1,828.4 | 1,655.0 |
| network_infrastructure | 186 | 1,832.6 | 1,832.0 |

Network infrastructure tickets average ~61 min longer than server-side tickets. The effect is mild and partially overlaps with `assignment_group` (Network group mean: 1,794 min; Service Desk: 1,969 min).

### 8. Temporal Trend (Opened Month)

Monthly mean durations range from ~1,429 min (Jun 2023) to ~2,175 min (Jan 2023/2024), suggesting possible seasonal or volume-related effects. January 2024 (n=77, mean=2,071 min) stands out as notably slower. This may reflect post-holiday staffing or increased ticket volume.

---

## Summary of Drivers

| Driver | Type | Effect Size | Confidence |
|---|---|---|---|
| Individual resolver (`assigned_to`) | Structured | Moderate (up to ~420 min median gap) | High (n≥91 per group) |
| Failure mode (`failure_mode`) | TAPP | Moderate (~380 min median range) | Moderate |
| Incident category (`incident_category`) | TAPP | Moderate (~960 min median range) | Moderate |
| Opened month (temporal) | Structured | Moderate (~740 min mean range) | Moderate |
| Time of day (`ticket_open_hour_band`) | TAPP | Small (~242 min median) | Low–Moderate |
| Category / assignment group | Structured | Small–moderate | Moderate |
| Priority | Structured | Weak, non-monotonic | Low |
| Resolver match (`resolver_match`) | TAPP | Negligible | Low |

## Conclusions

Resolution duration varies primarily due to **who handles the ticket** (individual resolver efficiency) and **what type of failure occurred** (connectivity/installation issues take longer than unclassified or sync failures). The TAPP-generated `failure_mode` and `incident_category` columns add meaningful semantic granularity on top of the raw `category` field, confirming that server/infrastructure and connectivity problems are structurally harder to resolve. Time-of-day (`ticket_open_hour_band`) provides a small but directionally consistent overnight penalty. Priority does not compress resolution time. The near-flat duration distribution across priority tiers suggests that triage urgency and actual resolution effort are decoupled in this dataset.
