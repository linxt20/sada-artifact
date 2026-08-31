---
dataset: airlines_review_full
scenario: causal_qatar_business
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "non_recommendation_outcome"
query: "Explain why some Qatar Airways Business-Class flights receive a non-recommended (Recommended = no) result."
source_table: augment_table/airlines_review_full/causal_qatar_business/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-08-03T05:51:23.845254+00:00
wall_seconds: 168.21
---

# Analysis: Why Some Qatar Airways Business-Class Flights Receive Non-Recommended Ratings

## Executive Summary

Of 592 Qatar Airways Business-Class reviews, 127 (21.5%) receive a non-recommended rating. The primary driver is **perceived poor value for money** (mean 2.2/5.0), which co-occurs with three reinforcing factors: (1) aircraft product downgrades or changes without refund, (2) inconsistent or rude crew service, and (3) ground service failures. Approximately 81% of non-recommended reviews cite pricing/value concerns, while major gaps between expectation and reality occur in 80% of cases.

---

## Method Note

This analysis uses both original structured columns and TAPP-generated semantic facets. The following augmented columns are cited in this report:
- **aircraft_product_mismatch**
- **ground_service_quality**
- **food_beverage_quality**
- **crew_service_consistency**
- **seat_comfort_privacy**
- **pricing_value_mismatch**
- **pricing_and_value_mismatch**
- **expectation_gap**
- **expectation_versus_reality_gap**
- **ife_connectivity_issues**
- **seat_comfort_and_privacy**

These TAPP columns provide structured semantic interpretation of textual review content, used to corroborate and extend findings from numeric ratings.

---

## 1. Value-for-Money: The Critical Driver (Primary Factor)

**Finding:** Poor value perception is the dominant factor in non-recommendation, appearing in 102/127 non-recommended reviews (80.3%).

| Metric | Non-Recommended | Recommended | Difference |
|--------|-----------------|------------|-----------|
| Value For Money (mean, 1–5 scale) | 2.22 | 4.29 | -2.07 |
| Rating ≤ 2 ("Poor"/1) | 49 reviews (38.6%) | — | — |

**TAPP Corroboration:** The `pricing_value_mismatch` column shows:
- **Expensive for service level:** 76/127 non-recommended reviews (59.8%)
- **Downgrade with no refund:** 26/127 (20.5%)
- **Seat fees not honored:** 6/127 (4.7%)

**Insight:** Qatar Airways Business-Class passengers explicitly perceive their ticket price as unjustified, especially when product quality or service falls short of premium expectations. This dissatisfaction is **not driven by baseline seat comfort alone** but by the gap between premium pricing and delivered value.

---

## 2. Aircraft Product Mismatch & Downgrades (Second Factor)

**Finding:** 51/127 non-recommended reviews (40.2%) involve aircraft or seating downgrades, typically triggered last-minute without compensation.

**TAPP Breakdown (`aircraft_product_mismatch`):**
- **Product downgrade:** 29 reviews (23%)
- **Aircraft changed without notice:** 22 reviews (17%)
- **Expected QSuite received older config:** 9 reviews (7%)
- **Consistent product (as booked):** 50 reviews (39%)

**Combined Impact with Pricing:** Among downgrade cases (n=51), 43 (84%) also cite expensive-for-service pricing. These reviews report:
- Booking QSuite seats, arriving at aircraft with 2-2-2 seating (dated, uncomfortable)
- No advance notification or refund offered
- Comparable or higher ticket price despite inferior product
- Average overall rating: **4.2/10** (severe dissatisfaction)

**Example Themes from Reviews:**
> "Changed aircraft to old 777 without Qsuites...charged same price...offered ridiculous 10k avios ($100) compensation"

> "Booked Q-Suite, downgraded to old 2-2-2 config at last minute, refused partial refund or seat fee reimbursement"

The **expectation_versus_reality_gap** (TAPP) shows "major disappointment" in 51/127 reviews (40.2%), with average value-for-money rating of just 1.8/5 in these cases.

---

## 3. Crew Service Inconsistency & Rudeness (Third Factor)

**Finding:** 53/127 non-recommended reviews (41.7%) report rude, passive-aggressive, or inattentive crew behavior.

**TAPP Evidence (`crew_service_consistency`):**
- **Rude or inattentive:** 53 reviews (41.7%)
- **Inconsistent service:** 26 reviews (20.5%)
- **Slow service:** 12 reviews (9.4%)
- **Good standard:** 27 reviews (21.2%)

**Paradox Observed:** Despite 70/127 non-recommended reviews rating Staff Service at 5/5, the semantic TAPP column detects 53 cases of poor crew conduct. This suggests:
- Some customers give "5/5" out of politeness or because individual crew members were kind
- The textual narrative reveals systemic issues (e.g., "crew were friendly but passive-aggressive," "some attendants exceptional, others sullen")

**Combined Impact with Value:** 41/53 rude-crew reviews (77%) also cite expensive-for-service pricing. Average value-for-money in this group: **1.8/5**.

**Example Themes:**
> "Crew were sullen, unsmiling, service abysmal...tablecloths given as serviettes...this was not the standard expected from business class"

> "Crew level has come down significantly...interactions from check-in to flight were passive aggressive"

The gap is sharpest when premium pricing meets baseline or degraded crew professionalism.

---

## 4. Ground Service Failures (Supporting Factor)

**Finding:** 49/127 non-recommended reviews (38.6%) report ground service issues.

**TAPP Breakdown (`ground_service_quality`):**
- **Poor check-in experience:** 25 reviews (19.7%)
- **Inconsistent ground staff:** 24 reviews (18.9%)
- **Lounge overcrowded/inadequate:** 6 reviews (4.7%)
- **Baggage handling failures:** 7 reviews (5.5%)
- **Good ground service:** 22 reviews (17.3%)

**Specific Issues:**
- Long wait times at check-in despite "business class" status
- No wheelchairs/priority services despite advance requests
- Chaotic boarding procedures despite premium tier
- Remote stand parking with 45+ minute bus rides
- Lounge closures or denial of lounge access despite business class status

These issues, while less directly tied to in-flight experience, reinforce the overall perception of poor value and inconsistent premium service.

---

## 5. Seat Comfort & Product Configuration (Contextual Factor)

**Finding:** Seat comfort is variable among non-recommended reviews, reflecting mixed aircraft configurations.

| Seat Comfort Rating (1–5) | Non-Recommended (n=127) | All Reviews |
|---------------------------|------------------------|-------------|
| Mean | 3.87 | 4.39 |
| Dated/Hard/Uncomfortable | 38 reviews (30%) | — |
| QSuite Exceptional Privacy | 20 reviews (16%) | — |

**TAPP Insight (`seat_comfort_and_privacy`):**
- **Dated/hard/uncomfortable:** 38 reviews → older 777 or A380 business config
- **Traditional config spacious:** 36 reviews → newer 787 or A350 with good seats but not QSuite
- **QSuite exceptional:** 20 reviews → some QSuite customers still non-recommended (due to other factors like price, crew)

**Key Finding:** Seat comfort alone does not predict recommendation. Customers with excellent QSuite seats still rate non-recommended when:
- Price is perceived as unjustified (especially after downgrades)
- Crew behavior is poor
- Ground service is failing
- WiFi/IFE or food quality is substandard

---

## 6. Food, Beverage & Entertainment Issues (Secondary Factor)

**Finding:** Food quality and connectivity are cited in ~27–22% of non-recommended reviews, but are secondary to value concerns.

**Food & Beverage (`food_beverage_quality`):**
- **Poor/limited selection:** 21 reviews (16.5%)
- **Cold or overcooked:** 7 reviews (5.5%)
- **Good standard quality:** 41 reviews (32.3%)
- **Excellent/varied/fresh:** 23 reviews (18.1%)

**IFE/WiFi Issues (`ife_connectivity_issues`):**
- **Technical malfunctions:** 8 reviews (6.3%)
- **WiFi unavailable or poor:** 11 reviews (8.7%)
- **Limited selection/poor TV:** 9 reviews (7.1%)

Among reviews citing food/WiFi issues, average value-for-money is **2.0–2.1/5**, indicating these service gaps amplify the value mismatch rather than being independent drivers.

---

## 7. Expectation Gap: The Critical Psychological Driver

**Finding:** 80% of non-recommended reviews report a significant or major gap between expectation and reality.

**TAPP Evidence (`expectation_gap` and `expectation_versus_reality_gap`):**

| Gap Level | expectation_gap | expectation_versus_reality_gap |
|-----------|-----------------|------------------------------|
| Significant gap | 69 reviews (54.3%) | 53 reviews (41.7%) |
| Major disappointment | 35 reviews (27.6%) | 51 reviews (40.2%) |
| Minor gap | 17 reviews (13.4%) | 18 reviews (14.2%) |
| **Total gap (significant + major)** | **104 (81.9%)** | **104 (81.9%)** |

**Severity Profile:** Among the 68 reviews with very low overall ratings (≤ 3/10):
- Average value-for-money: 1.72/5
- Most frequently cite: expensive-for-service (pricing_value_mismatch)
- Most frequently cite: rude/inattentive crew

**Psychological Insight:** Qatar Airways' strong brand reputation and premium pricing create high pre-flight expectations. When aircraft are downgraded, crew is inconsistent, or ground service is chaotic, the gap between brand promise and reality is acute, driving strong negative sentiment and non-recommendation.

---

## 8. Multi-Issue Severity Profiles

**Profile 1: Product Downgrade + Price Mismatch (Highest Severity)**
- **Count:** 43/127 (33.9%)
- **Avg Rating:** 4.2/10
- **Avg Value for Money:** 2.2/5
- **Characteristics:** Booked premium QSuite, received older aircraft, charged same or higher price, refused refund
- **Emotional Tone:** Betrayed, robbed, treated unfairly

**Profile 2: Rude Crew + Price Mismatch**
- **Count:** 41/53 poor-crew reviews (77%)
- **Avg Rating:** 3.0/10
- **Avg Value for Money:** 1.8/5
- **Characteristics:** Paid premium price, received dismissive or rude interactions, not compensated
- **Emotional Tone:** Disrespected, frustrated

**Profile 3: Ground Service Chaos + On-Plane Issues**
- **Count:** 49/127 (38.6%)
- **Avg Rating:** 3.3/10
- **Characteristics:** Long waits at check-in, chaotic boarding, remote stands with bus transfers, despite premium tier
- **Emotional Tone:** Undervalued, not prioritized

**Profile 4: QSuite Received, Priced Expensively, Minor Issues**
- **Count:** 4/127 (3.1%, paradox case)
- **Avg Rating:** 3.2/10
- **Characteristics:** Excellent seats, friendly crew, but WiFi unavailable or food limited; price perceived as excessive
- **Insight:** Even premium delivery cannot overcome perceived overpricing in a premium category.

---

## 9. Comparative Context: Recommended vs. Non-Recommended

| Dimension | Non-Recommended (n=127) | Recommended (n=465) |
|-----------|------------------------|-------------------|
| **Value for Money (1–5)** | 2.22 | 4.29 |
| **Overall Rating (1–10)** | 3.82 | 7.81 |
| **Staff Service (1–5)** | 4.01 | 4.64 |
| **Seat Comfort (1–5)** | 3.87 | 4.39 |
| **Food & Beverages (1–5)** | 3.85 | 4.31 |
| **Expensive-for-service price issue (%)** | 59.8% | — |
| **Rude/inattentive crew (%)** | 41.7% | — |
| **Product downgrade/change (%)** | 40.2% | — |
| **Expectation gap (major/significant, %)** | 81.9% | — |

**Standout Finding:** The gap in **Value for Money** (2.07 points, 48% reduction) is the largest single differentiator. Even among non-recommended reviews with technically good ratings in individual categories (staff, seat, food), value perception is dramatically lower.

---

## 10. Summary of Root Causes

### **Primary Cause: Perceived Value Mismatch (80.3% of non-recommended reviews)**
- Premium pricing misaligned with delivered product quality or service consistency
- Downgrades without refund or compensation
- Cancellation or unavailability of premium amenities (lounge access, paid WiFi)

### **Reinforcing Cause 1: Aircraft/Product Downgrades (40.2%)**
- QSuite flights changed to older 777 or A380 2-2-2 config last-minute
- No notification or opportunity to rebook
- Ticket price unchanged despite inferior product

### **Reinforcing Cause 2: Crew Inconsistency (41.7%)**
- Rude, passive-aggressive, or inattentive behavior
- Perception that premium service expectation is not met
- Especially damaging when paired with high ticket cost

### **Supporting Cause: Ground Service Failures (38.6%)**
- Check-in delays, chaotic boarding, lounge denials
- Remote parking and long bus transfers despite business class
- Undermines premium experience before and after flight

### **Contextual Factors: Food, WiFi, Entertainment (22–28%)**
- Secondary issues that amplify value perception when combined with primary causes
- Individually insufficient to drive non-recommendation but compound dissatisfaction

---

## Conclusion

Qatar Airways Business-Class non-recommendation is **fundamentally a value dissatisfaction issue**, not a product quality issue. Customers pay premium fares with premium expectations, but encounter:

1. **Product inconsistency** (downgrades without notice or refund)
2. **Service inconsistency** (crew rudeness or inattention despite high price)
3. **Unmet premium promises** (ground service, lounge access, amenities)

The psychological driver is **expectation gap**: the airline's strong brand reputation creates high pre-flight expectations, which are then violated by operational issues (downgrades, delays, crew behavior) that feel worse because of the premium price point. This combination—high price + degraded or inconsistent service—is what drives the 21.5% non-recommendation rate.

---

**Report Generated:** 2026-08-03  
**Dataset Size:** 592 Business-Class reviews (127 non-recommended, 465 recommended)  
**Augmented Columns Used:** 11 TAPP-generated semantic facets
