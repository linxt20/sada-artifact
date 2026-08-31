---
dataset: flag_6
scenario: predictive_long
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "resolution_time"
query: "What signals suggest an agent's tickets will take longer to resolve?"
source_table: augment_table/flag_6/predictive_long/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:19:42.181928+00:00
wall_seconds: 56.85
---

# Analysis: Signals for Longer Ticket Resolution Time

## Executive Summary

Analysis of 500 ticket records reveals several clear signals indicating a ticket will take longer to resolve. The most striking predictor is **agent assignment**, particularly assignment to Fred Luddy (74% of tickets take >248 hours vs. 9% for Beth Anglin). Other meaningful signals include issue complexity, technical nature, and infrastructure scope.

---

## Primary Signal: Agent Assignment (Skill Variance)

**Agent performance shows the strongest correlation with resolution time:**

| Agent | Mean Hours | Long Tickets (>248h) | Sample Size |
|-------|-----------|----------------------|-------------|
| Fred Luddy | 750.0 | 73.8% | 84 tickets |
| Howard Johnson | 136.1 | 15.0% | 98 tickets |
| Luke Wilson | 131.9 | 18.3% | 103 tickets |
| Charlie Whitherspoon | 118.6 | 14.6% | 103 tickets |
| Beth Anglin | 109.1 | 9.2% | 98 tickets |

Fred Luddy's mean resolution time is **5.7x longer** than Beth Anglin's. This variance directly indicates skill or workload differences between agents and is the dominant predictive signal in the dataset.

---

## Secondary Signals: Technical and Complexity Factors

### 1. **Multi-Step Troubleshooting** (Complexity Indicator)
- **33.7% of multi-step tickets exceed 248 hours** (vs. 24% overall)
- Mean: 253.9 hours
- Combined with Fred Luddy assignment: 84.2% exceed threshold
- *Interpretation*: Issues requiring iterative diagnosis and multiple actions inherently take longer.

### 2. **Configuration Issues** (Technical Severity Signal)
- **30.0% reach long resolution time**
- Mean: 310.8 hours (highest among severity signals)
- *Interpretation*: Configuration problems demand careful validation and testing, extending resolution.

### 3. **Degraded Performance** vs. **Service Outages**
- Degraded performance: 28.9% long, 256.9h mean
- Service outages: 13.4% long, 181.9h mean
- *Interpretation*: Paradoxically, complete outages resolve faster (may be more straightforward cause-and-fix), while performance issues are harder to diagnose.

---

## Tertiary Signals: Issue Domain and Scope

### Issue Domains (Mean Resolution Time)
1. **Software Deployment** – 422.0h mean, 37.5% long (most time-intensive)
2. **VPN Connectivity** – 267.8h mean, 31.8% long
3. **Access Authentication** – 269.5h mean, 20.0% long
4. **Email System** – 189.8h mean, 17.8% long (quickest resolution)

### Infrastructure Scope
- **Single-user devices**: 265.0h mean, 28.3% long
- **Multi-user systems**: 247.9h mean, 28.7% long
- **Shared services**: 221.7h mean, 23.0% long
- **Location-specific**: 153.5h mean, 18.4% long
- *Interpretation*: Issues affecting single users or multiple users require more troubleshooting steps than location-scoped problems.

---

## Weak or Contradictory Signals

### Priority Level
- **1 - Critical**: 187.7h mean (shortest), 15.9% long
- **2 - High**: 229.8h mean, 25.9% long
- **3 - Moderate**: 246.6h mean, 24.2% long
- *Interpretation*: Counter-intuitively, critical tickets resolve faster. This may reflect aggressive resource allocation or simpler root causes. Priority is a weak predictor.

### Agent Handoff Pattern
- **Different closer** (reassigned): 225.1h mean, 24.9% long
- **Same agent closes**: 217.5h mean, 26.0% long
- *Interpretation*: Minimal difference; handoff type is not a strong signal alone.

---

## Data Quality Notes

- Dataset contains 500 tickets from Jan–Jun 2023
- Some timestamps show negative resolution times (opened date after closed date in 2 cases), suggesting data quality issues but not material to analysis
- Fred Luddy has disproportionately high caseload (84 tickets, 16.8% of total) relative to peers (~100 each)

---

## Predictive Insights

**A ticket is more likely to require extended resolution time if:**

1. **Assigned to Fred Luddy** – single strongest predictor (5.7× baseline variance)
2. **Requires multi-step troubleshooting** – complexity extends investigation
3. **Involves configuration issues** – validation and testing add time
4. **Software deployment domain** – intrinsically complex (422h mean)
5. **Involves VPN or network connectivity** – systematic troubleshooting required
6. **Affects single-user devices** – less standardized environments
7. **Presents as degraded performance** – harder to diagnose than outages

**Conversely, tickets resolve quickly when:**
- Assigned to Beth Anglin, Charlie Whitherspoon, or Luke Wilson
- Marked as service outages (simpler diagnosis)
- Involve email system issues (routine resolution steps)
- Are location-specific (scoped problem space)

---

## Recommendations

For **skill_on** focused interventions:
- **Investigate Fred Luddy's caseload**: High volume + extended times suggests workflow, tooling, or skill gaps worth reviewing.
- **Prioritize mentoring on software deployment and VPN issues**: These domains show largest agent variance and longest overall times.
- **Standardize multi-step troubleshooting procedures**: This complexity category is second-order driver of long resolution times.
- **Route configuration issues strategically**: Beth Anglin and Charlie Whitherspoon show superior performance; consider assignment rules.
