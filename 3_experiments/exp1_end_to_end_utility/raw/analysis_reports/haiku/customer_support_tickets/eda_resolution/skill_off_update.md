---
dataset: customer_support_tickets
scenario: eda_resolution
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "resolution_minutes"
query: "How does resolution time vary across issue themes, channel, and priority?"
source_table: augment_table/customer_support_tickets/eda_resolution/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:06:08.845458+00:00
wall_seconds: 60.44
---

# Resolution Time Analysis: Customer Support Tickets

## Executive Summary

Resolution time in this customer support dataset varies significantly across issue themes, channels, and priority levels. **High-priority tickets take 1.8× longer to resolve than Low-priority tickets** (mean: 131 vs 38 minutes), and **email-based tickets require 4.4× longer than chat** (mean: 98 vs 22 minutes). Performance and Billing/Pricing issues are the most time-intensive problem categories, while Feature Requests resolve fastest.

## Key Findings

### 1. Priority as a Primary Driver

**High-priority issues dominate resolution time:**
- **High priority**: 131 min mean (median: 131, range: 48–180)
- **Critical priority**: 74 min mean (median: 72.5, range: 45–110)
- **Medium priority**: 42 min mean (median: 37, range: 22–140)
- **Low priority**: 38 min mean (median: 24, range: 12–90)

Counterintuitive observation: **Critical tickets resolve faster than High-priority tickets** (74 vs 131 minutes). This suggests either (a) High-priority issues involve more investigation or coordination than genuinely critical outages, or (b) Critical issues receive urgent triage that bypasses lengthy problem-solving cycles. Low-priority issues, despite being numerous (n=74), resolve in roughly one-third the time of High-priority cases.

### 2. Channel-Based Patterns

**Email creates the largest resolution friction:**
- **Email**: 98 min mean (n=100, 40% of tickets)
- **Phone**: 70 min mean (n=50)
- **In-app**: 35 min mean (n=50)
- **Chat**: 22.5 min mean (n=50)

Email's high mean is driven by asynchronous communication and complexity; the distribution skews toward longer resolution (max 180 min). Chat's rapid resolution (median 23 min, range 12–48) reflects real-time interaction, though volume is lower. In-app messaging sits between these extremes, suggesting moderate complexity or wait times for backend investigation.

### 3. Issue Theme Severity Hierarchy

**Performance issues are the slowest to resolve:**
- **Performance**: 115 min mean (n=23, median: 135)
- **Billing/Pricing**: 78 min mean (n=18)
- **Integration**: 75 min mean (n=17)
- **Data Loss/Integrity**: 72 min mean (n=14)
- **Feature Requests**: 37 min mean (n=34, median: 24) ← *fastest*

The 3× difference between Performance (115 min) and Feature Requests (37 min) reflects investigation depth: performance troubleshooting requires profiling, benchmarking, and potential architectural review. Feature requests, by contrast, are scoped and prioritized conversations.

**UI/UX themes split evenly** (52 min mean, n=53) around the overall median, suggesting a mix of quick cosmetic fixes and complex interaction bugs.

**Authentication issues** (68 min mean, n=31) and **Infrastructure/Outage** (63 min mean, n=23) sit in the mid-range, likely balancing critical user-blocking incidents with routine access troubleshooting.

### 4. Priority × Channel Interactions

**High-priority email tickets are the slowest combination:**
- High + email: 133 min mean (n=49)
- Critical + in-app: 57.5 min mean (n=12)
- Critical + phone: 80 min mean (n=38)

**Low-priority chat tickets resolve fastest:**
- Low + chat: 16 min mean (n=24)

This pattern suggests that High-priority issues routed through email involve complex documentation review, multiple stakeholder coordination, or back-and-forth clarifications that asynchronous channels amplify.

### 5. Priority × Theme Interactions

**High-priority Performance issues are extreme outliers:**
- High + Performance: 142 min mean
- High + Feature Request: 129 min mean
- High + Other: 134 min mean
- High + Integration: 135 min mean

**Low-priority Data Loss/Integrity issues resolve immediately:**
- Low + Data Loss/Integrity: 15 min mean (n=2)
- Low + Performance: 20 min mean (n=1)

This dichotomy reveals that priority labeling is outcome-dependent: what the customer perceives as "High" (e.g., a slow report query) entails extended investigation, whereas actual data integrity loss at Low priority (e.g., cosmetic duplicate display) can be triaged and closed quickly. The high-priority label correlates with problem complexity, not merely impact severity.

## Data Quality Notes

- **Sample size**: 250 tickets across four priority levels, four channels, and ten issue themes.
- **Distribution imbalance**: Email dominates (100 tickets, 40%), while Security is rare (n=2). Low-priority tickets are overrepresented (74 tickets, 30%).
- **Resolution time definition**: Likely time-to-first-resolution or time-to-close; no escalation or reopening data are visible.
- **Outliers**: One Performance ticket took 180 minutes (High + email); one UI/UX ticket took 165 minutes (High + email). These are plausible for complex investigations.

## Implications for SLA and Routing

1. **Email is the operational bottleneck**: With 4.4× longer mean resolution than chat and 1.4× longer than phone, consider routing routine issues away from email or implementing triage gates.
2. **High-priority Performance issues need escalation pathways**: At 142 min for High + Performance combinations, standard email-based triage is insufficient; escalate to senior engineering immediately.
3. **Critical ≠ Long resolution**: The low resolution times for Critical priority (74 min) suggest effective incident response for outages. This inverts typical SLA logic.
4. **Feature Requests are disproportionately fast-tracked**: At 37 min mean resolution, these are likely requirement-gathering conversations rather than technical fixes.

## Conclusion

Resolution time is principally driven by **issue complexity and channel friction**, secondarily by **stated priority**. High-priority labels correlate with high investigation overhead (Performance, Integration, Feature Requests at High priority all exceed 130 min), while channel choice has a 4–5× performance impact. Performance and Billing/Pricing issues consistently exceed 75-min resolution; Feature Requests and UI/UX issues consistently resolve within 37–52 min. Teams seeking SLA improvements should prioritize email-to-chat migration for suitable issue types and implement fast-track escalation for Performance issues at any stated priority level.
