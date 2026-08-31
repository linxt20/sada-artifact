---
dataset: imdb_movie_reviews
scenario: causal_audience
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "audience_dissatisfaction"
query: "Why are IMDb audiences dissatisfied?"
source_table: augment_table/imdb_movie_reviews/causal_audience/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:22:13.509748+00:00
wall_seconds: 33.3
---

# IMDb Movie Reviews: Why Are Audiences Dissatisfied?

## Overview

Analysis of 125 negative reviews reveals concrete patterns in audience dissatisfaction. The most striking finding is that **60% of dissatisfied audiences cite weak or problematic plots** as the primary source of their frustration, while **44.8% report emotional engagement failures**. These two dimensions—narrative and emotional—dominate audience complaints.

## Key Drivers of Dissatisfaction

### 1. Plot Issues (Dominant Factor)

**Weak plots** are the leading complaint, appearing in **75 of 125 negative reviews (60%)**. This represents a dramatic contrast to positive reviews, where weak plot citations drop to 9.6%. Audiences express dissatisfaction with:

- **Predictable or unoriginal storylines**: Reviewers repeatedly note "by the numbers" plots and derivative premises
- **Incoherent or poorly structured narratives**: 7 reviews (5.6%) specifically cite confusing, disjointed storytelling where "nothing makes sense"
- **Poorly paced execution**: Events feel rushed, tedious, or lack buildup to meaningful climaxes
- **Insufficient plot logic**: Characters behave illogically; narrative threads remain unresolved

**Representative examples**:
- *"The whole movie feels like a random slide show that goes nowhere"* 
- *"The story has been built on a foundation which is ludicrously impossible"*
- *"Nothing funny happens for a while...you won't have to laugh because the movie is funny, but because the story is pathetic"*

### 2. Emotional Engagement Failures (Secondary but Significant)

**Failure to move the audience** is the second major complaint, cited in **56 of 125 negative reviews (44.8%)**—nearly 11x more frequent than in positive reviews (4%). Audiences describe:

- **Lack of emotional resonance**: Reviews express boredom, disconnection, or numbness despite engaging subject matter
- **Unbelievable character motivation** (11.2%): Characters make inexplicable decisions that undermine narrative credibility
- **Unearned emotional moments** (4.8%): Attempts at pathos or sentiment feel manipulative or hollow
- **Forced sentiment** (1.6%): Emotions inserted without proper character development

**Representative examples**:
- *"It's so boring I nearly fell asleep"*
- *"Why would a strong, middle-aged woman do those things? The answer is she wouldn't"*
- *"The script...hasn't an iota of good humor"*

### 3. Additional Writing Problems

- **Poor dialogue** (8%): While less frequent than plot issues, weak writing including clichéd lines and stilted delivery appears in 10 reviews
- **Derivative concepts** (2.4%): A few audiences cite unoriginal premises borrowed from other films

## Comparative Context

The contrast with positive reviews is stark:
- In positive reviews (n=125), weak plot mentions drop to 9.6%
- Emotional failures in positive reviews occur in only 4% of cases
- This 6-to-11x difference indicates these factors are genuinely differentiating

## Nuances and Exceptions

- Some dissatisfied viewers acknowledge competent **technical aspects** (cinematography, directing technique) while still rating movies negatively due to story/emotional gaps
- A small subset of negative reviews cite issues beyond plot/emotion (e.g., poor acting, offensive content), suggesting audience dissatisfaction stems from multiple pathways
- Notably, 45 negative reviews (36%) cite **neither** plot problems nor emotional failures in their labeled categories, pointing to other unmeasured dissatisfaction drivers (e.g., casting, pacing outside of plot structure, genre misalignment)

## Conclusion

IMDb audiences are most dissatisfied when films present **weak, predictable, or incoherent plots (60%)** and fail to **emotionally engage viewers (44.8%)**. These two dimensions are not independent: weak plots often prevent audiences from forming emotional connections to characters and stakes. Audiences do not simply want competent technical filmmaking—they demand narratives with logical coherence, originality, or compelling development, paired with authentic emotional investment. The severity of this dissatisfaction is evidenced by harsh, emotional language in reviews and explicit statements that audiences regret watching.
