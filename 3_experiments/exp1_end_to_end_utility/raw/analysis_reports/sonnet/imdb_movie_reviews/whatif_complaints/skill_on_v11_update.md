---
dataset: imdb_movie_reviews
scenario: whatif_complaints
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: what_if
focus_variable: "label_pos"
query: "If films addressed the most common audience complaints, how much would positive sentiment increase?"
source_table: augment_table/imdb_movie_reviews/whatif_complaints/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:23:36.921754+00:00
wall_seconds: 61.28
---

# What-If Analysis: Impact of Addressing Audience Complaints on Positive Sentiment

**Dataset:** 250 IMDB movie reviews (125 positive / 125 negative, perfectly balanced)  
**Focus Variables:** `writing_script_complaint`, `complaint_severity`, `genre_expectation_mismatch`

---

## Baseline

| Metric | Value |
|--------|-------|
| Overall positive rate | 50.0% |
| Reviews with **no** complaints of any kind | 68.4% positive (n=98) |
| Reviews with **any** complaint | 38.2% positive (n=152) |

The 30-point gap between complaint-free and complaint-bearing reviews establishes a clear ceiling of achievable improvement.

---

## Most Common Audience Complaints

### 1. Writing & Script Complaints (n=69 reviews with complaints present)

| Complaint Type | Count | Positive Rate |
|---------------|-------|---------------|
| `not_present` | 181 | **67.9%** |
| `weak_screenplay` | 44 | 2.3% |
| `cliched_writing` | 10 | 10.0% |
| `bad_dialogue` | 9 | 0.0% |
| `incoherent_narrative` | 6 | 0.0% |

Writing/script complaints are the most prevalent complaint category and are **devastatingly correlated with negative sentiment** — nearly all reviews mentioning them are negative.

### 2. Genre Expectation Mismatch (n=125 with mismatch present)

| Genre | Count | Positive Rate |
|-------|-------|---------------|
| `not_present` | 125 | 54.4% |
| `horror` | 29 | 34.5% |
| `comedy` | 25 | 52.0% |
| `drama` | 23 | 52.2% |
| `sci_fi` | 11 | 36.4% |
| `musical` | 8 | 37.5% |

Genre mismatch has a **moderate** effect. Horror and sci-fi mismatches are most damaging (~15–20 point drop), while comedy and drama mismatches have minimal impact.

### 3. Complaint Severity

| Severity | Count | Positive Rate |
|----------|-------|---------------|
| 1 (mild) | 26 | 84.6% |
| 2 | 31 | 35.5% |
| 3 | 47 | 4.3% |
| 4 | 36 | **0.0%** |
| 5 (severe) | 17 | **0.0%** |

Severity is the strongest predictor: at severity ≥ 4, **no** reviews are positive. Severity ≥ 3 already yields near-zero positivity.

---

## Estimated Sentiment Uplift

| Scenario | Hypothetical Positive Rate | Increase |
|----------|--------------------------|---------|
| Baseline | 50.0% | — |
| Resolve **all** complaint-bearing negative reviews | 87.6% | **+37.6 pp** |
| Resolve only **severe (≥4) complaint** negatives | 71.2% | **+21.2 pp** |
| Achieve complaint-free baseline rate | ~68.4% | **+18.4 pp** |

- **94 negative reviews** carry at least one identifiable complaint (writing/script or genre mismatch).
- Resolving all would theoretically raise positive sentiment from 50% to ~88% — the upper-bound estimate.
- A realistic **targeted intervention** (addressing severity ≥ 4 writing/script issues, which affect 53 negative reviews) could yield a ~21 percentage-point increase.

---

## Key Findings

1. **Writing quality is the dominant complaint driver.** `weak_screenplay` alone accounts for 44 cases with a 2.3% positive rate — the single highest-leverage fix.
2. **Severity matters more than complaint type.** Even minor genre mismatches (severity 1–2) leave most reviews positive; the same complaint at severity 3+ collapses positivity to near zero.
3. **Genre-specific vulnerability:** Horror and sci-fi are disproportionately harmed by expectation mismatches; comedy and drama are largely resilient.
4. **Important caveats:** These are correlational patterns. Films with multiple simultaneous problems (67 reviews carry both writing and genre complaints) may not see additive benefits from fixing individual issues. The 50/50 dataset split is balanced by design and may not reflect natural base rates.

---

## Decision Recommendation

Prioritizing **script and dialogue quality** (especially eliminating weak screenplays and bad dialogue) offers the highest expected return on positive sentiment — potentially **+18 to +38 percentage points** depending on how broadly complaints can be resolved. Severity reduction from 4–5 down to 1–2 is the most realistic near-term target, with an estimated **+21 pp** improvement.
