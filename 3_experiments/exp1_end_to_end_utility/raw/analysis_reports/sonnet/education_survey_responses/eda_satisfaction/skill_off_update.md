---
dataset: education_survey_responses
scenario: eda_satisfaction
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: exploratory_data_analysis
focus_variable: "satisfaction_1to5"
query: "Across role, grade level, and subject, which open-response themes are associated with satisfaction?"
source_table: augment_table/education_survey_responses/eda_satisfaction/sonnet__skill_off_update.csv
generated_at: 2026-07-28T13:08:06.482937+00:00
wall_seconds: 57.86
---

# Open-Response Themes Associated with Satisfaction
**Dataset:** `education_survey_responses` | **Variant:** `skill_off_update` | **n = 250**

---

## 1. Overall Satisfaction Landscape

The dataset's satisfaction scores (1–5) average **3.14** (SD = 1.18), roughly centred. The most prevalent open-response themes are **social connection** (92 mentions) and **hands-on need** (91 mentions), followed by **engagement** (76). Less common but analytically important themes include **disengagement** (26), **teacher quality** (26), **flexible learning** (19), and **tech issues** (14).

---

## 2. Themes by Association with Satisfaction

The table below shows mean satisfaction when a theme is present vs. absent.

| Theme | Mean sat. (present) | Mean sat. (absent) | Δ | Corr. |
|---|---|---|---|---|
| **teacher_quality** | 3.88 | 3.05 | **+0.83** | +0.22 |
| **flexible_learning** | 3.74 | 3.09 | **+0.65** | +0.15 |
| outcomes_positive | 3.30 | 3.13 | +0.17 | +0.04 |
| new_opportunity | 3.26 | 3.13 | +0.13 | +0.03 |
| engagement | 3.18 | 3.12 | +0.06 | +0.03 |
| social_connection | 3.10 | 3.16 | −0.06 | −0.03 |
| equity_concern | 2.82 | 3.15 | −0.33 | −0.06 |
| hands_on_need | 2.82 | 3.32 | **−0.50** | −0.20 |
| tech_issues | 2.29 | 3.19 | **−0.90** | −0.18 |
| **outcomes_negative** | 2.05 | 3.23 | **−1.18** | −0.27 |
| **disengagement** | 2.12 | 3.26 | **−1.14** | −0.30 |

### Key positive drivers
- **Teacher quality** (n = 26): Strongest positive signal. Respondents praising instructor creativity, responsiveness, or quality score ~0.8 points higher than average. Concentrated among Parents (21 % prevalence) and Teachers themselves.
- **Flexible learning** (n = 19): Self-pacing and asynchronous access tied to +0.65 satisfaction lift. Appears most among 9–12 students (15 % prevalence).

### Key negative drivers
- **Disengagement** (n = 26, r = −0.30): Strongest negative correlate. Mean satisfaction drops to 2.12 when present. Elevated for Students (20 % prevalence) vs. Teachers (7 %) or Parents (4 %).
- **Outcomes negative** (n = 20, r = −0.27): Complaints about learning loss, grade impact, or failed skills yield mean satisfaction of 2.05. Appears most in Parent responses (14 %).
- **Tech issues** (n = 14): Small sample but dramatic drop (−0.90). Concentrated in Math (11 % prevalence) and K-5 responses.
- **Hands-on need** (n = 91): The most policy-relevant negative theme. Widespread especially in Arts (72 %) and Science (49 %), corresponding to those subjects' below-average satisfaction scores (2.98 and 3.27 respectively). Correlation is moderate (−0.20) but breadth is large.

### Neutral / ambiguous themes
- **Engagement** and **social connection** show near-zero net satisfaction effect. While engagement framing is generally positive, it co-occurs with disengagement contexts enough to flatten the signal. Social connection sentiment is mixed (longing for peers vs. celebration of online community).

---

## 3. Breakdown by Role

| Role | n | Mean sat. | Top themes (prevalence) |
|---|---|---|---|
| Student | 89 | 3.13 | Engagement (43%), Social connection (43%), Disengagement (20%) |
| Teacher | 81 | 3.06 | Hands-on need (47%), Social connection (36%), Engagement (22%) |
| Parent | 80 | 3.23 | Social connection (31%), Teacher quality (21%), Outcomes negative (14%) |

- **Students** report the most disengagement (20 %) — consistent with their lower satisfaction ceiling.
- **Teachers** flag hands-on need most urgently (47 %) and are the lowest-satisfaction group despite being educators; their concern is pedagogical rather than personal dissatisfaction.
- **Parents** are most likely to mention teacher quality (positively, 21 %) and outcomes negatively (14 %), reflecting a proxy-evaluator role.

---

## 4. Breakdown by Grade Level

| Grade | n | Mean sat. | Notable themes |
|---|---|---|---|
| K-5 | 76 | 3.05 | Social connection (38%), Engagement (34%), Outcomes negative (12%) |
| 6-8 | 76 | 3.20 | Hands-on need (36%), Engagement (29%), Social connection (29%) |
| 9-12 | 98 | 3.16 | Hands-on need (43%), Social connection (42%), Flexible learning (15%) |

- **K-5** has the lowest satisfaction and the highest rate of outcomes-negative mentions (12 %), suggesting concrete learning-loss concerns in early grades.
- **9-12** benefits most from flexible learning (15 %) — older students can self-regulate asynchronous content — partially offsetting the hands-on gap.

---

## 5. Breakdown by Subject

| Subject | n | Mean sat. | Notable themes |
|---|---|---|---|
| Arts | 46 | **2.98** (lowest) | Hands-on need (72%), Social connection (48%), Engagement (39%) |
| Math | 53 | 3.08 | Outcomes positive (25%), Tech issues (11%), Engagement (21%) |
| History | 46 | 3.15 | Social connection (50%), Engagement (37%), Disengagement (15%) |
| English | 50 | 3.20 | Social connection (46%), Teacher quality (18%), Outcomes negative (16%) |
| Science | 55 | **3.27** (highest) | Hands-on need (49%), Engagement (31%), Equity concern (9%) |

- **Arts** combines the highest hands-on need prevalence with the lowest satisfaction — the online format is a poor fit for studio/performance-based learning.
- **Science** is the highest-satisfaction subject despite near-identical hands-on need prevalence, likely because teachers have adapted with kitchen/home-lab experiments (reflected in teacher-quality and engagement mentions).
- **Math** is noteworthy for its tech-issues rate (11 %, highest subject) and outcomes-positive mentions (25 %) — suggesting polarisation between frustrated and successful learners.
- **History** has the highest disengagement rate (15 %) among subjects.

---

## 6. Summary of Key Findings

| Direction | Theme | Primary locus |
|---|---|---|
| ↑ Satisfaction | Teacher quality | Parents; English/Arts |
| ↑ Satisfaction | Flexible learning | 9–12 students; History/English |
| ↓ Satisfaction | Disengagement | Students; History; K-5 |
| ↓ Satisfaction | Outcomes negative | Parents; K-5; English |
| ↓ Satisfaction | Tech issues | Math; K-5 (small n) |
| ↓ Satisfaction | Hands-on need | Arts (severe); Science; Teachers |

**Caveats:** Correlations are modest (|r| ≤ 0.30) and most theme samples are small (n < 30), so causal inference is not warranted. Engagement and social-connection themes are near-ubiquitous and sentimentally mixed, limiting their discriminatory power. The hands-on-need theme's negative association is widespread but moderate, suggesting it reflects frustration without necessarily collapsing overall satisfaction.
