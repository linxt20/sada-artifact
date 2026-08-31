---
dataset: flag_2
scenario: eda_resolution
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary across category, priority, and assignment group?"
source_table: augment_table/flag_2/eda_resolution/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:17:12.413126+00:00
wall_seconds: 74.07
---

# Resolution Time Analysis: Category, Priority, and Assignment Group

**Query:** How does resolution time vary across category, priority, and assignment group?

---

## Method Note

TAPP-generated columns used in this analysis: `incident_category`, `failure_symptom`, `resolver_match`, `assignment_lag_present`, `resolution_delay_proxy`. Columns `affected_system`, `scope_qualifier`, and `caller_id_group` were reviewed but added no material signal beyond primary structured dimensions and are not foregrounded.

---

## Dataset Overview

- **500 total incidents**; 372 (74.4%) have a `closed_at` timestamp enabling direct resolution-time calculation.
- 128 records are in **New** or **In Progress** state (open/unresolved), representing a 25.6% non-closure rate — material when comparing group performance.
- Resolution time is measured as elapsed hours from `opened_at` to `closed_at`.

| Statistic | Hours |
|---|---|
| Mean | 1,043 |
| Median | 1,032 |
| 25th pct | 505 |
| 75th pct | 1,558 |
| Min | 24 |
| Max | 2,206 |

The **`resolution_delay_proxy`** TAPP column confirms the distribution: 69% of resolved incidents fall in the `over_seven_days` bucket, 12% `same_day`, and ~7% each in `one_to_three_days` and `four_to_seven_days`. This signals a bimodal pattern — cases resolve either quickly (same-day) or after an extended period.

---

## 1. Resolution Time by Priority

Priority differences are modest but structurally notable:

| Priority | N (resolved) | Mean Hours | Median Hours | Unresolved Rate |
|---|---|---|---|---|
| 1 - Critical | 57 | **1,119** | 1,255 | 27.8% |
| 2 - High | 283 | **1,020** | 974 | 25.5% |
| 3 - Moderate | 32 | **1,121** | 1,100 | 22.0% |

- **Critical incidents do not resolve faster than High** — their mean and median are both higher, which is counterintuitive and may indicate escalation complexity or resource contention.
- Moderate incidents have a similar mean to Critical (1,121 h vs 1,119 h), suggesting priority labeling does not reliably predict resolution speed in this dataset.
- The unresolved rate is highest for Critical (27.8%), further compounding effective backlog for the most urgent cases.

---

## 2. Resolution Time by Category

| Category | N (resolved) | Mean Hours | Median Hours | Unresolved Rate |
|---|---|---|---|---|
| Database | 86 | **955** | 967 | 25.9% |
| Inquiry / Help | 7 | **958** | 686 | 36.4% |
| Software | 70 | **1,051** | 985 | 18.6% |
| Hardware | 12 | **1,105** | 1,021 | 33.3% |
| Network | 197 | **1,079** | 1,046 | 26.8% |

- **Database** resolves fastest (mean 955 h, median 967 h); it is also the highest-volume non-Network category.
- **Network** is the dominant category (197 resolved, 269 total) and carries above-average resolution time (mean 1,079 h).
- **Hardware** has the highest unresolved rate (33.3%) alongside above-average resolution time — a compounding performance risk.
- **Inquiry / Help** shows a low median (686 h) but very small sample (7 records); its 36.4% unresolved rate is the worst, though N is too small to generalize.

The TAPP `incident_category` column refines the category signal:

| TAPP incident_category | N (resolved) | Mean Hours |
|---|---|---|
| server | 20 | 1,178 |
| software_update | 12 | 1,166 |
| vpn | 80 | 1,103 |
| email | 110 | 1,086 |
| network_connectivity | 53 | 948 |
| database | 89 | 947 |
| hardware | 4 | 926 |

Within the broad **Network** category, `vpn` incidents (n=80) average 1,103 h while `network_connectivity` incidents (n=53) average 948 h — a 155-hour gap. **Email** (n=110, mean 1,086 h) and **server** (n=20, mean 1,178 h) are the slowest semantic sub-types.

---

## 3. Resolution Time by Assignment Group

| Assignment Group | N (resolved) | Mean Hours | Median Hours | Unresolved Rate |
|---|---|---|---|---|
| Hardware | 4 | **926** | 794 | 20.0% |
| Database | 89 | **947** | 960 | 26.4% |
| Software | 25 | **1,028** | 823 | 21.9% |
| Network | 221 | **1,074** | 1,046 | 26.3% |
| Service Desk | 32 | **1,102** | 1,129 | 22.0% |
| Openspace | 1 | 1,853 | — | 0.0% |

- **Database** and **Hardware** groups are the fastest resolvers (mean ~926–947 h).
- **Service Desk** averages 1,102 h — higher than the Network group it partly supports — suggesting routing or triage overhead.
- **Network** handles 60% of all resolved incidents (221/372) and sits at mean 1,074 h; its scale means it dominates aggregate resolution time.
- `Openspace` (n=1) is an outlier at 1,853 h and should be treated as a routing anomaly.

---

## 4. Priority × Category Interaction

Mean resolution hours by category and priority:

| Category | 1 - Critical | 2 - High | 3 - Moderate |
|---|---|---|---|
| Database | 1,244 | 910 | 817 |
| Hardware | 1,298 | 1,010 | 1,435 |
| Inquiry / Help | 1,417 | 1,056 | 352 |
| Network | 1,039 | 1,082 | 1,211 |
| Software | 1,257 | 976 | 1,233 |

- **Critical-priority incidents are consistently slower** than High across every category except Network — the opposite of expected SLA behavior.
- Network is the exception: Critical (1,039 h) < High (1,082 h) < Moderate (1,211 h), suggesting Critical network issues do receive accelerated handling.
- Database Critical incidents take 1,244 h vs 910 h for High — a 37% increase, the widest intra-category priority gap.

---

## 5. TAPP Semantic Signal: Failure Symptom and Resolver Match

**`failure_symptom`** (TAPP) adds explanatory depth beyond structured category/priority:

| Failure Symptom | N (resolved) | Mean Hours |
|---|---|---|
| access_denied | 59 | 1,114 |
| outage_down | 80 | 1,104 |
| installation_failure | 10 | 1,072 |
| connection_failure | 187 | 1,014 |
| login_failure | 11 | 984 |
| crash | 6 | 830 |
| performance_degradation | 2 | 366 |

`access_denied` and `outage_down` symptoms are the slowest resolving — consistent with the slow VPN/email sub-types identified via `incident_category`. `connection_failure` (n=187, the modal symptom) sits at 1,014 h, near the overall mean.

**`resolver_match`** (True = incident was resolved by the originally assigned agent): resolver match (True, n=77 mean 1,031 h) vs. non-match (False, n=295 mean 1,047 h) shows virtually no difference (~16 h gap). This TAPP facet is **not a meaningful driver of resolution time** in this dataset.

**`assignment_lag_present`**: All 372 resolved records have `assignment_lag_present = True`, meaning this column has zero variance among resolved records and provides no discriminatory signal.

---

## Key Findings Summary

| Dimension | Fastest | Slowest | Key Observation |
|---|---|---|---|
| **Priority** | 2 - High (1,020 h) | 3 - Moderate (1,121 h) | Critical ≠ fast; priority does not govern resolution speed |
| **Category** | Database (955 h) | Hardware (1,105 h) | Network dominates volume at above-average time |
| **Assignment Group** | Database (947 h) | Service Desk (1,102 h) | Service Desk routing overhead notable |
| **TAPP: incident_category** | hardware/database (~926–947 h) | server/software_update (~1,166–1,178 h) | Semantic sub-type refines Category signal |
| **TAPP: failure_symptom** | performance_degradation (366 h) | access_denied/outage_down (~1,104–1,114 h) | Symptom type adds meaningful segmentation |

**Decision-ready takeaway:** Resolution time in this incident dataset is driven more by the *nature of the problem* (category, semantic sub-type, failure symptom) and *assignment group capacity* than by the formal priority label. Priority escalation is not accelerating closure, particularly for Critical tickets outside the Network group. Database incidents and the Database assignment group consistently outperform their peers. The ~25% open/unresolved rate is uniformly distributed across priority tiers, indicating no priority-based queue management is in effect.
