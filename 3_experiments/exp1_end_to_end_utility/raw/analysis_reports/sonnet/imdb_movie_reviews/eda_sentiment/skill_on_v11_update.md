---
dataset: imdb_movie_reviews
scenario: eda_sentiment
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review themes differ between positive and negative IMDb sentiment?"
source_table: augment_table/imdb_movie_reviews/eda_sentiment/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:22:45.158677+00:00
wall_seconds: 41.95
---

# IMDb Review Themes: Positive vs. Negative Sentiment Analysis

## Dataset Overview
- **250 reviews**, perfectly balanced: 125 positive (`label_pos=1`) and 125 negative (`label_pos=0`)
- Theme dimensions captured: verdict tone, recommendation stance, emotional impact, acting/directing assessments, primary praise/criticism targets, and comparison references

---

## 1. Verdict Tone & Recommendation Stance

| Dimension | Negative Reviews | Positive Reviews |
|---|---|---|
| Strongly negative/positive tone | 65 (52%) strongly negative | 68 (54%) strongly positive |
| Mixed tone | 13 (10%) | 11 (9%) |
| Recommend explicitly | 46 explicit discourage | 24 explicit recommend |
| Recommend implicitly | 64 implicit discourage | 90 implicit recommend |

**Pattern:** Both groups skew toward strong tones, but negative reviewers are more likely to *explicitly* discourage (46 vs. 24), while positive reviewers more often rely on *implicit* recommendation (90 vs. 64). A small but notable overlap exists: 7 negative reviews carry implicit-recommend stances, and 6 positive reviews carry implicit-discourage stances, suggesting nuanced or mixed experiences.

---

## 2. Emotional Impact

| Emotion | Negative (n=125) | Positive (n=125) |
|---|---|---|
| Strong negative | 59 (47%) | 6 (5%) |
| Mild negative | 53 (42%) | 6 (5%) |
| Mild positive | 7 (6%) | 68 (54%) |
| Strong positive | 0 | 46 (37%) |
| Neutral/detached | 6 (5%) | 5 (4%) |

**Pattern:** Negative reviews concentrate heavily in the negative emotion range (89% combined mild+strong negative), while positive reviews lean toward mild rather than strong positive emotion (54% mild vs. 37% strong). This suggests positive reviewers express enthusiasm more moderately, whereas negative reviewers are more uniformly dysphoric.

---

## 3. Acting & Directing Assessments

| Assessment | Negative | Positive |
|---|---|---|
| Acting: criticised | 64 (51%) | 1 (1%) |
| Acting: praised | 3 (2%) | 60 (48%) |
| Acting: mixed | 7 (6%) | 5 (4%) |
| Acting: not assessed | 51 (41%) | 59 (47%) |
| Directing: criticised | 83 (66%) | 1 (1%) |
| Directing: praised | 2 (2%) | 49 (39%) |
| Directing: not assessed | ~37 | ~68 |

**Pattern:** Directing/technical quality is the **most discriminating dimension**: 66% of negative reviews explicitly criticise it, vs. only 1% of positive reviews. Acting criticism is also strongly negative-associated (51% vs. 1%). Notably, acting/directing go unassessed more often in positive reviews — positive reviewers tend to focus on what engaged them (story, performance highlights) rather than technical critique.

---

## 4. Primary Praise & Criticism Targets

### Praise Targets
| Target | Negative | Positive |
|---|---|---|
| Not present | 111 (89%) | 15 (12%) |
| Story/plot | 5 | 31 (25%) |
| Specific actor | 4 | 23 (18%) |
| Acting (general) | 2 | 23 (18%) |
| Writing/script | 0 | 10 (8%) |
| Atmosphere/tone | 1 | 8 (6%) |

### Criticism Targets
| Target | Negative | Positive |
|---|---|---|
| Not present | 30 (24%) | 119 (95%) |
| Writing/script | 41 (33%) | 1 |
| Acting | 23 (18%) | 0 |
| Story/plot | 13 (10%) | 3 |
| Directing/pacing | 12 (10%) | 2 |

**Pattern:** The clearest thematic contrast: **negative reviews most frequently target writing/script as their primary complaint** (33%), followed by acting (18%), story (10%), and pacing (10%). **Positive reviews distribute praise broadly** across story, specific actors, general acting, and script — suggesting no single element dominates positive engagement. The 30 negative reviews with no primary criticism target suggest some reviewers criticise holistically or are hard to categorise.

---

## 5. Comparison References

| Reference Type | Negative | Positive |
|---|---|---|
| No comparison | 79 (63%) | 82 (66%) |
| Unfavourable comparison | 42 (34%) | 6 (5%) |
| Favourable comparison | 0 | 28 (22%) |
| Neutral reference | 4 | 9 |

**Pattern:** Negative reviewers make **unfavourable comparisons** prominently (34% of negative reviews), benchmarking the film against better works. Positive reviewers use **favourable comparisons** (22%), placing the film alongside respected titles. Most reviews in both groups make no explicit comparison, so this is a secondary theme.

---

## 6. Key Takeaways

1. **Writing/script flaws** are the dominant theme in negative reviews (33% primary criticism), while no single element dominates in positive reviews — positive engagement is more diffuse.
2. **Directing/technical criticism** is the sharpest discriminator: 66% of negative reviews criticise it vs. near-zero in positive.
3. Negative reviewers are more likely to **explicitly discourage** and use **unfavourable comparisons**; positive reviewers more often rely on implicit endorsement.
4. **Emotional intensity is asymmetric**: negative reviewers are more uniformly strongly negative, while positive reviewers cluster at "mild positive."
5. **Exceptions to note**: ~10% of reviews in each group carry mixed verdict tones, and small minorities of negative reviews contain praise targets (13%) or recommend stances (8%), indicating that even unfavorable reviews can acknowledge partial merits.
