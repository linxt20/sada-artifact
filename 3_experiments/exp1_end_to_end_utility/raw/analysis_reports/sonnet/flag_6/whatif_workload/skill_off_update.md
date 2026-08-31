---
dataset: flag_6
scenario: whatif_workload
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "resolution_time"
query: "If the ticket types that create the heaviest agent workload were reduced, how much would resolution time drop?"
source_table: augment_table/flag_6/whatif_workload/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:22:01.238583+00:00
wall_seconds: 42.43
---

# What-If Analysis: Reducing High-Workload Ticket Types and Resolution Time Impact

## Dataset Overview

| Metric | Value |
|---|---|
| Total tickets | 500 |
| Categories | 5 (Network, Database, Software, Hardware, Inquiry/Help) |
| Focus variable | `counterfactual_resolution_hours` |

---

## Identifying the Heaviest Workload Category

The dataset ranks categories by agent workload (`category_workload_rank`). **Network** tickets hold **Rank 1** (highest workload) and are the only category flagged as `is_high_workload_category = 1`.

| Category | Workload Rank | High Workload? | Ticket Count | Share | Avg Resolution (hrs) |
|---|---|---|---|---|---|
| **Network** | 1 | ✅ Yes | 284 | 56.8% | 230.56 |
| Database | 2 | No | 109 | 21.8% | 204.18 |
| Software | 3 | No | 72 | 14.4% | 248.06 |
| Hardware | 4 | No | 26 | 5.2% | 187.26 |
| Inquiry / Help | 5 | No | 9 | 1.8% | 134.92 |

Network is both the dominant category by volume (56.8% of all tickets) and above average in resolution time.

---

## Counterfactual Resolution Time Impact

The `counterfactual_resolution_hours` column encodes a scenario where high-workload tickets (Network) are handled under reduced-load conditions (approximated to the next-tier category average of **214.22 hrs**).

| Scope | Actual Avg (hrs) | Counterfactual Avg (hrs) | Drop (hrs) | Drop (%) |
|---|---|---|---|---|
| **Network tickets only** | 230.56 | 214.22 | **−16.34** | **−7.1%** |
| **All tickets (portfolio)** | 223.48 | 214.22 | **−9.26** | **−4.1%** |

- Non-Network categories are **unaffected** — their counterfactual equals their actual resolution hours.
- The portfolio-wide drop (~9.3 hrs / 4.1%) is diluted by the large number of non-Network tickets.

---

## Key Findings

1. **Network is the sole high-workload driver.** Reducing Network ticket volume or agent load is projected to cut per-ticket resolution time by ~16 hours (7.1%).
2. **Portfolio-wide benefit is meaningful but moderate (~4%).** Because non-Network categories already resolve faster on average, the absolute gain across all tickets is ~9 hours.
3. **No counterfactual benefit exists for lower-ranked categories.** Database (Rank 2) averages 204 hrs but is not flagged as high-workload, so it receives no reduction modelling — a potential gap if workload thresholds are revised.

---

## Caveats & Weak Evidence

- The counterfactual applies a **flat uniform reduction** (to 214.22 hrs) for all Network tickets, regardless of individual complexity or priority — real outcomes would vary.
- A small number of Network tickets already show **negative resolution hours** (data quality issue, e.g. INC0000000003: −4.3 hrs), suggesting timestamp anomalies that may slightly inflate the baseline mean.
- The analysis is limited to a **single workload tier** (Network). If Database or Software ticket volume grows, they could become future high-workload categories not captured here.

---

## Decision Summary

> Reducing Network ticket load (the heaviest workload category at 56.8% of volume) is projected to lower average resolution time by approximately **16 hours per Network ticket (7%)** and **9 hours across the full portfolio (4%)**. The effect is real but bounded — non-Network categories see no benefit under the current model, and actual gains will depend on how workload reduction is operationalized (e.g., better routing, added agents, or demand reduction).
