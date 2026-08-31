---
dataset: customer_support_tickets
scenario: causal_handling
variant: original
model: substrate-claude-haiku-4-5
query_subtype: causal_attribution
focus_variable: "handling_time_gap"
query: "Why do handling times differ by channel and priority?"
source_table: augment_table/customer_support_tickets/causal_handling/original.csv
source_report: dataset_portion_2/substrate-claude-haiku-4-5/customer_support_tickets__causal_handling/analyses/original/analysis.md
wall_seconds: 45.32
---

# Handling Times by Channel and Priority: Analysis Report

## Key Findings

Handling times differ substantially by both **channel** and **priority**, with **priority emerging as the stronger determinant** of resolution speed.

### Priority Impact (Primary Factor)

The dataset shows a clear inverse relationship between priority level and handling time:

- **Critical priority**: Mean ~75 minutes (median ~70 min) – fastest resolution
- **High priority**: Mean ~130 minutes (median ~125 min) – slower than critical
- **Medium priority**: Mean ~46 minutes (median ~40 min) – fastest average handling
- **Low priority**: Mean ~50 minutes (median ~55 min) – comparable to medium

**Paradox**: Critical incidents resolve faster than high-priority issues, suggesting that critical problems may trigger more direct escalation paths and dedicated resources, while high-priority issues may require more procedural handling (billing issues, performance investigations). Medium and low priorities cluster together, indicating routine triage assigns similar handling patterns regardless of urgency designation.

### Channel Impact (Secondary Factor)

Resolution times vary by channel:

- **Phone**: Mean ~80 minutes (median ~80 min) – highest variation, includes both rapid tactical fixes and complex live-support sessions
- **Email**: Mean ~100 minutes (median ~105 min) – reflects asynchronous back-and-forth, diagnostic gathering, and documentation requirements
- **Chat**: Mean ~27 minutes (median ~26 min) – fastest channel, suggests focused real-time problem-solving
- **In-app**: Mean ~35 minutes (median ~33 min) – second-fastest, likely feature requests and UI issues resolved quickly

**Pattern**: Synchronous channels (chat, in-app) resolve faster than asynchronous channels (email, phone). Chat in particular shows 73% faster mean handling than email, and 66% faster than phone.

### Channel × Priority Interaction

Cross-tabulation analysis reveals important interactions:

- **Phone for critical incidents**: ~78 min average – balances urgency with complexity
- **Email for critical incidents**: ~70 min average – asynchronous critical issues may be simpler (configuration, documentation)
- **Chat for all priorities**: Consistently short (12–33 min range) – suggests constrained interaction window
- **In-app across priorities**: Narrow range (18–40 min) – suggests lightweight issue scope

## Notable Patterns and Exceptions

1. **Email persistence**: Despite being asynchronous, email's high average (100 min) reflects that billing, performance, and data-related issues (common in email channel) require more investigation. The top 5 longest email tickets (155–180 min) involve billing discrepancies, memory leaks, and schema changes.

2. **Phone channel volatility**: Phone ranges from 14 minutes (Low priority feature request, CS-0011) to 110 minutes (Critical SSO outage, CS-0009), indicating that channel is used for both quick clarifications and high-stakes incidents.

3. **Chat efficiency**: Chat remains fast even for High and Critical priorities (typically 24–48 min), suggesting either that chat tends to attract narrower scope issues or that the real-time format naturally caps interaction length.

4. **In-app consistency**: In-app channel shows the tightest clustering (SD ~8 min), implying feature requests and UI bugs follow predictable resolution paths.

5. **Medium priority scale**: Medium has the most records (n~64), dominating the dataset. Both High and Critical have smaller samples, which may affect generalizability of high-priority conclusions.

## Factors Relevant to Dataset Focus

The dataset's **causal_handling** focus suggests these patterns reflect:

- **Resource allocation**: Critical incidents bypass standard queues; high-priority issues route to experienced agents but face normal SLAs.
- **Scope variation by channel**: Email and phone attract complex, investigation-heavy issues; chat and in-app handle feature requests and quick fixes.
- **Synchronous efficiency**: Real-time channels (phone, chat) constrain conversation duration naturally, while email permits back-and-forth that extends resolution.
- **Agent expertise**: Phone agents (AG-001, AG-004, AG-007, AG-011, AG-014) handle high-priority and critical incidents but may still require extended troubleshooting for production outages.

## Limitations and Weak Evidence

- **No direct causation**: Channel and priority are observed, not experimentally manipulated; longer email times may reflect issue complexity rather than channel choice.
- **Small critical sample**: Only ~18 critical tickets. Statistical confidence is limited.
- **No control for issue type**: Resolution time may correlate more strongly with "issue category" (billing vs. outage vs. feature request) than with channel or priority alone.
- **Agent variability unexplored**: Different agents show different mean times; individual agent skill/specialization may confound channel/priority effects.

## Conclusion

Handling times differ meaningfully by both channel and priority, but through different mechanisms:
- **Priority** determines how quickly work is _started_ and escalated.
- **Channel** determines _how_ the work proceeds (synchronous rapid exchange vs. asynchronous deep investigation).

**Decision-ready insight**: To reduce handling times, focus on (1) accelerating high-priority issue triage (which underperforms relative to critical), and (2) migrating suitable high-priority issues to chat/in-app when possible, which offer 65–70% speed gains over email and phone.
