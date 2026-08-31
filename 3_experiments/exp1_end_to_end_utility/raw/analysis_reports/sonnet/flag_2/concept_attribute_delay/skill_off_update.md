---
dataset: flag_2
scenario: concept_attribute_delay
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "incident_delay_reasons"
query: "Why do some incidents take longer to resolve?"
source_table: augment_table/flag_2/concept_attribute_delay/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:15:37.335526+00:00
wall_seconds: 56.71
---

# Incident Resolution Delay Analysis
**Dataset:** `sonnet__skill_off_update.csv` | **Variant:** `skill_off` | **n = 500 (372 with resolution_hours)**

---

## Summary

Resolution times range from **24 to 2,205.6 hours** (mean ≈ 1,043 h, median ≈ 1,032 h), indicating substantial variation. No single factor explains delays decisively — several moderate contributors operate together.

---

## Key Factors Examined

### 1. Assigned Agent
The clearest human-factor signal: agent identity correlates with meaningfully different mean resolution times.

| Agent | Mean Resolution Hours |
|---|---|
| Howard Johnson | 952.8 |
| Luke Wilson | 967.5 |
| Charlie Whitherspoon | 1,035.5 |
| Fred Luddy | 1,125.4 |
| Beth Anglin | 1,141.9 |

Beth Anglin and Fred Luddy average ~190 h longer than the fastest agents. In the **slowest quartile** (≥75th percentile), Beth Anglin handles 25.5% of incidents vs. only 18.3% in the fastest quartile — consistent with agent-level capacity or skill differences influencing delays. However, confounding by workload distribution cannot be ruled out.

### 2. Assignment Group
| Group | Mean Resolution Hours |
|---|---|
| Hardware | 925.8 |
| Database | 946.5 |
| Software | 1,028.3 |
| Network | 1,074.0 |
| Service Desk | 1,102.4 |
| Openspace | 1,852.8 *(n=1)* |

Network and Service Desk groups resolve ~150–175 h slower than Hardware/Database. The **Openspace** entry (1,852.8 h) is a single outlier and should not be generalised.

### 3. Priority
Priority shows a **counterintuitive, weak pattern**: Critical and Moderate incidents average slightly *longer* (~1,119 h) than High-priority ones (~1,019 h). The Pearson correlation between `priority_numeric` and `resolution_hours` is only **–0.016**, effectively negligible. Priority escalation does not reliably accelerate resolution in this dataset.

### 4. Weekend / Day of Opening
Incidents opened on weekends resolve ~54 h longer on average than weekday incidents (1,081 h vs. 1,027 h). Saturday is the worst single day (1,104 h). This effect is real but modest — weekend coverage gaps may contribute to initial response lag.

### 5. Category Mismatch
`category_mismatch = 1` adds only ~7.6 h on average (1,050 h vs. 1,043 h) with near-zero correlation (r = 0.004). Misrouting is **not** a meaningful driver of delay in this data.

### 6. Hour of Opening
Opening hour has a weak negative correlation with resolution time (r = –0.059): incidents opened later in the day resolve marginally faster, but the effect is negligible.

---

## Missing Data Note
128 of 500 records (25.6%) have no `resolution_hours` (not yet resolved or data not captured). If unresolved incidents are systematically harder, the true mean delay may be understated.

---

## Conclusions

| Factor | Direction | Strength |
|---|---|---|
| Assigned agent | Beth Anglin / Fred Luddy slower | Moderate |
| Assignment group | Network/Service Desk slower | Moderate |
| Weekend opening | Slight increase in delay | Weak–Moderate |
| Priority | No reliable relationship | Negligible |
| Category mismatch | No meaningful impact | Negligible |

**The most actionable finding** is that agent- and group-level differences account for the most visible delay patterns. Incidents routed to Beth Anglin, Fred Luddy, or the Network/Service Desk group consistently take longer, suggesting workload balancing or targeted skill development may reduce resolution times. Priority triage, contrary to expectation, does not appear to accelerate resolution.
