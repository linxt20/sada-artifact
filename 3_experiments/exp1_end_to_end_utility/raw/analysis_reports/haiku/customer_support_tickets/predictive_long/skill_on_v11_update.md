---
dataset: customer_support_tickets
scenario: predictive_long
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "resolution_minutes"
query: "What signals suggest a support ticket will take longer to resolve?"
source_table: augment_table/customer_support_tickets/predictive_long/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:11:22.503996+00:00
wall_seconds: 65.13
---

# Signals Predicting Long Support Ticket Resolution Times

## Executive Summary

Analysis of 250 support tickets reveals five key signals that strongly predict longer resolution times (>88 minutes, the 75th percentile):

1. **High Priority** (98% of High tickets exceed threshold)
2. **Email Channel** (52% exceed threshold)
3. **Performance or Partial Outage Issues** (94% exceed threshold)
4. **System Investigation Required** (39% exceed threshold)
5. **Architecture Review or Query Plan Work** (85% exceed threshold)

The strongest single predictor is **High priority status**, which correlates with 3.5× longer average resolution time than Low priority tickets.

---

## Key Findings

### Priority Level: Dominant Predictor

| Priority   | Avg. Time | % Long | Count |
|-----------|-----------|-------|-------|
| **High**  | **131 min** | **98%** | 50 |
| Critical  | 74 min   | 22%   | 50 |
| Medium    | 42 min   | 1%    | 76 |
| Low       | 38 min   | 3%    | 74 |

**Insight**: High priority tickets are resolved in 131 minutes on average—**more than 3× longer than Low priority** (38 min) and significantly longer than Critical (74 min), which suggests High priority may flag complex cases requiring deeper technical work rather than critical incidents requiring rapid response.

### Communication Channel: Email Signals Extended Resolution

| Channel  | Avg. Time | % Long | Count |
|----------|-----------|-------|-------|
| **Email** | **98 min** | **52%** | 100 |
| Phone    | 70 min    | 22%   | 50 |
| In-app   | 35 min    | 0%    | 50 |
| Chat     | 23 min    | 0%    | 50 |

**Insight**: Email tickets take **4.3× longer** than chat tickets. This may reflect that email channel selects for complex issues requiring investigation and follow-up, while chat/in-app capture quick clarifications. No email tickets are resolved below 89 minutes when other signals align.

### Issue Severity: Performance Degradation is Highest Predictor

| Outage Scale                           | Avg. Time | % Long | Count |
|----------------------------------------|-----------|-------|-------|
| **Performance Degradation/Partial**    | **132 min** | **94%** | 33 |
| Production Outage (Users Blocked)      | 75 min    | 28%   | 53 |
| Single Workflow Broken                 | 54 min    | 14%   | 104 |
| Unknown/No Outage Impact               | 37 min    | 3%    | 60 |

**Insight**: Performance degradation issues are the strongest outage-related signal—94% exceed the long threshold. These require investigation into databases, indexes, or query patterns before resolution is possible.

### Engineering Work Type: Architecture Review Adds Most Time

| Work Required                               | Avg. Time | % Long | Count |
|---------------------------------------------|-----------|-------|-------|
| **Requires Architecture Review/Query Plan** | **134 min** | **85%** | 13 |
| Requires Investigation (No Code Change)    | 82 min    | 36%   | 110 |
| Requires Root Cause Analysis                | 74 min    | 34%   | 79 |
| Requires Code or Deployment Change         | 42 min    | 10%   | 124 |

**Insight**: Architecture or query plan work is **3.2× longer** than pure code/deployment work. This reflects the investigation time needed before remediation begins—no immediate fix path exists.

### Technical Depth: Investigation Tasks Drive Duration

| Technical Depth                  | Avg. Time | % Long | Count |
|----------------------------------|-----------|-------|-------|
| **Requires System Investigation** | **84 min** | **39%** | 65 |
| **Requires Config Troubleshooting** | **81 min** | **38%** | 16 |
| Requires Root Cause Analysis     | 74 min    | 34%   | 79 |
| Requires Simple Fix/Clarification | 40 min    | 6%    | 90 |

**Insight**: System investigation and configuration work take 2× longer than simple fixes, reflecting the diagnostic time required before resolution.

### Feature Requests: Faster (Different Process)

| Status           | Avg. Time | % Long | Count |
|------------------|-----------|-------|-------|
| Feature Request  | 22 min    | 0%    | 53 |
| Bug/Issue        | 76 min    | 30%   | 197 |

**Insight**: Feature requests resolve in **22 minutes**—likely triaged and categorized for product review rather than troubleshot. This is a fundamentally different resolution path with lower time investment.

### Diagnostics Provided: Weak Predictor

| Diagnostics Provided           | Avg. Time | % Long |
|--------------------------------|-----------|-------|
| Reproduction Steps Provided    | 66 min    | 27%   |
| Insufficient Diagnostics       | 65 min    | 25%   |
| Screenshots/Network Data       | 61 min    | 17%   |
| Logs/Crash IDs Attached        | 60 min    | 0%    |

**Insight**: Counterintuitively, provided diagnostics show weak correlation with resolution time. This suggests that **diagnostic burden is not the limiting factor**—investigation complexity is.

### Scope: Limited Edge Case Effect

| Scope Span                      | Avg. Time | % Long |
|---------------------------------|-----------|-------|
| Entire Subsystem/Service        | 70 min    | 30%   |
| Multiple Tenants/Regions        | 62 min    | 22%   |
| Single User/Account             | 63 min    | 24%   |

**Insight**: System-wide scope shows 10% higher resolution time, but the effect is modest compared to priority or channel effects.

---

## Combined Signal Patterns

The longest tickets cluster around **High priority + Email + Performance/Partial outage + System investigation**:

- CS-0012 (180 min): High, Email, Performance Degradation, Architecture Review needed
- CS-0042 (165 min): High, Email, Performance Degradation, Architecture Review needed
- CS-0022 (155 min): High, Email, Performance Degradation, Architecture Review needed
- CS-0172 (150 min): High, Email, Performance Degradation, Config Troubleshooting needed

**Rare pattern for quick resolution (<25 min)**: Low/Medium priority + Chat/In-app + Feature request or simple clarification needed.

---

## Important Exceptions and Caveats

1. **Critical ≠ Long**: Despite being labeled Critical, Critical priority tickets average only 74 minutes—markedly shorter than High (131 min). This suggests "Critical" flags true emergencies (which resolve via rapid response), while "High" flags complex technical work.

2. **Weak Diagnostics Signal**: Tickets with better diagnostics (logs, crash IDs, reproduction steps) do not resolve measurably faster. Diagnostic completeness is not the bottleneck; **technical investigation depth is**.

3. **Email Channel Confound**: Email's long times may reflect **self-selection**—complex issues may be more likely to arrive via email than via chat, not that email itself causes delays.

4. **Feature Requests Are Different**: Feature requests (22 min avg) follow a routing-only process, not a troubleshooting process. Comparing them to bug fixes conflates two different resolution types.

5. **Small Sample Size Risk**: Architecture review work (n=13) has high average time (134 min) but small count; may not generalize.

---

## Actionable Insights for Support Operations

**To reduce resolution time for long-running tickets:**

- **Early triage**: Flag High-priority, email-sourced performance issues for immediate escalation to engineering (likely to exceed 90 min).
- **Reduce investigation scope**: Architecture reviews and system investigations are time sinks. Pre-built runbooks and self-service diagnostics for common performance patterns could shorten these.
- **Channel choice**: Encourage customers reporting performance issues to use phone or chat for faster initial triage before email for detailed follow-up.
- **Priority calibration**: Reconsider High vs. Critical distinction—High may better flag deep technical work, while Critical should reserve for true service outages.

---

## Conclusion

The strongest signals that a ticket will take longer to resolve are:

1. **High priority** status (strongest single predictor)
2. **Email channel** (4× longer than chat/in-app)
3. **Performance degradation/partial outage** impact
4. **System investigation** or architecture review required
5. **Not feature request** (feature routing is fast)

These signals interact: a High-priority email about performance degradation requiring architecture review will almost certainly exceed 90 minutes. Conversely, a Low-priority in-app feature request will almost certainly resolve in <30 minutes.
