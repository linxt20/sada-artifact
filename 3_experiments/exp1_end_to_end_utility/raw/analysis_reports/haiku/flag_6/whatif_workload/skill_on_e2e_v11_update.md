---
dataset: flag_6
scenario: whatif_workload
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: what_if
focus_variable: "resolution_time"
query: "If the ticket types that create the heaviest agent workload were reduced, how much would resolution time drop?"
source_table: augment_table/flag_6/whatif_workload/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:21:28.452072+00:00
wall_seconds: 132.57
---

# What-If Analysis: Impact of Reducing Heavy-Workload Ticket Types

## Executive Summary

Reducing ticket volume for the two heaviest agent workload types—**vpn_connectivity** and **email_service**—would deliver significant operational relief. Eliminating these types entirely would reduce total workload hours by **49.9%** (53,284 hours), while a **50% reduction** in volume would cut workload by **26.9%** (28,708 hours) with a **2.6% drop in average resolution time** across the system.

The analysis identifies that these two types account for **49.6%** of all resolved tickets (237 of 478) and consume **49.9%** of all agent hours (53,284 of 106,826 hours), making them the primary lever for workload optimization.

---

## Methods

**TAPP-generated columns used in this analysis:**
- `ticket_complexity_judgment` – Boolean indicator of semantic complexity assessment
- `ticket_scope_extent` – Categorical scope (single_user, enterprise_wide, building_floor, department)
- `agent_assignment` – Agent name assigned to each ticket

**Analysis approach:** Started from resolution time (outcome variable) and ticket type workload volume (primary driver), then used TAPP-generated columns to clarify semantic characteristics of heavy workload types and their resolution behavior across complexity and scope dimensions.

---

## Workload Distribution by Ticket Type

### Current Ticket Volume and Workload (478 resolved tickets, 106,826 total hours)

| Ticket Type | Count | % of Tickets | Avg Resolution (hrs) | Total Workload (hrs) | % of Hours |
|-------------|-------|--------------|----------------------|----------------------|-----------|
| **vpn_connectivity** | 106 | 22.2% | 267.8 | 28,385 | 26.6% |
| **email_service** | 131 | 27.4% | 190.1 | 24,899 | 23.3% |
| network_connectivity | 107 | 22.4% | 205.9 | 22,051 | 20.6% |
| database_access | 99 | 20.7% | 207.6 | 20,550 | 19.2% |
| software | 17 | 3.6% | 407.7 | 6,931 | 6.5% |
| access_account | 10 | 2.1% | 257.6 | 2,576 | 2.4% |
| hardware | 8 | 1.7% | 180.7 | 1,446 | 1.4% |

**Key finding:** The top two workload types (vpn_connectivity and email_service) create nearly identical total burden—26.6% and 23.3% of workload hours respectively—despite different ticket volumes and per-ticket resolution times. This is the primary driver of the what-if scenarios below.

---

## Semantic Characteristics of Heavy Workload Types

### VPN Connectivity (106 tickets, 267.8 hrs avg resolution)

Using the `ticket_complexity_judgment` and `ticket_scope_extent` TAPP columns:

- **Complexity:** 46.2% marked as high complexity; these high-complexity cases resolve in **351.1 hours** (31% longer than overall vpn type average)
- **Scope extent:** 94.3% are single-user issues (100 of 106), averaging 273.4 hours. Only 5.7% are enterprise-wide, which resolve faster at 174.4 hours
- **Agent distribution:** Distributed across all five agents; no single agent carries disproportionate vpn load

**Interpretation:** VPN issues are protracted even at individual scope; complexity compounds resolution time significantly. Single-user vpn issues consume 25,356 of 28,385 hours.

### Email Service (131 tickets, 190.1 hrs avg resolution)

- **Complexity:** 51.1% marked as high complexity; high-complexity cases resolve in **210.0 hours** (10% longer than overall email type average)
- **Scope extent:** 62.6% are single-user (82 of 131, 212.3 hrs avg), 34.4% are enterprise-wide (45 of 131, 159.8 hrs avg)—enterprise-wide email issues resolve **26% faster** than single-user email issues
- **Agent distribution:** Similar to vpn; no concentration on a single agent

**Interpretation:** Email service workload is bifurcated: single-user email sync/access issues are lengthy (212 hrs avg), while enterprise-wide email outages, despite broader impact scope, are resolved faster (160 hrs avg), likely due to focused infrastructure response.

---

## Resolution Time Impact by Scenario

### Baseline State
- **Total tickets:** 478
- **Average resolution time:** 223.5 hours
- **Median resolution time:** 150.0 hours
- **Total workload hours:** 106,826

### Scenario 1: Eliminate VPN and Email Service Types Entirely

**Assumption:** Organization stops accepting or routes these tickets to a managed service.

- **Remaining tickets:** 241 (50.4% of baseline)
- **New average resolution time:** 222.2 hours (**−0.6% change**)
- **New median resolution time:** 146.4 hours (**−2.4% change**)
- **Workload reduction:** 53,284 hours (**−49.9%**)

**Insight:** Eliminating these types does not dramatically reduce *average* resolution time per ticket (other types average 222.2 hrs vs. 223.5 hrs current), but eliminates ~50% of total agent effort. The benefit is primarily in reducing overall agent burden rather than speeding up remaining work.

### Scenario 2: 50% Reduction in VPN and Email Service Volume

**Assumption:** Proactive measures (self-service, automation) reduce incidents by 50%; e.g., VPN self-troubleshooting portal, email sync client improvements.

- **Remaining tickets:** 359 (75.1% of baseline)
- **New average resolution time:** 217.6 hours (**−2.6% change**)
- **New median resolution time:** 150.0 hours (**±0.0% change**)
- **Workload reduction:** 28,708 hours (**−26.9%**)

**Insight:** A 50% volume cut delivers measurable per-ticket speedup (2.6% average improvement), likely due to less agent context-switching and queue pressure. This is the most realistic high-impact scenario.

### Scenario 3: 25% Reduction in VPN and Email Service Volume

**Assumption:** Incremental improvement through training or process optimization.

- **Remaining tickets:** 419 (87.7% of baseline)
- **New average resolution time:** 223.2 hours (**−0.1% change**)
- **New median resolution time:** 150.1 hours (**±0.0% change**)
- **Workload reduction:** 13,300 hours (**−12.4%**)

**Insight:** A 25% reduction provides modest workload relief but minimal per-ticket resolution improvement.

---

## Key Drivers of Resolution Time in Heavy Workload Types

### Role of Complexity (ticket_complexity_judgment)

- **VPN:** High-complexity cases resolve 31% slower (351.1 vs. 273.4 hrs for low-complexity)
- **Email:** High-complexity cases resolve 10% slower (210.0 vs. 181.3 hrs for low-complexity)

Complexity is a meaningful but not dominant factor. Other process or systemic factors (queueing, agent skill distribution) may contribute more to total resolution time than the ticket's inherent complexity.

### Role of Scope (ticket_scope_extent)

- **Email:** Enterprise-wide cases resolve **26% faster** (159.8 hrs) than single-user cases (212.3 hrs), suggesting faster escalation/prioritization for broad outages
- **VPN:** Enterprise-wide cases also resolve faster (174.4 hrs) than single-user (273.4 hrs), though vpn enterprise incidents are rare (6 of 106)

**Counterintuitive finding:** Broader-scope incidents, despite affecting more users, are resolved faster. This suggests systemic issues trigger stronger organizational response and resource allocation.

---

## Agent Workload Distribution

Five agents (beth_anglin, charlie_whitherspoon, fred_luddy, howard_johnson, luke_wilson) handle the workload relatively evenly (98–103 tickets each). Heavy workload types are distributed across all agents without concentration, indicating no single agent specialization in vpn or email. This even distribution may limit optimization opportunities via skill-based routing.

---

## Recommendations

1. **Invest in self-service and automation for VPN and email issues:** A 50% reduction in volume (Scenario 2) would cut workload by 26.9% and reduce average resolution time by 2.6%, improving both capacity and performance.

2. **Prioritize enterprise-wide incidents:** Data shows enterprise-scope tickets resolve faster; implement escalation protocols to identify and fast-track widespread issues.

3. **Review complexity assessment accuracy:** High-complexity vpn tickets show 31% longer resolution; validate whether complexity tagging is predictive and whether agents need additional training for complex cases.

4. **Monitor single-user email vs. enterprise-wide email resolution patterns:** The 26% speed gap suggests different handling paths; document and standardize best practices from the faster enterprise-wide branch.

---

## Limitations and Caveats

- Analysis is retrospective; external factors (staffing changes, seasonal demand) may influence future performance
- Complexity and scope judgments are TAPP-generated semantic assessments; validation against agent feedback or domain expertise recommended
- Agent assignment reflects historical allocation, not necessarily optimal or preferred assignment
- What-if scenarios assume no behavioral changes; actual reduction in ticket volume might reallocate freed capacity or change resolution strategy

---

## Conclusion

Ticket types **vpn_connectivity** and **email_service** are responsible for 49.6% of ticket volume and 49.9% of agent workload hours. A **50% reduction in volume** for these types would yield **26.9% workload relief** and a **2.6% improvement in average resolution time** across the system—a meaningful operational win. The TAPP-generated columns reveal that high-complexity cases (especially vpn) and single-user scope (especially email) drive extended resolution; targeting these sub-categories for automation or process improvement could amplify the benefit of overall volume reduction.
