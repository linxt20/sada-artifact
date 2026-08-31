---
dataset: airlines_review_full
scenario: prediction_cathay_rating_model
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating_gt7"
query: "(Cathay MD) Build a model to organise/optimise routes and service so Overall Rating > 7."
source_table: augment_table/airlines_review_full/prediction_cathay_rating_model/sonnet__skill_off_update.csv
generated_at: 2026-08-03T05:42:38.457687+00:00
wall_seconds: 52.89
---

# Cathay Pacific: Model to Achieve Overall Rating > 7

**Dataset:** 744 verified/unverified reviews of Cathay Pacific Airways  
**Target:** Overall Rating > 7 (currently achieved in **46.8%** of reviews; median = 7, mean = 6.17)

---

## 1. Key Predictors of Overall Rating

| Feature | Correlation with Overall Rating |
|---|---|
| Value For Money | **+0.877** |
| Composite_Service_Score | +0.730 |
| Value_Gap | −0.717 |
| Seat Comfort | +0.156 |
| Staff Service | +0.110 |
| Food & Beverages | +0.109 |
| Inflight Entertainment | +0.089 |

**Value For Money (VFM)** is the dominant driver by a wide margin. Service dimensions individually are weak predictors but compound into the `Composite_Service_Score`, which is the second-strongest signal.

---

## 2. Critical Thresholds

### Value For Money
| VFM Score | % Reviews Achieving Rating > 7 | Count |
|---|---|---|
| 1–2 | 0% | 225 |
| 3 | 17% | 122 |
| 4 | 70% | 181 |
| **5** | **93%** | 216 |

**Implication:** VFM ≥ 4 is a near-necessary condition. No review with VFM ≤ 2 achieved Overall > 7.

### Composite Service Score (CSS)
| CSS Band | % Reviews > 7 | Count |
|---|---|---|
| < 1.5 | 0% | 22 |
| 1.5–2.5 | 4% | 173 |
| 2.5–3.5 | 51% | 401 |
| **> 3.5** | **92%** | 148 |

CSS > 3.5 combined with VFM ≥ 4 is the target operating zone.

---

## 3. Route & Service Segmentation

### By Cabin Class × Haul Type (% achieving Rating > 7)
| Class | Short/Medium-haul | Long-haul |
|---|---|---|
| First Class | **75%** | 42% |
| Business Class | **63%** | 55% |
| Economy Class | **52%** | 34% |
| Premium Economy | 30% | 43% |

- **Short/medium-haul routes outperform long-haul** for most cabin classes — likely because passenger expectations on duration are easier to meet.  
- **Economy long-haul is the weakest segment** (34%) and represents the largest volume (398 long-haul reviews vs 346 short/medium).
- **Premium Economy short/medium-haul anomaly (30%)**: underperforms Economy in the same haul band — a potential pricing/value mismatch worth investigating.

### By Route Performance Tier
| Tier | Mean Rating | Count |
|---|---|---|
| High | 9.2 | 173 |
| Medium | 6.6 | 393 |
| Low | 2.3 | 178 |

The Low tier (178 routes) is dragging the overall average significantly. Prioritising these routes for intervention would yield the fastest aggregate improvement.

---

## 4. Improvement Priority Analysis

| Priority Tag | Mean Rating | Count |
|---|---|---|
| Maintain | **9.1** | 348 |
| Price/Value Reset | **2.4** | 225 |
| Staff Service Uplift | 5.2 | 45 |
| Seat/Comfort Upgrade | 5.3 | 32 |
| Value For Money Enhancement | 4.9 | 50 |
| F&B Improvement | 4.9 | 27 |

**Price/Value Reset** is the single largest actionable cluster (225 reviews, mean 2.4). These are routes/cabins where passengers feel overcharged relative to what was delivered. Addressing pricing or tangibly improving the product on these routes is the highest-leverage action.

### Weakest Dimension (when not VFM)
When VFM is not the weakest dimension, **Value For Money still dominates** the low-rating pool (mean 3.1 for those flagged). For reviews flagged on other dimensions (Staff, F&B, Seat Comfort, IFE), mean ratings sit between 6.6–6.9 — close to the >7 threshold — suggesting these are **incremental improvements** rather than existential issues.

---

## 5. Traveller Segment
| Traveller Type | Mean Rating | Count |
|---|---|---|
| Solo Leisure | 6.7 | 328 |
| Family Leisure | 6.0 | 128 |
| Business | 5.8 | 129 |
| Couple Leisure | 5.6 | 159 |

Solo leisure travellers rate highest. Business travellers rate lower than expected given cabin class mix — reinforcing the value perception gap.

---

## 6. Decision-Ready Model: Rules for Rating > 7

A simple rule-based model derived from the data:

```
IF Value_For_Money >= 4
   AND Composite_Service_Score >= 2.5
   → ~70–92% probability of Overall Rating > 7

IF Value_For_Money <= 2
   → Overall Rating > 7 is essentially impossible (0% in data)

IF Route_Performance_Tier == "Low"
   → Priority intervention required (mean 2.3)
```

**Recommended route/service optimisation actions:**

1. **Price/Value alignment (highest priority):** 225 reviews are tagged "Price/Value Reset." Either reprice affected cabins/routes or materially upgrade the product offering to justify current fares.
2. **Long-haul Economy uplift:** Largest volume segment with only 34% achieving >7. Seat comfort, food, and staff ratios should be targeted.
3. **Premium Economy repositioning:** Short/medium-haul Premium Economy underperforms Economy (30% vs 52%) — examine if the product differentiation is sufficient.
4. **Protect "Maintain" routes:** 348 reviews already at mean 9.1 — these routes are operating well; avoid cost-cutting that could erode performance.
5. **Staff service on medium-tier routes:** CSS 2.5–3.5 converts to >7 only 51% of the time; staff service uplift could push borderline routes into the High tier.

---

## 7. Caveats & Weak Evidence

- Individual service dimension correlations (0.09–0.16) are weak — they contribute through the composite score but are not individually decisive. Do not over-invest in single-dimension fixes (e.g., IFE alone will not move the needle).
- The `High_Rating_Potential` flag paradoxically shows **0% achieving >7** (92 reviews) — this column appears to be a forward-looking intervention flag, not a descriptor of current performance. It should not be used as a predictor.
- Review counts for First Class (n=16) are too small for robust conclusions.
- External disruptions (weather diversions, delays) appear in low-rated reviews but cannot be systematically modelled from this data alone.
