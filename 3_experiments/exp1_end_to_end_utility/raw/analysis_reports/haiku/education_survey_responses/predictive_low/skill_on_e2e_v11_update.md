---
dataset: education_survey_responses
scenario: predictive_low
variant: skill_on_e2e
model: substrate-claude-haiku-4-5
prompt_style: e2e
query_subtype: predictive_feature_engineering
focus_variable: "satisfaction_1to5"
query: "What open-response signals predict low learning satisfaction?"
source_table: augment_table/education_survey_responses/predictive_low/haiku__skill_on_e2e_v11_update.csv
generated_at: 2026-07-30T07:13:58.991621+00:00
wall_seconds: 153.68
---

# Open-Response Signals Predicting Low Learning Satisfaction

## Executive Summary

Analysis of 250 education survey responses (from students, teachers, and parents across K-12 grades and five subjects) reveals that **low learning satisfaction (ratings 1–2, n=74) is robustly predicted by a combination of semantic signals in open-response text**, particularly around **peer interaction loss, poor engagement sentiment, and emotional distress**. High satisfaction (ratings 4–5, n=101) is characterized by their near-total absence.

The augmented dataset shows that low-satisfaction respondents report an average of **3.92 TAPP-identified semantic facets simultaneously**, compared to only 0.12 in high-satisfaction responses—a stark 33-fold difference. No single factor alone drives low satisfaction; rather, multiple interacting barriers across collaboration, instruction, modality fit, and emotional experience combine to suppress learning satisfaction.

---

## Methods Note

This analysis examined the augmented table combining original structured columns (satisfaction_1to5, respondent_role, grade_level, subject, open_response) with six TAPP-generated semantic columns:
- `interaction_collaboration_loss`
- `subject_modality_fit`
- `instruction_quality`
- `engagement_sentiment`
- `emotional_distress`
- `emotional_distress_signals`

All six augmented columns achieved 100% coverage (250/250 non-null) and are cited below where they clarify patterns. Original columns provided complementary perspective.

---

## Key Findings

### 1. Peer Interaction Loss is Near-Universal in Low Satisfaction

**89.2% (66 of 74) of low-satisfaction respondents report signals of `interaction_collaboration_loss`**, versus 0% in high-satisfaction responses.

The dominant form is **`cannot_replicate_peer_discussion`** (45 of 74 low-sat respondents; 60.8%):
- Spans all subjects: Math (12), History (12), English (10), Science (10), Arts (1)
- Equally distributed across student, teacher, and parent perspectives (18, 14, 13 respectively)
- Representative quotes: "No debates, no group projects," "Cameras off, microphones muted," "breakout rooms are awkward because nobody talks"

Other collaboration signals in low satisfaction:
- `collaborative_work_diminished`: 9 respondents
- `live_classroom_energy_missing`: 7 respondents
- `no_ensemble_or_group_performance`: 5 respondents (primarily in arts electives)

**Cross-check with structured data:** The respondent role distribution (Student 36%, Teacher 32%, Parent 32%) across low-satisfaction responses mirrors the overall sample, confirming that peer loss complaints are not isolated to one perspective.

---

### 2. Negative Engagement Sentiment is Categorical in Low Satisfaction

**100% (74 of 74) low-satisfaction respondents exhibit negative engagement**, with high specificity:

- **`dreading_or_avoiding_class`** (31 respondents, 41.9%): "I dread Monday morning logins," "she cries before every reading session," "thinking about dropping the elective"
- **`bored_or_disengaged`** (28 respondents, 37.8%): "I just click through assignments to keep my GPA," "Math feels exhausting," "feels pointless"
- **`neutral_or_functional_compliance`** (15 respondents, 20.3%): Passive resignation ("it's not ideal, but we're getting through")

In stark contrast, **100% (101 of 101) high-satisfaction respondents exhibit `enthusiastic_about_class_or_topics`**: "I actually look forward to art Tuesdays," "I've built a stronger body of work," "best class ever honestly."

**Cross-check with satisfaction ratings:** All 31 dread respondents and 28 bored respondents cluster in satisfaction ratings 1–2, with zero overlap to ratings 4–5. This perfect stratification validates the semantic encoding.

---

### 3. Emotional Distress is Nearly Ubiquitous in Low Satisfaction

**97.3% (72 of 74) low-satisfaction respondents report `emotional_distress` signals**, concentrated in two forms:

- **`loss_of_curiosity_or_motivation`** (33 respondents, 44.6%): "my curiosity drained by Friday," "lost the foundational experiences," "used to love history and now I just," "His motivation is gone"
- **`frustration_with_format_or_parent`** (27 respondents, 36.5%): "by the time it loads he's already three problems ahead," "we end up frustrated by dinner," "the technology simply cannot replace"

Less prevalent but severe:
- **`crying_or_anxiety_before_or_during_class`** (5 respondents, 6.8%): "My second grader cries before every reading session," "I can't find my pencil and the teacher can't see my paper"
- **`confidence_decline`** (7 respondents, 9.5%): "his confidence is completely shot," "portfolios will reflect this difficult environment"

**In high-satisfaction responses (n=101), 100% report `not_present` for emotional_distress**—no dread, loss, frustration, or anxiety signals emerge.

The `emotional_distress_signals` column corroborates this pattern, showing identical distributions and reaffirming the robustness of the semantic signal.

---

### 4. Instruction Quality Problems are Prevalent in Low Satisfaction

**74.3% (55 of 74) low-satisfaction respondents report `instruction_quality` issues**, while 0% of high-satisfaction responses do:

- **`minimal_or_no_active_instruction`** (20 respondents, 27.0%): "just worksheets uploaded with no instruction," "just reading PDFs alone," "just essays and silent reading"
  - Concentrated in humanities: History (9), English (5), Science (4)
- **`teacher_unresponsive_to_student_needs`** (19 respondents, 25.7%): "teacher can't tell when she's lost," "teacher rarely responds to emails," "the teacher cannot redirect"
- **`teacher_overwhelmed_or_disorganized`** (11 respondents, 14.9%): "chaos," "cobbling together what I can," "parents step up but I miss hands-on guidance"
- **`slow_or_missing_feedback`** (5 respondents, 6.8%): "essays returned weeks late," "rarely returns essays with comments"

In contrast, high-satisfaction respondents universally report `not_present` for instruction problems. Example positives: "teacher posts solution walkthroughs," "detailed feedback on my journal entries," "records solution walkthroughs."

---

### 5. Subject-Modality Misfit is Significant in Low Satisfaction

**51.4% (38 of 74) low-satisfaction respondents report `subject_modality_fit` issues**, compared to only 11.9% (12 of 101) in high-satisfaction:

- **`hands_on_labs_or_experiments_lost`** (13 low-sat, 4 high-sat): "simulations only go so far," "cannot run experiments," "labs require supplies we don't have," "hands-on instruction needs proximity"
  - STEM subjects (Science 9, Math 4 in low-sat)
- **`studio_or_performance_art_impossible`** (9 low-sat, 2 high-sat): "fine motor instruction needs proximity," "art/theater/band cannot translate," "sculpture without a studio," "I haven't touched clay in months"
- **`manipulatives_cannot_translate`** (7 low-sat, 0 high-sat): "manipulatives don't translate," "first graders are guessing rather than understanding," "numbers move and I can't find my pencil"
- **`spatial_reasoning_without_physical_tools`** (5 low-sat, 0 high-sat): "geometry without physical manipulatives," "proofs require drawing alongside the teacher," "screen-share lag makes it impossible"
- **`synchronous_music_performance_not_viable`** (4 low-sat, 1 high-sat): "we can't sing together because of the lag," "ensemble work...none of that translates," "records instead of performs"

Notably, high-satisfaction STEM and arts respondents (with 12 reporting modality issues) still maintain satisfaction through complementary strengths: "AP Chemistry remote has gone better than I dared hope," "digital photography has been amazing," "virtual nature walks...engagement is higher."

**Cross-check with subject distribution:** Low-satisfaction respondents are overrepresented in Arts (32.4% of low-sat vs. 18.4% of full sample) and Math (24.3% vs. 21.2%), both subjects with high modality friction.

---

### 6. Cumulative Signal Load Predicts Low Satisfaction

Low-satisfaction responses show **high co-occurrence of TAPP facets** (mean 3.92 signals per respondent):
- 54% (40 of 74) report exactly 4 simultaneous signal types
- 22% (16 of 74) report all 5 signal types
- Remaining 24% report 2–3 signals
- **None report zero signals**

In contrast, high-satisfaction responses show sparse signals (mean 0.12):
- 88% (89 of 101) report zero TAPP problem signals
- 12% (12 of 101) report one signal (typically a subject-modality issue that is offset by other strengths)
- **None report 3+ signals**

**Interpretation:** Low satisfaction emerges from **layered barriers**—when collaboration loss combines with disengagement, emotional loss, instruction gaps, and modality friction, the cumulative effect depresses satisfaction. High satisfaction occurs when these barriers remain absent or minimal.

---

### 7. Role-Specific Patterns

**Students** in low-satisfaction (27 of 89, 30.3%) emphasize:
- Peer interaction loss (18 of 27; "I miss circle time," "working with my friend," "debating with friends")
- Disengagement (16 of 27; "just click through," "exhausting," "pointless")
- Loss of curiosity (13 of 27; "used to love," "misses the hands-on labs")

**Teachers** in low-satisfaction (24 of 81, 29.6%) emphasize:
- Inability to replicate peer dynamics (13 of 24; "performing to a wall," "participation is anemic")
- Instruction delivery strain (11 of 24; "overwhelming," "feel completely ineffective")
- Modality barriers (15 of 24; overrepresented in arts/STEM fields)

**Parents** in low-satisfaction (23 of 80, 28.8%) emphasize:
- Observed emotional impact on their child (20 of 23; "cries before," "confidence completely shot," "motivation gone")
- Peer/community loss (14 of 23; "zero peer interaction," "no ensemble," "silent novel discussions")
- Subject-specific struggles (10 of 23 in math/sciences; "doesn't understand why," "visual learner struggling")

---

## Synthesis: Open-Response Signals Predict Low Learning Satisfaction

The augmented semantic analysis identifies a **robust, multi-factor predictive profile** of low learning satisfaction:

1. **Primary barrier: Peer interaction collapse** (89.2% of low-sat). Loss of peer discussion, collaborative work, and classroom energy uniformly correlates with low satisfaction. This is the most prevalent single signal.

2. **Emotional cascade: Negative engagement + distress** (100% and 97.3% of low-sat respectively). Boredom, dread, and loss of curiosity/motivation nearly always accompany low satisfaction. Anxiety and confidence decline appear in severe cases.

3. **Instruction gaps**: 74.3% of low-satisfaction respondents cite instruction quality problems (minimal instruction, unresponsive/overwhelmed teachers, slow feedback). High-satisfaction responses report zero instruction problems.

4. **Subject-modality friction**: 51.4% of low-sat respondents cite discipline-specific barriers (lost labs, disappeared manipulatives, impossible performance/art). This amplifies across STEM and arts but can be mitigated by strong instruction and engagement.

5. **Cumulative load**: Low satisfaction is not a single-factor problem. The average low-satisfaction respondent reports nearly **4 simultaneous semantic barriers**, while high-satisfaction respondents report effectively zero.

**Pedagogical implication:** Addressing low satisfaction requires simultaneous intervention across multiple dimensions—restoring peer interaction opportunities, redesigning instruction for active engagement, managing teacher capacity, and adapting disciplinary content to available modalities. Single-factor fixes are unlikely to succeed.

---

## Limitations

- **Temporal**: Data snapshot from a specific remote-learning period; effects may vary with pedagogical adaptation or return to hybrid/in-person formats.
- **Selection**: Respondents self-selected into survey; non-respondents' experiences unknown.
- **Causality**: Augmented signals are correlational; open-response text reports lived experience but does not establish mechanism.
- **Coverage imbalance**: `subject_modality_fit` issues are captured only in 38 of 74 low-sat cases; the remaining 36 exhibit the satisfaction-depression pattern via other mechanisms (instruction, collaboration, engagement alone).

---

## Conclusion

Open-response signals encoded in six TAPP-generated semantic facets (`interaction_collaboration_loss`, `subject_modality_fit`, `instruction_quality`, `engagement_sentiment`, `emotional_distress`, `emotional_distress_signals`) demonstrate strong, near-deterministic prediction of low learning satisfaction. The signals cluster in specific combinations—most prominently peer loss + negative engagement + emotional distress—and are notably absent in high-satisfaction responses. This multi-signal profile offers a granular, interpretable basis for identifying at-risk learners and designing targeted interventions.
