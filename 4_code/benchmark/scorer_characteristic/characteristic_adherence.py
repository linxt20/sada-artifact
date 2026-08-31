"""Per-category *characteristic adherence* evaluation for augmented tables.

Why this file exists (advisor sync, 2026-06-25)
-----------------------------------------------
The earlier ``scorer/semantic_reference_recall.py`` scores how many ground-truth
*reference* columns a generated augmentation table recovers. That recall view is
**not** the distinctive question for Focus-Oriented Intent (FOI). What actually
matters is whether the augmentation *adheres to the characteristic of its intent
category* --- the third column ("Characteristics") of Table 1 in the paper:

    * focus_relation (correlational) : the added columns are semantically
      CORRELATED predictors of the focus (associational, outside the focus).
    * causal_relation               : the added columns carry a TREATMENT
      together with the CONFOUNDERS the effect estimate needs --- in particular
      the confounders the user did not name. (This is the paper's headline
      claim, and the advisor's "Consultant 有吗?" question.)
    * focus_internal_structure      : the added columns are constitutive FACETS
      (parts / meronymy) of the focus concept, ideally MECE.

So this evaluator asks an LLM judge a *category-specific* question over the
generated columns only (the GT schema is NOT shown to the judge), and reports
adherence metrics per category instead of recall. It reuses the low-level
helpers of ``scorer/semantic_reference_recall.py`` (table IO, claude
invocation, spec parsing) so behaviour stays consistent with the existing
pipeline.

Standalone use::

    python characteristic_adherence.py --augment path/to/augment.csv \
        --specs path/to/specs.json --query "..." --category causal_relation \
        --out report.json

but it is normally driven by ``run_characteristic_adherence.py``.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

# Reuse the existing low-level helpers rather than duplicating them.
SCRIPT_DIR = Path(__file__).resolve().parent
SCORER_DIR = SCRIPT_DIR.parent / "scorer"
sys.path.insert(0, str(SCORER_DIR))

import semantic_reference_recall as semrec  # noqa: E402


# --------------------------------------------------------------------------- #
# Category detection
# --------------------------------------------------------------------------- #
CATEGORY_BY_STRUCTURE = {
    "causal_graph": "causal_relation",
    "prediction_tree": "focus_relation",
    "flat_feature_set": "focus_relation",
    "concept_tree": "focus_internal_structure",
}

CATEGORY_LABEL = {
    "focus_relation": "Focus relation (correlational X)",
    "causal_relation": "Causal relation (treatment + confounders)",
    "focus_internal_structure": "Focus internal structure (constitutive facets of Y)",
}


def detect_category(scenario: str, specs: dict[str, Any] | None) -> str:
    """Map a scenario to one of the three FOI categories.

    Preference order: planning_structure.StructureType -> intent_class ->
    keyword fallback on the scenario name (covers ``skill_off`` which has no
    specs.json of its own).
    """
    specs = specs or {}
    structure = ((specs.get("planning_structure") or {}).get("StructureType") or "").strip()
    if structure in CATEGORY_BY_STRUCTURE:
        return CATEGORY_BY_STRUCTURE[structure]
    intent_class = str(specs.get("intent_class") or "").lower()
    if intent_class == "causal":
        return "causal_relation"
    if intent_class in {"concept", "concept_attribute", "faceted"}:
        return "focus_internal_structure"
    name = scenario.lower()
    if any(tag in name for tag in ("causal", "whatif", "what_if", "attribution", "improve", "reduce")):
        return "causal_relation"
    if any(tag in name for tag in ("concept", "facet", "attribute", "focus_inference", "key_focus")):
        return "focus_internal_structure"
    # predictive / eda / prediction default to the correlational family.
    return "focus_relation"


def _focus_from_specs(specs: dict[str, Any] | None) -> str | None:
    if not specs:
        return None
    root = (specs.get("planning_structure") or {}).get("Root")
    return str(root) if root else None


# --------------------------------------------------------------------------- #
# Judge prompt (category-specific)
# --------------------------------------------------------------------------- #
def _columns_payload(
    new_columns: list[str],
    specs_by_name: dict[str, dict[str, Any]],
    table: pd.DataFrame,
) -> list[dict[str, Any]]:
    payload = []
    for name in new_columns:
        spec = specs_by_name.get(name, {})
        values = table[name].tolist() if name in table.columns else []
        payload.append(
            {
                "name": name,
                "description": semrec._description_from_spec(spec),
                "domain": semrec._domain_from_spec(spec)[:40],
                "observed_top_values": semrec._value_counts(values, limit=20),
            }
        )
    return payload


_RUBRIC = {
    "focus_relation": (
        "Characteristic: every added column should be a variable that lies OUTSIDE the focus and "
        "plausibly CORRELATES with it (an associational predictor / feature). It should not merely "
        "restate the focus, and it need not be a cause.\n"
        "Return JSON: {\n"
        '  "category": "focus_relation",\n'
        '  "per_column": [{"name": "...", "is_correlated_predictor": true, "restates_focus": false, "rationale": "..."}],\n'
        '  "n_predictors": 0, "predictor_fraction": 0.0,\n'
        '  "adherence": 0.0,  // overall: are the columns a coherent set of correlated predictors of the focus\n'
        '  "rationale": "..."\n'
        "}"
    ),
    "causal_relation": (
        "Characteristic: the added columns should occupy CAUSAL roles around the focus (the outcome): "
        "a TREATMENT whose effect is studied, and CONFOUNDERS --- variables that plausibly cause BOTH the "
        "treatment and the outcome and therefore must be adjusted for. The distinctive test is whether "
        "confounders (often not named in the query) are surfaced from the text.\n"
        "Return JSON: {\n"
        '  "category": "causal_relation",\n'
        '  "per_column": [{"name": "...", "causal_role": "treatment|confounder|mediator|outcome|other", "is_plausible_confounder": false, "rationale": "..."}],\n'
        '  "treatment_present": false, "treatment_columns": [],\n'
        '  "confounder_present": false, "confounder_columns": [], "n_confounders": 0,\n'
        '  "confounder_quality": 0.0,  // are the confounders plausible common causes of treatment AND outcome (0-1)\n'
        '  "adherence": 0.0,  // overall: has a treatment AND at least one plausible confounder\n'
        '  "rationale": "..."\n'
        "}"
    ),
    "focus_internal_structure": (
        "Characteristic: the added columns should be constitutive FACETS / PARTS of the focus concept "
        "(meronymy --- a part-of relationship), not external predictors or causes of it.\n"
        "Judge each column independently. Also estimate how completely the facet columns COVER the main "
        "constitutive aspects of the concept named by the query/focus (coverage), independent of how many "
        "columns there are.\n"
        "Return JSON: {\n"
        '  "category": "focus_internal_structure",\n'
        '  "per_column": [{"name": "...", "is_constitutive_facet": true, "is_external_predictor": false, "rationale": "..."}],\n'
        '  "facet_columns": [], "non_facet_columns": [],\n'
        '  "coverage": 0.0,  // 0-1: how completely the facet columns cover the concept\'s main aspects\n'
        '  "rationale": "..."\n'
        "}"
    ),
}


def build_prompt(
    *,
    category: str,
    query: str,
    focus: str | None,
    source_columns: list[str],
    columns_payload: list[dict[str, Any]],
) -> str:
    task = {
        "category": category,
        "category_label": CATEGORY_LABEL[category],
        "query": query,
        "focus_variable": focus,
        "original_columns": source_columns,
        "added_columns": columns_payload,
    }
    return (
        "You are a strict evaluator of a text-to-table augmentation operator.\n"
        "An augmentation took an analytical query with a focus variable and ADDED the columns below to "
        "the table. Judge ONLY whether the ADDED columns satisfy the characteristic required by the "
        "intent category. Do not reward or penalise based on column names, casing, or a hidden reference "
        "schema --- judge the SEMANTICS of each added column against the characteristic.\n\n"
        f"{_RUBRIC[category]}\n\n"
        "Scoring guidance: 'adherence' is the headline 0-1 score for this category. Be conservative: a "
        "mechanical or generic set of columns (e.g. text length, token counts, sentiment-only) that does "
        "not realise the characteristic should score near 0.\n\n"
        "Return strict JSON only.\n\n"
        f"Evaluation input JSON:\n{json.dumps(task, ensure_ascii=False, indent=2)}"
    )


# --------------------------------------------------------------------------- #
# Core evaluation
# --------------------------------------------------------------------------- #
def evaluate(
    *,
    augment_table: pd.DataFrame,
    new_columns: list[str],
    specs_by_name: dict[str, dict[str, Any]],
    category: str,
    query: str,
    focus: str | None,
    source_columns: list[str],
    judge_model: str,
    judge_timeout: int,
    attempts: int,
    log_path: Path,
    no_llm_judge: bool = False,
) -> dict[str, Any]:
    """Return a per-scenario characteristic-adherence report."""
    columns_payload = _columns_payload(new_columns, specs_by_name, augment_table)

    if no_llm_judge or not new_columns:
        judge = _empty_judgement(category, new_columns)
    else:
        prompt = build_prompt(
            category=category,
            query=query,
            focus=focus,
            source_columns=source_columns,
            columns_payload=columns_payload,
        )
        judge = semrec._invoke_judge(
            prompt,
            model=judge_model,
            timeout_s=judge_timeout,
            attempts=attempts,
            log_path=log_path,
        )

    metrics = _category_metrics(category, judge, n_added=len(new_columns), new_columns=new_columns)
    return {
        "category": category,
        "category_label": CATEGORY_LABEL[category],
        "query": query,
        "focus_variable": focus,
        "n_added_columns": len(new_columns),
        "added_columns": new_columns,
        "metrics": metrics,
        "judge": judge,
    }


def _empty_judgement(category: str, new_columns: list[str]) -> dict[str, Any]:
    base = {"category": category, "per_column": [], "adherence": 0.0, "rationale": "no added columns or judge skipped"}
    if category == "causal_relation":
        base.update({"treatment_present": False, "treatment_columns": [], "confounder_present": False, "confounder_columns": [], "n_confounders": 0, "confounder_quality": 0.0})
    elif category == "focus_relation":
        base.update({"n_predictors": 0, "predictor_fraction": 0.0})
    else:
        base.update({"facet_columns": [], "non_facet_columns": list(new_columns), "facet_fraction": 0.0, "mece": 0.0})
    return base


def _f(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


import re as _re


def _normalized_redundancy(new_columns: list[str] | None) -> float:
    """Fraction of columns that are near-duplicates (same name after normalization)."""
    cols = [str(c) for c in (new_columns or [])]
    if not cols:
        return 0.0
    norms = [_re.sub(r"[^a-z0-9]", "", c.lower()) for c in cols]
    unique = len(set(norms))
    return round(1.0 - unique / len(norms), 4)


def dedup_exact(columns: list[str]) -> tuple[list[str], list[str]]:
    """Drop EXACT-synonym duplicate columns (identical after lowercasing + stripping
    non-alphanumerics, e.g. ``FailureMode`` vs ``failure_mode``). Keeps the first
    occurrence in column order. Returns ``(kept, dropped)``. Does NOT touch
    semantically-near duplicates like ``TextureMouthfeel`` vs ``TextureAndMouthfeel``.
    """
    seen: dict[str, str] = {}
    kept: list[str] = []
    dropped: list[str] = []
    for c in columns:
        norm = _re.sub(r"[^a-z0-9]", "", str(c).lower())
        if norm in seen:
            dropped.append(str(c))
        else:
            seen[norm] = str(c)
            kept.append(str(c))
    return kept, dropped


def _category_metrics(category: str, judge: dict[str, Any], *, n_added: int, new_columns: list[str] | None = None) -> dict[str, Any]:
    """Flatten the judge output into a small, comparable metric block."""
    if category == "focus_internal_structure":
        # Fair, reproducible facet score: adherence = facet_fraction * coverage * (1 - redundancy).
        # facet_fraction comes from per-column judgments; redundancy is computed deterministically
        # from the column names (exposes duplicate-column defects explicitly); coverage is the judge's
        # estimate of how completely the facets cover the concept.
        per = judge.get("per_column") or []
        n_facet = sum(1 for c in per if isinstance(c, dict) and c.get("is_constitutive_facet"))
        facet_fraction = round(n_facet / n_added, 4) if n_added else 0.0
        redundancy = _normalized_redundancy(new_columns)
        coverage = round(max(0.0, min(1.0, _f(judge.get("coverage")))), 4)
        adherence = round(facet_fraction * coverage * (1.0 - redundancy), 4)
        return {
            "n_added_columns": n_added,
            "adherence": adherence,
            "facet_fraction": facet_fraction,
            "coverage": coverage,
            "redundancy": redundancy,
        }

    adherence = round(max(0.0, min(1.0, _f(judge.get("adherence")))), 4)
    common = {"n_added_columns": n_added, "adherence": adherence}
    if category == "causal_relation":
        return {
            **common,
            "treatment_present": bool(judge.get("treatment_present")),
            "confounder_present": bool(judge.get("confounder_present")),
            "n_confounders": int(_f(judge.get("n_confounders"))),
            "confounder_quality": round(max(0.0, min(1.0, _f(judge.get("confounder_quality")))), 4),
        }
    if category == "focus_relation":
        return {
            **common,
            "n_predictors": int(_f(judge.get("n_predictors"))),
            "predictor_fraction": round(max(0.0, min(1.0, _f(judge.get("predictor_fraction")))), 4),
        }
    return common


# --------------------------------------------------------------------------- #
# CLI (single scenario)
# --------------------------------------------------------------------------- #
def _main() -> int:
    parser = argparse.ArgumentParser(description="Characteristic-adherence evaluation of one augmented table.")
    parser.add_argument("--augment", required=True, type=Path, help="Augmented table (csv/xlsx/parquet).")
    parser.add_argument("--specs", type=Path, default=None, help="specs.json for the augmentation (optional).")
    parser.add_argument("--source", type=Path, default=None, help="Original table to diff for new columns (optional).")
    parser.add_argument("--query", default="", help="Analytical query text.")
    parser.add_argument("--scenario", default="", help="Scenario name (used for category fallback).")
    parser.add_argument("--category", default=None, choices=list(CATEGORY_LABEL), help="Override the detected category.")
    parser.add_argument("--judge-model", default="claude-opus-4-5")
    parser.add_argument("--judge-timeout", type=int, default=240)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--no-llm-judge", action="store_true")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    augment = semrec._read_table(args.augment).reset_index(drop=True)
    specs_payload = semrec._read_json(args.specs) if args.specs and args.specs.exists() else {}
    specs_by_name = {str(s.get("name")): s for s in (specs_payload.get("specs") or []) if s.get("name")}

    if specs_by_name:
        new_columns = [c for c in specs_by_name if c in augment.columns]
    elif args.source and args.source.exists():
        source = semrec._read_table(args.source)
        new_columns = semrec._source_new_columns(source, augment)
    else:
        new_columns = [str(c) for c in augment.columns]

    source_columns = (
        [str(c) for c in semrec._read_table(args.source).columns]
        if args.source and args.source.exists()
        else [str(c) for c in augment.columns if c not in new_columns]
    )
    category = args.category or detect_category(args.scenario, specs_payload)
    focus = _focus_from_specs(specs_payload)

    log_path = (args.out.parent if args.out else Path.cwd()) / "_characteristic_judge_call.json"
    report = evaluate(
        augment_table=augment,
        new_columns=new_columns,
        specs_by_name=specs_by_name,
        category=category,
        query=args.query,
        focus=focus,
        source_columns=source_columns,
        judge_model=args.judge_model,
        judge_timeout=args.judge_timeout,
        attempts=args.attempts,
        log_path=log_path,
        no_llm_judge=args.no_llm_judge,
    )
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        semrec._write_json(args.out, report)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
