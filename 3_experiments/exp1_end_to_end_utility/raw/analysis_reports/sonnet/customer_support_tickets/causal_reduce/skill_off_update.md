---
dataset: customer_support_tickets
scenario: causal_reduce
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "resolution_minutes"
query: "How can support teams reduce ticket resolution time?"
source_table: augment_table/customer_support_tickets/causal_reduce/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:05:31.749702+00:00
wall_seconds: 41.47
---

# Reducing Ticket Resolution Time — Analysis Report

**Dataset:** `customer_support_tickets` (250 tickets) | **Focus variable:** `resolution_minutes` (mean: 64.9 min, range: 12–180 min)

---

## Key Findings

### 1. Channel Selection Has the Largest Impact

| Channel | Avg Resolution (min) | Ticket Count |
|---------|---------------------|--------------|
| Chat    | 22.5                | 50           |
| In-app  | 35.0                | 50           |
| Phone   | 70.2                | 50           |
| Email   | 98.3                | 100          |

Chat resolves tickets **4× faster** than email. Email is both the slowest channel and the most heavily used (40% of tickets). Steering customers toward chat or in-app for appropriate issue types is the highest-leverage lever available.

> **Exception:** High-priority tickets submitted via email average 132.8 min vs. 48.0 min for the same priority via chat — suggesting email handling of urgent issues is especially costly.

---

### 2. Accurate Complexity Assessment Enables Faster Routing

| Estimated Complexity | Avg Resolution (min) |
|---------------------|---------------------|
| Low                 | 33.2                |
| Medium              | 64.6                |
| High                | 71.8                |

Complexity correlates strongly with resolution time, but the gap between medium and high is modest (~7 min). Misclassifying a low-complexity ticket as medium or high wastes the most time, since low-complexity tickets resolve in half the time.

---

### 3. Self-Service Deflection Cuts Time Significantly

- **Self-service candidates** (94 tickets, 38%): avg **47.0 min**
- **Non-candidates** (156 tickets, 62%): avg **75.6 min**
- Difference: **~28.6 min per ticket**

All self-service-candidate tickets fall in the `low` or `medium` complexity bands (avg 34.7 and 48.8 min respectively). Proactively surfacing knowledge base articles or guided flows for these tickets — especially in `feature_request`, `account`, and `auth` categories — could prevent escalation and shorten handling time.

---

### 4. Routing Accuracy Is Critical for Specialist Queues

| Routing Path                   | Avg Resolution (min) |
|-------------------------------|---------------------|
| route_to_product_team          | 36.4                |
| route_to_billing_specialist    | 60.7                |
| route_to_security_team         | 61.2                |
| handle_by_first_tier           | 69.2                |
| escalate_to_senior             | 76.0                |
| route_to_integration_specialist| 88.0                |

Integration and senior escalation paths are the slowest. Notably, `handle_by_first_tier` tickets without self-service potential average 79.3 min — nearly as slow as senior escalations — indicating first-tier agents may be struggling with complex cases that reach them incorrectly.

---

### 5. Priority Labeling Anomaly — "High" Is Slower Than "Critical"

| Priority | Avg Resolution (min) |
|---------|---------------------|
| Low      | 37.5                |
| Medium   | 41.6                |
| Critical | 74.4                |
| High     | **131.1**           |

Counter-intuitively, `High`-priority tickets take nearly **twice as long** as `Critical` tickets. Critical tickets may trigger faster SLA responses and escalation paths, while High tickets linger in standard queues. This suggests SLA enforcement and queue prioritization are not aligned with the `High` label.

---

## Recommendations for Support Teams

| Action | Expected Impact |
|--------|----------------|
| **Shift volume from email to chat/in-app** | ~40–75 min savings per ticket |
| **Enforce self-service routing for flagged candidates** | ~28 min savings per ticket |
| **Fix routing accuracy for integration tickets** | Reduces 88-min average for integration queue |
| **Audit High-priority SLA — treat it closer to Critical** | Addresses the 131-min outlier for High priority |
| **Improve first-tier triage to reduce incorrect escalations** | First-tier non-self-service tickets average 79 min; better triage could resolve more in-queue |

---

## Caveats

- With 250 tickets, some cells (e.g., High-priority chat, n=2) have very small sample sizes and should be interpreted cautiously.
- `issue_description` text was not analyzed; qualitative patterns in ticket language may reveal additional routing signals.
- No agent-level performance data was analyzed; agent skill variance (hidden here due to `skill_off` variant) may explain residual variance.
