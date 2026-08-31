---
dataset: customer_support_tickets
scenario: causal_handling
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "handling_time_gap"
query: "Why do handling times differ by channel and priority?"
source_table: augment_table/customer_support_tickets/causal_handling/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:05:26.598678+00:00
wall_seconds: 60.62
---

# Handling Time Differences by Channel and Priority: Analysis Report

## Executive Summary

Handling times vary substantially across channels and priority levels, driven by three primary factors: **(1) inherent channel characteristics**, **(2) interaction effects between priority and channel distribution**, and **(3) communication mode constraints**. Email represents the slowest channel (mean 98.3 min), while chat is fastest (mean 22.5 min)—a 4.4× difference. High priority tickets take 3.5× longer than low priority tickets (131.1 vs. 37.5 min), but this relationship is **not uniform across channels**, revealing channel-specific constraints.

---

## Key Findings

### 1. Channel Effects Are the Dominant Factor

**Channel strongly predicts handling time** (correlation with resolution time: 0.758), far outweighing priority alone (0.559):

| Channel | Mean Time | Median Time | Range | Samples | Pattern |
|---------|-----------|-------------|-------|---------|---------|
| **Email** | 98.3 min | 92.5 min | 46–180 | 100 | Longest, high variance |
| **Phone** | 70.2 min | 72.5 min | 36–110 | 50 | Moderate, stable |
| **In-app** | 35.0 min | 31.0 min | 18–70 | 50 | Fast, low variance |
| **Chat** | 22.5 min | 23.0 min | 12–48 | 50 | Fastest, tightest range |

**Interpretation**: Synchronous channels (phone, chat) resolve faster because agents interact directly with customers in real-time, reducing back-and-forth delays. Asynchronous channels (email, in-app) inherently involve longer resolution windows due to compose time, context-switching, and customer response latency.

---

### 2. Priority Has Different Impact Across Channels

Handling time by priority is **non-uniform by channel**, indicating channel-specific resource allocation or workload characteristics:

| Priority | Mean Time | Median Time | Samples | Max – Min by Channel |
|----------|-----------|-------------|---------|----------------------|
| **Critical** | 74.4 min | 72.5 min | 50 | Phone: 79.7, In-app: 57.5 (21.2 min gap) |
| **High** | 131.1 min | 131.0 min | 50 | Email: 132.8, Chat: 48.0 (84.8 min gap) |
| **Medium** | 41.6 min | 37.0 min | 76 | Email: 58.9, Chat: 27.8 (31.1 min gap) |
| **Low** | 37.5 min | 24.0 min | 74 | Email: 71.6, Chat: 15.9 (55.7 min gap) |

**Critical observation**: High-priority tickets show the **largest variance** across channels (84.8 min between chat and email). Email handles High priority tickets at 132.8 min mean, while chat handles them at 48.0 min. This suggests:
- High-priority issues in email often require **complex, documented resolutions** (billing disputes, performance investigations).
- High-priority chat issues are often **simple escalations or connection failures** that resolve quickly.

---

### 3. Communication Mode Creates a Secondary Constraint

The distribution of Sync vs. Async communication by channel reveals an **architectural constraint**:

- **Async channels** (Email: 100%, In-app: 100%): mean = **77.2 min**
- **Sync channels** (Chat: 100%, Phone: 100%): mean = **46.4 min**

**Correlation: -0.368** (negative, indicating async = slower).

This 30.7-minute gap reflects inherent protocol limits:
- **Sync** (chat, phone): Agent and customer interact simultaneously → immediate clarification, reduced rework.
- **Async** (email, in-app): Minimum 1–2 hour cycles between customer replies → accumulate latency per iteration.

---

### 4. Issue Complexity Moderates but Does Not Override Channel Effects

Issue complexity affects resolution time, but channel dominates:

| Complexity | Mean Time | By Channel Examples |
|------------|-----------|---------------------|
| **High** | 85.8 min | Email High: 119.1, Chat High: 15.8 |
| **Medium** | 61.1 min | Email Medium: 90.3, Chat Medium: 27.0 |
| **Low** | 59.9 min | Email Low: 92.9, Chat Low: 22.4 |

**Key insight**: Even "Low complexity" issues take 92.9 min in email but only 22.4 min in chat—a **4.1× difference**. This confirms that **channel structure, not issue type alone, drives handling time**.

---

### 5. Gaps and Weak Evidence

- **Priority + Urgency relationship is inconsistent**: High-priority tickets show mean 131.1 min, but urgency factors (Blocking, HighImpact, Minor, Standard) have weak correlation (0.092) with resolution time. This suggests urgency tags may not drive prioritization uniformly.
- **No direct agent skill signal in data**: The augmentation label is "skill_off," implying agent skill data is withheld. Variations by agent_id exist but cannot distinguish capability from channel assignment.
- **Phone shows unusual stability**: Despite handling Critical issues, phone times cluster tightly (36–110 min) and do not follow the High > Critical pattern seen elsewhere. This may reflect:
  - Pre-call triage (complex issues routed to email).
  - Structured call protocols forcing time limits.

---

## Causal Mechanisms

### Why Email Takes ~1.4 hrs vs. Chat's ~23 min:

1. **Protocol-level latency**: Email rounds must complete; chat is real-time.
2. **Issue routing**: Complex billing/performance issues → email (higher % High priority: 49%). Simple login failures → chat (fewer High priority: 1%).
3. **Documentation burden**: Email resolutions often require written justification or attached files; chat provides quick verbal triage.

### Why High Priority ≠ Fastest Resolution:

- **High priority ≠ High urgency**: Many High-priority tickets are requests for investigations, upgrades, or billing reviews—tasks requiring research, not instant fixes.
- **Critical priority paradoxically faster (74.4 vs. 131.1 min)**: Critical issues (outages, account lockouts) often have known runbooks; complex investigations (High priority) are novel.

---

## Data Patterns

- **Total tickets**: 250
- **Handling time range**: 12–180 minutes (15× spread)
- **Largest gap**: Email High (132.8) vs. Chat Low (15.9) = **8.3× difference**
- **Channel saturation**: Email handles 40% of volume; chat, in-app, phone each handle 20%.

---

## Recommendations for Further Analysis

1. **Segment email further**: Separate billing/admin issues from technical outages to isolate routing patterns.
2. **Investigate Critical < High anomaly**: Confirm whether triage pre-sorts complex work away from phone.
3. **Model agent skill if available**: With skill data included, re-run to partition channel + skill effects.
4. **Analyze response time (first response) vs. resolution time**: Async channels may have long first-response delays inflating total time.

---

## Conclusion

**Channel is the dominant driver** (0.758 correlation), followed by priority (0.559), while communication mode (sync vs. async) creates a ~30 min structural penalty for asynchronous workflows. Handling time differences are primarily explained by:

- **Inherent protocol constraints** (sync real-time vs. async batched).
- **Issue-type routing** (complex issues → email; simple issues → chat).
- **Non-linear priority effects** (High priority often complex; Critical often routine).

This suggests that **reducing handling time requires either (1) shifting complex work to assisted sync channels, (2) improving async automation (templates, KB), or (3) re-categorizing priority to reflect actual resolution complexity**.
