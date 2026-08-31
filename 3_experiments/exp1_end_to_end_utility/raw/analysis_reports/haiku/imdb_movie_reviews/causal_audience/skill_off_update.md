---
dataset: imdb_movie_reviews
scenario: causal_audience
variant: skill_off
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: causal_attribution
focus_variable: "audience_dissatisfaction"
query: "Why are IMDb audiences dissatisfied?"
source_table: augment_table/imdb_movie_reviews/causal_audience/haiku__skill_off_update.csv
generated_at: 2026-07-28T13:23:35.692680+00:00
wall_seconds: 26.05
---

# IMDb Audience Dissatisfaction Analysis  
**Focus: skill_off**

## Executive Summary

This analysis examines what drives audience dissatisfaction with movies on IMDb, using 125 negative reviews annotated with performance indicators. The primary drivers of negative sentiment are **acting quality issues** and **production problems**, occurring far more frequently in dissatisfied reviews than in positive ones.

## Key Findings

### 1. Acting Quality Is the Dominant Factor  
The most prominent signal of audience dissatisfaction is **acting performance issues**:
- **36.0%** of negative reviews contain acting complaints (45 out of 125)
- Only **6.4%** of positive reviews mention acting problems (8 out of 125)
- **Difference: +29.6 percentage points**

This is the strongest single differentiator in the dataset. Reviewers explicitly criticize wooden performances, miscast actors, lack of chemistry between leads, and over-acting or under-acting that breaks immersion. Example complaints include "stiff acting," "terrible acting," and "no chemistry between the 2 main stars."

### 2. Production Quality Problems  
Production quality is the second most significant factor:
- **20.8%** of negative reviews flag production issues (26 out of 125)
- **15.2%** of positive reviews contain such signals (19 out of 125)
- **Difference: +5.6 percentage points**

Problems cited include poor cinematography, low-quality visual effects, grainy picture quality, inadequate sound design, and overall technical incompetence. This suggests audiences notice and penalize technical shortcomings.

### 3. Character Development Concerns  
While present in both negative and positive reviews, character depth issues appear slightly more often in negative feedback:
- **23.2%** of negative reviews mention character depth problems (29 out of 125)
- **18.4%** of positive reviews include character signals (23 out of 125)
- **Difference: +4.8 percentage points**

Audiences express dissatisfaction when characters lack complexity, when character arcs are underdeveloped, or when character actions seem unmotivated.

### 4. Writing Quality and Pacing Rarely Appear  
Surprisingly weak signals in negative reviews:
- **Writing quality:** Only 6.4% of negative reviews (8 out of 125)
- **Pacing issues:** Only 4.0% of negative reviews (5 out of 125)

These low frequencies suggest either that acting and production problems overshadow writing issues in reviewer consciousness, or that poor writing is often attributed to other factors.

## Causal Interpretation

The **skill_off** variant label indicates the model is tested without causal attribution refinements. The data reveals a clear hierarchy of dissatisfaction triggers:

1. **Actor performance** (highest impact)
2. **Production execution** (medium impact)
3. **Character development** (medium impact)
4. **Script quality and pacing** (low impact)

## Conclusion

IMDb audiences are most dissatisfied when they encounter **poor acting performances** and **production quality failures**. These technical and performance dimensions drive negative sentiment more consistently than narrative factors. Addressing casting decisions and maintaining production standards would likely have the greatest impact on audience satisfaction.
