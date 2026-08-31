---
dataset: airlines_review
scenario: eda_rating_drivers
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "Overall Rating"
query: "Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?"
source_table: augment_table/airlines_review/eda_rating_drivers/haiku__skill_off_update.csv
generated_at: 2026-07-28T12:58:24.321726+00:00
wall_seconds: 94.32
---

# Airline Review Themes and Overall Rating Analysis
**Query:** Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?

**Dataset:** 900 reviews with ratings (1-10), 4 traveller types, 4 cabin classes, 7 review themes

---

## Executive Summary

**Staff Service** and **Inflight Entertainment** emerge as the strongest drivers of higher ratings across traveller types and classes. In contrast, **Value for Money** is consistently associated with lower ratings. **Seat Comfort** shows neutral sentiment and dominates reviews across all segments, while **Food & Beverages** demonstrates moderate positive association with ratings.

---

## 1. Overall Theme-Rating Associations

### Strong Positive Themes (Higher Ratings)
- **Staff Service**: +2.46 average rating impact (7.0 when mentioned vs. 4.5 when not) — most influential theme
- **Inflight Entertainment**: +1.73 rating impact (7.6 when mentioned vs. 5.8 when not) — 48.6% of high ratings mention this
- **Food & Beverages**: +1.33 rating impact (7.0 when mentioned vs. 5.6 when not) — appears in 72.9% of high ratings

### Neutral/Weak Positive Theme
- **Seat Comfort**: +0.57 rating impact (6.8 when mentioned vs. 6.3 when not) — dominant theme but weak sentiment driver

### Strong Negative Theme
- **Value for Money**: -2.08 rating impact (4.8 when mentioned vs. 6.9 when not) — **inverse correlation** with ratings
  - Present in 32.9% of low ratings but only 13.6% of high ratings
  - Signals customer dissatisfaction when explicitly discussed

---

## 2. Theme Distribution by Rating Level

| Theme | High Ratings (7-10) | Low Ratings (1-4) | Implication |
|-------|-------------------|-----------------|-------------|
| Staff Service | 88.6% | 66.3% | Widely cited positive driver (+22.3 pp) |
| Inflight Entertainment | 48.6% | 21.7% | Strong differentiator for satisfaction (+26.9 pp) |
| Food & Beverages | 72.9% | 50.8% | Mentioned more in positive reviews (+22.1 pp) |
| Seat Comfort | 49.1% | 38.8% | Prevalent but not discriminating (+10.3 pp) |
| Value for Money | 13.6% | 32.9% | **Dissatisfaction trigger** (-19.4 pp) |

---

## 3. Theme Patterns by Type of Traveller

### Solo Leisure Travelers (n=332, avg rating 6.87)
- **Highest impact theme**: Entertainment (7.55 avg rating when mentioned)
- **Dominant themes**: Seat Comfort (171 mentions), Staff Service (133)
- **Notable pattern**: Staff Service strong at 7.15; value concerns at 5.22
- **Interpretation**: Solo travelers prioritize service quality and entertainment options; price sensitivity evident

### Family Leisure Travelers (n=180, avg rating 6.57)
- **Highest impact theme**: Entertainment (8.12 avg rating when mentioned)
- **Dominant themes**: Staff Service (85), Seat Comfort (68)
- **Notable pattern**: Entertainment drives most satisfaction; value for money weaker (5.96)
- **Interpretation**: Family travelers most responsive to entertainment value; comfort and service equally important

### Couple Leisure Travelers (n=242, avg rating 6.37)
- **Highest impact theme**: Entertainment (7.13 avg rating when mentioned)
- **Dominant themes**: Seat Comfort (116), Staff Service (94)
- **Notable pattern**: Staff Service at 6.92; value concerns prominent at 4.70
- **Interpretation**: Lower average rating suggests pricing/value sensitivity; entertainment still differentiator

### Business Travelers (n=146, avg rating 5.99)
- **Highest impact theme**: Entertainment (7.65 avg rating when mentioned)
- **Dominant themes**: Staff Service (65), Seat Comfort (60)
- **Notable pattern**: **Lowest overall rating among traveler types**; staff service (6.42) and value (3.39) both weak
- **Interpretation**: Business travelers significantly more price-sensitive; service delivery misses expectations; entertainment secondary

---

## 4. Theme Patterns by Cabin Class

### Business Class (n=237, avg rating 7.10)
- **Strongest themes**: Staff Service (7.44), Entertainment (7.81), Food (7.30)
- **Premium advantage**: Staff service delivers +0.56 rating uplift vs. Economy
- **Notable**: Value for Money higher here (5.13 vs. 4.76 Economy)
- **Interpretation**: Premium cabin delivers on service; customers tolerate cost when quality aligns

### Economy Class (n=563, avg rating 6.37)
- **Strongest themes**: Entertainment (7.68), Food (6.95), Staff Service (6.88)
- **Value perception**: 4.76 when mentioned — persistent dissatisfaction despite lower fares
- **Interpretation**: Economy passengers seek entertainment/distractions and quality service; value perception remains problematic

### Premium Economy (n=86, avg rating 5.83)
- **Weakest performer overall** across themes
- **Notable weakness**: Seat Comfort at 5.76 (lowest among classes); value at 5.00
- **Interpretation**: Premium Economy passengers disappointed relative to expectations; positioning issue

### First Class (n=14, limited sample)
- **Highest average rating**: 7.93
- **Strongest themes**: Seat Comfort (9.22), Food (9.12)
- **Caveat**: Small sample size limits generalizability

---

## 5. Cross-Segment Insights: Type of Traveller × Class

### Business Class Premium Dynamics
- Solo Leisure + Business Class: 7.37 avg (highest solo segment)
- Couple Leisure + Business Class: 7.40 avg (highest couple segment)  
- Family Leisure + Business Class: 7.41 avg
- Business + Business Class: 6.21 avg (lowest business segment)

→ **Key finding**: Business class elevates leisure travelers significantly but fails to satisfy business travelers relative to their baseline

### Economy Class Vulnerability
- All traveler types score 6.0-6.7 in Economy
- Business travelers in Economy: 6.04 (lowest overall combination)
- Staff Service becomes critical differentiator in Economy across all traveler types

### Premium Economy Problem
- Lowest ratings in all traveler-class combinations (4.50-6.73 range)
- Business + Premium Economy: 4.50 (poorest performance)
- Suggests positioning confusion: premium price without premium delivery

---

## 6. Key Decision Points

**For Rating Enhancement by Segment:**

1. **Staff Service** (most leveraged across all segments):
   - 2.46-point rating impact
   - Non-negotiable for high ratings (88.6% of 7-10 ratings mention this)
   - Particularly critical in Economy and for Business travelers

2. **Entertainment** (segment-dependent lever):
   - Family travelers most responsive (8.12 avg when mentioned)
   - 26.9 percentage point difference between high and low ratings
   - Strong opportunity for differentiation across classes

3. **Value for Money** (inverse relationship):
   - Signals dissatisfaction when discussed (4.8 avg rating)
   - Business travelers most sensitive (3.39 rating)
   - Indicates pricing misalignment, especially in Premium Economy

4. **Seat Comfort** (presence required but insufficient):
   - Dominates 46% of reviews but only +0.57 rating impact
   - Necessary baseline requirement rather than satisfier
   - Weak point in Premium Economy (5.76 avg)

---

## Limitations and Caveats

- **Dominant theme attribution**: Analysis reflects coded primary themes; reviews discuss multiple aspects
- **Small subsamples**: First Class (n=14) and Business + Premium Economy (n=10) lack statistical power
- **Theme mention vs. sentiment**: Presence of theme doesn't capture sentiment polarity; seat comfort mentioned in both praise and complaints
- **Causality unclear**: Higher ratings may cause positive theme mentions rather than themes driving ratings
- **Value for Money context**: Inverse relationship suggests it's mentioned in complaint contexts rather than causally depressing ratings

---

## Conclusion

Across Type of Traveller and Class, **Staff Service quality** is the most universal driver of higher Overall Ratings (+2.46 impact), followed by **Inflight Entertainment** as a strong differentiator (+1.73 impact). **Seat Comfort** dominance in mention volume (46% of reviews) masks weak sentiment impact (+0.57), indicating it's a baseline requirement rather than a satisfier.

**Value for Money** shows inverse correlation with ratings, particularly acute for Business travelers (3.39 rating), signaling pricing/value perception problems. Leisure travelers benefit substantially from Business Class upgrades, while Business travelers remain disappointed even in premium cabins, suggesting unmet service expectations despite higher prices.

Premium Economy underperforms across all traveler types, indicating positioning or delivery misalignment relative to customer expectations.
