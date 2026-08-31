---
dataset: customer_support_tickets
scenario: causal_handling
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "handling_time_gap"
query: "Why do handling times differ by channel and priority?"
source_table: augment_table/customer_support_tickets/causal_handling/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:10:30.392076+00:00
wall_seconds: 66.37
---

# Customer Support Ticket Handling Times: Channel and Priority Analysis

**Dataset:** 250 support tickets  
**Variant:** skill_on (v11_update)  
**Analysis Date:** 2026-07-30

## Executive Summary

Handling times vary significantly by channel and priority. **Email is slowest** (98.3 min average), while **chat is fastest** (22.5 min average). This difference stems from:
- **Channel selection by priority:** Email handles 98% of High priority cases; phone handles 76% of Critical cases; chat is limited to Low/Medium
- **Issue complexity:** High priority cases (avg 131.1 min) often require deeper investigation; Low priority cases (avg 37.5 min) are mostly guidance
- **Intervention requirements:** Urgent escalations and complex troubleshooting extend resolution times; simple guidance keeps them short

---

## Channel-Level Findings

### Email (100 tickets, 98.3 min average)
- **Slowest channel by far** – nearly 4.4× chat speed and 1.4× phone speed
- **Priority mix:** 49 High (avg 132.8 min), 26 Medium (avg 58.8 min), 25 Low (avg 71.6 min)
- **Top interventions:** Bug fix/hotfix (59 tickets), documentation/guidance (18 tickets)
- **Why slow:** Asynchronous nature allows complex issues to accumulate. High priority tickets (mostly billing disputes and performance investigations) require detailed investigation and often involve multiple follow-ups

### Phone (50 tickets, 70.2 min average)
- **Second slowest** but concentrated on critical issues
- **Priority mix:** 38 Critical (avg 79.7 min), 12 Medium (avg 40.0 min), 0 Low/High
- **Top intervention:** 54% require urgent escalation/bridge calls (27/50 tickets)
- **Why moderate speed:** Real-time communication accelerates resolution for crisis situations, but Critical issues inherently take longer. Urgent escalations average 78.1 min

### In-App (50 tickets, 35.0 min average)
- **Moderate speed** with concentrated Critical support
- **Priority mix:** 25 Low (avg 24.2 min), 13 Medium (avg 35.2 min), 12 Critical (avg 57.5 min)
- **Top interventions:** 50% marked "not_present" (feature requests), 30% bug fixes
- **Why moderate:** Context-aware support (users already in the product) enables faster guidance. Critical cases still take longer due to system outages

### Chat (50 tickets, 22.5 min average)
- **Fastest channel** – specialised in quick resolution
- **Priority mix:** 25 Medium (avg 27.8 min), 24 Low (avg 15.9 min), 1 High (avg 48.0 min)
- **Top interventions:** 50% not_present (guidance/feature requests), 46% bug fixes
- **Why fast:** Excludes High/Critical cases by design. Medium and Low tickets are mostly straightforward guidance or simple feature requests requiring minimal investigation

---

## Priority-Level Findings

### High Priority (50 tickets, 131.1 min average) – LONGEST
- **Nearly exclusive to email:** 49/50 tickets (98%)
- **Issue types:** Billing disputes, performance degradation, investigation-heavy topics
- **Intervention mix:** 72% bug fixes requiring engineering review, 8% urgent escalation
- **Why slow:** Email channel + need for detailed investigation + often requires cross-team coordination

### Critical (50 tickets, 74.4 min average)
- **Routed primarily to phone:** 38/50 (76%)
- **Smaller cohorts:** 12 in-app, 0 email, 0 chat
- **Intervention mix:** 66% urgent escalation/bridge calls, 16% bug fixes, 8% data recovery
- **Why moderate:** Real-time phone channels accelerate crisis response, but severity of issues (production outages, security issues, data loss) naturally extends resolution time

### Medium (76 tickets, 41.6 min average)
- **Balanced across all channels:** 26 email, 25 chat, 13 in-app, 12 phone
- **Resolution times by channel:** Email 58.8 min, phone 40.0 min, in-app 35.2 min, chat 27.8 min
- **Intervention mix:** 87% bug fixes, 4% urgent escalation
- **Why moderate:** Mixed complexity; chat handles simpler Medium cases (27.8 min); email handles more complex ones (58.8 min)

### Low (74 tickets, 37.5 min average)
- **Chat-dominated for speed:** 24 via chat (avg 15.9 min) vs 25 via email (avg 71.6 min)
- **Intervention mix:** 64% not_present (feature requests/guidance), 24% documentation only
- **Why variable:** Chat handles quick guidance efficiently; email's slower speed even for Low priority suggests accumulation of documentation requests with thoughtful responses
- **Important exception:** Email's Low priority tickets average 71.6 min despite simple interventions—suggests asynchronous review cycles

---

## Cross-Channel × Priority Patterns

The most telling patterns emerge from interaction effects:

| Priority | Chat | Email | In-App | Phone |
|----------|------|-------|--------|-------|
| **Critical** | — | — | 57.5 min | 79.7 min |
| **High** | 48.0 min | 132.8 min | — | — |
| **Medium** | 27.8 min | 58.8 min | 35.2 min | 40.0 min |
| **Low** | 15.9 min | 71.6 min | 24.2 min | — |

**Key insight:** The same priority level resolves at vastly different speeds based on channel:
- **High priority:** Chat would be 2.8× faster (48 min) than email (133 min)—but High issues don't come through chat
- **Low priority:** Chat is 4.5× faster (16 min) than email (72 min)
- **Critical on phone (79.7 min) vs in-app (57.5 min):** ~40% faster in-app, likely because in-app issues are narrower in scope

---

## Resolution Intervention Effects

**Urgent escalations** (41 tickets, 81.9 min avg):
- By design, the slowest path—requires multiple teams and bridge calls
- Email escalations are slowest (135 min avg), suggesting cascading delays
- Phone escalations are fastest (78.1 min avg) despite high urgency, likely because real-time communication shortens decision loops

**Bug fixes** (110 tickets, 73.5 min avg):
- Highly variable by channel and priority
- Email bug fixes: 104 min avg (engineering investigation needed)
- Chat bug fixes: 28 min avg (simpler, confirmed issue)
- High priority bug fixes: 132.6 min avg (thorough analysis)
- Medium priority bug fixes: 41.6 min avg (faster engineering turnaround)

**Documentation/guidance** (19 tickets, 72.3 min avg):
- Surprisingly long given perceived simplicity
- Email documentation: 75.6 min avg
- Chat documentation: 13 min avg (consistent with channel speed)
- Suggests email documentation requests receive detailed, crafted responses

**Not_present/feature requests** (77 tickets):
- Fastest path: chat (avg ~20 min) where 50% of tickets fall here
- Longer in email (avg ~70 min) where they are less common

---

## Causal Factors Affecting Handling Time

### Channel Design
- **Chat** is optimised for synchronous, quick resolution (real-time feedback)
- **Email** is designed for asynchronous, thorough investigation
- **Phone** is reserved for real-time crises (Critical/outages)
- **In-app** provides context-aware, embedded support

### Issue Complexity & Priority Routing
- **High complexity issues cluster in email** (billing disputes, performance investigations require written documentation, cross-team handoffs)
- **Critical issues cluster in phone** (time-sensitive, decision-required situations benefit from verbal confirmation)
- **Simple requests cluster in chat** (guidance, quick troubleshooting)

### Intervention Logistics
- **Urgent escalations** require coordination across multiple teams, naturally extending time
- **Bug fixes** in email require engineering review cycles; in chat, confirmation is immediate
- **Documentation** in email is more thorough (written for reference); in chat, it's brief

### Batch vs. Real-Time Processing
- **Email** inherently batches (agent reviews multiple messages, investigates offline, responds asynchronously)
- **Chat/phone** process synchronously with immediate feedback
- **In-app** splits the difference: real-time UI but asynchronous backend resolution

---

## Important Caveats & Weak Evidence

1. **Causal routing bias:** Channel choice is not random—High priority cases naturally route to email (documentation-friendly), Critical to phone (real-time). The slower email times may partly reflect issue type, not channel inefficiency.

2. **Email outlier:** Low priority email tickets (71.6 min) are surprisingly slow given "simple" interventions. This may indicate:
   - Agents batch Low priority responses and review cycles add delay
   - Documentation requests receive more polished responses
   - Or accumulation in the email queue

3. **Limited sample for some cells:** 
   - Only 1 High priority ticket via chat
   - 0 Critical tickets via email
   - Cells with n<5 should be interpreted cautiously

4. **Agent efficiency not controlled:** Different agents (20 total) may have different speeds; high variance within channels (chat std dev 7.3, email std dev 37.8) suggests other factors at play

5. **"Skill_on" variant:** The v11_update label suggests this may be a control or variant dataset. Results reflect this specific configuration only.

---

## Recommendations (Exploratory)

- **To speed email:** Implement asynchronous escalation queues or parallel engineering review for High priority cases
- **To maintain chat speed:** Ensure simple cases remain routed to chat; complexity detection might auto-escalate
- **To optimise phone:** Real-time handling is working—focus on critical issue prevention rather than resolution speed
- **To audit Low priority:** Investigate why email Low tickets average 72 min; is this agents being thorough or workflow inefficiency?

---

**Report Complete**
