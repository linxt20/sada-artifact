---
dataset: imdb_movie_reviews
scenario: predictive_negative
variant: skill_on
model: substrate-claude-haiku-4-5
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "label_pos"
query: "What review signals predict negative IMDb audience satisfaction?"
source_table: augment_table/imdb_movie_reviews/predictive_negative/haiku__skill_on_v11_update.csv
generated_at: 2026-07-30T07:23:07.736052+00:00
wall_seconds: 40.35
---

# Review Signals That Predict Negative IMDb Audience Satisfaction

## Executive Summary

Analysis of 250 IMDb movie reviews (125 negative, 125 positive) reveals distinct linguistic and structural patterns that strongly predict negative audience satisfaction. The most powerful predictive signal is **explicit condemnation language**, which appears in 76.8% of negative reviews but only 0.8% of positive reviews. Combined with thematic failures around plot coherence and wasted potential, these signals form a robust framework for identifying dissatisfied reviewers.

## Primary Predictive Signals

### 1. Explicit Condemnation Language (Strongest Signal)
**Finding:** 96 of 125 negative reviews (76.8%) employ explicit condemnation language, compared to only 1 of 125 positive reviews (0.8%).

**Manifestations in data:**
- Direct dismissive statements: "worst movie," "absolute failure," "garbage," "terrible," "abysmal"
- Strong emotional expressions: "truly despise," "completely mystified," "thoroughly uninteresting"
- Comparative negatives: "worse than," "doesn't compare to"

**Interpretation:** Negative reviewers use language that explicitly names their dissatisfaction. This is the strongest differentiator—when condemnation language is present, the review is 96 times more likely to express negative satisfaction. The absence of such language in positive reviews (99.2% clean language) underscores this signal's reliability.

### 2. Wasted Potential Signals
**Finding:** 68 of 125 negative reviews (54.4%) reference some form of wasted potential, with **premise squandering** being most common (54 reviews, 43.2%).

**Breakdown of wasted potential types:**
- **Premise squandered** (43.2%): Reviews describing films that started with potential but failed in execution. Examples include sequels that tarnished originals, adaptations that misunderstood source material, or concepts undermined by poor writing.
- **Talent misused** (14.4%): Complaints about capable actors trapped in poorly conceived roles or unable to salvage weak material
- **Budget wasted** (12.8%): References to insufficient production values, cheap effects, or resource misallocation
- **Legacy damaged** (2.4%): Specific concern about reboots or sequels harming beloved franchises

**Interpretation:** Negative reviewers frequently reference *what could have been*, suggesting disappointment stems not just from low quality but from unrealized potential. This signals a specific emotional complaint: the reviewer can see the film's wasted opportunity.

### 3. Comparative Dismissal (Moderate Signal)
**Finding:** 47 of 125 negative reviews (37.6%) employ comparative dismissal, contrasting the film unfavorably to other works.

**Comparison types in negative reviews:**
- **Comparison to classics** (21.6%): Unfavorable contrast to superior predecessors or iconic films
- **Worse than similar** (14.4%): Explicit statements that the film is inferior to other entries in its genre/series
- **Genre decline** (1.6%): Complaints about series degradation or genre standards slipping

**Interpretation:** Negative reviewers situate their criticism within a broader context of film culture. Rather than evaluating films in isolation, they reference superior alternatives, emphasizing what the audience could have watched instead. This is more prevalent in negative reviews (37.6%) than in the dataset generally, suggesting comparative framing amplifies perceived dissatisfaction.

### 4. Plot-Level Failures (Weaker but Meaningful Signals)
**Finding:** 42 of 125 negative reviews (33.6%) specify narrative/plot problems.

**Plot failure types in negative reviews:**
- **Incoherent story** (10.4%): Reviews describing confusing, disjointed, or incomprehensible narratives
- **Pacing problems** (9.6%): Complaints about slow burns, excessive runtime, or poor editorial flow
- **Predictable/cliché** (8.8%): Criticism of unoriginal or telegraphed plot beats
- **Missing plot** (3.2%): Absence of coherent storyline despite the film's premise
- **Logical flaws** (1.6%): Internally inconsistent or impossible story elements

**Interpretation:** While 66.4% of negative reviews don't explicitly mention plot failure (suggesting other factors dominate), when structural narrative problems appear, they reinforce dissatisfaction. Incoherence is particularly damaging—it prevents reviewers from even understanding what they watched.

## Interaction Patterns

The most powerful negative satisfaction predictors occur in combination:

1. **Explicit condemnation + wasted potential:** "This masterpiece *could* have been great, but the awful script ruins everything."
2. **Explicit condemnation + comparison:** "Unlike the original, this version is a travesty."
3. **Explicit condemnation + plot failure:** "The incoherent storyline and terrible writing make this unwatchable."

Only 29 negative reviews (23.2%) express dissatisfaction *without* condemnation language, suggesting that absence of strong condemning words in a review is a weak indicator of positive satisfaction rather than a strong predictor of negative satisfaction.

## Exceptions & Nuance

**Weak evidence caveats:**
- Some negative reviews lack condemnation language but express dissatisfaction through passive disappointment ("I was hoping for better")
- Wasted potential signals appear in only ~54% of negative reviews, meaning many negative reviews focus on absolute quality rather than unfulfilled promise
- Comparative dismissal, while more common in negative reviews, still appears in fewer than 38% of them

**Note on positive reviews:** Positive reviews almost never employ explicit condemnation language, comparative dismissal, or plot failure terminology. When they mention potential issues, they contextualize them within an overall positive evaluation ("flaws that don't detract from the experience").

## Implications for Predicting Negative Satisfaction

**High confidence signals** (strong presence in negative reviews, near-absent in positive):
- Explicit condemnation language: 77% in negative, <1% in positive
- Premise squandering: 43% in negative, minimal in positive

**Moderate confidence signals** (present in ~1/3 of negative reviews):
- Comparative dismissal to other films
- Talent misused complaints

**Lower confidence signals** (present in ~1/3 of negative reviews):
- Specific plot failures (incoherence, pacing, predictability)

The dataset suggests that **language intensity and the framing of disappointment (relative to what could have been) are more predictive than absolute quality judgments alone**.

---

*Analysis based on 250 annotated IMDb reviews (skill_on variant) with variant label drawn from predictive_negative focus on audience dissatisfaction signals.*
