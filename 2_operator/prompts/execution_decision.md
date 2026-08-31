# TA++ v10 Execution Decision

Use this prompt before running categorization/tagging when the host model is executing the skill natively.

You are responsible for the physical execution decision. Do not delegate chunk-size or concurrency choices to the experiment runner.

Inputs to consider:

- `execution_plan.json#chunking.items.size`
- `execution_plan.json#categorization`
- `execution_plan.json#operators.tagging`
- row count
- selected evidence columns and their combined row width
- `execution_plan.json#visual_preview` and any existing `visual_preview_manifest.json`
- executor model family and current run pressure
- user preference for speed, cost, or quality

Decision fields to produce:

```json
{
  "categorize_chunk_size": 250,
  "tag_chunk_size": 200,
  "workers": 3,
  "reasoning": "short rationale grounded in row count, text width, model family, and observed risk"
}
```

Guidelines:

- Start from the planner envelope, then shrink only when needed for prompt stability.
- Use map-reduce categorization when row count or text width makes single-pass schema induction unstable.
- For Gemini and Haiku, prefer categorization around 250 rows and tagging around 100-200 rows.
- For GPT and Sonnet, 400 rows is usually acceptable; reduce to 250 or 200 for wide text.
- Avoid 500-row categorization chunks on wide tables; prior laptop runs showed oversized prompts and JSON failures.
- If a categorization proposal chunk fails after strict JSON retries, keep recovery inside the skill by splitting that proposal into smaller subchunks before global consolidation.
- Increase workers only when the executor/model backend is stable and the machine/API budget can handle it.
- Lower workers when other long jobs are running or when model calls are timing out/filtering.
- Record the final decision in the workdir, either by passing the values to `augment-e2e` or by writing an execution decision artifact.
- Do not use visual preview to relax tagging or merge strictness. Preview only affects schema/analysis context.

## Worker budget covers the category stage and tagging

`workers` is a single concurrency budget that the host applies to BOTH major stages:

- **Category stage** (schema induction): the host fans out `chunk_proposal` calls in parallel, and when there are many proposals it also runs the hierarchical `global_consolidation` batches at the same level **in parallel** (one worker per batch, capped at `min(workers, num_batches)`).
- **Tagging stage**: the host fans out the per-chunk tagging calls in parallel.

These two stages run sequentially relative to each other (categorize fully completes before tagging starts), so the SAME `workers` value is reused at full strength by each stage — picking a larger budget speeds up both the category stage and tagging without doubling peak load. Treat `workers` as the unified "category + tagging" parallelism knob: choose it so a single stage's fan-out (proposals/consolidation batches, or tag chunks) keeps the machine/API busy but not overloaded. For large tables the category stage benefits the most, because consolidation now parallelizes across batches instead of one giant single-pass merge.

Note on the harness budget floor: when the benchmark harness supplies `--max-workers` (the worker budget), the executor enforces that budget as the actual map-stage concurrency. A lower host-chosen `--workers` will NOT reduce parallelism below the budget — the map calls are order-independent and idempotent, so there is no quality reason to serialize them. Do not pass a small `--workers` (e.g. 1) expecting safety; it only wastes wall-clock. Use `--workers` only to request concurrency up to the budget, and lower the budget itself at the harness level if the backend is unstable.

If using the automated v10 executor, pass the decision as skill-level parameters:

```bash
python scripts/run_tapp.py augment-e2e \
  --input <input> \
  --workdir <workdir> \
  --query "..." \
  --model <executor_model> \
  --max-workers <budget> \
  --workers <optional_explicit_workers> \
  --categorize-chunk-size <categorize_chunk_size> \
  --tag-chunk-size <tag_chunk_size> \
  --execution-decision-note "<reasoning>"
```

The experiment runner should not invent these values. They belong to the host model applying this skill.

