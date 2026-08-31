---
dataset: customer_support_tickets
scenario: causal_handling
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "handling_time_gap"
query: "Why do handling times differ by channel and priority?"
source_table: augment_table/customer_support_tickets/causal_handling/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:05:08.404996+00:00
wall_seconds: 41.86
---

# Handling Time Differences by Channel and Priority
**Dataset:** `sonnet__skill_off_update.csv` — 250 tickets across 4 channels and 4 priority levels.

---

## 1. Handling Time by Channel

| Channel | Mean (min) | Median (min) | n | Async? |
|---------|-----------|-------------|---|--------|
| Chat    | 22.5      | 23.0        | 50 | No    |
| In-App  | 35.0      | 31.0        | 50 | Yes   |
| Phone   | 70.2      | 72.5        | 50 | No    |
| Email   | 98.3      | 92.5        | 100 | Yes  |

**Key pattern:** The two fastest channels (chat, in-app) handle tickets in under ~35 minutes on average, while the two slowest (phone, email) average 70–98 minutes. However, the `is_async_channel` flag does **not** cleanly explain the split — chat is synchronous yet fast, while phone is also synchronous but slow. In-app (async) is fast, while email (async) is the slowest.

The faster performance of chat and in-app likely reflects the **nature of issues routed there** (e.g., low/medium priority feature requests and auth issues) rather than the channel modality itself. Email, with the highest volume (n=100), is disproportionately loaded with **High-priority billing tickets** (49 of 50 High tickets go to email), which mechanically inflates its average.

---

## 2. Handling Time by Priority

| Priority | Mean (min) | Median (min) | n | Expected (min) |
|----------|-----------|-------------|---|----------------|
| Low      | 37.5      | 24.0        | 74 | 37.5 |
| Medium   | 41.6      | 37.0        | 76 | 41.6 |
| Critical | 74.4      | 72.5        | 50 | 74.4 |
| High     | 131.1     | 131.0       | 50 | 131.1 |

**Key pattern:** Handling time rises with priority, but not monotonically in the expected direction — **High tickets take longer than Critical**. This is a structural feature of the data: High-priority tickets are almost exclusively handled via **email** (49/50), the slowest channel, whereas Critical tickets go predominantly through **phone** (38/50). The channel assignment appears to drive observed resolution time as much as the priority label itself.

Notably, actual `resolution_minutes` match `expected_resolution_minutes` almost exactly (deviation near 0% for all segments), indicating the routing rules are well-calibrated and deviations are negligible.

---

## 3. Channel–Priority Interaction (Confounding)

| Priority | Chat | Email | In-App | Phone |
|----------|------|-------|--------|-------|
| Critical | —    | —     | 57.5   | 79.7  |
| High     | 48.0 | 132.8 | —      | —     |
| Low      | 15.9 | 71.6  | 24.2   | —     |
| Medium   | 27.8 | 58.8  | 35.2   | 40.0  |

The cross-tab shows **strong channel–priority confounding**: most cells are empty because tickets are routed to specific channels by priority. Within Medium (the most balanced tier), email is still ~2× slower than chat (58.8 vs. 27.8 min), confirming a genuine email channel penalty even after holding priority constant.

---

## 4. Summary of Causal Factors

| Factor | Evidence Strength | Direction |
|--------|------------------|-----------|
| Priority level drives expected complexity | Strong — monotonic except High > Critical | ↑ priority → ↑ time |
| Channel routing is largely determined by priority | Strong — sparse cross-tab | Confounds both dimensions |
| Email channel adds inherent latency | Moderate — visible within Medium/Low | +30–55 min vs. chat |
| Async vs. sync channel modality | Weak — inconsistent (in-app fast, phone slow) | Not a clean predictor |

---

## 5. Caveats

- **High > Critical anomaly** is driven by routing (High → email), not necessarily by ticket complexity.
- The near-zero deviation from expected resolution suggests the expected values may be derived from the same routing rules, limiting their independent diagnostic value.
- Low sample sizes in some cross-cells (e.g., High–Chat: n=1) make cell-level estimates unreliable.
