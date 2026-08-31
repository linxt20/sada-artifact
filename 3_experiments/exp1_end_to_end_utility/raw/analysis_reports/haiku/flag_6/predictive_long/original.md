---
dataset: flag_6
scenario: predictive_long
variant: original
model: substrate-claude-haiku-4-5
query_subtype: predictive_feature_engineering
focus_variable: "resolution_time"
query: "What signals suggest an agent's tickets will take longer to resolve?"
source_table: augment_table/flag_6/predictive_long/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_6__predictive_long/analyses/original/analysis.md
wall_seconds: 75.61
---

# Signals that a ticket will take longer to resolve

## Scope and focus variable
Resolution time is inferred from `closed_at - opened_at`. The table has 500 rows, but **72 are not usable for this metric** (`22` missing timestamps, `50` negative durations), so the patterns below are based on **428 valid tickets**.

Baseline: the median valid ticket takes **164 hours** to resolve (about **6.8 days**). A practical “long” ticket threshold is the top quartile: **$\ge 260$ hours** (about **10.8 days**).

## Strongest signals

| Signal in visible columns | Evidence from the data | Interpretation |
|---|---:|---|
| `assigned_to = Fred Luddy` | Median **691 h**; **80.3%** of his tickets are in the long-ticket quartile | By far the clearest signal. The longest tickets in the dataset are overwhelmingly assigned here. |
| `category = Software` | Median **188 h**; **28.1%** long | Software tickets run somewhat longer than other categories. |
| `assignment_group = Software` | Median **212 h**; **30.4%** long | Supports the same pattern, though sample size is small (`23`). |
| Connectivity / VPN / email-server descriptions in `short_description` | Repeated descriptions such as **“Unable to connect to VPN”** have median **249 h**; “connect”-type terms show elevated medians | Persistent access/connectivity issues appear more likely to stay open longer. |
| `caller_id = Bud Richman` | Median **189 h**; **30.9%** long | Caller mix matters somewhat, though this is weaker than assignee effects. |
| `sys_updated_by = admin` | Median **182 h**; **30.6%** long | Tickets touched by admins skew longer, possibly reflecting escalation or handoff. |

## Important supporting patterns

- **Category mix:** `Network` tickets are also slower than average (median **177 h**, **25.2%** long). `Database` is lower (median **143 h**), and `Hardware` is lower still (median **123 h**).
- **Repeated long-running ticket themes:** the longest cases include `Network`, `Database`, and `Software` issues such as VPN access, intranet access, email server failures, and OS/database server errors.
- **Timing effects are present but weak:** tickets opened on **Friday** have the highest median (**190 h**), and tickets opened in the **afternoon (12–17)** are slower than other time buckets (median **183 h**).

## Exceptions and weak evidence

- **Priority is not a strong “slow” signal.** `1 - Critical` tickets are actually faster than `2 - High` here (median **149 h** vs **172 h**). So higher stated urgency does **not** imply longer resolution in this dataset.
- **State is not useful for this question.** `Resolved` and `Closed` look very similar in duration.
- **Some strong-looking patterns may reflect process effects, not ticket difficulty.**  
  The `assigned_to = Fred Luddy` signal is extreme, but it may partly capture a queue/backlog pattern: his ticket durations rise steadily across the year, from about **118 h** median in January to over **1500 h** by November.
- **Small groups need caution.** `assignment_group = Software`, `Service Desk`, `Inquiry / Help`, and some exact descriptions have low counts, so they should be treated as hints, not firm rules.

## Decision-ready takeaway
The best practical signals that a ticket will take longer are:

1. **Who it is assigned to**, especially `Fred Luddy`.
2. **Software and network-oriented work**, especially connectivity/VPN/email server issues.
3. **Admin-touched or escalated-looking tickets** (`sys_updated_by = admin`).
4. **Some caller and timing effects**, especially `Bud Richman`, Friday opens, and afternoon opens.

The main non-signal is **priority**: critical tickets are **not** slower here. Because of the timestamp issues and the very strong single-assignee effect, these findings are best used as **triage signals**, not causal claims.
