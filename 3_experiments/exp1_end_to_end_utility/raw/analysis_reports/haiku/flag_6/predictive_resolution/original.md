---
dataset: flag_6
scenario: predictive_resolution
variant: original
model: substrate-claude-haiku-4-5
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary by agent and issue type?"
source_table: augment_table/flag_6/predictive_resolution/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_6__predictive_resolution/analyses/original/analysis.md
wall_seconds: 93.31
---

# Resolution time by agent and issue type

**Method.** Resolution time was computed as `closed_at - opened_at`. For comparison, the analysis used tickets with a non-null `closed_at`, a named `assigned_to`, and a non-negative duration: **428 of 500** rows. Excluded were **22** still-open tickets (`state` = `New` or `In Progress`) and **50** rows where `closed_at < opened_at`, which is a visible timestamp anomaly.

## 1) Agent differences are larger than issue-type differences

Median resolution time by `assigned_to`:

| Agent | Valid tickets | Median resolution |
|---|---:|---:|
| Beth Anglin | 85 | 124 h |
| Howard Johnson | 88 | 143 h |
| Charlie Whitherspoon | 89 | 150 h |
| Luke Wilson | 90 | 151 h |
| Fred Luddy | 76 | 691 h |

**Readout:** Beth is the fastest on typical tickets, Howard/Charlie/Luke are fairly close to each other, and Fred is a strong outlier with much longer times.

## 2) Issue type matters, but part of that effect is agent mix

Overall median resolution by `category`:

| Issue type | Valid tickets | Median resolution |
|---|---:|---:|
| Hardware | 25 | 123 h |
| Database | 90 | 143 h |
| Inquiry / Help | 7 | 176 h |
| Network | 242 | 177 h |
| Software | 64 | 188 h |

**Readout:** Across all agents, `Network` and `Software` resolve slower than `Database` and `Hardware`. However, that pattern is partly driven by who handled the work.

## 3) Agent-by-issue pattern

Median hours by `assigned_to` × `category`:

| Agent | Database | Hardware | Inquiry / Help | Network | Software |
|---|---:|---:|---:|---:|---:|
| Beth Anglin | 110 h (n=14) | 102 h (n=5) | 179 h (n=1) | 122 h (n=48) | 150 h (n=17) |
| Charlie Whitherspoon | 146 h (n=17) | 247 h (n=7) | 78 h (n=1) | 152 h (n=50) | 78 h (n=14) |
| Fred Luddy | 646 h (n=18) | 86 h (n=3) | — | 682 h (n=43) | 833 h (n=12) |
| Howard Johnson | 131 h (n=19) | 123 h (n=7) | 176 h (n=5) | 165 h (n=48) | 90 h (n=9) |
| Luke Wilson | 100 h (n=22) | 78 h (n=3) | — | 174 h (n=53) | 171 h (n=12) |

## 4) Decision-ready interpretation

- **Fred Luddy drives the slowest outcomes.** His median times are very high for `Database`, `Network`, and `Software` (646–833 h). This is the clearest agent effect in the table.
- **For Beth, Howard, and Luke, `Network` tends to be slower than `Database` and `Hardware`.**  
  - Beth: `Network` 122 h vs `Database` 110 h / `Hardware` 102 h  
  - Howard: `Network` 165 h vs `Database` 131 h / `Hardware` 123 h  
  - Luke: `Network` 174 h vs `Database` 100 h / `Hardware` 78 h
- **Charlie is the main exception.** His `Software` tickets are fast (78 h), while his `Hardware` tickets are slow (247 h), and his `Network`/`Database` work sits in the middle.
- **The global issue-type ranking overstates category effects.** If Fred is excluded, overall category medians compress substantially: `Database` 124 h, `Hardware` 124 h, `Software` 129 h, `Network` 153 h. That suggests **agent assignment explains more variation than issue type alone**.

## 5) Important caveats

- **Timestamp quality is imperfect.** There are **50 negative-duration rows**, concentrated in `Network` (29 rows). Those records weaken confidence in fine-grained comparisons.
- **Some cells are small.** `Inquiry / Help` has only **7** valid tickets total; several `Hardware` cells have only **3–7** tickets. Those results are directional, not strong evidence.
- **Open work is not counted in resolution time.** The 22 open tickets are mostly `Network`, and 8 are assigned to Fred Luddy, so resolved-only timing may understate current backlog effects.

## Bottom line

Resolution time varies **more by agent than by issue type** in this dataset. `Network` and `Software` look slower overall, but much of that pattern is explained by **who handled the ticket**, especially the very long durations on Fred Luddy’s `Network`, `Database`, and `Software` cases. For operational decisions, prioritize **agent-level workload/process review** first, then treat `Network` as the issue type most consistently associated with slower resolution across multiple agents.
