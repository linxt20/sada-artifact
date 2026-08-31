---
dataset: airlines_review
scenario: eda_rating_drivers
variant: original
model: substrate-claude-haiku-4-5
query_subtype: exploratory_data_analysis
focus_variable: "Overall Rating"
query: "Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?"
source_table: augment_table/airlines_review/eda_rating_drivers/original.csv
generated_at: 2026-07-26T12:50:44.681105+00:00
wall_seconds: 199.86
---

# EDA: Review Themes Associated with Overall Rating by Traveller Type and Class

## Executive Summary

This analysis examines 900 Singapore Airlines reviews to identify which review themes are associated with higher versus lower Overall Ratings across different passenger segments. The key finding is that **Staff Service quality is the strongest predictor of positive ratings** across all segments, while **Value for Money and Seat Comfort** are critical dissatisfaction drivers. Theme prevalence varies significantly by traveller type and class.

## Key Findings

### 1. Overall Theme Patterns: High vs. Low Ratings

**High Ratings (9-10, n=364 reviews):**
- Staff Service: 93.4%
- Inflight Entertainment: 83.5%
- Food & Beverages: 76.9%
- Seat Comfort: 63.2%

**Low Ratings (1-3, n=222 reviews):**
- Inflight Entertainment: 70.3%
- Staff Service: 66.2%
- Food & Beverages: 50.5%
- Value for Money: 41.9%

**Critical Insight:** Staff Service appears in 93.4% of high-rated reviews but only 66.2% of low-rated reviews. The difference is qualitative: high ratings emphasize exemplary crew attentiveness; low ratings cite inattentiveness or dismissiveness.

### 2. Themes by Type of Traveller

**Solo Leisure (n=332, avg rating 6.8)**
- High (n=145): Staff Service 92.4%, Inflight Entertainment 87.6%, Food 79.3%
- Low (n=65): Inflight Entertainment 73.8%, Staff Service 67.7%, Food 52.3%

**Family Leisure (n=180, avg rating 6.6)**
- High (n=78): Staff Service 94.9%, Inflight Entertainment 78.2%, Food 75.6%
- Low (n=48): Inflight Entertainment 72.9%, Staff Service 60.4%, Seat Comfort 50.0%
- Notable: Families notably more sensitive to seat comfort in negative reviews (50% vs ~42% other segments)

**Business Travelers (n=146, avg rating 6.1 - lowest)**
- High (n=50): Staff Service 92.0%, Food 78.0%, Inflight Entertainment 76.0%
- Low (n=43): Staff Service 74.4%, Inflight Entertainment 65.1%, Value for Money 55.8%
- Key: Business travelers most price-sensitive (55.8% low ratings cite value vs 28-41% for leisure)

**Couple Leisure (n=242, avg rating 6.8)**
- High (n=91): Staff Service 94.5%, Inflight Entertainment 85.7%, Food 73.6%
- Low (n=66): Inflight Entertainment 68.2%, Staff Service 63.6%, Seat Comfort 56.1%

### 3. Themes by Class

**Economy Class (n=563, avg rating 6.4)**
- High (n=221): Staff Service 94.6%, Inflight Entertainment 83.3%, Food 73.8%
- Low (n=158): Inflight Entertainment 66.5%, Staff Service 63.3%, Food 42.4%
- Largest segment; highest dissatisfaction count (158 low-rated reviews)

**Business Class (n=237, avg rating 6.9)**
- High (n=113): Staff Service 93.8%, Inflight Entertainment 84.1%, Food 81.4%
- Low (n=42): Inflight Entertainment 78.6%, Staff Service 76.2%, Food 69.0%

**Premium Economy (n=86, avg rating 5.8 - lowest)**
- High (n=21): Staff Service 90.5%, Food 85.7%, Inflight Entertainment 81.0%
- Low (n=21): Inflight Entertainment 81.0%, Seat Comfort 76.2%, Food 76.2%
- Critical: 50% parity between high/low ratings suggests inconsistent quality perception
- Themes suggest "premium pricing without premium quality" perception, particularly for seat comfort

**First Class (n=11, avg rating 7.5)**
- High (n=9): Inflight Entertainment 88.9%, Seat Comfort 77.8%, Food 77.8%
- Low (n=1): Sparse data; insufficient for inference

### 4. Component Rating Correlation with Overall Rating

**High-Rated Reviews average component scores:**
- Value For Money: 4.67/5 (93%)
- Staff Service: 4.0/5 (80%)
- Inflight Entertainment: 3.94/5 (79%)
- Seat Comfort: 3.74/5 (75%)
- Food & Beverages: 3.64/5 (73%)

**Low-Rated Reviews average component scores:**
- Value For Money: 1.48/5 (30%) - extreme dissatisfaction
- Staff Service: 3.74/5 (75%)
- Inflight Entertainment: 3.98/5 (80%)
- Seat Comfort: 3.71/5 (74%)
- Food & Beverages: 3.36/5 (67%)

**Key insight:** Value for Money is most discriminative (4.67 vs 1.48 = 214% gap). Pricing/fee concerns dominate among detractors.

### 5. Segment-Specific Patterns (Traveller Type x Class)

Business travelers in Premium Economy rate lowest (4.50 avg), with 55.8% of low-rated reviews citing value concerns - suggesting this class fails to justify premium positioning for business passengers. Family leisure travelers are notably more sensitive to seat comfort degradation (50% of low ratings mention it vs ~42% for other leisure types). Solo leisure travelers show most consistent satisfaction across class tiers.

## Weak Evidence and Caveats

1. **First Class sample size (n=11)** too small for reliable patterns. Couple Leisure First Class (n=3) shows perfect 10.0 rating, but may reflect selection bias rather than service quality.

2. **Inflight Entertainment paradox:** Low-rated reviews mention IFE frequently (70.3%) yet component scores moderate (3.98/5). Reviewers complain about system functionality (WiFi failures, limited content selection) rather than entertainment concept failures.

3. **Seat Comfort component stability:** Scores remain stable (3.7-3.8) across high and low-rated reviews despite frequent theme mentions. The 5-point scale may not capture qualitative seat design issues (recline mechanisms, footrest support, ergonomic padding).

4. **Cleanliness and Baggage Handling:** Infrequent in theme analysis (less than 20%) but represent critical pain points when mentioned, suggesting they occur in subset of experiences but have outsized impact.

## Recommendations by Segment

**Solo Leisure travelers:** Prioritize staff attentiveness training and IFE system reliability  
**Family Leisure travelers:** Address seat comfort ergonomics; maintain staff service excellence  
**Business travelers:** Improve pricing transparency and value-for-money perception; evaluate Premium Economy positioning  
**Economy Class:** Focus on staff service consistency and Inflight Entertainment functionality  
**Premium Economy:** Establish clear value differentiation through dedicated amenities and demonstrable seat comfort improvements

## Conclusion

**Staff Service excellence** is the universal high-rating driver (93.4% of high-rated reviews) across all traveller types and classes. **Value for Money** is the most discriminative dissatisfaction driver (4.67 vs 1.48 rating = 214% gap between high and low reviews).

Theme patterns vary meaningfully by segment:
- Business travelers prioritize value transparency; 55.8% of their negative reviews cite pricing/fee concerns
- Family leisure travelers prioritize seat comfort; 50% of their low-rated reviews mention seating issues
- Solo leisure travelers show most consistent satisfaction trajectory across class options

Singapore Airlines' service reputation is reflected in high staff service mention rates, but pricing transparency and seat comfort - especially in Premium Economy and Economy classes - represent key improvement opportunities for increasing overall satisfaction ratings.
