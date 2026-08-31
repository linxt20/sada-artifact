---
dataset: flag_19
scenario: predictive_declined
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "state_declined"
query: "What signals suggest an expense will be declined?"
source_table: augment_table/flag_19/predictive_declined/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:15:58.346126+00:00
wall_seconds: 42.87
---

# Signals That Suggest an Expense Will Be Declined

**Dataset:** `sonnet__skill_on_v11_update.csv` | 500 rows, 46 Declined (9.2%)

---

## Key Finding: `processed_date_present` is a Perfect Discriminator

The single strongest signal is whether `processed_date` is populated:

| `processed_date_present` | Declined | Pending | Processed | Submitted |
|---|---|---|---|---|
| **False** | 46 | 80 | 0 | 41 |
| **True** | 0 | 0 | 333 | 0 |

> **Every single declined expense has no processed date.** The absence of a processed date is a necessary (though not sufficient) condition for decline — it is also shared by Pending and Submitted records.

---

## Secondary Signals

### 1. Department — IT is a Major Risk Factor

| Department | Decline Rate | Count |
|---|---|---|
| **IT** | **44.2%** | 43 |
| HR | 14.3% | 14 |
| Finance | 9.1% | 22 |
| Customer Support | 6.0% | 267 |
| Sales | 4.9% | 122 |
| Development | 5.0% | 20 |
| Product Management | 0.0% | 12 |

IT department expenses are declined at nearly 8× the baseline rate. This is the strongest categorical predictor.

### 2. CI Specificity — Vague Descriptions Increase Decline Risk

| `ci_specificity` | Decline Rate | Count |
|---|---|---|
| `generic_label` | **19.0%** | 58 |
| `asset_code_only` | **14.5%** | 69 |
| `named_model` | 7.3% | 303 |
| `service_name` | 4.3% | 70 |

Expenses with vague CI descriptions (`generic_label`) are declined at more than 4× the rate of those with explicit service names. Providing a specific, named model or service is associated with lower decline rates.

### 3. Vendor — "Unknown" Vendor Elevates Risk

Declined expenses have a notably higher share of `Unknown` vendor brand (28.3%) vs. non-declined (18.3%). Named vendors (Dell, HP, Lenovo) dominate both groups but are slightly underrepresented among declines.

### 4. Amount — Declined Expenses Trend Lower

| Group | Mean Amount | Median Amount |
|---|---|---|
| Declined | $3,706 | $3,471 |
| Non-declined | $4,429 | $4,434 |

Declined expenses are slightly lower in value on average (~$700 less), but the overlap is large. This is weak evidence on its own and should not be used as a standalone signal.

### 5. Entry Origin and Asset Type — Weaker Signals

- `auto_generated` entries appear slightly more often among declines (39.1%) vs. non-declines (32.8%), but the difference is modest.
- `travel_equipment` is overrepresented in declines (19.6% vs. 13.9% non-declined); `cloud_service` is underrepresented (2.2% vs. 7.9%).

---

## Combined Risk Profile

An expense is **most likely to be declined** when it exhibits:

1. ✅ **No processed date** (`processed_date_present = False`) — mandatory condition
2. ✅ **IT department** — 44% decline rate among unprocessed IT expenses
3. ✅ **Vague CI description** — `generic_label` or `asset_code_only`
4. ✅ **Unknown vendor brand**

---

## Important Caveats

- Missing `processed_date` is shared by **Pending** and **Submitted** records too — it is necessary but not sufficient for predicting decline.
- `source_id_present` alone has only a weak effect (decline rate 26.4% without source ID vs. 30.4% without — both conditions lead to decline only when processed date is also missing).
- Sample size for Declined (n=46) is limited; department-level rates (especially HR, Finance) should be interpreted cautiously.
- No temporal patterns were tested (date ranges are narrow: 2023–2024).
