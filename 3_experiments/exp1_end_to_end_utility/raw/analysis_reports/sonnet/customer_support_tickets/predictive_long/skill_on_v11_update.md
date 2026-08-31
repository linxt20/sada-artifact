---
dataset: customer_support_tickets
scenario: predictive_long
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "resolution_minutes"
query: "What signals suggest a support ticket will take longer to resolve?"
source_table: augment_table/customer_support_tickets/predictive_long/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:11:07.954013+00:00
wall_seconds: 50.57
---

# Signals That Predict Longer Support Ticket Resolution

**Dataset:** 250 tickets · **Resolution range:** 12–180 min · **Mean:** 64.9 min · **Median:** 58 min  
*Threshold used for "long" below: ≥ 90 minutes (≈ top quartile)*

---

## 1. Priority — Strongest Single Predictor

| Priority | Mean (min) | n |
|----------|-----------|---|
| High | **131.1** | 50 |
| Critical | 74.4 | 50 |
| Medium | 41.6 | 76 |
| Low | 37.5 | 74 |

High-priority tickets take nearly **3.5× longer** than Low-priority tickets. Notably, *Critical* tickets resolve faster than High on average — likely because Critical incidents trigger immediate escalation paths, while High tickets represent complex but non-incident work that lingers.

---

## 2. Regression After Change — Second-Strongest Signal

| regression_after_change | Mean (min) | n |
|------------------------|-----------|---|
| True | **115.3** | 42 |
| False | 54.7 | 208 |

Tickets flagged as regressions following a recent change take **≈ 2.1× longer**. Investigation, rollback coordination, and root-cause confirmation all add time.

---

## 3. Channel — Email Dominates Long Queue

| Channel | Mean (min) | n |
|---------|-----------|---|
| Email | **98.3** | 100 |
| Phone | 70.2 | 50 |
| In-app | 35.0 | 50 |
| Chat | **22.5** | 50 |

All 63 tickets ≥ 90 min arrive via **email (52) or phone (11)**; zero long tickets come via chat or in-app. This likely reflects both ticket complexity (complex issues are written up via email) and asynchronous back-and-forth delays inherent to email.

---

## 4. Ticket Category

| Category | Mean (min) | n |
|----------|-----------|---|
| performance_degradation | **142.3** | 25 |
| billing_billing_error | 94.3 | 7 |
| data_loss_corruption | 91.3 | 8 |
| security_vulnerability | 90.7 | 7 |
| incident_outage | 69.2 | 21 |
| feature_request | **22.8** | 57 |

Performance degradation and data integrity issues are the hardest to resolve quickly. Feature requests are the fastest by far and represent a natural baseline for low-complexity tickets.

---

## 5. Root Cause Type

| Root Cause | Mean (min) | n |
|------------|-----------|---|
| capacity_exhaustion | **130.5** | 10 |
| data_corruption | 85.5 | 10 |
| config_misconfiguration | 84.8 | 33 |
| regression_code_bug | 70.8 | 94 |
| not_present (feature/how-to) | **38.0** | 77 |

Capacity exhaustion requires infrastructure-level intervention; configuration and data issues require careful verification before changes are applied.

---

## 6. Product Area

| Product Area | Mean (min) | n |
|--------------|-----------|---|
| search_indexing | **104.1** | 7 |
| platform_infrastructure | **100.0** | 35 |
| billing_payments | 83.3 | 22 |
| ui_frontend | 38.6 | 65 |

Platform and infrastructure tickets are deep-stack and cross-team; UI frontend tickets (mostly feature requests) resolve quickly.

---

## 7. Severity Signal & Business Deadline Pressure

| Reported Severity | Mean (min) |
|-------------------|-----------|
| explicit_p1_critical | **83.1** |
| production_blocking | **82.6** |
| degraded_non_blocking | 80.3 |
| cosmetic_minor | **23.2** |

| Deadline Pressure | Mean (min) |
|-------------------|-----------|
| hard_deadline_stated | **81.8** |
| soft_urgency_stated | 75.4 |
| not_present | 60.4 |

Higher stated severity correlates with longer resolution, consistent with complexity driving both severity perception and time needed. Hard deadlines do *not* shorten resolution time — agents may reprioritize but the work takes as long as it takes.

---

## 8. Affected User Scope & Environment

| User Scope | Mean (min) |
|------------|-----------|
| entire_tenant | **89.7** |
| subset_of_users | 66.5 |
| single_user | 55.2 |

| Environment | Mean (min) |
|-------------|-----------|
| production | **95.0** |
| not_specified | 52.8 |

Production-environment and tenant-wide issues require careful, coordinated changes and tend to take substantially longer.

---

## Summary: Key Risk Signals (Decision-Ready)

| Signal | Effect Size | Confidence |
|--------|-------------|------------|
| Priority = High | +76 min vs Low | Strong (n=50 vs 74) |
| regression_after_change = True | +61 min | Strong (n=42) |
| Channel = Email | +76 min vs Chat | Strong (n=100 vs 50) |
| Category = performance_degradation | +120 min vs feature_request | Strong |
| Root cause = capacity_exhaustion | +93 min vs no-cause | Moderate (n=10) |
| Environment = production | +42 min vs not_specified | Strong (n=68) |
| Affected scope = entire_tenant | +34 min vs single_user | Moderate (n=62) |

### Exceptions & Weak Evidence
- **Critical vs. High paradox:** Critical tickets resolve *faster* than High (74 vs 131 min), suggesting escalation procedures accelerate Critical tracks.
- **Hard deadline pressure does not shorten time:** Despite urgency, hard-deadline tickets average 82 min — slightly *above* the mean, indicating urgency labels reflect complexity, not agent speed-up.
- **Small-n categories** (security_vulnerability n=7, capacity_exhaustion n=10, search_indexing n=7) have high means but wide uncertainty; treat as directional only.
- **Reproducibility** shows modest separation: consistently reproducible (77 min) vs. intermittent (71 min) — weaker than other signals and may be confounded by category.
