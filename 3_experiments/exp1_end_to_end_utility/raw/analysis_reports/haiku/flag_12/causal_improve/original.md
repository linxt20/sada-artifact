---
dataset: flag_12
scenario: causal_improve
variant: original
model: substrate-claude-haiku-4-5
query_subtype: what_if
focus_variable: "incident_resolution_efficiency"
query: "How can we improve incident resolution efficiency?"
source_table: augment_table/flag_12/causal_improve/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_12__causal_improve/analyses/original/analysis.md
wall_seconds: 136.75
---

# Incident resolution efficiency

**Focus variable:** resolution time, measured as $closed\_at - opened\_at$ for 500 incidents.

## What the data shows
- **The main bottleneck is the Hardware queue.** `category=Hardware` appears in **406/500** incidents and `assignment_group=Hardware` in **405/500**. Hardware averages **7.56 days**, slower than Software (**6.40**) and Network (**6.74**). Also, **336** incidents are both `assignment_group=Hardware` and `priority=2 - High`, so small Hardware gains should move the overall average most.
- **A few hardware issue types dominate volume.** Grouping repeated `short_description` text shows about **202 printer** incidents averaging **7.65 days** and **56 keyboard** incidents averaging **7.79 days**. Those two issue families alone account for **258/500** incidents.
- **Assignee performance varies inside the same queue.** Within `assignment_group=Hardware`, mean resolution ranges from **6.87 days** for `assigned_to=Fred Luddy` (80 cases) to **8.31 days** for `Luke Wilson` (96 cases). The same gap remains in high-priority hardware: **7.11** vs **8.13** days. This points to workflow or load-balance differences worth standardizing.
- **The long tail is material.** Median resolution is **7.22 days**, but the 90th percentile is **13.35** and the 95th percentile is **15.64**. **43/500** incidents take **14+ days**, including **36** in Hardware. Incidents opened on **Friday** average **8.15 days** overall versus **6.83 days** on Monday; in Hardware, Friday rises to **8.53** days.
- **Priority labels are not separating work well.** `priority=2 - High` averages **7.50 days**, nearly the same as `3 - Moderate` at **7.41**. Only `1 - Critical` is somewhat faster at **6.96** days, and that group is small (**27** cases).

## Recommended actions
1. **Improve the Hardware path first.** Standardize triage and resolution runbooks for printer and keyboard tickets, keep common replacement parts/devices ready, and shift routine fixes to remote or self-service steps where possible.
2. **Reduce assignee variation in Hardware.** Compare the handling patterns of faster owners to slower owners, then apply the same playbooks, routing rules, or workload balancing—especially for high-priority hardware tickets.
3. **Control the aging tail.** Add an age-based escalation around **10-12 days** and a Friday handoff/coverage check. The data shows both a weekend-adjacent slowdown and a meaningful 14+ day tail.
4. **Tighten priority usage.** Reserve `2 - High` for incidents that truly need faster treatment, or create a narrower fast lane inside Hardware. The current label is too broad to produce visibly faster resolution.

## Exceptions and limits
- **Routing already looks mostly clean.** Hardware almost always routes to Hardware, Software to Software, Network to Network, and **19/20** `Inquiry / Help` tickets route to `Service Desk`. Misrouting is visible but appears rare, so routing cleanup alone is unlikely to be the main lever.
- **Some subgroup patterns are weak evidence.** Service Desk, Database, and Network have small counts, so owner-level differences there are less reliable.
- **This is observational.** The table supports prioritization, not causal proof; unobserved case complexity may explain part of the assignee gap.

## Bottom line
The clearest way to improve incident resolution efficiency is to **target the high-volume Hardware queue**, especially **printer and keyboard incidents**, **standardize the better owner workflows**, and **escalate aging Friday cases earlier**. Those are the strongest levers visible in the current data.
