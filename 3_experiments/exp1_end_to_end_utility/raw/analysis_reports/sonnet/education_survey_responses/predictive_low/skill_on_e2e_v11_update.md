---
dataset: education_survey_responses
scenario: predictive_low
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "satisfaction_1to5"
query: "What open-response signals predict low learning satisfaction?"
source_table: augment_table/education_survey_responses/predictive_low/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:13:13.773707+00:00
wall_seconds: 107.55
---

# Open-Response Signals Predicting Low Learning Satisfaction
**Dataset:** `education_survey_responses` — 250 survey responses (Students: 89, Teachers: 81, Parents: 80)  
**Outcome variable:** `satisfaction_1to5` ≤ 2 = "low satisfaction" (74 cases, **29.6% base rate**)  
**TAPP columns used:** `instruction_quality_signal`, `student_engagement_level`, `disengagement_pattern`, `positive_adaptation_signal`, `teacher_support_quality`, `subject_format_fit`, `peer_interaction_loss_signal`, `learner_emotional_distress`

---

## Key Finding

Low satisfaction is predicted by a **consistent cluster of five open-response signals** — poor format fit, absent teacher support, no positive adaptation, peer community loss, and emotional distress. When 4–5 of these co-occur, mean satisfaction collapses to **1.42–1.80** (scale 1–5). No single structured dimension (role, grade, subject) differentiates strongly; the predictive power is almost entirely in the semantic content of open responses.

---

## 1. Outcome Baseline

| Satisfaction | n | % |
|---|---|---|
| 1 (very low) | 25 | 10% |
| 2 (low) | 49 | 20% |
| 3 (neutral) | 75 | 30% |
| 4 (high) | 68 | 27% |
| 5 (very high) | 33 | 13% |

Low satisfaction is **not concentrated by role** (Student 30%, Teacher 30%, Parent 29%) or **grade level** (K-5: 30%, 6-8: 29%, 9-12: 30%) or **subject** (Math 34% highest, Science 25% lowest — modest variation). The predictive signal must come from qualitative content.

---

## 2. Primary Predictors from TAPP Columns

### 2a. `subject_format_fit` — Strongest single predictor

| Value | n | Low-sat n | Low-sat rate |
|---|---|---|---|
| `low_fit_compromised` | 72 | 72 | **100%** |
| `partial_fit_mixed` | 78 | 2 | 2.6% |
| `high_fit_thriving` | 100 | 0 | 0% |

All 72 respondents whose open text indicated the subject/content format was incompatible with the remote/online modality reported low satisfaction. This is the single most discriminating TAPP facet.

---

### 2b. `positive_adaptation_signal` — Near-perfect inverse predictor

| Value | n | Low-sat rate |
|---|---|---|
| `absent_not_present` | 58 | **100%** |
| `weak_surface_compliance` | 15 | 93% |
| `moderate_works_well_enough` | 77 | 2.6% |
| `strong_thriving_exceeded_expectations` | 100 | 0% |

When open responses contain no signal of constructive adaptation by teachers or learners, low satisfaction is near-certain. This cross-validates `subject_format_fit` but captures a distinct semantic dimension (agency/adaptation vs. structural fit).

---

### 2c. `teacher_support_quality`

| Value | n | Low-sat rate |
|---|---|---|
| `absent_unresponsive` | 13 | **100%** |
| `minimal_overwhelmed` | 46 | 98% |
| `adequate_trying` | 88 | 18% |
| `strong_innovative` | 103 | 0% |

59 respondents whose open texts described absent or overwhelmed teacher support had a 98–100% low-satisfaction rate.

---

### 2d. `learner_emotional_distress`

| Value | n | Low-sat rate |
|---|---|---|
| `high_distress_crying_avoidance` | 7 | **100%** |
| `moderate_frustration_dread` | 30 | **100%** |
| `mild_boredom_fatigue` | 21 | 71% |
| `not_present` | 192 | 11% |

Any mention of frustration, dread, avoidance, or crying in open text is a **perfect** predictor of low satisfaction. Mild boredom/fatigue still confers 71% low-sat risk. Combined with `subject_format_fit=low_fit_compromised`, the 37-case overlap yields mean satisfaction = **1.49**.

---

### 2e. `peer_interaction_loss_signal`

| Value | n | Low-sat rate |
|---|---|---|
| `severe_community_absent` | 79 | **82%** |
| `moderate_awkward_breakouts` | 8 | 13% |
| `not_present` | 157 | 5% |
| `mild_forums_substitute` | 6 | 0% |

Respondents describing total loss of peer community drive 82% low satisfaction. Among the 74 low-sat cases, 65 (88%) involved `severe_community_absent`.

---

### 2f. `student_engagement_level` (numeric, 1–5)

| TAPP engagement | n | Low-sat rate |
|---|---|---|
| 1 | 52 | **100%** |
| 2 | 27 | 78% |
| 3 | 67 | 1.5% |
| 4 | 12 | 0% |
| 5 | 92 | 0% |

This facet strongly mirrors `satisfaction_1to5` (both on 1–5 scale), confirming the open-response engagement signal is tightly coupled with the rated outcome.

---

### 2g. `disengagement_pattern`

| Value | n | Low-sat rate |
|---|---|---|
| `cameras_off_silent` | 4 | 100% |
| `compliance_only_no_joy` | 24 | 92% |
| `attention_span_collapse` | 14 | 64% |
| `disappeared_from_roster` | 12 | 42% |
| `not_present` | 196 | 17% |

Among low-sat cases, `compliance_only_no_joy` was the most common disengagement pattern (22 of 74 low-sat cases). This TAPP facet adds specificity to **how** disengagement manifests beyond the numeric `student_engagement_level`.

---

### 2h. `instruction_quality_signal` — Additive but partially redundant

| Value | n | Low-sat rate |
|---|---|---|
| `no_instruction_worksheets_only` | 6 | 100% |
| `passive_slideshow_readthrough` | 11 | 91% |
| `adequate_functional` | 125 | 46% |
| `innovative_adapted` | 108 | 0% |

This facet adds signal, but overlaps substantially with `teacher_support_quality` and `positive_adaptation_signal`. Its unique contribution is flagging pure worksheet-dump or passive delivery as specific failure modes.

---

## 3. Signal Stacking: Cumulative Risk

Assigning one "bad signal" point for each of five TAPP conditions (`low_fit_compromised`, emotional distress ≥ moderate, teacher support absent/minimal, no positive adaptation, severe peer loss):

| Bad signals present | n | Mean satisfaction |
|---|---|---|
| 0 | 161 | 3.83 |
| 1 | 17 | 2.94 |
| 2 | 5 | 1.80 |
| 3 | 6 | 2.00 |
| 4 | 30 | 1.80 |
| 5 | 31 | **1.42** |

31 respondents triggered all five bad signals; their mean satisfaction was **1.42**, representing the highest-risk subgroup. The 4–5 signal zone (n=61) accounts for **68% of all low-satisfaction cases**.

---

## 4. Synthesis: Predictive Signal Hierarchy

| Rank | Open-response signal (TAPP column) | Low-sat rate when present | Coverage among low-sat cases |
|---|---|---|---|
| 1 | `subject_format_fit = low_fit_compromised` | 100% | 97% (72/74) |
| 2 | `positive_adaptation_signal = absent/weak` | 93–100% | 97% (72/74) |
| 3 | `teacher_support_quality = absent/minimal` | 98–100% | 78% (59/74) |
| 4 | `learner_emotional_distress = moderate/high` | 100% | 50% (37/74) |
| 5 | `peer_interaction_loss_signal = severe` | 82% | 88% (65/74) |
| 6 | `disengagement_pattern ≠ not_present` | 42–100% | 54% (40/74) |
| 7 | `instruction_quality_signal = passive/none` | 91–100% | 22% (16/74) |

---

## 5. Conclusions

1. **Format-content mismatch** (`subject_format_fit`) is the single strongest signal: every respondent whose open text described online format as incompatible with their subject reported low satisfaction.
2. **Absence of adaptive agency** (`positive_adaptation_signal`) is equally decisive — respondents who saw no creative or constructive response from educators were almost certain to report low satisfaction.
3. **Teacher unavailability or overwhelm** (`teacher_support_quality`) and **total peer community loss** (`peer_interaction_loss_signal`) compound risk severely and independently.
4. **Emotional language** (frustration, dread, crying — `learner_emotional_distress`) perfectly identifies the worst-affected cases, especially when co-occurring with format mismatch.
5. Structured variables (role, grade, subject) add little predictive power; the signal is overwhelmingly in the qualitative open-response content as captured by TAPP semantic columns.

---

## Method Note

TAPP-generated columns analyzed: `instruction_quality_signal`, `student_engagement_level`, `disengagement_pattern`, `positive_adaptation_signal`, `teacher_support_quality`, `subject_format_fit`, `peer_interaction_loss_signal`, `learner_emotional_distress`. All eight columns were cross-tabulated against the structured `satisfaction_1to5` outcome and role/grade/subject groupings. `student_engagement_level` was treated as a numeric 1–5 facet parallel to the outcome scale; the remaining seven were treated as categorical. Signal stacking used five of the eight TAPP columns (excluding `student_engagement_level`, `disengagement_pattern`, and `instruction_quality_signal` as partially redundant) to build a cumulative risk score validated against mean satisfaction.
