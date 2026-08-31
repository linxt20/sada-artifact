---
dataset: flag_20
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's worth analyzing in these travel-expense records."
source_table: augment_table/flag_20/focus_inference/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:18:23.981937+00:00
wall_seconds: 86.22
---

# Travel-Expense Records: Analysis Report

## Executive Summary

The 500-record dataset spans expense/asset records opened June 2023 – April 2024. The most actionable finding is a structural split between **Travel** and **non-Travel** records that drives nearly all declination risk, processing completeness, and amount patterns. Three TAPP-generated columns (`travel_context`, `asset_category`, `source_id_present`) materially clarify this split; the remaining TAPP facets add limited incremental signal beyond the original `category` column.

---

## Method Note

TAPP-generated columns used in this report: `travel_context`, `asset_category`, `source_id_present`, `creation_method`, `record_action_type`, `processing_lag_band`, `department_group`. Columns `ci_form_factor`, `asset_brand`, `is_miscellaneous_ci` were examined but found redundant with or subordinate to the dimensions above and are noted only where relevant.

---

## 1. Outcome Distribution (State)

| State | Count | % of Total |
|---|---|---|
| Processed | 295 | 59.0% |
| Declined | 84 | 16.8% |
| Pending | 69 | 13.8% |
| Submitted | 52 | 10.4% |

The **declination rate of 16.8%** is the primary quality concern. Amounts range from \$128 to \$8,994 (mean \$4,389, median \$4,291).

---

## 2. The Dominant Driver: Travel vs. Non-Travel

The original `category` column separates records sharply:

| Category | N | Decline Rate | Mean Amount |
|---|---|---|---|
| Travel | 146 | **41.8%** | \$4,172 |
| Services | 47 | 10.6% | \$1,120 |
| Assets | 281 | 6.0% | \$5,220 |
| Miscellaneous | 26 | 3.8% | \$2,549 |

**Travel records account for 61/84 (72.6%) of all declined records** despite being only 29.2% of the dataset.

### Why Travel Records Are Structurally Different

Every single Travel record (146/146) has `source_id_present = False`, while only 27/354 (7.6%) of non-Travel records lack a source ID. Missing source ID correlates with a 35.8% decline rate vs. 6.7% when present. Travel records are systematically submitted without a backing reference ID, which is the proximate administrative reason for declinations.

TAPP's `travel_context` column confirms and sub-segments this finding:

| travel_context | N | Decline Rate |
|---|---|---|
| travel_accessory | 108 | 41.7% |
| travel_transport | 20 | 45.0% |
| travel_digital_system | 11 | **54.5%** |
| travel_accommodation | 1 | 0.0% |
| not_travel | 360 | 6.7% |

Within Travel, digital-system expenses (e.g., booking software) have the highest decline rate at 54.5%. TAPP's `asset_category` further resolves this:

| asset_category | N | Decline Rate |
|---|---|---|
| travel_equipment | 104 | 44.2% |
| travel_transport | 21 | 42.9% |
| hardware_server | 25 | **24.0%** |
| hardware_endpoint | 279 | 6.5% |
| cloud_service | 33 | 9.1% |

---

## 3. Missing Source ID as a Standalone Risk Factor

| source_id_present | N | Decline Rate | Processed Rate |
|---|---|---|---|
| False | 173 | **35.8%** | 30.1% |
| True | 327 | 6.7% | 68.2% |

This is the single strongest predictor of outcome in the dataset (35.8% vs. 6.7% decline). Since all Travel records lack a source ID, this is partially collinear with category, but within non-Travel, the 27 records missing a source ID still decline at 26% (7/27) vs. 4.5% (15/327) for those with one.

---

## 4. Department Patterns

| Department | N | Decline Rate | Travel Share |
|---|---|---|---|
| Customer Support | 272 | 17.6% | 28.7% |
| Sales | 141 | 18.4% | 31.2% |
| IT | 42 | 16.7% | 21.4% |
| Finance | 16 | 6.2% | 25.0% |
| Development | 16 | 0.0% | 25.0% |

Customer Support (272 records, 54.4% of the dataset) and Sales (141 records, 28.2%) dominate volume. Their elevated decline rates are largely explained by their higher Travel expense shares. Development's 0% decline rate (16 records, small sample) is notable but low-confidence. TAPP's `department_group` column is a near-exact copy of the original `department` field; it adds no incremental signal.

---

## 5. Creation Method

| creation_method | N | Decline Rate |
|---|---|---|
| manual | 315 | 18.1% |
| automated | 185 | 14.6% |

Manual records decline slightly more often, but the gap is modest (3.5 pp). TAPP's `record_action_type` shows that **registration** (n=319, 63.8% of records) dominates and declines at 18.5% (59/319); `procurement` (n=97) declines at 15.5%; `provisioning` (n=41) at only 2.4% (all cloud/service records).

---

## 6. Processing Lag

`processing_lag_band` cleanly partitions processed vs. unprocessed records:

| Band | N | Notes |
|---|---|---|
| not_processed | 205 | All Declined, Pending, or Submitted |
| same_day | 104 | All Processed |
| within_7_days | 182 | All Processed |
| 8_to_30_days | 7 | All Processed |
| over_30_days | 2 | All Processed |

104/295 processed records (35.3%) are same-day, 182/295 (61.7%) within 7 days. This column is essentially a restatement of `processed_date` presence and `state`; it adds definitional convenience but no new explanatory signal.

---

## 7. Amount Patterns

Submitted (unfinalized) records carry the highest mean amount (\$5,712 vs. \$4,284 for Processed), driven by Travel Submitted records averaging \$6,167. There is no strong monotonic relationship between amount and decline rate across quartiles (Q1: 20.8%, Q2: 15.2%, Q3: 20.8%, Q4: 10.4%), suggesting amount is not a primary decline driver.

---

## 8. Key Findings and Recommendations

| Priority | Finding | Evidence |
|---|---|---|
| **High** | Travel category has a 41.8% decline rate | 61/146 Travel records declined; 72.6% of all declines |
| **High** | All Travel records lack a source ID | 146/146 `source_id_present = False` for Travel |
| **High** | Missing source ID → 35.8% decline rate overall | 62/173 declined without source ID |
| **Medium** | travel_digital_system sub-type declines 54.5% | 6/11 records; small N, warrants monitoring |
| **Medium** | Customer Support + Sales = 82.6% of volume | Process changes here have maximum reach |
| **Low** | Manual creation slightly worse than automated | 18.1% vs. 14.6%; modest gap |

**Recommended focus areas:**
1. **Mandate source IDs for Travel submissions** — this alone could eliminate the structural 41.8% decline rate in that category.
2. **Audit Travel expense workflows in Customer Support and Sales**, which together produce 53/61 Travel declines.
3. **Investigate travel_digital_system expenses** (TAPP `travel_context` = `travel_digital_system`): 54.5% decline rate suggests unclear policy or miscategorization.
