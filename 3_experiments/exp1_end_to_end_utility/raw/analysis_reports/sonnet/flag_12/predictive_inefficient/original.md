---
dataset: flag_12
scenario: predictive_inefficient
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "inefficient_resolution"
query: "What signals suggest an incident resolution will be inefficient?"
source_table: augment_table/flag_12/predictive_inefficient/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_12__predictive_inefficient/analyses/original/analysis.md
wall_seconds: 73.52
---

# Incident-resolution inefficiency signals

## Basis
- The table has 500 incidents and no explicit `inefficient` label.
- Inefficiency was proxied with longer resolution time from `opened_at` to `closed_at`.
- Median resolution time is **173.2 hours**; the slowest 10% start at **320.3 hours** (about **13.3 days**).

## Stronger signals

| Signal | Evidence from the table | Read |
|---|---|---|
| **Owner / resolver identity** | `assigned_to` varies materially: **Luke Wilson** averages **195.5h** with **12.1%** in the slowest decile; **Howard Johnson** has **13.2%** slow-decile cases; **Fred Luddy** is lower at **165.0h** and **5.6%** slow-decile. `closed_by` shows a similar pattern: **Howard Johnson** has **186.3h** average and **13.9%** slow-decile, versus **Fred Luddy** at **5.6%**. | The clearest operational signal is who owns or closes the ticket. This may reflect workload, handoff patterns, or case mix. |
| **System-updated records** | `sys_updated_by = system` has the highest average duration: **198.9h**, with **13.8%** slow-decile cases, versus **admin` 173.9h / 7.5%** and **employee` 163.4h / 9.0%**. | Automated/system-touched workflows correlate with slower resolution. |
| **`state = Resolved` rather than `Closed`** | `Resolved` incidents average **184.3h** with **12.3%** slow-decile, versus `Closed` at **172.7h** and **7.8%**. | Incidents still sitting in `Resolved` appear more likely to have inefficient end-to-end handling than those fully `Closed`. |
| **Non-routine endpoint hardware language in `short_description`** | Higher slow-decile rates appear for terms like **workstation** (**21.1%**, $n=19$), **turning** (**20.0%**, $n=15$), **drive** (**18.2%**, $n=11$), **assistance** (**15.4%**, $n=13$), **malfunction** (**15.0%**, $n=20$), **screen** (**15.0%**, $n=20$), and **responding** (**13.2%**, $n=38$). | Descriptions that suggest diagnosis, physical device failure, or support requests tend to run longer than routine tickets. |

## Weaker or mixed signals

- **Category and assignment group are weak separators.**
  - `Hardware` dominates the dataset (**406/500** incidents) and has **181.4h** average duration with **10.1%** slow-decile incidence.
  - Other categories are close: `Software` **153.6h / 9.1%**, `Network` **161.6h / 9.1%**, `Database` **172.4h / 10.5%**, `Inquiry / Help` **182.1h / 10.0%**.
  - Read: category alone is not a strong predictor, though most slow cases still land in hardware because of volume.

- **Priority is not very informative here.**
  - `1 - Critical`: **11.1%** slow-decile, `2 - High`: **9.9%**, `3 - Moderate`: **10.4%**.
  - Read: higher stated urgency does not clearly prevent long resolution in this sample.

- **Timing effects exist but are modest.**
  - Weekend openings are only slightly slower on average (**182.2h** vs **177.0h** weekdays).
  - `Friday` and `Saturday` openings have the longest average durations (**195.7h** and **189.7h**).
  - By open period, `afternoon` (**11.3%**) and `night` (**11.0%**) have slightly higher slow-decile rates than `morning` (**8.3%**).
  - Read: time-of-open is a secondary signal, not a primary one.

- **Caller differences are limited.**
  - `caller_id = ITIL User` has **11.7%** slow-decile cases, versus **7.8%** for `Don Goodliffe`.
  - Read: requester identity may matter somewhat, but the spread is small.

## Important exceptions

- **High-volume printer incidents are not especially inefficient.**
  - Descriptions containing **printer** appear **200** times but only **9.0%** fall in the slowest decile.
  - Read: common repetitive issues can create workload without being the main inefficiency signal.

- **Not all technical issues are slow.**
  - In this sample, keywords such as **server**, **display**, **power**, and **replacement** had **0** slow-decile cases, though each appears in only about **10–20** records.
  - Read: some apparently serious technical terms do not consistently predict inefficient resolution.

## Limits
- This is correlation only.
- Inefficiency is inferred from duration, not directly labeled.
- Several groups are small (`Database`, `Inquiry / Help`, `Low` priority), so those comparisons are weak.
- `sys_updated_on` matches `closed_at` in all rows, so post-close update lag is not a usable signal.

## Decision-ready takeaway
The most useful warning signs for inefficient resolution are **workflow/ownership signals** (`assigned_to`, `closed_by`, `sys_updated_by`), a ticket ending in **`Resolved` rather than `Closed`**, and **short descriptions that imply non-routine endpoint troubleshooting**. By contrast, **category** and **priority** are much weaker screening fields in this dataset.
