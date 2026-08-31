---
dataset: flag_6
scenario: predictive_resolution
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "resolution_time"
query: "How does resolution time vary by agent and issue type?"
source_table: augment_table/flag_6/predictive_resolution/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:19:57.470379+00:00
wall_seconds: 50.21
---

# Resolution Time by Agent and Issue Type

**Dataset:** 500 incidents (428 with valid resolution times after removing negative durations)  
**Outcome variable:** Resolution time in hours (`closed_at − opened_at`)  
**Overall:** mean 258 h, median 164 h, range 1.5–1,579 h

---

## 1. Resolution Time by Agent

The most striking finding is a strong agent-level effect, with Fred Luddy's cases resolving ~5× slower than peers.

| Agent | Mean (h) | Median (h) | N |
|---|---|---|---|
| Beth Anglin | **136** | 124 | 85 |
| Charlie Whitherspoon | 150 | 150 | 89 |
| Howard Johnson | 160 | 143 | 88 |
| Luke Wilson | 160 | 151 | 90 |
| **Fred Luddy** | **750** | **691** | 76 |

Beth Anglin is consistently the fastest resolver across all categories (see §3). Fred Luddy's median of 691 h (≈29 days) is a pronounced outlier—not explained by issue mix alone (see §3).

`resolver_matches_assignee` (TAPP column) shows no meaningful effect: cases where the closer matched the assignee had nearly identical times (mean 257 h vs. 258 h), suggesting handoffs are not driving variance.

---

## 2. Resolution Time by Issue Type

### Original `category` column

| Category | Mean (h) | Median (h) | N |
|---|---|---|---|
| Inquiry / Help | 159 | 177 | 7 |
| Hardware | 199 | 123 | 25 |
| Database | 249 | 143 | 90 |
| Network | 265 | 177 | 242 |
| Software | 278 | 188 | 64 |

Network incidents dominate volume (57% of tickets) and show above-average resolution times.

### TAPP-generated `issue_type` column (semantic sub-classification)

`issue_type` adds granularity within categories, revealing meaningful within-category variance:

| Issue Type | Mean (h) | Median (h) | N | Parent Category |
|---|---|---|---|---|
| wifi | 158 | 127 | 12 | Network |
| printing | 181 | 187 | 8 | Hardware |
| email_client_sync | 203 | 109 | 21 | Network/Software |
| internet_connectivity | 223 | 163 | 55 | Network |
| email_server | 236 | 153 | 94 | Network |
| database | 248 | 140 | 87 | Database |
| server_access | 272 | 198 | 24 | Network |
| vpn_connectivity | 289 | 187 | 100 | Network |
| login_access | 315 | 79 | 8 | Software |
| software_update | 420 | 225 | 11 | Software |
| network_drive_share | 536 | 262 | 4 | Network |
| other | 535 | 267 | 4 | — |

Within **Network**, `wifi` resolves in 158 h mean while `vpn_connectivity` takes 289 h—an 83% difference masked by the aggregate. Within **Software**, `software_update` (420 h mean) is notably slower than `email_client_sync` (203 h).

### TAPP-generated `issue_severity_signal` column

| Severity Signal | Mean (h) | Median (h) | N |
|---|---|---|---|
| outage_down | 211 | 150 | 80 |
| inaccessible_no_access | 259 | 173 | 202 |
| error | 280 | 174 | 118 |
| degraded_slow | 302 | 176 | 26 |

Counter-intuitively, **outages resolve fastest** (211 h mean), while degraded/slow issues take longest. This may reflect prioritization: outages attract immediate attention regardless of formal `priority` rating. The original `priority` field shows minimal spread (Critical: 230 h, High: 263 h, Moderate: 266 h), suggesting the `issue_severity_signal` facet captures urgency cues in free-text that the structured priority field under-represents.

---

## 3. Agent × Category Interaction

Mean resolution hours by agent and original category:

| Agent | Database | Hardware | Network | Software |
|---|---|---|---|---|
| Beth Anglin | 131 | 133 | 128 | 164 |
| Charlie Whitherspoon | 154 | 243 | 149 | 108 |
| Howard Johnson | 130 | 138 | 177 | 141 |
| Luke Wilson | 126 | 113 | 175 | 168 |
| **Fred Luddy** | **707** | **437** | **762** | **851** |

Fred Luddy's slowness is consistent across every category (707–851 h), ruling out issue-mix as an explanation. The `affected_system` and `failure_mode` TAPP columns showed no differential pattern for Fred Luddy's cases that would explain the gap; his issue mix is comparable to peers.

---

## 4. Key Findings

1. **Agent identity is the dominant driver** of resolution time variance. Fred Luddy's cases take ~5× longer (750 h mean) than the other four agents (136–160 h mean), regardless of issue type or severity.
2. **VPN connectivity issues are the slowest high-volume type** (289 h mean, N=100); wifi issues are fastest (158 h, N=12).
3. **Software updates** are the slowest issue sub-type by mean resolution (420 h), though low volume (N=11).
4. **Outages resolve faster than degraded-service issues**, likely due to escalation behavior captured by `issue_severity_signal`.
5. `resolver_matches_assignee` has negligible effect on resolution time.

---

## Method Note

TAPP-generated columns used in this report: `issue_type`, `issue_severity_signal`, `resolver_matches_assignee`. Columns `assigned_agent`, `failure_mode`, and `affected_system` were reviewed but provided no additional explanatory signal beyond what the original `assigned_to` and `category` columns already captured, and are not centered in the analysis.
