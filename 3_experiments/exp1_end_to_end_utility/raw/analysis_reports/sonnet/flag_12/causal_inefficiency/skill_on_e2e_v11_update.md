---
dataset: flag_12
scenario: causal_inefficiency
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "resolution_efficiency"
query: "Why are some incidents resolved inefficiently, and which underlying issues drive it?"
source_table: augment_table/flag_12/causal_inefficiency/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:14:22.016194+00:00
wall_seconds: 100.7
---

# Causal Inefficiency in Incident Resolution: Analysis Report

**Dataset:** 500 incidents | **Period:** Jan 2023 onward | **Outcome metric:** Resolution time (hours from `opened_at` to `closed_at`)

---

## Method Note

TAPP-generated columns used in this report: `incident_category`, `issue_subtype`, `affected_asset_type`, `hardware_vs_software`, `reassignment_indicator`, `action_type`, `resolver_workload_proxy`, `urgency_signal`. The columns `resolver_workload_proxy` and `action_type` showed weak or redundant signal and are noted accordingly.

---

## 1. Defining Inefficiency

Resolution time ranges from 24 h to 514 h (mean 178 h, median 173 h). Incidents above the 75th-percentile threshold of **≥253 hours** are classified as inefficient (125 of 500, **25%**). This is the primary outcome variable; the analysis traces back its structural and semantic drivers.

---

## 2. Primary Driver: Hardware Category Dominance + Reassignment

### 2.1 Category-level resolution time

| Category | Mean (h) | Median (h) | n | Reassignment rate |
|---|---|---|---|---|
| Inquiry / Help | 182 | 183 | 20 | 20.0% |
| **Hardware** | **181** | **175** | **406** | **12.8%** |
| Database | 172 | 178 | 19 | 10.5% |
| Network | 162 | 186 | 22 | 13.6% |
| Software | 154 | 148 | 33 | 15.2% |

Hardware incidents make up **81% of the dataset** (406/500). Their above-average mean resolution time (181 h vs. overall 178 h) and volume combine to dominate total inefficiency. Software incidents resolve ~27 h faster on average.

### 2.2 Reassignment is the clearest structural driver

Reassigned incidents take **195 h** on average vs. **176 h** for non-reassigned — a **+19 h (11%) penalty** — with a higher inefficiency rate (reassigned: insufficient data label, see table below).

| Reassignment | Mean (h) | Median (h) | Inefficiency rate | n |
|---|---|---|---|---|
| No | 176 | 169 | 24.4% | 434 |
| **Yes** | **195** | **207** | **31.8%** | **66** |

The effect is strongest in **Hardware** (178 h → 203 h, +25 h) and **Network** (156 h → 195 h, +39 h). In Software, reassignment does *not* increase time (159 h → 125 h), suggesting that software reassignments often move tickets to more capable resolvers.

### 2.3 TAPP `incident_category` refines the Hardware story

Within Hardware, TAPP's `incident_category` reveals which sub-types are worst:

| incident_category | Mean (h) | Inefficiency rate | Reassignment rate | n |
|---|---|---|---|---|
| **workstation_hardware** | **198** | **35%** | **29%** | 51 |
| printer_hardware | 184 | 28% | 14% | 203 |
| peripheral_device | 176 | 26% | 4% | 134 |
| network_connectivity | 171 | 18% | 10% | 42 |
| software_application | 162 | 26% | 17% | 52 |
| server_infrastructure | 145 | 11% | 17% | 18 |

`workstation_hardware` is the most inefficient segment: highest mean time, highest inefficiency rate, and highest reassignment rate (29%). Printer hardware accounts for the most *volume* of inefficiency (203 incidents × 28% = ~57 inefficient incidents).

---

## 3. Secondary Driver: Affected Asset Type

TAPP's `affected_asset_type` shows that **storage devices and workstation/desktop endpoints** are the most time-consuming assets:

| affected_asset_type | Mean (h) | n |
|---|---|---|
| workstation_desktop | 221 | 21 |
| storage_device | 213 | 13 |
| keyboard_mouse | 184 | 70 |
| printer | 184 | 203 |
| monitor | 173 | 71 |
| software_application | 166 | 67 |
| network_device | 163 | 25 |
| server | 148 | 16 |
| laptop | 109 | 5 |

Workstation desktops and storage devices resolve ~35–48 h slower than the fleet mean — likely due to parts availability, diagnostic complexity, or specialist scarcity.

---

## 4. `issue_subtype`: Diagnostic Complexity Adds Time

| issue_subtype | Mean (h) | n |
|---|---|---|
| performance_degradation | 198 | 8 |
| hardware_failure | 183 | 57 |
| device_not_responding | 182 | 315 |
| connectivity_failure | 171 | 45 |
| software_crash | 166 | 27 |
| installation_request | 157 | 22 |

`device_not_responding` (315 cases, 63% of dataset) is the dominant subtype. Its mean (182 h) closely tracks overall hardware, confirming it as the modal inefficiency driver. `performance_degradation` has the highest mean but very small sample (n=8).

---

## 5. Priority Inversion

Critical incidents (priority 1) resolve faster (167 h) than High (180 h) and Moderate (178 h), suggesting escalation procedures are effective for Critical tickets. The inefficiency problem is concentrated in **Priority 2 – High**, which represents 79% of all incidents (394/500) and carries a 25% inefficiency rate. Reassignment within Priority 2 raises mean time from 177 h to 200 h.

---

## 6. TAPP Facets: Weak or Redundant Signal

- **`resolver_workload_proxy`**: Largely mirrors `reassignment_indicator` (all `reassigned_resolver` events = the 394 records where reassignment occurred at least once; `sole_resolver` = 106 non-reassigned). Adds no independent signal.
- **`action_type`**: `repair` dominates (369/500); all other types have small n. The single `maintenance` incident is an outlier (307 h, n=1). No actionable differentiation beyond confirming repair-heavy workload.
- **`urgency_signal`**: `standard` tickets (394 cases) have 27% inefficiency rate vs. 20% for `disruption_reported` and 9% for `immediate_attention` — but this largely tracks priority, offering limited additional explanatory power.
- **`hardware_vs_software`**: Hardware (396 cases, mean 181 h) vs. Software (56 cases, mean 163 h) confirms the category finding without added precision.

---

## 7. Resolver-Level Heterogeneity

| Assigned To | Mean (h) | n |
|---|---|---|
| Luke Wilson | 196 | 116 |
| Charlie Whitherspoon | 179 | 103 |
| Howard Johnson | 175 | 106 |
| Beth Anglin | 172 | 85 |
| Fred Luddy | 165 | 90 |

Luke Wilson's 116-incident load resolves ~31 h slower than Fred Luddy's 90-incident load, suggesting either workload concentration on difficult ticket types or a skill/capacity gap.

---

## 8. Root-Cause Summary

| Underlying Issue | Evidence | Magnitude |
|---|---|---|
| **Hardware volume concentration** | 81% of tickets are Hardware; mean 181 h vs. 154 h for Software | Primary structural driver |
| **Reassignment** | +19 h mean penalty; 29% rate in workstation_hardware | +11% resolution time |
| **Workstation/desktop & storage device complexity** | Mean 213–221 h for these asset types | +35–48 h above mean |
| **Printer volume** | 203 printer incidents at 184 h = largest inefficiency pool | ~57 inefficient incidents |
| **Priority 2 High concentration** | 394/500 tickets; no fast-track escalation benefit | Modal inefficiency band |
| **Resolver concentration** | Luke Wilson handles 23% of load at highest mean time | Workload/skill imbalance |

**Bottom line:** Inefficient resolution is primarily structural — a high-volume hardware queue dominated by printer and workstation incidents routed through a small resolver pool. Reassignment compounds delays by 19 h on average, most severely in workstation and network tickets. Fixing intake routing (reduce misrouted hardware tickets) and reducing reassignment in workstation_hardware (29% rate) represent the highest-leverage interventions.
