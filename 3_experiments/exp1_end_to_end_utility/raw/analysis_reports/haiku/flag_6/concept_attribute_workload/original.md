---
dataset: flag_6
scenario: concept_attribute_workload
variant: original
model: substrate-claude-haiku-4-5
query_subtype: faceted_decomposition
focus_variable: "agent_workload_burden"
query: "What kinds of tickets create heavier agent workload?"
source_table: augment_table/flag_6/concept_attribute_workload/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_6__concept_attribute_workload/analyses/original/analysis.md
wall_seconds: 109.3
---

# Analysis: What kinds of tickets create heavier agent workload?

## Bottom line

**Heavier workload is driven mainly by recurring access/connectivity tickets**—especially **VPN, email, network/internet, and database access** issues. These ticket types combine the strongest mix of **high volume**, **meaningful time-to-close**, and some **remaining open backlog**.

## Strongest patterns in the data

| Ticket kind | Why it looks heavier |
|---|---|
| **VPN / connectivity access** | **109** tickets match VPN-related descriptions (**21.8%** of all tickets). They also stay active for a while: median non-negative close duration is about **186.6 hours**, mean about **291.4 hours**. Repeated descriptions include **"Unable to connect to VPN" (25)** and **"Cannot connect to VPN" (16)**. |
| **Email incidents** | Email-related descriptions are the single biggest theme at **134 tickets (26.8%)**. They also carry the most urgency: **46** are **1 - Critical** (**34.3%** of email tickets). Common repeats are **"Email server not responding" (24)** and **"Email server down" (14)**. |
| **Database access issues** | Database-related work is also substantial: **105** description-themed tickets, or **109** in the `category` field. These have **23–27 critical tickets** depending on whether you use description theme or category, plus **6** unresolved tickets. Median non-negative close duration is about **140–143 hours**. |
| **General network/internet issues** | Network/internet descriptions account for **83 tickets (16.6%)** and have the **highest open share** among the main themes at **7.2%**. In the official `category` field, **Network** is even larger at **284 tickets (56.8%)**, showing this is the biggest queue by volume. |
| **Software/server work** | These look heavier **per ticket** than as total queue drivers. Software/app description themes have the **longest durations** (median about **212.0 hours**, mean about **367.9 hours**) and server issues are also long-running (median about **198.1 hours**), but volumes are much smaller (**15** and **31** tickets). |

## What this suggests operationally

- If **workload** means **total agent demand**, the main burden comes from **network-access problems**:
  - `category = Network`: **284 tickets**
  - `assignment_group = Network`: **328 tickets**
  - frequent repeats in `short_description`: VPN, email server, internet/Wi‑Fi access
- If **workload** means **harder/slower tickets**, the strongest signals are:
  - **VPN access**
  - **software/app issues**
  - **server-related issues**
- **Email incidents** appear especially costly in **urgency/escalation pressure**, because they have the highest critical share.

## Important nuance

**Priority alone does not explain heavier workload.**  
`1 - Critical` tickets are not the longest-running group in this dataset: median non-negative close duration is about **148.7 hours** for critical tickets versus **172.0 hours** for `2 - High`. That suggests the heavier workload comes more from **recurrence and sustained volume** than from priority label alone.

## Exceptions and weak evidence

- **Software** looks long-running, but the description-based software/app group is small (**15 tickets**), so that signal is weaker.
- Some `category` labels do not cleanly match `short_description`, so **ticket type is clearer from the text description than from category alone**.
- The dataset has **no explicit workload field**, so this answer infers workload from visible proxies:
  - ticket **count**
  - **priority** mix
  - **open/in-progress** share
  - **close duration**
- Duration evidence is imperfect because **50 records have negative open-to-close durations** and **22 have no `closed_at`**. Duration-based claims above therefore rely on **non-negative closed tickets only**.

## Decision-ready answer

The tickets most likely to create **heavier agent workload** are:

1. **VPN and other access/connectivity tickets** — biggest combination of repetition, queue volume, and long handling time.
2. **Email service incidents** — very frequent and the most likely to be marked critical.
3. **Database access tickets** — consistently high-volume and often critical.
4. **Software/server issues** — fewer tickets, but often heavier on a **per-ticket effort/time** basis.
