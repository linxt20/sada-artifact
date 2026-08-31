---
dataset: flag_12
scenario: concept_attribute_inefficiency
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "incident_inefficiency_reasons"
query: "What recurring issues drive resolution inefficiency?"
source_table: augment_table/flag_12/concept_attribute_inefficiency/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:14:06.531138+00:00
wall_seconds: 79.83
---

# Resolution Inefficiency Analysis
**Dataset:** 500 incidents | **Query:** What recurring issues drive resolution inefficiency?

---

## Method Note

**TAPP-generated columns used:** `failure_type`, `resolution_action_type`, `reassignment_indicator`, `self_resolution_indicator`, `scope_breadth`, `affected_asset_class`, `resolver_agent`.  
`incident_category` was largely redundant with the original `category` column and is not separately featured. All TAPP facets are cross-validated against original structured fields (`category`, `priority`, `assignment_group`, `opened_at`/`closed_at`).

---

## Outcome Variable: Resolution Time

Resolution time is computed from `opened_at` to `closed_at`. The distribution is wide and right-skewed:

| Stat | Hours |
|---|---|
| Minimum | 24.0 |
| Median | 173.2 |
| Mean | 178.4 |
| P75 (slow threshold) | 252.7 |
| Maximum | 514.0 |

Incidents exceeding **252.7 hours (P75)** are classified as *slow* (n = 125, 25%).

---

## Driver 1: Hardware Dominance and High-Friction Asset Classes

The dataset is **heavily skewed toward Hardware** (n = 406, 81%), so hardware inefficiency is the primary systemic driver overall.

Within Hardware, `affected_asset_class` reveals sharp variation:

| Asset Class | n | Mean Hours | Median Hours | Slow Rate |
|---|---|---|---|---|
| desktop_pc | 22 | **215.6** | 228.7 | High |
| storage_device | 13 | **212.9** | 208.2 | High |
| keyboard | 56 | 187.0 | 178.7 | — |
| printer | 203 | 183.8 | 181.6 | — |
| mouse | 14 | 173.8 | 163.5 | — |
| monitor | 71 | 173.3 | 145.6 | — |
| server | 14–15 | 144.8–146.2 | 163.6 | — |
| laptop | 5 | 108.8 | 112.6 | Low |

**Desktop PCs and storage devices** average ~2.9 extra days vs. laptops. Printers (n = 203, 41% of all incidents) anchor the mean at 183.8 h — a high-volume, moderate-friction class that contributes most to aggregate inefficiency purely through scale.

---

## Driver 2: Reassignment — Concentrated in Hardware Failures

The `reassignment_indicator` (13% of incidents, n = 65) is associated with a **+22-hour mean penalty** (197.2 h vs. 175.6 h) and a +37-hour median penalty (207.7 h vs. 170.3 h).

The penalty is concentrated in **hardware_failure + reassignment** combos:

| Reassignment | failure_type | n | Mean Hours |
|---|---|---|---|
| True | hardware_failure | 46 | **209.2** |
| True | connectivity_failure | 9 | 194.9 |
| False | hardware_failure | 337 | 178.2 |
| False | connectivity_failure | 40 | 170.6 |
| False | software_failure | 47 | 164.7 |

Reassigned hardware failures (n = 46) average **31 hours more** than non-reassigned hardware failures. Reassignment rates are highest in **Database** (21.1%) and **Inquiry/Help** (20.0%) categories, but those categories are small (n = 19–20); the absolute volume impact falls squarely on Hardware.

---

## Driver 3: Repair/Replacement Resolution Actions Are Slowest

The `resolution_action_type` reflects how incidents were resolved:

| Action Type | n | Mean Hours | Median Hours |
|---|---|---|---|
| replacement | 26 | **186.7** | 163.7 |
| repair | 368 | **182.0** | 181.5 |
| network_fix | 44 | 174.7 | 177.9 |
| investigation_only | 14 | 170.8 | 161.1 |
| software_update_applied | 38 | 154.2 | 150.0 |
| configuration_change | 10 | 143.9 | 176.1 |

**Repair and replacement** together account for 394 incidents (79%) and are the slowest categories. Software-based resolutions (`software_update_applied`, `configuration_change`) average 24–42 hours faster, indicating that physical intervention is the primary action-type bottleneck.

---

## Driver 4: Scope — Shared Equipment Delays Are Structural

`scope_breadth` shows that **shared_office_equipment** incidents are the slowest group:

| Scope | n | Mean Hours | Median Hours |
|---|---|---|---|
| shared_office_equipment | 197 | **184.8** | 181.6 |
| single_device | 205 | 178.2 | 165.8 |
| individual_user | 47 | 170.6 | 169.1 |
| infrastructure_wide | 44 | 165.5 | 175.5 |
| location_wide | 7 | 139.6 | 161.1 |

This aligns with printers and keyboards being the largest shared-equipment classes. When shared equipment is also reassigned, the scope × reassignment interaction compounds delay (`single_device` + reassigned: 202.8 h mean vs. 174.5 h without reassignment).

---

## Driver 5: Assignment Group — Service Desk Is a Chokepoint

The **Service Desk** group has the highest slow rate despite small volume:

| Assignment Group | n | Slow Rate |
|---|---|---|
| Service Desk | 19 | **31.6%** |
| Hardware | 405 | 25.9% |
| Software | 33 | 21.2% |
| Network | 23 | 17.4% |
| Database | 20 | 15.0% |

Service Desk's 31.6% slow rate, combined with a 20% reassignment rate in the Inquiry/Help category it handles, suggests it is a routing bottleneck rather than a resolution group.

---

## Driver 6: Self-Resolution Provides Modest but Consistent Benefit

Self-resolved incidents (`self_resolution_indicator = True`, n = 94) are **9 hours faster** on mean (171.1 h vs. 180.1 h) and resolve slightly faster at median (170.3 h vs. 174.9 h). The effect is real but modest — self-resolution is not a silver bullet for the hardware-dominated workload.

---

## Priority Anomaly: Critical Incidents Are Not Slowest

| Priority | n | Mean Hours |
|---|---|---|
| 2 - High | 394 | 180.0 |
| 3 - Moderate | 77 | 177.8 |
| 1 - Critical | 27 | **167.0** |
| 4 - Low | 2 | 32.6 |

Critical incidents resolve faster than High-priority ones, suggesting priority escalation does trigger faster handling. The **2 - High** priority band (79% of all incidents) is the true inefficiency mass — it contains most of the slow hardware + repair combinations.

---

## Summary: Recurring Inefficiency Drivers

| Rank | Driver | Evidence |
|---|---|---|
| 1 | **Hardware/repair workload dominance** | 81% of incidents; repair = 182 h mean; 26% slow rate |
| 2 | **Desktop PC & storage device asset classes** | 213–216 h mean; well above dataset average |
| 3 | **Reassigned hardware failures** | 209 h mean (+31 h vs. non-reassigned hardware) |
| 4 | **Shared office equipment scope** | 185 h mean; driven by high-volume printer incidents |
| 5 | **Service Desk routing bottleneck** | 31.6% slow rate; 20% reassignment |
| 6 | **Physical replacement actions** | 187 h mean vs. 154 h for software fixes |

The core pattern is a **hardware-centric workload requiring physical repair or replacement of shared equipment, with reassignment as an amplifier**. Reducing reassignments in hardware categories and accelerating desktop/storage device resolutions (through parts availability or specialist routing) would address the highest-frequency inefficiency modes.
