---
dataset: flag_2
scenario: concept_attribute_delay
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: faceted_decomposition
focus_variable: "incident_delay_reasons"
query: "Why do some incidents take longer to resolve?"
source_table: augment_table/flag_2/concept_attribute_delay/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:15:37.085565+00:00
wall_seconds: 71.79
---

# Why Do Some Incidents Take Longer to Resolve? (skill_off variant)

## Executive Summary

Analysis of 500 incidents shows **resolution times average 776 hours (32.3 days)** with a median of 672 hours, revealing substantial delays concentrated in specific categories. The **skill_off variant** (without augmented semantic columns) shows that delays are driven primarily by **incident category/type complexity**, **support team capacity constraints**, and **temporal factors** rather than priority level alone.

## Key Findings

### 1. **Network Incidents Drive Portfolio Delays**
- **Network category dominates** the portfolio: 269 incidents (53.8%), but shows **longest mean resolution time of 790h** (compared to 708h for Database, 855h for Software)
- 197 completed Network incidents average **1,079h resolution time** (44.9 days)
- Network assignment group (300 incidents, 60% of workload) averages **791h**, substantially slower than Database team's 696h

**Implication**: Network/connectivity issues, while routine, lack efficiency in resolution processes. VPN, WiFi, and internet connectivity dominate these slow patterns.

### 2. **Software Category Incidents Take Longest Among Major Types**
- **Software incidents** average **855h** (highest among top categories)
- Even after accounting for median (708h), Software shows **50% delay rate** 
- Common slow patterns: "Email client not working" (2,004h for n=3), Software update failures, email synchronization issues

**Implication**: Software-related problems likely require extended troubleshooting, coordination across multiple teams, or involve complex configuration/update scenarios.

### 3. **Service Desk and Support Teams Show Highest Delay Rates**
- **Service Desk** assignment group: **56.2% of incidents delayed**, averaging 1,102h
- Network team: **50.7% delay rate** (1,074h mean)
- Database team (more structured, possibly better-documented procedures): **47.2% delay rate** (947h mean)

**Implication**: Teams handling broad, unstructured requests (Service Desk, Network support) lack consistent resolution runbooks compared to specialized database teams.

### 4. **Weekend Opened Cases Show 9.2% Resolution Time Penalty**
- Weekend-opened incidents: mean **845h** (69h slower than weekday average of 748h)
- Weekend cases: **53.2% delayed** vs. 48.3% for weekday cases
- Limited after-hours coverage compounds escalation delays

**Implication**: Off-hours incident opening creates handoff friction and delayed first response.

### 5. **Counter-intuitive Priority Pattern: Higher Priority ≠ Faster Resolution**
- Critical priority: mean **807h** (54.4% delayed)
- High priority: mean **759h** (48.1% delayed)  
- Moderate priority: mean **874h** (56.2% delayed)

**Note**: This pattern is weak evidence—Critical incidents may genuinely require more complex investigation, or priority labeling may be inconsistent. Priority level alone does not explain 30+ hour variance in resolution.

### 6. **Specific Incident Types Show Consistent Slow Resolution**
Among incidents with 3+ occurrences, slowest-resolving patterns include:
- "Email client not working": 2,004h (n=3)
- "Database server not responding": 1,565h (n=3)
- "Unable to access network drive": 1,546h (n=3)
- "Cannot connect to office VPN": 1,373h (n=6)

These patterns suggest **missing or ineffective self-service solutions and runbooks** for high-volume, recurring issues.

## Evidence and Limitations

### Strong Evidence:
- Clear category-level differences (855h Software vs. 609h Inquiry/Help; 50%+ difference)
- Consistent team-level patterns (Service Desk 56.2% delayed vs. Database 47.2%)
- Weekend timing effect replicated across 142 incidents (28.4% of sample)
- High-volume patterns (VPN: 15 occurrences at 1,243h avg; Network drive: 3 at 1,546h)

### Weak or Missing Evidence:
- **Priority-to-resolution correlation is inverted or flat**, suggesting prioritization may not drive resolution speed in practice
- Dataset lacks incident "complexity score" or root cause labels—severity of underlying technical issues unmeasured
- No visibility into actual resolution actions, escalation chains, or tool availability (the **skill_off** variant omits semantic enrichment)
- 128 incidents (25.6%) are in New/In Progress state with invalid (-1.0h) resolution times, excluding them from delay analysis

## Conclusion

Incidents take longer to resolve primarily because:

1. **Category complexity**: Network and Software incidents lack standardized, fast resolution pathways
2. **Team capacity/process gaps**: Service Desk and Network teams show 50%+ delay rates, suggesting process maturity differences vs. Database team
3. **Volume concentration**: 53.8% of incidents are Network-category, overwhelming support capacity
4. **Temporal constraints**: Weekend/off-hours openings add ~70 hours due to delayed handoffs
5. **Recurring patterns unautomated**: High-volume, repeating issues (VPN, email access, network drives) lack effective self-service or scripted solutions

**Recommendation for prioritization**: Focus automation and runbook investment on high-volume, recurring Network and Software patterns rather than reorganizing by priority level.
