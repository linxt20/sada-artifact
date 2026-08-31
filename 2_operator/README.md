# tapp skill v11

TA++ v11 is derived from skill v10. It keeps every v10 capability (query-contract-aware schema planning, analysis-yield gate, strict row-aligned tagging, merge validation, and the OCR/dense `visual_preview` artifact) and adds concept-attribute fidelity rules plus deterministic facet de-duplication.

The v11 preview path is unchanged from v10: it renders fixed-resolution OCR/dense table images, defaulting to `1600x2200` with high information density. The preview is a context-compression artifact for schema planning and analysis reading; raw table/text remains authoritative for row-level tagging, exact counts, numeric calculations, joins, and merge gates.

## Changes vs skill-v10

v11 targets a specific weakness observed in the 4-way benchmark: on `focus_internal_structure` (faceted / concept-attribute) scenarios, v10's `skill_on` / `skill_on_e2e` outputs drifted to a generic domain template (e.g. decomposing an incident into `failure_mode` / `technical_locus` / `component_layer` for a query about *agent workload*) and emitted casing-duplicate columns (e.g. `failure_pattern` + `FailurePattern`), which lowered `facet_fraction` and triggered the redundancy penalty. The following changes address that. (The proposed "expressive-slot restriction" change was intentionally NOT applied, so `predictive` / `causal` planning keeps v10's expressive schema behavior.)

Prompt changes — `prompts/categorization.md`:

1. **Concept anchoring (Intent family 3 + Facet rule 15).** For faceted decomposition the planner must extract the focus concept as a literal noun phrase from the query, write it verbatim into `PlanningStructure.Root.Label`, and never substitute a generic domain template.
2. **Constitutive part-of test (Facet rule 15).** Every candidate facet must pass "Is this a constitutive part/dimension of the focus concept itself?"; facets that only describe the record generically are rejected.
3. **Parent-first + new-dimension admission (Facet rule 16).** Prefer the most stable parent facet per dimension; add a child only when it opens a distinct sub-dimension; every column must open a new, uncovered dimension of the concept.
4. **Focus-inference alignment + single-focus coherence (Intent family 3 + Facet rule 17).** The proposed focus must be table-derivable, match the query intent, and be a single coherent concept; all columns must relate to that one focus.
5. **Naming-style discipline (Facet rule 19).** Emit every facet name in one consistent `snake_case` convention; never emit two columns differing only by casing/naming style or exact synonyms.

Prompt changes — `prompts/categorization_large_scale.md` (map_reduce path):

6. Same concept-anchoring and single-focus rules applied to intent family 3, plus merge requirements 10-11: normalize final facet names to one `snake_case` convention, merge casing/synonym/`ConceptKey` duplicates into one column (recording dropped variants in `DroppedFacets`), and keep only constitutive facets for faceted decomposition.

Code changes — `scripts/run_tapp.py`:

7. **Deterministic facet de-duplication at merge.** New `_canonical_facet_key()` normalizes names across camelCase/PascalCase/snake_case boundaries; `cmd_merge` now drops any facet whose canonical key collides with one already kept (first occurrence wins), recording the drop in `merge_report.dropped` and `facet_report` with reason `duplicate_facet_name`. This is a safety net independent of model behavior and directly removes redundancy-inducing duplicate columns.

Not changed from v10: visual preview, tagging, coverage gates, closed-vocab enforcement, and all `predictive` / `causal` planning behavior.

## Core Additions

- `execution_plan.json#visual_preview` records preview policy.
- `augment-e2e` generates `<workdir>/visual_preview/visual_preview_manifest.json` and PNG pages after evidence-column selection.
- Preview artifacts are registered in `artifact_manifest.json` as `visual_preview` and `visual_preview_page`.
- Categorization task contracts include visual-preview metadata when generated.
- `prompts/categorization*.md` explicitly treat visual previews as lossy planning context, not strict tagging input.

## Commands

```bash
python scripts/run_tapp.py inspect <input_path> --host-model <executor_model>
python scripts/run_tapp.py plan --input <input_path> --workdir <workdir> --estimated-labels 30 --estimated-facets 3 --host-model <executor_model>
python scripts/run_tapp.py augment-e2e --input <input_path> --workdir <workdir> --query "..." --model <executor_model> --max-workers <budget> --attempts 2 --output <workdir>/augment.xlsx --allow-low-coverage-fallback
python scripts/run_tapp.py merge --input <input_path> --workdir <workdir> --output <workdir>/augment.xlsx
```

## Workdir Layout

```text
<workdir>/
  execution_plan.json
  evidence_columns.json
  visual_preview/
    visual_preview_manifest.json
    overview_page_001.png
  categorization/
  specs.json
  tags/
  traces/
  artifact_manifest.json
  merge_report.json
  facet_report.json
  augment.xlsx
```

## Boundary Rule

Experiment runners should still treat the skill as the owner of prompt templates, chunking, categorization execution, review/spec normalization, tagging retries, trace recording, and merge validation.

Runners provide only the input table, workdir, query, executor model, optional worker budget, and output path. Do not implement visual-preview rendering in benchmark runners; adjust `config/model_recipe.json#visual_preview` or the skill renderer instead.