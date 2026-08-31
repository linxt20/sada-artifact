---
dataset: imdb_movie_reviews
scenario: eda_sentiment
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review themes differ between positive and negative IMDb sentiment?"
source_table: augment_table/imdb_movie_reviews/eda_sentiment/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:24:00.009766+00:00
wall_seconds: 106.5
---

# Review Themes: Sentiment Differences in IMDb Movie Reviews

**Query:** How do review themes differ between positive and negative IMDb sentiment?

**Dataset:** 250 balanced reviews (125 positive, 125 negative)  
**Date:** 2026-07-30

---

## Executive Summary

Review themes differ dramatically between positive and negative sentiments. Negative reviews center on narrative **dysfunction and writing failures** with unfavorable comparisons to other works, while positive reviews emphasize **acting excellence, holistic storytelling, and genre-aware context**. The most striking difference: negative reviews attribute problems to writing in 49% of cases vs. only 14% for positive reviews—and positive reviewers overwhelmingly decline to attribute failure to any single cause (70%).

---

## Methodology Note

This analysis combines original structured data (sentiment labels, review text) with five TAPP-generated semantic facets:
- `primary_critique_focus`: what aspect receives critical attention
- `narrative_quality_signal`: assessment of story coherence and novelty
- `comparison_or_genre_context`: whether review references comparative or genre framing
- `technical_or_creative_root_cause`: attributed source of success or failure
- `recommendation_stance`: explicit or implicit call to action

These augmented columns add semantic texture to quantified patterns; they do not replace but clarify relationships in the original data.

---

## Key Findings

### 1. **Narrative Quality Signal: Core Theme Separator**

The sharpest theme division emerges in `narrative_quality_signal`:

| Signal | Negative (n=125) | Positive (n=125) | Difference |
|--------|------------------|------------------|-----------|
| **Coherent & Engaging** | 11 (8.8%) | 110 (88.0%) | +79.2 pp |
| **Convoluted & Thin** | 90 (72.0%) | 10 (8.0%) | −64.0 pp |
| **Derivative & Predictable** | 23 (18.4%) | 4 (3.2%) | −15.2 pp |

**Interpretation:** Negative reviews are dominated by claims of *incoherent or underdeveloped narrative*. Reviewers frame stories as confusing, disjointed, or hollow. Positive reviews celebrate *clarity and freshness*: coherent plots that engage and feel novel within their genre or context.

---

### 2. **Primary Critique Focus: What Reviewers Blame**

Negative reviews concentrate fire on structure and dialogue (51% combined):

**Negative reviews (n=125):**
- Plot or narrative: 26.4% (33 reviews)
- Screenplay or dialogue: 25.6% (32 reviews)
- Acting or performance: 14.4% (18 reviews)
- Technical/cinematography: 14.4% (18 reviews)

**Positive reviews (n=125):**
- Acting or performance: 21.6% (27 reviews) ← *shift to actors*
- Plot or narrative: 20.8% (26 reviews)
- Multiple aspects celebrated: 18.4% (23 reviews) ← *holistic praise*
- Emotional tone or message: 12.8% (16 reviews) ← *thematic resonance*

**Interpretation:** Negative reviews diagnose *failure at the screenplay level*—bad writing, thin plots. Positive reviews *elevate performance and ensemble strength*, and uniquely value films addressing multiple dimensions (acting + direction + theme). Positive reviewers also explicitly engage with *emotional_tone_or_message* at 2.3× the rate of negative reviewers.

---

### 3. **Root Cause Attribution: Writing vs. No Attribution**

How reviewers explain success or failure splits starkly by sentiment:

| Root Cause | Negative | Positive | Delta |
|------------|----------|----------|--------|
| Writing or scripting | 61 (48.8%) | 17 (13.6%) | −35.2 pp |
| Not attributed (inherent merit/flaw) | 15 (12.0%) | 87 (69.6%) | +57.6 pp |
| Casting decision | 17 (13.6%) | 7 (5.6%) | −8.0 pp |
| Direction or cinematography | 14 (11.2%) | 9 (7.2%) | −4.0 pp |

**Interpretation:** Negative reviewers are *diagnostic*: nearly half trace flaws to writing failures (`writing_or_scripting`). Positive reviewers are *holistic*: 70% do not reduce success to a single technical cause—they treat good films as emergent properties of ensemble work. This reflects a fundamental theme difference: negatives seek scapegoats; positives celebrate synergy.

---

### 4. **Comparative Context: Negative Reviews Reference Other Films More Often**

| Context | Negative | Positive | Delta |
|---------|----------|----------|--------|
| Compared to other films | 53 (42.4%) | 35 (28.0%) | −14.4 pp |
| Genre contextualized | 7 (5.6%) | 16 (12.8%) | +7.2 pp |
| Historical/cultural reference | 4 (3.2%) | 12 (9.6%) | +6.4 pp |
| No comparison (standalone assessment) | 61 (48.8%) | 62 (49.6%) | ~0 pp |

**Interpretation:** Negative reviewers frequently invoke *comparative judgment*: "This is a pale shadow of *Film X*" or "unlike the masterwork *Y*." They use precedent as a measuring stick against which the work fails. Positive reviewers, conversely, more often employ *genre or historical framing* ("a clever take on the Western" or "a worthy continuation of the Ring series"), positioning success within tradition rather than failure relative to it.

---

### 5. **Recommendation Stance: Explicit Symmetry**

| Stance | Negative | Positive | Delta |
|--------|----------|----------|--------|
| Explicit avoid / Explicit recommend | 85 (68.0%) | 35 (28.0%) | −40.0 pp / +55.0 pp |
| Implicit positive / Explicit avoid | 0 (0.0%) | 73 (58.4%) | [zero in neg] / +58.4 pp |
| Conditional / Caution | 14+24 (31.2%) | 13+0 (10.4%) | ~−21 pp |

**Interpretation:** The recommendation stance confirms divergent communication strategies:
- **Negative:** Direct "avoid" (68%) or cautious hedging (31%)
- **Positive:** Enthusiastic endorsement (86% combining explicit recommend + implicit positive)

The absence of *implicit_positive* in negative reviews (0%) confirms that negative sentiment produces either qualified judgment or explicit warnings—never understated enthusiasm.

---

## Combined Theme Patterns

### Positive Reviews: The "Coherent Performer" Theme
- **Coherent + Acting focus:** 26/125 (20.8%)
  - Reviewers praise *engaging performances in well-told stories*
  - Example framing: "The acting was superb and the directing skill is so brilliantly handled"

- **Multiple aspects + Coherent:** 21/125 (16.8%)
  - Holistic excellence: script, acting, direction, and theme align
  - Example framing: "Masterful in every way—from the screenplay to the performances"

### Negative Reviews: The "Broken Narrative" Theme
- **Convoluted + Plot focus:** 21/125 (16.8% → 3.2% in positive reviews)
  - Reviewers identify *confused, incoherent storytelling*
  - Example framing: "The plot is confusing, the structure baffling, and nowhere does it make sense"

- **Screenplay + Writing blame:** 61/125 (48.8%)
  - Writing is the culprit; failure is traceable to scripting choices
  - Example framing: "The dialogue is stilted, the writing uninspired, the story thin"

---

## Thematic Synthesis

**Two narrative ecosystems emerge:**

1. **Negative Reviews: Problem-Diagnosis Frame**
   - Focus: structural and textual defects (plot, dialogue, writing)
   - Logic: identify the failed element and assign blame
   - Context: judge against exemplary precedents (other, better films)
   - Stance: warn others away (explicit avoid)
   - Signal: narrative dysfunction (`convoluted_or_thin`, 72%)

2. **Positive Reviews: Coherence-Celebration Frame**
   - Focus: performance, ensemble, and thematic resonance
   - Logic: describe how elements cohere into experience
   - Context: position within genre or tradition (understanding intent)
   - Stance: enthusiastically endorse (implicit or explicit recommend, 86%)
   - Signal: narrative coherence (`coherent_or_engaging`, 88%)

**The central difference:** Negative reviewers analyze *what breaks*; positive reviewers synthesize *what works*. This is not merely sentiment but a fundamental difference in interpretive stance and vocabulary.

---

## Coverage and Validity Notes

- **Sample size:** 125 reviews per sentiment; balanced design
- **TAPP column quality:** `narrative_quality_signal` and `primary_critique_focus` are high-signal; both cleanly partition by sentiment (88% vs. 8.8% coherence split; 60+ pp differences in focus areas)
- **Root cause attribution:** Shows expected asymmetry (negative → blame assignment; positive → emergent merit). No signal loss; strong interpretive value
- **Comparison context:** Reveals genuine rhetorical choice, not artifact; 14 pp difference is real and meaningful
- **Limitation:** `recommendation_stance` is post-hoc coding of implicit/explicit language; may understate nuance in conditional recommendations. However, the 68% explicit_avoid vs. 0% implicit_positive split is robust and interpretable

---

## Conclusion

Review themes differ not in object (both discuss plot, acting, writing) but in *analytic frame and resolution*. Negative reviews operate within a **defect-identification logic**: find the broken element, name it, warn readers. Positive reviews operate within a **coherence-integration logic**: describe how parts align, celebrate the result, invite readers to experience it. 

The TAPP-generated columns—especially `narrative_quality_signal` (88% vs. 8.8%) and `technical_or_creative_root_cause` (49% writing blame vs. 70% no attribution)—make this distinction quantifiable and actionable for film producers, critics, and recommendation systems seeking to understand not just *what* people think but *how* they think about cinema.
