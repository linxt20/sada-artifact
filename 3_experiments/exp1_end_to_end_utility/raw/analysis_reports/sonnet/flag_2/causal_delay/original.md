---
dataset: flag_2
scenario: causal_delay
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: causal_attribution
focus_variable: "resolution_time"
query: "Controlling for priority and category, which underlying causes explain longer resolution times?"
source_table: augment_table/flag_2/causal_delay/original.csv
generated_at: 2026-07-26T13:26:08.936386+00:00
wall_seconds: 107.99
---

# Causal Delay Analysis: Underlying Causes of Longer Resolution Times

**Dataset:** 500 incidents | **Valid resolution times:** 372 (128 records lack `closed_at`)  
**Variant:** original

---

## Summary

After controlling for **priority** and **category**, the dominant causal drivers of longer resolution times are **incident category** (especially Hardware and Software), **assignment group routing**, **assigned agent**, and — to a lesser degree — **category/group misrouting**. Priority alone is a weak predictor of delay in this dataset.

---

## 1. Priority Is a Weak Delay Signal

| Priority | n | Avg Resolution (hrs) | Median (hrs) |
|---|---|---|---|
| 1 - Critical | 57 | 1,119 | 1,255 |
| 2 - High | 283 | 1,020 | 974 |
| 3 - Moderate | 32 | 1,121 | 1,104 |

Counter-intuitively, **3 - Moderate** incidents take as long as **1 - Critical** ones on average. Priority does not consistently predict faster resolution, which means the causal delay signal lies elsewhere.

---

## 2. Category Is the Strongest Structural Predictor

| Category | n | Avg Resolution (hrs) | Median (hrs) |
|---|---|---|---|
| Hardware | 12 | **1,105** | 1,032 |
| Network | 197 | **1,079** | 1,046 |
| Software | 70 | **1,051** | 1,061 |
| Inquiry / Help | 7 | 958 | 686 |
| Database | 86 | **955** | 974 |

**Hardware** and **Network** incidents resolve slowest on average. **Database** and **Inquiry / Help** resolve fastest — Database notably about 120 hours faster than Network despite similar volume and priority mix.

### Cross-tab: Category × Priority

| Category | Priority | n | Avg (hrs) |
|---|---|---|---|
| Software | 3 - Moderate | 16 | **1,233** |
| Database | 1 - Critical | 13 | **1,244** |
| Network | 3 - Moderate | 7 | **1,211** |
| Network | 2 - High | 153 | **1,082** |
| Database | 2 - High | 68 | 910 |
| Database | 3 - Moderate | 5 | **818** |

Key finding: **Software tickets at Moderate priority** are unexpectedly slow (~1,233 h avg), suggesting these are deprioritized despite being complex. **Database tickets at Critical priority** also run long (~1,244 h), pointing to deep technical complexity when database failures are severe. **Database at Moderate/High** resolves significantly faster (~818–910 h), indicating a bimodal difficulty pattern in that category.

---

## 3. Assignment Group Routing Matters

| Assignment Group | n | Avg (hrs) | Median (hrs) |
|---|---|---|---|
| Service Desk | 32 | **1,102** | 1,162 |
| Network | 221 | **1,074** | 1,046 |
| Software | 25 | 1,028 | 823 |
| Database | 89 | 947 | 960 |
| Hardware | 4 | 926 | 888 |

**Service Desk** and **Network group** handle the longest-running tickets. Service Desk is a triage/generalist queue — incidents assigned there without specialist routing take ~156 h longer than the Database group. Note: there is 1 "Openspace" record (1,853 h avg) but it is a single outlier with no statistical weight.

**Category–Group mismatch** (e.g., a Network category incident routed to Service Desk) adds a modest ~39 h average delay (1,075 h vs 1,036 h for matched cases). This is suggestive but not dramatic, given sample sizes.

---

## 4. Assigned Agent Effect

| Agent | n | Avg (hrs) | Median (hrs) |
|---|---|---|---|
| Beth Anglin | 73 | **1,142** | 1,298 |
| Fred Luddy | 74 | **1,125** | 1,104 |
| Charlie Whitherspoon | 71 | 1,036 | 1,061 |
| Luke Wilson | 85 | 968 | 816 |
| Howard Johnson | 69 | 953 | 910 |

**Beth Anglin** and **Fred Luddy** have the highest average resolution times (~190 h above Howard Johnson/Luke Wilson). This agent-level disparity persists across similar volumes of cases and may reflect workload concentration, specialization fit, or the types of tickets assigned to them. However, without controlling for which categories each agent handles, this should be treated as a hypothesis rather than a confirmed cause.

---

## 5. Incident Description Patterns (Proxy for Underlying Cause Type)

Short-description keyword analysis identifies issue *types* linked to the longest delays (among clusters with n ≥ 3):

| Description Pattern | n | Avg (hrs) |
|---|---|---|
| "email service not [responding]" | 4 | **1,613** |
| "software update required" | 3 | **1,591** |
| "database server not [responding]" | 3 | **1,565** |
| "email server connectivity" | 6 | **1,556** |
| "server connectivity issue" | 3 | **1,430** |

**Email service/server issues** and **software update failures** are the longest-tailed issue types — significantly exceeding category averages. This suggests that **service-level outages** (vs. user-level access problems) drive disproportionate delay.

---

## Key Findings (Decision-Ready)

1. **Category > Priority** as a delay predictor. Hardware and Network categories, and Software at Moderate priority, are the slowest segments.
2. **Critical-priority Database incidents** are unexpectedly slow (~1,244 h), suggesting major database failures require escalation paths that are not accelerated.
3. **Service Desk assignment** is a delay amplifier — incidents not routed directly to a specialist group take longer.
4. **Agent assignment** shows a meaningful spread (~190 h between fastest and slowest), warranting workload and skill-fit review for Beth Anglin and Fred Luddy.
5. **Email service outages and software update issues** are the worst-performing underlying issue types by description, exceeding even their category averages by 400–500 h.
6. **Caveats:** 128/500 records (26%) lack `closed_at` and are excluded; mismatch routing effect is modest; agent effects are unadjusted for category mix.
