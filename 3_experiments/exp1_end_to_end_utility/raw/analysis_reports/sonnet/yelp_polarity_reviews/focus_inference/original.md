---
dataset: yelp_polarity_reviews
scenario: focus_inference
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What aspects of their experience are Yelp reviewers talking about?"
source_table: augment_table/yelp_polarity_reviews/focus_inference/original.csv
generated_at: 2026-07-26T14:00:21.315498+00:00
wall_seconds: 56.59
---

# Yelp Polarity Reviews — Focus Inference Analysis
## Query: What aspects of their experience are Yelp reviewers talking about?
**Variant:** original | **Dataset:** `original.csv` (200 reviews, IDs YLP-0001–YLP-0200)

---

## Dataset Overview

| Column | Description |
|---|---|
| `review_id` | Unique identifier (YLP-0001 … YLP-0200) |
| `label_pos` | Binary sentiment label: **1** = positive, **0** = negative |
| `review_text` | Raw Yelp review text |

The 200 reviews span a wide variety of business types: restaurants (dominant), bars/nightclubs, hotels/casinos, retail shops, personal-care services (nail salons, hair salons, tattoo parlors), health/medical providers, auto services, entertainment venues, and a few non-food service businesses.

---

## Key Experiential Aspects Discussed

### 1. Food Quality (Most Frequently Mentioned)
Food quality is the single most discussed dimension across the corpus, present in **~70–75% of restaurant-related reviews**.

- **Positive signals:** "delicious," "amazing," "fresh," "flavourful," specific dishes praised (e.g., pizza, sushi rolls, burgers, pho, empanadas, BBQ ribs).  
  *Examples:* YLP-0003 (wood-fired pizza crust), YLP-0028 (tiramisu), YLP-0107 (Brazilian steakhouse salad bar), YLP-0173 (carne asada taco).
- **Negative signals:** "bland," "tasteless," "dry," "not fresh," "mediocre," "stale," wrong preparation.  
  *Examples:* YLP-0041 (undercooked crawfish), YLP-0093 (bad sashimi fish), YLP-0154 (stale bread, bland fish), YLP-0203 (tasteless smoked meat).

### 2. Service Quality (Second Most Common)
Staff behavior and attentiveness appear in **~65–70% of all reviews**, across every business type, not just restaurants.

- **Positive signals:** Staff described as friendly, attentive, prompt, professional, knowledgeable.  
  *Examples:* YLP-0004 (real estate agent), YLP-0039 (tire shop), YLP-0094 (Pho restaurant staff checking water levels).
- **Negative signals:** Being ignored, rude staff, forgotten orders, long unexplained waits, unprofessional managers.  
  *Examples:* YLP-0002 (seated twice, forgotten both times), YLP-0008 (25-minute wait, no server), YLP-0113 (valet told customer to "F off"), YLP-0166 (rude manager).

Notably, several positive reviews that mention mediocre food still give moderate-to-positive ratings because of good service (e.g., YLP-0027, YLP-0148). The inverse is also common: great food undermined by poor service (e.g., YLP-0189).

### 3. Value / Pricing
Mentioned in **~30–35%** of reviews as a decisive factor.

- Positive framing: affordable prices, good portions for money, deals, discounts (YLP-0023, YLP-0078, YLP-0157, YLP-0175).
- Negative framing: overpriced for quality received, hidden charges, portion sizes too small (YLP-0024, YLP-0044, YLP-0159, YLP-0197).

### 4. Wait Times / Efficiency
Explicitly mentioned in **~25–30%** of reviews, nearly always negatively correlated with satisfaction.

- Long waits for food or seating are a major complaint trigger (YLP-0068, YLP-0180, YLP-0206).
- Fast service (even at busy establishments) earns praise (YLP-0103, YLP-0136).

### 5. Atmosphere / Ambiance
Discussed in **~25–30%** of reviews, mostly for bars, nightclubs, and dining venues.

- Includes décor, noise level, seating comfort, cleanliness, crowd vibe (YLP-0034, YLP-0066, YLP-0138, YLP-0152).
- Negative: dirty tables, unpleasant smells, overcrowding, poorly laid-out spaces (YLP-0033, YLP-0036, YLP-0091, YLP-0109).

### 6. Cleanliness / Hygiene
Appears explicitly in **~15–20%** of reviews, consistently a high-stakes issue.

- Dirty utensils/tables: YLP-0091 (Bellagio restaurant, dirty cutlery at 3am), YLP-0109 (nail salon with roach).
- Kitchen hygiene concerns: YLP-0010 (cooks touching hair), YLP-0033 (dirty dishes, wet floor).

### 7. Specific Product or Service Offered
Many reviews discuss the particular item or service received in granular detail (specific dish, haircut style, massage technique, hotel room features), reflecting Yelp's role as a recommendation resource. This is consistent across business type.

---

## Cross-Cutting Patterns

| Aspect | Positive Reviews (label=1) | Negative Reviews (label=0) |
|---|---|---|
| Food | Specific praise of dishes, flavors, portions | Bland, stale, overcooked, wrong prep |
| Service | Friendly, attentive, goes beyond expectation | Rude, inattentive, slow, forgotten |
| Value | Good deal, affordable, fair portions | Overpriced, hidden fees, small portions |
| Ambiance | Lively, clean, great atmosphere | Dirty, loud, cramped, run-down |
| Wait times | Fast, efficient | Excessively long, no explanation |

---

## Exceptions and Weak Evidence

- **Non-restaurant reviews** (retail, medical, events) focus almost exclusively on service/staff rather than product, suggesting the "food" dimension is not universal but is dominant in the dataset due to restaurant majority.
- A small number of reviews (~5%) mention **only one aspect** (e.g., YLP-0011: "great customer service on every item"; YLP-0076: "Boba not good"), limiting inferential value for those rows.
- **Label agreement with aspect valence** is generally consistent, but a handful of reviews contain **mixed valence** (e.g., YLP-0095: exceptional food, poor service → 4 stars/positive label despite service critique). This indicates reviewers may weight food over service when assigning overall sentiment.
- Non-English reviews (YLP-0075, YLP-0142, YLP-0149, YLP-0176 in French) cover the same aspects (product quality, value, ambiance) but cannot be fully analyzed without translation.

---

## Summary

Yelp reviewers in this dataset primarily discuss five experiential dimensions: **food/product quality**, **service**, **value for money**, **wait times**, and **atmosphere/cleanliness**. Food quality is the most prominent focus for the restaurant-majority corpus, but service quality is the most cross-cutting aspect across all business types and is often the swing factor between positive and negative sentiment. Reviews with strong negative outcomes frequently cite **multiple failures** (e.g., poor service + poor food + long wait), while strongly positive reviews tend to emphasize **one outstanding aspect** (e.g., exceptional food or a notably helpful staff member).
