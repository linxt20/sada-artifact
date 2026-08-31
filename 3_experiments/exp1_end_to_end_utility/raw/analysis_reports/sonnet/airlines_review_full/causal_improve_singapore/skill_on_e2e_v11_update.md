---
dataset: airlines_review_full
scenario: causal_improve_singapore
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "overall_rating_recommendation"
query: "How can Singapore Airlines improve its overall rating and recommendation rate, especially on flights where passengers do not recommend it (Recommended = no)?"
source_table: augment_table/airlines_review_full/causal_improve_singapore/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-08-03T05:49:39.717925+00:00
wall_seconds: 108.37
---

# Singapore Airlines: Improving Overall Rating and Recommendation Rate

## Executive Summary

Singapore Airlines has a 64.3% recommendation rate (626 yes / 346 no, out of 972 reviews) and a mean overall rating of **6.5/10**. The 346 non-recommending passengers give a mean rating of only **2.8/10**, versus **8.6** for recommenders — a 5.8-point gap. Three structural drivers dominate: perceived **value for money**, **cabin class experience gaps** (premium class unmet expectations), and **crew service quality**. Disruption handling and ground service are secondary but addressable contributors.

---

## Method Note

TAPP-generated columns used in this analysis: `crew_service_quality`, `food_quality_issue`, `cabin_class_experience_gap`, `disruption_handling_quality`, `customer_service_resolution_quality`, `ground_service_quality`, `ife_quality`, `service_decline_perception`, `service_consistency_across_legs`. The column `seat_comfort_issue` was examined but found weak (structured Seat Comfort scores differ minimally between recommenders and non-recommenders; see below).

---

## 1. Outcome Variables and Overall Context

| Metric | All SQ | Not Recommended (n=346) | Recommended (n=626) |
|--------|--------|--------------------------|----------------------|
| Mean Overall Rating | 6.5 | 2.8 | 8.6 |
| Recommendation Rate | 64.3% | — | — |

**Trend:** Ratings and recommendation rates declined sharply in 2020–2021 (mean rating 4.4; rec. rate 28.6%), likely driven by COVID-era disruptions. Recovery is clear through 2022–2024 (mean 7.3; rec. rate 70.8% in 2024), but the 2019–2021 trough coincides with peak `service_decline_perception` signals (True rate: 33% in 2016–2019 reviews vs. <8% in 2020–2023 reviews — notably, `service_decline_perception` captures pre-COVID comparisons to remembered past standards, explaining its pre-2020 concentration).

---

## 2. Primary Driver: Value for Money

**Value For Money** has by far the strongest correlation with Overall Rating (r = **0.89**), compared to all other structured columns (Food & Beverages: 0.09, Staff Service: 0.07, Seat Comfort: 0.01, IFE: −0.04).

| Value For Money Score | Not Recommended | Recommended |
|-----------------------|-----------------|-------------|
| Mean VFM score | **1.80** | **4.35** |
| VFM ≤ 2 share | **74.3%** (257/346) | N/A |

74% of non-recommending passengers rated Value For Money at 1 or 2 out of 5. This is the single most potent lever. Passengers perceive that Singapore Airlines' price premium is not justified by the experience delivered, particularly in **Economy** (n=608, rec. rate 62.0%) and **Premium Economy** (n=95, rec. rate **56.8%** — the lowest of all classes).

---

## 3. Cabin Class Experience Gap (`cabin_class_experience_gap`)

| `cabin_class_experience_gap` | n (SQ total) | Mean Overall Rating |
|------------------------------|--------------|----------------------|
| meets_class_expectations | 5 | 9.25 |
| partial_gap | 120 (rec_no) | 5.55 |
| significant_gap_premium_class | 221 (rec_no) | **2.86** |

Among non-recommenders, **63.9% are flagged as `significant_gap_premium_class`**, versus only **5.1% of recommenders**. This facet is strongly cross-validated by Premium Economy's lowest recommendation rate (56.8%) and Business Class being third-worst (71.9%). Passengers boarding premium cabins with elevated expectations leave the most dissatisfied when product or service falls short.

**Implication:** Close the premium-class experience gap by ensuring seat hardware, meal quality, and proactive service match the cabin's price point — especially in Business Class and Premium Economy.

---

## 4. Crew Service Quality (`crew_service_quality`)

| `crew_service_quality` | Not Recommended (%) | Recommended (%) |
|------------------------|---------------------|-----------------|
| warm_proactive | 5.5% | **74.4%** |
| professional_neutral | 27.5% | 19.3% |
| robotic_impersonal | 7.8% | 3.4% |
| rude_dismissive | **57.2%** | 2.4% |

57% of non-recommenders experienced **rude or dismissive crew**, versus only 2.4% of recommenders. This is the sharpest binary split of any TAPP facet. Cross-check against structured **Staff Service** rating: non-recommenders score 3.80 vs. 4.02 for recommenders — a modest gap on the 1–5 scale, suggesting the structured Staff Service column partially but not fully captures this dimension. The `crew_service_quality` TAPP facet adds meaningful semantic resolution.

**Implication:** Targeted crew attitude and service recovery training, particularly focused on eliminating dismissive interactions, could substantially shift recommendation outcomes.

---

## 5. Disruption Handling (`disruption_handling_quality`)

Among the 346 non-recommenders, **144 (41.6%)** experienced a disruption. Of those, **138 (95.8%)** were coded as `poor_communication_or_no_support` — near-total failure in disruption management for this group. By contrast, among recommenders, 88.0% had `not_applicable` (no disruption).

**`customer_service_resolution_quality`** reinforces this: 71.4% of non-recommenders had `not_contacted` post-issue, and 26.6% had `refused_or_unresolved` — leaving zero with `resolved_satisfactorily`. No non-recommending passenger received a satisfactory resolution.

**Implication:** Proactive disruption communication (real-time updates, rebooking support) and post-flight complaint resolution are critical unmet needs. Even reactive-but-adequate handling (only 5 cases) outperforms silence.

---

## 6. Food Quality (`food_quality_issue`)

| `food_quality_issue` | Not Recommended (%) |
|----------------------|----------------------|
| Unknown / no data | 44.2% |
| poor_taste_or_presentation | **39.3%** |
| special_meal_failure | 6.9% |
| insufficient_options | 4.9% |
| praised_or_acceptable | 4.6% |

39% of non-recommenders with a food assessment experienced poor taste or presentation; 6.9% had special meal failures. Mean Food & Beverages rating: 3.40 (not recommended) vs. 3.63 (recommended). The gap is moderate but consistent — F&B improvements have incremental rather than transformative impact given the weak structural correlation with Overall Rating (r=0.09).

---

## 7. Ground Service (`ground_service_quality`)

Among non-recommenders: **26% experienced ground service issues** (ground staff unhelpful: 49; check-in/boarding failure: 30; lounge issues: 11). This is a secondary but real driver, particularly for Business/First Class passengers expecting lounge access and smooth boarding.

---

## 8. IFE and Seat Comfort: Weak Drivers

- **Inflight Entertainment** has a slightly *negative* correlation (r = −0.04) with Overall Rating, indicating it is not a meaningful driver of satisfaction/dissatisfaction. `ife_quality` shows high Unknown/not-applicable rates (83% of non-recommenders), confirming limited signal.
- **Seat Comfort** shows minimal gap (3.65 vs. 3.70 across recommender groups). `seat_comfort_issue` flags mostly `comfortable_no_issue` (78.6% of non-recommenders), confirming seat hardware is not a primary complaint driver.

---

## 9. Service Decline Perception (`service_decline_perception`)

**48.3% of non-recommenders** perceive a service decline (vs. 9.9% of recommenders). This TAPP flag correlates with lower Value For Money (mean VFM: 2.14 when True vs. 3.85 when False) and is concentrated in pre-2020 reviews (33% rate in 2016–2019 vs. <8% post-2021), suggesting these passengers are long-time SQ flyers comparing against a remembered higher standard. This segment requires reputation recovery through demonstrable product reinvestment.

---

## 10. Prioritized Recommendations

| Priority | Lever | Key Evidence |
|----------|-------|--------------|
| 🔴 **1. Value For Money** | Reprice or reinvest in product to justify fare premium | r=0.89 with rating; 74% of non-rec have VFM ≤ 2; mean 1.80 |
| 🔴 **2. Close premium class gap** | Align Business/Premium Economy product to expectations | `significant_gap_premium_class` = 63.9% of non-rec; Prem. Eco rec. rate 56.8% |
| 🔴 **3. Crew attitude** | Eliminate rude/dismissive interactions; reinforce warm-proactive service | 57% of non-rec have `rude_dismissive`; 74% of rec have `warm_proactive` |
| 🟡 **4. Disruption handling** | Proactive communication + post-flight resolution | 96% of disruption-affected non-rec got `poor_communication_or_no_support`; 0 resolved satisfactorily |
| 🟡 **5. Ground service** | Improve check-in, boarding, lounge experience | 26% of non-rec experienced ground failures |
| 🟢 **6. Food quality** | Improve taste consistency and special meal reliability | 39% of non-rec cite `poor_taste_or_presentation`; limited rating impact (r=0.09) |

---

*Analysis based on n=972 Singapore Airlines reviews. TAPP-generated columns used as supplementary semantic evidence; all major claims cross-validated against structured rating columns and outcome variables.*
