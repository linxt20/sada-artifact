---
dataset: imdb_movie_reviews
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What aspects of the films are reviewers focusing on?"
source_table: augment_table/imdb_movie_reviews/focus_inference/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:24:37.829896+00:00
wall_seconds: 140.73
---

# Analysis Report: Aspects of Films Reviewers Focus On

**Dataset:** IMDB Movie Reviews (250 reviews, balanced 125 negative / 125 positive)  
**Analysis Date:** 2026-07-30  
**Model:** substrate-claude-haiku-4-5  
**Query:** What aspects of the films are reviewers focusing on?

---

## Method Note

This analysis integrates TAPP-generated semantic facet columns with the original structured dataset. The six TAPP-generated columns analyzed are:
- `technical_craft_focus`
- `narrative_substance_focus`
- `performance_evaluation_focus`
- `emotional_response_focus`
- `genre_convention_focus`
- `thematic_message_focus`

These columns were generated via skill-v11 augment-e2e pipeline to decompose reviewer focus across craft, evaluative, and content dimensions. All findings combine facet counts with source label (review sentiment) breakdowns.

---

## Executive Summary

IMDB reviewers distribute their focus across six key dimensions in a clear hierarchy. **Emotional response dominates universally** (100% of reviews), followed by **narrative substance** (77.2%) and **performance evaluation** (54.4%). Reviewers are significantly less likely to foreground technical craft (28.8%) or thematic messaging (25.2%). Critically, **sentiment shapes focus priorities**: negative reviewers emphasize plot coherence and genre clichés as criticism, while positive reviewers engage more with character depth and thematic substance.

---

## Main Findings

### 1. Focus Hierarchy: Six-Tier Ranking

Reviews prioritize aspects in a consistent order:

| Rank | Focus Dimension | Coverage | Count |
|------|-----------------|----------|-------|
| 1    | **Emotional Response** | 100.0% | 250/250 |
| 2    | **Narrative Substance** | 77.2% | 193/250 |
| 3    | **Performance Evaluation** | 54.4% | 136/250 |
| 4    | **Genre Convention** | 50.8% | 127/250 |
| 5    | **Technical Craft** | 28.8% | 72/250 |
| 6    | **Thematic Message** | 25.2% | 63/250 |

**Interpretation:** Emotional response (viewer satisfaction, entertainment value, emotional engagement, humor) is *baked into every review*. Story and characters come next, followed by acting quality and genre expectations. Visual and thematic depth are tertiary concerns.

---

### 2. Emotional Response: Universal and Concrete

All 250 reviews (100%) contain explicit reference to emotional or entertainment response.

**Breakdown (emotional_response_focus):**
- **Viewer satisfaction** (59.6%, n=149): Direct judgments of overall satisfaction ("great film," "waste of time")
- **Entertainment value** (19.6%, n=49): Fun factor, engagement, spectacle appeal
- **Emotional engagement** (14.0%, n=35): Character connection, mood impact, visceral reaction
- **Humor success** (6.8%, n=17): Comedic effectiveness, timing, joke landing

**Key insight:** Reviewers rarely discuss *only* plot or acting; they nearly always frame judgments through personal emotional or entertainment outcome. This dimension serves as the anchoring frame for all other evaluations.

---

### 3. Narrative Substance: Story and Character Focus

77.2% of reviews explicitly engage with narrative substance (`narrative_substance_focus`). This is the most decisive secondary dimension.

**What reviewers evaluate within narrative:**
- **Plot coherence** (26.8%, n=67): Logic, consistency, believability of story events
- **Character development** (24.0%, n=60): Depth, arc, believability of character motivation
- **Plot originality** (10.4%, n=26): Freshness of premise, departure from genre formula
- **Narrative pacing** (7.2%, n=18): Story rhythm, scene duration, plot progression tempo
- **Dialogue quality** (6.8%, n=17): Script writing, authenticity, wit or naturalness of speech
- **Predictability** (2.0%, n=5): Surprise factor, formulaic vs. unexpected beats

**Critical sentiment split (Label 0=Negative, 1=Positive):**
- Negative reviews (83.2% engage with narrative) emphasize **plot_coherence** (37.6%, n=47 of 125)
- Positive reviews (71.2% engage with narrative) emphasize **character_development** (32.0%, n=40 of 125)

**Interpretation:** Negative reviewers fault films on structural logic ("the plot makes no sense"); positive reviewers praise character richness. The 12-point gap in narrative engagement (83.2% vs. 71.2%) suggests negative reviewers are more motivated to dissect story failures.

---

### 4. Performance Evaluation: Acting as Central Criterion

54.4% of reviews (136/250) focus on acting and casting.

**Within performance_evaluation_focus:**
- **Acting quality** (49.6%, n=124): By far the dominant form—raw assessment of actor skill, presence, or delivery
- **Casting fit** (2.0%, n=5): Suitability of actor choice for role
- **Emotional delivery** (1.6%, n=4): Nuance, authenticity, or impact of performance
- **Chemistry between actors** (1.2%, n=3): Onscreen rapport, pairing effectiveness

**Sentiment pattern:**
- Negative: 50.4% (n=63/125) discuss acting
- Positive: 58.4% (n=73/125) discuss acting

Acting quality is nearly equally central to both positive and negative verdicts—it serves as a universal criterion. Negative reviews may cite "wooden" acting as a flaw; positive reviews highlight "terrific" or "nuanced" performances. The 8-point higher rate in positive reviews suggests positive reviewers are somewhat more likely to credit good acting as a reason for enjoyment.

---

### 5. Genre Convention: Clichés as Criticism, Originality as Praise

50.8% of reviews (127/250) reference genre and convention expectations.

**Within genre_convention_focus:**
- **Cliché or derivative** (32.4%, n=81): Adherence to tired tropes, formulaic plotting, unoriginal premise
- **Originality/novelty** (10.4%, n=26): Fresh approach, subversion of genre expectations, novel twist
- **Genre trope adherence** (7.2%, n=18): Conformity to or expected execution of genre rules
- **Genre expectation subversion** (0.8%, n=2): Deliberate defiance of genre norms

**Sentiment divergence is stark:**
- Negative reviews: 58.4% (n=73/125) engage with genre → **56.8% (n=71) cite clichés**
- Positive reviews: 43.2% (n=54/125) engage with genre → **originality is more common**

**Interpretation:** Genre convention serves as a *critical lens* more in negative than positive evaluations. Negative reviewers use "it's just another [type]" as a condemnation. Positive reviewers, when they mention genre, are more likely to praise novelty or clever trope-play rather than complaint. This 13-point gap in negative engagement with genre (58.4% vs. 43.2%) indicates negative reviewers use genre predictability as a fault.

---

### 6. Technical Craft: Cinematography Dominates, Rest Sparse

28.8% of reviews (72/250) foreground technical production aspects.

**Within technical_craft_focus:**
- **Cinematography** (12.4%, n=31): Visual framing, composition, camera work, lighting
- **Special effects** (5.6%, n=14): VFX quality, practical effects, CGI execution
- **Direction** (4.4%, n=11): Directorial vision, scene staging, pacing choices
- **Pacing** (3.2%, n=8): Technical rhythm, editing tempo (distinct from narrative pacing)
- **Editing** (1.6%, n=4): Cut timing, montage, sequence assembly
- **Production design** (0.8%, n=2): Set design, costume, production value
- **Sound design** (0.8%, n=2): Audio mix, music, sound effects

**Sentiment neutrality:**
- Negative: 30.4% (n=38/125) mention technical craft
- Positive: 27.2% (n=34/125) mention technical craft

Technical craft is mentioned infrequently and with similar rates across sentiment. When present, cinematography is the dominant technical concern. Most reviews do not engage deeply with production techniques unless they are notably exceptional or disastrous.

---

### 7. Thematic Message: Positive Reviews More Engaged

25.2% of reviews (63/250) engage with thematic or ideological content.

**Within thematic_message_focus:**
- **Moral or philosophical theme** (12.0%, n=30): Ethical questions, philosophical inquiry, life lessons
- **Social commentary** (10.4%, n=26): Critique of social norms, political messaging, commentary on systems
- **Cultural representation** (2.0%, n=5): Portrayal of specific groups, cultural accuracy
- **Message clarity** (0.8%, n=2): How clearly thematic content is conveyed

**Dramatic sentiment split:**
- Negative reviews: 15.2% (n=19/125) mention themes
- Positive reviews: 35.2% (n=44/125) mention themes
- **Difference: 20 percentage points**

Among those that do mention themes:
- Negative reviews that mention themes (n=19): focus on **social_commentary** (42.1%, n=8)
- Positive reviews that mention themes (n=44): focus on **moral_or_philosophical_theme** (54.5%, n=24)

**Interpretation:** Thematic engagement is **twice as common in positive reviews**. Positive reviewers are drawn to and celebrate moral or philosophical depth; negative reviewers, when they mention themes, often critique heavy-handed or misguided social commentary. This suggests **thematic substance is a driver of appreciation but not typically a driver of criticism**.

---

## Focus Patterns by Sentiment

### Negative Reviews (n=125): Critical Disassembly

Negative reviewers adopt a **critical inventory** approach:

1. **Emotional response** (100%): Always frame complaints as unsatisfying or unengaging
2. **Narrative substance** (83.2%): Aggressively unpack plot/dialogue failures; emphasize plot_coherence breakdown
3. **Genre convention** (58.4%): Weaponize clichés and predictability as proof of laziness
4. **Technical craft** (30.4%): Occasionally blame poor cinematography or effects
5. **Performance** (50.4%): Note bad acting as evidence of incompetence
6. **Thematic message** (15.2%): Rarely engage; when present, critique messaging as problematic

### Positive Reviews (n=125): Celebratory Depth

Positive reviewers adopt a **holistic appreciation** model:

1. **Emotional response** (100%): Frame satisfaction, entertainment, or emotional connection
2. **Narrative substance** (71.2%): Less urgent than in negative reviews; when present, emphasize character_development
3. **Performance** (58.4%): Slightly more likely to credit good acting as a strength
4. **Genre convention** (43.2%): Less concerned with formula; more likely to note originality when mentioned
5. **Technical craft** (27.2%): Rarely foregrounded; similar rate to negative
6. **Thematic message** (35.2%): Twice as likely as negative reviews; engage with moral/philosophical depth

---

## Integration with Original Columns

The augmented columns clarify and decompose the sentiment (label_pos) signal:

- **label_pos = 0 (Negative)**: Driven by failures in plot coherence, narrative logic, dialogue quality, and genre conformity (clichés)
- **label_pos = 1 (Positive)**: Driven by character depth, acting quality, emotional engagement, and thematic substance

The TAPP facets do not replace label_pos; they *operationalize* the semantic dimensions underlying it.

---

## Coverage and Reliability Notes

### High-Coverage Facets (Reliable):
- **Emotional response**: 100% coverage—every review expresses satisfaction/dissatisfaction
- **Narrative substance**: 77.2% coverage—strong signal, core to both positive and negative judgments
- **Performance evaluation**: 54.4% coverage—solid, consistent across sentiment

### Medium-Coverage Facets (Moderately Reliable):
- **Genre convention**: 50.8% coverage—useful for sentiment distinction but not universal
- **Technical craft**: 28.8% coverage—sparse, cinematography-heavy when present

### Lower-Coverage Facets (Selective):
- **Thematic message**: 25.2% overall, but driven by positive reviews (35.2% vs. 15.2%)—most reliable as an indicator of positive appreciation, less common in negative evaluations

---

## Conclusion

Movie reviewers focus on six interconnected dimensions, in a clear priority order. **Emotional satisfaction is omnipresent and frames all evaluation.** Story and acting are the primary craft levers—negative reviewers critique story failures; positive reviewers celebrate character depth. **Genre predictability serves as a criticism axis primarily in negative reviews.** Technical production rarely drives verdicts. **Thematic substance distinguishes positive from negative reviews more sharply than any other facet**: positive reviewers are twice as likely to engage, and when they do, they celebrate moral/philosophical depth rather than criticize messaging missteps.

The augmented TAPP-generated columns (`emotional_response_focus`, `narrative_substance_focus`, `performance_evaluation_focus`, `genre_convention_focus`, `technical_craft_focus`, `thematic_message_focus`) effectively decompose the underlying semantic structure of reviewer focus and validate the query's framing: reviewers reliably foreground distinct aspects of films, and the patterns differ meaningfully by sentiment.
