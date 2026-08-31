# Experiments

One directory per experiment. Each is self-contained in the same four parts:

```text
expN_.../
├── README.md    the paper claim, and how each number here maps to it
├── prompts/     every LLM-facing prompt, rendered from the code
├── raw/         the per-item outputs the numbers are aggregated from
└── tables/      the regenerated tables, with a PASS status per value
```

The runnable generation and scoring code lives in `../4_code/` rather than inside
each experiment, because several modules are shared across experiments (the
Claude-CLI and table-IO helpers, the judge base, the rubric definitions) and the
archived scripts resolve them as siblings. Each README links the exact files.

| Directory | Paper | Verified values |
|---|---|---:|
| `exp1_end_to_end_utility/` | Table 2 | 8 |
| `exp2_analysis_form/` | Table 3 | 24 |
| `exp3_schema_suitability/` | Table 4(a), Table 4(b), Appendix Table 1 | 75 |
| `exp4_scale_and_grounding/` | §5.5 prose | 18 |
| `exp5_predictive_features/` | Tables 5–6 | 110 |
| | **Total** | **235** |

Table 1 of the paper is the FOI intent taxonomy — conceptual, with no artifact of
its own. The illustrative Figure 3 of §4.2 is not part of this repository.

Experiments 1 and 2 share a corpus: Experiment 2 classifies the reports
Experiment 1 generated, so `exp2_analysis_form/` has no `analysis_reports/` of
its own and points at Experiment 1's.

## Prompts are generated, not transcribed

`_extract_prompts.py` renders every prompt file by importing the module that owns
it and reading its constant or calling its builder with placeholder arguments.
This means the files cannot silently drift from the code:

```bash
python3 _extract_prompts.py --check    # verify; writes nothing
python3 _extract_prompts.py            # regenerate
```

Standard library only, no model calls.
