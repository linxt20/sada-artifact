---
dataset: amazon_polarity_reviews
scenario: predictive_sentiment
variant: original
model: substrate-claude-haiku-4-5
query_subtype: exploratory_data_analysis
focus_variable: "label_pos"
query: "How do review facets differ by sentiment label?"
source_table: augment_table/amazon_polarity_reviews/predictive_sentiment/original.csv
source_report: dataset_portion_2/substrate-claude-haiku-4-5/amazon_polarity_reviews__predictive_sentiment/analyses/original/analysis.md
wall_seconds: 42.28
---

# Review Facets by Sentiment Label: Amazon Polarity Reviews

## Dataset Overview
The Amazon Polarity Reviews dataset contains **250 customer product reviews** with binary sentiment labels:
- **Positive reviews (label=1): ~50% of dataset**
- **Negative reviews (label=0): ~50% of dataset**

Review structure includes: `review_id`, `label_pos` (sentiment), `title`, and `content` fields.

## Key Findings on Review Facets by Sentiment

### 1. **Title Language and Tone**
**Negative Reviews:**
- Titles employ emphatic negation: "Skip it," "Not happy," "SUCKS," "Worst Movie," "DO NOT waste your money"
- Use imperative directives: "Avoid," "Pass on," "Closer to junk"
- Feature exclamation marks and capitalization for emphasis
- Often position problems upfront: "didn't last long," "Disappointingly"

**Positive Reviews:**
- Titles emphasize satisfaction and recommendation: "Keeps skin clear," "Very Healing," "Excellent," "Great Book," "Works Great"
- Highlight superlatives: "Best movie," "Tremendous quality," "The Final Detail"
- Use positive adjectives and warmth: "warm and cozy," "pleasantly surprised," "Great value"
- Example pattern: Description of product/item followed by positive attribute

### 2. **Content Length and Verbosity**
**Negative Reviews:**
- Tend to be longer and more detailed (visible in samples: ~150-200+ words average)
- Include specific complaint enumeration: "First being...", "And...", "The worst part is..."
- Provide narrative structure of disappointment: problem identification → evidence → conclusion

**Positive Reviews:**
- Range from concise praise (20-50 words) to detailed positive experiences
- Shorter positive reviews: "Good value," "Works Great," "warm and cozy" (~10-30 words)
- Longer positive reviews focus on features appreciated and recommendations

### 3. **Evidence and Justification**
**Negative Reviews:**
- Provide specific failure instances: durability issues, functional failures, defective components
- Cite comparisons to alternatives or prior versions
- Include timeline references: "lasted maybe 4 months," "Within two months it fell apart"
- Detail problematic interactions and consequences

**Positive Reviews:**
- Highlight key benefits and satisfaction outcomes
- Provide context of use: "I've been using this product for many years"
- Offer evidence of quality: "soft and smooth," "well made and comfortable"
- Emphasize personal enthusiasm and repeated use intention

### 4. **Emotional Expression Patterns**
**Negative Reviews:**
- Explicit disappointment markers: "extremely displeased," "I HATE this product," "was a complete waste"
- Emotion intensity: "SUCKS," "Terrible," "Horrible," "Absolutely Useless!"
- Frustration signals: "I would rather sit at the dentist's office," exasperation metaphors

**Positive Reviews:**
- Enthusiasm markers: "LOVE," "delighted," "pleasantly surprised," multiple exclamation marks
- Gratitude and warmth: "thankful," "heartwarming," "wonderful"
- Personal satisfaction: "I can't get enough," "love," "enjoyable"

### 5. **Comparative and Conditional Language**
**Negative Reviews:**
- Comparisons emphasizing product inferiority: "would never buy," "not as good as," "less expensive model works better"
- Conditional warnings: "If you need X, avoid this," "Don't make this one your first"
- Causal explanations of why product failed expectations

**Positive Reviews:**
- Positive comparisons: "nearly as good as," "excellent addition to"
- Qualification of praise: "for the price," "good value," acknowledging minor tradeoffs
- Recommendation conditions: "if you like," "best for," targeting appropriate audiences

### 6. **Specificity of Product Categories**
Both positive and negative reviews span diverse product categories:
- **Media (books, movies, music):** Critical analysis of narrative, performance, artistic merit
- **Physical products (tools, appliances, clothing):** Focus on durability, functionality, design
- **Bath/beauty products:** Efficacy and sensory experience descriptions

Negative reviews across categories emphasize product failure or waste; positive reviews emphasize satisfaction and value.

## Patterns Summary

| Dimension | Negative Reviews | Positive Reviews |
|-----------|-----------------|-----------------|
| **Title tone** | Emphatic negation, warnings | Affirmation, superlatives |
| **Typical length** | Longer, structured complaints | Variable: brief praise to detailed endorsement |
| **Justification** | Specific failures, timeline | Satisfaction outcomes, personal experience |
| **Emotional tone** | Strong disappointment, frustration | Enthusiasm, warmth, gratitude |
| **Language markers** | "waste," "doesn't," "poor," "broken" | "excellent," "love," "satisfied," "recommend" |

## Important Caveats
- This analysis is based on visible patterns in the first ~100 reviewed examples; corpus-wide linguistic metrics (average word count, sentiment word frequency) would require computational text analysis
- Both positive and negative reviews contain genuine engagement with product/content details—this is not a simplistic polarity where negative = dismissive or positive = shallow
- Review length variation exists within both sentiment categories; negative reviews are *generally* longer but substantial positive reviews also occur

## Conclusion
Review facets differ substantially by sentiment label. Negative reviews employ emphatic, warning-oriented language with detailed failure narratives, while positive reviews emphasize satisfaction, warmth, and recommendation. Both demonstrate product engagement, but through opposing evaluative frameworks.
