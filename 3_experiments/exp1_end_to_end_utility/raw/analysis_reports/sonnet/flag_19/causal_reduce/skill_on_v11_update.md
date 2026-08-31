---
dataset: flag_19
scenario: causal_reduce
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "state_declined"
query: "How can we reduce declined expense submissions?"
source_table: augment_table/flag_19/causal_reduce/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:15:21.071116+00:00
wall_seconds: 56.32
---

# Reducing Declined Expense Submissions — Analysis Report

**Dataset:** 500 expense submissions | **Declined:** 46 (9.2%) | **Date:** 2026-07-30

---

## Key Finding: All Declined Submissions Were Never Processed

The `processing_lag_band` data reveals that **100% of the 46 declined submissions fall in the `not_processed` band** (46/167 = 27.5% decline rate). No submission with a recorded processed date was declined. This is the single strongest signal: submissions that stall without processing are overwhelmingly at risk of declination.

---

## Factor 1: Department — IT Is a Critical Hotspot

| Department | Total | Declined | Decline Rate |
|---|---|---|---|
| **IT** | 43 | 19 | **44.2%** |
| HR | 14 | 2 | 14.3% |
| Finance | 22 | 2 | 9.1% |
| Customer Support | 267 | 16 | 6.0% |
| Sales | 122 | 6 | 4.9% |
| Development | 20 | 1 | 5.0% |
| Product Management | 12 | 0 | 0% |

IT's 44.2% decline rate dwarfs all other departments. Nearly half of all IT submissions are declined. This is the most actionable target — IT-specific process review (reviewer capacity, submission quality standards, or approval workflows) is likely required.

---

## Factor 2: CI Identifier Quality — Generic/Vague Labels Drive Declines

| CI Identifier Quality | Total | Declined | Decline Rate |
|---|---|---|---|
| `generic_or_category_label` | 63 | 11 | **17.5%** |
| `opaque_id_or_code` | 73 | 10 | **13.7%** |
| `specific_model_name` | 293 | 22 | 7.5% |
| `service_name` | 71 | 3 | 4.2% |

Submissions with vague or opaque CI identifiers decline at roughly 2–4× the rate of those with specific model names. Requiring submitters to provide a specific model name (e.g., "Dell Latitude 7490") rather than a generic label (e.g., "Random Access Memory Component") would likely reduce declines.

---

## Factor 3: Category — Miscellaneous Has Elevated Risk

| Category | Total | Declined | Decline Rate |
|---|---|---|---|
| Miscellaneous | 17 | 3 | **17.6%** |
| Travel | 94 | 10 | 10.6% |
| Assets | 310 | 27 | 8.7% |
| Services | 79 | 6 | 7.6% |

The `Miscellaneous` category has the highest decline rate, though the absolute volume is small (n=17). Eliminating or restricting the Miscellaneous category by requiring proper categorization at submission time may reduce declines.

---

## Factor 4: Missing Source ID

Submissions without a `source_id` (`has_source_id = False`) decline at **12.5%** vs. 8.2% for those with a source ID. Enforcing source ID linkage at submission time (especially in IT and HR) would reduce this gap.

---

## Factor 5: Submission Origin Type

| Origin Type | Total | Declined | Decline Rate |
|---|---|---|---|
| `travel_expense` | 89 | 10 | **11.2%** |
| `auto_generated` | 155 | 15 | 9.7% |
| `manual_purchase` | 216 | 18 | 8.3% |
| `service_provision` | 40 | 3 | 7.5% |

Travel expense submissions have the highest decline rate by origin type. Combined with the `travel_expense_narrative` description specificity showing 11.1% decline rate, travel expense submissions warrant review of their approval requirements and guidance.

---

## Recommendations (Priority Order)

1. **Investigate IT Department workflows** — With a 44.2% decline rate, IT represents the largest opportunity. Audit whether IT submissions lack required approvals, documentation, or CI data.
2. **Enforce specific CI identifiers** — Block or flag submissions using `generic_or_category_label` or `opaque_id_or_code` before submission. Require a recognizable model name or service name.
3. **Mandate source IDs** — Make `source_id` a required field at submission time to reduce unlinked (and thus unverifiable) submissions.
4. **Restrict "Miscellaneous" category** — Route miscellaneous submissions through mandatory re-categorization to reduce vague submissions that reviewers decline.
5. **Improve travel expense guidance** — Provide clearer templates or pre-approval workflows for travel-related submissions to reduce the 11.2% decline rate.

---

## Caveats & Weak Evidence

- The `processing_lag_band = not_processed` for all declined records could reflect that declination *causes* non-processing (i.e., declined = never assigned a processed date), rather than indicating a separate causal pathway. Caution is warranted in interpreting this as an independent factor.
- The IT department anomaly (44.2% decline) is striking but the sample is small (n=43); external factors (e.g., a policy change, a specific reviewer) may explain this pattern.
- Amount does not appear to be a strong driver: declined submissions average $3,706 vs. $4,436 for processed — a modest difference unlikely to be actionable.
- Product Management shows 0% decline rate but has only 12 records — insufficient to draw conclusions.
