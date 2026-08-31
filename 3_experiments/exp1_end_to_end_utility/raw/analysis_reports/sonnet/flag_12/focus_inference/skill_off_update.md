---
dataset: flag_12
scenario: focus_inference
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth analyzing in these incident tickets."
source_table: augment_table/flag_12/focus_inference/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:10:51.191772+00:00
wall_seconds: 58.77
---

# Incident Ticket Analysis Report

## Dataset Overview

- **500 tickets** spanning January–February 2023, covering IT hardware, software, network, database, and help desk incidents.
- Key columns of analytical interest: `category`, `device_type`, `priority`, `resolution_time_hours`, `description_vague`, `self_resolved`, `assigned_to`.

---

## 1. Volume and Category Distribution

| Category | Tickets | Share |
|---|---|---|
| Hardware | 406 | 81.2% |
| Software | 33 | 6.6% |
| Network | 22 | 4.4% |
| Inquiry / Help | 20 | 4.0% |
| Database | 19 | 3.8% |

Hardware dominates overwhelmingly. Within hardware, **printers alone account for 202 tickets (40% of all tickets)**, making them the single largest source of incidents. Monitors (71), keyboards (56), and servers (38) follow at a much lower volume.

---

## 2. Resolution Time Patterns

- **Mean resolution time: ~178 hours** (~7.4 days), with high variance (std ≈ 109 hrs).
- The minimum of exactly **24.0 hours** appears repeatedly — likely a system default or SLA-floor artifact, not genuine same-day resolution. This warrants data-quality scrutiny.

**By category** (fastest → slowest):

| Category | Avg Hours |
|---|---|
| Software | 153.6 |
| Network | 161.6 |
| Database | 172.4 |
| Hardware | 181.4 |
| Inquiry / Help | 182.1 |

Software and Network resolve ~20 hours faster than Hardware on average, likely reflecting clearer problem definitions and fewer physical logistics.

**By device type**, desktops (197.9 hrs) and keyboards (187.0 hrs) are the slowest; "other" (157.5) and network devices (159.6) resolve fastest.

**By priority**, the pattern is counterintuitive: Critical tickets (avg 167 hrs) resolve faster than High (180 hrs) or Moderate (178 hrs) — consistent with prioritized routing. However, the sample of Critical tickets is small (n=27), so this finding is suggestive rather than definitive.

---

## 3. Description Vagueness (`description_vague`)

- **35.2% of tickets** (176/500) have vague descriptions.
- Vague tickets take on average **~16 hours longer** to resolve (188.8 hrs vs. 172.7 hrs).
- **Printer tickets are especially vague**: 64.4% of printer tickets are flagged as vague, far above the dataset average — likely because reporters describe symptoms generically ("not working properly") rather than root causes.
- Vagueness does **not** meaningfully predict self-resolution: both vague and non-vague groups self-resolve at ~21% rate, suggesting vagueness affects agent effort but not user self-sufficiency.

---

## 4. Self-Resolution (`self_resolved`)

- **21.2% of tickets** (106/500) are self-resolved.
- Self-resolution is more common in **Network (31.8%)** and **Database (26.3%)** categories, and rarer in **Inquiry/Help (15%)** and **Hardware (20.4%)**.
- By device type, **database** (40%) and **network** (33%) issues self-resolve most often — plausibly because connectivity or service disruptions can clear spontaneously.
- **Server issues self-resolve least** (13.2%), consistent with physical hardware failures requiring hands-on intervention.
- Self-resolved tickets show only marginally shorter resolution times (174.8 vs. 179.4 hrs), suggesting most self-resolutions are still logged late or left open until closure sweep.

---

## 5. Agent Performance

| Agent | Avg Resolution (hrs) |
|---|---|
| Fred Luddy | 165.0 |
| Beth Anglin | 172.4 |
| Howard Johnson | 175.5 |
| Charlie Whitherspoon | 178.8 |
| Luke Wilson | 195.5 |

Luke Wilson's average is ~30 hours higher than Fred Luddy's. This gap may reflect caseload mix (device/category assignment) rather than individual performance — further controlling for ticket type would be needed before drawing conclusions.

---

## 6. Key Takeaways for Decision-Making

| Signal | Strength | Action Implication |
|---|---|---|
| Printer volume dominance (40%) | Strong | Investigate root causes; consider preventive maintenance program |
| Vague descriptions add ~16 hrs | Moderate | Enforce structured intake forms, especially for printer tickets |
| Self-resolution concentrated in network/database | Moderate | Consider wait-and-monitor SOP for these categories before dispatch |
| 24-hr resolution floor likely artificial | Weak/data quality | Validate timestamps; may distort SLA metrics |
| Critical tickets resolve faster | Suggestive (small n=27) | Prioritization process appears functional but needs larger sample |
| Agent resolution time gap | Weak without mix control | Investigate Luke Wilson's caseload before drawing performance conclusions |

---

## Caveats

- The dataset covers only ~2 months; seasonal or organizational patterns cannot be assessed.
- The `description_vague` and `self_resolved` columns appear to be derived/augmented labels — their generation methodology is unknown and may introduce labeling noise.
- Multiple tickets with exactly 24.0-hour resolution times suggest possible data imputation rather than actual closure records.
