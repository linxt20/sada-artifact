---
dataset: flag_2
scenario: eda_resolution
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary across category, priority, and assignment group?"
source_table: augment_table/flag_2/eda_resolution/original.csv
generated_at: 2026-07-26T13:27:45.734207+00:00
wall_seconds: 94.91
---

# Resolution Time Analysis: Category, Priority, and Assignment Group

**Dataset:** `original.csv` — 500 IT incident records  
**Focus variable:** Resolution time (hours), computed as `closed_at − opened_at` for tickets in **Resolved** or **Closed** state (n = 372; 128 tickets in *New* or *In Progress* states are excluded).

---

## Overall Baseline

| Metric | Value |
|--------|-------|
| Valid (closed/resolved) tickets | 372 |
| Mean resolution time | **1,043 h (~43 days)** |
| Median resolution time | **1,032 h (~43 days)** |

Resolution times are very long (measured in weeks, not hours), suggesting these incidents reflect long-running service requests rather than quick break-fix tickets, or that timestamps span calendar time including non-working hours.

---

## 1. Resolution Time by Category

| Category | n | Mean (h) | Median (h) | P25 (h) | P75 (h) | Max (h) |
|---|---|---|---|---|---|---|
| Database | 86 | 955 | 974 | 499 | 1,342 | 2,170 |
| Hardware | 12 | 1,105 | 1,032 | 614 | 1,795 | 1,997 |
| Inquiry / Help | 7 | 958 | 686 | 463 | 1,486 | 2,018 |
| Network | 197 | 1,079 | 1,046 | 492 | 1,601 | 2,198 |
| Software | 70 | 1,051 | 1,061 | 535 | 1,486 | 2,206 |

**Key patterns:**
- **Database** resolves fastest on average (mean 955 h, median 974 h), with a tighter spread compared to other categories.
- **Hardware** has the highest mean (1,105 h), though its sample is small (n = 12); wide interquartile range (614–1,795 h) indicates high variability and weak evidence.
- **Network** dominates volume (197 of 372 closed tickets, 53%) with a moderate mean (1,079 h); its distributions are broadly similar to Software.
- **Inquiry / Help** has the lowest median (686 h) but a small sample (n = 7) and a high max (2,018 h), making this unreliable.

**Conclusion:** Category differences exist but are modest (spread of ~150 h in means). Database tends to close slightly faster; Hardware appears slower but is under-sampled.

---

## 2. Resolution Time by Priority

| Priority | n | Mean (h) | Median (h) | P25 (h) | P75 (h) | Max (h) |
|---|---|---|---|---|---|---|
| 1 - Critical | 57 | 1,119 | 1,255 | 506 | 1,637 | 2,170 |
| 2 - High | 283 | 1,020 | 974 | 506 | 1,493 | 2,206 |
| 3 - Moderate | 32 | 1,121 | 1,104 | 442 | 1,925 | 2,198 |

**Key patterns:**
- **Counterintuitively, Critical (P1) tickets do NOT resolve faster** than High (P2) tickets. P1 mean (1,119 h) is ~10% higher than P2 (1,020 h), and P1 median (1,255 h) is notably higher than P2 (974 h).
- **Moderate (P3)** tickets have the highest mean (1,121 h) and the widest spread (P75 = 1,925 h), though n = 32.
- **High (P2)** is both the dominant priority class (76% of closed tickets) and the quickest to resolve.

**Conclusion:** Priority does not correlate with resolution speed in the expected direction. This may reflect escalation complexity for critical issues, or insufficient SLA enforcement. Decision-makers should investigate whether critical tickets face bottlenecks not captured here.

---

## 3. Resolution Time by Assignment Group

| Assignment Group | n | Mean (h) | Median (h) | P25 (h) | P75 (h) | Max (h) |
|---|---|---|---|---|---|---|
| Database | 89 | 947 | 960 | 499 | 1,334 | 2,170 |
| Hardware | 4 | 926 | 888 | 701 | 1,997 | 1,997 |
| Network | 221 | 1,074 | 1,046 | 499 | 1,594 | 2,206 |
| Openspace | 1 | 1,853 | — | — | — | 1,853 |
| Service Desk | 32 | 1,102 | 1,162 | 629 | 1,515 | 2,198 |
| Software | 25 | 1,028 | 823 | 535 | 1,903 | 2,162 |

**Key patterns:**
- **Database group** resolves fastest (mean 947 h, median 960 h), consistent with the category-level finding.
- **Network group** handles the largest volume (221 tickets, 59%) and is moderately slow (mean 1,074 h).
- **Service Desk** is slower than Database or Network (mean 1,102 h, median 1,162 h), possibly routing tickets that are harder to close definitively.
- **Hardware** group is fast (mean 926 h) but with only 4 tickets — results are not reliable.
- **Openspace** has a single ticket (1,853 h) — no conclusions can be drawn.
- **Software** group shows a wide gap between mean (1,028 h) and median (823 h), suggesting right-skew from a few outliers with very long resolution times.

**Conclusion:** The Database group is consistently the fastest resolver. Network's dominance in volume makes it the most operationally significant group to optimize.

---

## Summary & Exceptions

| Factor | Direction | Strength |
|--------|-----------|----------|
| Category | Database faster; Hardware slightly slower | Moderate (small Hardware n) |
| Priority | No expected gradient; P2 resolves faster than P1 | Counterintuitive — investigate |
| Assignment Group | Database group fastest; Service Desk slowest among well-sampled groups | Moderate |

**Important caveats:**
- 128 tickets (26%) remain open (*New* / *In Progress*) and are excluded; if higher-priority tickets are disproportionately open, the priority comparison is biased.
- Hardware and Inquiry/Help categories, and Hardware/Openspace assignment groups, have very small sample sizes (≤ 12 tickets) — patterns there are weak evidence.
- The absence of an escalation path or SLA breach flag in the dataset limits causal interpretation.
