---
dataset: flag_12
scenario: predictive_inefficient
variant: original
model: substrate-claude-haiku-4-5
query_subtype: predictive_feature_engineering
focus_variable: "inefficient_resolution"
query: "What signals suggest an incident resolution will be inefficient?"
source_table: augment_table/flag_12/predictive_inefficient/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_12__predictive_inefficient/analyses/original/analysis.md
wall_seconds: 84.85
---

# Signals of inefficient incident resolution

## Basis
No explicit `inefficient` label is visible in the table. The operational proxy used here is resolution time, computed from `closed_at - opened_at`. In this dataset of 500 incidents, the median resolution time is 173.2 hours, and the slowest quartile begins at $252.7$ hours. “Inefficient” below refers to incidents in that upper quartile.

## Strongest signals in the visible data

| Signal | Evidence from columns | Interpretation |
|---|---|---|
| `assigned_to = Luke Wilson` | 116 incidents; mean 195.5 hours; 32.8% in the slowest quartile vs 25% overall | Strongest person-level signal in the table |
| Hardware workload | `category = Hardware`: 406 incidents; mean 181.4 hours; 25.9% slowest-quartile | Slightly worse than baseline and, more importantly, the dominant source of long cases |
| Printer-related descriptions | `short_description` contains “printer”: 200 incidents; mean 183.9 hours; 27.0% slowest-quartile. Exact phrase `Printer not working properly`: 30 incidents; mean 211.6 hours; 43.3% slowest-quartile | Repetitive printer faults appear to linger |
| `sys_updated_by = system` | 160 incidents; mean 198.9 hours; 28.8% slowest-quartile. Within Hardware: 128 incidents; mean 203.0 hours; 30.5% slowest-quartile | System-touched workflows are consistently slower |
| End-of-week openings | Friday: 75 incidents; 29.3% slowest-quartile. Saturday: 70 incidents; 31.4% slowest-quartile. Monday is much lower at 17.4% | Suggests backlog or handoff effects |
| Morning openings | 6:00–11:59 openings: 109 incidents; 31.2% slowest-quartile vs 20.0% for evening openings | Timing appears relevant, though not decisively |

## Patterns worth acting on
- The clearest early warning combination is a **Hardware incident assigned to Luke Wilson**: 96 incidents, mean 199.6 hours, 33.3% in the slowest quartile.
- That pattern is even worse for some timing pockets, especially **Luke Wilson + Thursday opening**: 15 incidents, 46.7% slowest-quartile.
- Failure-style wording is somewhat informative:
  - `short_description` contains **“unable”**: 40 incidents, 30.0% slowest-quartile.
  - contains **“working”**: 87 incidents, 29.9%.
  - By contrast, generic **“issue”** language is lower at 18.0%.

## Weak or contrary signals
- **Priority is not a useful warning signal here.**  
  `1 - Critical` is not slower than `2 - High` or `3 - Moderate`:
  - Critical: 18.5% slowest-quartile
  - High: 25.4%
  - Moderate: 26.0%
- **Network and Database incidents are not especially inefficient** in this sample:
  - Network: 18.2%
  - Database: 10.5%
- **Caller effects are weak.**  
  The highest observed caller group, `David Loo`, is at 28.6%, only modestly above the 25% baseline.

## Important exceptions and caveats
- `category` and `assignment_group` are nearly redundant in this data (`Hardware` maps heavily to the `Hardware` group), so they should not be treated as independent signals.
- Some high-rate pockets are **small** and should be treated cautiously:
  - `Inquiry / Help`: 20 incidents, 35.0%
  - `Service Desk`: 19 incidents, 31.6%
  - `Need assistance with software installation`: 7 incidents, 57.1%
- Some correlated fields are **not truly predictive** for early warning because they are known late in the lifecycle:
  - `state = Resolved` is slightly slower than `Closed` (26.2% vs 23.8%)
  - `closed_by = Howard Johnson` is higher at 29.6%
  These may reflect outcome leakage rather than useful pre-resolution signals.

## Decision-ready conclusion
The most credible signals that an incident resolution will be inefficient are:

1. **Hardware-heavy incidents**, especially **printer-related** ones.
2. **Assignment to Luke Wilson**, particularly within Hardware.
3. **System-updated cases**, which show consistently longer resolution times.
4. **Friday/Saturday and morning openings**, which may indicate backlog or handoff drag.

The weakest predictors are **priority**, **caller**, and most non-hardware categories. Overall, the practical screening rule from this table is: flag **hardware/printer tickets**, especially when **assigned to Luke Wilson** or **opened near the end of the week**, as the highest-probability inefficient resolutions.
