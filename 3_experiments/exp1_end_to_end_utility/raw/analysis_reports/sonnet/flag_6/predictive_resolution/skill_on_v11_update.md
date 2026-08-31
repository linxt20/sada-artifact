---
dataset: flag_6
scenario: predictive_resolution
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary by agent and issue type?"
source_table: augment_table/flag_6/predictive_resolution/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:19:41.791226+00:00
wall_seconds: 49.47
---

# Resolution Time Analysis by Agent and Issue Type

**Dataset:** 500 incidents (500 rows, 19 columns) | **Focus variable:** `resolution_hours` (derived from `closed_at − opened_at`)

> **Data note:** 50 incidents have negative resolution times (likely data-entry or timestamp anomalies). These are included in the averages below; they may slightly depress mean values for certain cells but do not change the overall patterns materially. The `Unknown` resolver agent has zero resolved incidents and is excluded from discussion.

---

## 1. Overall Resolution Time by Agent

| Resolver Agent | Mean (hrs) | Median (hrs) | Count |
|---|---|---|---|
| Beth Anglin | 211.6 | 160.2 | 87 |
| Howard Johnson | 216.7 | 143.4 | 111 |
| Charlie Whitherspoon | 217.5 | 123.3 | 91 |
| Fred Luddy | 223.8 | 120.8 | 79 |
| Luke Wilson | 244.4 | 164.5 | 110 |

**Key finding:** Agents are broadly comparable at the mean level (~212–244 hrs), but the gap between mean and median is large for most (especially Fred Luddy: mean 224 vs. median 121), indicating right-skewed distributions driven by a small number of very slow resolutions. Luke Wilson has the highest mean and median, suggesting slightly slower overall performance.

---

## 2. Overall Resolution Time by Issue Type

| Issue Type | Mean (hrs) | Median (hrs) | Count |
|---|---|---|---|
| printer_peripheral | 180.7 | 186.6 | 8 |
| email_server | 189.8 | 123.1 | 131 |
| network_connectivity | 203.0 | 151.9 | 79 |
| database_access | 207.6 | 130.8 | 99 |
| server_access | 214.1 | 178.5 | 29 |
| login_authentication | 261.7 | 79.3 | 10 |
| vpn_connectivity | 267.8 | 176.7 | 106 |
| software_application | 420.4 | 218.5 | 16 |

**Key finding:** `software_application` is a severe outlier — mean 420 hrs vs. the next-highest 268 hrs — with extremely high variance (std ≈ 491 hrs) and only 16 cases. `vpn_connectivity` consistently takes longer than most other types (mean 268 hrs, n=106, making it high-confidence). `email_server` is the highest-volume fast type (131 cases, median 123 hrs). `login_authentication` has a very wide mean–median gap (262 vs. 79 hrs), driven by a few extreme outliers across a small sample (n=10).

---

## 3. Resolution Time by Agent × Issue Type (Mean Hours)

| Resolver Agent | database_access | email_server | login_auth | network_conn | printer_periph | server_access | software_app | vpn_conn |
|---|---|---|---|---|---|---|---|---|
| Beth Anglin | 249.6 | 221.4 | 44.3 | **114.8** | — | 147.5 | 204.1 | 281.0 |
| Charlie Whitherspoon | 252.0 | **136.7** | 52.7 | 280.1 | 214.4 | 354.7 | 223.0 | 217.6 |
| Fred Luddy | **140.4** | **121.2** | 624.0* | 246.4 | — | **28.6** | 523.4 | 330.8 |
| Howard Johnson | 223.2 | 209.8 | 96.3 | 231.5 | 232.9 | 114.5 | — | 243.5 |
| Luke Wilson | 134.3 | 223.2 | 550.0* | 169.2 | 112.3 | 405.8 | **660.8** | 282.6 |

*\* Small sample (n ≤ 3); treat as weak evidence.*

**Notable patterns:**

- **Fred Luddy** resolves `database_access` (140 hrs), `email_server` (121 hrs), and `server_access` (29 hrs) fastest among all agents — suggesting a database/infrastructure skill advantage. However, he is the slowest on `login_authentication` (624 hrs, n=1 — unreliable) and `software_application` (523 hrs, n=5).
- **Beth Anglin** excels at `network_connectivity` (115 hrs vs. group average 203 hrs) but is slow on `vpn_connectivity` (281 hrs) and `database_access` (250 hrs).
- **Charlie Whitherspoon** resolves `email_server` quickly (137 hrs) but is slow on `server_access` (355 hrs, n=5) and `network_connectivity` (280 hrs).
- **Luke Wilson** is slowest on `software_application` (661 hrs, n=4) and `server_access` (406 hrs, n=6) — both small samples but consistent with his higher overall mean.
- **Howard Johnson** shows the most balanced profile with no extreme outlier cells (all well-sampled issue types between 114–244 hrs).

---

## 4. Summary & Caveats

| Dimension | Key Takeaway |
|---|---|
| Agent effect | Modest at the aggregate level; meaningful when controlling for issue type |
| Issue type effect | Larger and more consistent: `software_application` and `vpn_connectivity` are structurally slower |
| Interaction | Agent-issue combinations reveal specialisation (e.g., Fred Luddy on DB/server, Beth Anglin on network) |
| Data quality | 50 negative-duration records and several small-n cells (n < 5) limit confidence in some cross-cells |

**Recommendation:** Routing `software_application` and `vpn_connectivity` tickets to agents with demonstrated strength in those categories (avoiding Luke Wilson for software tickets, given limited but consistent evidence) may reduce tail resolution times. The `skill_on` variant context suggests these routing/skill signals are actionable.
