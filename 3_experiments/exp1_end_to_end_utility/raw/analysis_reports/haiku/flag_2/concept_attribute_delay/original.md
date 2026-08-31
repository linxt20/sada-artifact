---
dataset: flag_2
scenario: concept_attribute_delay
variant: original
model: substrate-claude-haiku-4-5
query_subtype: faceted_decomposition
focus_variable: "incident_delay_reasons"
query: "Why do some incidents take longer to resolve?"
source_table: augment_table/flag_2/concept_attribute_delay/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_2__concept_attribute_delay/analyses/original/analysis.md
wall_seconds: 116.7
---

# Why do some incidents take longer to resolve

## Summary

Using $resolution\ time = closed\_at - opened\_at$, **372 of 500** incidents have measurable durations (`Closed` or `Resolved`). The median resolution time is about **1032 hours** (~43 days), and the longest cases reach **2205.6 hours** (~92 days).

The strongest visible reasons some incidents take longer are:

1. **A strong aging/time-period effect**
2. **More delay in network-, email-, and access-related work**
3. **Slower queues in `Network` and `Service Desk`**
4. **Priority is not a strong explanation**

## What the table shows

| Factor | Visible pattern | Why it matters |
| --- | --- | --- |
| **Opened date** | Early incidents in Jan 2023 resolve quickly: `INC0000000000` takes **24h**, `INC0000000001` **31.2h**, `INC0000000003` **38.4h**. The longest incidents were all opened in late Oct 2023 and closed in Jan 2024, taking about **2104.8-2205.6h**. | The biggest observable driver is **when the ticket entered the queue**. Long cases are concentrated in a later period, consistent with backlog or process-delay effects. |
| **Category** | Mean resolution time by `category`: `Network` **1078.7h** (197 cases), `Software` **1050.6h** (70), `Database` **955.0h** (86), `Hardware` **1105.2h** (12). | `Network` issues are both common and slower than `Database` issues. `Hardware` looks slow too, but the sample is small. |
| **Assignment group** | Mean by `assignment_group`: `Service Desk` **1102.4h** (32), `Network` **1074.0h** (221), `Software` **1028.3h** (25), `Database` **946.5h** (89). | Queue/team effects are visible. `Network` and `Service Desk` cases tend to stay open longer than `Database` cases. |
| **Assignee** | Mean by `assigned_to`: `Beth Anglin` **1141.9h**, `Fred Luddy` **1125.4h**, `Charlie Whitherspoon` **1035.6h**, `Luke Wilson` **967.5h**, `Howard Johnson` **952.8h**. | Some assignees are associated with longer tickets, but this may reflect case mix or timing rather than individual performance. |
| **Priority** | Mean by `priority`: `1 - Critical` **1118.7h**, `2 - High` **1019.5h**, `3 - Moderate` **1120.7h**. | Delay is **not** explained simply by urgency. Higher priority does not consistently resolve faster or slower. |

## Concrete long-delay pattern

The longest incidents are dominated by **connectivity, email, VPN, and access** problems:

- `INC0000000370` — **Trouble accessing VPN**
- `INC0000000368` — **Unable to access network drive**
- `INC0000000367` — **Email server connectivity issues**
- `INC0000000364` — **Unable to connect to VPN**
- `INC0000000362` — **Email system outage reported**
- `INC0000000360` — **Email system is down**
- `INC0000000358` — **Cannot connect to office VPN**
- `INC0000000357` — **Unable to access office intranet**

This matches the slower averages for the `Network` category and the `Network` / `Service Desk` assignment groups.

Several of the longest cases also show possible routing complexity, for example:

- `INC0000000371`: `category=Software`, `assignment_group=Network`
- `INC0000000369`: `category=Software`, `assignment_group=Service Desk`

These examples suggest that cross-team handling may add delay, but the evidence is only suggestive from this table.

## Important caveats

- **128 incidents** are still `New` or `In Progress` and have no `closed_at`, so they cannot be included in duration analysis.
- Those unresolved rows appear near the end of the dataset, so the visible timing pattern is partly affected by **right-censoring**.
- `Hardware` has only **12** resolved cases, so that signal is weaker than the `Network` vs `Database` comparison.

## Decision-ready answer

Some incidents take longer mainly because they are concentrated in a later backlog period and because they are more often **network/access/email/VPN** issues handled by slower queues such as **`Network`** and **`Service Desk`**. By contrast, **priority** is a weak explanation in this dataset.

**Best operational focus:** monitor aging by `opened_at`, review routing for connectivity/email incidents, and compare process/capacity between `Network` / `Service Desk` and `Database` teams.
