---
dataset: education_survey_responses
scenario: eda_satisfaction
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: exploratory_data_analysis
focus_variable: "satisfaction_1to5"
query: "Across role, grade level, and subject, which open-response themes are associated with satisfaction?"
source_table: augment_table/education_survey_responses/eda_satisfaction/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:13:11.427987+00:00
wall_seconds: 125.25
---

# Open-Response Themes Associated with Satisfaction: Education Survey Analysis

**Dataset:** 250 respondents (89 Students, 81 Teachers, 80 Parents) | **Outcome:** `satisfaction_1to5` (mean 3.14, SD 1.18)

---

## Method Note

TAPP-generated columns used: `teaching_approach`, `innovative_curriculum_adaptation`, `student_engagement_level`, `subject_remote_fit`, `instructor_responsiveness`. These were extracted from the `open_response` free-text field and cross-validated against the structured columns `respondent_role`, `grade_level`, and `subject`. `instructor_responsiveness` has 29 missing values (11.6%); all other TAPP columns are fully covered.

---

## 1. Outcome Baseline by Structured Groups

Satisfaction differences by structured group alone are **modest** (< 0.25 points across roles, grade levels, and subjects). The open-response themes coded by TAPP explain far more variance.

| Dimension | Highest mean | Lowest mean | Δ |
|---|---|---|---|
| **Role** | Parent 3.22 | Teacher 3.06 | 0.16 |
| **Grade level** | 6–8: 3.20 | K–5: 3.05 | 0.15 |
| **Subject** | Science 3.27 | Arts 2.98 | 0.29 |

---

## 2. TAPP Theme Effects on Satisfaction

Each TAPP facet shows large, monotonic satisfaction gradients that hold across all three structured dimensions.

### 2a. Student Engagement Level (`student_engagement_level`)

The single strongest predictor. High engagement in open responses nearly perfectly separates high-satisfaction respondents.

| Engagement level | Mean sat. | n | % of high-sat (4–5) responses |
|---|---|---|---|
| `high_engagement` | **4.33** | 100 | 99% |
| `mixed_bifurcated` | 2.92 | 83 | — |
| `low_disengaged` | **1.64** | 67 | 0% |

**Gradient is flat across grade levels** (K-5: 4.30 / 1.55; 6-8: 4.36 / 1.64; 9-12: 4.32 / 1.72 for high vs. low engagement), meaning engagement themes matter equally from kindergarten through high school. Similarly uniform across all five subjects (range 4.26–4.38 for high engagement; 1.55–1.69 for low).

### 2b. Subject Remote Fit (`subject_remote_fit`)

Near-perfect alignment with satisfaction tier:

| Remote fit | Mean sat. | n | % of low-sat responses |
|---|---|---|---|
| `high_fit` | **4.33** | 99 | 0% |
| `moderate_fit` | 3.00 | 79 | — |
| `low_fit` | **1.65** | 72 | 97% |

Subject-level breakdown reveals that all subjects show identical patterns when respondents mention fit issues — no subject is structurally immune (Arts high_fit: 4.38; Math high_fit: 4.33; History high_fit: 4.26). The slightly lower overall Arts mean (2.98) partially reflects more `low_fit` mentions in that subject.

### 2c. Teaching Approach (`teaching_approach`)

| Approach | Mean sat. | n |
|---|---|---|
| `project_based` | **4.30** | 20 |
| `active_interactive` | **4.14** | 64 |
| `flipped_classroom` | 3.80 | 5 |
| `mixed` | 3.12 | 103 |
| `passive_lecture_only` | **1.61** | 57 |

Active/project-based themes appear in 56% of high-satisfaction responses; passive lecture themes appear in 91% of low-satisfaction responses. This effect holds across all roles: Parents mentioning active-interactive approaches average 4.38; Teachers 3.62; Students 4.20. Teachers expressing active approaches still rate lower than Students/Parents — likely because they also carry implementation burdens that temper their own satisfaction.

### 2d. Innovative Curriculum Adaptation (`innovative_curriculum_adaptation`)

| Adaptation level | Mean sat. | n |
|---|---|---|
| `high_innovation` | **4.28** | 93 |
| `moderate_adaptation` | 3.08 | 88 |
| `minimal_or_none` | **1.68** | 69 |

89% of high-satisfaction (4–5) responses mention `high_innovation`; 91% of low-satisfaction responses mention `minimal_or_none`. Teachers show the widest gap: high_innovation Teachers average 4.12 vs. minimal Teachers at ~1.6. Distribution of innovation mentions is relatively balanced across subjects (~16–23 each), so subject differences in overall satisfaction are not driven by differential innovation rates.

### 2e. Instructor Responsiveness (`instructor_responsiveness`)

| Responsiveness | Mean sat. | n |
|---|---|---|
| `highly_responsive` | **4.31** | 93 |
| `adequately_responsive` | 2.98 | 96 |
| `slow_or_absent` | **1.50** | 32 |

`slow_or_absent` mentions appear in 71% of low-satisfaction responses. The effect is consistent across roles (Student slow_or_absent: 1.50; Parent: 1.53; Teacher: 1.33). Note: 29 respondents have no responsiveness signal coded — likely open responses that focused on content/curriculum rather than instructor behavior.

---

## 3. Interaction: Role × Themes

| Role | Best theme combo (mean) | Worst theme combo (mean) |
|---|---|---|
| **Parent** | active_interactive + high_innovation → ~4.38 | passive + minimal → ~1.5 |
| **Student** | active_interactive + high_engagement → ~4.35 | passive + low_disengaged → ~1.5 |
| **Teacher** | project_based + high_innovation → ~4.12–4.30 | passive + minimal → ~1.3–1.6 |

Teachers show slightly lower peak satisfaction than Students/Parents even on the same positive themes, consistent with the implementation-burden hypothesis (they experience the same classroom positively but also bear the design and delivery stress).

---

## 4. Theme Co-occurrence: Mutually Reinforcing Patterns

The four high-satisfaction themes (`high_engagement`, `high_fit`, `active_interactive`/`project_based`, `high_innovation`) co-occur heavily. Virtually all low-satisfaction responses (sat 1–2) combine `low_disengaged` + `low_fit` + `passive_lecture_only` + `minimal_or_none`. The intermediate satisfaction tier (sat = 3) is dominated by `mixed_bifurcated` engagement + `moderate_fit` + `mixed` teaching approach + `moderate_adaptation` — these "mixed" open-response signals cluster at exactly the midpoint.

---

## 5. Key Findings

1. **Engagement and subject/remote fit are the dominant themes** — both show near-perfect stratification of satisfaction across all roles, grade levels, and subjects, with no structural group interactions that alter the direction.
2. **Active/project-based teaching and curriculum innovation are closely coupled positive drivers** — respondents who mention one almost always mention the other, and both independently correlate with satisfaction ~4.1–4.3 vs. ~1.6 for their negative counterparts.
3. **Instructor responsiveness is a strong low-satisfaction driver** — `slow_or_absent` has the lowest mean (1.50) of any TAPP category and is mentioned in 71% of low-satisfaction responses, but is less frequently the *sole* theme in high satisfaction.
4. **Structural group differences (role, grade, subject) are small** — the ≤0.3-point gaps across groups are dwarfed by 2.5–2.7-point gaps within groups by theme. Open-response themes, not demographic/structural categories, are the primary satisfaction differentiators.
5. **Science edges out other subjects** (3.27) partly because it has the highest share of `high_fit` and `high_innovation` mentions (23 high-innovation vs. ~16–19 for others), but even this structural advantage disappears when controlling for themes.
