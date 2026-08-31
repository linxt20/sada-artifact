---
dataset: airlines_review_full
scenario: prediction_satisfaction_drivers
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "overall_rating"
query: "What drives customer satisfaction (Overall Rating) across the different airlines?"
source_table: augment_table/airlines_review_full/prediction_satisfaction_drivers/haiku__skill_on_v11_update.csv
generated_at: 2026-08-03T05:55:43.104636+00:00
wall_seconds: 100.51
---

# Customer Satisfaction Drivers Across Airlines

## Executive Summary

This analysis examines what drives customer satisfaction (Overall Rating) across major international airlines using 8,100 verified passenger reviews. The dataset reveals **five critical drivers** that consistently predict satisfaction, with substantial variation in how different airlines perform across these dimensions.

## Key Findings

### 1. **Value for Money is the Strongest Satisfaction Driver**

**Evidence:**
- Spearman correlation with Overall Rating: **r = 0.867** (strongest among all factors)
- Customers perceiving excellent value: **9.32/10 average rating** (n=1,964)
- Customers perceiving poor/overpriced: **2.39/10 average rating** (n=3,508)

**Pattern:** Value for money perception transcends aircraft type or route length. Even airlines with premium positioning (Business Class) receive low ratings when passengers feel overcharged relative to service quality.

**Airline Variance:**
- Qatar Airways: 36.1% report excellent value → avg 7.20 rating
- Singapore Airlines: 34.2% report poor/overpriced → avg 6.54 rating
- Turkish Airlines: 64.0% report poor/overpriced → avg 3.68 rating

---

### 2. **Ground Staff Efficiency (Fast, Smooth, Helpful Service)**

**Evidence:**
- Customers experiencing fast/smooth/helpful ground staff: **9.13/10 average rating**
- Customers experiencing chaotic/rude/unhelpful staff: **1.92/10 average rating**
- Differential impact: **7.21-point spread** on 10-point scale

**Pattern:** Ground staff efficiency affects pre-flight and connection experiences. High-performing airlines (e.g., Qatar) have superior check-in and boarding processes, while low performers (Turkish Airlines, Emirates) report chaotic procedures and unhelpful staff.

**Operationally Critical:** This driver has clear, measurable outcomes—from check-in speed to baggage handling to connection assistance.

---

### 3. **Problem Resolution Capability (Proactive vs. Unresponsive)**

**Evidence:**
- Proactive/empathetic resolution: **9.35/10 average rating** (n=1,298)
- Unresponsive/hostile/refused: **1.90/10 average rating** (n=2,262)
- Differential impact: **7.45-point spread**

**Pattern:** When issues arise (delays, baggage loss, booking errors, missed connections), customer satisfaction critically depends on whether the airline:
- **Proactively addresses** the problem with empathy
- **Responds promptly** and helpfully
- **Dismisses complaints** or responds with hostility

**Airline Variance:**
- Qatar Airways: 38.6% receive responsive/helpful resolution → 7.20 rating
- Singapore Airlines: 27.5% responsive helpful, but 18.5% unresponsive → 6.54 rating
- Turkish Airlines: 48.4% unresponsive/hostile → 3.68 rating

**Critical Insight:** Many complaints in low-rated airlines stem not from initial failures but from poor recovery—refusals to compensate for damages, unhelpful rebooking, lack of follow-through on promised solutions.

---

### 4. **Cabin Crew Service Quality (Attentive & Friendly vs. Dismissive)**

**Evidence:**
- Attentive/friendly crew: **8.91/10 average rating** (n=2,931)
- Rude/dismissive crew: **1.95/10 average rating** (n=1,823)
- Differential impact: **6.96-point spread**

**Pattern:** In-flight crew demeanor profoundly shapes perception of the flight experience. Attentive service includes:
- Personal attention and genuine hospitality
- Proactive beverage/meal service
- Small courtesies (memory of special requests, genuine smiles)
- Responsiveness to passenger needs

**Airline Variance:**
- Qatar Airways: 56.7% attentive/friendly → 7.20 rating
- Singapore Airlines: 40.7% attentive/friendly, but 12.0% rude/dismissive → 6.54 rating
- Turkish Airlines: 47.7% rude/dismissive → 3.68 rating

**Evidence from Reviews:** Singapore Airlines shows service inconsistency—some crews exemplary, others described as "not the Singapore Airlines I know." Turkish Airlines and Emirates consistently receive complaints about dismissive crew attitudes.

---

### 5. **Aircraft Condition & Airline Consistency**

**Evidence - Aircraft Condition:**
- New/modern/well-maintained: **8.26/10 average rating** (n=1,459)
- Dated/tired/worn: **4.68/10 average rating** (n=617)
- Differential: **3.58-point spread**

**Evidence - Airline Consistency:**
- Consistently excellent: **9.27/10 average rating** (n=2,612)
- Declining/degraded: **2.22/10 average rating** (n=2,994)
- Differential: **7.05-point spread**

**Pattern:** Newer aircraft create measurable comfort improvements, but more impactful is whether the airline maintains consistent standards. Low satisfaction airlines show "inconsistent variable" (4.89 rating) or "declining degraded" (2.22 rating) patterns, suggesting quality degradation post-COVID or cost-cutting.

**Airline Variance:**
- Singapore Airlines: 35.4% unknown aircraft condition; 30.9% report declining quality
- Turkish Airlines: Predominantly "declining/degraded" trend noted in reviews

---

### 6. **Flight Operational Reliability (On-Time Performance)**

**Evidence:**
- On-time/smooth flights: **6.48/10 average rating** (n=5,863)
- Significant delays (30+ min): **2.54/10 average rating** (n=696)
- Major disruptions/cancellations: **1.83/10 average rating** (n=456)

**Pattern:** Operational delays independently reduce satisfaction, but only among passengers without other complaints. When combined with poor ground/crew service, operational failures amplify dissatisfaction.

**Airline Variance:**
- Qatar Airways: 86.9% on-time → 7.20 rating
- Singapore Airlines: 72.0% on-time → 6.54 rating
- Turkish Airlines: 48.5% on-time → 3.68 rating

**Important Caveat:** 14.2% of Singapore Airlines reviews lack operational reliability data, suggesting variable data capture or passenger focus on other dimensions.

---

## Airline-Specific Patterns

| **Airline** | **Avg Rating** | **Strongest Driver** | **Weakest Driver** | **Key Issue** |
|---|---|---|---|---|
| **Qatar Airways** | 7.20 | Excellent value (36%), responsive crew | Generally balanced | Minimal issues |
| **Singapore Airlines** | 6.54 | Mixed: 40.7% attentive crew vs 12% rude | Value perception (34% poor/overpriced) | Post-COVID service inconsistency |
| **Turkish Airlines** | 3.68 | None pronounced | ALL drivers weak—47.7% rude crew, 64% overpriced | Systematic service failures |
| **Emirates** | 4.67 | Operational reliability | Value & crew quality poor | Perception of rising costs + staff issues |

---

## Numeric Rating Features (Supporting Role)

While the categorical "driver" columns dominate prediction, numeric ratings show:
- **Staff Service:** r = 0.230 with Overall Rating (moderate strength)
- **Seat Comfort:** r = 0.208 with Overall Rating
- **Food & Beverages:** r = 0.158 with Overall Rating
- **Inflight Entertainment:** r = 0.135 with Overall Rating

These moderate-strength correlations indicate that while comfort matters, **service quality and value perception dominate** satisfaction outcomes.

---

## Exceptions & Important Caveats

1. **Data Coverage Gaps:** ~14% of Singapore Airlines reviews lack flight operational reliability data; ~38% lack aircraft condition data, suggesting these factors may be under-represented in driver importance.

2. **Reverse Causality Risk:** Poor satisfaction may drive negative framing of all factors. However, the sharp differentiation between "on-time/smooth" (6.48) and "major disruption" (1.83) flights suggests operational issues have independent causal impact.

3. **Value Perception is Contextual:** Premium cabin reviews consistently report "poor/overpriced" regardless of service quality, suggesting pricing strategy is a major satisfaction lever independent of operational performance.

4. **Post-COVID Trend:** Multiple Singapore and Air France reviews mention service degradation "post-COVID," indicating potential structural changes in staffing and consistency.

---

## Decision-Ready Implications

**For Airlines Seeking Satisfaction Improvements:**

1. **Prioritize Value Communication:** Passengers perceive poor value even when services are adequate. Transparent pricing, clear inclusions, and demonstrated premium value offset high fares.

2. **Invest in Problem Resolution:** Customer service staff training for handling complaints has disproportionate satisfaction impact—the difference between 9.35 and 1.90 ratings is resolution approach.

3. **Ensure Crew Consistency:** The gap between "attentive/friendly" (8.91) and "rude/dismissive" (1.95) suggests crew training and morale are critical. Singapore Airlines' variance indicates consistency is slipping.

4. **Operationalize Ground Services:** Fast/smooth ground handling (9.13 rating) is achievable through process design and correlates with 7.21-point satisfaction improvement over chaotic operations.

5. **Consistency > Perfection:** Airlines with "consistently excellent" ratings (9.27) outperform those with "inconsistent variable" (4.89) patterns, even if inconsistent airlines occasionally excel.

---

## Conclusion

Customer satisfaction across airlines is driven by **five overlapping factors in hierarchical order:**
1. **Value for Money Perception** (r=0.867)—transcends all other factors
2. **Ground Staff Efficiency** (9.13 vs 1.92 rating spread)
3. **Problem Resolution** (9.35 vs 1.90 rating spread)
4. **Cabin Crew Service Quality** (8.91 vs 1.95 rating spread)
5. **Operational Reliability & Aircraft Condition** (supporting factors)

Airlines varying widely in Overall Rating (3.68 to 7.95 mean) differ not in isolated dimensions but across all five drivers simultaneously. High-satisfaction airlines (Qatar, ANA) excel broadly, while low-satisfaction airlines (Turkish, Air France) underperform across the board. This suggests systemic organizational capability rather than tactical fixes as the primary satisfaction determinant.
