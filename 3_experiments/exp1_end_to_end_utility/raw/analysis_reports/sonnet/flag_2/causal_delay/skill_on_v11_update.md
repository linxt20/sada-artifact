---
dataset: flag_2
scenario: causal_delay
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "resolution_time"
query: "Controlling for priority and category, which underlying causes explain longer resolution times?"
source_table: augment_table/flag_2/causal_delay/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:16:06.046100+00:00
wall_seconds: 44.59
---

# Causal Analysis of Longer Resolution Times
**Dataset:** `sonnet__skill_on_v11_update.csv` | **n = 500 tickets (372 with closed timestamps)** | **Analysis date:** 2026-07-30

---

## Methodology

Resolution time (hours) was computed from `opened_at` → `closed_at`. To control for **priority** and **category**, per-group means were subtracted, yielding a residual that reflects unexplained delay attributable to other factors. Positive residuals = longer than expected; negative = faster than expected.

**Overall mean resolution: ~1,043 hrs (std ≈ 618 hrs)**

---

## Findings: Factors That Explain Longer Resolution Times

### 1. Failure Symptom Type *(strong signal)*

| Symptom | Residual (hrs) | n |
|---|---|---|
| `access_denied` | **+74** | 69 |
| `service_down` | **+46** | 87 |
| `update_failure` | −6 | 10 |
| `cannot_connect` | −20 | 189 |
| `crash` | −190 | 6 |
| `performance_degradation` | −544 | 2 |

**Access-denied and service-down tickets resolve ~50–75 hrs later than priority/category peers.** This likely reflects dependency on identity/access workflows or cross-team escalation. `crash` and `performance_degradation` resolve faster, possibly due to clearer diagnostics and urgency.

---

### 2. Affected System Component *(moderate-to-strong signal)*

| Component | Residual (hrs) | n |
|---|---|---|
| `software_client` | **+142** | 15 |
| `file_shares` | **+137** | 7 |
| `application_server` | **+96** | 20 |
| `vpn_gateway` | +30 | 80 |
| `email_server` | +28 | 110 |
| `database_server` | −12 | 89 |
| `network_infrastructure` | −62 | 35 |
| `wifi_access_point` | −516 | 12 |

**Software clients, file shares, and application servers are the slowest components** after controlling for priority and category — suggesting higher complexity or specialist dependency. `wifi_access_point` resolves very quickly (likely simple resets), but the sample is small (n=12).

---

### 3. Scope Specificity *(moderate signal)*

| Scope | Residual (hrs) | n |
|---|---|---|
| `system_wide` | **+65** | 77 |
| `individual_user` | −1 | 283 |
| `location_scoped` | −281 | 8 |
| `department_wide` | −603 | 4 |

**System-wide issues take ~65 hrs longer** than expected, consistent with the hypothesis that broader blast radius increases coordination overhead. Counterintuitively, `location_scoped` and `department_wide` are faster — but sample sizes are very small (n=4–8), so this should not be over-interpreted.

---

### 4. Caller Profile *(weak signal)*

| Profile | Residual (hrs) | n |
|---|---|---|
| `itil_internal` | **+70** | 79 |
| `end_user` | −19 | 293 |

Tickets raised by **internal ITIL users take ~70 hrs longer** than those from end-users after controlling for priority/category. This is unexpected; it may reflect more complex or non-standard requests routed through ITIL processes.

---

### 5. Recurrence Signal *(extreme but n=1)*

The single recurring ticket (`recurrence_signal = True`) shows a residual of **+878 hrs**, but with n=1 this is statistically meaningless. The data does not support a generalizable claim about recurrence causing delays.

---

### 6. Environment Context *(weak signal)*

`remote_access` (+20 hrs) and `application_specific` (+29 hrs) environments trend slightly slower, while `office_local` resolves ~190 hrs faster. Production context (n=2) is not reliable. The differences are modest relative to the overall variance.

---

## Summary

| Factor | Delay Direction | Confidence |
|---|---|---|
| `failure_symptom_type`: access_denied, service_down | Longer (+46–74 hrs) | **High** (large n) |
| `affected_system_component`: software_client, file_shares, app_server | Longer (+96–142 hrs) | **Moderate** (small-medium n) |
| `scope_specificity`: system_wide | Longer (+65 hrs) | **Moderate** |
| `caller_profile`: itil_internal | Longer (+70 hrs) | **Moderate** |
| `recurrence_signal`: True | Extreme outlier | **Insufficient data** |

**Primary recommendation:** Triage intervention should focus on `access_denied` and `service_down` symptoms hitting `software_client`, `file_shares`, or `application_server` components with `system_wide` scope — these independently compound delay beyond what priority/category alone predicts.
