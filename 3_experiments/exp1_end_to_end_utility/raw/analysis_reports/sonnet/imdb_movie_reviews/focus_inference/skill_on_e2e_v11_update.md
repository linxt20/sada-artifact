---
dataset: imdb_movie_reviews
scenario: focus_inference
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What aspects of the films are reviewers focusing on?"
source_table: augment_table/imdb_movie_reviews/focus_inference/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:23:29.084054+00:00
wall_seconds: 66.44
---

# IMDB Movie Reviews: What Aspects Are Reviewers Focusing On?

**Query:** What aspects of the films are reviewers focusing on?  
**Dataset:** 250 IMDB reviews (125 positive / 125 negative, balanced)

---

## Method Note

Analysis combines the original structured columns (`review_id`, `label_pos`, `review_text`) with seven TAPP-generated semantic facet columns: `acting_performance_assessment`, `script_writing_assessment`, `direction_filmmaking_assessment`, `plot_narrative_structure_focus`, `genre_tone_execution`, `entertainment_engagement_verdict`, and `comparison_or_adaptation_reference`. Coverage and sentiment-alignment were computed for each facet; cross-tabulations against `label_pos` validate discriminative power.

---

## Key Findings

### 1. Reviewers Cover Multiple Facets per Review

The median review touches **5 out of 7 measured facets** (mean = 5.16, min = 2, max = 7), confirming that IMDB reviewers write holistic evaluations rather than single-topic assessments.

| # Facets Mentioned | Reviews (n=250) |
|---|---|
| 2 | 6 |
| 3 | 21 |
| 4 | 53 |
| 5 | 58 |
| 6 | 71 |
| 7 | 41 |

---

### 2. Facet Coverage: What Reviewers Focus On Most

| Facet (TAPP column) | Mentioned in N reviews | Coverage |
|---|---|---|
| `entertainment_engagement_verdict` | 250 / 250 | **100%** |
| `comparison_or_adaptation_reference` | 250 / 250 | **100%** |
| `genre_tone_execution` | 239 / 250 | **95.6%** |
| `direction_filmmaking_assessment` | 205 / 250 | **82.0%** |
| `plot_narrative_structure_focus` | 135 / 250 | **54.0%** |
| `script_writing_assessment` | 110 / 250 | **44.0%** |
| `acting_performance_assessment` | 101 / 250 | **40.4%** |

**Overall entertainment/engagement** and **genre/tone execution** are near-universal focuses. Direction and filmmaking craft are discussed in 4 of 5 reviews. Plot, script, and acting are mentioned in roughly half or fewer reviews, suggesting they are discussed selectively rather than universally.

---

### 3. Direction & Filmmaking: Most Discriminative Craft Facet

`direction_filmmaking_assessment` appears in 82% of reviews and is strongly polarized by sentiment:

| Assessment | Neg reviews | Pos reviews |
|---|---|---|
| strong_negative (n=69) | 100% | 0% |
| moderately_negative (n=23) | 95.7% | 4.3% |
| mixed (n=38) | 60.5% | 39.5% |
| moderately_positive (n=29) | 0% | 100% |
| strong_positive (n=46) | 4.3% | 95.7% |

Direction-related criticism (negative or mixed, n=130) is heavily concentrated in negative reviews, making it the craft element most tied to overall verdict.

---

### 4. Genre/Tone Execution: Near-Universal Focus, Highly Predictive

`genre_tone_execution` is present in 95.6% of reviews and splits almost perfectly on sentiment:

| Genre Execution | N | Neg rate | Pos rate |
|---|---|---|---|
| well_executed | 104 | 4.8% | **95.2%** |
| mismatched_to_genre_expectations | 104 | **95.2%** | 4.8% |
| tonally_inconsistent | 22 | 81.8% | 18.2% |
| genre_subverted_intentionally | 9 | 11.1% | 88.9% |

Reviewers are intensely attuned to whether a film delivers on its genre promise. "Mismatched expectations" (n=104) is as common as "well executed" (n=104), reflecting that genre disappointment is a dominant driver of negative reviews.

---

### 5. Entertainment/Engagement: Universal Verdict Layer

`entertainment_engagement_verdict` is present in **every review** (100%) and perfectly aligns with `label_pos`:

| Verdict | N | Neg rate | Pos rate |
|---|---|---|---|
| highly_engaging | 82 | 0% | **100%** |
| watchable_or_acceptable | 65 | 38.5% | 61.5% |
| boring_or_slow | 52 | **94.2%** | 5.8% |
| unwatchable | 51 | **100%** | 0% |

This confirms reviewers always render an engagement verdict—this is the capstone of every review—while intermediate ratings ("watchable") show moderate positive tilt.

---

### 6. Script/Writing: Selectively Discussed, Strongly Negative When Present

`script_writing_assessment` appears in 44% of reviews but negative-review writing is flagged far more often (78 negative vs. 32 positive reviews). When script problems are cited, they are severe: `strong_negative` (n=40, 100% neg), `moderately_negative` (n=35, 94.3% neg). Positive writing is rarely praised explicitly (strong_positive n=24, always in positive reviews; moderately_positive n=1).

---

### 7. Acting: Balanced Mention, Clearly Polarized

`acting_performance_assessment` appears in 40.4% of reviews (51 negative, 50 positive), suggesting actors receive similar attention across sentiment. The ratings are deterministic: `strong_positive` (n=37) → 97.3% positive reviews; `strong_negative` (n=24) + `moderately_negative` (n=20) → 100% negative reviews.

---

### 8. Comparisons & References

`comparison_or_adaptation_reference` is always coded (100%) but 61.6% (n=154) have "no comparison made." When comparisons appear: 61 reviews compare to other films (62.3% negative), 26 reference director/actor body of work (50/50), and 9 reference source material (55.6% negative). Comparison-rich negative reviews tend to use analogies to underscore failure.

---

## Summary: Review Focus Hierarchy

1. **Entertainment & engagement** — universal focus (100%); the bottom-line verdict every reviewer delivers.
2. **Genre/tone execution** — near-universal (95.6%); whether the film satisfies genre expectations is the dominant craft criterion.
3. **Direction & filmmaking** — broad focus (82%); most-discussed specific craft element.
4. **Plot/narrative structure** — moderate focus (54%); discussed when story logic or originality is a concern.
5. **Script/writing** — selective focus (44%); raised primarily to explain negative reactions.
6. **Acting performance** — selective focus (40%); evenly distributed, but decisive when mentioned.
7. **Comparisons to other works** — contextual (38.4% of reviews make explicit comparisons), typically used to contextualize failure.
