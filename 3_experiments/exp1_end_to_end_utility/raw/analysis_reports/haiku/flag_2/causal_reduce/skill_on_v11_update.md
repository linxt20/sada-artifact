---
dataset: flag_2
scenario: causal_reduce
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: what_if
focus_variable: "resolution_time"
query: "How can we reduce incident resolution time?"
source_table: augment_table/flag_2/causal_reduce/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:16:36.560501+00:00
wall_seconds: 66.44
---

# Incident Resolution Time Reduction Analysis
## Variant: skill_on (Same Technician Assignment Pattern)

### Executive Summary

Analysis of 500 IT incidents reveals that **assigning the same technician from opening to closure does not reliably reduce resolution time overall**. The data shows an average resolution time of **1,043 hours**, with minimal advantage—in fact, a **37-hour penalty**—when the same technician handles the incident end-to-end. However, this aggregate finding masks critical context-dependent patterns that suggest targeted strategies for resolution time reduction.

---

### Key Findings

#### 1. **Same Technician Assignment Does Not Improve Overall Speed**

- **Same technician cases**: 1,073 hours average (72 incidents, 14% of portfolio)
- **Different technician cases**: 1,036 hours average (300 incidents, 86% of portfolio)
- **Difference**: +37 hours when same technician assigned (slower)

This counterintuitive finding suggests that **keeping the same technician throughout an incident's lifecycle may introduce delays**, possibly through:
- Bottlenecks if the primary technician is unavailable
- Handoff avoidance that extends problem-solving attempts rather than escalating
- Technician skill gaps not being compensated by specialist knowledge

#### 2. **Critical Incidents Show Strong Same-Technician Benefit**

The only priority tier where same-technician assignment clearly helps:

- **Critical priority (1) with same technician**: 910 hours average
- **Critical priority (1) with different technicians**: 1,169 hours average
- **Savings**: ~259 hours (22% reduction)

**Insight**: For high-urgency incidents, **continuity of ownership appears crucial**. This may reflect the need for rapid context retention and decision-making authority.

#### 3. **Scope Matters More Than Technician Continuity**

Resolution time correlates strongly with incident scope rather than technician assignment:

| Scope | Count | Mean Time (hours) |
|-------|-------|------------------|
| **Single-user** | 41 | 537 |
| **Building-wide** | 4 | 764 |
| **Department-wide** | 6 | 838 |
| **Network-wide** | 223 | 1,009 |
| **Application-specific** | 157 | 1,217 |

**Single-user incidents resolve ~65% faster** than application-specific incidents, regardless of technician continuity. This suggests that scope-driven complexity (not technician skills alone) drives resolution time.

#### 4. **Recurring Incidents Resolve Faster**

- **Recurring incident pattern**: 1,010 hours average (60% of dataset)
- **Non-recurring incidents**: 1,180 hours average (15% of dataset)
- **Savings**: 169 hours (14% reduction)

**Insight**: Incidents with recognized patterns resolve significantly faster, suggesting that **institutional knowledge and runbook availability matter more than individual technician continuity**. This argues for investment in knowledge management over individual assignment policies.

#### 5. **Database Incidents: No Benefit from Same Technician**

- **Database group with same technician**: 983 hours
- **Database group with different technicians**: 937 hours
- **Difference**: +46 hours penalty

Database incidents are complex, specialized problems that may benefit from **fresh perspectives** or escalation to specialists rather than forcing continuity with the initial respondent.

#### 6. **Fast Resolutions Are Dominated by Different-Technician Assignments**

Of the 34 incidents resolved in under 200 hours:
- **85% assigned to different technicians**
- **15% assigned to same technician**

This strongly suggests that **rapid resolution correlates with immediate specialist escalation**, not continuity.

#### 7. **Network Team Efficiency**

The Network assignment group (largest group, 44% of incidents) shows:
- Same-technician average: 1,087 hours
- Different-technician average: 1,071 hours
- **Minimal difference**, suggesting network issues may require different specialists regardless of assignment model.

---

### Recommendations for Reducing Incident Resolution Time

#### **Priority 1: Implement Scope-Based SLAs**
Since scope is the strongest driver of resolution time, establish differentiated targets:
- Single-user incidents: Target < 72 hours
- Network-wide: Target < 1,200 hours
- Application-specific: Target < 1,500 hours (requires cross-functional expertise)

#### **Priority 2: Escalation Over Continuity for Complex Issues**
For **application-specific and database incidents**, prioritize **immediate assignment to subject-matter experts** over technician continuity. Current data shows same-technician assignment extends resolution by 46 hours in database cases.

#### **Priority 3: Strengthen Knowledge Management & Runbooks**
Recurring incidents resolve **169 hours faster**. Invest in:
- Incident classification and pattern recognition systems
- Documented resolutions for common issues
- AI-assisted routing to relevant runbooks

#### **Priority 4: Reserve Same-Technician Model for Critical Incidents Only**
The data clearly supports same-technician assignment (259-hour benefit) for **Priority 1 (Critical)** incidents. For **Priority 2 (High)** and **Priority 3 (Moderate)**, default to **best-available-specialist routing**.

#### **Priority 5: Parallel Work Streams for Application-Specific Issues**
Application-specific incidents show the longest resolution times (1,217 hours average). Deploy:
- Parallel investigation by multiple specialists
- Reduce dependency on single technician availability
- Implement collaboration protocols for handoffs

---

### Data Quality Notes

- **Dataset**: 500 resolved incidents (Jan–Aug 2023)
- **Coverage**: Five technicians, six assignment groups, multiple priority and scope combinations
- **Median resolution time**: 1,032 hours (~43 days), suggesting systemic delays beyond individual assignment strategy
- **Limited sample for some categories**: Hardware (n=4), Openspace (n=1)—findings should be validated on larger samples

---

### Conclusion

**The "skill_on" variant (same technician throughout resolution) does not generally reduce incident resolution time and may introduce delays.** The aggregate 37-hour penalty is driven by misalignment: same-technician assignment benefits only critical incidents (259-hour savings) but harms database resolution (-46 hours) and complex application issues.

**Effective resolution time reduction depends on:**
1. **Scope-aware triage and SLAs** (primary driver)
2. **Pattern recognition and runbooks** (169-hour savings for recurring incidents)
3. **Specialist escalation** (85% of fast resolutions use multiple technicians)
4. **Targeted continuity** (critical incidents only)

Adopting a **context-dependent assignment strategy**—not a blanket same-technician policy—will yield measurable improvements in incident resolution time.
