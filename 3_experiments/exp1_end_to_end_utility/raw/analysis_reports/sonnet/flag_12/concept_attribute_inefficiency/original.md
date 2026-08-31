---
dataset: flag_12
scenario: concept_attribute_inefficiency
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: faceted_decomposition
focus_variable: "incident_inefficiency_reasons"
query: "What recurring issues drive resolution inefficiency?"
source_table: augment_table/flag_12/concept_attribute_inefficiency/original.csv
source_report: dataset_portion_1/substrate-claude-sonnet-4-6/flag_12__concept_attribute_inefficiency/analyses/original/analysis.md
wall_seconds: 81.31
---

# Resolution inefficiency drivers

The visible focus variable is time to resolution, inferred from `opened_at` to `closed_at`. Across 500 incidents, mean resolution time is **178.4 hours** and median is **173.2 hours**; the 75th percentile is **252.7 hours**, so the slow tail is material.

## Recurring drivers

- **Routine hardware incidents dominate the backlog and resolve slowly.**
  - `category = Hardware` accounts for **406/500** incidents.
  - `assignment_group = Hardware` accounts for **405/500** incidents.
  - Hardware also resolves slightly slower than the full set: **181.4 hours** mean vs **178.4** overall.
  - This points to inefficiency being driven more by **high-volume end-user device work** than by rare specialist categories.

- **Printer issues are the clearest recurring source of delay.**
  - The most frequent `short_description` values are heavily printer-related:
    - `Printer not working properly`: **30** incidents, **211.6 hours** mean
    - `Printer not functioning properly`: **26** incidents, **179.2 hours** mean
    - `Printer is not working properly`: **14** incidents, **174.3 hours** mean
    - `Printer not responding`: **11** incidents, **185.7 hours** mean
  - These are near-duplicate concepts with different wording, and they repeatedly take about **7–9 days** on average. The pattern suggests fragmented handling of a common issue type rather than isolated hard cases.

- **Other peripheral device issues also recur with long resolution times.**
  - `Keyboard not responding`: **6** incidents, **202.7 hours** mean
  - `Keyboard malfunctioning`: **5** incidents, **201.2 hours** mean
  - `Keyboard not functioning properly`: **5** incidents, **256.8 hours** mean
  - Repeated keyboard/device failures appear to be another inefficient queue inside the same hardware-heavy workflow.

- **Resolver-level variation may be contributing.**
  - By `assigned_to`, average resolution time differs noticeably:
    - `Luke Wilson`: **116** incidents, **195.5 hours** mean
    - `Charlie Whitherspoon`: **103**, **178.8 hours**
    - `Howard Johnson`: **106**, **175.5 hours**
    - `Beth Anglin`: **85**, **172.4 hours**
    - `Fred Luddy`: **90**, **165.0 hours**
  - This is consistent with either workload imbalance or different issue mixes. The table supports variation, but not the cause.

## Secondary patterns

- **Help / installation requests are inconsistent rather than uniformly slow.**
  - `category = Inquiry / Help`: **20** incidents, **182.1 hours** mean.
  - Example split:
    - `Need assistance with software installation`: **7** incidents, **247.6 hours** mean
    - `Need help with software installation`: **4** incidents, **45.8 hours** mean
  - The same general need appears under different descriptions with very different outcomes. This may reflect inconsistent triage or labeling, but evidence is weaker than for printer/peripheral issues.

- **Priority does not show a strong efficiency gradient.**
  - `2 - High`: **394** incidents, **180.0 hours** mean
  - `1 - Critical`: **27** incidents, **167.0 hours** mean
  - Critical tickets are somewhat faster, but not dramatically so. The larger issue appears to be the **large high-priority hardware volume**, not just severity labeling.

## Exceptions and weak evidence

- Not every repeated hardware issue is slow:
  - `Monitor display issue`: **12** incidents, **165.2 hours**
  - `Monitor screen is flickering`: **8** incidents, **147.1 hours**
  - So the inefficiency is not all hardware equally; it is strongest in **printer** and some **keyboard/peripheral** concepts.

- `Software` (**153.6 hours**) and `Network` (**161.6 hours**) resolve faster on average than Hardware, so the main drag is not broad technical complexity across all categories.

- `state = Resolved` tickets average **184.3 hours** vs **172.7** for `Closed`, but this is better treated as a workflow signal than a proven cause.

## Bottom line

The main recurring issues behind resolution inefficiency are **high-volume hardware tickets**, especially **printer problems** and, secondarily, **keyboard/peripheral failures**. The data also suggests **description fragmentation** for the same underlying concepts and **resolver-level variation** in turnaround. Evidence for software/help inefficiency exists, but it is mixed and less consistent.
