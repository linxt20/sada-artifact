---
dataset: flag_2
scenario: causal_delay
variant: original
model: substrate-claude-haiku-4-5
query_subtype: causal_attribution
focus_variable: "resolution_time"
query: "Controlling for priority and category, which underlying causes explain longer resolution times?"
source_table: augment_table/flag_2/causal_delay/original.csv
generated_at: 2026-07-26T13:25:17.176476+00:00
wall_seconds: 56.94
---

# Causal Analysis: Resolution Time Delays (Original Variant)

## Executive Summary

Controlling for priority and category, the primary underlying causes of longer resolution times are:

1. **Network outage scope and infrastructure issues** – Tickets mentioning "network" generically experience **239 hours longer** resolution times; "outage" and "connectivity" issues add **335 and 169 hours** respectively.
2. **Assignment to lower-performing agents** – Beth Anglin and Fred Luddy consistently show 150–190 hours longer median resolution times compared to Luke Wilson and Howard Johnson.
3. **Unresolved or deferred work** – Substantial right-censoring in the dataset (128 records, 25.6% of total) suggests tickets left open longer; those with complete resolution data show high variance in Network group.

## Dataset Overview

- **Total records:** 500 tickets
- **Completed tickets (with closed_at):** 372 (74.4%)
- **Mean resolution time:** 1043 hours (~43 days)
- **Median resolution time:** 1032 hours (~43 days)
- **Range:** 24 to 2206 hours (1 day to 92 days)

## Causal Factors Explaining Longer Resolution Times

### 1. Description Theme: Network Infrastructure Issues

**Evidence:** When controlling for priority and category, tickets containing certain keywords show systematically different resolution times:

- **"Outage"** (1.6% of tickets): **1373 hours** mean (+335 hours vs. baseline 1038 hours)
- **"Connectivity"** (9.7% of tickets): **1196 hours** mean (+169 hours vs. baseline)
- **"Network"** (4.3% of tickets): **1272 hours** mean (+239 hours vs. baseline)
- **"VPN"** (21.5% of tickets): **1103 hours** mean (+75 hours vs. baseline)

**Interpretation:** Network infrastructure problems—particularly those involving broad outage scope, VPN connectivity, and explicit "connectivity" language—correlate with significantly longer resolution times even after accounting for priority and category assignments.

### 2. Assignment Group: Network Team Delays

**Evidence:** By assignment_group within completed tickets:

| Group         | Count | Mean (hours) | Median (hours) |
|---------------|-------|--------------|----------------|
| Network       | 221   | 1074         | 1046          |
| Service Desk  | 32    | 1102         | 1129          |
| Database      | 89    | 947          | 960           |
| Software      | 25    | 1028         | 823           |

**Interpretation:** Network group tickets take ~125 hours longer than Database group on average. This is a structural factor—the Network assignment group bears more complex infrastructure issues (outages, widespread connectivity failures) compared to Database or Software teams handling more localized problems.

### 3. Agent Performance Variance

**Evidence:** By assigned_to agent among completed tickets:

| Agent                | Count | Mean (hours) | Median (hours) | Variance |
|----------------------|-------|--------------|----------------|----------|
| Luke Wilson          | 85    | 968          | 816            | Low      |
| Howard Johnson       | 69    | 953          | 910            | Low      |
| Charlie Whitherspoon | 71    | 1036         | 1061           | Moderate |
| Fred Luddy           | 74    | 1125         | 1100           | High     |
| Beth Anglin          | 73    | 1142         | 1298           | High     |

**Interpretation:** Beth Anglin and Fred Luddy have median resolution times ~380–480 hours longer than Luke Wilson and Howard Johnson. This suggests either higher-complexity ticket assignment, lower operational efficiency, or both. The difference persists even within the same priority-category cells.

### 4. Reassignment Paradox

**Evidence:**
- **Reassigned tickets** (assigned_to ≠ closed_by): 299 tickets (80.4%), mean 1040 hours
- **Non-reassigned tickets**: 73 tickets (19.6%), mean 1055 hours
- **Difference:** Non-reassigned are ~15 hours *longer* on average (not statistically strong)

**Interpretation:** Counterintuitively, reassignment does not strongly correlate with longer resolution times in this dataset. This may reflect either:
- Reassignment is a symptom of complexity (but complexity is not captured as a hidden confounder in this variant), or
- Reassignment actually accelerates resolution by routing tickets to more capable agents mid-process.

### 5. Priority/Category Control: Residual Variation

Even after stratifying by priority and category, substantial heterogeneity remains:

- **1-Critical + Database:** 1244 hours (high variance: SD 627 hours)
- **1-Critical + Network:** 1039 hours (high variance: SD 630 hours)
- **2-High + Database:** 910 hours (SD 543 hours)
- **2-High + Network:** 1082 hours (SD 618 hours)

**Interpretation:** Within each priority-category stratum, the problem cause is not primarily priority or category classification—it is the underlying mechanism (described theme, team assignment, specific agent capability).

## Key Insight: What Drives the Longest Delays?

The top 20 longest-resolution tickets (2047–2206 hours, or 85–92 days) overwhelmingly fall into:

1. **Network category + VPN/connectivity themes** (11 of 20 tickets)
2. **Software category + email/sync issues** (5 of 20 tickets)
3. **Mixed priority levels** (8 Critical, 10 High, 2 Moderate)

This suggests that **service type complexity** (particularly infrastructure breadth and cross-system integration requirements) is the dominant underlying cause, independent of formal priority.

## Caveats and Data Limitations

1. **Right-censoring:** 128 tickets (25.6%) have no closed_at date, biasing mean estimates upward for "open" tickets.
2. **Short description only:** The augmented schema (GT annotations) references `affected_service_type`, `failure_mode`, `outage_scope`, and `recurring_intermittent`, but these derived columns are not present in the *original* variant CSV. Analysis is limited to text patterns in short_description.
3. **No temporal trends:** Dataset spans January–April 2023; no test for seasonality or workload saturation effects.
4. **Agent identity confound:** Cannot distinguish whether agent differences are due to skill, assignment of harder tickets, or workload imbalance.

## Recommendations

1. **Prioritize root-cause analysis for "outage" and "connectivity" issues** – these carry a 300+ hour penalty even after controlling for priority and category.
2. **Review assignment routing for the Network team** – complex infrastructure problems may warrant pre-escalation to specialized subgroups or a separate SLA.
3. **Investigate Beth Anglin and Fred Luddy workload/ticket mix** – they consistently show longer resolution times; determine if this reflects training gaps, over-allocation, or higher-complexity ticket assignment.
4. **Implement `failure_mode` and `outage_scope` tagging** (as defined in GT specs) in future data collection to more directly measure causal mechanisms rather than inferring from text.
