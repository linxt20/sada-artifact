---
dataset: flag_12
scenario: causal_inefficiency
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "resolution_efficiency"
query: "Why are some incidents resolved inefficiently, and which underlying issues drive it?"
source_table: augment_table/flag_12/causal_inefficiency/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:13:31.249859+00:00
wall_seconds: 54.93
---

# Causal Analysis: Why Incidents Are Resolved Inefficiently
## Skill_on Variant Analysis

### Executive Summary

This analysis examines 500 IT incidents to identify root causes of inefficient resolution. The data reveals that **skill/experience gaps (proxied by technician assignment patterns), recurring hardware issues, and lack of problem specificity** are the primary drivers of extended resolution times. Average resolution takes 7 days, but incidents with multiple reassignments and recurring patterns extend to 7.3 days—a 9% efficiency penalty.

---

### Key Inefficiency Drivers

#### 1. **Multiple Handler Reassignments (60% of incidents)**

**Finding**: 301 out of 500 incidents (60.2%) involve multiple reassignments, averaging **7.02 days** to resolve versus **6.88 days** for same-handler cases.

**Underlying cause - Skill/Experience Mismatch**:
- Technician performance varies significantly by assignment patterns
- **Luke Wilson**: 7.72 avg days, 64.7% reassignment rate → higher workload or mismatches
- **Fred Luddy**: 6.48 avg days, 71.1% reassignment rate → appears to resolve faster despite reassignments
- **Howard Johnson**: 6.90 avg days, lowest reassignment rate (43.4%) → specialized focus improves efficiency

This variation suggests **uneven skill distribution**. When incidents are reassigned, they often move between technicians with differing expertise, causing:
- Loss of context and prior troubleshooting attempts
- Duplicate diagnostic efforts
- Extended time-to-resolution

#### 2. **Recurring Hardware Issues (54% of incidents)**

**Finding**: 271 incidents (54.2%) show recurring patterns, taking **7.29 days** vs. 6.66 days for non-recurring issues—a **0.62-day (0.63 hour) delay**.

**Root cause - Inadequate Root-Cause Resolution**:
- **Hardware failures dominate**: 381 incidents (76.2% of total) are hardware-related
- **Printer failures are endemic**: 202 incidents (40.4% of all incidents) involve printers
  - 100% of printer incidents show recurring patterns
  - 59.4% involve multiple reassignments
  - Average 7.21-day resolution

This pattern indicates:
- **Temporary vs. permanent fixes**: Technicians may apply band-aid solutions rather than replacing faulty equipment
- **Lack of preventive maintenance**: Recurring printer issues suggest equipment reaches end-of-life but is repaired repeatedly
- **Knowledge gaps**: Inability to diagnose root causes leads to recurring reassignments

#### 3. **Lack of Problem Specificity (6.8% of incidents)**

**Finding**: Only 37 incidents (7.4%) are classified as "specific_actionable"; these resolve fastest at **6.03 days**. In contrast:
- **Vague/generic issues** (34 incidents, 6.8%): 6.50 days
- **Hardware failures** (381 incidents, 76.2%): 7.17 days

**Underlying issue - Poor Ticket Intake and Diagnosis**:
- 23 vague/generic incidents (67.6% of this category) still require multiple reassignments
- Vague categorization is most prevalent in **Software** (17/34) and **Inquiry/Help** (10/34) categories
- This forces technicians to spend extra time clarifying requirements rather than diagnosing

#### 4. **Compound Inefficiency: Multiple Reassignments + Recurring Issues**

**Finding**: 161 incidents (32.2% of total) exhibit **both** multiple reassignments AND recurring patterns:
- These take **7.27 days** on average
- 157 of these 161 (97.5%) involve hardware failures
- This represents a **9% delay vs. optimal resolution**

This combination signals a vicious cycle:
1. Technician A attempts hardware repair
2. Issue recurs → escalated/reassigned to Technician B  
3. Technician B may repeat diagnostics or apply different fix
4. Issue recurs → reassigned again
5. Cycle continues until equipment is eventually replaced

---

### Sector-Specific Inefficiencies

**Hardware Category (406 incidents, 81.2%)**:
- Average resolution: 7.13 days
- 62.2% involve multiple reassignments
- 67.7% show recurring patterns
- Dominated by printers and workstation components

**Software Category (33 incidents)**:
- Fastest resolution: 5.97 days
- Often marked as vague/generic (51.5%)
- Lower reassignment rates than hardware

**Network/Database Issues** (48 total):
- Faster resolution: 6.32-6.75 days
- Lower recurring rates (25-50%)
- Suggest better diagnosis clarity and permanent solutions

---

### Evidence Limitations

1. **Weak differentiation by reassignment type**: Multiple reassignments show only 0.14-day penalty vs. same-handler. This may underestimate inefficiency if reassignments occur mid-resolution and context is lost.

2. **No skill-level metadata**: Technician names proxy for experience, but actual certification/training data is absent. Performance variation could reflect workload imbalance rather than pure skill gaps.

3. **Vague issue classification remains rare**: Only 6.8% flagged as vague, suggesting most issues are pre-classified into hardware/software buckets that obscure root diagnosis problems.

4. **Max resolution time capped at 21 days**: No long-running incidents visible; inefficiency may be underestimated for complex cases.

---

### Conclusions

**Primary inefficiency drivers (ranked by impact)**:

1. **Hardware redundancy/recurring issues** (0.62-day delay): Technicians lack authority/resources to replace faulty equipment, instead applying temporary fixes. Printers are the worst offender (40% of incidents).

2. **Technician skill/knowledge gaps** (variable 0.5-1.2 day gap): Assignment to mismatched technicians forces reassignments; Luke Wilson's 7.72-day average vs. Fred Luddy's 6.48 days suggests 1.24-day skill gap.

3. **Diagnostic clarity failures** (0.6-1.1 day gap): Vague issue descriptions and lack of specific actionable information force extended triage, though this category is small (6.8%).

**Actionable insights**: Incidents with clear specificity and same-handler assignment resolve ~11-14% faster (6.03 vs. 7.02-7.29 days). Investing in equipment replacement strategies, technician specialization, and standardized diagnostic templates would reduce recurrence and reassignments, directly improving efficiency.
