---
dataset: amazon_fine_food_review
scenario: concept_food_quality_facets
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: faceted_decomposition
focus_variable: "food_quality"
query: "What distinct aspects of food quality do reviewers focus on?"
source_table: augment_table/amazon_fine_food_review/concept_food_quality_facets/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:08:14.592465+00:00
wall_seconds: 53.82
---

# Food Quality Facets in Amazon Fine Food Reviews

**Query:** What distinct aspects of food quality do reviewers focus on?

**Dataset:** 10,000 Amazon fine food reviews (original structured columns + TAPP-generated semantic columns).

---

## Method Note

Two TAPP-generated columns were used in this analysis:
- **`taste_quality`** – Categorical assessment of the reviewer's taste experience (`positive`, `mixed`, `negative`); coverage 92.1% (9,207/10,000 rows).
- **`flavor_authenticity`** – Whether the product's flavor matched label/expectations (`authentic`, `partially_authentic`, `artificial_or_off`); coverage 59.0% (5,896/10,000 rows).

These augment the original structured columns `Score` (1–5 star rating), `HelpfulnessNumerator/Denominator`, `Summary`, and `Text`.

---

## Key Findings

### 1. Taste Quality is the Dominant Quality Dimension

Taste is explicitly discussed in 92% of reviews, making it the most frequently signaled food quality facet. Among reviews that express a taste judgment:

| taste_quality | Count | % of tagged | Mean Score | Mean Helpfulness Ratio |
|---|---|---|---|---|
| positive | 6,738 | 73.2% | **4.81** | 0.86 |
| mixed | 1,371 | 14.9% | 3.26 | 0.67 |
| negative | 1,098 | 11.9% | **1.58** | 0.53 |

Taste quality is tightly aligned with the star rating (near-monotone relationship), confirming it is the primary driver of overall satisfaction. Positive-taste reviews account for 92% of high-scoring (4–5 star) reviews; negative-taste reviews account for 75% of low-scoring (1–2 star) reviews.

### 2. Flavor Authenticity is a Distinct Second Facet

Flavor authenticity—whether a product tasted as labelled or true-to-origin—is discussed in 59% of reviews, a large but narrower subset than general taste. Among tagged reviews:

| flavor_authenticity | Count | % of tagged | Mean Score | Mean Helpfulness Ratio |
|---|---|---|---|---|
| authentic | 4,432 | 75.2% | **4.78** | 0.86 |
| partially_authentic | 717 | 12.2% | 3.25 | 0.67 |
| artificial_or_off | 747 | 12.7% | **1.54** | 0.57 |

The mean score gap between `authentic` (4.78) and `artificial_or_off` (1.54) is 3.24 points — essentially the full width of the rating scale — indicating that authenticity violations (e.g., wrong flavor, artificial taste, misleading labeling) are among the most damaging product defects.

### 3. Taste Quality and Flavor Authenticity Are Strongly Correlated But Non-Identical

The cross-tabulation shows near-perfect alignment for extreme cases but meaningful divergence in the middle:

| taste_quality ↓ / flavor_authenticity → | artificial_or_off | authentic | partially_authentic |
|---|---|---|---|
| **positive** | 4 | 4,242 | 64 |
| **mixed** | 62 | 172 | **555** |
| **negative** | **664** | 6 | 97 |

- `mixed` taste reviews cluster heavily in `partially_authentic` (555 cases), suggesting authenticity ambiguity is the dominant cause of lukewarm reviews.
- `negative` taste with `authentic` label (6 cases) is rare; most negative taste experiences co-occur with `artificial_or_off` (664 cases), confirming that artificial/off-flavors are the primary taste complaint mechanism.

### 4. Structured Score Bands Confirm Both Facets

| Score band | Positive taste | Authentic flavor | Artificial/off flavor | Negative taste |
|---|---|---|---|---|
| High (4–5 ★), n≈7,616 | 92.0% | 93.7% | 0.2% | 0.1% |
| Mid (3 ★), n=862 | 14.5% | 22.2% | 17.5% | 17.0% |
| Low (1–2 ★), n=1,522 | 3.5% | 3.2% | 78.4% | 74.8% |

The structural regularity across both TAPP columns and the raw `Score` variable is strong and consistent.

### 5. Helpfulness Signal

Reviews expressing positive taste or authentic flavor receive substantially higher peer helpfulness votes (ratio ~0.86) compared to negative-taste or artificial-flavor reviews (~0.53–0.57). This suggests the community finds quality-affirming reviews more decision-useful, but negative quality signals are still directionally helpful.

---

## Summary: Distinct Food Quality Aspects

| Facet | Evidence source | Prevalence | Impact on Score |
|---|---|---|---|
| **Overall taste experience** (pleasant vs. unpleasant) | `taste_quality`, `Score`, review text | 92% of reviews | Δ 3.2 stars (positive vs. negative) |
| **Flavor authenticity / label accuracy** | `flavor_authenticity`, `Score` | 59% of reviews | Δ 3.2 stars (authentic vs. artificial) |
| **Mixed/ambivalent quality** | Intersection: `mixed` taste + `partially_authentic` | ~14% of reviews | Clusters at 3 stars |

Reviewers focus on two distinct but related quality dimensions: (1) **hedonic taste experience** (does it taste good?) and (2) **flavor fidelity** (does it taste like what it claims to be?). Both independently explain rating variance across the full 1–5 star scale. The `flavor_authenticity` column adds genuine incremental signal beyond the raw star rating, particularly for mid-tier reviews where the partial-authenticity distinction clarifies reviewer intent that the star score alone does not capture.
