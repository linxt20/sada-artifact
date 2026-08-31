---
dataset: customer_support_tickets
scenario: eda_resolution
variant: original
model: substrate-claude-haiku-4-5
query_subtype: exploratory_data_analysis
focus_variable: "resolution_minutes"
query: "How does resolution time vary across issue themes, channel, and priority?"
source_table: augment_table/customer_support_tickets/eda_resolution/original.csv
generated_at: 2026-07-26T13:04:59.608519+00:00
wall_seconds: 50.45
---

# Resolution Time Analysis: Customer Support Tickets

## Executive Summary

This analysis examines how resolution time varies across three critical dimensions in a customer support dataset of 250 tickets: **issue themes**, **support channels**, and **priority levels**. The findings reveal substantial variation in resolution speed driven by priority and channel, with important interactions between these factors and issue type.

## Key Findings

### Overall Resolution Metrics
- **Mean resolution time:** 64.9 minutes
- **Median resolution time:** 58 minutes  
- **Range:** 12 to 180 minutes (3-hour maximum)
- **Standard deviation:** 41.1 minutes (indicates substantial variability)

### 1. Priority Drives Resolution Speed Most Strongly

Resolution time varies dramatically by priority level, following an inverse relationship with urgency:

| Priority | Avg. Time (min) | Median | Sample Size | Range |
|----------|-----------------|--------|-------------|-------|
| **Critical** | 74.4 | 72.5 | 50 | 45–110 |
| **High** | 131.1 | 131.0 | 50 | 48–180 |
| **Medium** | 41.6 | 37.0 | 76 | 22–140 |
| **Low** | 37.5 | 24.0 | 74 | 12–90 |

**Insight:** Counter-intuitively, High-priority tickets take 2x longer to resolve than Critical tickets (131 vs. 74 minutes). This suggests High-priority issues may involve complex investigations or require coordination, while Critical issues may receive expedited handling. Medium and Low tickets resolve relatively quickly (~37–42 min), clustering around the median.

### 2. Channel Strongly Influences Resolution Time

Channel choice shows the most consistent pattern in the data:

| Channel | Avg. Time (min) | Median | Sample Size | Range |
|---------|-----------------|--------|-------------|-------|
| **Email** | 98.3 | 92.5 | 100 | 46–180 |
| **Phone** | 70.2 | 72.5 | 50 | 36–110 |
| **In-App** | 35.0 | 31.0 | 50 | 18–70 |
| **Chat** | 22.5 | 23.0 | 50 | 12–48 |

**Insight:** Chat is fastest (mean 22.5 min), likely because issues are simpler or agent bandwidth allows synchronous problem-solving. Email is slowest (98.3 min), reflecting async back-and-forth, complex narrative issues, and documentation overhead. Phone and in-app occupy a middle ground. The 4× difference between fastest (chat) and slowest (email) channels is highly significant.

### 3. Issue Theme Correlates with Resolution Complexity

Extracted themes from issue descriptions show thematic variation:

| Theme | Avg. Time (min) | Median | Sample Size |
|-------|-----------------|--------|-------------|
| **Performance** | 103.0 | 130.0 | 21 |
| **Integration** | 80.2 | 65.0 | 5 |
| **Billing** | 76.9 | 80.0 | 19 |
| **Technical Error** | 73.4 | 65.0 | 49 |
| **Security** | 63.8 | 65.0 | 4 |
| **Other** | 63.8 | 55.0 | 33 |
| **Authentication** | 67.5 | 58.0 | 25 |
| **Inquiry** | 62.7 | 43.0 | 13 |
| **UI/UX** | 65.3 | 39.0 | 23 |
| **Feature Request** | 38.4 | 24.0 | 58 |

**Insight:** Performance issues take longest (103 min avg), likely requiring system investigation and potential rollback decisions. Feature requests resolve fastest (38 min), presumably because they require acknowledgment and scope discussion rather than technical resolution. Technical errors and billing issues cluster in the 70–80 minute range.

### 4. Critical Interactions Between Priority and Channel

Cross-tabulation reveals important structural patterns:

- **Critical tickets route only to phone (38 cases) or in-app (12 cases)**, never email or chat. This explains why Critical average is lower than High—they bypass the slow email channel.
- **High-priority tickets concentrate in email (49 of 50)**, explaining their 131-minute average. Email's inherent latency dominates this tier.
- **Low and Medium tickets distribute across all channels**, allowing channel-driven variation to appear.

**Key interaction:** A Critical issue via phone averages 79.7 min, while a High-priority issue via email averages 132.8 min—a 53-minute gap largely attributable to channel, not priority.

### 5. Theme × Channel Interaction

Performance issues in email average **130.5 min** vs. 21.5 min in chat (6× difference). Feature requests in email average **87.2 min** vs. 17.9 min in chat. These gaps suggest that complex themes hit email's async bottleneck harder than simple clarifications suited to chat.

### 6. Weak Evidence and Caveats

- **Security and integration themes have small sample sizes** (n=4 and n=5), limiting confidence in their statistics.
- **Agent variation is not analyzed** (50 agents across 250 tickets suggests ~5 tickets per agent on average), which may mask significant agent-to-agent performance differences.
- **Issue descriptions are not consistently categorized**; theme extraction is heuristic-based and may misclassify compound issues.
- **No temporal trend analysis** (data does not indicate ticket creation time), so resolution time does not account for workload or seasonal effects.

## Recommendations

1. **Email bottleneck:** Email's 98-minute average is the primary lever for improvement. Consider email-to-chat escalation for simpler issues or asynchronous email batching.
2. **Channel routing:** Ensure High-priority and Complex tickets bypass email when possible, preferring phone or in-app channels.
3. **Feature request triage:** At 38 min average, feature requests are fast but represent 23% of volume. Separate intake workflow could reduce noise in critical/high-priority queues.
4. **Performance investigation:** Performance issues exceed 103 min on average and should receive dedicated specialist routing rather than general queue.

## Limitations

This analysis grounds claims in observed column data (priority, channel, resolution_minutes) and extracted themes from descriptions. However, missing context—such as actual resolution success, rework rates, agent expertise, and business impact beyond time—limits the depth of causal inference. Resolution time alone does not measure quality or customer satisfaction.
