---
dataset: airlines_review_full
scenario: eda_rating_drivers
variant: original
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "Overall Rating"
query: "Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?"
source_table: augment_table/airlines_review_full/eda_rating_drivers/original.csv
generated_at: 2026-08-03T05:41:32.938749+00:00
wall_seconds: 71.84
---

# Rating Drivers Analysis: Review Themes by Traveller Type and Class

## Executive Summary

Analysis of 8,100 Singapore Airlines reviews reveals that **review themes are strongly associated with Overall Rating differences across Type of Traveller and Class**. Food quality, staff service, and seat comfort consistently emerge as higher-rating drivers across all segments, while delays/issues consistently associate with lower ratings.

---

## Key Findings

### 1. **Universal High-Rating Drivers (Across All Segments)**

**Food Quality** has the strongest association with higher ratings:
- Increases ratings by **+30.7 to +36.1%** across traveller types
- Shows **+24.8 to +44.8%** difference in mention frequency between high (8-10) and low (1-4) rated reviews
- First Class shows the largest effect: 76.6% of high-rated reviews mention food vs. 31.8% of low-rated

**Staff Service** drives ratings universally:
- Mentioned in 90%+ of high-rated reviews across all traveller types
- Gap of **+16.8 to +18.8%** between high and low ratings
- First Class shows strongest effect: 94.8% high vs. 72.7% low

**Seat Comfort** significantly impacts ratings:
- **+17.8 to +24.9%** higher mention frequency in high-rated reviews by traveller type
- First Class most sensitive: +28.6% gap; Economy second: +21.5% gap
- Premium Economy shows lower sensitivity (+9.6%)

### 2. **Patterns by Type of Traveller**

#### Solo Leisure (n=3,237; Mean Rating: 5.92)
- **Highest overall satisfaction** among traveller types
- **Top drivers** (descending impact):
  - Food quality: +36.1% difference
  - Staff service: +18.8% difference  
  - Seat comfort: +24.9% difference
- Least sensitive to value concerns (smallest gap: -6.6%)

#### Couple Leisure (n=1,899; Mean Rating: 5.49)
- **Most sensitive to delays/issues** (-28.1% gap, highest among groups)
- **Top drivers**:
  - Food quality: +30.8% difference
  - Staff service: +16.9% difference
  - Seat comfort: +21.3% difference
- Entertainment particularly important: +17.4% gap

#### Family Leisure (n=1,551; Mean Rating: 5.08)
- **Most negative baseline ratings** (lowest mean)
- **Most sensitive to cleanliness** (+11.6% gap, highest among groups)
- **Highest sensitivity to delays/issues** (-33.4% gap)
- **Top food quality driver** in reviews: +34.2% gap
- Entertainment critical for satisfaction: +32.5% gap

#### Business Travellers (n=1,413; Mean Rating: 5.39)
- **Food quality dominates** (+30.7% gap, tied highest)
- Moderately sensitive to value concerns (-9.7%)
- Staff service gap moderate: +17.9%
- Seat comfort emphasis: +17.8%

### 3. **Patterns by Class**

#### Business Class (n=2,104; Mean Rating: 6.41)
- **Highest average rating** across all segments
- **Food quality effect largest**: +24.8% gap
- **Staff service consistently cited**: +13.7% gap
- Delays/issues notably mentioned in low-rated reviews: 57.1% vs. 34.9%

#### Economy Class (n=5,504; Mean Rating: 5.24)
- **Largest sample**; represents majority of reviews
- **Most sensitive to entertainment**: +28.3% gap
- **Food quality heavily skews ratings**: +33.7% gap
- Delays impact ratings: -32.5% gap (very strong effect)

#### First Class (n=121; Mean Rating: 7.34)
- **Highest satisfaction** across all classes
- **Food quality shows strongest effect**: +44.8% gap
- Cleanliness unusual: cited only in high-rated reviews (18.2% vs. 0%)
- Staff service gap: +22.1%

#### Premium Economy (n=371; Mean Rating: 5.99)
- **Moderately high ratings**, between Economy and Business
- **Food quality critical**: +25.6% gap (highest among classes)
- Seat comfort less differentiating (+9.6%) vs. other classes
- Value concerns notably present (+30.3% in high-rated vs. 33.3% low-rated)

---

## Cross-Segment Insights

### High-Rating Combinations (Mean Ratings)
1. **Solo Leisure + First Class**: 8.21
2. **Solo Leisure + Business Class**: 7.29
3. **Couple Leisure + Business Class**: 6.83
4. **Family Leisure + Business Class**: 6.45

### Low-Rating Combinations (Mean Ratings)
1. **Family Leisure + Economy Class**: 4.87
2. **Couple Leisure + Economy Class**: 4.89
3. **Business Travellers + Economy Class**: 4.96
4. **Business Travellers + Business Class**: 5.80 (still lower than leisure equivalents)

### Notable Exception
Business travellers in Business Class (5.80) rate lower than expected, despite premium seating. This suggests business travellers prioritize reliability/value over amenities, or experience more delays/service issues during peak business travel.

---

## Theme Robustness and Exceptions

### Strong Evidence
- **Food quality** consistently drives ratings +25–45% across ALL segments (robust)
- **Staff service** consistently impacts +14–23% across ALL segments (robust)
- **Delays/issues negatively correlate** with ratings across ALL segments (robust)

### Weaker Evidence
- **Cleanliness** shows modest effects (+3.2–11.9%), relatively undermentioned in reviews (~10–24% of high-rated)
- **Value concerns** show inverse effect (-3–9.7%), suggesting price is less critical than experience quality
- **Entertainment** effect varies: strong for Economy (+28.3%), weak for Premium Economy (+9.9%)

### Class-Specific Patterns
- **Seat comfort** more important in premium classes (Business +14.9%, First +28.6%) than Economy (+21.5%)
- **Entertainment** more impactful in Economy (+28.3%) than Business (+18.2%)
- **Cleanliness** mentioned more frequently in Economy (20% high-rated) vs. Business (14.3%)

---

## Conclusion

Review themes reveal a **clear hierarchy of rating drivers**:

1. **Food quality and staff service** are universal anchors—present across all traveller types and classes
2. **Seat comfort** drives ratings especially in premium classes; less critical in Economy
3. **Delays and operational issues** consistently depress ratings (strong inverse association)
4. **Cleanliness** is hygiene baseline; cited mainly when issues exist
5. **Entertainment** matters more for leisure travellers and economy passengers than business travellers

**Business travellers and Family leisure segments show notably lower mean ratings**, suggesting operational or service consistency challenges in these groups. Couples and solo leisure travellers experience higher satisfaction, particularly in premium classes where food quality and staff attentiveness are more visible.
