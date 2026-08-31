---
dataset: flag_6
scenario: predictive_resolution
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary by agent and issue type?"
source_table: augment_table/flag_6/predictive_resolution/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_6__predictive_resolution/analyses/original/analysis.md
wall_seconds: 72.02
---

# Resolution time by agent and issue type

**Basis.** Resolution time was derived as $closed\_at - opened\_at$, using tickets in terminal states (`Closed` or `Resolved`). Out of 500 rows, 428 were usable for timing analysis; 50 terminal tickets had negative durations from inconsistent timestamps, and 22 tickets were still `New` or `In Progress`.

## Bottom line

Resolution time varies **much more by agent than by issue type** in this dataset.

- **Beth Anglin** has the shortest overall median resolution time at **124 hours** (~**5.2 days**, $n=85$).
- **Howard Johnson**, **Charlie Whitherspoon**, and **Luke Wilson** are fairly similar overall at **143-151 hours** (~**6.0-6.3 days**).
- **Fred Luddy** is the clear outlier at **691 hours** (~**28.8 days**, $n=76$), and he is slower in **every major issue type**.

By issue type overall:

- **Hardware:** **123 hours** median (~**5.1 days**, $n=25$)
- **Database:** **143 hours** (~**6.0 days**, $n=90$)
- **Network:** **177 hours** (~**7.4 days**, $n=242$)
- **Software:** **188 hours** (~**7.8 days**, $n=64$)
- **Inquiry / Help:** **176 hours** (~**7.4 days**, $n=7$; weak evidence)

## By agent

| Agent (`assigned_to`) | Usable tickets | Median resolution |
|---|---:|---:|
| Beth Anglin | 85 | 124 hours |
| Howard Johnson | 88 | 143 hours |
| Charlie Whitherspoon | 89 | 150 hours |
| Luke Wilson | 90 | 151 hours |
| Fred Luddy | 76 | 691 hours |

**Interpretation:**  
The main operational split is **Fred Luddy versus everyone else**. The other four agents cluster within about one day of each other, while Fred’s median is roughly **4.5x-5.5x longer**.

## By issue type

| Issue type (`category`) | Usable tickets | Median resolution | Readout |
|---|---:|---:|---|
| Hardware | 25 | 123 hours | Fastest overall, but low volume |
| Database | 90 | 143 hours | Mid-range |
| Network | 242 | 177 hours | Slower and highest volume |
| Software | 64 | 188 hours | Slowest major category overall |
| Inquiry / Help | 7 | 176 hours | Too few cases for a strong conclusion |

**Interpretation:**  
`Network` and `Software` tend to take longer than `Database` and `Hardware`, but these issue-type differences are modest compared with the agent effect.

## Agent-by-issue interaction

Median resolution time in hours:

| Agent | Database | Hardware | Network | Software |
|---|---:|---:|---:|---:|
| Beth Anglin | 110 | 102 | 122 | 150 |
| Charlie Whitherspoon | 146 | 247 | 152 | 78 |
| Howard Johnson | 131 | 123 | 165 | 90 |
| Luke Wilson | 100 | 78 | 174 | 171 |
| Fred Luddy | 646 | 86* | 682 | 833 |

\*Fred Luddy’s `Hardware` median is based on only **3** tickets.

### Important patterns

- **Network** is the largest category and shows meaningful spread by agent:  
  **Beth** is fastest at **122 hours**, then **Charlie** (**152**), **Howard** (**165**), **Luke** (**174**), while **Fred** is far slower at **682**.
- **Database** shows a similar pattern:  
  **Luke** is fastest at **100 hours**, **Beth** next at **110**, and **Fred** again much slower at **646**.
- **Software** is where non-Fred differences are most visible:  
  **Charlie** (**78 hours**) and **Howard** (**90**) resolve much faster than **Beth** (**150**) and **Luke** (**171**); **Fred** is again extreme at **833**.
- **Hardware** should be treated cautiously because counts are small for several agents (for example, **Luke** and **Fred** each have only **3** usable tickets).

## Exceptions and evidence strength

- The strongest finding is **Fred Luddy’s consistently long resolution times**. This is not explained by category mix alone, because he is slow across `Database`, `Network`, and `Software`, and the **10 longest valid tickets** in the dataset are all assigned to him.
- The apparent speed differences among **Beth**, **Howard**, **Charlie**, and **Luke** are real but much smaller. They may matter operationally, but they are not large enough here to justify strong performance claims without more context.
- `Inquiry / Help` is too sparse to rely on, and several agent-category cells have only **1-3** tickets.
- Data quality matters: **50 negative durations** indicate timestamp problems, so exact hour values should be treated as directional rather than exact.

## Decision-ready takeaway

If the goal is to reduce resolution time, the first place to investigate is **agent-level variation**, especially the backlog or workflow behind **Fred Luddy’s** tickets. Issue type matters too—`Network` and `Software` are generally slower—but category alone does **not** explain the largest delays. Among the other agents, **Beth Anglin** is the fastest overall, while **software work** appears especially efficient for **Charlie Whitherspoon** and **Howard Johnson**.
