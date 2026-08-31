---
dataset: amazon_polarity_reviews
scenario: predictive_sentiment
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review facets differ by sentiment label?"
source_table: augment_table/amazon_polarity_reviews/predictive_sentiment/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:09:25.637053+00:00
wall_seconds: 57.61
---

# How Review Facets Differ by Sentiment Label — Amazon Polarity Reviews

**Dataset:** 250 reviews (125 negative `label_pos=0`, 125 positive `label_pos=1`), perfectly balanced.  
**Method note:** TAPP-generated columns used: `product_category`, `quality_dimension`, `complaint_severity`, `emotional_intensity`, `primary_emotion`, `expectation_gap_direction`, `defect_or_failure_type`, `recommendation_stance`. All are analyzed as additional explanatory facets alongside the original structured columns (`label_pos`, `title`, `content`). `complaint_severity` has 115/250 nulls (concentrated in positives; 107 of 125 positive reviews have no severity coded), limiting its direct use as a cross-label comparator.

---

## 1. Strongest Discriminators of Sentiment

### 1.1 `primary_emotion`
The sharpest single facet. Emotion clusters are nearly perfectly polarized:

| primary_emotion | neg (0) | pos (1) | pos_rate |
|---|---|---|---|
| anger_frustration | 26 | 0 | 0.00 |
| disgust | 26 | 0 | 0.00 |
| disappointment | 55 | 4 | 0.07 |
| sadness | 1 | 0 | 0.00 |
| surprise_negative | 1 | 0 | 0.00 |
| neutral | 14 | 14 | 0.50 |
| joy_delight | 2 | 103 | **0.98** |
| surprise_positive | 0 | 4 | 1.00 |

Negative reviews overwhelmingly express **disappointment** (55/125, 44%) or split between **anger/frustration** and **disgust** (26 each, 21% each). Positive reviews are dominated by **joy_delight** (103/125, 82%). Neutral emotion is the only shared territory (14 each).

### 1.2 `expectation_gap_direction`
Perfectly aligned with label direction:

| expectation_gap_direction | neg (0) | pos (1) | pos_rate |
|---|---|---|---|
| far_below_expectations | 72 | 0 | 0.00 |
| below_expectations | 44 | 6 | 0.12 |
| met_expectations | 4 | 49 | 0.92 |
| exceeded_expectations | 2 | 67 | 0.97 |
| no_prior_expectation_stated | 3 | 3 | 0.50 |

Negative sentiment is anchored in **far_below_expectations** (72/125, 58%); positive sentiment in **exceeded_expectations** (67/125, 54%) and **met_expectations** (49/125, 39%). No positive review lands in `far_below_expectations`.

### 1.3 `recommendation_stance`
Near-perfect alignment:

| recommendation_stance | neg (0) | pos (1) | pos_rate |
|---|---|---|---|
| explicitly_warns_against | 39 | 0 | 0.00 |
| implicitly_negative | 64 | 1 | 0.02 |
| neutral_or_mixed | 17 | 14 | 0.45 |
| implicitly_positive | 1 | 60 | 0.98 |
| explicitly_recommends | 2 | 50 | 0.96 |

Negative reviews are predominantly **implicitly_negative** (64/125, 51%) or **explicitly_warns_against** (39/125, 31%). Positive reviews split between **implicitly_positive** (60/125, 48%) and **explicitly_recommends** (50/125, 40%).

---

## 2. Moderate Discriminators

### 2.1 `quality_dimension`
**performance_accuracy** is the most negative-skewed dimension (pos_rate 0.24; 32 neg vs 10 pos), consistent with reviews flagging factual errors, product malfunctions, or inaccurate descriptions. **content_quality** is the dominant dimension overall (151/250 reviews) and is slightly positive-leaning (0.55). **delivery_packaging** is exclusively positive (6/6), but n is tiny.

| quality_dimension | neg | pos | pos_rate |
|---|---|---|---|
| performance_accuracy | 32 | 10 | 0.24 |
| build_quality | 12 | 8 | 0.40 |
| content_quality | 68 | 83 | 0.55 |
| usability_design | 5 | 9 | 0.64 |
| delivery_packaging | 0 | 6 | 1.00 |

### 2.2 `defect_or_failure_type`
Defect presence is nearly exclusive to negative reviews: 50/125 negatives (40%) carry a defect tag versus only 2/125 positives (2%). Among defect types, **functional_failure** is most common (29 neg), followed by **physical_breakage** (6 neg). When a defect is absent (`not_present`), reviews lean positive (pos_rate 0.62).

### 2.3 `emotional_intensity`
Negative reviews have a slightly higher mean intensity (3.12 vs 2.84 on a 1–5 scale). High-intensity level 4 skews negative (38 neg vs 18 pos, pos_rate 0.32). This is consistent but weaker than the emotion-type signal above.

---

## 3. Weaker / Contextual Facets

### 3.1 `product_category`
Moderate signal: **music** is positive-leaning (pos_rate 0.72; 29 pos vs 11 neg) while **physical_product** is negative-leaning (pos_rate 0.41; 51 neg vs 36 pos). Books and movies are near-neutral. The category effect is partly mediated by quality dimension and defect type (physical products carry more defect tags).

### 3.2 `complaint_severity`
Only 135/250 reviews have a value (nearly all nulls are in positives). Among those coded, severity 3–5 is almost entirely negative (severity 4: 44 neg, 0 pos; severity 5: 10 neg, 0 pos). This confirms the coding logic (severity not applicable to positives) and adds little independent signal beyond `label_pos` itself.

---

## 4. Summary Table: Key Facet Contrasts

| Facet | Dominant negative pattern | Dominant positive pattern |
|---|---|---|
| `primary_emotion` | disappointment (44%), anger/disgust (21% each) | joy_delight (82%) |
| `expectation_gap_direction` | far_below_expectations (58%) | exceeded (54%) + met (39%) |
| `recommendation_stance` | implicitly_negative (51%), warns_against (31%) | implicitly_positive (48%), recommends (40%) |
| `quality_dimension` | performance_accuracy (26% of neg) | content_quality (66% of pos) |
| `defect_or_failure_type` | defect present in 40% of neg reviews | defect present in 2% of pos reviews |
| `emotional_intensity` | mean 3.12 | mean 2.84 |
| `product_category` | physical_product overrepresented | music overrepresented |

---

## 5. Key Findings

1. **Emotional framing and expectation alignment are the most diagnostic facets.** Reviews expressing `disappointment`, `anger_frustration`, or `disgust` and falling `far_below_expectations` are almost universally negative. Reviews expressing `joy_delight` and `exceeded_expectations` are almost universally positive.
2. **Recommendation stance closely mirrors label**: implicitly or explicitly negative stances capture 103/125 negatives; positive stances capture 110/125 positives.
3. **Defect presence is a negative-specific signal**: 40% of negative reviews cite a concrete defect (functional failure, breakage, etc.) versus 2% of positives.
4. **Performance/accuracy concerns drive negative quality assessments**; positive reviews more often address content quality.
5. **Product category provides secondary context**: physical products carry more defects and negatives; music skews positive, likely reflecting taste-based satisfaction.
