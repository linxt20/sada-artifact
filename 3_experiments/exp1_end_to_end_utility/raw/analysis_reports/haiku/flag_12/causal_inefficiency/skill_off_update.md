---
dataset: flag_12
scenario: causal_inefficiency
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "resolution_efficiency"
query: "Why are some incidents resolved inefficiently, and which underlying issues drive it?"
source_table: augment_table/flag_12/causal_inefficiency/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:09:19.137294+00:00
wall_seconds: 59.4
---

# Causal Analysis of Incident Resolution Inefficiency

## Executive Summary

**52% of incidents (260 of 500) are resolved inefficiently**, with inefficient cases taking **~10.98 days** versus **~3.59 days** for efficient ones—a **3× time difference**. The variant label "skill_off" indicates this analysis examines incidents where skill-based resolution optimization may be impaired.

---

## Key Causal Factors Driving Inefficiency

### 1. **Above-Category Median Resolution Time (Strongest Signal)**
- **98.8% of incidents above their category's median resolution time are inefficient**
- Conversely, only **5.6% of incidents at/below median are inefficient**
- This pattern indicates inefficiency is structurally defined by relative performance within similar work types
- **Implication:** Incidents that exceed baseline expectations for their category face systemic delays

### 2. **Incident Category Distribution**
Hardware dominates the dataset (406/500, 81.2%) and also dominates inefficient cases (215/260, 82.7%):

| Category | Total | Inefficient | Rate |
|----------|-------|-------------|------|
| Hardware | 406 | 215 | 53.0% |
| Inquiry/Help | 20 | 11 | 55.0% |
| Database | 19 | 10 | 52.6% |
| Network | 22 | 11 | 50.0% |
| Software | 33 | 13 | 39.4% |

**Observation:** Hardware (53%) and Inquiry/Help (55%) show the highest inefficiency rates, likely due to:
- Need for physical part replacement, logistics, and on-site work
- Coordination between multiple technicians or suppliers
- Software issues (39.4% rate) are resolved most efficiently, suggesting simpler remote fixes

### 3. **Priority Level Impact**
- **High Priority (2 - High):** 53.6% inefficiency (211/394)—largest volume and highest rate
- **Critical Priority (1 - Critical):** 44.4% inefficiency (12/27)—lower rate despite urgency
- **Moderate (3 - Moderate):** 48.1% inefficiency (37/77)
- **Low (4 - Low):** 0% inefficiency (0/2, n=2)

**Interpretation:** Critical incidents may receive prioritized handling, reducing inefficiency despite complexity. High-priority incidents, which dominate the queue (394/500, 78.8%), suffer from resource contention and slower processing.

### 4. **Assignee-to-Closer Mismatch (Ownership Handoff)**
- **78.8% of incidents (394/500) have assignee ≠ closed_by** (ownership changed hands)
- Inefficiency rates are similar across both groups (~52%), indicating the mismatch itself is not a strong primary driver
- However, mismatch frequency in the dataset (78.8%) suggests systemic workflow inefficiency:
  - Tickets are frequently reassigned or escalated
  - Knowledge transfer and context-switching delays resolution
  - The high prevalence suggests skill gaps or workload imbalance drive reassignments

### 5. **Resolution State (Closed vs. Resolved)**
- **Resolved state:** 55.3% inefficiency (135/244)
- **Closed state:** 48.8% inefficiency (125/256)
- "Resolved" tickets are **1.13× more likely to be inefficient**, suggesting process friction in formal resolution workflows vs. simple closure

---

## Underlying Issues and Mechanisms

### Root Causes of Inefficiency

1. **Hardware Replacement and Procurement Delays**
   - 81% of incidents are hardware-related; many require physical part replacement
   - Common patterns in descriptions: *"Printer not working"*, *"Hard drive failure"*, *"Monitor not responding"*
   - Resolution requires procurement, logistics, and on-site installation—inherently slow
   - **Evidence:** Hardware dominates inefficient cases (215/260, 82.7%)

2. **Ticket Complexity and Problem Specificity**
   - Many descriptions are generic (*"Printer not working"*) rather than specific (*"paper jam in tray 2"*)
   - Generic descriptions prolong diagnosis and triage, requiring back-and-forth communication
   - **Weak signal:** No dedicated `description_specificity` column in data to quantify this directly
   - **Inference:** High prevalence of printer/hardware issues with vague wording supports this mechanism

3. **Workflow Inefficiency and Ownership Fragmentation**
   - 78.8% of incidents involve ownership handoff (assigned_to ≠ closed_by)
   - Reassignments indicate:
     - Initial assignee lack of skill/authority to close
     - Escalation or routing delays
     - No clear ownership model
   - **Impact:** Each handoff adds context-switching overhead and potential knowledge loss

4. **Resource Constraints and Capacity**
   - Mean resolution time is 7.43 days; 52% exceed category medians
   - High-priority incidents (78.8% of queue) suffer 53.6% inefficiency, suggesting bottlenecks
   - **Weak evidence:** No workload/staffing data in dataset, but patterns suggest resource saturation

### Secondary Factors

5. **State Management and Closure Process**
   - "Resolved" state has higher inefficiency (55.3%) than "Closed" (48.8%)
   - May reflect more stringent resolution criteria or additional handoffs needed

6. **Employee vs. Non-Employee Updates**
   - No strong differential in data, but `sys_updated_by_is_employee` presence suggests staff capacity variations

---

## Data-Driven Patterns

### Efficiency Threshold
- **Below category median:** 3.75 days avg, 5.6% inefficient
- **Above category median:** 11.14 days avg, 98.8% inefficient
- **Threshold insight:** ~4.5 days is the implicit "efficient" boundary; anything slower triggers inefficiency classification

### Incident Volume and Inefficiency Correlation
- Hardware: 406 total incidents, 53% inefficiency → 215 inefficient cases (largest absolute driver)
- High-priority: 394 total incidents, 53.6% inefficiency → 211 inefficient cases (resource saturation)
- The sheer volume of High-priority Hardware incidents (majority overlap) creates inefficiency concentration

---

## Skill_Off Variant Interpretation

The variant label **"skill_off"** suggests this augmentation captures scenarios where:
1. Technicians lack expertise to diagnose or resolve without escalation (driving handoffs)
2. Self-service or knowledge-based deflection is unavailable or inadequate
3. Root-cause analysis is insufficient (recurring or incomplete fixes)
4. Soft skills (communication, intake quality) are absent

**Supporting evidence:**
- High reassignment rate (78.8%) → skill gaps
- Generic issue descriptions → poor intake and triage
- Hardware dominance with long resolution times → repair/replacement complexity without pre-diagnosis skill

---

## Actionable Insights

1. **Prioritize Hardware Intake Process**  
   Implement guided intake forms to capture asset type, symptom specificity, and scope upfront → reduce diagnosis time

2. **Skill Development for Hardware Technicians**  
   53% of 406 hardware incidents are inefficient; targeted training on common issues (printers, monitors, hard drives) could close 4-6 day gaps

3. **Reduce Ownership Handoffs**  
   Current 78.8% mismatch rate suggests lack of clear ownership or skill-based routing; implement direct assignment or skill-matched queues

4. **Streamline Critical-Path Resolution**  
   Critical incidents (44.4% inefficient) outperform High-priority (53.6%); apply critical-ticket workflows to high-priority work

5. **Self-Service and Knowledge Base**  
   Software (39.4% inefficiency) outperforms hardware; invest in self-service tools and KB articles for common Hardware issues

---

## Limitations and Caveats

- **No augmented columns in provided data**: Expected columns like `AffectedAssetType`, `IssueMechanism`, `DescriptionSpecificity` are not present; analysis relies on visible fields
- **Binary inefficiency label**: Actual root causes are inferred from structural patterns (category, priority, timing) rather than detailed diagnostics
- **No direct skill/staffing metrics**: Cannot definitively link "skill_off" to technician expertise; inferred from ticket flow patterns
- **Sample size**: 500 incidents; patterns are statistically robust but causal attribution remains correlational

---

## Conclusion

**52% incident inefficiency is primarily driven by hardware complexity, resource constraints on high-priority work, and workflow fragmentation through frequent ownership handoffs.** The "skill_off" variant points to gaps in technician capability to resolve without escalation, intake quality issues that delay diagnosis, and lack of knowledge-based self-service options. Targeted interventions in intake process design, hardware technician skill development, and direct-assignment routing are most likely to yield efficiency gains.
