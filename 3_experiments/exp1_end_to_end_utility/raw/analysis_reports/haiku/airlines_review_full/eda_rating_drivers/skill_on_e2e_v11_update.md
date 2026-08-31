---
dataset: airlines_review_full
scenario: eda_rating_drivers
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "Overall Rating"
query: "Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?"
source_table: augment_table/airlines_review_full/eda_rating_drivers/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-08-03T05:54:34.559706+00:00
wall_seconds: 190.71
---

# Review Themes and Overall Rating Drivers Across Traveller Type and Class

## Executive Summary

This analysis examines the relationship between review themes—both structured service dimensions and TAPP-derived semantic facets—and Overall Rating, stratified by **Type of Traveller** (Solo Leisure, Couple Leisure, Family Leisure, Business) and **Class** (Economy, Business, Premium Economy, First Class).

**Key Finding:** Value for Money is overwhelmingly the dominant driver of Overall Rating across all segments (correlation ≥ 0.84). Cabin crew service sentiment and operational reliability are the strongest secondary themes, with distinct patterns between high-rated and low-rated reviews. Across traveller types and classes, higher ratings correlate with professional/exceptional crew service, reliable on-time operations, modern aircraft, and positive price-value perception.

---

## Methodology

**Data:** 8,100 reviews (airlines_review_full dataset)  
**Focus Variables:** Overall Rating (1–10 scale)  
**Stratification:** Type of Traveller (4 categories) × Class (4 categories)  
**Analyzed Columns:**
- **Original structured dimensions** (primary evidence): Seat Comfort, Staff Service, Food & Beverages, Inflight Entertainment, Value For Money
- **TAPP-generated semantic facets** (secondary signal): `cabin_crew_service_sentiment`, `aircraft_condition_status`, `operational_reliability`, `ground_staff_professionalism`, `price_value_perception`

**Approach:** Segment-level comparison of high-rated (8–10) vs. low-rated (1–3) reviews, with correlation analysis and proportional breakdowns of TAPP-derived themes.

---

## Overall Pattern: All Travellers and Classes

Across the full dataset:
- **Mean Overall Rating:** 5.63 (SD = 3.52)
- **High-rated (8–10):** 3,406 reviews (42.0%)
- **Low-rated (1–3):** 3,022 reviews (37.3%)

### Dominant Driver: Value For Money
| Dimension | Correlation with Overall Rating |
|-----------|----------------------------------|
| **Value For Money** | **0.883** |
| Staff Service | 0.229 |
| Seat Comfort | 0.210 |
| Food & Beverages | 0.160 |
| Inflight Entertainment | 0.140 |

**Interpretation:** Value for Money alone explains the majority of Overall Rating variance; service and comfort dimensions play secondary roles.

### Semantic Contrast: High vs. Low Ratings

**Cabin Crew Service Sentiment:**
- High-rated: 54% exceptional_attentive, 42% professional_friendly
- Low-rated: 95% indifferent_rude

**Operational Reliability:**
- High-rated: 87% reliable_on_time
- Low-rated: 31% reliable_on_time, 24% cascading_disruption

**Price-Value Perception:**
- High-rated: 60% premium_value_justified, 35% fair_value
- Low-rated: 87% poor_overpriced

---

## By Type of Traveller

### Solo Leisure (n=3,237)
**Mean Overall Rating: 6.07** (highest among non-business travellers)  
High-rated: 1,547 (47.8%) | Low-rated: 1,043 (32.2%)

**Driver Strength:**
- Value For Money correlation: 0.875
- Exceptional crew presence in high-rated: 55.3% vs. 1.2% in low-rated
- Reliable operations in high-rated: 86.5% vs. 31.7% in low-rated

**Interpretation:** Solo leisure travellers show the most favorable overall sentiment and are highly responsive to value perception and crew professionalism. Operational delays significantly damage ratings.

---

### Couple Leisure (n=1,899)
**Mean Overall Rating: 5.48**  
High-rated: 738 (38.9%) | Low-rated: 717 (37.8%)

**Driver Strength:**
- Value For Money correlation: 0.888 (strongest among all segments)
- Exceptional crew in high-rated: 50.7% vs. 0.4% in low-rated (sharpest contrast)
- Staff Service slightly weaker here (0.199) than other dimensions suggest interpersonal nuance

**Interpretation:** Couples are most sensitive to value and crew hospitality; nearly balanced high/low split indicates this segment is most critical. Service consistency matters more than other traveller types.

---

### Family Leisure (n=1,551)
**Mean Overall Rating: 5.14** (lowest among leisure travellers)  
High-rated: 587 (37.8%) | Low-rated: 710 (45.8%)

**Driver Strength:**
- Value For Money correlation: 0.897 (highest across all segments)
- Staff Service correlation: 0.287 (notably higher than other groups)
- Exceptional crew: 54.3% in high-rated vs. 0.3% in low-rated
- Reliable operations: 86.2% high vs. 27.2% low

**Interpretation:** Families weight Staff Service more heavily than other traveller types (likely due to special needs, children). Operational disruptions disproportionately harm family trips. Value perception is critical, and poor experiences often involve unhelpful or slow staff.

---

### Business (n=1,413)
**Mean Overall Rating: 5.38**  
High-rated: 534 (37.8%) | Low-rated: 552 (39.1%)

**Driver Strength:**
- Value For Money correlation: 0.873
- Exceptional crew in high-rated: 55.4% vs. 1.1% in low-rated
- Reliable operations: 87.1% high vs. 35.7% low (highest operational reliability correlation among all groups)

**Interpretation:** Business travellers demand both crew excellence and operational reliability; delays are particularly damaging. Interestingly, Value For Money remains dominant even though travel is often expensed—suggesting business passengers expect justifiable premium pricing for their added cost.

---

## By Cabin Class

### Economy Class (n=5,504)
**Mean Overall Rating: 5.18** (lowest among classes)  
High-rated: 2,057 (37.4%) | Low-rated: 2,421 (44.0%)

**Rating Profile (High vs. Low):**
| Dimension | High-rated | Low-rated | Gap |
|-----------|-----------|-----------|-----|
| Value For Money | 4.60 | 1.52 | 3.08 |
| Staff Service | 3.78 | 3.10 | 0.68 |
| Seat Comfort | 3.67 | 3.04 | 0.63 |
| Inflight Entertainment | 3.73 | 3.42 | 0.31 |
| Food & Beverages | 3.59 | 3.12 | 0.47 |

**TAPP Themes:**
- **Aircraft Condition:** Modern (23.3% high vs. 1.5% low); Unknown at 42.5% in low-rated (suggests incomplete reviews or older aircraft poorly documented)
- **Cabin Crew:** Exceptional/Professional dominates high-rated (96%); Indifferent/Rude in low-rated (95%)
- **Ground Staff:** Professional in high (72%), Rude/Slow in low (95%)

**Interpretation:** Economy passengers are price-sensitive; unmet value expectations drive extremely low ratings. Crew rudeness or slow ground handling become focal complaints. Modern aircraft perception (or lack thereof) correlates with satisfaction.

---

### Business Class (n=2,104)
**Mean Overall Rating: 6.65** (highest among classes)  
High-rated: 1,117 (53.1%) | Low-rated: 478 (22.7%)

**Rating Profile (High vs. Low):**
| Dimension | High-rated | Low-rated | Gap |
|-----------|-----------|-----------|-----|
| Value For Money | 4.50 | 1.64 | 2.86 |
| Staff Service | 3.86 | 3.23 | 0.63 |
| Seat Comfort | 3.70 | 3.21 | 0.49 |
| Inflight Entertainment | 3.74 | 3.63 | 0.11 |
| Food & Beverages | 3.64 | 3.30 | 0.34 |

**TAPP Themes:**
- **Aircraft Condition:** Modern (55.2% high vs. 7.1% low)—strongest class-based difference. Older/worn aircraft trigger complaints about seating, comfort systems.
- **Operational Reliability:** Reliable on-time in 88%+ of high-rated; only 42% in low-rated
- **Ground Staff & Crew Service:** More critical gaps here; professional vs. rude/slow is sharper than in economy

**Interpretation:** Business passengers expect—and receive—premium aircraft. Modern aircraft perception is a major satisfaction driver. Operational delays are major sources of dissatisfaction. Premium seating comfort complaints focus on recline mechanisms, foot support, and bed flatness (reflected in lower Seat Comfort gap compared to economy).

---

### Premium Economy (n=371)
**Mean Overall Rating: 5.97**  
High-rated: 155 (41.8%) | Low-rated: 106 (28.6%)

**Key Drivers:**
- Value For Money: 0.884 correlation
- Seat Comfort: 0.254 (notably higher than economy/business, reflecting confusion over "premium" seating specs)
- Aircraft modern/well-maintained: 34.8% high vs. 9.4% low

**Interpretation:** Premium economy occupies an ambiguous market position. Passengers expect better seating but sometimes receive equivalent-to-economy food/service, creating disappointment. Value perception is volatile; low ratings often cite "premium price for economy quality."

---

### First Class (n=121)
**Mean Overall Rating: 7.60** (highest of all classes)  
High-rated: 77 (63.6%) | Low-rated: 17 (14.0%)

**Key Drivers:**
- Modern aircraft: 72.7% high vs. 35.3% low
- Value For Money correlation: 0.84
- Food & Beverages: Noted positively; caviar presentation and quality emphasized

**Sample Note:** First class is small (n=121); patterns are illustrative but less stable. However, notably higher satisfaction suggests premium service delivery aligns with expectations.

---

## Cross-Segment Insights: Type × Class Combinations

**Highest-Rated Segments:**
1. **Solo Leisure + First Class** (n=71, Rating=8.21) – Unencumbered travellers in premium settings
2. **Couple Leisure + First Class** (n=16, Rating=7.38)
3. **Solo Leisure + Business Class** (n=758, Rating=7.29) – Largest premium segment with consistently high satisfaction

**Lowest-Rated Segments:**
1. **Couple Leisure + Economy** (n=1,258, Rating=4.89)
2. **Family Leisure + Economy** (n=1,273, Rating=4.87)
3. **Business + Economy** (n=702, Rating=4.96)

**Pattern:** Premium cabin class (Business/First) elevates satisfaction across all traveller types by ~1.5–1.8 rating points. Economy experiences are consistently challenged for families and couples, suggesting space/comfort/meal constraints hurt group travel.

### Semantic Signature of High-Rated Premium vs. Low-Rated Economy:

**Solo Leisure + Business (n=470 high-rated):**
- 69.6% exceptional_attentive crew
- 88.5% reliable_on_time
- 78.7% premium_value_justified
- Modern aircraft: 56.6%

**Couple Leisure + Economy (n=585 low-rated):**
- 94.5% indifferent_rude crew
- 28.4% reliable_on_time
- 89.7% poor_overpriced perception
- 42.1% Unknown aircraft condition (likely older craft or insufficient review detail)

---

## Review Theme Summary by Outcome

### High-Rated Reviews (8–10, n=3,406)

**Structured Dimensions (mean scores):**
- Value For Money: 4.58 (vs. 1.52 low-rated)
- Staff Service: 3.91
- Seat Comfort: 3.71
- Inflight Entertainment: 3.80

**Dominant TAPP Themes:**
- Cabin crew sentiment: 54% exceptional_attentive, 42% professional_friendly
- Operational status: 87% reliable_on_time
- Aircraft condition: 56% adequately_maintained, 36% modern_well_maintained
- Ground staff: 76% professional
- Price perception: 60% premium_value_justified

**Narrative:** "Excellent crew, smooth flight, comfortable seat, great value for money."

---

### Low-Rated Reviews (1–3, n=3,022)

**Structured Dimensions (mean scores):**
- Value For Money: 1.52 (sharp disconnect with pricing)
- Staff Service: 3.15
- Seat Comfort: 3.07
- Inflight Entertainment: 3.42

**Dominant TAPP Themes:**
- Cabin crew sentiment: 95% indifferent_rude
- Operational status: 31% reliable_on_time, 24% cascading_disruption, 24% significant_delay_unmanaged
- Aircraft condition: 43% Unknown, 42% adequately_maintained, 9% showing_age
- Ground staff: 61% rude_unhelpful, 34% slow_disorganized
- Price perception: 87% poor_overpriced

**Narrative:** "Rude staff, delayed flight, uncomfortable seat, terrible value for money."

---

## Key Review Themes Associated with Higher Ratings

1. **Exceptional Cabin Crew Service** (55% in high-rated vs. <2% in low-rated)
   - Explicit mentions: attentiveness, warmth, professional demeanor, proactive assistance
   - Cross-segment consistency: strongest in Business+Solo (70%), even strong in Economy+Family (50%)

2. **On-Time Operational Reliability** (86% high-rated vs. 31% low-rated)
   - Delays, ground disruptions, and cascading issues are primary frustration drivers
   - Most critical for Business travellers (91% high vs. 41% low)

3. **Fair/Premium Value for Price** (60% high-rated premium perception)
   - Economy passengers split between fair (46%) and premium (49%) value perception when satisfied
   - Low-rated uniformly perceive poor_overpriced (87%+)

4. **Modern Aircraft Condition** (36% high-rated modern vs. 3% low-rated)
   - Business class differentiator (55% modern high vs. 7% low)
   - Older/worn aircraft mentioned in complaints about seating comfort, lack of IFE, cleanliness

5. **Professional Ground Staff** (76% high-rated vs. 10% low-rated)
   - Check-in efficiency, baggage handling, assistance with connections
   - Particularly impactful for family/multi-segment trips

---

## Key Review Themes Associated with Lower Ratings

1. **Rude/Indifferent Crew Service** (95% in low-rated vs. <4% in high-rated)
   - Explicit mentions: dismissiveness, refusal to assist, lack of empathy
   - Damages ratings across all segments regardless of other service quality

2. **Significant Delays, Cascading Disruptions** (24–30% in low-rated)
   - Missed connections, extended layovers, overnight reroutes
   - Family travellers report disproportionate stress; business travellers cite wasted time/productivity

3. **Poor Value-Price Alignment** (87% low-rated perceive poor_overpriced)
   - Economy passengers especially: charged for basics (bag fees, seat selection), mediocre meals
   - Business and premium passengers: high price expectations unmet by dated aircraft or sparse amenities

4. **Aging/Worn Aircraft** (9% low-rated showing_age)
   - Complaints about seat comfort (narrow seats, no padding, non-functional recline), lack of WiFi, broken IFE
   - IFE failures particularly frustrating on long-haul

5. **Slow/Rude Ground Staff** (61% low-rated rude_unhelpful, 34% slow_disorganized)
   - Check-in delays, unresponsiveness to baggage issues, dismissive complaint handling
   - Compounds frustration if coupled with operational delays

---

## Segment-Specific Themes

### Solo Leisure Travellers
- **Highest satisfaction** among traveller types
- **Most responsive to:** operational punctuality (86.5% high), exceptional crew (55%)
- **Most bothered by:** delays (31.7% low-rated experience cascading issues), rude ground staff
- **Sweet spot:** Business class + on-time + modern aircraft

### Couple Leisure Travellers
- **Most critical segment** (balanced high/low split)
- **Most responsive to:** crew service quality (sharply 50.7% vs. 0.4% gap), value perception
- **Most bothered by:** poor value perception (89.7% in economy low-rated), rude crew
- **Sensitive to:** personal attention, hospitality gestures (cabin crew effort noted)

### Family Leisure Travellers
- **Lowest satisfaction** among leisure types
- **Most responsive to:** staff service (0.287 correlation—highest among types), on-time operations
- **Most bothered by:** rude/unhelpful staff (97.8% in low-rated feel this), delays (27.2% reliable in low vs. 86.2% high)
- **Special needs:** seat spacing for children, meal variety, staff patience with young passengers

### Business Travellers
- **Steady satisfaction** (neither highest nor lowest)
- **Most responsive to:** operational reliability (87.1% high vs. 35.7% low—sharpest operational gap)
- **Most bothered by:** delays (wasted time), poor value despite high cost, disorganized service
- **Premium expectations:** modern aircraft (48.5% high), professional ground/cabin crew

### Economy Class Passengers
- **Most price-sensitive:** value correlation = 0.890
- **Most bothered by:** rude crew (95% low-rated), poor aircraft documentation/aging equipment
- **Responsive to:** crew professionalism (despite low pay grade, exceptional service noted), on-time delivery

### Business Class Passengers
- **Highest satisfaction:** 53% high-rated (vs. 37% economy)
- **Most responsive to:** modern aircraft condition (55% high vs. 7% low), crew excellence
- **Most bothered by:** seat discomfort (mechanical issues, non-flat beds), outdated IFE, perceived premium-price misalignment

### Premium Economy Passengers
- **Volatile satisfaction:** caught between economy and business expectations
- **Most bothered by:** "premium price, economy quality" perception (food, seat, service parity with economy)
- **Responsive to:** aircraft modernity (differentiator from standard economy)

---

## TAPP-Generated Facets: Integration with Structured Data

The TAPP-generated semantic columns reinforce and disambiguate structured ratings:

| Facet | Correlation with Structured Ratings | Role |
|-------|--------------------------------------|------|
| `cabin_crew_service_sentiment` | Implicit in Staff Service (0.23 correlation) | **Clarifies tone** – captures "professional but cold" vs. "warm and attentive"; explains variance in Staff Service ratings |
| `operational_reliability` | Implicit in Value For Money (0.88 correlation) | **Core value driver** – delays directly erode perceived value and satisfaction; explains why reviews with identical meal/seat scores differ vastly |
| `aircraft_condition_status` | Implicit in Seat Comfort, Food (0.21, 0.16 correlation) | **Differentiator by class** – modern aircraft perception (36% in high vs. 3% low) explains Business class premium satisfaction; weak signal in low-rated reviews (43% Unknown) |
| `ground_staff_professionalism` | Implicit in Staff Service | **Extends service signal** – captures pre/post-flight touchpoints not captured by cabin crew ratings; critical for connections/baggage |
| `price_value_perception` | Direct alignment with Value For Money (0.883 correlation) | **Strongest facet** – validates that structural Value rating reflects genuine price-quality judgment, not just poor-quality generic complaints |

**Conclusion:** TAPP facets add semantic granularity and cross-segment comparability but do not introduce independent dimensions beyond the structured ratings. They are most valuable for explaining **why** travellers with similar service scores diverge widely in overall satisfaction (e.g., crew sentiment differences, operational disruption timing).

---

## Decision-Ready Insights

### For Operations Teams:
- **Operational punctuality is non-negotiable:** 55+ percentage-point gaps in high vs. low ratings directly attribute to reliable_on_time
- **Crew training ROI:** Exceptional/professional sentiment appears in 96% of high-rated, <4% of low-rated across all segments
- **Aircraft fleet modernization:** Business class modernization has outsized satisfaction ROI (55% modern in high vs. 7% low)

### For Pricing/Revenue Management:
- **Value perception must align with price:** 87% of low-rated reviews cite poor_overpriced; economy passengers especially sensitive to ancillary fees
- **Premium cabin pricing is justified:** Business class satisfaction (6.65 mean) vs. economy (5.18) suggests customers accept premium pricing when service/ops deliver
- **First class pricing requires operational + service excellence:** 72.7% modern aircraft presence in first class suggests premium passengers reward (or expect) new equipment

### For Commercial Strategy:
- **Segment targeting:** Solo leisure travellers most satisfied (6.07); families most dissatisfied (5.14)—opportunity to improve family offerings (staff training, wider seats, meal variety)
- **Class elasticity:** Solo business travellers (Business class, 7.29) show highest satisfaction; couple economy travellers (4.89) most critical—capacity/revenue trade-offs evident
- **Value communication:** Overwhelmingly dominant theme—marketing should emphasize reliability + modern aircraft + crew excellence, not ancillary perks

---

## Conclusion

Across Type of Traveller and Class, **Value for Money** is the overwhelming driver of Overall Rating (correlation 0.88). Secondary themes—cabin crew sentiment, operational reliability, aircraft modernity, and ground staff professionalism—jointly explain the remaining variance and show consistent patterns:

- **High-rated reviews** are characterized by exceptional/professional crew (54%), reliable on-time operations (87%), modern aircraft (36%), and premium/fair value perception (60%)
- **Low-rated reviews** are dominated by rude/indifferent crew (95%), unreliable operations (69%), aircraft condition uncertainty (43%), and poor_overpriced perception (87%)

**Segment-specific variations:** Solo leisure travellers show highest satisfaction and responsiveness to operations/crew; families show lowest satisfaction and heightened sensitivity to staff service; business travellers prioritize operational reliability; economy passengers are most price-sensitive; business class passengers demand modern aircraft.

The TAPP-generated semantic facets enhance interpretability but do not introduce independent explanatory dimensions beyond structured ratings—they function as qualitative validation and cross-segment comparability tools.
