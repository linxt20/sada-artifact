---
dataset: flag_2
scenario: predictive_long
variant: original
model: substrate-claude-haiku-4-5
query_subtype: predictive_feature_engineering
focus_variable: "resolution_time"
query: "What signals suggest an incident will take longer to resolve?"
source_table: augment_table/flag_2/predictive_long/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_2__predictive_long/analyses/original/analysis.md
wall_seconds: 146.61
---

# Signals that suggest longer incident resolution

- Analysis uses the 372 records with both `opened_at` and `closed_at`. Resolution time is computed as `closed_at - opened_at`.
- Typical resolution is already long in this dataset: median $= 1032.0$ hours, and the top quartile of longer cases starts at $1557.6$ hours.

## Strongest signal by far: later `opened_at` date

- `opened_at` month is the clearest predictor of a longer resolution.
- Median resolution rises almost perfectly month by month:
  - January: $135.6$ hours
  - February: $362.4$
  - March: $517.2$
  - April: $772.8$
  - May: $1032.0$
  - June: $1244.4$
  - July: $1438.8$
  - August: $1629.6$
  - September: $1881.6$
  - October: $2104.8$
- This pattern is so strong that calendar timing appears to dominate all other fields. It is likely a dataset artifact, not a normal operational signal, so it should be validated before use.

## Secondary signals: network/connectivity work trends longer

These effects are much weaker than the `opened_at` trend, but they are directionally consistent.

- `assignment_group = Network`: median $1046.4$ hours; long-case rate $27.1\%$ (`n=221`)
- `category = Network`: median $1046.4$ hours; long-case rate $27.9\%$ (`n=197`)
- Compared with:
  - `category = Database`: $967.2$ hours; $20.9\%$ long (`n=86`)
  - `category = Inquiry / Help`: $686.4$ hours; $14.3\%$ long (`n=7`)

`short_description` wording supports the same pattern:

- contains **connectivity**: median $1262.4$ hours; $41.7\%$ long (`n=36`)
- contains **network**: $1424.4$ hours; $37.5\%$ long (`n=16`)
- contains **vpn**: $1100.4$ hours; $30.0\%$ long (`n=80`)

Lower-duration terms include:

- **database**: $967.2$ hours; $19.5\%$ long (`n=82`)
- **connection**: $816.0$ hours; $12.8\%$ long (`n=39`)

## Weak evidence: time of day

- Incidents opened overnight are somewhat slower in raw terms:
  - `opened_at` 00:00-05:59: median $1276.8$ hours; $29.2\%$ long
  - 06:00-11:59: median $837.6$ hours; $19.3\%$ long
- This effect is modest and may partly reflect the same date-driven pattern above.

## Signals with limited value

- `priority` is not a reliable separator:
  - `1 - Critical`: median $1255.2$ hours; $28.1\%$ long (`n=57`)
  - `2 - High`: $974.4$ hours; $24.0\%$ long (`n=283`)
  - `3 - Moderate`: $1100.4$ hours; $31.3\%$ long (`n=32`)
- Person fields such as `assigned_to`, `closed_by`, `caller_id`, and `sys_updated_by` show raw differences, but those are weak compared with the calendar effect and should not be treated as stable causal signals.
- `state` adds little: `Closed` and `Resolved` have similar medians ($1068.0$ vs $960.0$ hours).

## Bottom line

- In this dataset, the main signal for a long resolution is a later `opened_at` date/month.
- Because that effect is nearly deterministic, it is likely an artifact and should not be operationalized without validation.
- If non-calendar signals are needed, the best available secondary indicators are **network / connectivity / VPN-related incidents** and, more weakly, **overnight-opened incidents**.
- `priority` and individual assignee/caller fields provide weak evidence.
