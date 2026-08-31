---
dataset: education_survey_responses
scenario: predictive_low
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "satisfaction_1to5"
query: "What open-response signals predict low learning satisfaction?"
source_table: augment_table/education_survey_responses/predictive_low/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:09:00.550117+00:00
wall_seconds: 54.07
---

# Open-Response Signals Predicting Low Learning Satisfaction

## Dataset Overview

- **Total responses:** 250 (Students: 89, Teachers: 81, Parents: 80)
- **Low satisfaction flagged** (`open_predicts_low_satisfaction = 1`): **77 (30.8%)**
- **Not flagged low:** 173 (69.2%)
- Grade levels and subjects are roughly evenly distributed across both groups.

---

## Key Signal Differences: Low vs. Not-Low Groups

| Signal | Low Group Mean | Not-Low Group Mean | Δ |
|---|---|---|---|
| `open_neg_social_signals` | 0.701 | 0.029 | **+0.672** |
| `open_neg_emotional_signals` | 0.325 | 0.029 | **+0.296** |
| `open_neg_comprehension_signals` | 0.312 | 0.023 | **+0.289** |
| `open_neg_tech_signals` | 0.234 | 0.012 | **+0.222** |
| `open_neg_teacher_signals` | 0.143 | 0.006 | **+0.137** |
| `open_neg_engagement_signals` | 0.091 | 0.040 | **+0.051** |
| `open_pos_signals` | 0.195 | 0.711 | **−0.516** |
| `open_neg_categories_hit` | 1.494 | 0.133 | **+1.361** |
| `open_net_neg_per100words` | +4.12 | −1.48 | **+5.60** |

---

## Strongest Predictive Signals

### 1. Negative Social Signals (strongest single predictor)
The most discriminating signal by far. Low-satisfaction respondents mention **isolation, lack of peer interaction, and absence of group work** at 24× the rate of satisfied respondents (mean 0.70 vs. 0.03). Example language: *"zero peer interaction"*, *"can't collaborate with classmates"*, *"misses being able to raise her hand."*

### 2. Emotional Distress Signals
Emotional language (frustration, anxiety, crying, helplessness) is 11× more prevalent in the low group (0.33 vs. 0.03). Parents and students describing children who **"cry before every session"** or feel **"lost and overwhelmed"** are strong flags.

### 3. Comprehension Breakdown Signals
Difficulty following instruction—*"can't keep up," "already three problems ahead," "doesn't understand"*—appears 14× more in low responses (0.31 vs. 0.02). Closely linked to pacing mismatches in online delivery.

### 4. Technology Failure Signals
Camera freezes, platform log-outs, audio drops, and connectivity issues appear 19× more in low responses (0.23 vs. 0.01). Tech failures compound other issues by blocking comprehension and participation simultaneously.

### 5. Teacher Feedback Deficit Signals
Mentions of teachers being **unable to notice confusion**, lacking presence, or failing to respond appear at 24× the rate in the low group (0.14 vs. 0.006).

### 6. Multi-Category Co-occurrence
The average low-satisfaction response hits **1.49 negative categories**, versus 0.13 for not-low. Responses combining ≥2 categories (e.g., tech + social + emotional) are near-certain low predictors.

### 7. Net Negativity Density
`open_net_neg_per100words` averages **+4.1** for low vs. **−1.5** for not-low—meaning low responses have a net surplus of negative language per 100 words, while satisfied responses lean net positive.

---

## Satisfaction Score Distribution

| Rating | Low group (n=77) | Not-low group (n=173) |
|---|---|---|
| 1 | 16 (21%) | 9 (5%) |
| 2 | 26 (34%) | 23 (13%) |
| 3 | 30 (39%) | 45 (26%) |
| 4 | 4 (5%) | 64 (37%) |
| 5 | 1 (1%) | 32 (18%) |

The low-flag group is dominated by ratings 2–3, confirming open-response text captures dissatisfaction even at middling numeric ratings.

---

## Subject & Role Patterns

- **Arts** is the most common subject in the low group (21/77, 27%), suggesting creative/collaborative subjects suffer more in online formats.
- All three roles (Student, Teacher, Parent) contribute roughly equally to the low group (~31/21/25), indicating dissatisfaction is systemic rather than role-specific.

---

## Exceptions and Weak Evidence

- **13 low-flagged responses contain at least one positive signal**, indicating mixed-sentiment text where negatives dominate but some positives exist. These are correctly classified due to multi-category hit counts.
- **32 responses rated ≤2 on the numeric scale are NOT flagged low**, suggesting some low-rated respondents use emotionally neutral or terse language that doesn't trigger open-response signals—a coverage gap.
- **Engagement signals** are the weakest predictor (0.09 vs. 0.04, Δ = 0.05), possibly because disengagement is expressed indirectly through social or emotional language rather than explicit engagement terminology.

---

## Decision-Ready Summary

> **Open-response text most strongly predicts low learning satisfaction when it contains: (1) social isolation language, (2) emotional distress, (3) comprehension difficulty, and (4) technology failure—especially in combination (≥2 categories). A net negativity density above ~4 per 100 words and near-zero positive signals further confirm low satisfaction. Arts subjects and mixed-sentiment responses with clear negative dominance warrant particular attention.**
