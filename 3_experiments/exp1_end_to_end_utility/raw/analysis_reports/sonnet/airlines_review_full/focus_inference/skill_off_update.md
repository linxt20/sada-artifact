---
dataset: airlines_review_full
scenario: focus_inference
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "Help me understand what's in these airline reviews — I'm not sure which aspect is most worth analyzing."
source_table: augment_table/airlines_review_full/focus_inference/sonnet__skill_off_update.csv
generated_at: 2026-08-03T05:42:12.027003+00:00
wall_seconds: 42.74
---

# Airline Reviews Dataset — Exploratory Analysis

## Dataset at a Glance

| Dimension | Value |
|---|---|
| Reviews | 8,100 |
| Airlines covered | 10+ (Turkish Airlines, Qatar Airways, Emirates, Singapore Airlines, Air France, …) |
| Cabin classes | Economy (68%), Business (26%), Premium Economy (5%), First (1%) |
| Traveller types | Solo Leisure (40%), Couple (23%), Family (19%), Business (17%) |
| Recommendation split | Yes 53% / No 47% |

---

## Column Guide

The dataset blends **raw review fields** (Title, Name, Review Date, Airline, Route, Class, Type of Traveller, Month Flown, Reviews) with **structured sub-ratings** (Seat Comfort, Staff Service, Food & Beverages, Inflight Entertainment, Value For Money, Overall Rating 1–10) and **three augmented/derived columns**:

| Column | What it measures |
|---|---|
| `sentiment_score` | NLP polarity of the free-text review (−1 very negative → +1 very positive) |
| `dominant_complaint` | Most prominent complaint category: `none / staff / delay / seat / food / value / entertainment` |
| `rating_sentiment_gap` | Numerical rating minus sentiment-implied rating (positive = rated higher than tone suggests) |

---

## Most Worth Analyzing: Value For Money Drives Overall Satisfaction

**`Value For Money` has by far the strongest correlation with `Overall Rating` (r = 0.88)**, dwarfing all other sub-ratings.

| Sub-rating | Corr. with Overall Rating |
|---|---|
| Value For Money | **0.88** |
| Staff Service | 0.23 |
| Seat Comfort | 0.21 |
| Food & Beverages | 0.16 |
| Inflight Entertainment | 0.14 |

This means passengers who feel they got fair value almost universally rate the flight highly, regardless of individual service attributes. Analysing what drives perceived value (cabin class, fare paid, route) is therefore the highest-leverage question in this dataset.

---

## Complaint Categories Reveal a Clear Severity Ladder

Complaints are segmented into six types. Reviews with **no dominant complaint** average **7.4/10**; any complaint category drops the rating sharply:

| Dominant Complaint | Mean Overall Rating | Share of Reviews |
|---|---|---|
| none | 7.4 | 64% |
| entertainment | 3.7 | 1% |
| food | 3.5 | 5% |
| seat | 3.2 | 7% |
| staff | 2.3 | 13% |
| delay | 2.0 | 8% |
| **value** | **1.6** | **3%** |

**Value and delay complaints are the most destructive to satisfaction.** Staff complaints are the most *common* complaint category (13% of all reviews), making them a high-frequency and high-impact target.

---

## Sentiment vs. Numeric Ratings

`sentiment_score` correlates strongly with `Overall Rating` (r = 0.74), confirming the free text and numeric ratings are broadly consistent. However, the median `rating_sentiment_gap` is **−0.13** (passengers write slightly more positively than their numeric score implies), and the distribution is wide (std = 0.57). Reviewers who do *not* recommend the airline show a larger gap (−0.36) — suggesting dissatisfied passengers understate negativity in prose relative to their score, or vent in text beyond what the scale captures.

---

## Cabin Class Effect

Higher cabin classes rate consistently better, but the economy/business gap (~1.5 rating points) is meaningful without being dramatic:

| Class | Mean Overall Rating |
|---|---|
| First Class | 7.6 |
| Business Class | 6.7 |
| Premium Economy | 6.0 |
| Economy Class | 5.2 |

This suggests that **Economy satisfaction is structurally lower** and may warrant separate analysis rather than pooling all classes together.

---

## Longer Reviews Signal Dissatisfaction

`review_length` correlates **negatively** with Overall Rating (r = −0.23). Unhappy passengers write more — a useful signal when scanning for at-risk reviews or training classifiers.

---

## Recommendations for Next Steps

1. **Primary analysis:** Investigate what drives `Value For Money` scores across airlines, routes, and cabin classes — this variable unlocks overall satisfaction.
2. **Complaint analysis:** Focus on **staff** complaints (most frequent) and **value/delay** complaints (most damaging). Turkish Airlines and Qatar Airways, which dominate the dataset, deserve separate breakdowns.
3. **Sentiment-gap investigation:** The `rating_sentiment_gap` distribution has heavy tails (range −2 to +2). Extreme gap rows likely contain the richest qualitative insights.
4. **Weak evidence caveat:** Inflight entertainment scores have the lowest correlation with satisfaction (0.14) — this attribute may matter less to most passengers or simply be rated more uniformly.
