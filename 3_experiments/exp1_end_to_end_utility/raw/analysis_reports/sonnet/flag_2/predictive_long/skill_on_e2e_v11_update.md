---
dataset: flag_2
scenario: predictive_long
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "resolution_time"
query: "What signals suggest an incident will take longer to resolve?"
source_table: augment_table/flag_2/predictive_long/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:17:22.978109+00:00
wall_seconds: 65.73
---

# Signals That Predict Longer Incident Resolution Time

**Query:** What signals suggest an incident will take longer to resolve?  
**Dataset:** 500 incidents (372 with computed resolution times; 128 open/in-progress at data export)  
**Outcome variable:** Resolution time in hours = `closed_at − opened_at`

---

## Method Note

TAPP-generated columns used in this analysis: `incident_category`, `problem_symptom_type`, `opened_hour_of_day`, `is_unassigned_at_open`, `assignee_resolver_match`, `is_recurring_issue_type`. The column `is_unassigned_at_open` was uniformly `False` across all 372 resolved records and contributed no signal. `assignee_resolver_match` and `is_recurring_issue_type` showed negligible effect (see §5). All material claims are cross-checked against original structured columns (`priority`, `category`, `assignment_group`, `assigned_to`).

---

## 1. Baseline

| Statistic | Hours |
|-----------|-------|
| Mean | 1,043 |
| Median | 1,032 |
| P25 | 505 |
| P75 | 1,558 |
| Max | 2,206 |

Resolution times are broadly distributed with a range of ~24 h to ~2,206 h (≈92 days), indicating high variance. Incidents still in "New" or "In Progress" state (n = 128, 25.6%) are right-censored and excluded from time calculations but represent a meaningful backlog.

---

## 2. Assignment Group and Assignee (Strongest Structural Predictors)

**Assignment group** is the single strongest original structured predictor:

| Assignment Group | Mean Hours | Median Hours | N |
|------------------|-----------|-------------|---|
| Service Desk | **1,102** | 1,129 | 32 |
| Network | **1,074** | 1,046 | 221 |
| Software | 1,028 | 823 | 25 |
| Database | 947 | 960 | 89 |
| Hardware | 926 | 794 | 4 |

Network group handles the most volume (221 / 372 = 59%) and resolves ~130 h slower than Database and ~150 h slower than Hardware on median.

**Individual assignee** also matters:

| Assignee | Mean Hours | Median Hours | N |
|----------|-----------|-------------|---|
| Beth Anglin | **1,142** | 1,298 | 73 |
| Fred Luddy | **1,125** | 1,100 | 74 |
| Charlie Whitherspoon | 1,036 | 1,061 | 71 |
| Luke Wilson | 967 | 816 | 85 |
| Howard Johnson | 953 | 910 | 69 |

Incidents routed to Beth Anglin or Fred Luddy resolve ~190–390 h slower (median) than those routed to Luke Wilson or Howard Johnson.

---

## 3. Incident Category and Problem Symptom Type (TAPP Semantic Signal)

**`incident_category`** (TAPP) adds semantic granularity beyond the original `category` column:

| incident_category | Mean Hours | Median Hours | N |
|-------------------|-----------|-------------|---|
| server | **1,178** | 1,162 | 20 |
| software_update | **1,166** | 956 | 12 |
| vpn | **1,102** | 1,100 | 80 |
| auth | **1,096** | 1,061 | 11 |
| email | **1,089** | 1,104 | 103 |
| network | 948 | 895 | 53 |
| database | 946 | 960 | 89 |
| hardware_peripheral | 926 | 794 | 4 |

Server issues, software updates, VPN, and email incidents resolve ~150–230 h slower (mean) than database or hardware peripheral issues. This is not captured by the original `category` field alone (which only distinguishes Network / Software / Database / Hardware).

**`problem_symptom_type`** (TAPP) reveals the outage symptom as a strong elongation driver:

| problem_symptom_type | Mean Hours | Median Hours | N |
|----------------------|-----------|-------------|---|
| restore_request | **1,612** | 1,612 | 2 |
| outage | **1,126** | 1,126 | 86 |
| cannot_connect | 1,034 | 1,025 | 243 |
| other | 1,017 | 888 | 7 |
| login_failure | 984 | 910 | 11 |
| update_failure | 971 | 658 | 7 |
| crash | 830 | 722 | 6 |
| sync_failure | 806 | 679 | 8 |

Outage-type incidents (n = 86) resolve ~90 h slower in mean than the baseline and ~100 h slower than connectivity issues. Within the Network category, outage incidents average 1,118 h vs. 1,074 h overall for Network — confirming the effect. Restore requests are slowest but very rare (n = 2).

---

## 4. Off-Hours Opening Time (`opened_hour_of_day`)

| Opened | Mean Hours | Median Hours | N |
|--------|-----------|-------------|---|
| off_hours | **1,097** | 1,104 | 132 |
| business_hours | 1,014 | 910 | 240 |

Incidents opened **off-hours** resolve ~83 h slower in mean and ~194 h slower in median than business-hours incidents. The effect persists within the Critical priority tier (off-hours Critical: 1,154 h vs. business-hours Critical: 1,095 h) and within High priority (off-hours: 1,098 h vs. business-hours: 977 h).

---

## 5. Priority (Weak or Counterintuitive Signal)

| Priority | Mean Hours | Median Hours | N |
|----------|-----------|-------------|---|
| 1 - Critical | 1,119 | 1,255 | 57 |
| 3 - Moderate | 1,121 | 1,100 | 32 |
| 2 - High | 1,019 | 974 | 283 |

Critical incidents resolve **longer** than High priority on median (+281 h), suggesting that high-severity tickets are not being fast-tracked or may involve more complex, systemic issues. Priority is not a reliable short predictor of fast resolution in this dataset.

---

## 6. Weak or Null TAPP Signals

| TAPP Column | Observation |
|-------------|-------------|
| `is_unassigned_at_open` | All resolved records = `False`; no variance, no predictive power |
| `assignee_resolver_match` | Match=True: 1,055 h vs. Match=False: 1,041 h — negligible 14 h difference |
| `is_recurring_issue_type` | Non-recurring: 1,090 h vs. Recurring: 1,039 h — slight but weak, 51 h difference |

---

## 7. Combined Risk Profile

An incident is likely to take **longer to resolve** when it exhibits several of the following signals:

| Signal | Type | Effect (mean hours above baseline) |
|--------|------|-------------------------------------|
| Assigned to Beth Anglin or Fred Luddy | Original (`assigned_to`) | +100 to +200 h |
| Assigned to Network or Service Desk group | Original (`assignment_group`) | +100 to +150 h |
| `incident_category` = server or software_update | TAPP | +120 to +135 h |
| `problem_symptom_type` = outage | TAPP | +82 h |
| `opened_hour_of_day` = off_hours | TAPP | +83 h (mean), +194 h (median) |
| `incident_category` = vpn or email | TAPP | +45 to +60 h |
| Priority = Critical | Original (`priority`) | +100 h median vs. High |

The highest-risk combination is: **Network/Service Desk group + off-hours opening + outage or VPN/email symptom + assigned to Beth Anglin or Fred Luddy**, which could collectively predict resolution times well above the 1,558 h (P75) threshold.
