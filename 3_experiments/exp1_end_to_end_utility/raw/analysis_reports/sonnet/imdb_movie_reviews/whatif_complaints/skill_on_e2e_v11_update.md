---
dataset: imdb_movie_reviews
scenario: whatif_complaints
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: what_if
focus_variable: "label_pos"
query: "If films addressed the most common audience complaints, how much would positive sentiment increase?"
source_table: augment_table/imdb_movie_reviews/whatif_complaints/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:23:58.667031+00:00
wall_seconds: 76.39
---

# What-If Analysis: Positive Sentiment Increase if Films Addressed Common Audience Complaints

**Dataset:** 250 IMDB movie reviews (125 positive / 125 negative, balanced)  
**Query:** If films addressed the most common audience complaints, how much would positive sentiment increase?

---

## Method Note

TAPP-generated columns used: `writing_script_complaint`, `complaint_severity`, `genre_expectation_mismatch`. These are cross-validated against the original outcome column `label_pos` (binary: 1 = positive review, 0 = negative). No other TAPP columns exist in the augmented table.

---

## 1. Baseline Sentiment

| Metric | Value |
|---|---|
| Total reviews | 250 |
| Positive reviews | 125 (50.0%) |
| Negative reviews | 125 (50.0%) |

---

## 2. Complaint Landscape

### 2a. Writing/Script Complaints (`writing_script_complaint`)

| Complaint Type | N | Positive Rate |
|---|---|---|
| `not_present` | 194 | **63.4%** |
| `excessive_cliche` | 12 | 8.3% |
| `weak_screenplay` | 27 | 3.7% |
| `poor_narrative_coherence` | 11 | 0.0% |
| `bad_dialogue` | 6 | 0.0% |

56 reviews (22.4%) flag a writing/script complaint. Their collective positive rate is just **3.6%** (2/56), versus 63.4% for complaint-free reviews — a 60-point gap. This is the dominant complaint driver.

### 2b. Complaint Severity (`complaint_severity`)

| Severity | N | Positive Rate |
|---|---|---|
| 1 (minor) | 108 | 96.3% |
| 2 | 42 | 45.2% |
| 3 | 54 | 3.7% |
| 4 | 31 | 0.0% |
| 5 (severe) | 15 | 0.0% |

Severity is a near-perfect predictor of sentiment: all 46 reviews rated severity ≥ 4 are negative (0% positive). Severity 1 reviews are almost entirely positive (96.3%). This confirms `complaint_severity` adds strong independent signal.

### 2c. Genre Expectation Mismatch (`genre_expectation_mismatch`)

| Category | N | Positive Rate |
|---|---|---|
| `not_present` | 146 | 52.1% |
| `drama` | 32 | 50.0% |
| `action` | 10 | 50.0% |
| `comedy` | 18 | 44.4% |
| `horror` | 22 | 45.5% |
| `sci_fi` | 13 | 46.2% |
| `musical` | 6 | 33.3% |

104 reviews (41.6%) show a genre expectation mismatch. Their positive rate (47.1%) is only slightly below the no-mismatch rate (52.1%). This facet is **weak** — the gap is small (~5 pp) and overlaps with balanced sampling, making genre mismatch a minor contributor.

---

## 3. What-If Counterfactual Estimates

The counterfactual asks: if films resolved each complaint type, and affected reviews then matched the positive rate of complaint-free reviews, how much would overall sentiment improve?

| Scenario | Affected Reviews | Current Positives | Counterfactual Positives | Overall Pos. Rate (Before → After) | Absolute Lift |
|---|---|---|---|---|---|
| Fix writing/script complaints | 56 | 2 | 35.5 | 50.0% → **63.4%** | **+13.4 pp** |
| Fix genre expectation mismatch | 104 | 49 | 54.1 | 50.0% → 52.1% | +2.1 pp |
| Fix both (combined, no double-count) | 130 | 50 | 81.2 | 50.0% → **62.5%** | **+12.5 pp** |

> **Assumption:** Complaint-affected reviews, if addressed, would reach the positive rate of complaint-free reviews (benchmark: 63.4% for no writing complaint; 52.1% for no genre mismatch; 62.5% for neither).

---

## 4. Priority Findings

1. **Writing/script quality is the highest-leverage complaint.** Fixing `weak_screenplay`, `poor_narrative_coherence`, `bad_dialogue`, and `excessive_cliche` across the 56 affected reviews would yield a projected **+13.4 percentage-point increase** in positive sentiment (50% → 63.4%).

2. **Complaint severity amplifies impact.** All 46 reviews with `complaint_severity` ≥ 4 are negative. Resolving the most severe complaints alone would theoretically rescue ~23 additional positive reviews (+9.2 pp), making severity the key triage variable.

3. **Genre mismatch is a weak driver.** Despite affecting 104 reviews (41.6%), the positive-rate gap is only ~5 pp. Genre mismatch likely reflects audience self-selection rather than a fixable film deficiency; it contributes only **+2.1 pp** in the counterfactual.

4. **Combined uplift ceiling:** Addressing all detectable complaints in this dataset projects a maximum gain of approximately **+12–13 percentage points** in positive sentiment (from 50% to ~63%), driven almost entirely by the writing/script dimension.

---

## 5. Summary

> **If films addressed the most common audience complaints — primarily weak screenwriting, poor narrative coherence, and bad dialogue — positive sentiment in this dataset would increase by an estimated ~13 percentage points (from 50% to ~63%).** Genre expectation mismatches are widespread but contribute minimally (~2 pp). The `complaint_severity` column confirms that only high-severity complaints (levels 3–5, covering 100 reviews) are reliably associated with negative outcomes; minor complaints (severity 1) coexist with overwhelmingly positive reviews and need not be targeted.
