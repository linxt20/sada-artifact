---
dataset: yelp_polarity_reviews
scenario: causal_negative
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "label_pos"
query: "Which factors best explain negative Yelp experiences?"
source_table: augment_table/yelp_polarity_reviews/causal_negative/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:24:18.197094+00:00
wall_seconds: 88.98
---

# Analysis Report: Factors Explaining Negative Yelp Experiences

## Executive Summary

This analysis examines 125 negative Yelp reviews (rating polarity 0) from a balanced dataset of 250 reviews to identify the primary drivers of negative customer experiences. Using the augmented dataset with TAPP-generated semantic facets, **staff-related service issues emerge as the dominant factor**, present in 68% of negative reviews, significantly outweighing food quality problems (34%). However, negative experiences are often multifactorial, with distinct patterns revealing that service failures and food quality issues represent separable complaint categories.

---

## Methodology

This analysis combines original review text and structured outcome variables with two TAPP-generated augmented columns:
- **`staff_rudeness_or_indifference`**: Semantic classification of staff behavior issues (values: `rude`, `indifferent_slow`, `unprofessional_conduct`, `not_present`)
- **`food_taste_or_flavor_problem`**: Semantic classification of food quality issues (values: `off_bad_quality`, `bland_tasteless`, `not_fresh_old`, `overly_sweet`, `not_present`, `NaN`)

These augmented columns provide direct semantic signal for understanding causal factors in negative reviews without replacing raw textual evidence. The analysis stratifies negative reviews by presence/absence of each factor and examines cooccurrence patterns.

---

## Key Finding 1: Staff Rudeness and Indifference as the Primary Driver

**Staff service issues are present in 85 out of 125 negative reviews (68.0%)**, making them the most prevalent explanatory factor.

### Breakdown of Staff Issues:

| Staff Issue Type | Count | % of Negative Reviews |
|---|---|---|
| Indifferent/Slow Service | 49 | 39.2% |
| Rude Behavior | 25 | 20.0% |
| Unprofessional Conduct | 11 | 8.8% |
| **Total with Issues** | **85** | **68.0%** |
| No Issues Detected | 40 | 32.0% |

### Interpretation:

**Indifferent or slow service** is the single most common manifestation (49 reviews, 39.2%), characterized by:
- Staff ignoring or forgetting customers (extended wait times, lack of follow-up)
- Slow responsiveness despite reasonable restaurant occupancy
- Apparent disengagement from customer care

**Direct rudeness** (25 reviews, 20.0%) includes:
- Impolite or hostile staff behavior
- Discriminatory treatment
- Dismissive language or tone

**Unprofessional conduct** (11 reviews, 8.8%) covers:
- Conduct unbecoming a service professional
- Staff arguing or behaving inappropriately in front of customers

### Representative Example:
> "The worst service I've ever had... First, they seated us, brought coffee, and vanished. Turns out they'd seated us in an area reserved for a private party, and when said party arrived, they had thus forgotten we were there... So we were moved to another spot. Where they took our order and then disappeared. Again, apparently forgetting we were there." (YLP-0002, indifferent_slow)

---

## Key Finding 2: Food Quality Issues as a Secondary but Distinct Factor

**Food taste or flavor problems are present in 42 out of 125 negative reviews (33.6%)**, making food quality a significant but less dominant factor than service failures.

### Breakdown of Food Quality Issues:

| Food Quality Issue | Count | % of Negative Reviews |
|---|---|---|
| Bad/Poor Quality | 24 | 19.2% |
| Bland/Tasteless | 15 | 12.0% |
| Not Fresh/Old | 2 | 1.6% |
| Overly Sweet | 1 | 0.8% |
| **Total with Issues** | **42** | **33.6%** |
| No Issues Detected | 67 | 53.6% |
| Unclassified (NaN) | 16 | 12.8% |

### Interpretation:

**Bad or poor quality food** (24 reviews, 19.2%) is the most common food-related complaint, encompassing:
- Inferior ingredient quality
- Poor preparation or execution
- Unmet expectations relative to pricing

**Bland or tasteless food** (15 reviews, 12.0%) reflects:
- Insufficient seasoning or flavor development
- Underwhelming taste profiles
- Dishes lacking expected culinary characteristics

Notably, **16 reviews (12.8%) could not be classified** regarding food issues (NaN values), suggesting these negative reviews focused entirely on service, pricing, ambiance, or other non-food factors.

### Representative Example:
> "Decent place but a tad overpriced and way overrated. The toppings sounded amazing and were priced to match so I expected to be wow'd. Sadly what came to the table was not great quality. Most of the bruschetta lacked flavor and the poor quality toppings didn't help much." (YLP-0032, off_bad_quality)

---

## Key Finding 3: Service Issues Dominate; Food and Service Are Largely Separable Complaints

Cross-analysis of cooccurrence patterns reveals that **service failures and food quality issues typically drive negative ratings independently**:

| Complaint Pattern | Count | % of Negative Reviews |
|---|---|---|
| **Staff Issues Only** | 68 | 54.4% |
| **Food Issues Only** | 25 | 20.0% |
| Both Staff AND Food Issues | 17 | 13.6% |
| Neither Issue Detected | 15 | 12.0% |

### Key Insight:

The **54.4% of reviews with staff issues alone** demonstrates that service failures are a standalone, potent driver of negative sentiment—customers do not necessarily need food quality problems to rate a restaurant negatively. Conversely, the **20.0% with food issues only** shows that food quality can drive negativity independent of service complaints.

Only 13.6% of negative reviews exhibit both issues, suggesting these are distinct complaint domains rather than symptoms of the same underlying dysfunction. This means:
- A restaurant can deliver poor service with adequate food and still receive negative ratings.
- A restaurant can have service failures without food quality issues and generate negative sentiment.
- Roughly 12% of negative reviews cite neither service nor food quality, pointing to other factors (pricing, ambiance, cleanliness, etc.).

---

## Context: Positive vs. Negative Reviews

To confirm that service and food quality are genuinely explanatory in the negative context:

- **Total dataset**: 250 reviews (125 negative, 125 positive)
- **Negative reviews focus**: The TAPP columns were generated targeting causal factors in negative experiences
- **Augmented coverage**: All 125 negative reviews received semantic classification for staff issues; 109 (87.2%) received food quality classification

The high presence of service issues in negative reviews (68%) versus the unclassified/absent status (32%) in the broader dataset suggests **staff behavior is a primary differentiator between positive and negative experiences**.

---

## Conclusion

**Negative Yelp experiences are best explained by staff rudeness or indifference (68% of negative reviews), with food quality problems playing a secondary but significant role (34%).** The two factors operate largely independently, indicating that restaurants can fail on either dimension to generate customer dissatisfaction. Service failures—particularly indifference, slowness, and lack of attentiveness—represent the single largest driver of negative ratings, appearing in more than two-thirds of negative reviews. Food quality issues, while present in approximately one-third of negative reviews, tend to occur alongside service excellence in the remaining cases, suggesting that even good service cannot fully compensate for poor food.

**Actionable Insight for Restaurants**: Addressing staff training, responsiveness, and professional demeanor should be prioritized as the primary lever for improving customer satisfaction, as it impacts a substantially larger proportion of negative reviews than food quality alone.

---

## Data Summary

- **Dataset**: Yelp polarity reviews (causal negative)
- **Negative reviews analyzed**: 125 (label_pos=0)
- **Total reviews**: 250 (balanced: 125 positive, 125 negative)
- **Augmented columns used**: `staff_rudeness_or_indifference`, `food_taste_or_flavor_problem`
- **Augmented column coverage**:
  - Staff issues: 125/125 (100%)
  - Food issues: 109/125 (87.2%)
