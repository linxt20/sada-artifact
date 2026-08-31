"""B-2: instruction-following / characteristic adherence, per FOI subtype.

Experiment B-2 (SADA_experiment_design_final.md)
-----------------------------------------------
B-2 is fundamentally an **instruction-following** test: for each of the 6 FOI
intent subtypes, the paper makes a specific technical claim about what the
augmented columns should look like. The grader prompt must state that claim
explicitly -- otherwise the judge only asks "are these columns reasonable?",
which is exactly the shallow failure mode the advisor warned about.

What changed vs ``scorer_characteristic`` (v1)
---------------------------------------------
1. **6 subtypes, not 3 families.** v1 collapsed predictive_feature_engineering
   with exploratory_data_analysis, and what_if with causal_attribution. Those
   pairs have genuinely different claims (a predictor set for a *model* vs. for
   *understanding*; an *intervenable* treatment vs. an *observed* cause), so
   each now gets its own tailored rubric while sharing a family-level metric
   block so results stay aggregable.

2. **Causal: the confounder must be UNNAMED.** The paper's headline claim is
   that SADA surfaces confounders the analyst did *not* name in the query. v1
   only asked "is a confounder present", which a system can satisfy by echoing
   a confounder straight out of the query text. v2 asks the judge to mark, per
   confounder, whether it was already named in the query, and reports
   ``unnamed_confounder_present`` / ``n_unnamed_confounders`` as the primary
   causal metrics.

3. **Causal: treatment must be intervenable (what_if).** For ``what_if`` the
   treatment has to be something you could actually set/change; for
   ``causal_attribution`` it may be a merely observed cause.

4. **MECE restored for faceted decomposition.** The design doc lists MECE as a
   B-2 metric. v1's ``characteristic_adherence.py`` declared ``mece`` in its
   empty-judgement stub but never asked the judge for it nor used it in the
   score; ``_fair2`` replaced it with ``coverage``. v2 asks for BOTH
   mutual-exclusivity and exhaustiveness explicitly and folds them into the
   score.

5. **Adherence is composed, not free-scored.** v1 let the judge emit a holistic
   ``adherence`` float for the causal/correlational families, so the headline
   number was a vibe rather than a function of the sub-claims. v2 computes
   adherence deterministically from the checkable sub-metrics; the judge only
   supplies the components. This makes the score auditable and stops the judge
   from silently re-weighting the technical claim.

Adherence formulas (all in [0,1]):

  predictive_feature_engineering : predictor_fraction * predictive_utility
  exploratory_data_analysis      : predictor_fraction * relationship_informativeness
  causal_attribution             : treatment_present * (0.4 + 0.6*unnamed_bonus) * confounder_quality
  what_if                        : treatment_intervenable * (0.4 + 0.6*unnamed_bonus) * confounder_quality
  faceted_decomposition          : facet_fraction * mece * (1 - redundancy)
  focus_inference                : focus_coherence * structure_quality * (1 - redundancy)

where ``unnamed_bonus`` = 1 if at least one confounder was NOT named in the
query else 0, and ``mece`` = sqrt(mutual_exclusivity * exhaustiveness).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
SCORER_DIR = ROOT / "scorer"
CHAR_DIR = ROOT / "scorer_characteristic"
for _p in (str(SCORER_DIR), str(CHAR_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import semantic_reference_recall as semrec  # noqa: E402
import characteristic_adherence as charadh  # noqa: E402


# --------------------------------------------------------------------------- #
# The 6 FOI subtypes and their families
# --------------------------------------------------------------------------- #
SUBTYPES = (
    "predictive_feature_engineering",
    "exploratory_data_analysis",
    "causal_attribution",
    "what_if",
    "faceted_decomposition",
    "focus_inference",
)

FAMILY_OF = {
    "predictive_feature_engineering": "correlational",
    "exploratory_data_analysis": "correlational",
    "causal_attribution": "causal",
    "what_if": "causal",
    "faceted_decomposition": "focus_internal",
    "focus_inference": "focus_internal",
}

SUBTYPE_LABEL = {
    "predictive_feature_engineering": "Correlational / predictive feature engineering",
    "exploratory_data_analysis": "Correlational / exploratory data analysis",
    "causal_attribution": "Causal / attribution (observed cause)",
    "what_if": "Causal / what-if (intervenable treatment)",
    "faceted_decomposition": "Focus internal / faceted decomposition (MECE facets)",
    "focus_inference": "Focus internal / focus inference (no given focus)",
}

# GT expected_structure -> subtype fallback when GT.subtype is absent/unknown.
_STRUCT_FALLBACK = {
    "causal_graph": "causal_attribution",
    "prediction_tree": "predictive_feature_engineering",
    "flat_feature_set": "predictive_feature_engineering",
    "concept_tree": "faceted_decomposition",
}


def resolve_subtype(gt_query: dict[str, Any] | None) -> str:
    """Canonical subtype for a scenario, from the GT annotation."""
    q = gt_query or {}
    subtype = str(q.get("subtype") or "").strip().lower()
    if subtype in SUBTYPES:
        return subtype
    structure = str(q.get("expected_structure") or "").strip()
    if structure in _STRUCT_FALLBACK:
        return _STRUCT_FALLBACK[structure]
    family = str(q.get("family") or "").strip().lower()
    if family == "causal":
        return "causal_attribution"
    if family in {"concept", "concept_attribute", "faceted"}:
        return "faceted_decomposition"
    return "predictive_feature_engineering"


# --------------------------------------------------------------------------- #
# Per-subtype rubrics -- the technical claim, stated explicitly
# --------------------------------------------------------------------------- #
_RUBRICS: dict[str, str] = {
    "predictive_feature_engineering": (
        "TECHNICAL CLAIM UNDER TEST (predictive feature engineering):\n"
        "The added columns must be usable FEATURES for PREDICTING the focus variable. Each should be a "
        "variable that lies OUTSIDE the focus (not a restatement, not a component or a deterministic "
        "function of it, and not something only knowable after the outcome -- that would be leakage) and "
        "should plausibly carry predictive signal about it.\n"
        "Judge each column on: is it a legitimate predictor (predictor), or does it restate/leak the focus "
        "(leakage), or is it simply unrelated (irrelevant)?\n\n"
        "Return strict JSON only:\n"
        "{\n"
        '  "subtype": "predictive_feature_engineering",\n'
        '  "focus_variable": "...",\n'
        '  "per_column": [{"name": "...", "role": "predictor|leakage|restatement|irrelevant", '
        '"is_predictor": true, "rationale": "..."}],\n'
        '  "n_predictors": 0,\n'
        '  "predictive_utility": 0.0,   // 0-1: as a SET, how much genuine predictive leverage do these give '
        'a model of the focus (beyond the original columns)?\n'
        '  "rationale": "..."\n'
        "}"
    ),
    "exploratory_data_analysis": (
        "TECHNICAL CLAIM UNDER TEST (exploratory data analysis):\n"
        "The added columns must open up INFORMATIVE RELATIONSHIPS around the focus for a human explorer. "
        "Each should be an external, associational variable that can be grouped/segmented on and compared "
        "against the focus. Unlike feature engineering, the goal is human UNDERSTANDING, not model input: "
        "columns must have interpretable, well-separated categories or scales, not opaque scores.\n"
        "Penalise columns that merely restate the focus, and columns whose values are so fine-grained or so "
        "near-constant that no meaningful comparison can be drawn.\n\n"
        "Return strict JSON only:\n"
        "{\n"
        '  "subtype": "exploratory_data_analysis",\n'
        '  "focus_variable": "...",\n'
        '  "per_column": [{"name": "...", "role": "predictor|restatement|irrelevant", '
        '"is_predictor": true, "is_interpretable_segmentation": true, "rationale": "..."}],\n'
        '  "n_predictors": 0,\n'
        '  "relationship_informativeness": 0.0,   // 0-1: as a SET, how well do these support discovering '
        'interpretable relationships with the focus?\n'
        '  "rationale": "..."\n'
        "}"
    ),
    "causal_attribution": (
        "TECHNICAL CLAIM UNDER TEST (causal attribution):\n"
        "The added columns must set up a CAUSAL ESTIMATION around the focus (the OUTCOME). Specifically they "
        "must supply:\n"
        "  (a) a TREATMENT -- the candidate cause whose effect on the outcome is being attributed; and\n"
        "  (b) CONFOUNDERS -- variables that plausibly cause BOTH the treatment and the outcome, and which "
        "therefore MUST be adjusted for or the attribution is biased.\n\n"
        "THE DECISIVE TEST: a confounder is only evidence of real causal reasoning if the system SURFACED it "
        "from the data/text rather than copying it from the query. For EACH confounder you identify, decide "
        "whether that variable was ALREADY NAMED OR CLEARLY IMPLIED in the analytical query text. Set "
        '"named_in_query": true if it was. Confounders with "named_in_query": false are the ones that '
        "demonstrate the capability under test.\n"
        "Do NOT count mediators (on the causal path from treatment to outcome) or colliders as confounders -- "
        "adjusting for those is a mistake, and labelling them confounders is an error you should mark.\n\n"
        "Return strict JSON only:\n"
        "{\n"
        '  "subtype": "causal_attribution",\n'
        '  "outcome_variable": "...",\n'
        '  "per_column": [{"name": "...", "causal_role": "treatment|confounder|mediator|collider|outcome|other", '
        '"named_in_query": false, "rationale": "..."}],\n'
        '  "treatment_present": false, "treatment_columns": [],\n'
        '  "confounders": [{"name": "...", "named_in_query": false, "plausibility": 0.0}],\n'
        '  "confounder_quality": 0.0,   // 0-1: are the confounders genuine common causes of BOTH treatment '
        'and outcome (not mediators/colliders/noise)?\n'
        '  "rationale": "..."\n'
        "}"
    ),
    "what_if": (
        "TECHNICAL CLAIM UNDER TEST (what-if / intervention):\n"
        "The added columns must set up an INTERVENTIONAL question about the focus (the OUTCOME). This is "
        "stricter than attribution:\n"
        "  (a) the TREATMENT must be something an actor could actually SET, CHANGE, or DECIDE -- an "
        "intervenable lever (a policy, an action, an assignment, a configurable property). An immutable "
        "attribute (e.g. an intrinsic trait, a date that already happened) is NOT a valid what-if treatment, "
        "even if it causes the outcome; and\n"
        "  (b) CONFOUNDERS -- common causes of both the treatment and the outcome, which must be adjusted for "
        "before the counterfactual effect can be read off.\n\n"
        "THE DECISIVE TEST: for EACH confounder, decide whether it was ALREADY NAMED OR CLEARLY IMPLIED in "
        'the query text ("named_in_query"). Confounders NOT named in the query are the ones that demonstrate '
        "the capability under test.\n"
        "Do NOT count mediators or colliders as confounders.\n\n"
        "Return strict JSON only:\n"
        "{\n"
        '  "subtype": "what_if",\n'
        '  "outcome_variable": "...",\n'
        '  "per_column": [{"name": "...", "causal_role": "treatment|confounder|mediator|collider|outcome|other", '
        '"named_in_query": false, "rationale": "..."}],\n'
        '  "treatment_present": false, "treatment_columns": [],\n'
        '  "treatment_intervenable": false,   // is at least one identified treatment actually settable/changeable?\n'
        '  "confounders": [{"name": "...", "named_in_query": false, "plausibility": 0.0}],\n'
        '  "confounder_quality": 0.0,\n'
        '  "rationale": "..."\n'
        "}"
    ),
    "faceted_decomposition": (
        "TECHNICAL CLAIM UNDER TEST (faceted decomposition):\n"
        "The added columns must be constitutive FACETS / PARTS of the focus concept -- a part-of (meronymy) "
        "relationship. A facet is 'an aspect OF' the concept, NOT an external predictor of it, NOT a cause of "
        "it, and NOT a restatement of the whole concept.\n\n"
        "Then judge the facet set on MECE:\n"
        "  * mutual_exclusivity [0-1]: do the facets carve the concept into NON-OVERLAPPING aspects? Two "
        "columns capturing the same underlying aspect under different names lowers this.\n"
        "  * exhaustiveness [0-1]: do the facets together COVER the concept's main constitutive aspects? "
        "Judge against the concept itself, not against column count.\n\n"
        "Return strict JSON only:\n"
        "{\n"
        '  "subtype": "faceted_decomposition",\n'
        '  "concept": "...",\n'
        '  "per_column": [{"name": "...", "is_constitutive_facet": true, '
        '"role": "facet|external_predictor|cause|restatement|irrelevant", "rationale": "..."}],\n'
        '  "facet_columns": [], "non_facet_columns": [],\n'
        '  "mutual_exclusivity": 0.0,\n'
        '  "exhaustiveness": 0.0,\n'
        '  "rationale": "..."\n'
        "}"
    ),
    "focus_inference": (
        "TECHNICAL CLAIM UNDER TEST (focus inference):\n"
        "The query names NO focus -- the system must first PROPOSE one. By design there is NO ground-truth "
        "focus, so do not anchor on any particular answer. Instead judge:\n"
        "  * focus_coherence [0-1]: do the added columns collectively centre on ONE coherent, data-inferable "
        "focus concept, rather than being a scattered grab-bag? Infer the implied focus yourself.\n"
        "  * structure_quality [0-1]: given that implied focus, do the columns form a sound analytical "
        "structure around it (coherent facets, or a coherent predictor/attribute set) at a useful "
        "granularity -- neither a single restatement nor undifferentiated noise?\n"
        "  * focus_actionability [0-1]: is the implied focus one an analyst could actually act on / "
        "investigate further, as opposed to a trivial or vacuous framing?\n\n"
        "Return strict JSON only:\n"
        "{\n"
        '  "subtype": "focus_inference",\n'
        '  "implied_focus": "...",\n'
        '  "per_column": [{"name": "...", "supports_focus": true, "rationale": "..."}],\n'
        '  "focus_coherence": 0.0,\n'
        '  "structure_quality": 0.0,\n'
        '  "focus_actionability": 0.0,\n'
        '  "rationale": "..."\n'
        "}"
    ),
}


def build_prompt(
    *,
    subtype: str,
    query: str,
    focus: str | None,
    concept: str | None,
    source_columns: list[str],
    columns_payload: list[dict[str, Any]],
) -> str:
    task = {
        "analytical_query": query,
        "focus_variable": focus,
        "concept_to_decompose": concept,
        "original_table_columns": source_columns,
        "added_columns": columns_payload,
    }
    return (
        "You are a strict evaluator of a text-to-table augmentation operator, grading INSTRUCTION FOLLOWING.\n"
        "An augmentation system was asked to serve the analytical query below and ADDED the columns listed. "
        "Your job is NOT to ask whether the columns are 'reasonable in general' -- it is to test whether they "
        "satisfy the SPECIFIC technical claim for this intent subtype, stated below. A set of columns can be "
        "perfectly sensible and still FAIL this test.\n\n"
        f"INTENT SUBTYPE: {SUBTYPE_LABEL[subtype]}\n\n"
        f"{_RUBRICS[subtype]}\n\n"
        "Judge the SEMANTICS of each added column. Ignore naming style, casing, and column order, and do not "
        "compare against any hidden reference schema. Be conservative: a mechanical or generic set of columns "
        "(text length, token counts, bare sentiment) does not realise any of these claims.\n\n"
        f"Evaluation input JSON:\n{json.dumps(task, ensure_ascii=False, indent=2)}"
    )


# --------------------------------------------------------------------------- #
# Metrics -- computed from the judge's components, not free-scored
# --------------------------------------------------------------------------- #
def _clip(value: Any) -> float:
    return round(max(0.0, min(1.0, charadh._f(value))), 4)


def _confounders(judge: dict[str, Any]) -> list[dict[str, Any]]:
    """Confounders, preferring the explicit list but falling back to per_column
    roles (judges sometimes fill only one of the two)."""
    explicit = [c for c in (judge.get("confounders") or []) if isinstance(c, dict) and c.get("name")]
    if explicit:
        return explicit
    return [
        {"name": c.get("name"), "named_in_query": c.get("named_in_query"), "plausibility": 1.0}
        for c in (judge.get("per_column") or [])
        if isinstance(c, dict) and str(c.get("causal_role") or "").lower() == "confounder"
    ]


def compute_metrics(subtype: str, judge: dict[str, Any], *, n_added: int, new_columns: list[str]) -> dict[str, Any]:
    redundancy = charadh._normalized_redundancy(new_columns)
    per = [c for c in (judge.get("per_column") or []) if isinstance(c, dict)]
    base: dict[str, Any] = {"n_added_columns": n_added, "subtype": subtype, "family": FAMILY_OF[subtype]}

    if subtype in ("predictive_feature_engineering", "exploratory_data_analysis"):
        n_pred = sum(1 for c in per if c.get("is_predictor"))
        predictor_fraction = round(n_pred / n_added, 4) if n_added else 0.0
        if subtype == "predictive_feature_engineering":
            set_score = _clip(judge.get("predictive_utility"))
            extra = {"predictive_utility": set_score,
                     "leakage_rate": round(sum(1 for c in per if str(c.get("role") or "").lower() == "leakage") / len(per), 4) if per else 0.0}
        else:
            set_score = _clip(judge.get("relationship_informativeness"))
            extra = {"relationship_informativeness": set_score,
                     "interpretable_fraction": round(sum(1 for c in per if c.get("is_interpretable_segmentation")) / len(per), 4) if per else 0.0}
        return {**base, "adherence": round(predictor_fraction * set_score, 4),
                "predictor_fraction": predictor_fraction, "n_predictors": n_pred,
                "redundancy": redundancy, **extra}

    if subtype in ("causal_attribution", "what_if"):
        confs = _confounders(judge)
        n_conf = len(confs)
        unnamed = [c for c in confs if not c.get("named_in_query")]
        treatment_present = bool(judge.get("treatment_present")) or any(
            str(c.get("causal_role") or "").lower() == "treatment" for c in per
        )
        conf_quality = _clip(judge.get("confounder_quality"))
        unnamed_bonus = 1.0 if unnamed else 0.0
        if subtype == "what_if":
            gate = 1.0 if (treatment_present and bool(judge.get("treatment_intervenable"))) else 0.0
            extra = {"treatment_intervenable": bool(judge.get("treatment_intervenable"))}
        else:
            gate = 1.0 if treatment_present else 0.0
            extra = {}
        adherence = round(gate * (0.4 + 0.6 * unnamed_bonus) * conf_quality, 4)
        return {**base, "adherence": adherence,
                "treatment_present": treatment_present,
                "confounder_present": n_conf > 0,
                "n_confounders": n_conf,
                "unnamed_confounder_present": bool(unnamed),
                "n_unnamed_confounders": len(unnamed),
                "unnamed_confounder_fraction": round(len(unnamed) / n_conf, 4) if n_conf else 0.0,
                "confounder_quality": conf_quality,
                "mediator_mislabel_count": sum(1 for c in per if str(c.get("causal_role") or "").lower() in {"mediator", "collider"}),
                "redundancy": redundancy, **extra}

    if subtype == "faceted_decomposition":
        n_facet = sum(1 for c in per if c.get("is_constitutive_facet"))
        facet_fraction = round(n_facet / n_added, 4) if n_added else 0.0
        mut_ex = _clip(judge.get("mutual_exclusivity"))
        exhaust = _clip(judge.get("exhaustiveness"))
        mece = round(math.sqrt(mut_ex * exhaust), 4)
        return {**base, "adherence": round(facet_fraction * mece * (1.0 - redundancy), 4),
                "facet_fraction": facet_fraction, "n_facets": n_facet,
                "mutual_exclusivity": mut_ex, "exhaustiveness": exhaust, "mece": mece,
                "redundancy": redundancy}

    # focus_inference
    coherence = _clip(judge.get("focus_coherence"))
    structure = _clip(judge.get("structure_quality"))
    actionability = _clip(judge.get("focus_actionability"))
    return {**base, "adherence": round(coherence * structure * (1.0 - redundancy), 4),
            "focus_coherence": coherence, "structure_quality": structure,
            "focus_actionability": actionability, "redundancy": redundancy}


# --------------------------------------------------------------------------- #
# Evaluate one variant
# --------------------------------------------------------------------------- #
def evaluate(
    *,
    augment_table: pd.DataFrame,
    new_columns: list[str],
    specs_by_name: dict[str, dict[str, Any]],
    subtype: str,
    query: str,
    focus: str | None,
    concept: str | None,
    source_columns: list[str],
    judge_model: str,
    judge_timeout: int,
    attempts: int,
    log_path: Path,
    no_llm_judge: bool = False,
) -> dict[str, Any]:
    columns_payload = charadh._columns_payload(new_columns, specs_by_name, augment_table)

    if no_llm_judge or not new_columns:
        judge = {"subtype": subtype, "per_column": [], "rationale": "no added columns or judge skipped"}
    else:
        prompt = build_prompt(
            subtype=subtype,
            query=query,
            focus=focus,
            concept=concept,
            source_columns=source_columns,
            columns_payload=columns_payload,
        )
        judge = semrec._invoke_judge(
            prompt, model=judge_model, timeout_s=judge_timeout, attempts=attempts, log_path=log_path
        )

    metrics = compute_metrics(subtype, judge, n_added=len(new_columns), new_columns=new_columns)
    return {
        "scorer": "B-2 characteristic adherence (per-subtype)",
        "subtype": subtype,
        "subtype_label": SUBTYPE_LABEL[subtype],
        "family": FAMILY_OF[subtype],
        "query": query,
        "focus_variable": focus,
        "concept": concept,
        "n_added_columns": len(new_columns),
        "added_columns": new_columns,
        "metrics": metrics,
        "judge": judge,
    }


# --------------------------------------------------------------------------- #
# CLI (single table)
# --------------------------------------------------------------------------- #
def _main() -> int:
    parser = argparse.ArgumentParser(description="B-2 per-subtype characteristic adherence of one augmented table.")
    parser.add_argument("--augment", required=True, type=Path)
    parser.add_argument("--specs", type=Path, default=None)
    parser.add_argument("--source", type=Path, default=None)
    parser.add_argument("--query", default="")
    parser.add_argument("--subtype", required=True, choices=list(SUBTYPES))
    parser.add_argument("--focus", default=None)
    parser.add_argument("--concept", default=None)
    parser.add_argument("--judge-model", default="claude-opus-4.8-xhigh")
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
        new_columns = semrec._source_new_columns(semrec._read_table(args.source), augment)
    else:
        new_columns = [str(c) for c in augment.columns]
    source_columns = [str(c) for c in augment.columns if str(c) not in set(map(str, new_columns))]

    report = evaluate(
        augment_table=augment,
        new_columns=[str(c) for c in new_columns],
        specs_by_name=specs_by_name,
        subtype=args.subtype,
        query=args.query,
        focus=args.focus,
        concept=args.concept,
        source_columns=source_columns,
        judge_model=args.judge_model,
        judge_timeout=args.judge_timeout,
        attempts=args.attempts,
        log_path=(args.out.parent if args.out else Path.cwd()) / "_b2_judge_call.json",
        no_llm_judge=args.no_llm_judge,
    )
    if args.out:
        semrec._write_json(args.out, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
