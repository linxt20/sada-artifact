---
dataset: imdb_movie_reviews
scenario: predictive_negative
variant: original
model: substrate-claude-sonnet-4-6
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict negative IMDb audience satisfaction?"
source_table: augment_table/imdb_movie_reviews/predictive_negative/original.csv
source_report: dataset_portion_2/substrate-claude-sonnet-4-6/imdb_movie_reviews__predictive_negative/analyses/original/analysis.md
wall_seconds: 76.32
---

# What Review Signals Predict Negative IMDb Audience Satisfaction?

## Dataset Overview

- **Columns:** `review_id`, `label_pos`, `review_text`
- **Focus variable:** `label_pos` — binary label where **0 = negative** review (dissatisfied audience), **1 = positive** review
- **Source:** IMDb user reviews covering films, TV series, and other entertainment content
- The dataset is structured for binary sentiment prediction; `review_text` is the sole predictor available

---

## Key Signals That Predict Negative Satisfaction (`label_pos = 0`)

### 1. Explicit Failure Vocabulary in the Opening Sentence
Negative reviews consistently open with direct condemnation. Common openers include phrases such as:
- *"awful, simply awful"* (IMDB-0099)
- *"Painful is the only word to describe this awful rendition"* (IMDB-0044)
- *"I just wondering what is the purpose of making movies like this?"* (IMDB-0052)
- *"This is one of the worst movies i've ever encountered"* (IMDB-0114)

**Signal:** Any review whose first sentence contains extreme negative adjectives (*awful, atrocious, abysmal, terrible, horrible, dreadful, horrid, godawful*) is a strong predictor of `label_pos = 0`. Positive reviews rarely use such language in their opening.

---

### 2. Complaints About Core Craft Dimensions
Negative reviews cluster complaints around the same set of film-craft dimensions:

| Dimension | Exemplar negative phrase |
|---|---|
| Acting | *"wooden acting"*, *"bad acting"*, *"no chemistry"* |
| Script / Writing | *"bad plot"*, *"cretinous dialog"*, *"hackneyed and clichéd"* |
| Pacing | *"extremely slow"*, *"boring"*, *"predictable"*, *"nothing ever really did [happen]"* |
| Special effects | *"worst CGI ever"*, *"effects suck"*, *"looked godawful"* |
| Direction | *"poor lighting"*, *"messy"*, *"incoherent"* |

Negative reviews often cite **multiple** craft failures simultaneously (IMDB-0105: *"writing too reliant on f-word... acting some of the worst... special effects look godawful"*), whereas positive reviews tend to highlight specific strengths.

---

### 3. Comparative Disappointment / Unmet Expectations
Many negative reviews explicitly state a prior expectation that was not met:
- *"I had high expectations following..."* (IMDB-0038)
- *"I was so excited when I discovered this was available! What a waste of energy!"* (IMDB-0141)
- *"I had high hopes for this movie"* (IMDB-0214)

**Signal:** The phrase pattern *"I had high expectations / I was excited / I couldn't wait — but..."* is reliably associated with `label_pos = 0`.

---

### 4. Time/Money Waste Framing
Negative reviewers frame the experience as a loss of time or money:
- *"Do not waste your time with this movie"* (IMDB-0102)
- *"It was the WORST \$4.50 I've ever spent"* (IMDB-0179)
- *"I wasted an hour and a half of my life"* (IMDB-0214)
- *"Save your time. It's not even worth the time it takes to watch it for free."* (IMDB-0079)

**Signal:** Explicit cost-of-viewing framing (time, money, opportunity cost) is almost exclusively in negative reviews.

---

### 5. Strong Recommendation Against Viewing
Negative reviews frequently close with active anti-recommendations:
- *"Do not buy this film!"* (IMDB-0180)
- *"Please do not even bother with this gut wrenching..."* (IMDB-0044)
- *"Stay away from Whipped"* (IMDB-0131)
- *"Don't waste your money on this"* (IMDB-0179)

Positive reviews close with pro-recommendations (*"highly recommended"*, *"a must see"*, *"check it out"*). The direction of the closing call-to-action is a reliable discriminating signal.

---

### 6. Hyperbolic Superlative Negativity
Negative reviews use superlatives of failure to emphasize intensity:
- *"the worst movie I have ever seen"* (IMDB-0230)
- *"probably the worst of the trilogy (perhaps of all time)"* (IMDB-0105)
- *"one of the most god awful wrestlemanias ever"* (IMDB-0068)

**Signal:** Superlative phrases anchored to worst/ever/all time, when negative in valence, are almost exclusively in `label_pos = 0` reviews.

---

### 7. Plot Incoherence / Predictability Complaints
Two related but distinct failure modes appear frequently:
- **Incoherence:** *"actions frequently seem to have no relation to each other"* (IMDB-0187), *"incoherent"*, *"messy, disjointed order"*
- **Predictability:** *"beyond predictable"* (IMDB-0176), *"predictable and well-trodden premise"* (IMDB-0003), *"you can almost predict how the story goes"* (IMDB-0029)

These two failure types are somewhat opposite but both reliably negative signals.

---

## Signals Present in Negative Reviews But With Weaker Predictive Value

- **Short review length:** Some very short reviews are negative (IMDB-0103: *"This is a disclaimer; WATCH AT YOUR PERIL!"*), but some very short reviews are also positive (IMDB-0036, IMDB-0120). Length alone is a weak predictor.
- **Profanity:** Negative reviews sometimes use profanity (*"pile of crap"*, *"crap"*), but positive reviews also occasionally use informal strong language. Profanity is a moderately useful but noisy signal.
- **References to low budget or production issues:** Most negative reviews mentioning low budgets or poor technical quality are `label_pos = 0`, but some positive reviews explicitly enjoy low-budget charm (IMDB-0087, IMDB-0228).

---

## Notable Exceptions

- **Ambivalent reviews:** Several `label_pos = 0` reviews acknowledge partial merit (*"not the worst"*, *"the acting was passable"*, IMDB-0079) — these are harder to classify from surface vocabulary alone.
- **Genre-specific tolerance:** Some reviewers give negative labels to films they partly enjoyed (e.g., IMDB-0067: *"a worthwhile and reasonably entertaining watch but over-rated"*). The `label_pos = 0` classification in these cases is driven by the overall judgment, not every sentence.
- **Fan-disappointment reviews:** Reviews from genre fans who expected more (IMDB-0027: *"This movie is missing a lot of the songs from the musical"*) can be ambiguous in tone but end negative.

---

## Summary: Most Reliable Predictive Signals

| Signal | Direction | Strength |
|---|---|---|
| Extreme negative adjectives in opening | → negative | **High** |
| Multiple craft failures cited together | → negative | **High** |
| "Waste of time/money" framing | → negative | **High** |
| Anti-recommendation closing | → negative | **High** |
| Superlative worst/ever phrases | → negative | **High** |
| Unmet-expectations framing ("I had high hopes...but") | → negative | **High** |
| Predictability complaints | → negative | **Moderate** |
| Profanity | → negative | **Low-Moderate** |
| Short review length | → negative | **Low** |

The strongest composite predictor is: **explicit negative affect vocabulary** (especially opening/closing sentences) combined with **time-or-money-waste framing** and **anti-recommendation directives**. Reviews combining all three are reliably `label_pos = 0` in the visible data.
