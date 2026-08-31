---
dataset: airlines_review_full
scenario: eda_rating_drivers
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "Overall Rating"
query: "Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?"
source_table: augment_table/airlines_review_full/eda_rating_drivers/haiku__skill_on_v11_update.csv
generated_at: 2026-08-03T05:52:12.043146+00:00
wall_seconds: 70.11
---

# Review Themes and Overall Rating Drivers: Analysis Report
## Airlines Review Full Dataset | Skill On v11 Update

---

## Executive Summary

This analysis examines 8,100 airline reviews to identify which review themes are associated with **higher vs. lower Overall Ratings** across **Type of Traveller** and **Class**. Eight thematic dimensions are analyzed, revealing clear patterns in what drives customer satisfaction.

**Key Findings:**
- **Crew service warmth** is the strongest overall driver: 75.2% of higher-rated reviews (6–10) feature warm/attentive crew, while 85.5% of lower-rated reviews (1–5) cite inattentive/rushed service.
- **Value perception** shows the sharpest contrast: 61.6% of higher-rated reviews perceive excellent value; 53.2% of lower-rated reviews cite overpriced experiences.
- **Service consistency across class** reveals structural issues: 76.3% of low-rated reviews mention degraded economy or tier disparities.
- **Class and traveller type interact strongly**: Business-class customers consistently rate 0.8–1.9 points higher than economy peers in the same traveller segment.

---

## Theme-Level Insights: Higher vs. Lower Ratings

### 1. **Crew Service Warmth** — Strongest Single Driver
| Rating Level | Dominant Theme | Percentage |
|---|---|---|
| **Higher (6–10)** | Warm & Attentive | 75.2% |
| **Lower (1–5)** | Inattentive & Rushed | 85.5% |

**Interpretation:** Crew comportment dominates perceived quality. Positive crew interactions strongly correlate with satisfaction across all segments. Economy reviews frequently critique crew attentiveness, especially Family Leisure (56% inattentive in economy).

---

### 2. **Seat Comfort & Design** — Highly Class-Dependent
| Rating Level | Dominant Theme | Percentage |
|---|---|---|
| **Higher (6–10)** | Spacious & Comfortable | 52.1% |
| **Lower (1–5)** | Unknown / Cramped | 57.9% / 20.3% |

**Interpretation:** Premium classes (Business/First) consistently cite spacious designs (55–81%). Economy reviews often lack specific comfort mentions (42–54% "Unknown"), but when mentioned, cramped seating dominates negatives. Solo Leisure in Economy shows high unknown rate (45%), suggesting less emphasis on comfort in short leisure flights.

---

### 3. **Food & Beverage Quality** — Quality Over Quantity
| Rating Level | Dominant Theme | Percentage |
|---|---|---|
| **Higher (6–10)** | Excellent & Tasty | 51.9% |
| **Lower (1–5)** | Unknown / Poor & Bland | 64.4% / 24.3% |

**Interpretation:** High ratings emphasize food quality distinctly; poor quality is a key pain point in low ratings. Business travelers and First Class show higher mention rates of excellent food (33–75%). Economy and Premium Economy show mixed results, with Family Leisure and Couple Leisure showing weaker food ratings (29–28% "excellent").

---

### 4. **Aircraft Condition & Age** — Secondary Satisfaction Factor
| Rating Level | Dominant Theme | Percentage |
|---|---|---|
| **Higher (6–10)** | Modern & Well-Maintained | 44.6% |
| **Lower (1–5)** | Unknown / Adequate | 46.9% / 34.4% |

**Interpretation:** Modern aircraft appear in ~45% of higher-rated reviews but correlate less strongly than crew/food/value themes. Old/dated equipment mentioned in ~10% of lower-rated reviews. This theme is less decisive than service or comfort.

---

### 5. **Customer Service Responsiveness** — Critical in Negatives
| Rating Level | Dominant Theme | Percentage |
|---|---|---|
| **Higher (6–10)** | Responsive & Helpful | 77.8% |
| **Lower (1–5)** | Unresponsive/Frustrating & Dismissive | 48.3% + 39.5% = 87.8% |

**Interpretation:** Strong responsiveness drives satisfaction. Notably, dismissive/unresponsive service is a **major differentiator** in low ratings (87.8% combined). Business travelers show lower responsive ratings in economy (34.2%), highlighting frustration when premium service is absent.

---

### 6. **Value Perception** — Second-Strongest Driver
| Rating Level | Dominant Theme | Percentage |
|---|---|---|
| **Higher (6–10)** | Excellent Value | 61.6% |
| **Lower (1–5)** | Overpriced for Experience | 53.2% |

**Interpretation:** Value perception is **inverted** between rating levels—61.6% vs. 53.2%. Economy reviews often cite overpricing (35–39%), especially Family Leisure and Couple Leisure. Business travelers in economy feel premium pricing is not justified (35% overpriced perception in Business traveller economy).

---

### 7. **Service Consistency Across Class** — Reveals Class Tier Issues
| Rating Level | Dominant Theme | Percentage |
|---|---|---|
| **Higher (6–10)** | Class-Appropriate / Consistent High | 41.1% + 40.2% = 81.3% |
| **Lower (1–5)** | Degraded Economy | 76.3% |

**Interpretation:** **Single largest pain point** in low-rated reviews. Economy reviews systematically mention degraded service (50–60%), while some Business travelers cite two-tier disparities (39%). Higher ratings split between "class-appropriate" (economy feels fair) and "consistent high" (premium tiers). Couple Leisure Economy shows the worst perception: 60% degraded.

---

### 8. **Special Requests & Accommodation** — Personalization Matters
| Rating Level | Dominant Theme | Percentage |
|---|---|---|
| **Higher (6–10)** | Personalized & Accommodating | 67.5% |
| **Lower (1–5)** | Inflexible / Refused & Discriminatory | 50.3% + 43.3% = 93.6% |

**Interpretation:** When accommodation is denied or refused, satisfaction drops sharply (93.6% in negatives). First/Business Class expect personalization (52–72%); economy less so. Family Leisure in economy cite refusal/discrimination most (31.9%), suggesting stricter policies affect families.

---

## Segment-Level Patterns: Type of Traveller × Class

### Solo Leisure Travelers
- **Business Class** (n=758, avg=7.29): Strongest positive segment
  - 75.8% warm crew, 61.1% spacious seats, 48.8% excellent food
  - Highest value perception (49.7% excellent value)
  - Minimal class disparity concerns (46% consistent high)

- **Economy Class** (n=2,271, avg=5.57): Large, mixed segment
  - 45.6% inattentive crew, 45.3% Unknown seat comfort
  - 50.3% degraded economy perception
  - Still 42.1% rate crew as responsive (more balanced than other traveller types)

- **Differential**: +1.72 points from economy to business

---

### Family Leisure Travelers
- **Business Class** (n=216, avg=6.45): Moderate satisfaction
  - 51.4% warm crew, 52.3% spacious seats
  - Similar value perception to Solo (39.8% excellent value)

- **Economy Class** (n=1,273, avg=4.87): **Lowest economy segment**
  - 56% inattentive crew, 57.7% degraded economy perception
  - 38.7% overpriced perception (highest among travellers)
  - 31.9% refused/discriminatory accommodation (highest)

- **Differential**: +1.58 points; family dynamics amplify service gaps

---

### Couple Leisure Travelers
- **Business Class** (n=502, avg=6.83): **Highest business segment** after Solo First
  - 53.8% warm crew, 55.4% spacious seats, 47.4% excellent food
  - 53% responsive service, 39.8% consistent high

- **Economy Class** (n=1,258, avg=4.89): Large, dissatisfied segment
  - 55.1% inattentive crew, 60% degraded economy, 33.4% unresponsive service
  - 38.3% overpriced; 34.7% inflexible accommodation

- **Differential**: **+1.94 points** (largest gap); couples most sensitive to class differences

---

### Business (Primarily Purpose) Travelers
- **Business Class** (n=628, avg=5.80): **Mediocre satisfaction**
  - Only 40.9% warm crew (lowest among traveller types in business)
  - 39.3% cite two-tier disparity issues
  - 34.9% cite premium not delivered
  - Highest expectations, disappointed by service quality

- **Economy Class** (n=702, avg=4.96): Frustration-driven
  - 51.1% inattentive crew, 57.4% degraded economy
  - 35.3% overpriced perception; 33.8% inflexible

- **Differential**: +0.84 points (smallest gap); suggests business travelers have uniformly high service expectations unmet

---

## Key Exceptions & Weak Evidence

1. **Aircraft Condition (Moderate Impact):** While modern aircraft appear in ~45% of higher ratings, reviews rarely cite it as a primary satisfaction driver—secondary to service and food.

2. **First Class Data (n=121 total):** Limited sample sizes (Solo=71, Couple=16, Family=11, Business=23) mean First Class patterns are directional only. Solo First Class shows highest ratings (8.21) with strongest theme alignment; Business First Class shows moderate satisfaction (6.87).

3. **Premium Economy Anomaly:** Premium Economy customers show surprisingly low satisfaction (5.22–6.52 avg) despite premium pricing. Perceived as "premium price for economy quality" (cited by Couple Leisure and Business travellers).

4. **Unknown Values:** 15–54% of theme values are "Unknown," indicating reviews don't always explicitly address all dimensions. Highest in food/comfort mentions for economy.

---

## Conclusions

### Drivers of **Higher Ratings (6–10)**
1. **Crew warmth** (75.2%) — Essential foundation
2. **Responsive service** (77.8%) — Problem resolution matters
3. **Value perception** (61.6%) — Fare justification critical
4. **Personalized accommodation** (67.5%) — Customization expected
5. **Spacious/comfortable seating** (52.1%) — Varies by class

### Drivers of **Lower Ratings (1–5)**
1. **Inattentive crew** (85.5%) — Service failures dominate
2. **Degraded economy perception** (76.3%) — Tier consistency issues
3. **Inflexible/refused accommodation** (93.6%) — Policy failures sting
4. **Unresponsive/dismissive service** (87.8%) — Problem escalation failures
5. **Overpriced experience** (53.2%) — Value not perceived

### Segment Recommendations
- **Solo Leisure:** Retain strength in business; focus on economy crew training
- **Family Leisure:** Greatest dissatisfaction in economy; prioritize crew consistency and accommodation flexibility
- **Couple Leisure:** Largest class sensitivity (+1.94); premium experience must exceed economy clearly
- **Business Travelers:** Set realistic expectations; perceive premium not delivered; focus on consistency across all classes

---

**Report Generated:** 2026-08-03  
**Dataset:** 8,100 reviews | 4 traveller types × 4 cabin classes  
**Variant Label:** skill_on
