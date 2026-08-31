---
dataset: flag_9
scenario: causal_hardware
variant: original
model: substrate-claude-haiku-4-5
query_subtype: causal_attribution
focus_variable: "hardware_incident_spike"
query: "Why did hardware incidents spike in the anomaly window?"
source_table: augment_table/flag_9/causal_hardware/original.csv
source_report: dataset_portion_1/substrate-claude-haiku-4-5/flag_9__causal_hardware/analyses/original/analysis.md
wall_seconds: 106.08
---

# Hardware incident spike in the anomaly window

## Summary

The spike appears to be a **real surge in hardware tickets**, concentrated in a short window, not a broad rise in all incident types.

- A clear anomaly runs from **2023-07-19 to 2023-08-17**.
- In that 30-day window there were **90 hardware incidents** out of **144 total incidents**.
- Outside that window, hardware incidents were **50 before** and **42 after**, with the **same baseline rate** on both sides: about **0.25 hardware incidents/day** and **20.2% of all incidents**.
- During the window, hardware jumped to **3.0/day** and **62.5% of all incidents**.

## What drove the spike

### 1. The surge was mostly hardware-specific
Monthly hardware volume jumped from typical levels of **4-12 per month** to:

- **44 in 2023-07**
- **52 in 2023-08**

Hardware also became the majority of all incidents:

- **55.0%** of incidents in July
- **53.6%** in August

Other categories did not show a similar jump in the same window:

- Window totals: **Hardware 90**, **Inquiry/Help 19**, **Software 14**, **Network 11**, **Database 10**

This points to a **category-specific disruption**, not a general ticketing surge.

### 2. Printer and peripheral failures explain most of the increase
Within the anomaly window, hardware incidents were dominated by end-user device issues:

- **Printer:** **40**
- **Display/Monitor:** **16**
- **Keyboard:** **12**
- **Endpoint generic:** **6**
- **Storage:** **4**
- **Server hardware:** **4**
- **Mouse:** **3**

So the spike was driven mainly by **printer and workstation peripheral problems**, not by server-class failures.

Repeated descriptions reinforce this:

- `Printer not working properly` — **8**
- `Printer is not functioning properly` — **3**
- `Printer not functioning properly` — **3**
- `Printer not responding` — **2**
- `Printer malfunctioning frequently` — **2**
- `Monitor screen flickering` — **2**
- `Monitor display issue` — **2**

This looks like a **wave of similar endpoint hardware faults**, especially printers.

### 3. The pattern is distributed, not tied to one reporter or one technician
The window is not dominated by a single caller or assignee.

**Caller mix in window:**

- Don Goodliffe — **31**
- Bud Richman — **21**
- David Loo — **19**
- ITIL User — **19**

**Assigned_to mix in window:**

- Fred Luddy — **23**
- Beth Anglin — **19**
- Luke Wilson — **19**
- Charlie Whitherspoon — **15**
- Howard Johnson — **14**

This spread suggests the spike was **broadly experienced and broadly handled**, not just one person repeatedly opening tickets.

## What does *not* explain the spike well

### 1. Not an assignment-group reclassification
All hardware incidents, both inside and outside the window, are in:

- `assignment_group = Hardware`

So the spike does not look like a routing change visible in this dataset.

### 2. Not a severity-policy shift
Priority mix in the window is:

- **2 - High:** **68**
- **3 - Moderate:** **13**
- **1 - Critical:** **9**

Outside the window, hardware is also mostly high priority:

- **2 - High:** **77**
- **3 - Moderate:** **8**
- **1 - Critical:** **7**

So the spike was **more volume**, not just more aggressive priority labeling.

### 3. Not obviously a closure/backlog artifact
Operational handling looks stable:

- Window states: **Resolved 48**, **Closed 42**
- Outside: **Closed 47**, **Resolved 45**

Resolution time is also similar:

- Window mean: **7.04 days**
- Outside mean: **7.43 days**

That weakens the idea that the spike came from delayed processing or mass cleanup.

## Decision-ready conclusion

The anomaly window spike happened because the dataset shows a **short, concentrated burst of hardware incidents dominated by printer, monitor, and keyboard problems**, with **printer-related tickets as the largest driver**. The increase was **specific to hardware**, **spread across multiple callers and technicians**, and **not accompanied by visible changes in priority, assignment routing, or closure behavior**.

## Limits / weak evidence

The dataset does **not** include asset IDs, locations, change records, vendor data, or root-cause fields. Because of that, it cannot prove whether the underlying trigger was, for example, a bad hardware batch, office move, maintenance event, or driver rollout. The strongest supported claim is only that the spike was caused by a **real wave of end-user hardware/peripheral failures, especially printer issues**.
