---
dataset: flag_12
scenario: predictive_inefficient
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "inefficient_resolution"
query: "What signals suggest an incident resolution will be inefficient?"
source_table: augment_table/flag_12/predictive_inefficient/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:13:58.224917+00:00
wall_seconds: 46.27
---

# Signals of Inefficient Incident Resolution

**Dataset:** 500 incidents | **Inefficiency threshold:** resolution time ≥ 75th percentile (≈253 hours, ~10.5 days) | **Baseline inefficiency rate:** 25%

---

## Key Predictive Signals

### 1. Description Specificity — Strongest Single Signal
Incidents described with vague language resolve slower and hit inefficiency more often:

| Description Type | Inefficiency Rate | Avg. Resolution (hrs) |
|---|---|---|
| `replacement_or_maintenance_request` | **30.0%** | 175 |
| `generic_malfunction` | **27.2%** | 191 |
| `specific_symptom` | 22.5% | 168 |

Incidents phrased as generic malfunctions or open-ended maintenance requests are 25–33% more likely to be inefficient than those with a specific symptom described.

---

### 2. Day of Week at Opening
Incidents opened late in the week are markedly more likely to be inefficient, presumably due to weekend coverage gaps:

| Day Opened | Inefficiency Rate |
|---|---|
| Saturday | **31.4%** |
| Thursday | 29.2% |
| Friday | 28.6% |
| Monday | 17.4% |

Monday-opened tickets resolve most efficiently; the Sat–Fri–Thu cluster shows a clear end-of-week drag.

---

### 3. Failure Type
| Failure Type | Inefficiency Rate | Avg. Resolution (hrs) |
|---|---|---|
| `power_failure` | **30.8%** | 180 |
| `inquiry_or_assistance` | 28.6% | 167 |
| `not_responding` | 26.0% | 184 |
| `software_failure` | 20.6% | 154 |

Power failures and undiagnosed "not responding" issues take longest. Software failures resolve relatively quickly.

---

### 4. Requires Physical Action
Incidents requiring a physical intervention (`requires_physical_action = True`) carry a modestly higher inefficiency rate (25.5% vs. 22.5%) and average ~13 more hours to resolve. This effect is consistent but not dominant alone.

---

### 5. Repeat Incident Signal
`repeat_incident_signal = True` is associated with a slightly elevated inefficiency rate (26.5% vs. 23.9%) and ~10 more hours on average. This suggests unresolved root causes drive recurring, slower-to-close tickets — a meaningful signal despite its modest magnitude.

---

### 6. Assignee Identity (Proxy for Skill Match)
| Assignee | Avg. Resolution (hrs) |
|---|---|
| Luke Wilson | **196** |
| Charlie Whitherspoon | 179 |
| Howard Johnson | 175 |
| Fred Luddy | 165 |

Luke Wilson's assignments average ~30 hours more than Fred Luddy's. However, `assignee_is_resolver` (whether the assigned agent is the one who closes the ticket) shows virtually no difference in efficiency (25.2% vs. 24.9%), suggesting handoffs alone are not the driver.

---

## Combined Risk Profile

An incident with **≥2 of the following** should be flagged as high inefficiency risk:
- Opened on Friday, Saturday, or Thursday
- Description is `generic_malfunction` or `replacement_or_maintenance_request`
- `failure_type` is `power_failure` or `not_responding`
- `requires_physical_action = True`
- `repeat_incident_signal = True`

---

## Caveats and Weak Evidence

- **Priority** shows a counterintuitive pattern: Critical (P1) incidents resolve *faster* on average (167 hrs, 18.5% inefficiency rate) than High (P2) incidents (180 hrs, 25.4%), likely due to escalation procedures. Priority alone is not a reliable predictor of inefficiency.
- The `assignee_is_resolver` flag showed essentially no predictive power (difference < 0.3 pp), making it a weak signal.
- Effect sizes across all factors are modest (all factors remain within a ~10 pp band of the 25% baseline), indicating that **combinations of signals** are more actionable than any single variable.
- With 500 records, some subgroup estimates (e.g., `4 - Low` priority, `Database` category) are based on small samples and should be treated cautiously.
