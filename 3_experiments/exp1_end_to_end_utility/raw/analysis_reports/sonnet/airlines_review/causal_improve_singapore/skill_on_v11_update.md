---
dataset: airlines_review
scenario: causal_improve_singapore
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "overall_rating_recommendation"
query: "How can Singapore Airlines improve its overall rating and recommendation rate, especially on flights where passengers do not recommend it (Recommended = no)?"
source_table: augment_table/airlines_review/causal_improve_singapore/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:03:54.437679+00:00
wall_seconds: 56.6
---

# Singapore Airlines: Improving Overall Rating & Recommendation Rate

**Dataset:** 900 verified reviews | 580 recommended (64.4%), 320 not recommended (35.6%)  
**Mean Overall Rating:** 6.53 / 10 (non-recommended: 2.77 | recommended: 8.61)

---

## 1. The Core Driver: Value for Money

The single largest gap between recommended and non-recommended passengers is **Value for Money** (mean 1.82 vs. 4.34, gap = **+2.52**). Among the 320 non-recommenders, **163 (51%) scored Value for Money at 1/5**, and 96% scored it ≤ 3. This is the primary lever to pull.

The augmented column `cabin_class_value_gap` confirms this: **92.8% of non-recommenders** were flagged as `premium_underdelivered`, while among passengers where `value_met`, only 1.9% did not recommend. Addressing the perceived value gap—particularly in Business and Premium Economy—is the highest-priority improvement.

---

## 2. Cabin Crew Service Quality

`cabin_crew_service_quality` is strongly associated with recommendation outcome:

| Crew Quality | % Not Recommended |
|---|---|
| `dismissive_or_rude` | **92.0%** |
| `inattentive_robotic` | 74.8% |
| `adequate_professional` | 39.0% |
| `attentive_proactive` | **1.9%** |

Among non-recommenders, only 8 (2.5%) had `attentive_proactive` crew. Shifting crew behavior from "adequate" to "attentive and proactive" is the clearest service-side intervention. Staff Service mean gap is modest (+0.21) but the tail-risk of dismissive behavior is severe.

---

## 3. Food & Beverage Issues

Food-related issues are a secondary but meaningful driver:

| Food Issue | % Not Recommended |
|---|---|
| `poor_taste_or_texture` | 71.8% |
| `wrong_or_missing_meal` | 68.9% |
| `insufficient_quantity_or_variety` | 48.3% |
| `no_issue` | 27.2% |

Mean Food & Beverages score gap is small (+0.23), but specific failure modes—wrong/missing meals and poor taste—have disproportionate impact on non-recommendation. Special meal service failure (True) also produces a 68.6% non-recommendation rate vs. 34.2% when False.

---

## 4. Service Consistency & Amenity Reductions

- **Service consistency decline** (True): 63.6% non-recommendation vs. 30.3% when stable — suggests passengers penalize perceived cuts or inconsistency.
- **Service amenity reduction** (significant): 83.3% non-recommendation vs. 24.3% when no reduction. Even minor reductions push the rate to 38.0%.
- **Loyalty program friction** (True): 75.8% non-recommendation vs. 34.0% when absent.

These findings suggest passengers are sensitive to *deterioration signals*—perceived cuts in amenities or program benefits trigger disproportionate dissatisfaction.

---

## 5. Cabin Class & Traveller Segment Risk

**Premium Economy has the highest non-recommendation rate (41.9%)**, followed by Economy (38.0%) and Business (28.3%). The `premium_underdelivered` pattern is most prevalent in non-recommenders across all classes, pointing to a consistent expectation gap rather than a class-specific anomaly.

Business travelers (40.4%) and Couples (40.1%) are more likely to not recommend than Solo Leisure travelers (30.1%), suggesting business and couple-segment expectations around value and consistency are harder to meet.

---

## 6. Prioritized Recommendations

| Priority | Action | Evidence Basis |
|---|---|---|
| **1** | Close the value-for-money perception gap, especially in Business/Premium Economy | `premium_underdelivered` in 92.8% of non-recommenders; VFM mean = 1.82 |
| **2** | Reduce dismissive/inattentive crew interactions through training | 92% non-rec rate for dismissive crew; 1.9% for proactive crew |
| **3** | Fix special meal fulfillment and food quality consistency | Wrong/missing meals → 68.9% non-rec; poor taste → 71.8% |
| **4** | Avoid or communicate service/amenity reductions carefully | Significant reductions → 83.3% non-rec |
| **5** | Address loyalty program friction points | Loyalty friction → 75.8% non-rec |

---

## Caveats & Weak Evidence

- **Inflight Entertainment** shows a negligible or slightly negative gap (-0.05) between recommended and non-recommended flights — it is not a differentiating factor.
- **Seat Comfort** gap is near zero (+0.03), suggesting physical product is not the primary complaint.
- The `Unknown` category in several augmented columns (5–7% of rows) limits full coverage but does not materially distort trends.
- Causal direction cannot be fully established from review data alone; low Value for Money scores may reflect post-hoc rationalization rather than independent causes.
