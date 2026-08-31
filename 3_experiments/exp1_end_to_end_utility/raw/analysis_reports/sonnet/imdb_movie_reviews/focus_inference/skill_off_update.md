---
dataset: imdb_movie_reviews
scenario: focus_inference
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: focus_inference
focus_variable: "proposed_focus_variable"
query: "What aspects of the films are reviewers focusing on?"
source_table: augment_table/imdb_movie_reviews/focus_inference/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:24:30.049004+00:00
wall_seconds: 36.94
---

# Film Review Focus Analysis — IMDB Movie Reviews (`skill_off` variant)

## Dataset Overview

- **250 reviews**, evenly split between positive (`label_pos=1`, n=125) and negative (`label_pos=0`, n=125).
- Each review is tagged with nine binary focus flags (`focus_*`) and a `primary_focus` label.
- On average, each review addresses **2.3 distinct aspects**; 27 reviews (10.8%) were tagged with no specific focus (coded as `general` in `primary_focus`).

---

## Aspect Prevalence (All Reviews)

| Aspect | Reviews Mentioning (n) | Rate |
|---|---|---|
| **Acting** | 133 | 53.2% |
| **Plot / Story** | 111 | 44.4% |
| **Directing** | 77 | 30.8% |
| **Entertainment / Humor** | 72 | 28.8% |
| **Visuals / Cinematography** | 58 | 23.2% |
| **Atmosphere / Tone** | 43 | 17.2% |
| **Dialogue** | 37 | 14.8% |
| **Music / Sound** | 31 | 12.4% |
| **Effects / Technical** | 12 | 4.8% |

**Acting** is the dominant focus, both as the most-mentioned aspect (53%) and as the single most common `primary_focus` (133/250 reviews). **Plot/story** is a strong second. Together these two account for the majority of critical attention.

---

## Primary Focus Distribution

| Primary Focus | Count | Share |
|---|---|---|
| acting | 133 | 53.2% |
| plot_story | 49 | 19.6% |
| general | 27 | 10.8% |
| directing | 12 | 4.8% |
| entertainment_humor | 7 | 2.8% |
| visuals_cinematography | 7 | 2.8% |
| atmosphere_tone | 7 | 2.8% |
| music_sound | 5 | 2.0% |
| dialogue | 2 | 0.8% |
| effects_technical | 1 | 0.4% |

The concentration in `acting` (53%) is striking; almost no reviews center primarily on technical/effects work.

---

## Sentiment Differences

| Aspect | Positive Rate | Negative Rate | Δ |
|---|---|---|---|
| Entertainment / Humor | 32.0% | 25.6% | **+6.4%** (more in positive) |
| Atmosphere / Tone | 19.2% | 15.2% | +4.0% |
| Dialogue | 10.4% | 19.2% | **−8.8%** (more in negative) |
| Plot / Story | 40.8% | 48.0% | −7.2% |
| Directing | 27.2% | 34.4% | −7.2% |
| Acting | 50.4% | 56.0% | −5.6% |
| Visuals / Cinematography | 20.8% | 25.6% | −4.8% |

Negative reviews are moderately more likely to discuss **dialogue**, **directing**, and **plot/story** — aspects often cited as failures. Positive reviews lean slightly more toward **entertainment/humor** and **atmosphere/tone**. Differences are modest (all ≤ 9 pp), so aspect focus is not a strong predictor of sentiment on its own.

---

## Key Takeaways

1. **Acting dominates**: Over half of all reviews foreground performer quality, making it the single most salient lens through which IMDB reviewers evaluate films.
2. **Plot/story is a reliable second concern**: 44% of reviews engage with narrative, reflecting audiences' story-driven expectations.
3. **Technical aspects are rarely the primary focus**: Effects (4.8%) and music/sound (12.4%) appear mainly as secondary mentions.
4. **Reviews are multi-aspect**: 73% of reviews flag two or more focus areas, suggesting holistic evaluations rather than single-axis criticism.
5. **Weak sentiment signal from focus alone**: While negative reviews slightly over-index on dialogue and directing, the differences are small and should not be over-interpreted without further modelling.
