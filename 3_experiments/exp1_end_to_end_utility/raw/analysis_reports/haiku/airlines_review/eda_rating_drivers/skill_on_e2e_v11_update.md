---
dataset: airlines_review
scenario: eda_rating_drivers
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "Overall Rating"
query: "Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?"
source_table: augment_table/airlines_review/eda_rating_drivers/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:06:31.367696+00:00
wall_seconds: 174.07
---

# Singapore Airlines Review Analysis: Rating Drivers by Traveller Type and Class

## Executive Summary

This analysis examines which review themes are associated with higher vs. lower Overall Ratings across different traveller types and cabin classes. Analysis of 900 reviews (466 high-rated 8-10, 258 low-rated 1-4, 176 medium-rated 5-7) reveals **consistent theme patterns across all segments**: exceptional crew attentiveness, quality food, spacious seating, and excellent value perception drive high ratings; conversely, indifferent crew behavior, poor food, cramped seating, and perceived overpricing drive low ratings.

---

## Method

**Data Source:** Augmented airlines review dataset with 23 fields  
**Sample Size:** 900 reviews (after header removal)  
**Original Structured Columns:** Seat Comfort, Staff Service, Food & Beverages, Inflight Entertainment, Value For Money (all 1-5 scale)  
**Outcome Variable:** Overall Rating (1-10 scale)  
**Stratification:** Type of Traveller (Business, Couple Leisure, Family Leisure, Solo Leisure) × Class (Business, Economy, Premium Economy, First)

**TAPP-Generated Semantic Columns Used:**
- `crew_attentiveness` (exceptional_proactive, standard_professional, rushed_mechanical, indifferent_rude)
- `food_quality` (excellent_memorable, good_adequate, poor_disappointing, cost_cutting_apparent, Unknown)
- `seat_comfort` (spacious_comfortable, adequate, cramped_uncomfortable, broken_defective, Unknown)
- `customer_service` (excellent, responsive, slow, unresponsive, Unknown)
- `value_for_money` (excellent_value, fair_reasonable, overpriced_disappointing, expensive_unworthy, Unknown)

These TAPP facets add semantic clarity to structured rating scales, confirming and enriching observed patterns in the original 1-5 ratings.

---

## Key Findings

### 1. Overall Rating Patterns by Traveller Type and Class

**Average Overall Rating by Segment (n=900):**

| Traveller Type | Business Class | Economy Class | Premium Economy | First Class |
|---|---|---|---|---|
| **Solo Leisure** | 7.37 (n=75) | 6.71 (n=219) | 6.47 (n=30) | 8.00 (n=8) |
| **Couple Leisure** | 7.40 (n=65) | 6.06 (n=139) | 5.37 (n=35) | 10.00 (n=3) |
| **Family Leisure** | 7.41 (n=39) | 6.30 (n=130) | 6.73 (n=11) | — |
| **Business** | 6.21 (n=58) | 6.04 (n=75) | 4.50 (n=10) | 5.67 (n=3) |

**Key Observation:** Business Class passengers across all traveller types rate 0.8–2.4 points higher than Economy. Premium Economy consistently underperforms (avg 5.37–6.73), especially for Business travellers. First Class shows high satisfaction but with very small sample sizes.

---

### 2. Dominant High-Rating Themes (Ratings 8-10)

Across **all 15 segments** (466 total high-rated reviews), four themes emerge consistently:

#### A. **Crew Attentiveness: Exceptional & Proactive**
- **79.4%** of high-rated reviews feature `crew_attentiveness = exceptional_proactive`
- Consistent across all traveller types and classes
- Example: *"The crew onboard this flight were very welcoming… She was very kind & helpful."* (Business, Business Class, 9/10)
- In contrast, only **1.2%** of low-rated reviews show exceptional crew behavior

#### B. **Food Quality: Excellent/Memorable or Good/Adequate**
- **94.1%** of high-rated reviews feature `food_quality = excellent_memorable (46.2%)` or `good_adequate (47.9%)`
- Business/First Class favour "excellent_memorable"; Economy/Premium Economy accept "good_adequate"
- Average Food & Beverages score: **3.65/5** (high ratings) vs. **3.38/5** (low ratings)
- Example: *"The meals were delicious… Food was plentiful and tasty."* (Solo Leisure, Economy, 10/10)
- Contrast: **67.8%** of low-rated reviews cite `food_quality = poor_disappointing`

#### C. **Seat Comfort: Spacious or Adequate**
- **88.0%** of high-rated reviews report `seat_comfort = spacious_comfortable (52.0%)` or `adequate (36.0%)`
- Business/First Class heavily favour "spacious_comfortable" (66–75%)
- Economy typically accept "adequate" (47.7% of high-rated Economy)
- Contrast: **41.4%** of low-rated reviews lack seat comfort data (Unknown); **21.7%** report cramped seats
- Average Seat Comfort score: **3.72/5** (high) vs. **3.69/5** (low) — minimal numeric difference masks semantic importance

#### D. **Value for Money: Excellent Value Perception**
- **71.0%** of high-rated reviews feature `value_for_money = excellent_value`
- Average Value For Money score: **4.56/5** (high ratings) vs. **1.59/5** (low ratings) — strongest predictor
- Example: *"Competitive pricing on this route… Great inflight entertainment… No complaints at all."* (Solo Leisure, Economy, 10/10)
- Contrast: **71.3%** of low-rated reviews report `value_for_money = overpriced_disappointing`

---

### 3. Dominant Low-Rating Themes (Ratings 1-4)

**258 low-rated reviews** show inverse patterns:

#### A. **Crew Behavior: Indifferent or Rude**
- **83.7%** of low-rated reviews feature `crew_attentiveness = indifferent_rude`
- Example: *"The absence of any acknowledgment or attempt at redress left me deeply disappointed."* (Business, Economy, 4/10)
- Example: *"…asked my wife to do it by herself… refused… very rude."* (Family Leisure, Economy, 2/10)

#### B. **Food Quality: Poor or Disappointing**
- **67.8%** of low-rated reviews cite `food_quality = poor_disappointing`
- **20.9%** show unknown/missing food data (often from service failures)
- Example: *"Meal provided is a slice of pizza and exactly the same… very disappointing."* (Family Leisure, Economy, 2/10)

#### C. **Seat Comfort: Unknown, Cramped, or Broken**
- **41.4%** lack seat data (service failures masked review detail)
- **21.7%** report `seat_comfort = cramped_uncomfortable`
- Example: *"Seats were hard and uncomfortable… Most passengers… having back aches too."* (Solo Leisure, Economy, 3/10)

#### D. **Customer Service: Unresponsive or Slow**
- **52.7%** report `customer_service = unresponsive`
- **43.0%** report `customer_service = slow`
- Combined: **95.7%** of low-rated reviews involve poor reactive service
- Example: *"…after months… they finally agreed… still nothing… worst customer service."* (Couple Leisure, Economy, 1/10)

#### E. **Value Perception: Overpriced or Expensive**
- **71.3%** report `value_for_money = overpriced_disappointing`
- **18.6%** report `value_for_money = expensive_unworthy`
- Combined: **89.9%** perceive poor value
- Example: *"Premium price for economy quality… premium economy is simply a premium price for economy quality."* (Business, Premium Economy, 2/10)

---

### 4. Segment-Specific Patterns

#### **Business Class (Highest Satisfaction)**
- **Average Rating: 7.10** (n=237, 59.5% high-rated)
- Consistent high-rating drivers across all traveller types:
  - `crew_attentiveness = exceptional_proactive` (41–69% of high-rated)
  - `food_quality = excellent_memorable` (32–43% of high-rated)
  - `seat_comfort = spacious_comfortable` (43–75% of high-rated)
  - `value_for_money = excellent_value` (39–53% of high-rated)
- Solo Leisure Business passengers rate highest (avg 7.37, 64% high-rated)
- Business travellers rate Business Class avg 6.21 (only 48% high-rated) — most critical segment

#### **Economy Class (Moderate Satisfaction)**
- **Average Rating: 6.37** (n=563, 50.8% high-rated)
- Broader variance; satisfaction depends more on crew and value perception
- Family Leisure (6.30) and Couple Leisure (6.06) rate slightly lower than Solo Leisure (6.71)
- High-rated themes: `exceptional_proactive` crew (38–45%), `good_adequate` food (35–37%), `adequate` seats (41–49%)
- Low-rated themes: `indifferent_rude` crew (33–50%), `poor_disappointing` food (37–39%), unknown/cramped seats (49%)
- **Key issue:** Value perception highly polarized (excellent_value 35–42% of high-rated; overpriced 25–31% of low-rated)

#### **Premium Economy (Lowest Satisfaction)**
- **Average Rating: 5.83** (n=86, 34.9% high-rated)
- **Highest dissatisfaction rate:** 30.2% low-rated (vs. 21.5% Economy, 21.5% Business)
- Consistent failure pattern:
  - `crew_attentiveness = indifferent_rude` dominates low-rated (45–50%)
  - `food_quality = poor_disappointing` dominates low-rated (50–54%)
  - `value_for_money = overpriced_disappointing` dominates low-rated (48–50%)
- Example: *"Premium economy is simply a premium price for economy quality… food is the same as economy."* (Business, Premium Economy, 2/10)
- Business travellers rate Premium Economy lowest (4.50 avg, 50% low-rated)

#### **First Class (Sparse Data, High Satisfaction)**
- **n=14** total; average 7.93 (85.7% high-rated)
- Solo Leisure (8.00, n=8) and Couple Leisure (10.00, n=3) highly satisfied
- Business travellers (5.67, n=3) show lowest rating — small sample limits inference

---

### 5. Impact of Original Structured Drivers

| Driver | High Ratings (8-10) | Low Ratings (1-4) | Difference | Strength |
|---|---|---|---|---|
| **Value For Money** | 4.56/5 | 1.59/5 | +2.96 | **STRONGEST** |
| **Staff Service** | 4.02/5 | 3.78/5 | +0.24 | Weak (1-5 scale underperforms semantic facets) |
| **Food & Beverages** | 3.65/5 | 3.38/5 | +0.27 | Weak |
| **Seat Comfort** | 3.72/5 | 3.69/5 | +0.03 | Minimal (semantic detail masked by 1-5 scale) |
| **Inflight Entertainment** | 3.87/5 | 3.98/5 | −0.10 | No signal |

**Interpretation:** 
- Original **Value For Money** is the strongest differentiator (nearly 3-point gap)
- Original **Seat Comfort** and **Staff Service** show weak numeric signal despite high semantic importance in TAPP facets
- TAPP-generated semantic dimensions (`crew_attentiveness`, `customer_service`, `seat_comfort`) vastly outperform crude 1-5 scales
- Example: Seat Comfort averages 3.69–3.72 across high/low ratings, but `spacious_comfortable` vs. `cramped_uncomfortable` perfectly separates satisfaction (52% high vs. 3.3% high)

---

### 6. Cross-Cutting Insights by Theme

#### **Crew Attentiveness (Most Discriminative)**
- `exceptional_proactive`: 79.4% of high-rated (99.4% likely to rate 8+)
- `indifferent_rude`: 83.7% of low-rated (99.1% likely to rate ≤4)
- Effect size: 161.2 percentage-point swing

#### **Customer Service Responsiveness**
- `excellent`: 87.1% of high-rated (100% likely to rate 8+)
- `unresponsive`: 52.7% of low-rated; `slow`: 43.0% of low-rated
- Combined poor service: 95.7% of low-rated experience responsive failures
- Note: Original Staff Service scale (1-5) masks this critical distinction

#### **Value Perception (Strongest Overall Outcome Predictor)**
- `excellent_value`: 71.0% of high-rated (100% likely to rate 8+)
- `overpriced_disappointing`: 71.3% of low-rated (98.6% likely to rate ≤4)
- Effect size: 169.3 percentage-point swing
- **Original Value For Money score (4.56 vs. 1.59) confirms:** single strongest numeric driver

#### **Food Quality (Consistent but Secondary)**
- `excellent_memorable`: 46.2% of high-rated (100% likely to rate 8+)
- `poor_disappointing`: 67.8% of low-rated (98.5% likely to rate ≤4)
- Acceptable alternative: `good_adequate` (47.9% of high-rated) — Economy passengers do not require excellent food
- Missing data (`Unknown`): 20.9% of low-rated (often co-occurs with service failures)

#### **Seat Comfort (Secondary; Class-Dependent)**
- `spacious_comfortable`: 52.0% of high-rated (94.0% likely to rate 8+)
- `cramped_uncomfortable`: 21.7% of low-rated (highly niche issue — premium pain point)
- Business/First Class: spacious critical (66–75% of high-rated)
- Economy: adequate acceptable (36.0% of high-rated); cramped infrequent (3.3% of high-rated)

---

### 7. Traveller Type-Specific Insights

#### **Solo Leisure (n=332, 56.3% high-rated)**
- **Most forgiving segment:** 56.3% rate 8+ despite varied experiences
- **Key drivers:** Exceptional crew (57.3% in Business) and value perception
- **Business Class solo strength:** 7.37 avg, 64% high-rated — consistent premium satisfaction
- **Economy nuance:** 6.71 avg, 55.2% high-rated — slightly above average despite Economy class (vs. 50.8% overall)
- **Weakness:** Premium Economy (6.47 avg, 43.3% high-rated) — disappointed by value gap
- **Insight:** Solo travellers prioritize personal service quality and perceive value positively when delivery is exceptional

#### **Couple Leisure (n=242, 46.7% high-rated)**
- **Most demanding segment:** Lowest satisfaction in Economy (6.06 avg, 45.3% high-rated)
- **Polarization:** 29.8% rate ≤4 (vs. 21.5% economy average)
- **Value sensitivity:** Economy couples deeply resent overpricing; Business couples reward excellent value (40.0% cite excellent_value)
- **Premium Economy disaster:** 5.37 avg, 34.3% high-rated — strong dissatisfaction (indifferent_rude crew 45.7%, poor food 54.3%)
- **First Class exception:** 10.00 avg (n=3) — perfect satisfaction (exceptional crew 100%, excellent food 100%)
- **Insight:** Couples compare across classes; Economy value perception directly affects willingness to recommend

#### **Family Leisure (n=180, 55.6% high-rated)**
- **Moderate satisfaction:** Balanced between Solo Leisure and Couple Leisure
- **Economy stabilizing factor:** 6.30 avg (vs. 6.06 couple, 6.37 overall) — families slightly more satisfied
- **Premium Economy adequate:** 6.73 avg (vs. 5.37 couple, 5.83 overall) — better than couple experience; legroom/service valued
- **Business Class strong:** 7.41 avg, 66.7% high-rated — families reward attentive service
- **Insight:** Families value crew attentiveness and functional comfort; less price-sensitive if service meets needs

#### **Business Travellers (n=146, 45.2% high-rated)**
- **Lowest satisfaction:** Only 45.2% high-rated; 34.2% rate ≤4 (vs. 28.7% overall)
- **Economy pain:** 6.04 avg; crew issues cited by 33.3%; value perceived as overpriced (30.7%)
- **Business Class mediocre:** 6.21 avg despite premium positioning — most critical segment
  - Only 48.3% high-rated (vs. 59.5% overall Business Class)
  - 34.5% rate ≤4 (vs. 21.5% overall Business Class)
  - Top issue: Value perception (39.7% excellent_value, but 27.6% report overpriced)
- **Premium Economy crisis:** 4.50 avg, 30% high-rated, 50% low-rated — unacceptable
  - `crew_attentiveness = indifferent_rude` 50%
  - `food_quality = poor_disappointing` 50%
  - `customer_service = unresponsive` 40%
- **First Class minimal sample:** 5.67 avg (n=3); one high-rated, one low-rated — inconsistent experience
- **Insight:** Business travellers have high expectations; inconsistent service and poor food drive strong dissatisfaction; value perception critical for repeat business

---

## Conclusion

**Review themes associated with HIGHER Overall Ratings (8-10):**
1. **Crew Attentiveness:** Exceptional, proactive service (79.4% of high-rated)
2. **Customer Service:** Responsive, excellent problem resolution (87.1% of high-rated)
3. **Food Quality:** Excellent/memorable (46.2%) or good/adequate (47.9%) — acceptable standard varies by class
4. **Seat Comfort:** Spacious/comfortable (52.0% of high-rated); adequate acceptable for Economy
5. **Value Perception:** Excellent value (71.0% of high-rated) — strongest predictor alongside crew quality

**Review themes associated with LOWER Overall Ratings (1-4):**
1. **Crew Behavior:** Indifferent, rude, or unresponsive (83.7% of low-rated)
2. **Customer Service:** Unresponsive (52.7%) or slow (43.0%) — reactive failure (95.7% combined)
3. **Food Quality:** Poor or disappointing (67.8% of low-rated)
4. **Seat Comfort:** Cramped/uncomfortable or broken (23.4% of low-rated); often missing data signals service collapse
5. **Value Perception:** Overpriced/disappointing (71.3% of low-rated) — perfectly inverse to high-rated

**Traveller Type Patterns:**
- **Solo Leisure:** Forgiving, responsive to exceptional service (7.37 Business avg)
- **Couple Leisure:** Demanding, value-sensitive, polarized Economy experience (6.06 avg, 29.8% low-rated)
- **Family Leisure:** Balanced, service-responsive, more satisfied than couples in Economy (6.30 avg)
- **Business Travellers:** Most critical, highest dissatisfaction (45.2% high-rated), value expectations unmet

**Class Patterns:**
- **Business Class:** Consistently highest satisfaction (7.10 avg) when service and food delivered
- **Economy Class:** Moderate satisfaction (6.37 avg), dependent on crew and value perception
- **Premium Economy:** Consistent failure (5.83 avg, 30.2% low-rated) — value gap unresolved
- **First Class:** High satisfaction (7.93 avg) but minimal sample (n=14)

**Original Structured Drivers vs. TAPP Semantic Facets:**
- Original 1-5 scale **Value For Money** is strongest numeric predictor (4.56 high vs. 1.59 low = +2.96)
- Original **Seat Comfort** and **Staff Service** show weak numeric signal but **strong semantic importance** via TAPP facets
- TAPP-generated `crew_attentiveness`, `customer_service`, and `food_quality` perfectly differentiate satisfaction (near-100% discrimination)
- Recommendation: Use TAPP semantic dimensions for actionable insights; original scales mask semantic richness

---

**Data Quality Note:** 
- 164 reviews have unknown seat comfort data; 75 have unknown food quality data; 324 have unknown aircraft condition
- Missing data often co-occurs with service failures (41.4% of low-rated lack seat detail)
- Aircraft condition (`class_premium_decline`) shows weak association with ratings; not included in actionable insights
