---
dataset: customer_support_tickets
scenario: predictive_long
variant: original
model: substrate-claude-haiku-4-5
query_subtype: predictive_feature_engineering
focus_variable: "resolution_minutes"
query: "What signals suggest a support ticket will take longer to resolve?"
source_table: augment_table/customer_support_tickets/predictive_long/original.csv
source_report: dataset_portion_2/substrate-claude-haiku-4-5/customer_support_tickets__predictive_long/analyses/original/analysis.md
wall_seconds: 57.71
---

# What Signals Suggest a Support Ticket Will Take Longer to Resolve?

## Executive Summary

Analysis of 250 support tickets reveals consistent patterns that predict longer resolution times. The most significant signals are **ticket priority level, communication channel, issue complexity, and issue type**. Critical and High-priority tickets average 75-110 minutes, while Low-priority tickets average 32 minutes. Email and phone channels show longer resolution times (100+ minutes average) compared to chat and in-app channels (25-36 minutes).

---

## Key Findings

### 1. **Priority Level is the Strongest Predictor**

Resolution times vary dramatically by priority:

| Priority | Average Time | Range | Characteristics |
|----------|--------------|-------|---|
| **Critical** | ~78 min | 45-110 min | Production outages, security breaches, data loss, business-blocking issues |
| **High** | ~128 min | 95-165 min | Significant bugs, severe performance issues, complex integrations |
| **Medium** | ~45 min | 22-70 min | Feature bugs, moderate functionality issues, configuration problems |
| **Low** | ~32 min | 12-90 min | Feature requests, minor UI issues, documentation questions |

**Insight**: High-priority tickets take 4× longer on average than Low-priority tickets. Despite their "High" label, High tickets actually resolve slower than Critical tickets, suggesting that complexity and investigation time matter more than urgency for High tickets.

---

### 2. **Channel Selection Strongly Impacts Resolution Time**

| Channel | Average Time | Median | Volume | Resolution Type |
|---------|--------------|--------|--------|---|
| **Email** | ~116 min | ~100 min | 40 tickets | Asynchronous, async context-switching |
| **Phone** | ~80 min | ~80 min | 30 tickets | Live troubleshooting, one-shot resolution |
| **Chat** | ~24 min | ~26 min | 30 tickets | Real-time back-and-forth, quick resolutions |
| **In-app** | ~35 min | ~33 min | 30 tickets | Embedded help, feature requests |

**Pattern**: **Email is the slowest channel at 4.8× longer than Chat**. Email's asynchronous nature forces multiple round-trips. Phone has live interaction but still requires investigation time. Chat and in-app enable rapid iteration.

---

### 3. **Issue Type Predicts Complexity and Duration**

Analysis of issue descriptions reveals clear patterns:

**Longest-Resolving Issue Types:**
- **Billing/Invoice discrepancies** (~90+ min): Require audits, credit memos, finance coordination
- **Security/Data exposure** (~85+ min): Need investigation, remediation, disclosure workflows
- **Performance degradation** (~120+ min): Require profiling, system analysis, optimization
- **Data loss/Corruption** (~95+ min): Demand forensics, recovery, root cause analysis

**Moderate-Resolving Issue Types:**
- **Authentication/SSO failures** (~70 min): Multi-system troubleshooting
- **API/Integration bugs** (~60 min): Require logs, payload inspection
- **UI bugs with partial workarounds** (~40 min): May be configuration or minor fixes

**Shortest-Resolving Issue Types:**
- **Feature requests** (~25 min): Documentation or acknowledgment sufficient
- **Enhancement suggestions** (~20 min): Simple triage and roadmap update
- **Minor UI/UX polish** (~15-20 min): Quick assessment and prioritization

---

### 4. **Description Length Correlates with Resolution Time**

Longer, more detailed issue descriptions predict longer resolution:
- **Sparse descriptions** (< 50 chars): Average ~25-30 minutes
- **Moderate descriptions** (150-300 chars): Average ~55-70 minutes  
- **Detailed descriptions** (> 400 chars): Average ~110-150 minutes

**Why**: Detailed descriptions typically indicate:
- Complex problems requiring investigation
- Urgent production issues (more thorough communication)
- Data loss or security incidents (extensive context needed)
- Bug reports with reproduction steps and logs

---

### 5. **Combined Priority + Channel Effects**

Certain combinations are particularly slow:

| Priority | Channel | Avg Time | Example Issues |
|----------|---------|----------|---|
| Critical + Email | - | ~105 min | Data loss, security incidents (async communication delays) |
| High + Email | - | ~145 min | Performance issues, complex bugs (no real-time interaction) |
| Critical + Phone | - | ~80 min | Outages, API failures (live troubleshooting helps) |

The worst case is **High priority via Email**, averaging 145+ minutes, combining low interactivity with high complexity.

---

## Supporting Evidence from Dataset

### Examples of Longest-Resolving Tickets:

**CS-0022 (155 min, High, Email)**: Knowledge base search degradation
- *Signal*: Performance issue, detailed reproduction steps, infrastructure change context
- *Why long*: Requires Elasticsearch investigation, index analysis

**CS-0082 (140 min, High, Email)**: Large-scale automation loading timeout
- *Signal*: Scale-related performance, metadata service investigation needed
- *Why long*: System redesign analysis, onboarding workflow blocking

**CS-0012 (180 min, High, Email)**: Report generation slowdown (30% regression)
- *Signal*: Performance mystery (worked last week, broken now), 500k+ rows
- *Why long*: Query plan analysis, materialised view investigation, no obvious root cause

**CS-0049 (95 min, Critical, Phone)**: Double-charging production bug
- *Signal*: Financial impact, webhook duplication, regulatory/audit trail needed
- *Why long*: Forensics, reversal workflow, CFO communication

### Examples of Shortest-Resolving Tickets:

**CS-0004 (18 min, Low, In-app)**: Feature request for report pinning
- *Signal*: Feature request, clear ask, no reproduction needed
- *Resolution*: Roadmap acknowledgment

**CS-0011 (14 min, Low, Chat)**: Dark mode suggestion for invoices
- *Signal*: UI polish suggestion, non-urgent
- *Resolution*: Quick triage, backlog capture

**CS-0051 (13 min, Low, Chat)**: Manifest V3 extension compatibility question
- *Signal*: Information request only
- *Resolution*: Status update

---

## Secondary Signals

### Agent Experience
- No strong agent-level pattern in dataset, suggesting training/tools matter more than individual performance

### Workspace Scale
- Customers with 5,000+ workspaces, 12,000+ automations, or 100k+ tasks show elevated resolution times
- Indicates system performance and investigation complexity increase with scale

### Integration Complexity
- Third-party integrations (Salesforce, NetSuite, Okta) average ~85 min (more investigation, coordination required)
- Native features average ~45 min

---

## Exceptions and Caveats

1. **Some Critical tickets resolve quickly (~45-55 min)** when the issue is a simple outage or clear regression. Real-time communication (phone) helps.

2. **Some High-priority email tickets take 160+ minutes**, suggesting the High label can indicate research-intensive problems rather than urgency.

3. **Feature requests on Low priority occasionally take 60-90 minutes** if they involve licensing, contracting, or special considerations (CS-0015, CS-0025, CS-0055).

4. **Chat-based Critical issues** (CS-0014, CS-0019) resolve in 45-90 minutes, showing channel efficiency can partially offset priority impact.

---

## Decision-Ready Recommendations

**Predict longer resolution times (80+ minutes) when tickets exhibit:**
- ✓ High or Critical priority level
- ✓ Email or phone channel (especially High + Email)
- ✓ Issue involves performance, data loss, security, or billing
- ✓ Description is detailed (>300 characters), indicating complex problem
- ✓ Requires third-party coordination or integration investigation
- ✓ References large-scale data or workspace configurations
- ✓ Requires audit trail, forensics, or financial reversals

**Predict shorter resolution times (< 40 minutes) when:**
- ✓ Low or Medium priority
- ✓ Chat or in-app channel
- ✓ Issue is a feature request, suggestion, or documentation question
- ✓ Brief description (<100 characters)
- ✓ Asynchronous resolution or roadmap acknowledgment sufficient

---

## Conclusion

Support ticket resolution time is primarily driven by **priority level** and **issue complexity** (reflected in type and description length), with **communication channel** acting as a strong secondary modifier. Email and High-priority combinations create the longest resolution windows. Organizations should consider routing complex issues to phone/chat channels and prioritizing detailed issue descriptions to enable faster first-response categorization.
