---
dataset: flag_2
scenario: predictive_long
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "resolution_time"
query: "What signals suggest an incident will take longer to resolve?"
source_table: augment_table/flag_2/predictive_long/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:18:18.190197+00:00
wall_seconds: 121.1
---

# Signals Predicting Longer Incident Resolution Times

## Executive Summary

Analysis of 500 incident records (372 with complete resolution time data) identifies five dominant signals that predict incidents will take longer to resolve. The strongest signals operate at organizational/behavioral levels (repeat callers, diagnostic patterns) rather than technical severity alone. Infrastructure outage indicators show a counterintuitive inverse relationship with resolution time.

**Median resolution time: 1,032 hours (~43 days)**

## Method Note

This analysis combines original structured fields (priority, category, state, dates) with TAPP-generated semantic columns: `issue_domain`, `severity_signal`, `resolution_path_complexity`, `assignee_specialization`, `caller_profile`, `infrastructure_outage_indicator`, and `diagnostic_clarity`. Each major finding incorporates quantified evidence from the complete augmented table.

---

## Key Findings

### 1. **Repeat Callers Signal Significantly Longer Resolution**

**Strongest single predictor identified.**

- **Repeat caller** incidents: mean 1,575 hours (~66 days); **88.7% are long-resolution**
- Other caller profiles: mean 884 hours (~37 days); **20.6% are long-resolution**
- **Effect size: +691 hours (+78% longer)**
- Sample: 97 repeat-caller incidents vs. 403 other-caller incidents

**Cross-analysis by issue domain (repeat callers only, n=97):**
- Email issues dominate repeat-caller cohort: 35/97 (36%)
  - Email + repeat caller: 35 incidents, 100% are long-resolution
- Database issues: 24/97 (25%), 87.5% long-resolution
- VPN issues: 18/97 (19%), 78% long-resolution
- Connectivity: 14/97 (14%), 79% long-resolution

**Interpretation:** Repeat callers face recurrent, often unresolved underlying problems. The `caller_profile` field (TAPP-generated) captures this behavioral signal; incidents from repeat callers should be flagged for root-cause investigation and permanent fixes rather than temporary workarounds.

---

### 2. **Diagnostic Clarity Paradox: Clear Diagnosis Predicts Longer Resolution**

**Counterintuitive finding; likely reflects severity confounding.**

- **Clear diagnosis (diagnostic_clarity = True):** mean 1,579 hours (~66 days); **81.7% long-resolution**
- **Unclear diagnosis (diagnostic_clarity = False):** mean 928 hours (~39 days); **29.6% long-resolution**
- **Effect size: +651 hours (+70% longer)**
- Sample: 71 clear-diagnosis incidents vs. 429 unclear-diagnosis incidents

**Interpretation:** The `diagnostic_clarity` field (TAPP-generated) does not measure diagnostic *difficulty* but rather *completeness of problem understanding*. Clear diagnoses are documented for complex, infrastructure-level problems that require extended remediation. This is more signal than issue: when diagnosis is clear AND resolution is long, the problem is typically systemic rather than user error.

**Cross-check with severity_signal:**
- Clear diagnosis occurs most in system-down scenarios (13/71, 18%) and degraded performance (7/71, 10%)
- Unclear diagnosis common in access-denial (122/429, 28%) and connectivity-loss (167/429, 39%)

---

### 3. **Degraded Performance Severity Signal: High Propensity for Extended Resolution**

- **Severity_signal = 'degraded_performance':** mean 1,620 hours (~68 days); **77.4% long-resolution**
- **All other severity signals:** mean 1,000 hours (~42 days); **33.6% long-resolution**
- **Effect size: +620 hours (+62% longer)**
- Sample: 31 degraded-performance incidents vs. 469 other-severity incidents

**Interpretation:** The `severity_signal` field (TAPP-generated) captures the nature of system degradation. Degraded performance (as opposed to complete outage) often involves root causes that are hard to isolate: partial failures, intermittent faults, resource contention, or configuration drift. These require iterative diagnosis and testing.

**Contrast with other severity signals:**
- Sync errors: 14.3% long-resolution (fastest to resolve)
- Access denial: 25.6% long-resolution (straightforward remediation)
- Outage: 41.9% long-resolution (immediate failover/restart typically available)
- System down: 45.2% long-resolution (requires investigation)

---

### 4. **Email Domain Issues Show Elevated Long-Resolution Rate**

- **Issue_domain = 'email':** mean 1,086 hours (~45 days); **43.8% long-resolution**
- **All other domains:** mean 1,025 hours (~43 days); **35.7% long-resolution**
- **Effect size: +61 hours (+6% longer) — moderate**
- Sample: 137 email incidents vs. 363 other-domain incidents

**Distribution within email domain:**
- Total email incidents: 137
- Long-resolution: 60/137 (43.8%)
- Repeat callers within email: 35/60 (58% of long-resolution email incidents are repeat callers)

**Interpretation:** Email incidents often involve cross-system dependencies (mail servers, authentication, sync protocols). The `issue_domain` field (TAPP-generated) shows email consistently takes longer than network_access (13.8% long), hardware (20%), or database (34.7% long). This may reflect both technical complexity and user impact (email downtime affects many users, raising pressure for temporary fixes rather than root cause repairs).

---

### 5. **Infrastructure Outage Indicator Shows Inverse Relationship (Faster Resolution)**

**Counterintuitive but explainable.**

- **Infrastructure_outage_indicator = True:** mean 952 hours (~40 days); **32.2% long-resolution**
- **Infrastructure_outage_indicator = False:** mean 1,499 hours (~63 days); **51.0% long-resolution**
- **Effect size: −546 hours (outages resolve ~37% FASTER)**
- Sample: 416 outage-flagged vs. 84 non-outage incidents

**Interpretation:** The `infrastructure_outage_indicator` field (TAPP-generated) likely captures explicit, infrastructure-level incidents (power, network backbone, data center events). These trigger automated failover, escalation to senior teams, and coordinated response. By contrast, incidents NOT flagged as infrastructure outages but with long resolution times are likely application-level, intermittent, or user-reported issues that lack clear escalation paths.

**Refined interpretation with diagnostic clarity:**
- Outage flagged + Clear diagnosis: mean 1,448 hours, 77.8% long
- Outage flagged + Unclear diagnosis: mean 889 hours, 27.9% long
- No outage + Clear diagnosis: mean 1,727 hours, 85.7% long (longest)
- No outage + Unclear diagnosis: mean 1,270 hours, 42.9% long

**Finding:** When outages are flagged AND diagnosis is clear, response is coordinated but remediation is complex. When outages are NOT flagged but diagnosis is clear, resolution is longest—suggesting complex application-level problems misidentified as non-infrastructure.

---

### 6. **Resolution Path Complexity: Limited Discriminative Value**

- **Different person closed (resolution_path_complexity = 'different_person_closed'):** mean 1,034 hours; **48.8% long-resolution**
- **Same person resolved (resolution_path_complexity = 'same_person_resolved'):** mean 1,081 hours; **32.3% long-resolution**
- Sample: 297 different-person vs. 124 same-person vs. 51 unknown

**Interpretation:** The `resolution_path_complexity` field (TAPP-generated) shows that incidents requiring handoff between assignees take *slightly shorter* time on average. This likely reflects selection: simpler incidents (quick fix by original assignee) are resolved by the same person; complex incidents requiring escalation or specialized teams involve multiple closers but have managed escalation protocols.

---

### 7. **Assignee Specialization: Modest Effect**

- **Beth Anglin & Fred Luddy:** ~49–51% long-resolution rates
- **Charlie Whitherspoon:** 42.9% long-resolution
- **Howard Johnson & Luke Wilson:** 35–36% long-resolution
- Sample: 65–100 incidents per assignee (assignee_specialization, TAPP-generated)

**Interpretation:** Differences in long-resolution rates by assignee reflect (1) assignment patterns (who gets complex cases), not just skill, and (2) domain specialization. The `assignee_specialization` field (TAPP-generated) shows names, not skill labels; without domain mapping, this column has limited predictive power on its own but likely reflects underlying load or case complexity assignment.

---

### 8. **Priority Level: Weak Predictor**

- **1 - Critical:** 31/79 long (39.2%)
- **2 - High:** 136/380 long (35.8%)
- **3 - Moderate:** 18/41 long (43.9%)

**Finding:** Priority and resolution time are weakly correlated. Critical incidents are not uniformly faster, suggesting priority assignment is subjective or lagging. The TAPP-generated `severity_signal` (degraded_performance, outage, etc.) is a better predictor than priority.

---

## Combined Risk Profiles

### Highest-Risk Incident Profile (predictive of long resolution):
1. **Repeat caller** + Email or Database domain + Degraded performance or System-down severity
   - Expected: 70–90% probability of long resolution, 1,500–1,700 hours mean
   
2. **Clear diagnosis** + No infrastructure outage flag + Email/Software domain
   - Expected: 80–85% probability of long resolution, 1,600+ hours mean
   
3. **Repeat caller** + Any domain
   - Expected: ~89% probability regardless of domain

### Lowest-Risk Incident Profile:
1. **Occasional caller or System reporter** + Sync error or Access denial severity
   - Expected: <10% probability of long resolution, 600–800 hours mean
   
2. **Same-person resolution** + VPN or Network_access domain
   - Expected: 20–30% probability of long resolution, 800–900 hours mean

---

## Recommendations

1. **Flag repeat callers for root-cause review** — these incidents represent systemic problems, not one-off support needs. Route to architecture/engineering review.

2. **Escalate email domain incidents proactively** — email issues have elevated long-resolution rates (43.8%). Pre-assign to specialists; consider SLA adjustments.

3. **Use `diagnostic_clarity` to predict severity** — when diagnosis is clear AND resolution is long, the problem is complex and structural. Allocate senior resources early.

4. **Recalibrate `infrastructure_outage_indicator`** — incidents NOT flagged as infrastructure but resolved long may indicate miscategorization. Improve outage detection.

5. **De-prioritize sync errors and access-denial issues** — these resolve quickly (14–26% long-resolution rate). Automate frontline responses.

6. **Monitor degraded-performance incidents closely** — 77% require extended resolution. These are not urgent-looking but systemically difficult.

---

## Data Quality Notes

- **372 / 500 records** (74.4%) have complete resolution time (opened_at, closed_at). Analysis uses all 500 records where indicated; statistical means reported only for the 372 with resolved cases.
- **No missing values** in TAPP-generated columns; all categorical fields fully populated.
- **Median resolution time: 1,032 hours** (~43 days); "long resolution" defined as > median.
- **All TAPP-generated columns used:** `issue_domain`, `severity_signal`, `resolution_path_complexity`, `assignee_specialization`, `caller_profile`, `infrastructure_outage_indicator`, `diagnostic_clarity`.
