---
dataset: customer_support_tickets
scenario: eda_resolution
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_minutes"
query: "How does resolution time vary across issue themes, channel, and priority?"
source_table: augment_table/customer_support_tickets/eda_resolution/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:10:50.115393+00:00
wall_seconds: 51.89
---

# Resolution Time Analysis: Issue Theme, Channel, and Priority

**Dataset:** 250 support tickets | **Focus variable:** `resolution_minutes`

---

## 1. Priority

Priority is the strongest single driver of resolution time, but with a notable non-monotonic pattern:

| Priority | Mean (min) | Median (min) | Count |
|----------|-----------|--------------|-------|
| High     | 131.1     | 131.0        | 50    |
| Critical | 74.4      | 72.5         | 50    |
| Medium   | 41.6      | 37.0         | 76    |
| Low      | 37.5      | 24.0         | 74    |

**Key finding:** `High` priority tickets take *longer* than `Critical` on average (131 vs. 74 min). This is counter-intuitive and likely reflects the channel/theme composition of each group — all `High` priority tickets are routed through email and involve complex themes (bugs, billing, configuration), while `Critical` tickets are handled via phone and in-app channels. This confounding effect is important to flag before drawing operational conclusions.

---

## 2. Channel

Channel shows a strong and consistent pattern:

| Channel | Mean (min) | Median (min) | Count |
|---------|-----------|--------------|-------|
| Email   | 98.3      | 92.5         | 100   |
| Phone   | 70.2      | 72.5         | 50    |
| In-app  | 35.0      | 31.0         | 50    |
| Chat    | 22.5      | 23.0         | 50    |

- **Chat** is the fastest channel by a wide margin (~22 min median).
- **Email** is the slowest (~93 min median), nearly 4× chat.
- **In-app** and **Phone** are intermediate, with phone being moderately slow likely due to escalation complexity.
- The email channel also carries the widest range (46–180 min), suggesting high variance in ticket difficulty or agent handling.

---

## 3. Issue Theme

Themes span a wide resolution range:

| Issue Theme              | Mean (min) | Median (min) | Count |
|--------------------------|-----------|--------------|-------|
| performance_degradation  | 142.4     | 140.0        | 26    |
| data_loss_corruption     | 102.0     | 95.0         | 5     |
| integration_sync         | 91.7      | 75.0         | 3     |
| billing_invoicing        | 84.5      | 80.0         | 22    |
| security_incident        | 83.3      | 82.5         | 6     |
| authentication_access    | 77.3      | 80.0         | 12    |
| configuration_settings   | 70.5      | 62.5         | 16    |
| outage_availability      | 65.2      | 62.5         | 18    |
| bug_functional           | 56.3      | 43.0         | 81    |
| feature_request          | 25.9      | 22.0         | 61    |

- **Performance degradation** is the most time-consuming theme (mean 142 min), and all 26 instances are `High` priority, indicating a consistent pattern rather than an outlier effect.
- **Feature requests** are resolved fastest (mean ~26 min), consistent with low complexity and often Low/Medium priority routing.
- **Data loss/corruption** and **integration/sync** themes show high mean times but small sample sizes (n=5 and n=3 respectively) — treat with caution.
- **Outage/availability** resolves faster (mean 65 min) than might be expected, possibly because these are well-practiced incident workflows.

---

## 4. Interaction Effects

Cross-cutting the three dimensions reveals:

- **High priority via email** dominates the slow tail: bug_functional (118.8 min), configuration_settings (133.3 min), data_loss_corruption (132.5 min), integration_sync (140.0 min).
- **Critical via phone** resolves in ~80 min — faster than High/email for nearly every theme, despite higher nominal severity.
- **Low priority via email** is notably slow for billing and configuration themes (65–90 min), suggesting email introduces delay independent of urgency — likely due to async back-and-forth or queue depth.
- A single Medium-priority `bug_functional` via email hit 140 min, consistent with the email/functional-bug penalty seen elsewhere.

---

## 5. Summary & Exceptions

| Driver | Direction | Strength |
|--------|-----------|----------|
| Channel = email | Increases resolution time | Strong |
| Channel = chat | Decreases resolution time | Strong |
| Theme = performance_degradation | Increases (all routed as High/email) | Strong |
| Theme = feature_request | Decreases | Strong |
| Priority = High vs. Critical | High is *slower* (channel confound) | Moderate — interpret carefully |

**Exceptions / weak evidence:**
- `integration_sync` and `data_loss_corruption` show high means but tiny samples (n ≤ 5); no firm conclusions.
- `outage_availability` resolves surprisingly quickly for its severity — may reflect dedicated escalation paths.
- The priority ordering is not monotonic; channel composition is a significant confound and should be controlled before using priority alone as a resolution-time predictor.
