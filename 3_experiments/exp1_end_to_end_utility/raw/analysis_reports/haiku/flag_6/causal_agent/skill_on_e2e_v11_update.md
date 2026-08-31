---
dataset: flag_6
scenario: causal_agent
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "agent_resolution_discrepancy"
query: "Why do some agents have longer resolution times?"
source_table: augment_table/flag_6/causal_agent/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:20:34.499805+00:00
wall_seconds: 128.39
---

# Resolution Time Variability Across Agents: Causal Analysis

## Executive Summary

Resolution times vary dramatically across agents in this incident dataset, driven primarily by agent workload patterns combined with incident complexity and problem scope. Fred Luddy's incidents take approximately **626 hours (5.05x) longer** than other agents to resolve (750 hrs vs. 124 hrs mean), with complexity and problem scope being key accelerating factors. This analysis combines original structured columns with TAPP-generated semantic facets to identify root causes.

## Key Findings

### 1. Stark Agent-Level Performance Gap
- **Fred Luddy**: Mean 750 hrs, Median 691 hrs (n=76 incidents)
- **Others (Beth, Luke, Charlie, Howard)**: Mean 124 hrs, Median 123 hrs (n=402 incidents)
- **Magnitude**: Fred Luddy's incidents resolve ~505% longer than peers

### 2. Incident Complexity (TAPP-generated `incident_complexity_signal`) Interacts Strongly with Agent

For **complex incidents** (complexity signal = True):
- **Fred Luddy**: 1,259 hrs (n=24) — severe impact
- **Luke Wilson**: 184 hrs (n=10) — moderate impact
- **Charlie Whitherspoon**: 125 hrs (n=10) — minimal impact
- **Howard Johnson**: 94 hrs (n=12) — inverse relationship

For **non-complex incidents** (complexity signal = False):
- **Fred Luddy**: 515 hrs (n=52) — still 4.6x higher than Beth Anglin (111 hrs, n=90)

**Interpretation**: Complexity compounds Fred Luddy's delays; he shows a 2.45x multiplier effect, whereas other agents show minimal or inverse complexity impact.

### 3. Problem Scope (TAPP-generated `problem_scope`) Drives Variability

**Fred Luddy's problem scope impact**:
- Infrastructure-wide: 769 hrs (n=62, 81.6% of workload)
- Facility-wide: 939 hrs (n=3, significant outlier)
- Individual device: 815 hrs (n=7)
- Department: 194 hrs (n=4, fastest)

**Beth Anglin (control) by problem scope**:
- Infrastructure-wide: 102 hrs (n=72, 73.5% of workload)
- Individual device: 151 hrs (n=17)
- Department: 136 hrs (n=2)
- Facility-wide: 72 hrs (n=7, fastest)

**Interpretation**: Scope drives resolution time differentially by agent. Infrastructure incidents take ~7.5x longer under Fred Luddy vs. Beth Anglin, suggesting handling efficiency or routing delays.

### 4. Workload and Priority Distribution (Original Structured Columns)

**Incident counts (similar across agents)**:
- Luke Wilson: 103 incidents
- Charlie Whitherspoon: 103 incidents
- Beth Anglin: 98 incidents
- Howard Johnson: 98 incidents
- Fred Luddy: 76 incidents (fewer, but still significant delay effect)

**Priority distribution (nearly identical)**:
- All agents handle ~17–18% Critical, ~76–78% High, ~5–6% Moderate
- Average priority score: Fred Luddy (1.88) vs. Luke Wilson (1.89) — no material difference

**Interpretation**: Incident volume and priority mix do not explain the gap. The issue is *per-incident resolution efficiency*, not queue depth.

### 5. Incident Category Distribution (TAPP-generated `incident_category`)

**Breakdown** (primary categories):
- **Connectivity**: ~40% for all agents
- **Database**: ~21–22% for all agents
- **Email**: ~16–17% for all agents

**Category-specific performance** (selected sample):
- Database incidents: Fred Luddy resolves ~6–8x slower than peers
- Connectivity incidents: Fred Luddy resolves ~5–7x slower than peers

**Interpretation**: Slow resolution is consistent across incident types; not limited to a single category.

### 6. Agent Closure Alignment (TAPP-generated `agent_closure_alignment`) as Moderating Factor

**Fred Luddy**:
- Aligned closures (n=52): 558 hrs
- Misaligned closures (n=24): 1,166 hrs (2.1x worse)

**Beth Anglin** (control):
- Aligned closures (n=57): 122 hrs
- Misaligned closures (n=41): 92 hrs (0.75x — inverse!)

**Interpretation**: For Fred Luddy, closure misalignment dramatically worsens outcomes. This suggests incidents may be escalated or reopened, adding delay. For other agents, misalignment has minimal or no adverse effect. This is a critical behavioral difference.

## Method Note: TAPP-Generated Columns Used

The following augmented columns from the TAPP v11 orchestration are referenced in this analysis:

1. **`incident_complexity_signal`** (boolean): Binary flag indicating computational or business complexity
   - Used to stratify and assess resolution time multipliers by agent
   - Shows strong interaction with Fred Luddy's resolution performance

2. **`problem_scope`** (categorical): Scope classification—individual_device, infrastructure, department, facility_wide
   - Reveals infrastructure-wide incidents consume disproportionate time under Fred Luddy
   - Minimal variance in other agents

3. **`incident_category`** (categorical): Semantic categorization—database, connectivity, email, application, security, infrastructure
   - Confirms slowdown is not type-specific
   - Provides context for why infrastructure-wide incidents trend high for Fred Luddy

4. **`agent_closure_alignment`** (boolean): Whether incident closure status aligns with expected workflow state
   - Strong moderating/amplifying effect for Fred Luddy but not others
   - Suggests process deviation or re-escalation pattern

5. **`assigned_agent`** (categorical): Direct assignment mapping (original column repurposed for this facet)
   - Primary grouping variable for all stratified analyses

All TAPP-generated columns are retained in original structured table form; no synthetic derivations were created.

## Root Causes and Hypotheses

### Primary Driver: Complexity and Scope Handling
Fred Luddy's disproportionate resolution times are driven by:
1. **Incidents with complexity signal = True resolve 2.45x slower** (1,259 hrs vs. 515 hrs for simple incidents)
2. **Infrastructure-wide incidents** (most common in his backlog, 81.6%) take 769 hrs on average
3. **Facility-wide incidents** spike to 939 hrs (sample size small but consistently extreme)

### Secondary Driver: Closure Misalignment and Escalation Pattern
Fred Luddy shows elevated resolution time (2.1x) for incidents with misaligned closure status, suggesting:
- Possible re-escalation or reopening of incidents
- Workflow deviations that extend time-to-final resolution
- Other agents do not exhibit this pattern, indicating agent-specific process deviation

### Workload and Priority: Not Primary Drivers
- Incident counts are balanced (76–103 per agent)
- Priority mix is nearly identical across agents (~1.87–1.91 average score)
- Incident categories are similarly distributed
- **Conclusion**: The issue is resolution *efficiency per incident*, not queue management or triage

## Conclusions

1. **Fred Luddy's longer resolution times (750 hrs vs. 124 hrs for others) are driven by a combination of:**
   - Assignment to complex, infrastructure-wide incidents (structural or skill-based mismatch)
   - Incident complexity amplifying his resolution time by 2.45x (vs. minimal effect for peers)
   - Closure workflow misalignment, suggesting possible re-escalation or process deviation

2. **Incident characteristics (complexity, scope) explain significant variance** but are not evenly distributed:
   - Complex incidents: Fred Luddy (1,259 hrs) vs. Luke Wilson (184 hrs)
   - Infrastructure-wide: Fred Luddy (769 hrs) vs. Beth Anglin (102 hrs)

3. **Process and workflow factors matter as much as incident type:**
   - Closure misalignment has 2.1x impact on Fred Luddy but minimal impact on peers
   - Suggests agent-specific bottlenecks, escalation patterns, or handoff delays

4. **Recommendations for intervention:**
   - Review Fred Luddy's handling of complex and infrastructure-wide incidents for skill gaps or process bottlenecks
   - Investigate closure workflow and escalation patterns to reduce misalignment penalty (2.1x multiplier)
   - Consider rebalancing incident assignment or providing targeted training for complex incident resolution
   - Benchmark best practices from Beth Anglin, Luke Wilson, and Charlie Whitherspoon for transfer
