---
dataset: airlines_review_full
scenario: causal_qatar_business
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "non_recommendation_outcome"
query: "Explain why some Qatar Airways Business-Class flights receive a non-recommended (Recommended = no) result."
source_table: augment_table/airlines_review_full/causal_qatar_business/haiku__skill_on_v11_update.csv
generated_at: 2026-08-03T05:49:17.292863+00:00
wall_seconds: 85.95
---

# Analysis: Non-Recommended Qatar Airways Business-Class Flights

## Executive Summary

Of 592 Qatar Airways Business Class reviews in the dataset, 127 (21.5%) received a "Recommended = no" outcome. These non-recommendations are driven by **value perception failures**, **service inconsistencies**, and **unmet traveler expectations**, rather than uniform product deficiencies. The primary causal mechanism is a perceived misalignment between premium ticket price and actual service delivery.

---

## Key Findings

### 1. **Value Perception: The Dominant Factor**

**Strong Evidence:**
- Non-recommended reviews average **2.22/10 on Value For Money** versus **4.29/10** for recommended flights (gap of 2.07 points)
- **51.1%** of non-recommended reviews cite price-value problems:
  - 36 reviews (28.3%): "price_high_for_decline"
  - 29 reviews (22.8%): "price_unjustified_for_product"
  - 16 reviews (12.6%): "premium_price_for_old_aircraft"

**Pattern:** Customers paid premium Business Class fares but experienced product downgrades, outdated aircraft, or service gaps that made the price feel unjustified.

### 2. **Service Inconsistency and Attentiveness Gaps**

**Evidence:**
- 52.8% (67 of 127) of non-recommended reviews cite service quality problems:
  - 31 reviews (24.4%): Poor attentiveness / inattentive crew
  - 26 reviews (20.5%): Disorganized service (boarding chaos, lack of coordination)
  - 10 reviews (7.8%): Rude behavior or crew unmotivated
- Staff Service ratings average **4.01** for non-recommended (versus **4.39** for recommended)

**Pattern:** Even when core product (seats, food) received moderate ratings, failures in crew responsiveness and operational organization drove dissatisfaction.

### 3. **Traveler Expectation Mismatches**

**Evidence:**
- 58.3% (74 of 127) of non-recommended reviews show **business_traveler_operational_friction**:
  - Flight downgrades without adequate compensation
  - Delays or missed connections that disrupted business plans
  - Booking/check-in issues (e.g., ticket name discrepancies)
- 23.6% (30 reviews): Leisure travelers frustrated with comfort expectations

**Pattern:** Business travelers expected reliable, seamless execution; when they encountered operational failures or seat changes, perception of value collapsed.

### 4. **Product Delivery Issues (Secondary Factor)**

**Evidence:**
- 15.0% (19 of 127): Very low Seat Comfort ratings (1–2)
- 18.9% (24 of 127): Very low Food & Beverages ratings (1–2)
- Common complaints: aircraft equipment downgrades, QSuite not supplied, seat malfunction

**Note:** Product issues alone did not fully explain non-recommendations; the same product failures on recommended flights were tolerated when staff service was attentive.

### 5. **Overall Satisfaction Collapse**

**Evidence:**
- Non-recommended reviews: mean Overall Rating **3.82/10**
- Recommended reviews: mean Overall Rating **8.43/10**
- Distribution of non-recommended: 51 reviews (40%) rated 1–2, only 10 reviews (7.9%) rated 8–10

**Pattern:** Non-recommendations reflect deep dissatisfaction, not marginal complaints.

---

## Causal Structure

### Primary Path: Value Perception Failure
```
Premium Ticket Price 
  + Service Quality Gap / Operational Friction / Aircraft Downgrade
  + Low Attentiveness or Crew Disorganization
  → Perceived Injustice in Value Proposition
  → Recommendation = NO
```

### Secondary Amplifiers:
- **Product inconsistency** (expected QSuite or new aircraft, received older product)
- **Business traveler friction** (schedule/booking disruptions compounded price frustration)
- **Unresponsive crew** (reduced ability to recover from initial dissatisfaction)

---

## Notable Patterns

### When Non-Recommendations Occurred:
1. **Downgrades with inadequate compensation** – customers paid premium yet received lower cabin class
2. **Older aircraft operated at Business Class prices** (e.g., A340 vs. newer A350)
3. **Boarding and operational chaos** despite Business Class priority expectations
4. **Service decline relative to past Qatar Airways experiences** (previous standards not maintained)

### When Non-Recommendations Were Avoided:
- Even with aging aircraft or modest amenities, customers recommended when:
  - Crew was proactive and attentive
  - Value proposition was transparent (e.g., discounted Business upgrade clearly communicated)
  - No product promises were broken

---

## Conclusion

Qatar Airways Business Class non-recommendations are not caused by a single product failure, but rather a **value perception mismatch** triggered by:
1. Gap between promised and delivered service quality (52.8% of cases)
2. Aircraft or seat-class downgrades without justification (15% critical cases)
3. Operational failures (58.3% business traveler friction)

The **focus variable**—non_recommendation_outcome—is primarily driven by **perceived price-to-value injustice** combined with crew attentiveness failures. Customers accept moderate product limitations if service feels premium; they reject premium prices when service feels standard or inconsistent.

**Actionable insight:** Improving non-recommendation rates requires focus on crew training and operational consistency, not just product upgrades, as service failures amplify price perception.
