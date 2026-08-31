---
dataset: customer_support_tickets
scenario: eda_resolution
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: exploratory_data_analysis
focus_variable: "resolution_minutes"
query: "How does resolution time vary across issue themes, channel, and priority?"
source_table: augment_table/customer_support_tickets/eda_resolution/original.csv
generated_at: 2026-07-26T13:05:34.410810+00:00
wall_seconds: 81.92
---

# Resolution Time Analysis: Issue Themes, Channel, and Priority

**Dataset:** 250 support tickets · `resolution_minutes` (12–180 min, mean 64.9, median 58.0)

---

## 1. Resolution Time by Priority

| Priority | n | Mean (min) | Median (min) |
|----------|---|-----------|-------------|
| Low | 74 | 37.5 | 24.0 |
| Medium | 76 | 41.6 | 37.0 |
| Critical | 50 | 74.4 | 72.5 |
| High | 50 | 131.1 | 131.0 |

**Key finding:** The priority ordering is counterintuitive — `High` tickets take nearly **twice as long** as `Critical` tickets. However, this is almost entirely explained by channel confounding (see §3): Critical tickets are routed to phone/in-app (faster channels), while High tickets are routed almost exclusively to email (slowest channel). Low and Medium resolve quickly, consistent with their lower urgency.

---

## 2. Resolution Time by Channel

| Channel | n | Mean (min) | Median (min) |
|---------|---|-----------|-------------|
| chat | 50 | 22.5 | 23.0 |
| in-app | 50 | 35.0 | 31.0 |
| phone | 50 | 70.2 | 72.5 |
| email | 100 | 98.3 | 92.5 |

**Channel is the strongest differentiator.** Chat is fastest (≈23 min), in-app is second (≈31 min), phone is moderate (≈72 min), and email is the slowest by a wide margin (≈92 min median). Email accounts for 40% of all tickets and pulls the overall mean up significantly. The low variance within chat and in-app (tight medians close to means) suggests these channels are consistently fast.

---

## 3. Priority × Channel Confounding

Priority groups are **not randomly distributed across channels** — they are almost fully nested:

| Priority | Dominant Channel(s) |
|----------|-------------------|
| Critical | phone (76%), in-app (24%) |
| High | email (98%) |
| Low | chat / email / in-app (roughly equal) |
| Medium | mixed (all four) |

This means the apparent "High > Critical" paradox in §1 is an artifact of routing rules, not actual escalation performance. When looking at within-channel means: email tickets for High average 132.8 min, while Critical on phone averages 79.7 min and on in-app 57.5 min — differences driven by channel, not priority handling per se.

---

## 4. Resolution Time by Issue Theme

Themes were derived from `issue_description` keywords. Counts are approximate due to multi-topic descriptions.

| Theme | n | Mean (min) | Median (min) |
|-------|---|-----------|-------------|
| Performance | 13 | 99.5 | 135.0 |
| Export | 4 | 87.0 | 102.5 |
| Integration/API | 16 | 84.9 | 77.5 |
| Billing/Invoice | 17 | 80.8 | 80.0 |
| Login/Auth | 30 | 67.6 | 61.0 |
| Dashboard/Analytics | 71 | 64.1 | 50.0 |
| Bug/Error | 8 | 60.0 | 60.0 |
| Other | 44 | 58.3 | 55.0 |
| Account | 30 | 50.0 | 32.5 |
| Notification | 17 | 42.2 | 30.0 |

**Slower themes:** Performance issues (mean 99.5 min) and Integration/API (84.9 min) take longest — consistent with technical complexity. Billing/Invoice is also above average (80.8 min), suggesting investigation time or back-office dependencies.

**Faster themes:** Notification and Account issues resolve most quickly (≈30–42 min median), suggesting simpler, self-contained fixes.

**Caution:** Export (n=4) and Bug/Error (n=8) have small samples; estimates are unreliable. Dashboard/Analytics is the largest theme (n=71) with moderate resolution time (median 50 min) and high variance (mean 64 vs. median 50), indicating a wide mix of sub-issues.

---

## 5. Summary & Decision Implications

| Factor | Impact on Resolution Time |
|--------|--------------------------|
| **Channel** | Strongest driver. Email adds ~70 min vs. chat. |
| **Priority** | Apparent effect is largely mediated by channel routing. |
| **Issue Theme** | Performance/API/Billing add meaningful time; Account/Notification are fast. |

**Recommendations:**
- Re-examine the **email routing policy** for High-priority tickets — shifting some to phone or chat could substantially reduce resolution time.
- Flag **Performance** and **Integration/API** tickets for specialist routing given consistently high resolution times.
- Treat Critical ticket performance cautiously: favorable numbers partly reflect faster channel routing rather than better agent handling.
