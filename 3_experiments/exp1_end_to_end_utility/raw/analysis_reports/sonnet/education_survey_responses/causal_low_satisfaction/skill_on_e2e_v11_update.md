---
dataset: education_survey_responses
scenario: causal_low_satisfaction
variant: skill_on_e2e
model: substrate-claude-sonnet-4-6
prompt_style: e2e
query_subtype: causal_attribution
focus_variable: "satisfaction_1to5"
query: "Why is learning satisfaction low for certain groups, and which factors drive it?"
source_table: augment_table/education_survey_responses/causal_low_satisfaction/sonnet__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:12:52.807829+00:00
wall_seconds: 128.08
---

# Causal Analysis: Why Is Learning Satisfaction Low?
**Dataset:** `education_survey_responses` | **N = 250** | **Query date:** 2026-07-30

---

## Executive Summary

Overall mean satisfaction is **3.14 / 5**; **74 respondents (29.6%)** score 1–2 ("low satisfaction"). Low satisfaction is not concentrated in one demographic group—it is distributed fairly evenly across roles, grade levels, and subjects—but it is *almost perfectly predicted* by a cluster of four structural failure modes surfaced by the TAPP-augmented columns.

---

## 1. Outcome Variable & Structured Group Differences

**Satisfaction distribution (n = 250):**

| Score | Count | % |
|-------|-------|---|
| 1 | 25 | 10% |
| 2 | 49 | 20% |
| 3 | 75 | 30% |
| 4 | 68 | 27% |
| 5 | 33 | 13% |

**Low-satisfaction rate by demographic group:**

| Group | Mean Sat | Low-Sat Rate | n |
|-------|----------|--------------|---|
| **Role: Student** | 3.13 | 30.3% | 89 |
| **Role: Teacher** | 3.06 | 29.6% | 81 |
| **Role: Parent** | 3.22 | 28.8% | 80 |
| **Grade: K–5** | 3.05 | 30.3% | 76 |
| **Grade: 6–8** | 3.20 | 28.9% | 76 |
| **Grade: 9–12** | 3.16 | 29.6% | 98 |
| **Subject: Math** | 3.08 | 34.0% | 53 |
| **Subject: Arts** | 2.98 | 32.6% | 46 |
| **Subject: Science** | 3.27 | 25.5% | 55 |

**Key finding:** No single demographic group stands out as uniquely at risk. Math and Arts have the highest low-satisfaction rates but only modestly so. Low satisfaction is a cross-cutting phenomenon driven by *process* factors, not group membership.

---

## 2. Causal Drivers: TAPP-Augmented Factor Analysis

The six TAPP-generated columns show near-perfect separation between low- and high-satisfaction respondents. All six are strongly relevant; none are redundant with the original structured columns.

### 2.1 Pedagogy Adaptation Quality (`pedagogy_adaptation_quality`)

| Value | Mean Sat | Low-Sat Rate | n |
|-------|----------|--------------|---|
| absent_or_neglectful | 1.47 | **100%** | 15 |
| passive_or_unchanged | 1.71 | **100%** | 51 |
| adequate_but_unremarkable | 2.88 | 10% | 80 |
| innovative_and_engaging | 4.29 | 0% | 104 |

All 66 respondents in the two "failed pedagogy" categories scored ≤ 2. This is the single strongest individual predictor of low satisfaction.

### 2.2 Teacher Feedback & Responsiveness (`teacher_feedback_and_responsiveness`)

| Value | Mean Sat | Low-Sat Rate | n |
|-------|----------|--------------|---|
| absent_or_unreachable | 1.33 | 100% | 6 |
| slow_or_minimal | 1.75 | **95.6%** | 68 |
| adequate | 3.13 | 3.5% | 86 |
| timely_and_detailed | 4.32 | 0% | 90 |

Slow or absent feedback is present in **96.0% of low-satisfaction responses** (71/74).

### 2.3 Peer Social Interaction Loss (`peer_social_interaction_loss`)

| Value | Mean Sat | Low-Sat Rate | n |
|-------|----------|--------------|---|
| significant_loss_of_community | 1.78 | **89.6%** | 77 |
| partial_loss_manageable | 2.97 | 6.7% | 75 |
| adapted_or_replaced_digitally | 4.32 | 0% | 41 |
| not_present (already remote-native) | 4.35 | 0% | 57 |

93% of low-satisfaction respondents (69/74) experienced significant community loss.

### 2.4 Subject–Remote Format Fit (`subject_remote_format_fit`)

| Value | Mean Sat | Low-Sat Rate | n |
|-------|----------|--------------|---|
| low_fit | 1.65 | **100%** | 72 |
| moderate_fit | 2.99 | 2.6% | 78 |
| high_fit | 4.33 | 0% | 100 |

Math and Arts scoring higher low-satisfaction rates (34% and 33%) aligns with these subjects having lower remote format fit. Science (25.5% low-sat) has stronger lab-at-home adaptability.

### 2.5 Student Engagement Level (`student_engagement_level`)

| Value | Mean Sat | Low-Sat Rate | n |
|-------|----------|--------------|---|
| disengaged_or_checked_out | 1.58 | **100%** | 55 |
| partially_engaged | 2.77 | 20.4% | 93 |
| actively_engaged | 4.31 | 0% | 102 |

Engagement appears to be both a mediator and an outcome—poor pedagogy and absent feedback produce disengagement, which further depresses satisfaction.

### 2.6 Async Format Benefit (`async_format_benefit`)

| Value | Mean Sat | Low-Sat Rate | n |
|-------|----------|--------------|---|
| not_present | 2.67 | **44.0%** | 168 |
| moderate_benefit | 3.28 | 0% | 18 |
| strong_benefit | 4.33 | 0% | 64 |

100% of low-satisfaction respondents (74/74) receive no async benefit. This reflects that asynchronous flexibility (recorded lectures, self-paced materials) is a meaningful protective factor—but only when well-implemented alongside adequate pedagogy and feedback.

---

## 3. Co-Occurrence: Compound Risk Cluster

**54 of 74 low-satisfaction respondents (73%)** simultaneously exhibit all four core failure modes:
- `pedagogy_adaptation_quality` = *absent_or_neglectful* or *passive_or_unchanged*
- `peer_social_interaction_loss` = *significant_loss_of_community*
- `teacher_feedback_and_responsiveness` = *slow_or_minimal* or *absent_or_unreachable*
- `student_engagement_level` = *disengaged_or_checked_out*

The remaining 20 low-satisfaction respondents have 2–3 of the four factors. **No low-satisfaction respondent is missing all four.** This compound cluster, not any single factor, is the primary causal driver.

---

## 4. Summary of Causal Mechanisms

```
Poor pedagogy adaptation  ──┐
Absent/slow teacher feedback ──┼──► Disengagement ──► Low Satisfaction (1–2)
Significant peer/social loss  ──┤
Low subject–remote format fit ──┘
        ↑
No async format benefit (absent mitigation)
```

- **Primary cause:** Teachers who did not adapt pedagogy (*passive_or_unchanged*, *absent_or_neglectful*) + minimal feedback loops → students disengage → satisfaction collapses to 1–2.
- **Amplifier:** Social isolation (`peer_social_interaction_loss = significant_loss_of_community`) removes the community support that could buffer poor instruction.
- **Subject/format mismatch:** Math and Arts in remote settings score low on `subject_remote_format_fit`, correlating with slightly elevated low-sat rates (34%, 33% vs. 25–28% for History/English/Science).
- **K–5 marginally worse:** Youngest learners (K–5: 30.3% low-sat) are more dependent on in-person scaffolding; parents report platform reliability failures and zero peer interaction (consistent with `peer_social_interaction_loss = significant_loss_of_community`).
- **No async benefit as absence of protective factor:** Strong async implementation fully eliminates low satisfaction in this dataset (0% low-sat among `strong_benefit` group, n=64), making it a high-leverage intervention point.

---

## 5. Actionable Implications

| Priority | Intervention | Evidence |
|----------|-------------|---------|
| 🔴 High | Mandate structured pedagogy redesign for remote delivery | 100% low-sat when `pedagogy_adaptation_quality` ≤ passive |
| 🔴 High | Establish feedback SLAs (e.g., 24-hr response) | 95.6% low-sat with slow/absent feedback |
| 🟠 Medium | Implement digital peer interaction mechanisms | 89.6% low-sat with significant community loss |
| 🟠 Medium | Subject-specific remote playbooks for Math & Arts | Highest low-sat rates; lowest `subject_remote_format_fit` |
| 🟡 Lower | Expand async content libraries | Strong async benefit → 0% low-sat, but only works with above foundations |

---

## Method Note

**TAPP-generated columns used in this report (exact names):**
`pedagogy_adaptation_quality`, `peer_social_interaction_loss`, `teacher_feedback_and_responsiveness`, `async_format_benefit`, `student_engagement_level`, `subject_remote_format_fit`

All six columns showed strong, non-redundant signal. Original structured columns (`respondent_role`, `grade_level`, `subject`, `satisfaction_1to5`) served as the primary grouping and outcome variables; TAPP columns provided the semantic causal layer explaining *why* satisfaction is low within those groups.
