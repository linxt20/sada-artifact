---
dataset: flag_12
scenario: causal_improve
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "incident_resolution_efficiency"
query: "How can we improve incident resolution efficiency?"
source_table: augment_table/flag_12/causal_improve/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:12:41.311091+00:00
wall_seconds: 68.28
---

# Incident Resolution Efficiency Analysis

## Dataset Overview

The dataset contains **500 incidents** spanning 2023, predominantly Hardware category (81%), with a mix of Software, Network, Database, and Inquiry/Help tickets. Mean resolution time is approximately **179 hours (~7.5 days)** across all incidents.

---

## Key Findings

### 1. Reassignment + Repeat Incident Signal Are the Strongest Combined Drag on Resolution Time

| Reassignment | Repeat Incident | Mean Resolution (hrs) | Count |
|---|---|---|---|
| No | No | 172.2 | 197 |
| No | Yes | 180.4 | 159 |
| Yes | No | 174.2 | 74 |
| Yes | Yes | **195.9** | 70 |

Incidents flagged for **both reassignment and repeat signal** take ~24 hours (~14%) longer than those with neither flag. This is the clearest actionable pattern in the data.

**Recommendation:** Prioritize reducing reassignments for tickets already flagged as repeat incidents. This likely reflects routing failures for known recurring issues that should have established owners or playbooks.

---

### 2. Resolution Action Type Significantly Affects Duration

| Resolution Action | Mean Hours | Count |
|---|---|---|
| investigation | 159.9 | 11 |
| software_install_update | 161.4 | 48 |
| connectivity_fix | 173.7 | 47 |
| repair_maintenance | **181.8** | 369 |
| replacement | 183.6 | 22 |

`repair_maintenance` dominates (74% of tickets) and is consistently slower than `software_install_update` or `connectivity_fix`. Hardware repair queues or parts availability may be the bottleneck. Accelerating hardware maintenance workflows (e.g., pre-positioned spare parts, faster vendor SLAs) offers the highest aggregate impact given the volume.

---

### 3. Priority Escalation Is Not Working Optimally

| Priority | Mean Resolution (hrs) | Count |
|---|---|---|
| 1 - Critical | **167.0** | 27 |
| 2 - High | 180.0 | 394 |
| 3 - Moderate | 177.8 | 77 |

Critical incidents resolve ~13 hours faster than High, which is a modest advantage for the severity level. However, the difference is not dramatic, suggesting priority-based SLA enforcement may be inconsistent. High-priority incidents (79% of all tickets) should be reviewed for over-classification, which dilutes escalation effectiveness.

---

### 4. Software and Network Categories Resolve Faster

| Category | Mean Resolution (hrs) |
|---|---|
| Software | 153.6 |
| Network | 161.6 |
| Database | 172.4 |
| Hardware | **181.4** |
| Inquiry / Help | 182.1 |

Software and Network incidents resolve roughly **1–2 days faster** than Hardware. This pattern aligns with the repair_maintenance action type lag noted above.

---

### 5. Repeat Incident Signal Indicates Process Gaps

**46% of incidents** carry a `repeat_incident_signal=True`, meaning nearly half the ticket volume is recurring. These incidents average **185 hours** vs. **173 hours** for non-repeat incidents — a 12-hour penalty. Addressing root causes (e.g., printer fleet maintenance, keyboard/monitor lifecycle management) could significantly reduce total ticket volume and average resolution time simultaneously.

---

## Caveats and Weak Evidence

- **`repeat_caller_flag`** is `True` for all 500 records, making it non-discriminating in this dataset — it cannot be used to segment behavior.
- The **critical priority** sample is small (n=27), so the faster resolution observed may not be statistically robust.
- **`failure_symptom_severity`** shows very little differentiation in resolution time (partial vs. total failure differ by < 1 hour), suggesting it does not drive resolution speed in practice.
- The `Unknown` resolution action type (n=2) resolves fastest at 115 hours but is too rare to draw conclusions from.

---

## Summary Recommendations

| Action | Expected Impact | Evidence Strength |
|---|---|---|
| Reduce reassignments on repeat incidents | −24 hrs avg resolution | Strong (n=70 vs 197 baseline) |
| Accelerate hardware repair_maintenance workflows | High aggregate impact (74% of volume) | Strong |
| Root-cause recurrent incidents (46% repeat rate) | Volume reduction + time savings | Moderate–Strong |
| Tighten priority 1 vs 2 classification criteria | Better SLA differentiation | Moderate |
