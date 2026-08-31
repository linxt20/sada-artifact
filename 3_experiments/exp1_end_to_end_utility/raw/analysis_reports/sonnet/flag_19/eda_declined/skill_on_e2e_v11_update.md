---
dataset: flag_19
scenario: eda_declined
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "state_declined"
query: "What kinds of expenses tend to get declined, and does it differ by department?"
source_table: augment_table/flag_19/eda_declined/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:16:16.731224+00:00
wall_seconds: 73.67
---

# Declined Expense Analysis
**Dataset:** 500 expense records · 46 declined (9.2% overall decline rate)

---

## Method Note
TAPP-generated columns used in this analysis: `asset_category`, `procurement_action_type`, `is_travel_related`, `has_source_id`, `ci_id_quality`, `entry_origin`. Column `asset_brand` was inspected but showed weak differentiation. `procurement_action_type` was largely uniform (asset_registration dominated) and added limited signal beyond `category`.

---

## 1. What Kinds of Expenses Get Declined?

### By Category

| Category | Total | Declined | Decline Rate |
|---|---|---|---|
| Miscellaneous | 17 | 3 | **17.6%** |
| Travel | 94 | 10 | **10.6%** |
| Assets | 310 | 27 | 8.7% |
| Services | 79 | 6 | 7.6% |

**Miscellaneous** has the highest decline rate (17.6%), though its absolute volume is small (n=17). **Travel** is notable as the second-highest rate (10.6%) with meaningful volume (n=94, 10 declined).

### By Amount

Declined expenses have a **lower median amount** ($3,471) compared to non-declined ($4,434), suggesting that higher-value expenses are not more likely to be declined — if anything, smaller or incomplete requests may be more prone to rejection.

| State | Count | Mean ($) | Median ($) |
|---|---|---|---|
| Declined | 46 | 3,706 | 3,471 |
| Not Declined | 454 | 4,429 | 4,434 |

### By Asset Type (`asset_category`)

Within the Assets category, **hardware_laptop** accounts for the plurality of declined items (22 of 46 total declines, 48%). `hardware_desktop` has a relatively elevated decline rate (~6.1% of its 99 records). `hardware_server` and `cloud_service` show 0 and 2.8% decline rates respectively, suggesting infrastructure-class assets are rarely declined.

| asset_category | Total | Declined | Rate |
|---|---|---|---|
| hardware_laptop | 205 | 22 | 10.7% |
| travel_equipment | 76 | 9 | 11.8% |
| hardware_desktop | 99 | 6 | 6.1% |
| software_service | 38 | 5 | 13.2% |
| hardware_peripheral | 28 | 2 | 7.1% |
| cloud_service | 36 | 1 | 2.8% |
| hardware_server | 15 | 0 | 0.0% |

`travel_equipment` and `software_service` show elevated decline rates among TAPP-identified asset sub-types.

### Travel-Related Expenses (`is_travel_related`)

Expenses flagged as travel-related decline at **10.6%** vs. 8.9% for non-travel, a modest difference consistent with the `Travel` category finding above.

---

## 2. Does It Differ by Department?

| Department | Total | Declined | Decline Rate |
|---|---|---|---|
| **IT** | 43 | 19 | **44.2%** |
| HR | 14 | 2 | 14.3% |
| Finance | 22 | 2 | 9.1% |
| Customer Support | 267 | 16 | 6.0% |
| Development | 20 | 1 | 5.0% |
| Sales | 122 | 6 | 4.9% |
| Product Management | 12 | 0 | 0.0% |

**IT stands out dramatically** — 44.2% of IT expenses are declined, vs. a 5–14% range for all other departments. IT alone accounts for 19 of 46 total declines (41%) despite being only 8.6% of all records.

### IT Department Breakdown

Within IT, **Assets** drive the declines (13 of 19 IT declines). `asset_category` shows IT declines are split across `hardware_laptop` (9), `hardware_desktop` (4), `travel_equipment` (3), and `software_service` (2) — spread across types rather than concentrated in one sub-type, suggesting a department-level review policy rather than a category-specific rule.

| Category | IT Total | IT Declined | IT Decline Rate |
|---|---|---|---|
| Assets | 23 | 13 | 56.5% |
| Services | 7 | 2 | 28.6% |
| Travel | 10 | 3 | 30.0% |
| Miscellaneous | 3 | 1 | 33.3% |

---

## 3. Supporting TAPP Facet Signals

### `has_source_id` (reference linkage)
Expenses **without** a source ID are declined at a higher rate (12.5%) than those with one (8.2%), suggesting unlinked or informal requests face more scrutiny.

### `ci_id_quality` (asset identifier quality)
Expenses with `opaque_serial_code` CI identifiers decline at 13.5%, compared to 8.5% for `standard_model_name` and 7.7% for `generic_placeholder`. Poorly formatted asset identifiers modestly correlate with decline, but the effect is not dramatic.

### `entry_origin`
Auto-generated entries decline at 11.4% vs. 8.2% for manually-entered — a minor difference; no strong pattern.

---

## 4. Summary

| Finding | Key Metric |
|---|---|
| **IT department** is the primary driver of declines | 44.2% decline rate (19/43 records) |
| **Miscellaneous** category has the highest decline rate | 17.6% (3/17) |
| **Travel** and **travel_equipment** show elevated rates | ~10–12% |
| **hardware_laptop** and **software_service** are highest-volume declined asset types | 22 and 5 declines respectively |
| Declined amounts are **lower** on average | Median $3,471 vs. $4,434 |
| Expenses **missing source IDs** decline at a higher rate | 12.5% vs. 8.2% |

The dominant pattern is departmental: IT's 44% decline rate is anomalous and warrants investigation into whether IT purchasing follows a different approval workflow or has a backlog of improperly submitted asset requests. Outside IT, declines are spread across Miscellaneous and Travel categories, often for smaller amounts and records with weaker documentation (`has_source_id = False`, `ci_id_quality = opaque_serial_code`).
