---
dataset: flag_6
scenario: whatif_workload
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: what_if
focus_variable: "resolution_time"
query: "If the ticket types that create the heaviest agent workload were reduced, how much would resolution time drop?"
source_table: augment_table/flag_6/whatif_workload/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:21:14.478065+00:00
wall_seconds: 111.56
---

# What-If Workload Analysis: Reducing Heavy-Workload Ticket Types and Impact on Resolution Time

## Summary

The dataset contains **500 tickets** (478 closed/resolved) with an overall mean resolution time of **223.5 hours** (median: 150.0 hours). Reducing the ticket types that impose the heaviest agent workload — primarily **VPN connectivity** and **software update/installation** incidents — would lower mean resolution time by **4–10%**, depending on reduction magnitude. The effect is moderate because the highest-volume groups are not always the highest-resolution-time groups.

---

## Method Note

TAPP-generated columns used in this analysis: `incident_category`, `ticket_complexity_signal`, `recurrence_indicator`. These columns added semantic granularity (e.g., distinguishing VPN from general Network tickets, flagging performance-degradation outliers) beyond the raw `category` and `priority` fields. `resolver_match` had 100% value = True and provided no discriminating signal. `affected_system`, `failure_mode`, `location_scope`, and `is_open_unresolved` were reviewed but not centered in the analysis due to high overlap with other structured fields or low analytical leverage.

---

## 1. Identifying the Heaviest Workload Ticket Types

Agent workload is measured as **ticket volume × mean resolution time** (proxy for total agent-hours consumed).

### By `assignment_group` (original structured column)

| Assignment Group | Tickets (n) | Mean Res. (hrs) | Estimated Agent-Hours | % of Total |
|---|---|---|---|---|
| **Network** | 314 | 221.8 | 69,634 | **65.2%** |
| Database | 100 | 208.4 | 20,838 | 19.5% |
| Software | 25 | 347.3 | 8,682 | 8.1% |
| Service Desk | 29 | 197.9 | 5,738 | 5.4% |
| Hardware | 10 | 193.4 | 1,934 | 1.8% |

**Network** dominates agent workload by volume. **Software** carries the highest mean resolution time (347.3 hrs) despite small volume.

### By `incident_category` (TAPP-generated)

Within the Network category, `incident_category` reveals which sub-types drive the most workload:

| Incident Category | n | Mean Res. (hrs) | Agent-Hours | % of Total |
|---|---|---|---|---|
| **vpn_connectivity** | 106 | 267.8 | 28,385 | **26.6%** |
| email_server | 107 | 197.1 | 21,094 | 19.7% |
| database_access | 99 | 207.6 | 20,549 | 19.2% |
| network_wifi | 37 | 217.2 | 8,038 | 7.5% |
| internet_connectivity | 42 | 190.4 | 7,995 | 7.5% |
| server_access | 30 | 218.5 | 6,555 | 6.1% |
| **software_update_install** | 15 | 425.4 | 6,381 | **6.0%** |

**`vpn_connectivity`** is the single largest agent-hour sink (26.6% of all estimated agent-hours), combining high volume (106 tickets) and above-average resolution time (267.8 hrs). **`software_update_install`** has the highest mean resolution time (425.4 hrs), though its small volume (n=15) limits total impact.

---

## 2. What-If Scenarios: Resolution Time Impact

Using the `incident_category` to define the "heaviest workload" segment (VPN + software_update), the following scenarios model the change in **mean resolution time**:

| Scenario | New Mean Res. (hrs) | Drop from 223.5 hrs | % Reduction |
|---|---|---|---|
| Reduce VPN + SW-update by 25% | 219.2 | −4.3 hrs | 1.9% |
| Reduce VPN + SW-update by 50% | 214.2 | −9.3 hrs | 4.1% |
| Eliminate VPN + SW-update entirely | 201.8 | −21.6 hrs | **9.7%** |

These 121 combined tickets represent 25% of the dataset but account for ~32% of total agent-hours. Their mean resolution time (287.3 hrs) is 28% above the dataset overall mean.

If only the **Software assignment group** (highest mean resolution at 347.3 hrs) were reduced by 50%, the overall mean would drop by only ~3.5 hrs (1.5%) due to its small volume (n=25).

---

## 3. Why the Effect Is Bounded

- **VPN tickets are mostly `simple_single_user`** (105/106 per `ticket_complexity_signal`), suggesting the long resolution time reflects routing/escalation delays or queue depth rather than inherent technical complexity. Reducing VPN volume lowers the queue; it does not change individual case difficulty.
- **`recurrence_indicator`**: 459/478 (96%) of resolved tickets are flagged as recurring — there is essentially no differentiation by this signal, so it does not amplify or explain workload concentration.
- **Network tickets do not resolve faster than others despite representing 65% of volume** (mean 221.8 hrs vs. overall 223.5 hrs), meaning their removal would only modestly shift the mean.
- **`performance_degradation` tickets** (14 closed, mean 385.7 hrs) are a small but high-resolution outlier group — predominantly database_access and internet_connectivity incidents at Critical/High priority. Targeting this cluster specifically could reduce extreme outliers even if volume reduction is modest.

---

## 4. Recommendations

| Action | Target | Expected Mean Resolution Drop |
|---|---|---|
| Deflect/automate VPN reconnection issues (self-service portal) | 106 vpn_connectivity tickets | Up to −21.6 hrs (if fully eliminated); −9.3 hrs at 50% reduction |
| Expedite software_update_install via scheduled maintenance windows | 15 tickets, mean 425 hrs | −1 to −3 hrs on mean (small volume) |
| Address performance_degradation database tickets (n=14, mean 385.7 hrs) | ticket_complexity_signal = performance_degradation | Reduces severe outliers, limited mean impact |
| Prioritize Software assignment group queue management | 25 tickets, mean 347 hrs | −3.5 hrs at 50% reduction |

**Overall conclusion:** Reducing the heaviest-workload ticket types (VPN + software update) by 50% would cut mean resolution time from 223.5 to approximately **214 hours** — a reduction of roughly **4–10%** depending on depth of reduction. The ceiling is capped because the dominant high-volume group (Network/VPN) has only moderately elevated resolution time, not a dramatically worse resolution profile than the rest of the portfolio.
