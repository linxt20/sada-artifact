---
dataset: flag_2
scenario: concept_attribute_delay
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "incident_delay_reasons"
query: "Why do some incidents take longer to resolve?"
source_table: augment_table/flag_2/concept_attribute_delay/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:16:33.285780+00:00
wall_seconds: 55.2
---

# Incident Resolution Delay Analysis

**Dataset:** `sonnet__skill_on_v11_update.csv` | 500 closed/resolved incidents + 17 not-yet-closed  
**Focus variable:** `open_to_close_days_bucket`

---

## Resolution Time Distribution

| Bucket | Count | Share |
|---|---|---|
| same_day | 62 | 12.4% |
| one_to_three_days | 30 | 6.0% |
| four_to_seven_days | 46 | 9.2% |
| eight_to_fourteen_days | 27 | 5.4% |
| **fifteen_plus_days** | **318** | **63.6%** |
| not_closed | 17 | 3.4% |

The distribution is heavily right-skewed: nearly two-thirds of incidents remain open for more than two weeks. The analysis below examines what distinguishes long-running incidents from same-day resolutions.

---

## Key Factors Driving Longer Resolution

### 1. Assignment Status at Opening (`assigned_at_open`) — Strongest Structural Signal

This is the sharpest discriminator in the dataset:

| assigned_at_open | same_day | 1–3 days | 4–7 days | 8–14 days | 15+ days |
|---|---|---|---|---|---|
| **False** | 51 (82%) | 0 | 0 | 0 | 0 |
| **True** | 11 (18%) | 30 | 46 | 27 | 318 |

Every incident resolved in **four or more days had been assigned at opening**; conversely, virtually all same-day closures were incidents **not yet formally assigned** at the moment they were opened. This counter-intuitive pattern likely reflects a workflow artifact: incidents quickly self-resolved or were auto-closed before formal assignment, while incidents that entered the assignment queue took on queuing and hand-off delays. Fourteen `not_closed` incidents also lack formal assignment, suggesting they are either pending or abandoned.

### 2. Failure Mode (`failure_mode`)

`connection_failure` is by far the most common mode across all buckets (63–83%), so it does not cleanly separate fast from slow resolutions. However, it constitutes **65% of 15+ day incidents** (207 of 318) and is the dominant mode in every bucket, indicating that connection failures are the core workload regardless of resolution speed.

More informative are rarer modes concentrated in long queues:
- `service_unresponsive`: 52 of its occurrences are in the 15+ day bucket vs. 7 same-day.
- `authentication_failure`: 11 of 14 total occurrences are in the 15+ day bucket (79%).
- `sync_failure` and `crash`: almost entirely 15+ days.

These failure types likely require deeper investigation or vendor involvement, extending timelines.

### 3. Scope (`scope_indicator`)

`system_wide` incidents make up 62% of the 15+ day bucket (197 of 318), compared to 55% of same-day closures. The difference is modest, suggesting scope alone is not decisive, but broadly impacting incidents — especially those marked `system_wide` paired with complex failure modes — tend to persist longer.

`remote_access` incidents (75 in 15+ days) are also disproportionately long-running, potentially due to distributed infrastructure complexity.

### 4. Category (`category`)

| Category | 15+ days share of its total |
|---|---|
| Network | 168 / ~220 = ~76% |
| Software | 60 / ~72 = ~83% |
| Database | 73 / ~92 = ~79% |
| Hardware | 11 / ~13 = ~85% |

All categories skew heavily toward the 15+ day bucket, which is consistent with `assigned_at_open=True` being an almost universal feature of long incidents. No single category stands out as uniquely problematic.

### 5. Priority (`priority`)

The 15+ day bucket contains a notably lower share of **1 - Critical** incidents (50/318 = 16%) compared to same-day (14/62 = 23%). This suggests critical incidents receive faster handling, as expected. However, the majority of long-running incidents are **2 - High** (242/318 = 76%), indicating that "high" priority incidents still accumulate in the queue without the urgency that drives immediate resolution.

### 6. Resolver Match (`resolver_match`)

The `resolver_match` rate for 15+ day incidents (20.8%) is slightly *higher* than for same-day (13.6%). This unexpected pattern weakens the hypothesis that resolver mismatches are a primary driver of delay. It may instead reflect that complex incidents requiring specialist skills are eventually matched to the right resolver, but only after prolonged triaging.

---

## Summary of Findings

| Factor | Direction of Effect | Strength |
|---|---|---|
| `assigned_at_open = False` → fast closure | Faster resolution | **Strong** |
| `failure_mode`: auth/sync/crash/service_unresponsive | Slower resolution | **Moderate** |
| `scope_indicator = system_wide` | Slightly slower | **Weak** |
| `priority = 1 - Critical` | Slightly faster | **Weak** |
| `resolver_match` | No clear effect | **Weak / contradictory** |

**Bottom line:** The dominant pattern is that incidents formally assigned at opening almost always take multiple days or weeks to close, while incidents not yet in the assignment queue at opening are resolved the same day. Beyond this workflow artifact, incidents involving authentication failures, sync issues, crashes, and service unresponsive modes take significantly longer, as do broadly-scoped (`system_wide`) incidents. High-priority (2 - High) incidents make up the bulk of long-running cases, suggesting priority escalation mechanisms for this tier may be insufficient.
