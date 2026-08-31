---
dataset: yelp_polarity_reviews
scenario: causal_improve
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: what_if
focus_variable: "user_satisfaction"
query: "How can businesses improve Yelp user satisfaction?"
source_table: augment_table/yelp_polarity_reviews/causal_improve/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/yelp_polarity_reviews__causal_improve/analyses/original/analysis.md
wall_seconds: 84.49
---

# How Can Businesses Improve Yelp User Satisfaction?

## Dataset Overview

The dataset (`yelp_polarity_reviews__causal_improve.csv`) contains **binary-labelled Yelp reviews**: `label_pos = 1` (positive / satisfied) and `label_pos = 0` (negative / dissatisfied). Each row includes a `review_id` and full-text `review_text`. No star ratings, business category, or demographic metadata are present. All findings are grounded in patterns visible across the review texts.

---

## 1. Focus Variable: `label_pos`

`label_pos` is the satisfaction outcome — the target variable for improvement. Patterns extracted from review text identify what drives or destroys this outcome.

---

## 2. Key Drivers of Positive Sentiment (`label_pos = 1`)

### a. Service Quality — Most Frequently Cited Positive Factor
Staff friendliness, attentiveness, and professionalism appear in nearly every positive review:

> *"The employees are always friendly and composed."* (YLP-0001)  
> *"The service was stellar."* (YLP-0028)  
> *"I've never had one bad experience here."* (YLP-0070)  
> *"Service is always excellent, very friendly staff."* (YLP-0162)

**Actionable signal:** Warm, knowledgeable, and attentive staff is the single strongest predictor of a positive label in this dataset.

### b. Food Quality and Freshness
Positive reviews consistently praise freshness, flavour, and portion size:

> *"The food quality was better than I imagined."* (YLP-0132)  
> *"Food is delivered to your table fast and delicious."* (YLP-0136)  
> *"Very good pizza… Crust cooked very well in the wood burning oven."* (YLP-0003)

### c. Value for Money
Reviews frequently reference pricing as fair or surprising:

> *"Reasonably priced."* (YLP-0078)  
> *"For about $6 you get soup, egg roll, crab puff, fried rice and your choice of entree."* (YLP-0157)

### d. Cleanliness and Atmosphere
Positively labelled reviews of hotels, clinics, and restaurants cite cleanliness and pleasant ambience:

> *"The clinic is very clean and not smelly."* (YLP-0134)  
> *"Really nice… clean, stylish, spacious, and comfortable."* (YLP-0226)

### e. Special Touches / Going Above and Beyond
Loyalty programmes, freebies, and personalised service drive sentiment above the baseline:

> *"Sign up for the email list! — you get a free pita."* (YLP-0001)  
> *"Even checked that my wedding band diamonds were secure without me having to ask."* (YLP-0170)  
> *"They filled all 4 tires for me. He didn't ask for a tip."* (YLP-0039)

---

## 3. Key Drivers of Negative Sentiment (`label_pos = 0`)

### a. Poor or Inattentive Service — Dominant Complaint
Service failures dominate negative reviews across every business type:

> *"They forgot we were there. Twice."* (YLP-0002)  
> *"Waited 25 minutes. No one came to take our order."* (YLP-0008)  
> *"Service was horrible!"* (YLP-0008, YLP-0120)  
> *"Asking 6 times for a glass of water is annoying."* (YLP-0048)

**Staff rudeness** is a secondary but potent driver:

> *"One sales representative was extremely rude."* (YLP-0218)  
> *"Lady at the dressing room gave a lot of attitude."* (YLP-0080)  
> *"The worker told me to F off."* (YLP-0113)

### b. Food Quality Failures
Negative reviews cite food that is cold, bland, stale, or improperly prepared:

> *"The roast beef was dry and lacked flavor."* (YLP-0038)  
> *"Burgers were small and cold. Fries arrived cold and over salted."* (YLP-0077)  
> *"The fish was BAD."* (YLP-0093)  
> *"Everything was mediocre."* (YLP-0112)

### c. Hygiene and Cleanliness Issues
Visible dirt, uncleaned tables, pests, and unsanitary conditions directly cause negative labels:

> *"My table was dirty and so were the ones around me."* (YLP-0007)  
> *"I saw a big roach in the corner of the ceiling."* (YLP-0109)  
> *"The cutlery was dirty."* (YLP-0091)

### d. Pricing Transparency and Value Mismatch
Prices that do not match expectations or perceived quality generate strong negative reactions:

> *"Pricing was way off, and they should have announced that on the website."* (YLP-0012)  
> *"For 30 bucks per person, the selection was limited."* (YLP-0038)  
> *"Overpriced, service is bad."* (YLP-0159)

### e. Wait Times and Operational Failures
Long waits without acknowledgement are a reliable negative signal:

> *"Waited at the bar for 45 minutes to order food."* (YLP-0018)  
> *"Sat for over 15 minutes while a man kept saying he'd check on my food."* (YLP-0027)  
> *"Waited over an hour to be seen past our appointment time."* (YLP-0240)

### f. Management Behaviour
Manager indifference or hostile behaviour converts a recoverable complaint into a permanent loss:

> *"All 3 managers are standing at the counter. Not once did one stop by."* (YLP-0068)  
> *"The manager tried to kick me out."* (YLP-0166)

---

## 4. Patterns by Business Context

| Context | Top Positive Factor | Top Negative Factor |
|---|---|---|
| Restaurants / Food | Food quality + fast service | Cold/bland food; slow/absent service |
| Hotels | Cleanliness; upgrade gestures | Rude staff; noisy rooms; hidden charges |
| Bars / Nightclubs | Atmosphere; drink variety | Entry process; crowd management; poor service |
| Service businesses (salons, vets, auto) | Skilled, friendly staff | Incompetence + failure to apologise |
| Retail | Staff knowledge; helpfulness | Rudeness; long wait at counter |

---

## 5. Exceptions and Weak Evidence

- **Food quality alone is not sufficient**: YLP-0027 gives negative despite praising the food because of slow service. YLP-0041 and YLP-0163 show the same pattern. Service can override food in determining `label_pos`.
- **Ambience has mixed causal weight**: Some reviews praise atmosphere yet assign negative labels due to service or food failures (YLP-0166, YLP-0048). Ambience alone rarely drives label = 1 without accompanying service quality.
- **Price sensitivity is contextual**: Reviewers at budget venues tolerate value trade-offs (YLP-0216: "You get what you pay for"). The pricing complaint is strongest when the gap between expectation and reality is not disclosed upfront.
- **Sample composition**: The reviewed sample spans multiple industries (restaurants, hotels, healthcare, retail), so effect sizes for any single industry cannot be precisely estimated from this dataset alone.

---

## 6. Decision-Ready Recommendations

| Priority | Action | Evidence basis |
|---|---|---|
| **High** | Train and retain friendly, attentive staff; empower them to apologise proactively | Dominant factor in both positive and negative labels |
| **High** | Ensure food/product quality consistency — temperature, freshness, seasoning | Cited in the majority of negative food-related reviews |
| **High** | Maintain visible cleanliness (tables, utensils, restrooms, floors) | Hygiene issues immediately trigger negative labels |
| **Medium** | Communicate pricing transparently before service delivery | Pricing surprises disproportionately harm satisfaction |
| **Medium** | Set realistic wait-time expectations and acknowledge delays | Acknowledged waits are tolerated; ignored waits are not |
| **Medium** | Equip managers to intervene and recover service failures | Manager inaction or hostility is a terminal negative signal |
| **Low** | Offer loyalty perks or small unexpected gestures | Mentioned in positive reviews but not a universal expectation |

---

## Summary

Across 200+ labelled Yelp reviews, **service quality** is the single most causally prominent factor for user satisfaction, present in both directions — excellent service generates `label_pos = 1` even when other factors are mediocre, while poor or rude service produces `label_pos = 0` even when food or atmosphere are praised. **Food quality and cleanliness** rank second. Pricing matters primarily as a transparency issue rather than absolute cost. Businesses seeking to improve Yelp ratings should treat staff training and operational responsiveness as their primary levers.
