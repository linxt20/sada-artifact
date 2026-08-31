---
dataset: airlines_review
scenario: eda_rating_drivers
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "Overall Rating"
query: "Across Type of Traveller and Class, which review themes are associated with higher vs. lower Overall Rating?"
source_table: augment_table/airlines_review/eda_rating_drivers/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:04:42.933694+00:00
wall_seconds: 105.07
---

# Review Themes Associated with Higher vs. Lower Overall Ratings
## Analysis across Type of Traveller and Class

**Dataset:** 900 Singapore Airlines reviews | **Analysis Period:** Jan–Feb 2024 (primarily)  
**Focus:** Identifying review themes that correlate with Overall Rating (1–10 scale) across traveller segments and cabin classes

---

## Executive Summary

**Strong theme associations emerge between Overall Rating and five dominant review drivers:**

1. **Crew warmth and engagement** – The single strongest differentiator (84% of high-rated reviews vs. 6% mention low warmth; inverse holds for low ratings)
2. **Ground staff service quality** – 84% of high-rated reviews praise helpful/efficient service vs. 91% of low-rated reviews cite rudeness/dismissiveness
3. **Meal quality consistency** – 80% of high-rated reviews mention high-quality meals vs. 46% of low-rated reviews explicitly note poor quality
4. **Value-for-money perception** – 74% of high-rated reviews justify the premium vs. 89% of low-rated reviews call the fare overpriced
5. **Communication/responsiveness failures** – Present in only 6% of high-rated reviews but 63% of low-rated reviews

These patterns hold consistently across traveller types (Solo, Family, Couple, Business) and cabin classes (Economy, Premium Economy, Business, First).

---

## Key Findings by Type of Traveller

### Solo Leisure Travellers (N=284, mean rating 7.07)
- **Higher ratings (n=209, mean 8.98):** Emphasize crew warmth (84%), high meal quality (83%), and justified pricing (73%)
- **Lower ratings (n=65, mean 1.69):** Complaint themes include poor meals (49%), overpricing (83%), and rude staff (86%)
- **Pattern:** Meal quality becomes more important than seat comfort; consistent focus on value perception

### Family Leisure Travellers (N=141, mean rating 7.06)
- **Higher ratings (n=111, mean 9.02):** 87% note high crew warmth, 83% praise meal quality, 78% justify value
- **Lower ratings (n=48, mean 1.60):** 90% report low crew warmth, 92% criticize staff dismissiveness, 88% perceive overpricing
- **Pattern:** Ground staff behavior strongly differentiates satisfaction (87% helpful vs. 92% dismissive). Highest negative staff sentiment among all traveller types.

### Couple Leisure Travellers (N=240, mean rating 6.93)
- **Higher ratings (n=136, mean 8.92):** 82% cite crew warmth, 71% praise meal quality (lowest among segments), 68% justify value
- **Lower ratings (n=66, mean 1.79):** 88% cite low warmth, 95% perceive dismissive staff, 91% judge as overpriced
- **Pattern:** Highest propensity to perceive overpricing across all low-rated reviews (91%); value perception is a primary differentiator

### Business Travellers (N=133, mean rating 6.13)
- **Higher ratings (n=75, mean 8.85):** 87% praise crew warmth, 84% note meal quality (highest among segments), 81% justify premium positioning
- **Lower ratings (n=43, mean 1.51):** 91% report low warmth, 88% cite dismissive staff, 95% view service as overpriced
- **Key distinction:** **Communication/responsiveness failures** are exceptionally high in low-rated business reviews (68% vs. 6% in high-rated), suggesting business travellers expect and value proactive outreach during disruptions
- **Pattern:** Lowest average rating among traveller types; most sensitive to communication gaps and ground staff responsiveness

---

## Key Findings by Cabin Class

### Business Class (N=237, mean rating 7.35)
- **Higher ratings (n=158, mean 8.99):** 87% crew warmth, 84% high meal quality, 76% value justified
- **Lower ratings (n=42, mean 1.76):** 88% low warmth, 50% poor meals, 88% overpriced
- **Seat comfort:** 13% of high-rated reviews mention seat problems vs. 26% of low-rated (suggesting seat issues elevate complaint frequency in premium cabins)
- **Insight:** Premium cabin customers hold high baseline expectations; crew service and meal consistency are table stakes

### Economy Class (N=563, mean rating 6.46)
- **Higher ratings (n=325, mean 8.96):** 84% crew warmth, 78% high meal quality, 74% value justified
- **Lower ratings (n=158, mean 1.63):** 89% low warmth, 44% poor meals, 89% overpriced
- **Seat comfort:** Only 6% of high-rated reviews mention seat problems vs. 16% of low-rated, indicating seat issues are more tolerated in economy than premium
- **Insight:** Largest and most variable segment; crew demeanor and communication compensate for modest seat configurations when positive

### Premium Economy (N=86, mean rating 6.29)
- **Higher ratings (n=38, mean 8.55):** 74% crew warmth, 76% high meal quality, 63% value justified (lowest justification rate)
- **Lower ratings (n=21, mean 1.76):** 86% low warmth, 57% seat comfort problems (dramatically higher than other classes), 90% overpriced
- **Key finding:** **Seat comfort emerges as a critical pain point** (57% in low-rated reviews) compared to 8% in high-rated—suggesting Premium Economy buyers prioritize seat quality given the premium price point
- **Insight:** Most vulnerable segment for value perception; seat comfort dissatisfaction directly undermines the premium positioning

### First Class (N=14, small sample, mean rating 7.86)
- **Higher ratings (n=10, mean 9.60):** 100% crew warmth, 100% high meal quality, 100% value justified
- **Lower ratings (n=1):** Insufficient data for robust comparison
- **Caveat:** Very small sample (n=14); patterns directional only

---

## Cross-Cutting Insights

### Crew Warmth vs. Robotic Service
- **Universal differentiator across all segments:** Mentioned in 84–87% of high-rated reviews; 86–91% of low-rated reviews cite robotic/low warmth
- **Effect size:** Single largest gap between high and low ratings
- **Segments most sensitive:** Family Leisure and Business travellers show highest negative staff sentiment in low-rated reviews (92% and 88%, respectively)

### Meal Quality Consistency
- **Inverse correlation with ratings:** 
  - High ratings: 80% note high quality
  - Low ratings: 46% cite poor quality (41% have missing data, suggesting meals not memorable or unavailable)
- **Class variation:** Business Class shows highest positive mention (84%) but also highest poor-quality mentions (50%) among low-rated reviews
- **Traveller variation:** Business travellers most frequently praise meal quality in positive reviews (84%); Solo Leisure equally high (83%)

### Value & Pricing Perception
- **Strongest negative indicator in low ratings:** 87–95% of low-rated reviews cite overpricing
- **Weakest justification in high ratings:** Couple Leisure (68%) and Premium Economy (63%) show lowest "value justified" proportions
- **Business travellers:** 81% of high-rated business reviews justify premium despite service lapses, suggesting context (route, convenience) may override experience in B2B contexts

### Ground Staff & Communication
- **Ground staff dismissiveness:** 91% in low-rated vs. 8% in high-rated reviews (dramatic gap)
- **Communication failures:** Especially acute in low-rated Business traveller reviews (68% vs. 6% in high-rated)—suggests business travellers expect and value transparency during disruptions (delays, rebooking)

### Seat Comfort as Class-Dependent Driver
- **Economy/Business:** Minor factor (6–13% of high-rated, 16–26% of low-rated mention it)
- **Premium Economy:** Major pain point (57% of low-rated mention seat problems vs. 8% of high-rated)—indicating value misalignment when premium cabin seats underperform

---

## Segmentation Implications

### For Solo & Family Leisure Segments:
- Crew warmth and meal consistency are primary differentiators
- Staff dismissiveness strongly predicts low ratings
- Seat comfort is a secondary concern

### For Couple Leisure Segment:
- Highest sensitivity to value perception (91% negative in low ratings)
- Ground staff quality exceptionally predictive of dissatisfaction
- Consider targeted value communication and staff training for this segment

### For Business Segment:
- Communication and responsiveness failures disproportionately drive low ratings (68%)
- Ground staff performance critical (87% in low ratings report dismissiveness)
- Despite service gaps, high-rated business reviews justify premium (81%)—suggesting context tolerance but expectation of professionalism

### For Premium Economy Class (Cross-Traveller):
- Seat comfort is the dominant unmet expectation (57% in low ratings)
- Value perception is weakest relative to high-rated reviews (63% justify)
- Redesign focus: either improve seat quality or recalibrate pricing/positioning

---

## Data Quality Notes

- **Sample robustness:** Economy Class (563 reviews) and Business Class (237 reviews) provide reliable segments; Premium Economy (86) and First Class (14) are smaller
- **Theme coverage:** Text-derived themes (crew warmth, meal quality, staff service) are consistently recorded; ~2–4% of records have "Unknown" values in some theme columns, indicating occasional inability to classify from review text
- **Rating distribution:** Bimodal with peaks at 10 (207 reviews, 23%) and 1 (122 reviews, 14%), consistent with airline review polarization; median rating 8.0 but mean 6.53 due to low-rating tail

---

## Conclusion

Review themes strongly associated with **higher Overall Ratings** across traveller types and classes:
- **Crew warmth & engagement** (84% presence)
- **Helpful, efficient ground staff** (84% presence)
- **High-quality, consistent meals** (80% presence)  
- **Justified value for money** (74% presence)
- **Absence of communication failures** (94% absence = 6% presence)

**Lower-rated reviews (1–3 rating)** are dominated by inverse themes:
- Low/robotic crew engagement (87%)
- Rude/dismissive ground staff (91%)
- Poor meal quality or unavailability (46%)
- Perception of overpricing (87%)
- Communication/responsiveness failures (63%)

These associations are **consistent across all traveller types and classes**, with notable amplification in Business traveller communication failures and Premium Economy seat comfort dissatisfaction.
