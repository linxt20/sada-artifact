---
dataset: customer_support_tickets
scenario: eda_resolution
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_minutes"
query: "How does resolution time vary across issue themes, channel, and priority?"
source_table: augment_table/customer_support_tickets/eda_resolution/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:10:44.727630+00:00
wall_seconds: 47.31
---

# Resolution Time Analysis: Patterns Across Priority, Channel, and Issue Theme
**Dataset:** customer_support_tickets (250 tickets)  
**Analysis Focus:** skill_on_v11_update variant  

## Executive Summary

Resolution time varies dramatically across priority levels, communication channels, and issue types, with interaction effects that reveal operational priorities and resource constraints. **High-priority tickets in email channels take 3x longer than low-priority chat tickets** (132.8 vs. 15.9 minutes), though this reflects both genuine complexity and channel capacity differences. Performance degradation issues are consistently the longest to resolve (116.5 min avg), while feature requests resolve fastest (22.1 min avg).

## Key Findings

### 1. Priority Level Impact

Priority is the strongest predictor of resolution time (correlation: 0.559 with resolution minutes).

| Priority | Avg Time | Median | Range | Count |
|----------|----------|--------|-------|-------|
| **High** | **131.1 min** | 131.0 | 48–180 | 50 |
| **Critical** | 74.4 min | 72.5 | 45–110 | 50 |
| **Medium** | 41.6 min | 37.0 | 22–140 | 76 |
| **Low** | 37.5 min | 24.0 | 12–90 | 74 |

**Unexpected pattern:** Critical tickets resolve *faster* (74 min) than High-priority tickets (131 min). This suggests High-priority tickets may involve complex escalations or lower-priority issues with inflated severity labels, while Critical issues receive immediate resource allocation and faster routing to engineers.

### 2. Channel Impact

Communication channel correlates with resolution speed, ranging from 2.2× variation (chat to email):

| Channel | Avg Time | Median | Count |
|---------|----------|--------|-------|
| **Email** | **98.3 min** | 92.5 | 100 |
| **Phone** | 70.2 min | 72.5 | 50 |
| **In-app** | 35.0 min | 31.0 | 50 |
| **Chat** | 22.5 min | 23.0 | 50 |

Email shows the highest resolution time, likely due to async back-and-forth with customers requiring context reconstruction at each step. Chat's brevity and real-time synchronization enable rapid resolution. In-app (internal/support tools) falls between phone and chat, suggesting agent-to-developer ticket routing overhead.

### 3. Issue Theme (Category) Impact

Issue type drives complexity independent of priority. Performance degradation and billing issues demand investigation; feature requests are triaged quickly.

| Category | Avg Time | Median | Count |
|----------|----------|--------|-------|
| **Performance degradation** | **116.5 min** | 131.0 | 44 |
| **Billing issue** | 93.5 min | 90.0 | 10 |
| **Data integrity** | 73.1 min | 67.5 | 34 |
| **Authentication/access** | 72.4 min | 62.0 | 35 |
| **Documentation clarification** | 68.4 min | 70.0 | 23 |
| **Integration failure** | 61.9 min | 60.0 | 11 |
| **UI/UX bug** | 40.9 min | 33.5 | 44 |
| **Feature request** | **22.1 min** | 21.0 | 49 |

The 5× gap between performance degradation (116.5 min) and feature requests (22.1 min) reflects engineering investigation time. Infrastructure issues demand diagnosis; cosmetic enhancements can be acknowledged and queued without immediate action.

### 4. Critical Interaction Patterns

#### High-Priority Email Anomaly
**High-priority tickets via email average 132.8 minutes**—the highest in the dataset. Breakdown:
- 49 High+email tickets, mean 132.8 min
- Performance degradation dominates this group (31/49 tickets, 137.4 min avg)
- Data integrity adds 124.7 min avg for High+email
- Billing issues take 118.3 min

This channel/priority combination creates a bottleneck: complex technical issues (performance degradation) arrive asynchronously via email, forcing extended investigation cycles with limited real-time collaboration.

#### Low-Priority Chat Efficiency  
**Low-priority chat tickets resolve in 15.9 minutes** (the baseline efficiency):
- 24 Low+chat tickets
- Dominated by feature requests (22/24), which resolve in 21.8 min (Low priority)
- Allows quick triage: "noted for roadmap" with minimal engagement

#### Critical Priority Distribution  
Critical tickets split across channels differently than High priority:
- **In-app (12 tickets, 57.5 min):** Fastest critical resolution
- **Phone (38 tickets, 79.7 min):** Standard critical response time
- Notably *no* Critical tickets via email, suggesting priority escalation bypasses async channels when urgent

#### Medium Priority Balancing  
Medium priority shows more uniform channel distribution (chat: 27.8 min, email: 58.8 min), indicating these are handled in steady-state mode without special routing.

### 5. Issue Theme × Priority Interactions

**High-priority performance degradation (32 tickets) averages 137.4 minutes**—the single slowest category-priority combination, with 5 tickets hitting the 155–180 minute ceiling. These are likely infrastructure outages requiring coordination across multiple teams.

**Low-priority feature requests (48 tickets) average 21.8 minutes**, confirming that requestor urgency combined with solution simplicity enables rapid acknowledgment.

Critical authentication/access issues average 82.5 min (14 tickets), reflecting the mix of easy credential resets and complex IdP integration debugging.

## Potential Exceptions or Weak Evidence

1. **Critical email gap:** No Critical tickets routed via email raises a question: are they reclassified to High, filtered to phone/in-app, or genuinely rare? The absence itself is data, but without routing rules context, the pattern cannot be fully explained.

2. **High-priority chat outlier:** Single High-priority chat ticket (48 min) is too small to establish a trend; High tickets may be intentionally routed away from chat.

3. **Email's structural delay:** The email channel's consistent slowness (98.3 min avg) likely reflects message latency and async back-and-forth, not agent speed. Same tickets via phone might resolve faster with real-time dialogue.

4. **Performance degradation skew:** This category's extreme range (38–180 min) and high std dev (39.5) suggests it contains both quick diagnostics ("rollback completed") and multi-hour investigations. Median (131 min) closer to mean than for other categories, supporting genuine bimodal distribution.

## Conclusions & Decision Readiness

**Resolution time is optimized by aligning issue complexity with channel capability:**
- **Route urgent technical issues (Critical/High + performance/auth) to phone or in-app** to enable synchronous debugging and reduce email's 2–3× latency penalty.
- **Email is appropriate for Low/Medium priority clarifications and feature requests**, which tolerate async delays.
- **Chat should remain restricted to simpler issues** (Low/Medium priority, feature requests, documentation clarification); expanding to complex issues will likely inflate resolution times beyond the 22.5-min baseline.

**High-priority tickets averaging 131 minutes warrant review:** either the severity classification is inflated for complex-but-non-critical issues, or these genuinely require deep investigation. Cross-referencing with SLA targets would clarify if this is acceptable or a bottleneck.

**Issue theme is as predictive as priority**, suggesting triage logic should weight issue type (e.g., "performance degradation" → escalate; "feature request" → queue) alongside priority label to optimize staffing.
