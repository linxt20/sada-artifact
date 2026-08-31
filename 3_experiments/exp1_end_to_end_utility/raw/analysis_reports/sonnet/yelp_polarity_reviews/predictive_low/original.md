---
dataset: yelp_polarity_reviews
scenario: predictive_low
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict low Yelp user satisfaction?"
source_table: augment_table/yelp_polarity_reviews/predictive_low/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/yelp_polarity_reviews__predictive_low/analyses/original/analysis.md
wall_seconds: 80.98
---

# What Review Signals Predict Low Yelp User Satisfaction?

## Dataset Overview

The dataset (`yelp_polarity_reviews__predictive_low.csv`) contains **250 Yelp reviews** spanning restaurants, hotels, nightclubs, service businesses, and retail. Each row has three columns:

| Column | Type | Description |
|---|---|---|
| `review_id` | string | Unique identifier (YLP-0001 … YLP-0250) |
| `label_pos` | binary (0/1) | Focus variable — **0 = negative/low satisfaction**, 1 = positive |
| `review_text` | free text | Full review body |

Of the 250 reviews, approximately **105–115** carry `label_pos = 0` (low satisfaction) and ~135–145 carry `label_pos = 1` (positive), giving a modestly imbalanced but workable split. All predictive signal must be extracted from `review_text`, as no structured numeric or categorical features are present beyond the label.

---

## Signal Categories That Predict `label_pos = 0` (Low Satisfaction)

### 1. Service Failure Language (Strongest Signal)

The most consistent textual marker of low-satisfaction reviews is explicit complaint vocabulary around staff behaviour and wait times.

**Lexical markers observed:**

- **Absolute superlatives in negative framing**: *"worst service I've ever had"* (YLP-0002), *"worst customer service ever"* (YLP-0113), *"horrible service"* (YLP-0008, YLP-0035, YLP-0087, YLP-0120), *"terrible service"* (YLP-0189)
- **Explicit wait-time grievances**: Being forgotten after seating (YLP-0002), 25-minute waits with no staff contact (YLP-0008), 45-minute waits at a bar (YLP-0018), 20-minute food waits (YLP-0035, YLP-0068), repeated staff inattention (YLP-0180)
- **Staff rudeness and dismissiveness**: Rude employees (YLP-0021, YLP-0080, YLP-0097, YLP-0113, YLP-0159), hostile managers (YLP-0166), unprofessional phone interactions (YLP-0019, YLP-0086)
- **Abandonment / being ignored**: *"No one came to take our order"* (YLP-0008), *"forgot we were there"* (YLP-0002), *"she just disappeared on us"* (YLP-0180)

> **Takeaway**: Reviews where service is the primary subject — especially those using absolute negative evaluators (*"worst," "horrible," "terrible"*) or time-delay narratives — are highly predictive of `label_pos = 0`.

---

### 2. Food Quality Complaints

Poor food quality is the second most common driver of low labels, typically co-occurring with — but also independent of — service complaints.

**Recurring signals:**

- **Freshness / hygiene concerns**: Stale bread (YLP-0154), dirty cutlery (YLP-0091), dirty tables (YLP-0007, YLP-0033), roaches (YLP-0109), unsanitary kitchen (YLP-0102), food not cooked properly (YLP-0041), bad fish / sent food back (YLP-0093)
- **Flavour failure phrases**: *"tasteless"* (YLP-0088), *"bland"* (YLP-0203, YLP-0195, YLP-0088), *"mediocre"* (YLP-0032, YLP-0047, YLP-0117), *"nothing special"* (YLP-0154), *"no flavor"* (YLP-0203)
- **Temperature failures**: *"cold"* food (YLP-0077, YLP-0247), *"lukewarm"* (YLP-0219)
- **Value mismatch**: Expensive dishes that fail to deliver (*"for 30 bucks per person"* with mediocre food, YLP-0038; overpriced and poor quality, YLP-0032, YLP-0154, YLP-0105)

---

### 3. Price/Value Dissatisfaction

Standalone price complaints without commensurate quality are a reliable low-label signal.

Examples: being surprised by hidden charges (YLP-0012), feeling ripped off (YLP-0044, YLP-0197), excessive rental-car fees (YLP-0197, YLP-0233), overpriced drinks with little alcohol (YLP-0222), guacamole upcharges (YLP-0044).

**Key phrase pattern**: *"overpriced"* + a quality qualifier like *"mediocre," "not worth it,"* or *"nothing special"* is a near-certain negative signal. *"Overpriced"* alone is weaker — some positive reviews (YLP-0248) acknowledge high prices while remaining satisfied.

---

### 4. Structural Complaint Formats

Negative reviews use distinctive narrative structures:

- **Pros/Cons lists with empty Pros**: *"Pros: none"* (YLP-0005) immediately signals `label_pos = 0`
- **Conditional return statements**: *"I will never go back"* (YLP-0008), *"won't be back"* (YLP-0127), *"I would not go back"* (YLP-0165), *"I probably won't be back"* (YLP-0015)
- **Direct deterrence to others**: *"Don't go here"* (YLP-0022), *"Nope. Don't do it"* (YLP-0127), *"JUST SAY NO!"* (YLP-0102)
- **Star-override intent**: *"If I could give this place negative stars"* (YLP-0024), *"Zero stars is unavailable"* (YLP-0087), *"I would give them negative stars"* (YLP-0224)

These phrases are highly specific to `label_pos = 0` and function as near-deterministic classifiers.

---

### 5. Facility / Cleanliness Complaints

Cleanliness issues consistently co-occur with low labels:

- Dirty tables and chairs (YLP-0007, YLP-0033, YLP-0219)
- Foul smells (YLP-0219)
- Visible pests or unsanitary conditions (YLP-0102, YLP-0109)
- Run-down facilities (YLP-0013, YLP-0185)
- Unclean hotel rooms (YLP-0172, YLP-0223)

---

### 6. Organisational / Process Failures

These are prominent in hotel, healthcare, and service-business reviews:

- Long waits with no apology (YLP-0240, YLP-0068)
- Booking/reservation errors (YLP-0013, YLP-0156)
- Hidden fees and billing surprises (YLP-0197, YLP-0233)
- Lack of communication from service providers (YLP-0085)

---

## Positive Contrasts (What Is Absent in Low-Satisfaction Reviews)

High-satisfaction (`label_pos = 1`) reviews share consistent features that are largely absent in negatives:

- Specific staff name mentions in positive context (*"Alex made a special effort"*, *"Lee is amazing"*)
- Food texture/flavour enthusiasm (*"delicious," "amazing," "to die for"*)
- Unprompted return intent (*"will definitely be back," "can't wait to come back"*)
- Comparative benchmarking (*"best buffet in Vegas," "best tiramisu I have ever eaten"*)

---

## Exceptions and Weak-Evidence Notes

- **Mixed reviews are noisy**: Several `label_pos = 0` reviews acknowledge positives (good service but bad food, or good food but terrible service). Service alone or food alone can drive a low label even when the other dimension is adequate (YLP-0041: food was the issue; YLP-0035: service caused a low label despite food being "usually good").
- **Short negative reviews** (*"Boba not good"* — YLP-0076; *"Horrible service. Don't bother stopping here!"* — YLP-0120) are highly reliable low-label signals despite minimal length, making review length a weak predictor alone.
- **Sarcasm and hedged complaints** (*"I mean they forgot me! Twice!"* — YLP-0002) require semantic understanding beyond simple keyword matching; purely lexical models may underperform on these.
- **Non-English reviews** (French, YLP-0075, YLP-0142, YLP-0149, YLP-0176) are present in both label classes and require language-aware modelling.
- **Overpriced alone is insufficient**: YLP-0248 (`label_pos = 1`) still rated positively despite acknowledging high prices. The combination of *overpriced* + *poor quality/poor service* is the signal, not price complaint alone.
- **Dataset scope**: With 250 samples, effect sizes are directionally reliable but not statistically precise. No numeric engagement features (useful counts, photos) are available to augment text signals.

---

## Summary Table

| Signal Category | Example Phrases | Predictive Strength |
|---|---|---|
| Service failure superlatives | *"worst service ever," "horrible service"* | Very High |
| Non-return / deterrence statements | *"I will never go back," "Don't go here"* | Very High |
| Negative star-override intent | *"would give zero/negative stars"* | Very High |
| Wait-time grievance narratives | *"waited 25 min, no one came"* | High |
| Staff rudeness references | *"rude," "dismissive," "attitude"* | High |
| Food quality failures | *"bland," "tasteless," "cold," "stale"* | High |
| Hygiene / cleanliness issues | dirty facilities, pests, unclean cutlery | High |
| Price + quality mismatch | *"overpriced"* + negative quality qualifier | Moderate–High |
| Pros/Cons format with empty Pros | *"Pros: none"* | Very High (when present) |
| Mediocre / "just ok" language alone | *"mediocre," "just ok," "nothing special"* | Moderate |
