---
dataset: flag_13
scenario: focus_inference
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth attention in these incident descriptions."
source_table: augment_table/flag_13/focus_inference/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:12:14.278026+00:00
wall_seconds: 62.76
---

# Incident Description Analysis — `attention_flag` Focus
**Dataset:** `sonnet__skill_off_update.csv` | 500 incidents | Variant: `skill_off`

---

## 1. Focus Variable: `attention_flag`

The dataset's key signal is the `attention_flag` column, which classifies each incident into one of four tiers:

| Flag | Count | Share |
|---|---|---|
| **Routine** | 389 | 77.8% |
| **Medium** | 53 | 10.6% |
| **High** | 37 | 7.4% |
| **Low-Anomaly** | 21 | 4.2% |

Most incidents are routine background noise. The ~22% flagged non-routine deserve focused attention.

---

## 2. What Drives a "High" Flag

**High** incidents are the clearest, most actionable tier:

- **100% are Priority 1 – Critical** (all 37 High-flagged incidents).
- **Dominant pattern: outage language.** Short descriptions uniformly use terms like *"down," "outage," "failure," "shutdown."*
- **Top topics:** Email (22/37 = 59%), Database (8/37 = 22%), Server (5/37 = 14%).
- **Typical examples:**
  - *"Email server outage"*, *"Email system failure"*, *"Database server is down"*, *"Server outage in main facility"*
- **Category alignment:** Network category dominates (25/37), reflecting how email/server issues are grouped, not just network connectivity per se.

> **Decision signal:** Any P1-Critical incident describing an outage or system-down state—especially for Email or Database—is a reliable High-attention trigger.

---

## 3. What Drives a "Medium" Flag

Medium incidents (53) represent a transitional zone:

- **87% are Priority 1 – Critical** (46/53); a small tail of 6 are P2-High and 1 is P3-Moderate.
- **Topics:** Email (21), Database (13), Network (4), Software (4), VPN (7), Server (2), Printer (2).
- Descriptions are more varied than High: *"Email server not responding," "Unable to access database," "Email function is not working properly," "Printing issues."*
- The key differentiator vs. High: descriptions tend to **stop short of explicit outage/down language**, or the topic (e.g., VPN, Printer) is lower business impact.

> Medium incidents still warrant review but lack the definitive outage signal of High cases.

---

## 4. What Drives a "Low-Anomaly" Flag

Low-Anomaly incidents (21) are the most distinctive tier to understand:

- **All are Priority 2 – High** (20) or P3-Moderate (1)—none are Critical.
- **Topics:** Database (12), Email (6), Network (3).
- **Descriptions signal degradation, not outage:** *"Database connection issues persist," "SQL Server performance issue," "Database is running slow," "Email system overload," "Email client continuously crashing," "Slow network connection."*
- **Pattern:** Recurring or persistent sub-failure conditions (slowdowns, crashes, post-update failures, backup failures) that are not a full service-down event but deviate from routine.

> Low-Anomaly incidents are worth attention precisely because they may be **early warnings** of escalation to full outages. The word "persist," "performance," "slow," "crashing," and "after update" are useful lexical markers.

---

## 5. Routine Incidents — What to Deprioritize

Routine incidents (389) are characterized by:
- **P2-High** (365/389) or lower priority.
- Standard connectivity complaints: *"Cannot connect to VPN," "Unable to connect to WiFi," "Database connection issue," "Email client not syncing."*
- Topics: VPN (102), Database (103), Network (72), Email (85).

Despite high individual counts, these are isolated, expected issues handled through standard workflows.

---

## 6. Topic-Level Risk Summary

| Topic | High | Medium | Low-Anomaly | Routine | Risk Profile |
|---|---|---|---|---|---|
| **Email** | 22 | 21 | 6 | 85 | Highest outage concentration |
| **Database** | 8 | 13 | 12 | 103 | High anomaly + outage risk |
| **Server** | 5 | 2 | 0 | 7 | Small volume, all outages |
| **VPN** | 0 | 7 | 0 | 102 | Routine-dominant, medium edge |
| **Network** | 1 | 4 | 3 | 72 | Mostly routine |

---

## 7. Key Exceptions and Caveats

- **Six Medium incidents are P2-High** (not P1-Critical), suggesting priority alone is not a perfect predictor of attention level; description semantics also matter.
- **One Low-Anomaly incident is P3-Moderate** — confirming anomaly detection is partially independent of priority rating.
- **`is_high_frequency_topic`** tags 459/500 incidents as Yes, making it a weak discriminator on its own; it does not cleanly separate flagged from routine.
- The `Low-Anomaly` category is small (21 incidents); patterns are suggestive but statistically thin.

---

## Summary

| Attention Tier | Key Signal |
|---|---|
| **High** | P1-Critical + outage/down/failure language in Email, Database, or Server |
| **Medium** | P1-Critical but softer failure language, or lower-impact topics (VPN, Printer) |
| **Low-Anomaly** | P2-High with degradation language: slow, crashing, persist, post-update |
| **Routine** | P2 or lower + standard connectivity complaints; high volume, low novelty |
