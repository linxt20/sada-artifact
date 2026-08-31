---
dataset: flag_12
scenario: concept_attribute_inefficiency
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "incident_inefficiency_reasons"
query: "What recurring issues drive resolution inefficiency?"
source_table: augment_table/flag_12/concept_attribute_inefficiency/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:13:40.328362+00:00
wall_seconds: 57.09
---

# Resolution Inefficiency Analysis
**Dataset:** `sonnet__skill_on_v11_update.csv` | 500 incidents | Focus variable: `skill_on`

---

## Executive Summary

Resolution inefficiency is driven by a concentrated cluster of hardware-centric, physically-bound, and recurrence-prone incidents. The overall mean resolution time is **178.4 hours (~7.4 days)**, with a wide spread (std ≈ 109 h, max ≈ 514 h), suggesting systemic — not random — bottlenecks.

---

## Key Drivers of Resolution Inefficiency

### 1. Hardware Dominance + Mandatory Physical Intervention

- **81.2% of all incidents** are categorized as `Hardware`; 100% of Hardware incidents require physical intervention (`requires_physical_intervention = True`).
- Hardware has the **second-highest mean resolution time** (181.4 h), just behind Inquiry/Help (182.1 h).
- The dominant failure mode `not_responding` (256 incidents, 51%) is almost entirely hardware-based (253/256), averaging **185.4 h** — the single highest failure mode.
- `physical_damage` (54 incidents, 184.3 h) and `flickering_display` (22 incidents, 181.8 h) compound the backlog.

Physical intervention creates a hard scheduling dependency (technician dispatch, parts availability) that inflates cycle time regardless of urgency.

### 2. Recurrence Signal — Chronic, Unresolved Root Causes

- **92.6% of all incidents** carry `recurrence_signal = True`, indicating repeat patterns rather than isolated events.
- Hardware incidents have the highest recurrence rate (**95.6%**), followed by Network (90.9%) and Software (87.9%).
- Incidents that are *both* physical-intervention-required *and* recurring (392 incidents — **78.4% of the dataset**) average **181.9 h**, the dominant slow path.
- The near-universal recurrence signal strongly suggests root causes are not being eliminated at resolution — patch-and-repeat cycles inflate total organizational workload.

### 3. `not_responding` Failure Mode as a Structural Bottleneck

- `not_responding` is the largest single failure mode (256 cases, 51.2%) and the slowest (185.4 h avg).
- This mode almost exclusively maps to hardware + physical intervention — the two factors most resistant to remote or scripted resolution.
- It accounts for disproportionate queue load and likely competes for the same limited technician bandwidth as `physical_damage` cases.

### 4. Priority Inversion: High Priority ≠ Faster Resolution

- `1 - Critical` incidents resolve in **167.0 h** on average — *faster* than `2 - High` (180.0 h) and `3 - Moderate` (177.8 h).
- This suggests the bulk-category (`2 - High`, 394/500 incidents) lacks sufficient differentiation to trigger expedited handling, effectively nullifying priority triage for most of the queue.

### 5. Urgency Signal Misalignment

- `standard` urgency tickets (400/500, 80%) take the **longest** to resolve (180.2 h), while `immediate_attention` tickets resolve faster (172.2 h).
- Most hardware/not_responding incidents are classified as `standard` urgency despite high recurrence — this mismatch delays escalation.

---

## Supporting Patterns

| Factor | Avg Resolution (h) | Count | % of Total |
|---|---|---|---|
| `not_responding` + physical | 185.4 | 256 | 51.2% |
| `physical_damage` + physical | 184.3 | 54 | 10.8% |
| Recurrent + physical (combined) | 181.9 | 392 | 78.4% |
| Software (no physical required) | 153.6 | 33 | 6.6% |
| Non-recurrent + no physical | 194.0 | 18 | 3.6%* |

*\*Non-recurrent, non-physical cases (n=18) show the highest avg due to small sample — weak evidence, interpret cautiously.*

---

## Exceptions and Weak Evidence

- **`self_resolved_by_assignee`** shows minimal impact on resolution time (174.8 h vs 179.4 h), suggesting this pathway does not meaningfully accelerate closure.
- **Paper jams** (4 incidents) resolve fastest (141.9 h) but are too rare to influence aggregate metrics.
- **Non-recurrent incidents without physical intervention** (n=18) appear slowest (194 h), but the small sample makes this unreliable — likely noise or edge-case incidents.
- Network and Software, despite lower recurrence rates, still show high recurrence (91% and 88%) — root cause elimination is a system-wide, not category-specific, problem.

---

## Decision-Ready Conclusions

1. **Reduce physical dispatch dependency**: The not_responding + physical_intervention combination drives half the queue. Remote diagnostics, pre-positioned spare hardware, or self-service hardware swap programs could cut cycle time.
2. **Break the recurrence loop**: 93% recurrence signals unresolved root causes. Post-incident root cause analysis and permanent fix tracking should be mandated for Hardware incidents.
3. **Re-tier the priority model**: `2 - High` is effectively a catch-all. Sub-segmenting by physical requirement or recurrence history would enable smarter queue prioritization.
4. **Align urgency classification**: Physical + recurrent incidents classified as `standard` urgency are systematically under-prioritized relative to their actual resolution drag.
