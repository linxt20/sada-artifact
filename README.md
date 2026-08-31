# SADA Experiment Artifact

Code, raw per-item outputs, prompts and regenerated tables for Experiments 1–5 of
the paper.

## Start here

```bash
./1_verify/verify_all.sh
```

No model calls, no network, Python standard library only. It re-aggregates the
archived per-item outputs and checks the result against every paper-facing value.
Expected output: `Reproduction status: PASS` over **235 values**.

Then read `index.md` — the claim-by-claim map from each number in the paper to
the code, prompt, raw output and table behind it.

## Layout

The top level is ordered by reading path.

```text
sada-artifact/
├── README.md                 you are here
├── index.md                  paper number -> artifact map
│
├── 1_verify/                 one command, and its report
│   ├── verify_all.sh
│   ├── reproduce_paper_results.py
│   └── report/               REPRODUCTION_REPORT.md, verification.json
│
├── 2_operator/               the SADA operator: the paper's contribution
│   ├── SKILL.md              the operator contract
│   ├── prompts/              the 7 stage prompts
│   ├── scripts/              run_tapp.py, host_executor.py, ...
│   └── config/
│
├── 3_experiments/            one self-contained directory per experiment
│   ├── exp1_end_to_end_utility/     Table 2
│   ├── exp2_analysis_form/          Table 3
│   ├── exp3_schema_suitability/     Table 4(a), 4(b), Appendix Table 1
│   ├── exp4_scale_and_grounding/    Section 5.5
│   └── exp5_predictive_features/    Tables 5-6
│       └── each holding: README.md, prompts/, raw/, tables/
│
├── 4_code/                   all runnable generation and scoring code
│   ├── benchmark/            Experiments 1-4
│   ├── TextTabBench/         Experiment 5
│   ├── run_method.sh         SADA-side regeneration (needs models + data)
│   └── run_baselines.sh      baseline regeneration (needs models + data)
│
├── 5_reference/
│   ├── configs/              scope, the 108 analysis queries, upstream provenance
│   ├── data/                 what inputs are needed and where to get them
│   └── paper/                a copy of the paper's experiment section
│
├── requirements.txt          suggested dependencies
├── requirements-observed.txt observed environment snapshot
├── THIRD_PARTY.md
├── LICENSE                   MIT, for the source code
└── LICENSE-DATA              CC BY 4.0, for the archived outputs
```

`2_operator/` sits at the top level rather than inside `4_code/` because it is the
paper's contribution, not experiment plumbing. `4_code/` itself
stays a single tree because several modules are shared across experiments and the
archived scripts resolve them as siblings; splitting it per experiment would mean
rewriting import paths in code that is otherwise preserved as-run.

## What is verified

| Experiment | Paper location | Values |
|---|---|---:|
| Exp. 1 | Table 2 | 8 |
| Exp. 2 | Table 3 | 24 |
| Exp. 3 | Table 4(a) | 36 |
| Exp. 3 signals | Table 4(b) + Appendix Table 1 | 39 |
| Exp. 4 | §5.5 prose | 18 |
| Exp. 5 | Tables 5–6 | 110 |
| | **Total** | **235** |

The illustrative Yelp comparison of Figure 3 (§4.2) is not part of this
repository. It was produced with a later revision of the operator than
Experiments 1–5 and supports no quantitative claim in the paper; every number the
paper reports rests on the experiments above.

## Reproduction scope

- Experiments 1–3 exclude `airlines_review_full`, which was added to the pool
  later.
- Experiment 3 keeps the true unequal sample counts, for example Haiku
  `what_if` at `17/16/16`.
- Experiment 4 aggregates the two units common to all conditions; see
  `3_experiments/exp4_scale_and_grounding/README.md`.
- Experiment 5 excludes `mercari`; Table 6 uses the SHAP top-k=64 results.

All of it is recorded in `5_reference/configs/experiment_scope.json`.

## The operator version

Every SADA result in Experiments 1–5 came from `2_operator/`. Its
`scripts/run_tapp.py` sets `SKILL_VERSION = "skill_v10"`, and every archived run
records `"skill_version": "skill_v10"` — that match is how a reviewer can confirm
the results came from exactly this directory and not a later revision. The
constant was simply not bumped when the v11 concept-fidelity rules landed. See
`index.md` §4.

## Running from scratch

`4_code/run_method.sh` and `4_code/run_baselines.sh` are the entry points for the
model-dependent tasks. A full re-run needs the source data and the complete
upstream repository layout, Claude CLI/API access, the corresponding Python
environment, and `UPSTREAM_ROOT` pointing at the complete repository:

```bash
UPSTREAM_ROOT=/path/to/full/repository ./4_code/run_method.sh exp3_augmentation
```

Some archived scripts still contain original absolute paths. They are preserved
as-run; where an artifact-local fallback was added it is commented in place, and
the offline verification path depends on none of them. See `index.md` §7.

`requirements.txt` gives the suggested dependencies.
`requirements-observed.txt` records the core package versions actually importable
in the retained TextTabBench virtual environment on 2026-08-31 — an environment
snapshot, not a proven lockfile for the original runs.
