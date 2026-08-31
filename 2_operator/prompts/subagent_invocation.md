# TA++ v10 — Subagent Invocation Contract

This document is the TA++ isolation protocol. Each LLM-driven stage
(`categorize_proposal`, `categorize_consolidation`, `categorize_final_selection`,
`review`, `tag`, `tag_consolidation`) MUST run in an isolated subagent, not in the
host's main scratchpad. The host orchestrator is responsible for enforcing this
contract and for recording the result in the workdir's `artifact_manifest.json`
and `traces/` directory so the entire run is reproducible from disk alone.

## 1. Why isolation

- **Token budget**: TA++ stages can each emit and consume thousands of tokens. Mixing
  them into the host's transcript inflates context and degrades downstream quality.
- **Reasoning hygiene**: subagent reasoning must be inspected, not silently inherited.
  The host should only see the structured output (typed JSON) plus, optionally, a
  short author-provided `reasoning_summary`.
- **Reproducibility**: every stage must be re-runnable from the same input artifacts
  to the same output artifacts (modulo LLM nondeterminism). That requires inputs to
  be addressable by content hash, not by transient memory.

## 2. Required isolation properties

When the host invokes a subagent for a TA++ stage, the invocation MUST satisfy all of
the following:

| Property | Requirement |
|---|---|
| Process isolation | The subagent runs in a separate context window. No host CoT is inherited. |
| Input addressability | Every input is referenced by a placeholder of the form `<<artifact:<kind>@sha256:<short>>>` registered in `artifact_manifest.json`. Raw inline payloads larger than 1 KB MUST be artifact-backed first. |
| Output addressability | Every structured output is written to `<workdir>/...`, then registered with `python scripts/run_tapp.py record-artifact ...`. The host receives only the placeholder string. |
| Reasoning persistence | The host MUST persist a trace via `python scripts/run_tapp.py record-trace ...` after each stage. The trace records `stage`, `status`, `model`, `input_refs`, `output_refs`, optional `reasoning_summary`, and timing. |
| Tool authority | The subagent has read-only access to declared input artifacts plus its prompt template. It MUST NOT browse the rest of the workdir or the network. |
| Determinism budget | If the same `(prompt template hash, input artifact hashes, model, sampling settings)` recurs, the host SHOULD reuse the prior `output_refs` and emit a `status: "cached"` trace instead of re-invoking. |

If the host runtime cannot enforce process isolation, the host MUST refuse the run
and report `STATUS: ERROR isolation_unsupported`. The skill will not silently degrade to
in-context execution.

## 3. Stage invocation template

Use this template to drive each stage:

```text
SYSTEM
You are a TA++ v10 subagent. Read only the inputs listed under INPUTS below.
Do not refer to any prior conversation or hidden context. Emit your output in
exactly the structure described under OUTPUT_SCHEMA. After the structured
output, add at most 2 sentences of `reasoning_summary` for audit.

INPUTS
- <<artifact:execution_plan@sha256:...>>
- <<artifact:specs@sha256:...>>            # if applicable
- <<artifact:tags/<FacetName>_chunk_<n>@sha256:...>>  # if applicable

OUTPUT_SCHEMA
<paste the relevant prompt schema from prompts/categorization.md, prompts/tagging.md, etc.>

OUTPUT_TARGET
<workdir>/<output relative path, e.g., tags/<FacetName>_chunk_<n>.json>
```

The host substitutes each placeholder with the actual content read via
`python scripts/run_tapp.py resolve --workdir <wd> --ref "<<artifact:...>>" --read`
right before dispatching the subagent. The placeholder string itself is what the
host stores in its own transcript.

## 4. Required host-side checklist (per stage)

```bash
# 1. Resolve every input artifact
for ref in $INPUT_REFS; do
  python scripts/run_tapp.py resolve --workdir "$WD" --ref "$ref" --read >/dev/null
done

# 2. Invoke subagent with the resolved inputs (host-runtime specific)
host_invoke_subagent --prompt "$PROMPT" --inputs "$RESOLVED_INPUTS" --output-target "$OUT_PATH"

# 3. Register the structured output
python scripts/run_tapp.py record-artifact \
  --workdir "$WD" \
  --kind "$STAGE_KIND" \
  --path "$OUT_PATH" \
  --stage "$STAGE_NAME"

# 4. Persist the trace
python scripts/run_tapp.py record-trace \
  --workdir "$WD" \
  --stage "$STAGE_NAME" \
  --status ok \
  --model "$EXECUTOR_MODEL" \
  --plan-id "$PLAN_ID" \
  $(printf -- '--input-ref %s ' $INPUT_REFS) \
  --output-ref "<<artifact:$STAGE_KIND@sha256:...>>" \
  --latency-ms "$LATENCY_MS" \
  --input-tokens "$IN_TOKENS" \
  --output-tokens "$OUT_TOKENS" \
  --reasoning-summary "$SUMMARY"
```

The four steps MUST appear in this order. Step 4 (`record-trace`) is mandatory even
when the stage failed; pass `--status failed` and `--reasoning-summary` containing
the failure reason. Failed traces are what makes ablation runs replayable.

## 5. Auditing a finished workdir

After a full run, the workdir is self-describing:

```text
<workdir>/
  execution_plan.json           # Pillar 3 physical plan
  specs.json                    # Reviewed facet specs
  tags/
    <Facet>.json | <Facet>_chunk_*.json
  augmented.parquet             # strict-validated output
  merge_report.json             # merge audit
  facet_report.json             # per-facet merge status
  oos_report.json               # OOS abstention metrics
  artifact_manifest.json        # Pillar 4.B content-addressed registry
  traces/
    <stage>_<timestamp>_<hash>.json   # Pillar 4.C per-stage traces
```

To replay a run end-to-end:

1. Read `artifact_manifest.json` and re-fetch every artifact by sha256 to verify the
   manifest is internally consistent.
2. Walk `traces/` in chronological order. For each trace, the listed `input_refs`
   MUST resolve to artifacts present in the manifest before the trace's
   `finished_at`. If any input is missing or its sha256 does not match, the run is
   not replayable and the audit MUST flag it.
3. For each stage, optionally re-invoke the subagent with the same inputs and
   compare the new output's sha256 against the one recorded. Drift is acceptable
   for LLM stages; mismatch on Python stages (`plan`, `merge`, `oos_report`) is a
   correctness bug.

This audit procedure is what closes the loop on Pillar 4.A: subagent isolation is
not an unverifiable claim, it is observable from disk after the fact.

