---
name: skill-v11
description: TA++ schema augmentation v11. Extends v10 with concept-fidelity rules for faceted decomposition / focus inference (query-anchored concept, constitutive part-of test, parent-first selection, single-focus coherence) and deterministic facet-name de-duplication, while preserving v10's OCR/dense visual preview and raw-data-authoritative tagging/merge validation.
---

# TA++ v11 Skill

TA++ v11 is a text-to-table augmentation operator derived from v10. It materializes query-relevant typed columns from text evidence so downstream table analysis can group, compare, and audit semantic drivers.

V11 keeps every v10 capability (v9 query contract, intent-aware planning structures, analysis-yield gate, strict row-aligned tagging, merge validation, and the OCR/dense visual preview) and hardens the `concept_attribute` family: faceted decomposition must anchor on the concept named in the query and keep only constitutive facets, focus inference must propose a single coherent query-aligned focus, and a deterministic merge-stage de-duplication drops casing/naming-style duplicate columns. See README.md for the full v10 -> v11 change list.

```text
inspect/plan -> evidence selection -> visual preview -> query contract -> intent-aware schema decision -> review -> tag -> merge
```

## Visual Preview Rule

Visual previews are lossy context-compression artifacts. Use them for schema planning, category proposal, review context, and analysis preview. Do not use them as the authority for:

- row-level tagging
- exact counts
- joins
- numeric calculations
- merge gates
- strict row-index validation

Raw source table data and row-level text payloads remain the authority for those operations.

## Default Preview Policy

V10 defaults to a high-resolution OCR/dense canvas:

```json
{
  "resolution": {"width": 1600, "height": 2200},
  "density": "ocr",
  "overview_rows": 60,
  "rows_per_image": 60,
  "max_columns": 6
}
```

The goal is to maximize readable information per image, not merely lower resolution. The optimization target is `page_count * image_tokens_per_page` while preserving complete visible content.

## Boundary Rule

Experiment runners must not read TAPP prompts, choose categorization/tagging chunk sizes, render visual previews, normalize specs, retry tag chunks, fill row indices, or call `record-trace` directly. Those are skill responsibilities in v10.

Runners should only provide input table, workdir, query, executor model, optional maximum worker/concurrency budget, and output path/format.

## Workdir Artifacts

```text
<workdir>/
  execution_plan.json
  evidence_columns.json
  visual_preview/
    visual_preview_manifest.json
    overview_page_001.png
  specs.json
  tags/
  merge_report.json
  facet_report.json
  traces/
  artifact_manifest.json
```

## When To Use

Use v10 when a paper-aligned benchmark query needs query-contract-aware schema planning and the input table has enough text or width that visual preview can reduce prompt-body context. Use v9 or disable `visual_preview.enabled` when the host model cannot use images and text previews are already small.