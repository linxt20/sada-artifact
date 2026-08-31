---
dataset: healthcare_visit_notes
scenario: predictive_long
variant: skill_off
model: substrate-claude-sonnet-4-6
prompt_style: neutral
query_subtype: predictive_feature_engineering
focus_variable: "visit_duration_min"
query: "What visit-note signals suggest a longer visit?"
source_table: augment_table/healthcare_visit_notes/predictive_long/sonnet__skill_off_update.csv
generated_at: 2026-07-28T12:43:39.842997+00:00
wall_seconds: 38.62
---

# Visit-Note Signals for Longer Visits
**Dataset:** `sonnet__skill_off_update.csv` | 250 visits | Variant: `skill_off`

---

## Focus Variable
`visit_duration_min` — ranges 15–60 min, median = **25 min**, mean ≈ 25.4 min. "Longer visit" is operationalized as above-median (> 25 min).

---

## Key Signals (Strongest to Weakest)

### 1. Department — Strongest Discriminator
| Department | Mean Duration (min) |
|---|---|
| Emergency | **45.5** |
| Cardiology | **30.1** |
| Orthopedics | 25.9 |
| General Practice | 21.9 |
| Pediatrics | 19.9 |
| Dermatology | **17.0** |

Emergency and Cardiology departments are the clearest structural predictors. All 17 visits ≥ 45 min are in Emergency.

### 2. Urgency Level
| Urgency | Mean Duration (min) |
|---|---|
| Emergency | **45.5** |
| Urgent | 23.2 |
| Routine | 22.6 |

Emergency-flagged urgency drives duration far above other levels. Notably, "Urgent" and "Routine" are nearly identical, so urgency only meaningfully separates the Emergency tier.

### 3. Comorbidity Count (r = +0.19)
| Comorbidity Count | Mean Duration (min) |
|---|---|
| 2 | **32.2** |
| 1 | 25.8 |
| 0 | 24.2 |

The highest positive numeric correlation. Visits documenting 2 comorbidities average ~8 min longer than those with none, consistent with more complex management requiring additional discussion and documentation.

### 4. Sentence Count (r = +0.14)
Visits with more sentences in the note tend to run longer. Short visits (≤ 15 min) cluster tightly around 4 sentences; longer visits show greater spread (up to 7+). This is a **moderate** signal.

### 5. Age Group
| Age Group | Mean Duration (min) |
|---|---|
| 60+ | **29.5** |
| 40–59 | 25.3 |
| 18–39 | 23.5 |
| 0–17 | **19.9** |

Older patients (60+) have noticeably longer visits, likely driven by comorbidities and Cardiology follow-ups. Pediatric visits are the shortest.

### 6. Multi-Complaint Flag (r = +0.05)
Visits with multiple complaints average ~1.7 min longer (26.9 vs. 25.2 min). The effect is **weak** and not a reliable standalone predictor.

---

## Weak or Counterintuitive Signals

- **`note_length_chars` (r = −0.11)** and **`medical_term_count` (r = −0.09)** are negatively correlated with duration. Emergency notes are long in duration but relatively concise in character count (fast-paced documentation style), while shorter specialty visits (e.g., Dermatology) may use dense technical terminology. These signals should **not** be used as positive indicators of duration.
- **`action_count` (r ≈ −0.01)**: Essentially no linear relationship with duration.

---

## Summary

The strongest predictors of a longer visit are **department (Emergency, Cardiology)** and **urgency (Emergency)** — both categorical and likely confounded with each other. Among note-intrinsic signals, **comorbidity count** and **sentence count** provide modest but genuine lift. Multi-complaint flag, note length in characters, and medical term count are weak or misleading signals in this dataset.

| Signal | Direction | Strength |
|---|---|---|
| Department = Emergency/Cardiology | ↑ | Strong |
| Urgency = Emergency | ↑ | Strong |
| Comorbidity count (2) | ↑ | Moderate |
| Sentence count | ↑ | Moderate |
| Age group = 60+ | ↑ | Moderate |
| Multi-complaint flag | ↑ | Weak |
| Note length (chars) | ↓ (counterintuitive) | Weak/misleading |
