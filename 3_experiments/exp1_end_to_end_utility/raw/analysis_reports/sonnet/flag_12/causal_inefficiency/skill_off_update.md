---
dataset: flag_12
scenario: causal_inefficiency
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "resolution_efficiency"
query: "Why are some incidents resolved inefficiently, and which underlying issues drive it?"
source_table: augment_table/flag_12/causal_inefficiency/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:09:40.614328+00:00
wall_seconds: 55.01
---

# Incident Resolution Inefficiency Analysis

## Dataset Overview

- **500 incidents** across categories: Hardware, Software, Network, Database, Inquiry/Help
- **125 incidents (25%)** flagged as inefficient (`inefficiency_flag = 1`)
- Inefficient incidents average **319 hours** to resolve vs. **132 hours** for efficient ones (a ~2.4× gap)
- Average resolution delay for inefficient incidents: **+144 hours** over SLA; efficient incidents run **−44 hours** under SLA

---

## Key Inefficiency Drivers

### 1. Exceeding Expected Resolution Time (`above_expected_by_X%`)
This is the **primary discriminating factor**. All 125 flagged incidents include an `above_expected` tag in their driver string. The overrun magnitudes range from a few percent to over 200%:
- Extreme outliers include delays of **+221%**, **+205%**, **+193%**, and **+183%** over expected SLA.
- Among the 125 inefficient cases, the majority pair `reassigned` with `above_expected` — confirming that exceeding the SLA threshold, not reassignment alone, triggers the flag.

### 2. Reassignment (`reassigned`)
Reassignment is the most **prevalent** driver tag, appearing in **394 out of 500 incidents** (79%), yet it alone does not determine inefficiency. Incidents marked `reassigned` only (no `above_expected` tag) average **−83 hours** against SLA — meaning many reassigned tickets are still resolved on time. However, when reassignment co-occurs with SLA overrun, it amplifies delay:
- Nearly all flagged inefficient incidents with reassignment also carry an `above_expected` tag.
- The combination `reassigned|above_expected_by_61pct` is the single most common inefficient driver pattern (5 incidents).

### 3. Low Priority Deprioritization (`low_priority`)
79 incidents carry a `low_priority` tag, largely corresponding to **3 - Moderate** priority (77 of 79). Of these, **20 become inefficient** (~25% inefficiency rate). These incidents tend to have positive resolution delays (avg **+16 hours**), suggesting lower-urgency tickets slip past SLA thresholds due to resource attention being directed elsewhere. The driver often appears in combination: `reassigned|low_priority|above_expected_by_X%`.

---

## Inefficiency by Category

| Category | Inefficiency Rate | Avg Resolution (hrs) |
|---|---|---|
| Software | 30.3% | 154 |
| Network | 27.3% | 162 |
| Hardware | 25.4% | 181 |
| Inquiry/Help | 20.0% | 182 |
| Database | 10.5% | 172 |

**Software** has the highest inefficiency rate despite shorter average resolution times — indicating that SLA expectations for Software tickets are tighter, making overruns more likely. **Database** incidents are the least likely to be flagged inefficient, suggesting more realistic SLA targets or more specialized handling.

---

## Inefficiency by Assigned Agent

| Agent | Incidents | Inefficiency Rate | Avg Resolution (hrs) |
|---|---|---|---|
| Howard Johnson | 106 | 30.2% | 175 |
| Luke Wilson | 116 | 29.3% | 196 |
| Charlie Whitherspoon | 103 | 25.2% | 179 |
| Beth Anglin | 85 | 20.0% | 172 |
| Fred Luddy | 90 | 17.8% | 165 |

**Howard Johnson** and **Luke Wilson** show notably higher inefficiency rates and, in Luke Wilson's case, the highest average resolution time (196 hours). This may point to workload, skill mismatch, or ticket complexity concentration — though the dataset does not directly record agent skill level. Fred Luddy has both the lowest inefficiency rate and lowest average resolution time.

---

## Priority and Inefficiency

| Priority | Inefficiency Rate |
|---|---|
| 3 - Moderate | 26.0% |
| 2 - High | 25.4% |
| 1 - Critical | 18.5% |
| 4 - Low | 0.0% |

Critical incidents are resolved relatively more efficiently, likely due to escalation urgency. Moderate-priority tickets are flagged most often, consistent with the `low_priority` deprioritization pattern.

---

## Summary of Root Causes

| Driver | Role in Inefficiency |
|---|---|
| **SLA overrun** (`above_expected`) | Necessary condition — all 125 flagged incidents include this |
| **Reassignment** | Ubiquitous (79% of all tickets), but only harmful when paired with SLA overrun |
| **Low priority / deprioritization** | Contributes to ~16% of flagged cases, mainly Moderate-priority tickets |
| **Agent workload/skill** | Howard Johnson and Luke Wilson show elevated rates; weak evidence without skill data |
| **Category mismatch** | Software and Network have tighter SLAs relative to actual resolution patterns |

---

## Exceptions and Caveats

- **Reassignment alone does not cause inefficiency**: 168 reassigned-only incidents averaged 83 hours *under* SLA.
- **The `skill_off` variant label** suggests agent skill information has been suppressed in this dataset. Agent-level differences in inefficiency rates are visible but cannot be attributed to documented skill mismatches without that column.
- Priority 4 - Low incidents show 0% inefficiency, but the sample is very small (n=2).
- Hardware dominates the dataset (~70% of tickets), which limits cross-category generalization.
