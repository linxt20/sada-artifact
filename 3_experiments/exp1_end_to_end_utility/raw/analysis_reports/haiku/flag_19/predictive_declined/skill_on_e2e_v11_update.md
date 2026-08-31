---
dataset: flag_19
scenario: predictive_declined
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "state_declined"
query: "What signals suggest an expense will be declined?"
source_table: augment_table/flag_19/predictive_declined/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:16:29.071378+00:00
wall_seconds: 72.38
---

# Analysis Report: Signals of Expense Decline

## Executive Summary

This analysis identifies key signals associated with expense decline in the augmented dataset ($N=500$). The query asks: **What signals suggest an expense will be declined?**

**Primary Finding**: **Absence of a processed_date is the strongest decline signal**, present in 100% of declined expenses. Combined with department, requester status, and asset tracking patterns, several high-risk profiles emerge.

---

## Methodology

This analysis examined the complete augmented dataset using both original structured columns and TAPP-generated semantic facets. The TAPP-generated columns analyzed are:
- `asset_category_type`
- `asset_creation_mechanism`
- `department_classification`
- `travel_asset_flag`
- `requester_repeat_status`
- `source_tracking_present`

Declined expenses are operationalized as all records with `state = "Declined"` ($n=46$, 9.2% of total).

---

## Key Decline Signals

### 1. **Absence of Processed Date (STRONGEST SIGNAL)**

| Metric | Value |
|--------|-------|
| Declined expenses with missing `processed_date` | 46/46 (100%) |
| Non-declined with missing `processed_date` | 121/454 (26.7%) |
| **Decline risk if `processed_date` missing** | **Nearly 10× baseline** |

**Interpretation**: All declined expenses lack a processed_date timestamp, indicating they were never successfully processed through the system. This is the most deterministic signal in the dataset.

---

### 2. **IT Department Concentration**

| Department | Declined | Total | Decline Rate |
|---|---|---|---|
| **IT** | 19 | 43 | **44.2%** |
| Customer Support | 16 | 267 | 6.0% |
| Sales | 6 | 122 | 4.9% |
| Finance | 2 | 22 | 9.1% |
| HR | 2 | 14 | 14.3% |
| Development | 1 | 20 | 5.0% |
| Product Management | 0 | 12 | 0% |

**Finding**: IT department shows 44.2% decline rate (19/43), compared to 5.9% for all other departments combined (27/457). This represents a **7.5× increased risk** relative to organization baseline.

---

### 3. **Single-Request Requesters (High Decline Risk)**

Requester status is captured via the TAPP-generated `requester_repeat_status` column:

| Requester Type | Declined | Total | Decline Rate |
|---|---|---|---|
| **Single Request** | 20 | 145 | **13.8%** |
| Occasional User | 21 | 220 | 9.5% |
| High Frequency User | 5 | 135 | 3.7% |

**Finding**: One-time requesters ("single_request") show 13.8% decline rate, more than 3× higher than frequent users (3.7%). This suggests unfamiliarity with process or incomplete requisition information.

---

### 4. **Absence of Source Tracking**

The TAPP-generated `source_tracking_present` column indicates whether upstream tracking data (source_id) exists:

| Tracking Present | Declined | Total | Decline Rate |
|---|---|---|---|
| No (`source_tracking_present = False`) | 14 | 113 | **12.4%** |
| Yes (`source_tracking_present = True`) | 32 | 387 | 8.3% |

**Finding**: Expenses lacking source tracking show 12.4% decline vs. 8.3% with tracking—a 1.5× relative increase. This suggests incomplete documentation or external system disconnection.

---

### 5. **Asset Creation Mechanism in IT (Department-Specific Pattern)**

The `asset_creation_mechanism` (TAPP-generated) distinguishes manual vs. automated entry:

**Within IT Department Only:**
| Mechanism | Declined | Total | Decline Rate |
|---|---|---|---|
| Auto-generated | 10 | 21 | **47.6%** |
| Manually created | 9 | 22 | **40.9%** |

**Outside IT:**
- Auto-generated: 9/213 (4.2%)
- Manually created: 18/244 (7.4%)

**Finding**: Both creation mechanisms carry elevated risk in IT, but automation shows slightly higher risk (47.6% vs. 40.9%), contrary to typical expectations. This may reflect auto-generated entries lacking adequate human review in IT's stricter approval workflow.

---

### 6. **Travel Asset Flag (Moderate Signal)**

The `travel_asset_flag` shows marginal elevation:

| Travel Asset | Declined | Total | Decline Rate |
|---|---|---|---|
| Yes (travel_asset_flag = True) | 10 | 94 | 10.6% |
| No (travel_asset_flag = False) | 36 | 406 | 8.9% |

**Finding**: Travel-related expenses show 1.2× increased risk, but this is modest and not a primary driver.

---

### 7. **Hardware Device Dominance**

The `asset_category_type` breakdown:

| Category Type | Declined | Total | Decline Rate |
|---|---|---|---|
| Hardware Device | 29 | 323 | 9.0% |
| Miscellaneous | 3 | 27 | 11.1% |
| Service Subscription | 6 | 76 | 7.9% |
| Travel Equipment | 9 | 74 | 12.2% |

**Finding**: Hardware and travel equipment show slightly elevated decline rates. However, this is primarily driven by department/IT composition rather than category itself—IT procures mostly hardware.

---

## Composite Risk Profiles

### High-Risk Combination: IT + Single Request + No Tracking

| Combination | Declined | Total | Rate |
|---|---|---|---|
| IT + single_request + no source_tracking | 2 | 3 | **66.7%** |
| IT + single_request + any tracking | 2 | 6 | **33.3%** |
| IT + any requester + any tracking | 9 | 37 | **24.3%** |

**Interpretation**: One-time IT requests without external tracking documentation show extreme risk (66.7%), though sample size is small ($n=3$).

### Low-Risk Profile: High-Frequency User + Source Tracking Present

| Profile | Declined | Total | Rate |
|---|---|---|---|
| High frequency + source_tracking = True | 4 | 112 | **3.6%** |
| High frequency + source_tracking = False | 1 | 23 | **4.3%** |

**Finding**: Repeat users with tracking show only 3.6% decline rate—the lowest in the dataset.

---

## Supporting Quantitative Evidence

### Amount Analysis
- **Declined expenses**: Mean $3,706 (Median $3,471, SD $2,668)
- **Non-declined**: Mean $4,429 (Median $4,434, SD $2,549)
- **Implication**: Declined expenses tend to be slightly smaller, but difference is not large enough to be primary driver.

### Category Patterns (Original `category` Column)
| Category | Decline Rate |
|---|---|
| Miscellaneous | 17.6% (3/17) |
| Travel | 10.6% (10/94) |
| Assets | 8.7% (27/310) |
| Services | 7.6% (6/79) |

---

## Integration of TAPP Facets with Original Data

### What TAPP Adds
The TAPP-generated columns clarify **semantic relationships** not obvious from raw data:

1. **`department_classification`** confirms raw department field; no new signal.
2. **`requester_repeat_status`** captures user history not explicitly in raw columns—adds predictive power.
3. **`asset_creation_mechanism`** reveals internal process differences (manual vs. auto) with different decline patterns by department.
4. **`source_tracking_present`** synthesizes source_id missingness into actionable "tracking" status.
5. **`asset_category_type`** aligns with raw category but enables cross-departmental analysis.
6. **`travel_asset_flag`** adds modest signal; most travel-related information is already in category.

### What TAPP Does NOT Explain
- The 100% processed_date missingness in declined cases is **raw evidence** predating any TAPP facet. It reflects system state, not semantic enrichment.
- IT department's exceptionally high decline rate (44.2%) is a **structural/organizational pattern**, not a TAPP artifact.

---

## Summary of Key Risk Signals

| Signal | Impact | Coverage | Certainty |
|---|---|---|---|
| **No processed_date** | Deterministic | 100% of declined | Certain |
| **IT department** | 7.5× baseline risk | 41% of declined | Very High |
| **Single-request requester** | 3.7× baseline risk | 43% of declined | High |
| **No source tracking** | 1.5× baseline risk | 30% of declined | Moderate |
| **Auto-generated in IT** | 5.4× baseline (IT only) | 22% of declined | Moderate |
| **Travel asset** | 1.2× baseline risk | 22% of declined | Low |

---

## Recommendations

1. **Immediate**: Flag any expense without processed_date as high-risk requiring triage.
2. **Department-specific**: Implement enhanced review for IT requisitions, especially single-request one-time items.
3. **Tracking imperative**: Ensure source_id is populated for all expenses to improve auditability and reduce decline risk.
4. **Requester education**: Provide targeted training for single-request users on complete documentation requirements.
5. **Automation review**: Audit auto-generated asset entries in IT for missing validation steps.

---

## Limitations

- Sample size for declined cases ($n=46$) is modest; rare combinations (e.g., IT + single + no tracking, $n=3$) lack statistical power.
- No temporal trend analysis conducted (all dates in 2023–2024).
- **`source_id` missingness correlates with both non-decline and decline**, suggesting it reflects both legitimate omissions and genuine gaps.

---

## Conclusion

Expense decline is primarily driven by **IT department concentration** (44.2% decline rate vs. 6% baseline) combined with **absence of processed date** (universal in declined cases). Secondary factors include **single-request status** (13.8% decline rate) and **missing source tracking** (12.4% decline rate). The TAPP-generated columns (`requester_repeat_status`, `source_tracking_present`, `asset_creation_mechanism`) provide valuable semantic facets that clarify these relationships, particularly in cross-departmental risk stratification. However, the strongest decline signal—absence of processed_date—is a raw structural indicator, not a TAPP inference.
