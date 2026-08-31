"""Fair2 evaluation for the *focus internal structure* category.

Motivation (advisor sync, 2026-07-16)
-------------------------------------
The paper (SADA, Table 1 / §2.2 / §3.1) splits ``focus internal structure`` into
two sub-intents that must be judged differently:

  * **Faceted decomposition** --- the focus is a *textual concept named in the
    query* (e.g. the concept *complaint*, *food quality*). The added columns
    should be its constitutive FACETS (part-of / meronymy), not predictors of
    it. There IS a ground-truth "focus" here, but it is the concept the QUERY
    names --- not a scalar column, and not the (sometimes broken / placeholder)
    ``focus_variable`` string in our annotations. So we infer the concept once
    from the query (variant-blind, model-blind, frozen, shared) and judge every
    variant's columns against that same concept.

  * **Focus inference** --- "Focus: none initially" (paper). The system must
    PROPOSE a focus; a wrong focus makes even flawless extraction worthless. By
    definition there is NO ground-truth focus, so anchoring on a fixed one
    contradicts the taxonomy. We instead judge (a) whether the added columns
    center on a single coherent, data-inferable focus concept, and (b) whether
    they form a reasonable analytical structure around it.

Routing: GT ``subtype == focus_inference`` -> focus-inference rubric. Otherwise
run Stage-0 concept inference; if the query does not actually name a concept
(``is_focus_named == false``, e.g. "help me understand what to focus on") we
also route to the focus-inference rubric. This keeps the decision query-driven
and principled instead of hand-labelling scenarios.

The faceted adherence formula is IDENTICAL to ``characteristic_evaluation_fair``
(``facet_fraction * coverage * (1 - redundancy)``) so the two runs stay
comparable; only the *anchor concept* changes (query-inferred vs. annotation
``focus_variable``).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import characteristic_adherence as charadh  # noqa: E402  (adds scorer/ to path)
import semantic_reference_recall as semrec   # noqa: E402


FACET_CATEGORY = "focus_internal_structure"
FOCUS_INFERENCE_CATEGORY = "focus_inference"

CATEGORY_LABEL = {
    FACET_CATEGORY: "Focus internal structure / faceted decomposition (query-inferred concept)",
    FOCUS_INFERENCE_CATEGORY: "Focus internal structure / focus inference (no given focus)",
}


# --------------------------------------------------------------------------- #
# Stage-0: infer the concept-to-decompose from the QUERY ONLY (variant-blind).
# --------------------------------------------------------------------------- #
def build_concept_prompt(*, query: str, domain_hint: str | None) -> str:
    task = {
        "analytical_query": query,
        "dataset_domain_hint": domain_hint or "",
    }
    return (
        "You are analysing a focus-oriented analytical request over a text-rich table.\n"
        "This request belongs to the FOCUS INTERNAL STRUCTURE family: the analyst wants to look "
        "INWARD at a focus concept and decompose it into its constitutive FACETS (part-of / meronymy).\n\n"
        "Your ONLY job now is to read the analytical query (and the domain hint) and decide which sub-intent it is.\n\n"
        "DEFAULT to FACETED DECOMPOSITION. Treat the query as faceted (is_focus_named = true) whenever ANY "
        "concept, theme, or subject can be identified from the query to decompose into parts --- even if:\n"
        "  * the concept is COMPOUND or dual-pole, e.g. 'praise AND complaints', 'satisfaction and complaint "
        "themes' (concept = 'praise/complaint themes'); combine the poles into one compound concept.\n"
        "  * the query is phrased CAUSALLY or as 'why/what drives/what kinds', e.g. 'Why do some incidents take "
        "longer to resolve?' (concept = 'incident resolution delay reasons'), 'What kinds of tickets create "
        "heavier agent workload?' (concept = 'agent workload'), 'What drives praise and complaints?' "
        "(concept = 'praise/complaint drivers'). In this family, still extract the underlying concept and "
        "decompose it into part-of facets.\n"
        "  * the query names the subject only broadly, e.g. 'What travel policy risks appear...?' "
        "(concept = 'travel policy risk').\n\n"
        "Route to FOCUS INFERENCE (is_focus_named = false) ONLY in the RARE case where the query names NO "
        "subject at all and a focus must first be PROPOSED before anything can be decomposed --- i.e. a truly "
        "open, contentless request such as 'Help me understand what's in this data; I'm not sure what's "
        "actionable' or 'What should I focus on / concentrate on in this table?'. If in doubt, choose FACETED.\n\n"
        "If a concept is identified, return it and a short list of the constitutive facets you would EXPECT a "
        "good decomposition to cover (a soft reference for coverage, NOT an exhaustive answer key).\n"
        "Judge ONLY from the query text. Do NOT invent columns and do NOT look at any augmentation output.\n\n"
        "Return strict JSON only:\n"
        "{\n"
        '  "is_focus_named": true,\n'
        '  "concept_to_decompose": "food quality",   // the concept (may be compound), or null only if truly open\n'
        '  "expected_facets": ["taste", "texture", "freshness", "value"],  // soft, 3-8 items, [] only if focus not named\n'
        '  "rationale": "..."\n'
        "}\n\n"
        f"Input JSON:\n{json.dumps(task, ensure_ascii=False, indent=2)}"
    )


def infer_concept(
    *,
    query: str,
    domain_hint: str | None,
    judge_model: str,
    judge_timeout: int,
    attempts: int,
    log_path: Path,
) -> dict[str, Any]:
    prompt = build_concept_prompt(query=query, domain_hint=domain_hint)
    out = semrec._invoke_judge(
        prompt,
        model=judge_model,
        timeout_s=judge_timeout,
        attempts=attempts,
        log_path=log_path,
    )
    concept = out.get("concept_to_decompose")
    return {
        "is_focus_named": bool(out.get("is_focus_named")) and bool(concept),
        "concept_to_decompose": str(concept) if concept else None,
        "expected_facets": [str(f) for f in (out.get("expected_facets") or []) if f],
        "rationale": str(out.get("rationale") or ""),
    }


# --------------------------------------------------------------------------- #
# Stage-1 prompts
# --------------------------------------------------------------------------- #
def build_facet_prompt(
    *,
    query: str,
    concept: str,
    expected_facets: list[str],
    columns_payload: list[dict[str, Any]],
) -> str:
    task = {
        "analytical_query": query,
        "concept_to_decompose": concept,
        "expected_facets_soft_reference": expected_facets,
        "added_columns": columns_payload,
    }
    return (
        "You are a strict evaluator of a text-to-table augmentation operator.\n"
        "The request is a FACETED DECOMPOSITION of a single concept: the added columns should be the "
        "constitutive FACETS / PARTS of the concept below (a part-of / meronymy relationship), NOT external "
        "predictors, causes, or restatements of it. A facet is 'a kind of / an aspect of' the concept.\n\n"
        f"CONCEPT TO DECOMPOSE (fixed for all systems being compared): \"{concept}\"\n"
        "The 'expected_facets_soft_reference' list is a NON-binding hint of aspects a good decomposition tends "
        "to cover; do NOT penalise valid facets merely for being absent from that list, and do NOT reward "
        "columns just for matching its wording.\n\n"
        "Judge each added column independently against THIS concept. Then estimate how completely the facet "
        "columns COVER the concept's main constitutive aspects (coverage), independent of column count.\n\n"
        "Return strict JSON only:\n"
        "{\n"
        f'  "category": "{FACET_CATEGORY}",\n'
        '  "concept_to_decompose": "%s",\n' % concept
        + '  "per_column": [{"name": "...", "is_constitutive_facet": true, "is_external_predictor": false, "rationale": "..."}],\n'
        '  "facet_columns": [], "non_facet_columns": [],\n'
        '  "coverage": 0.0,   // 0-1: how completely the facet columns cover the concept\'s main aspects\n'
        '  "rationale": "..."\n'
        "}\n\n"
        "Scoring guidance: a generic or mechanical set of columns (sentiment-only, text length, or predictors "
        "of the concept rather than parts of it) should have few/no constitutive facets.\n\n"
        f"Evaluation input JSON:\n{json.dumps(task, ensure_ascii=False, indent=2)}"
    )


def build_gt_facet_prompt(
    *,
    query: str,
    concept: str,
    gt_facets: list[dict[str, Any]],
    columns_payload: list[dict[str, Any]],
) -> str:
    """GT-grounded faceted judge.

    Instead of asking the judge to decide, from an abstract "part-of / meronymy"
    rubric, whether each produced column is a constitutive facet, we give it the
    GROUND-TRUTH reference facets (the annotator-authored ``augmentation_plan.specs``
    for this scenario: name + description + value domain) and ask it to
    SEMANTICALLY MATCH each produced column to one of those GT facets. This fixes
    the systematic bias where GT-sanctioned facets that happen to read like a
    mechanism / severity / action (e.g. ``OperationalBurdenDriver``,
    ``IssueSeverity``, ``AutomationPotential``) were wrongly rejected as
    "external predictors". A column counts as a facet iff it aligns with a GT
    facet; coverage is over the GT facet set.
    """
    task = {
        "analytical_query": query,
        "concept_to_decompose": concept,
        "ground_truth_reference_facets": gt_facets,
        "added_columns": columns_payload,
    }
    return (
        "You are a strict evaluator of a text-to-table augmentation operator on a FACETED DECOMPOSITION task.\n"
        f"CONCEPT TO DECOMPOSE (fixed for all systems being compared): \"{concept}\".\n\n"
        "You are given the GROUND-TRUTH reference facets ('ground_truth_reference_facets'): the "
        "annotator-authored set of facets that a correct decomposition of this concept should contain "
        "(each has a name, a description, and often a categorical value domain). This GT set is the "
        "AUTHORITATIVE definition of what counts as a valid facet for this concept. IMPORTANT: the GT set "
        "intentionally INCLUDES facets that may read like a driver/mechanism, a severity/impact level, a "
        "resolution/handling path, or an actionability signal --- these ARE valid facets here. Do NOT apply "
        "your own abstract 'must be pure part-of, not a predictor' test; defer to the GT set.\n\n"
        "For EACH produced column, decide whether it SEMANTICALLY MATCHES one of the GT reference facets "
        "(same underlying aspect, regardless of naming/casing/among value-encoding differences). Map it to "
        "the single best-matching GT facet name, or null if it corresponds to NO GT facet. Matching is by "
        "meaning: e.g. 'root_cause_mechanism' matches a GT 'OperationalBurdenDriver'; 'workaround_available' "
        "matches a GT 'AutomationPotential'; a generic sentiment/text-length/id column matches nothing.\n\n"
        "Return strict JSON only:\n"
        "{\n"
        f'  "category": "{FACET_CATEGORY}",\n'
        '  "concept_to_decompose": "%s",\n' % concept
        + '  "per_column": [{"name": "...", "matched_gt_facet": "GTFacetName or null", "rationale": "..."}],\n'
        '  "covered_gt_facets": ["GTFacetName", "..."],   // distinct GT facets matched by >=1 produced column\n'
        '  "rationale": "..."\n'
        "}\n\n"
        f"Evaluation input JSON:\n{json.dumps(task, ensure_ascii=False, indent=2)}"
    )


def build_focus_inference_prompt(
    *,
    query: str,
    columns_payload: list[dict[str, Any]],
) -> str:
    task = {
        "analytical_query": query,
        "added_columns": columns_payload,
    }
    return (
        "You are a strict evaluator of a text-to-table augmentation operator.\n"
        "The request is a FOCUS INFERENCE task: the query is open-ended and names NO focus, so a good system "
        "must first PROPOSE a coherent focus concept (inferable from the data/text) and then structure the "
        "added columns around it. There is deliberately NO ground-truth focus; judge the columns on their own "
        "internal coherence.\n\n"
        "Assess two things:\n"
        "  (1) focus_coherence [0-1]: do the added columns collectively center on ONE coherent, data-inferable "
        "focus concept (as opposed to a scattered, unfocused grab-bag of unrelated columns)? Infer the implied "
        "focus yourself from the columns.\n"
        "  (2) structure_quality [0-1]: given that implied focus, do the columns form a reasonable analytical "
        "structure around it (coherent facets or a coherent predictor/attribute set), at a useful granularity "
        "(neither a single restatement nor scattered noise)?\n\n"
        "Return strict JSON only:\n"
        "{\n"
        f'  "category": "{FOCUS_INFERENCE_CATEGORY}",\n'
        '  "implied_focus": "...",          // the focus you infer the columns center on, or null\n'
        '  "per_column": [{"name": "...", "supports_focus": true, "rationale": "..."}],\n'
        '  "focus_coherence": 0.0,\n'
        '  "structure_quality": 0.0,\n'
        '  "rationale": "..."\n'
        "}\n\n"
        "Scoring guidance: an unfocused / generic set of columns with no discernible single focus should score "
        "low on focus_coherence.\n\n"
        f"Evaluation input JSON:\n{json.dumps(task, ensure_ascii=False, indent=2)}"
    )


# --------------------------------------------------------------------------- #
# Evaluate one variant
# --------------------------------------------------------------------------- #
def evaluate(
    *,
    augment_table,
    new_columns: list[str],
    specs_by_name: dict[str, dict[str, Any]],
    query: str,
    concept_info: dict[str, Any],
    judge_model: str,
    judge_timeout: int,
    attempts: int,
    log_path: Path,
    no_llm_judge: bool = False,
    gt_facets: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    columns_payload = charadh._columns_payload(new_columns, specs_by_name, augment_table)
    is_focus_named = bool(concept_info.get("is_focus_named"))
    category = FACET_CATEGORY if is_focus_named else FOCUS_INFERENCE_CATEGORY
    gt_facets = gt_facets if gt_facets is not None else (concept_info.get("gt_facets") or [])
    gt_facets = [f for f in gt_facets if isinstance(f, dict) and f.get("name")]
    use_gt = bool(is_focus_named and gt_facets)

    if no_llm_judge or not new_columns:
        judge = {"category": category, "per_column": [], "rationale": "no added columns or judge skipped"}
    elif use_gt:
        prompt = build_gt_facet_prompt(
            query=query,
            concept=concept_info.get("concept_to_decompose") or "",
            gt_facets=gt_facets,
            columns_payload=columns_payload,
        )
        judge = semrec._invoke_judge(prompt, model=judge_model, timeout_s=judge_timeout, attempts=attempts, log_path=log_path)
    elif is_focus_named:
        prompt = build_facet_prompt(
            query=query,
            concept=concept_info.get("concept_to_decompose") or "",
            expected_facets=concept_info.get("expected_facets") or [],
            columns_payload=columns_payload,
        )
        judge = semrec._invoke_judge(prompt, model=judge_model, timeout_s=judge_timeout, attempts=attempts, log_path=log_path)
    else:
        prompt = build_focus_inference_prompt(query=query, columns_payload=columns_payload)
        judge = semrec._invoke_judge(prompt, model=judge_model, timeout_s=judge_timeout, attempts=attempts, log_path=log_path)

    metrics = _metrics(category, judge, n_added=len(new_columns), new_columns=new_columns, gt_facets=gt_facets if use_gt else None)
    return {
        "category": category,
        "category_label": CATEGORY_LABEL[category],
        "query": query,
        "concept_to_decompose": concept_info.get("concept_to_decompose"),
        "is_focus_named": is_focus_named,
        "gt_grounded": use_gt,
        "gt_reference_facets": [f.get("name") for f in gt_facets] if use_gt else [],
        "n_added_columns": len(new_columns),
        "added_columns": new_columns,
        "metrics": metrics,
        "judge": judge,
    }


def _metrics(
    category: str,
    judge: dict[str, Any],
    *,
    n_added: int,
    new_columns: list[str],
    gt_facets: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    redundancy = charadh._normalized_redundancy(new_columns)
    if category == FACET_CATEGORY:
        per = judge.get("per_column") or []
        if gt_facets:
            # GT-grounded: a column is a facet iff it matches a GT reference facet.
            gt_names = {str(f.get("name")) for f in gt_facets if f.get("name")}
            matched_by_col = [
                str(c.get("matched_gt_facet")).strip()
                for c in per
                if isinstance(c, dict) and c.get("matched_gt_facet") and str(c.get("matched_gt_facet")).strip().lower() not in {"", "null", "none"}
            ]
            n_facet = sum(1 for m in matched_by_col if m in gt_names)
            # fall back to name-insensitive containment if the judge lightly renamed
            if not gt_names:
                covered = set()
            else:
                covered = {m for m in matched_by_col if m in gt_names}
                declared = {str(x).strip() for x in (judge.get("covered_gt_facets") or []) if str(x).strip() in gt_names}
                covered |= declared
            facet_fraction = round(n_facet / n_added, 4) if n_added else 0.0
            coverage = round(len(covered) / len(gt_names), 4) if gt_names else 0.0
            adherence = round(facet_fraction * coverage * (1.0 - redundancy), 4)
            return {
                "n_added_columns": n_added,
                "adherence": adherence,
                "facet_fraction": facet_fraction,
                "coverage": coverage,
                "redundancy": redundancy,
                "gt_grounded": True,
                "n_gt_facets": len(gt_names),
                "n_covered_gt_facets": len(covered),
                "n_matched_columns": n_facet,
            }
        n_facet = sum(1 for c in per if isinstance(c, dict) and c.get("is_constitutive_facet"))
        facet_fraction = round(n_facet / n_added, 4) if n_added else 0.0
        coverage = round(max(0.0, min(1.0, charadh._f(judge.get("coverage")))), 4)
        adherence = round(facet_fraction * coverage * (1.0 - redundancy), 4)
        return {
            "n_added_columns": n_added,
            "adherence": adherence,
            "facet_fraction": facet_fraction,
            "coverage": coverage,
            "redundancy": redundancy,
        }
    # focus inference
    focus_coherence = round(max(0.0, min(1.0, charadh._f(judge.get("focus_coherence")))), 4)
    structure_quality = round(max(0.0, min(1.0, charadh._f(judge.get("structure_quality")))), 4)
    adherence = round(focus_coherence * structure_quality * (1.0 - redundancy), 4)
    return {
        "n_added_columns": n_added,
        "adherence": adherence,
        "focus_coherence": focus_coherence,
        "structure_quality": structure_quality,
        "redundancy": redundancy,
    }
