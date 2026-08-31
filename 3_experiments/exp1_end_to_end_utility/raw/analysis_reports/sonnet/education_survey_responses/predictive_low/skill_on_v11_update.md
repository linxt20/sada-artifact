---
dataset: education_survey_responses
scenario: predictive_low
variant: skill_on
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "satisfaction_1to5"
query: "What open-response signals predict low learning satisfaction?"
source_table: augment_table/education_survey_responses/predictive_low/sonnet__skill_on_v11_update.csv
generated_at: 2026-07-30T07:12:51.436252+00:00
wall_seconds: 88.93
---

# Open-Response Signals Predicting Low Learning Satisfaction

**Dataset:** 250 education survey responses · Focus variable: `satisfaction_1to5` · Low satisfaction defined as ≤ 2 (n = 74, 30%)

---

## 1. Structured-Column Context

Before examining open text, the structured columns reveal near-perfect separators for low satisfaction:

| Column | Values strongly associated with low sat (≤2) | Low-sat rate |
|---|---|---|
| `teacher_responsiveness` | `absent_or_unresponsive`, `slow_or_infrequent` | 100%, 96% |
| `instructional_mode_quality` | `worksheets_only_no_instruction`, `passive_slideshow_readthrough` | 100%, 90% |
| `student_engagement_signal` | `disengaged_avoidance_behavior`, `disengaged_cameras_off` | 100%, 100% |
| `subject_format_fit` | `fundamentally_incompatible`, `poorly_adapted` | 100%, 100% |
| `peer_interaction_loss` | `severe_loss_community_absent`, `moderate_loss_affects_learning` | 100%, 65% |

These structured signals provide a strong baseline; the open responses add *texture and specificity* to each failure mode.

---

## 2. Open-Response Signal Themes

### 2.1 Technical Disruption ("lost," "lag," "freeze," "load")
- **"lost"** appears in 11% of low-sat responses vs. 0% of high-sat responses.
- **"lag"** appears 7× more frequently in low vs. high satisfaction.
- Respondents describe falling irreversibly behind: *"by the time it loads he's already three problems ahead"*; *"the platform logs her out repeatedly."*
- **Predictive signal:** Technical failure language — especially *platform disconnection* and *inability to keep pace* — is a strong low-satisfaction marker.

### 2.2 Social / Peer Isolation ("miss," "friend," "alone," "silent")
- **"miss"** appears in 15% of low-sat vs. 3% of high-sat responses (5× ratio).
- **"silent"** and **"alone"** appear exclusively or near-exclusively in low-sat text.
- Representative quotes: *"zero peer interaction"*; *"Choir over Zoom is the worst — we can't sing together."*
- **Predictive signal:** Explicit mention of missing peers, silence in class, or absence of social learning is a reliable low-satisfaction cue.

### 2.3 Passive/Worksheet-Only Instruction ("worksheet," "no instruction")
- **"worksheet"** appears 7× in low-sat, 0× in high-sat responses.
- Respondents describe receiving uploaded files with no accompanying teaching: *"just worksheets uploaded with no instruction … the teacher rarely responds."*
- **Predictive signal:** References to worksheet-only or self-directed work without teacher support co-occur exclusively with low satisfaction.

### 2.4 Emotional Distress ("overwhelm," "cry," "dread," "quit")
- **"overwhelm"** (5%), **"quit"** (5%) appear only in low-sat responses.
- Emotional language ranges from child distress (*"cries before every reading session"*) to teacher burnout (*"I dread Monday mornings"*) to student withdrawal (*"thinking about dropping the elective"*).
- **Predictive signal:** Affective distress vocabulary — especially avoidance intent and tears/anxiety — strongly predicts satisfaction ≤ 2.

### 2.5 Subject-Format Incompatibility ("can't," "doesn't translate," "pointless")
- Low-sat responses for Arts and Math frequently describe the format as fundamentally broken for the subject: *"manipulatives don't translate"*; *"Choir over Zoom is the worst."*
- Math (18 low-sat cases) and Arts (15) are the most over-represented subjects.
- **Predictive signal:** Explicit statements that the online format is *structurally incompatible* with the subject (e.g., performance arts, early-math manipulatives) signal very low satisfaction.

---

## 3. Role and Grade Patterns

Low-satisfaction responses are roughly evenly distributed across **Students** (27), **Teachers** (24), and **Parents** (23), suggesting systemic rather than role-specific dissatisfaction. Grade **9–12** has the most low-sat cases (29), driven by disengagement and isolation language; **K–5** (23) is driven more by parental reporting of child distress and platform access issues.

---

## 4. Exceptions and Weak Evidence

- **"interact"** and **"camera"** do not discriminate well (similar rates in low and high satisfaction), so camera presence alone is not predictive.
- A small share of `responsive_minimal_feedback` teachers still achieve mid-range satisfaction (34% low vs. 66% not-low), indicating teacher responsiveness is necessary but not alone sufficient.
- The structured columns are near-perfect predictors; open responses add explanatory richness but few cases where open text predicts low satisfaction that the structured columns miss.

---

## 5. Decision-Ready Summary

| Open-response signal | Low-sat rate when present | Strength |
|---|---|---|
| "lost" / falling behind in real time | 11% of low-sat, 0% of high-sat | **Strong** |
| Peer/social isolation language | 15% (miss), 8% (silent/alone) vs. ≤3% high | **Strong** |
| Worksheet-only / no live instruction | 7% vs. 0% high | **Strong** |
| Emotional distress / withdrawal intent | 5% each, exclusive to low | **Strong** |
| Technical failure (lag, freeze, load) | 4–7% vs. ≤1% high | **Moderate** |
| Subject-format incompatibility | Qualitative, Arts/Math concentrated | **Moderate** |

Surveyors and educators should flag open responses containing *any combination* of isolation language, distress vocabulary, passive-instruction complaints, or real-time technical disruption as high-risk for low learning satisfaction.
