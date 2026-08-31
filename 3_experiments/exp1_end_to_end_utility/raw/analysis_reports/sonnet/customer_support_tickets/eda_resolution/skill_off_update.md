---
dataset: customer_support_tickets
scenario: eda_resolution
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_minutes"
query: "How does resolution time vary across issue themes, channel, and priority?"
source_table: augment_table/customer_support_tickets/eda_resolution/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:06:03.427239+00:00
wall_seconds: 40.34
---

# Resolution Time Analysis: Issue Theme, Channel, and Priority

**Dataset:** 250 tickets | Columns: `resolution_minutes`, `issue_theme`, `channel`, `priority`

---

## 1. Resolution Time by Priority

Priority is the **strongest driver** of resolution time, but the ordering is counter-intuitive:

| Priority | Mean (min) | Median (min) | N |
|----------|-----------|--------------|---|
| High | 131.1 | 131.0 | 50 |
| Critical | 74.4 | 72.5 | 50 |
| Medium | 41.6 | 37.0 | 76 |
| Low | 37.5 | 24.0 | 74 |

**Key finding:** `High` tickets take *longer* than `Critical` tickets on average (131 vs. 74 min). This may reflect routing or escalation differences — Critical tickets are possibly handled via faster channels (phone/in-app), while High tickets skew toward email (see §3). Medium and Low tickets resolve roughly similarly and about 3× faster than High.

---

## 2. Resolution Time by Issue Theme

| Theme | Mean (min) | Median (min) | N |
|-------|-----------|--------------|---|
| ui | 105.2 | 125.0 | 5 |
| integration | 96.5 | 95.0 | 11 |
| data | 91.7 | 75.0 | 7 |
| performance | 81.5 | 70.0 | 51 |
| billing | 66.1 | 70.0 | 49 |
| auth | 64.8 | 58.0 | 41 |
| account | 57.5 | 48.0 | 24 |
| other | 55.7 | 30.0 | 7 |
| feature | 39.4 | 27.0 | 55 |

- **Slowest themes:** `ui`, `integration`, and `data` — but all have small samples (≤11 tickets), so conclusions should be treated cautiously.
- **Largest reliable theme:** `performance` (n=51, mean 81.5 min) and `feature` (n=55, mean 39.4 min) show a clear gap (~2×), indicating technical outage/performance issues take substantially longer than feature requests.
- `feature` has the lowest mean *and* the widest mean-vs-median gap (39.4 mean vs. 27.0 median), suggesting a right-skewed distribution — most feature tickets resolve quickly but a few outliers inflate the mean.

---

## 3. Resolution Time by Channel

| Channel | Mean (min) | Median (min) | N |
|---------|-----------|--------------|---|
| email | 98.3 | 92.5 | 100 |
| phone | 70.2 | 72.5 | 50 |
| in-app | 35.0 | 31.0 | 50 |
| chat | 22.5 | 23.0 | 50 |

- **Chat and in-app** resolve ~4× faster than email.
- Email is the slowest channel by a wide margin and also the largest volume (100 tickets).
- Phone sits in the middle, consistent with synchronous but more involved interactions.

---

## 4. Priority × Channel Interaction

The cross-tab reveals **channel and priority are not independently assigned**:

| Priority | chat | email | in-app | phone |
|----------|------|-------|--------|-------|
| Critical | — | — | 57.5 | 79.7 |
| High | 48.0 | 132.8 | — | — |
| Low | 15.9 | 71.6 | 24.2 | — |
| Medium | 27.8 | 58.8 | 35.2 | 40.0 |

- `High` tickets appear **only** in chat and email; email-routed High tickets average 132.8 min — the highest single cell in the table.
- `Critical` tickets appear **only** in phone and in-app, which are mid-tier speed channels, explaining why Critical resolves faster than High overall.
- This channel-priority confound means the raw priority ordering (High > Critical) likely reflects channel routing effects rather than genuine prioritization failures.

---

## 5. Priority × Theme Interaction

Across all themes, `High` priority consistently yields the longest resolution (range: 105–145 min), while `Low` priority resolves fastest (range: 20–70 min). Notable:

- `feature` + `High` averages **145 min** — the highest theme-priority combination despite feature requests generally being simple.
- `performance` + `Low` averages just **19.8 min**, suggesting low-priority performance reports are resolved quickly (possibly auto-closed or minor).

---

## Summary & Decision Points

| Factor | Effect on Resolution Time |
|--------|--------------------------|
| Priority | High paradoxically slowest; Critical faster due to channel routing |
| Channel | Email slowest (98 min); Chat fastest (22 min); 4× spread |
| Theme | Performance/integration slow; Feature fastest; ui/data/integration have small samples |
| Interaction | High tickets concentrated in email; Critical in phone/in-app — channel routing drives much of the priority effect |

**Recommendations:** Investigate why `High` tickets route to email rather than faster channels. Reducing email share for High-priority tickets could substantially cut resolution times. Theme-level differences are meaningful for `performance` vs. `feature`, but `ui`, `data`, and `integration` patterns need more data before acting on them.
