---
dataset: customer_support_tickets
scenario: predictive_long
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "resolution_minutes"
query: "What signals suggest a support ticket will take longer to resolve?"
source_table: augment_table/customer_support_tickets/predictive_long/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:06:42.731750+00:00
wall_seconds: 44.34
---

# Signals for Longer Support Ticket Resolution

**Dataset:** 250 customer support tickets | **Focus variable:** `resolution_minutes` (mean: 64.9 min, range: 12–180 min, 75th pct: 88.75 min)

---

## Key Signals (Ranked by Correlation Strength)

### 1. Priority — Strongest Signal (r = 0.56 on `priority_rank`)

| Priority | Mean Resolution (min) | % Tickets > 88.75 min |
|----------|----------------------|----------------------|
| High | **131.1** | **98%** |
| Critical | 74.4 | 22% |
| Medium | 41.6 | 1.3% |
| Low | 37.5 | 2.7% |

**High priority tickets dominate long resolution times.** Notably, Critical tickets resolve faster than High on average (74 vs. 131 min) — possibly because Critical issues trigger escalated, immediate response protocols, while High tickets may queue longer before receiving sustained attention.

### 2. Channel — Strong Signal (r = 0.50 on `channel_complexity`)

| Channel | Mean Resolution (min) | % Tickets > 88.75 min |
|---------|----------------------|----------------------|
| Email | **98.3** | **52%** |
| Phone | 70.2 | 22% |
| In-app | 35.0 | 0% |
| Chat | 22.5 | 0% |

**Email channel is the clearest channel-level predictor of long resolution.** Asynchronous communication likely introduces wait cycles. Chat and in-app channels resolve quickly — no tickets exceeded the 75th-percentile threshold.

### 3. Composite Complexity Score (r = 0.44)

| Score Quartile | Mean Resolution (min) |
|---------------|----------------------|
| Q1 (low) | 31.1 |
| Q2 | 65.1 |
| Q3 | **92.6** |
| Q4 | 81.4 |

Higher composite complexity scores are associated with longer resolution, though Q4 dips below Q3 — suggesting diminishing linearity at the top end (possibly very complex tickets also have dedicated resources).

### 4. Description Word Count (r = 0.21)

Tickets with longer issue descriptions (more words) resolve slightly more slowly (Q1: 54.7 min → Q4: 76.4 min). This is a weak but consistent signal: more elaborate descriptions may indicate more complex, multi-faceted issues.

### 5. Multi-System Keyword Count (r = 0.10)

Tickets referencing multiple systems show a small positive association with resolution time. This is weak evidence — not a standalone predictor, but consistent with the "complexity" theme.

---

## Weak / Non-Signals

- **`has_error_code`**: Near-zero correlation (r = 0.008). Tickets with error codes resolve in virtually the same time as those without (66 vs. 65 min). Error codes do not reliably indicate harder resolutions.
- **`urgency_keyword_count`**, **`scope_keyword_count`**, **`investigation_keyword_count`**: All correlations < 0.10 — negligible predictive value on their own.

---

## Summary Decision Rules

| Signal | Direction | Confidence |
|--------|-----------|------------|
| Priority = **High** | ↑ Much longer | Strong |
| Channel = **Email** | ↑ Longer | Strong |
| `composite_complexity_score` in Q3+ | ↑ Longer | Moderate |
| Longer issue description | ↑ Slightly longer | Weak |
| Priority = **Critical** | ↑ Moderate (not extreme) | Note: exception to priority ordering |

**Bottom line:** The combination of **High priority + email channel** is the clearest predictor of a ticket exceeding ~90 minutes. Composite complexity score provides additive signal. Error codes and urgency keywords are not useful predictors in this dataset.
