---
dataset: flag_19
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth analyzing and actionable in these expense records."
source_table: augment_table/flag_19/focus_inference/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:16:19.444885+00:00
wall_seconds: 69.57
---

# Expense Records Analysis: What's Worth Analyzing and Actionable

## Overview

The dataset contains **500 expense records** spanning multiple departments, with a total recorded spend of **$2,181,285**. Records span the full lifecycle from opened to processed, with meaningful variation in approval outcomes, processing speed, and spend composition.

**Method note:** TAPP-generated columns used in this report: `spend_type`, `travel_flag`, `asset_lifecycle_action`, `record_origin`, `processing_lag_band`, `has_source_id`, `high_volume_user_flag`. Columns `asset_category` and `asset_brand` were reviewed but are largely redundant with the existing `category` and `ci` fields and are not foregrounded. `travel_flag` is a perfect mirror of `category == Travel` and adds no independent signal.

---

## 1. Processing Backlog — $533K at Risk

The single most actionable finding is a large unresolved backlog:

| State | Count | Total Amount |
|---|---|---|
| Processed | 333 | $1,477,255 |
| **Pending** | **80** | **$351,805** |
| **Submitted** | **41** | **$181,760** |
| Declined | 46 | $170,465 |

**121 records (24%) totaling $533,565 are unresolved** (Pending or Submitted). Customer Support owns the largest share ($282,873 across 64 records), followed by Sales ($126,839, 29 records).

`processing_lag_band` confirms the unresolved records are entirely in the `not_processed` band — no overlap with any lag bucket, indicating these are structural holds, not just slow queues. Among processed records, **112 (34%) took over one week**, concentrated in `physical_hardware` ($381K) and `travel_expense` ($86K) — the two highest-value `spend_type` categories.

**Action:** Prioritize clearing the Pending queue in Customer Support and Sales; separately audit why physical hardware and travel expenses regularly breach the one-week processing threshold.

---

## 2. IT Department Has an Anomalously High Decline Rate

| Department | Total Records | Declined | Decline Rate |
|---|---|---|---|
| IT | 43 | 19 | **44.2%** |
| HR | 14 | 2 | 14.3% |
| Finance | 22 | 2 | 9.1% |
| Customer Support | 267 | 16 | 6.0% |
| Sales | 122 | 6 | 4.9% |
| Development | 20 | 1 | 5.0% |
| Product Management | 12 | 0 | 0.0% |

IT's 44% decline rate is far outside the norm (~5–9% for other large departments). The 19 IT declines include 14 `physical_hardware`, 3 `travel_expense`, 1 `software_subscription`, and 1 `cloud_service` — the declines span spend types, suggesting a policy or approvals workflow issue rather than a single category problem. Mean declined amount in IT ($4,474) is near the overall processed mean ($4,436), so the declines are not trivially small-ticket items.

**Action:** Audit IT's approval workflow. With nearly half of submissions declined, there is likely a mismatch between submission practices and policy.

---

## 3. Spend Composition: Physical Hardware Dominates

| spend_type | Count | Mean Amount | Total |
|---|---|---|---|
| physical_hardware | 326 | $5,250 | $1,711,583 |
| travel_expense | 89 | $4,059 | $361,267 |
| cloud_service | 51 | $902 | $46,027 |
| network_service | 17 | $2,777 | $47,206 |
| software_subscription | 11 | $892 | $9,808 |
| Unknown | 6 | $899 | $5,394 |

**Physical hardware is 65% of records and 78% of total spend**, with a mean ticket size ($5,250) materially higher than all other categories. Cloud services, software subscriptions, and network services individually account for under $50K each — manageable but worth monitoring for growth trends.

The `asset_lifecycle_action` column shows that **353 of 326 physical hardware records** (70% of all records) are tagged `registration` — largely post-purchase asset bookkeeping — while `new_acquisition` (58) and `provisioning` (48) represent forward-looking spend commitments.

**Action:** Physical hardware unit costs and volumes should be the primary budget control lever. Track `new_acquisition` and `provisioning` records proactively rather than waiting for `registration`.

---

## 4. Source ID Coverage and Data Quality

`has_source_id` is False for **15% of all records (77 of 500)**. Among Pending records, 23 of 80 (29%) lack a source ID — a higher rate than Processed (20%) or Submitted (22%). Declined records also show 28% without a source ID.

`record_origin` shows 344 records are `manual_entry` vs. 156 `auto_generated`. Manual entries have a slightly higher decline rate (8% vs. 12% for auto-generated), but the difference is modest. The `processing_lag_band` pattern does not differ significantly between origins.

**Action:** The elevated missing-source-ID rate among Pending records warrants a validation gate — requiring source IDs before records enter the approval queue would reduce resolution delays.

---

## 5. High-Volume Users Represent Concentrated Spend

The `high_volume_user_flag` marks 272 users (54%) as high-volume. Despite being the majority, their mean spend per record ($4,185) is slightly *lower* than non-flagged users ($4,575), suggesting the flag captures frequency rather than ticket size. The top 10 users by cumulative spend range from $54K–$79K; **Felipe Mahone leads at $79,020**.

**Action:** Spot-check the top 10 users for policy compliance. The flag is a useful proxy for audit prioritization, but should be cross-referenced with the number of `Declined` or `Pending` submissions per user.

---

## Summary of Priority Actions

| Priority | Finding | Metric |
|---|---|---|
| 🔴 High | Clear Pending/Submitted backlog | 121 records, $533K |
| 🔴 High | Investigate IT decline rate | 44% decline rate vs. <10% elsewhere |
| 🟡 Medium | Reduce physical hardware processing lag | 34% of processed records took >1 week |
| 🟡 Medium | Enforce source ID at submission | 29% of Pending records missing source_id |
| 🟢 Low | Monitor cloud/SaaS spend growth | Currently <$60K combined, but fast-growing categories |
