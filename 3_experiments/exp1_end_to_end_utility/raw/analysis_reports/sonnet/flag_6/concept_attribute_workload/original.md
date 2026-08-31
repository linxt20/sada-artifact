---
dataset: flag_6
scenario: concept_attribute_workload
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: faceted_decomposition
focus_variable: "agent_workload_burden"
query: "What kinds of tickets create heavier agent workload?"
source_table: augment_table/flag_6/concept_attribute_workload/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_6__concept_attribute_workload/analyses/original/analysis.md
wall_seconds: 103.8
---

# What kinds of tickets create heavier agent workload?

## Bottom line

Using **ticket volume** and **elapsed handling time** from `opened_at` to `closed_at` as workload proxies, the heaviest agent workload comes from:

1. **Network tickets**, especially **VPN** and **email/server** issues.
2. **Software/system tickets** on a **per-ticket** basis.
3. **Database access/connectivity** tickets as a secondary workload source.

## Evidence from the table

### 1. Network issues dominate total workload
`category = Network` is the largest source of work by far:

- **284 / 500 tickets** in the raw data.
- About **58.1% of all valid closed-ticket hours** (`64,108.7` hours of `110,416.9`).
- Mean closed duration on valid tickets: about **264.9 hours**.

Within network work, repeated `short_description` patterns are concentrated around:

- **VPN**:
  - `Unable to connect to VPN` — **22 tickets**, **529.6 mean hours**, **11,651.5 total hours**
  - `Cannot connect to VPN` — **15 tickets**, **201.8 mean hours**
- **Email/server**:
  - `Email server not responding` — **21 tickets**, **164.4 mean hours**
  - `Email server down` — **11 tickets**, **130.1 mean hours**

Interpretation: **VPN and email/server incidents create the biggest overall burden because they recur often**, and some VPN variants also stay open a long time.

### 2. Software/system issues look heaviest per ticket
Although smaller in count, software work appears heavier per case:

- `category = Software`:
  - **64 valid tickets**
  - **277.9 mean hours**
  - **188.4 median hours**
- `assignment_group = Software`:
  - **23 valid tickets**
  - **379.9 mean hours**
  - **212.0 median hours**

The grouped text theme **Software/system** also has the highest average burden among major themes:

- **19 valid tickets**
- **409.2 mean hours**

Interpretation: **software/system tickets are not the main volume driver, but they appear more time-consuming when they do occur**.

### 3. Database tickets are a meaningful secondary source
Database work is not as dominant as network, but it is still substantial:

- `category = Database`:
  - **109 total tickets**
  - **90 valid closed tickets**
  - **22,426.5 total hours**
  - About **20.3% of all valid closed-ticket hours**

Common database descriptions include:

- `Unable to access database` — **12 tickets**
- `Unable to access company database` — **7 tickets**

Interpretation: **database access/connectivity issues create sustained workload through both moderate volume and long handling times**.

## Priority signal

Priority is **not** a strong indicator that a ticket is heavier:

- `2 - High` accounts for **78.3% of total valid closed-ticket hours**, but mainly because it is **379 / 500 tickets**.
- Mean hours are similar for `2 - High` (**263.4**) and `3 - Moderate` (**266.4** on valid tickets).
- `1 - Critical` is actually lower on average (**229.9**).

Interpretation: **workload is driven more by issue type and volume than by priority label alone**.

## Exceptions and weak evidence

- The dataset has **no direct workload field** such as touch count, reassignment count, or agent effort. The analysis therefore uses **duration and ticket volume as proxies**.
- There are **22 unresolved tickets** and **50 tickets with negative durations** from timestamp inconsistencies, so duration-based conclusions rely mainly on **428 valid closed tickets**.
- Some strongest per-ticket effects come from **small groups**:
  - `Software/system` theme: **19 tickets**
  - `assignment_group = Software`: **23 tickets**
  These patterns are suggestive, but less stable than the network findings.
- Unresolved-rate evidence is modest, but **Network/Internet access** and **Database access/connectivity** have somewhat higher unresolved shares than email or VPN.

## Decision-ready conclusion

If the goal is to reduce agent workload, the clearest targets are:

1. **Network tickets first**, especially **VPN** and **email/server availability** issues, because they generate the most total work.
2. **Software/system tickets second**, because they appear **heaviest per case**.
3. **Database access/connectivity tickets third**, because they contribute a large secondary workload pool.

In short: **high-volume connectivity issues create the most overall workload, while software/system tickets appear the most labor-intensive per ticket.**
