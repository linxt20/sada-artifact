# scorer_update — characteristic-adherence evaluation

Updated grader produced after the **2026-06-25 advisor sync**. It replaces the
"how many ground-truth columns did we recover" view (recall) with the question
the advisor actually asked:

> 对增广表格的评测,要按 category 看它是否满足该类的 *characteristic*。
> 因果的就问:**treatment 有吗?confounder 有吗?** —— 用大模型做 judge。

## What changed vs `../scorer`

| | `../scorer` (old) | `scorer_update` (new) |
|---|---|---|
| Question | Recall of GT reference columns + cell accuracy | Does the augmentation satisfy its **intent category's characteristic**? |
| Judge target | generated cols vs hidden GT schema | generated cols vs the *characteristic* (Table 1 col 3) |
| Causal metric | recall of GT confounder cols | **treatment present? confounder present? #confounders, confounder quality** |
| Focus relation | recall | predictor fraction / adherence (are added cols correlated predictors) |
| Faceted | recall | facet fraction + MECE |
| Key comparison | skill_on vs GT | **skill_off vs skill_on vs skill_on_e2e** per category |

The new view directly supports the paper's distinctive claim (causal intents
surface confounders the user did not name) and gives a per-category,
per-variant table instead of a single recall number.

## Files

- `characteristic_adherence.py` — core evaluator. Detects the FOI category
  (`focus_relation` / `causal_relation` / `focus_internal_structure`) from
  `specs.json` (`planning_structure.StructureType` → `intent_class` → scenario
  keyword), builds a **category-specific** LLM-judge prompt over the *added*
  columns only, and returns adherence metrics. Reuses the low-level helpers of
  `../scorer/semantic_reference_recall.py` (table IO, `claude -p` invocation,
  spec parsing) so behaviour stays consistent.
- `run_characteristic_adherence.py` — driver over `dataset_portion_1/2` ×
  `{haiku, sonnet}` × `{skill_off, skill_on, skill_on_e2e}`. Writes per-scenario
  JSON and an aggregated `characteristic_result/SUMMARY.{json,md}`.

## Run

```bash
# whole sweep (LLM judge = opus by default)
python run_characteristic_adherence.py --judge-model claude-opus-4-5

# quick smoke test without calling the LLM (adherence forced to 0)
python run_characteristic_adherence.py --no-llm-judge --limit 2

# one table, standalone
python characteristic_adherence.py --augment <augment.csv> --specs <specs.json> \
    --query "How can we improve incident resolution efficiency?" --out report.json
```

## Output (per category, per variant)

- **causal_relation**: adherence, treatment-present rate, **confounder-present
  rate**, mean #confounders, confounder quality.
- **focus_relation**: adherence, predictor fraction.
- **focus_internal_structure**: adherence, facet fraction, MECE.

Expected pattern (the story for the paper): `skill_off` ≈ 0 adherence (mechanical
columns realise no characteristic), `skill_on` / `skill_on_e2e` high — and for
causal scenarios the confounder-present rate jumps from near-0 to high.

## Not removed

`../scorer/semantic_reference_recall.py` is left untouched; this folder is the
*characteristic* view that the advisor asked to lead with. Recall can still be
reported as a secondary signal if needed.
