---
dataset: yelp_polarity_reviews
scenario: causal_negative
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "label_pos"
query: "Which factors best explain negative Yelp experiences?"
source_table: augment_table/yelp_polarity_reviews/causal_negative/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:23:56.360358+00:00
wall_seconds: 55.87
---

# Factors Explaining Negative Yelp Experiences

**Dataset:** 250 Yelp reviews (125 negative `label_pos=0`, 125 positive `label_pos=1`)  
**Method note:** Two TAPP-generated columns were analyzed — `service_staff_behavior` (categorical: type of staff misconduct or `not_present`) and `complaint_severity` (ordinal 1–5, missing for 112 rows, predominantly NaN in positive reviews). Both are used as supplementary evidence alongside the primary outcome variable `label_pos`.

---

## 1. Primary Outcome Distribution

The dataset is perfectly balanced: 125 negative and 125 positive reviews. This allows clean comparison of factor rates across sentiment groups.

---

## 2. Staff Behavior Is a Dominant Driver of Negative Reviews

`service_staff_behavior` is the strongest single discriminator between negative and positive reviews:

| Staff Behavior | Negative (`label_pos=0`) | Positive (`label_pos=1`) |
|---|---|---|
| `not_present` | 74 (59%) | 122 (98%) |
| `rude_or_hostile` | 29 (23%) | 1 (1%) |
| `dismissive_or_condescending` | 14 (11%) | 0 |
| `unprofessional` | 7 (6%) | 2 (2%) |
| `discriminatory` | 1 (1%) | 0 |
| **Any staff issue** | **51 / 125 (41%)** | **3 / 125 (2%)** |

**41% of all negative reviews** cite a specific staff misconduct pattern, versus just **2% of positive reviews** — a 20× difference. `rude_or_hostile` is the most prevalent sub-type (29 negative reviews), followed by `dismissive_or_condescending` (14).

---

## 3. Complaint Severity Is Higher in Negative Reviews

`complaint_severity` scores (1–5 scale) were assigned to 123 negative reviews but only 15 positive reviews, indicating the column primarily captures complaint intensity in dissatisfied reviews.

| Group | N scored | Mean severity | Severity ≥ 4 |
|---|---|---|---|
| Negative (`label_pos=0`) | 123 | **3.55** | 66 (54%) |
| Positive (`label_pos=1`) | 15 | 2.40 | 1 (7%) |

Negative reviews cluster at severity 3–4 (median = 4.0), while the few positive reviews that received a score averaged 2.4. **66 negative reviews (53% of all negatives) scored ≥ 4**, reflecting widespread intensity of dissatisfaction.

---

## 4. Staff Misconduct Amplifies Complaint Severity

Within negative reviews, staff behavior sub-types that involve active hostility or unprofessionalism correlate with higher severity scores than reviews where staff is not the issue:

| Staff Behavior (negative reviews only) | Mean Severity |
|---|---|
| `unprofessional` | 4.14 |
| `rude_or_hostile` | 4.10 |
| `discriminatory` | 4.00 |
| `dismissive_or_condescending` | 3.71 |
| `not_present` (other factors) | 3.24 |

Reviews where staff issues were flagged score ~0.5–0.9 points higher on average than reviews where the complaint stems from other factors (food quality, value, wait times, etc.).

---

## 5. Non-Staff Drivers of Negative Experiences

74 negative reviews (59%) carry `service_staff_behavior = not_present`, indicating that staff conduct alone does not explain all negative outcomes. These reviews average complaint severity 3.24 (still moderate-high), with 28/74 (38%) scoring ≥ 4. Textual review sampling reveals recurring themes in this group: **price increases/poor value**, **food quality disappointment**, and **mismatched expectations from prior high ratings**. These represent a second major causal cluster distinct from interpersonal service failures.

---

## 6. Summary of Key Factors

| Factor | Evidence Strength | Notes |
|---|---|---|
| **Rude/hostile staff** | ★★★★★ | 29 neg reviews; 4.1 avg severity; near-absent in positive reviews |
| **Dismissive/condescending staff** | ★★★★☆ | 14 neg reviews; 3.7 avg severity; exclusive to negatives |
| **High complaint severity (≥4)** | ★★★★☆ | 54% of negatives; only 7% of scored positives |
| **Unprofessional staff** | ★★★☆☆ | 7 neg reviews; highest avg severity (4.14) |
| **Non-staff issues (food, value, expectations)** | ★★★☆☆ | 59% of negatives lack staff flag; still moderate severity |

---

## Conclusion

Negative Yelp experiences are best explained by two broad factors: **(1) staff behavior failures**—particularly rude/hostile and dismissive conduct, present in 41% of negative reviews and almost absent from positive ones—and **(2) non-interpersonal complaints** (food quality, price/value mismatch, unmet expectations), which account for the remaining 59% of negatives. When staff issues are present, they consistently raise complaint severity, suggesting they convert dissatisfaction into intensely negative experiences. Interventions targeting staff training would address the highest-severity complaint tier, while product/pricing issues require a separate operational response.
