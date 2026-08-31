---
dataset: amazon_polarity_reviews
scenario: predictive_sentiment
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review facets differ by sentiment label?"
source_table: augment_table/amazon_polarity_reviews/predictive_sentiment/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:02:50.648497+00:00
wall_seconds: 37.04
---

# Review Facets by Sentiment Label — `sonnet__skill_off` Variant

**Dataset:** Amazon Polarity Reviews · Predictive Sentiment · `skill_off_update`  
**Rows:** 250 (125 negative `label_pos=0`, 125 positive `label_pos=1`) · **Columns:** 13

---

## 1. Facet Means by Label

| Facet | Negative (0) | Positive (1) | Δ (Pos − Neg) | Significance |
|---|---|---|---|---|
| `review_word_count` | 68.9 | 65.3 | −3.5 | n.s. |
| `review_sentence_count` | 4.91 | 4.79 | −0.12 | n.s. |
| `exclamation_count` | 0.68 | 0.66 | −0.02 | n.s. |
| `question_count` | 0.15 | 0.04 | **−0.11** | * (p=0.04) |
| `caps_word_count` | 1.19 | 0.55 | **−0.64** | n.s. (p=0.16) |
| `positive_word_count` | 0.83 | **1.90** | +1.07 | *** (p<0.001) |
| `negative_word_count` | **0.98** | 0.19 | −0.79 | *** (p<0.001) |
| `avg_word_length` | 4.41 | **4.59** | +0.18 | ** (p=0.001) |
| `has_personal_pronoun` (rate) | 0.82 | 0.80 | −0.02 | n.s. |

---

## 2. Key Findings

### Strongly differentiating facets (statistically significant)

**Positive/negative word counts** are the clearest discriminators:
- Positive reviews average **1.90 positive words** vs. 0.83 in negative reviews (+129%).
- Negative reviews average **0.98 negative words** vs. 0.19 in positive reviews (+416%).
- Both differences are highly significant (p < 0.001), confirming that lexical sentiment signals are well-preserved even in the `skill_off` variant.

**Average word length** is modestly but reliably longer in positive reviews (4.59 vs. 4.41 chars/word, p=0.001), suggesting positive reviewers tend to use slightly more formal or descriptive vocabulary.

**Question count** is marginally higher in negative reviews (0.15 vs. 0.04, p=0.04). Negative reviewers more often pose rhetorical or complaint-driven questions (e.g., *"What is my daughter supposed to have?"*).

### Weakly differentiating or null facets

- **Review length** (word count, sentence count): nearly identical across labels — negative reviews are only ~3.5 words longer on average, not significant.
- **Exclamation count**: essentially equal (0.68 vs. 0.66), showing no sentiment-linked enthusiasm difference at this sample size.
- **CAPS word count**: negative reviews show a higher mean (1.19 vs. 0.55) hinting at more emotional emphasis, but the difference does not reach significance (p=0.16), likely due to high within-group variance.
- **Personal pronoun usage**: both groups use personal pronouns in ~80–82% of reviews — no sentiment signal.

---

## 3. Implications & Caveats

- The `skill_off` variant **retains strong lexical polarity signals** (positive/negative word counts), making those features reliable for classification even without skill augmentation.
- Structural features (length, punctuation exclamations) offer **little predictive lift** on their own.
- The question-count finding is statistically marginal (only one * level) and should be interpreted with caution — a larger sample could confirm or dismiss it.
- CAPS emphasis direction (negative > positive) aligns with intuition but lacks statistical power here; worth revisiting with more data.
