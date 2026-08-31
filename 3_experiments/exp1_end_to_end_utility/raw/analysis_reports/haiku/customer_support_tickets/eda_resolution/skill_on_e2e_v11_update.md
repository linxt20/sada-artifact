---
dataset: customer_support_tickets
scenario: eda_resolution
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "resolution_minutes"
query: "How does resolution time vary across issue themes, channel, and priority?"
source_table: augment_table/customer_support_tickets/eda_resolution/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:13:15.112877+00:00
wall_seconds: 190.12
---

# Resolution Time Analysis: Customer Support Tickets EDA

**Query:** How does resolution time vary across issue themes, channel, and priority?

**Dataset:** 250 customer support tickets  
**Outcome Variable:** `resolution_minutes` (mean = 64.9 min, median = 58.0 min, range = 12–180 min)  
**Primary Drivers:** `priority`, `channel`, `issue_theme` (original structured fields)  
**TAPP-Generated Columns Used:** `urgency_and_blocker_status`, `issue_type`

---

## Executive Summary

Resolution time is primarily driven by a combination of **priority level, communication channel, and issue theme**. High-priority (High) tickets via email require 131 minutes on average—more than **5× longer** than low-priority chat inquiries (16 minutes). The relationship is highly interactive: 

- **Channel effect is strongest:** Chat is fastest (22.5 min mean), email is slowest (98.3 min mean).
- **Priority paradox:** High-priority tickets take longest (131 min); Critical tickets are faster (74 min).
- **Issue theme matters more for High priority:** Performance issues via email drive extreme resolution times (142 min mean).
- **TAPP-generated facets add semantic clarity** but are substantially redundant with priority and issue type classifications.

---

## Primary Findings

### 1. Channel Effect (Strongest Signal)

| Channel | n   | Mean (min) | Median | Std Dev | Range |
|---------|-----|-----------|--------|---------|-------|
| **Chat**   | 50  | 22.5      | 23.0   | 7.3     | 12–48 |
| **In-app** | 50  | 35.0      | 31.0   | 14.1    | 18–70 |
| **Phone**  | 50  | 70.2      | 72.5   | 20.3    | 36–110 |
| **Email**  | 100 | 98.3      | 92.5   | 37.8    | 46–180 |

**Chat is 4.4× faster than email** (median: 23 vs. 92.5 min). In-app and phone occupy middle ground. Email's high variance (SD = 37.8) and wide range reflect complex issues requiring detailed investigation.

### 2. Priority Effect (Complex, Non-Monotonic)

| Priority   | n  | Mean (min) | Median | Std Dev | Range |
|------------|----|-----------| -------|---------|-------|
| **High**     | 50 | **131.1**    | 131.0  | 21.1    | 48–180 |
| **Critical** | 50 | 74.4       | 72.5   | 14.7    | 45–110 |
| **Medium**   | 76 | 41.6       | 37.0   | 16.7    | 22–140 |
| **Low**      | 74 | 37.5       | 24.0   | 25.5    | 12–90  |

**Counterintuitive insight:** High-priority tickets take 1.8× longer than Critical tickets. Critical priority (50 tickets) are concentrated in phone channel (n=38) and in-app (n=12), both with shorter median times. High-priority tickets (50 tickets) concentrate in email (n=49), which intrinsically takes longer. This is a channel confound, not a true priority effect.

**Interpretation:** Priority label does not directly measure resolution speed; it reflects issue complexity and communication medium.

### 3. Issue Theme Effect (Strongest Semantic Driver)

| Issue Theme               | n   | Mean (min) | Median | Range |
|---------------------------|-----|-----------|--------|-------|
| **Performance**             | 35  | 128.0     | 140.0  | 48–180 |
| **Data Management**         | 11  | 92.6      | 80.0   | 65–160 |
| **Billing Account**         | 23  | 84.4      | 80.0   | 55–135 |
| **Integration**             | 10  | 77.1      | 77.5   | 36–115 |
| **Authentication/SSO**      | 24  | 71.0      | 63.5   | 22–120 |
| **Functionality**           | 67  | 58.3      | 50.0   | 24–140 |
| **UX Enhancement**          | 29  | 34.8      | 30.0   | 14–115 |
| **Feature Request**         | 50  | **26.4**      | 21.5   | 12–90  |

Performance issues require **4.8× longer resolution** than feature requests (128 vs. 26 min). Performance issues are technically complex (require investigation, root cause analysis). Feature requests are routing/triaging decisions.

### 4. Two-Way Interaction: Priority × Channel

The highest resolution times occur at the intersection of **High priority + Email**:

| Priority × Channel | n  | Mean (min) | Median |
|--------------------|----|-----------| -------|
| **High + Email**     | 49 | 132.8     | 132.0 |
| **Critical + Phone** | 38 | 79.7      | 80.0  |
| **Medium + Email**   | 26 | 58.8      | 55.0  |
| **Low + Email**      | 25 | 71.6      | 70.0  |
| **Low + Chat**       | 24 | 15.9      | 16.0  |

The 132.8-minute mean for High+Email is driven by email's inherent communication overhead, not High priority per se. Critical+Phone (80 min) shows prioritization in a higher-bandwidth channel resolves faster.

### 5. Three-Way Interaction: Priority × Channel × Issue Theme

The most extreme case: **High priority + Email + Performance issues** (n=29, mean = 141.8 min, median = 140 min). These are technically sophisticated problems (performance debugging) routed via asynchronous email communication, creating a compounding delay effect.

Fastest resolution: **Low priority + Chat + Feature Requests** (n=22, mean = 15.9 min). These are simple requests handled in real-time synchronous conversation.

**Table: Top 5 slowest combinations (min n ≥ 3):**

| Priority | Channel | Issue Theme         | n  | Mean   |
|----------|---------|---------------------|----|----|
| High     | Email   | Performance         | 29 | 141.8  |
| High     | Email   | Data Management     | 3  | 131.0  |
| High     | Email   | Functionality       | 9  | 120.7  |
| High     | Email   | Billing Account     | 3  | 118.3  |
| Medium   | Email   | Functionality       | 17 | 59.6   |

---

## TAPP-Generated Columns: Semantic Evaluation

### Urgency and Blocker Status

The TAPP column `urgency_and_blocker_status` captures business impact dimensions missing from raw priority:

| Urgency Status          | n  | Mean (min) | Median |
|-------------------------|----|-----------| -------|
| **Time-Sensitive**        | 3  | 106.0     | 130.0 |
| **Revenue Risk**          | 11 | 92.7      | 85.0  |
| **Customer Blocked**      | 51 | 88.3      | 80.0  |
| **High-Impact Outage**    | 20 | 74.3      | 70.0  |
| **User Friction**         | 92 | 68.0      | 50.0  |
| **Enhancement Only**      | 72 | 35.7      | 24.0  |

**Value Added:** This column distinguishes blocking vs. enhancement urgency within the same priority level (e.g., Low priority + revenue risk ≠ Low priority + enhancement). However, this semantic distinction is largely determined by `issue_type` (bug vs. feature), not independent enrichment. The ranking aligns closely with resolution patterns driven by problem category, not novel semantic signal.

**Assessment:** Marginally useful for SLA segmentation; substantively redundant with `issue_type` + `priority` for prediction. Low coverage edge case: 1 missing value.

### Issue Type

The TAPP column `issue_type` provides finer taxonomy within `issue_theme`:

| Issue Type              | n  | Mean (min) | Median |
|-------------------------|----|-----------| -------|
| **Bug Performance**       | 28 | 138.1     | 140.0 |
| **Billing Error**         | 6  | 103.3     | 95.0  |
| **Bug Data Integrity**    | 10 | 92.0      | 82.5  |
| **API Auth Error**        | 9  | 77.8      | 80.0  |
| **Bug Functionality**     | 86 | 56.8      | 46.0  |
| **Documentation Gap**     | 22 | 69.4      | 70.0  |
| **Feature Request**       | 63 | 30.2      | 23.0  |
| **Infrastructure Outage** | 18 | 67.7      | 62.5  |

**Value Added:** Discriminates among bugs: performance bugs are 2.4× slower (138 min) than functionality bugs (57 min). This reflects that performance investigation requires profiling/load testing vs. reproducible step identification. Full coverage (250/250 rows).

**Assessment:** Adds moderate discriminatory signal within broad themes. Feature requests and infrastructure outages are cleanly separated. Should be retained for targeted resolution strategies (e.g., routing performance bugs to senior engineers).

---

## Interaction Between Original and TAPP Columns

**Priority vs. Urgency Status:** High priority concentrates in customer_blocked (n=17) and user_friction (n=26). Critical priority concentrates in customer_blocked (n=23) and high_impact_outage (n=19). The outage classification explains why Critical does not show longest times—outages resolve faster in phone channel. The semantic distinction provides mild explanatory power for the priority paradox but does not restructure primary patterns.

**Issue Theme vs. Issue Type:** 
- Performance theme = 100% bug_performance type (monolithic, no refinement).
- Functionality theme = mostly bug_functionality (76/86 bug_functionality type within it), but includes infrastructure_outage and documentation_gap.
- Feature request theme = 100% feature_request type (exact redundancy).

**Conclusion:** `issue_type` adds orthogonal detail within broad themes but does not discover new resolution drivers. Complements rather than replaces `issue_theme`.

---

## Key Patterns & Decision Points

### Pattern 1: Channel Dominates for Simple Issues
- **Chat:** Fastest across all priorities. 47 of 72 fast tickets (≤30 min) use chat; 43 are feature requests.
- **Implication:** Route simple requests (feature requests, documentation questions) to chat for real-time triage.

### Pattern 2: Email Scales Resolution Time Regardless of Priority
- Email is 4.4× slower than chat (98 vs. 22 min mean).
- This holds even for Low-priority issues (chat: 16 min, email: 72 min).
- **Implication:** Email's asynchronous nature and context-switching overhead are structural, not priority-dependent. Consider email-to-chat escalation workflows.

### Pattern 3: Performance & Data Issues Are Intrinsically Slow
- Performance theme issues average 128 min; data management 93 min.
- No amount of priority escalation halves this (Critical + Performance in phone: 66 min; still 3× slower than feature requests).
- **Implication:** These require engineering investigation; staffing/skills and complexity, not channel routing, are the constraint.

### Pattern 4: Low Priority via Email Is a Data Quality Anomaly
- 25 Low-priority email tickets average 72 min—as long as High-priority phone (79 min).
- Likely cause: Billing & account issues tagged Low priority but requiring investigation.
- **Implication:** Priority tagging may be inconsistent; recalibrate Low priority definition or audit misclassifications.

---

## Summary: Resolution Time Drivers & Effect Sizes

| Driver              | Range (Mean)      | Effect Size       | Remarks |
|---------------------|-----------------|------------------|---------|
| **Channel**         | 22.5–98.3 min   | 4.4× (chat vs email) | Dominant; structural |
| **Issue Theme**     | 26.4–128 min    | 4.8× (feature vs performance) | Reflects problem complexity |
| **Priority**        | 37.5–131.1 min  | 3.5× (Low vs High) | Confounded by channel; non-monotonic |
| **Urgency (TAPP)**  | 35.7–106 min    | 3.0× (enhancement vs time-sensitive) | Orthogonal to priority; captured by issue_type |
| **Issue Type (TAPP)** | 30.2–138.1 min | 4.6× (feature vs bug_performance) | Adds specificity within bugs |

---

## Method Note

**TAPP-Generated Columns Used in Analysis:**
- `urgency_and_blocker_status`: 7-category semantic classifier capturing business impact (customer_blocked, revenue_risk, time_sensitive, user_friction, enhancement_only, high_impact_outage, not_present). Coverage: 249/250.
- `issue_type`: 10-category taxonomy of root-cause/service category (bug_functionality, bug_performance, feature_request, documentation_gap, infrastructure_outage, bug_data_integrity, api_auth_error, billing_error, deployment_issue, configuration_rollback). Coverage: 250/250.

**Analytical Approach:** Stratified summary statistics (mean, median, SD, range) for each driver; two-way and three-way crosstabulations to identify interactions; subset analysis of extreme cases (resolution ≥120 min, ≤30 min); redundancy checks via cross-tabulation between TAPP columns and original structured fields.

**TAPP Value Conclusion:** `urgency_and_blocker_status` provides semantic enrichment but is substantially captured by `issue_type` + severity assessment (moderate utility for SLA segmentation). `issue_type` adds discriminatory power within broad themes, especially bug subcategories, and should be retained for targeting resolution strategies (high utility for staffing/routing).
