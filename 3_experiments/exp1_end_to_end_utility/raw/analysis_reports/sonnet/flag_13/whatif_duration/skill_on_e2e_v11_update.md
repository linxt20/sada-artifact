---
dataset: flag_13
scenario: whatif_duration
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: what_if
focus_variable: "resolution_duration"
query: "If the most common operational burdens described in the text were eliminated, how much would resolution duration drop?"
source_table: augment_table/flag_13/whatif_duration/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:16:09.009415+00:00
wall_seconds: 118.06
---

# What-If Analysis: Eliminating Common Operational Burdens and Resolution Duration Impact

## Summary

The dataset contains 500 closed/resolved incidents. The outcome variable — resolution duration — is stored in `sys_updated_on` (which holds elapsed time in `MM:SS.s` format, re-expressed below in minutes).

| Statistic | Value |
|-----------|-------|
| N | 500 |
| Mean duration | 1,803 min (~30.1 h) |
| Median duration | 1,791 min (~29.8 h) |
| Std dev | ~1,011 min |

---

## Identifying the Most Common Operational Burdens

Two analytical dimensions surface the dominant operational burdens: the TAPP-generated `failure_type` column (semantic classification of what went wrong) and `scope_indicator` (how widely the incident affected users). Original structured columns (`category`, `priority`, `assignment_group`) corroborate these patterns.

### Burden 1 — Connectivity Failures (`failure_type = connectivity_failure`)

Connectivity failures are by far the most prevalent failure type: **228 of 500 incidents (45.6%)**. They map primarily to `category = Network` and `incident_category` values of `network_connectivity` and `vpn_access`.

| failure_type | Count | Share | Mean duration (min) | Excess vs. overall |
|---|---|---|---|---|
| **connectivity_failure** | **228** | **45.6%** | **1,878** | **+75 min** |
| access_denial | 118 | 23.6% | 1,789 | −14 min |
| outage | 88 | 17.6% | 1,723 | −80 min |
| Unknown | 27 | 5.4% | 1,652 | −151 min |
| performance_degradation | 16 | 3.2% | 1,364 | −439 min |
| sync_failure | 12 | 2.4% | 1,947 | +144 min |
| installation_failure | 11 | 2.2% | 1,893 | +90 min |

Connectivity failures take ~75 min longer per incident than the overall mean. The `network_connectivity` incident sub-category (n=80) averages 1,916 min — the highest of any `incident_category`.

### Burden 2 — Location-Specific Scope (`scope_indicator = location_specific`)

Location-specific incidents — those affecting a particular physical site rather than an individual or a whole system — carry a large per-incident penalty:

| scope_indicator | Count | Share | Mean duration (min) | Excess vs. overall |
|---|---|---|---|---|
| individual | 268 | 53.6% | 1,771 | −32 min |
| system_wide | 195 | 39.0% | 1,791 | −12 min |
| **location_specific** | **37** | **7.4%** | **2,100** | **+297 min** |

At +297 min (+5.0 h), location-specific incidents carry the steepest per-incident overhead, consistent with on-site coordination and physical diagnosis requirements evident in the `short_description` text.

### Other Burden Signals (Weak or Redundant)

- **`reassignment_indicator`**: Reassigned incidents (n=403) averaged 1,802 min vs. 1,809 min for non-reassigned (n=97) — effectively no difference. Reassignment is not a meaningful duration driver here.
- **`recurrence_signal`**: 99.2% of incidents are flagged as recurring (n=496), leaving no statistical contrast.
- **`time_of_day_band`**: Overnight incidents (n=106) average 1,868 min vs. 1,777 min for business hours — a modest +91 min gap, but this is likely a proxy for staffing coverage rather than a separate operational burden category.
- **`priority`**: Near-flat across priorities (1-Critical: 1,821 min; 2-High: 1,796 min), offering little additional signal beyond `failure_type`.

---

## What-If Scenarios

### Scenario A — Eliminate Connectivity Failure Overhead

If all `connectivity_failure` incidents were resolved at the pace of non-connectivity incidents (baseline mean: 1,702 min), the portfolio mean would fall from **1,803 min → 1,702 min**, a drop of **~101 min (~5.6%)**.

$$\Delta\bar{t}_A = \frac{228}{500} \times (1878 - 1702) = 101 \text{ min}$$

### Scenario B — Eliminate Location-Specific Scope Overhead

If location-specific incidents resolved at the non-location-specific mean (1,779 min), the drop would be **~24 min (~1.3%)** — meaningful per incident but small in portfolio terms due to the low count (n=37).

$$\Delta\bar{t}_B = \frac{37}{500} \times (2100 - 1779) = 24 \text{ min}$$

### Scenario C — Eliminate Both Burdens Together

Treating the 243-incident union of connectivity failures or location-specific scope as the "burdened" set, and resetting them to the clean baseline (incidents with neither burden, n=257, mean = 1,710 min):

| Measure | Value |
|---|---|
| Burdened incidents | 243 (48.6% of portfolio) |
| Clean baseline mean | 1,710 min |
| Overall mean (actual) | 1,803 min |
| **Hypothetical mean** | **1,710 min** |
| **Mean duration drop** | **93 min (5.2%)** |
| **Median drop (approx.)** | **~80 min** |

---

## Key Finding

**Eliminating the two most common operational burdens — high-volume connectivity failures (`failure_type = connectivity_failure`, 45.6% of incidents) and location-specific scope incidents (`scope_indicator = location_specific`, 7.4%)  — is estimated to reduce mean resolution duration by approximately 93–101 minutes (~5–6%), from ~1,803 min to ~1,700–1,710 min (~28.4 h).**

The connectivity failure burden dominates the effect by volume. Location-specific incidents have the largest per-incident penalty (+5 h) but are rare enough to contribute only modestly at the portfolio level. Addressing how network/VPN connectivity incidents are triaged and routed (corroborated by `incident_category = network_connectivity` and `vpn_access` concentrations) offers the largest single lever.

---

## Method Note

**TAPP-generated columns used in this report:** `failure_type`, `scope_indicator`, `incident_category`, `time_of_day_band`, `reassignment_indicator`, `recurrence_signal`.

Columns `failure_type` and `scope_indicator` provided the primary analytical signal. `incident_category` corroborated `failure_type` patterns. `time_of_day_band` was noted as a secondary moderator. `reassignment_indicator` and `recurrence_signal` were assessed and found to be weak or low-contrast drivers for this query.
