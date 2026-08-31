"""One-off merge: fold the fair2 focus_internal_structure results into
``final_result`` so it holds a complete three-category evaluation.

- Copies every fair2 concept-scenario result tree (per-scenario ``_concept.json``
  plus ``<model>/<variant>_characteristic.json``) into ``final_result``,
  overwriting the stale fair-method concept results left there.
- Rebuilds ``final_result/SUMMARY.json`` and ``SUMMARY.md`` combining the causal
  + correlational aggregates (already in final_result) with the fair2
  focus_internal_structure aggregates.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FINAL = ROOT / "final_result"
FAIR2 = ROOT / "characteristic_evaluation_fair2_regen"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _copy_concept_results() -> int:
    copied = 0
    for scenario_dir in sorted(p for p in FAIR2.iterdir() if p.is_dir()):
        dst = FINAL / scenario_dir.name
        shutil.copytree(scenario_dir, dst, dirs_exist_ok=True)
        copied += 1
    return copied


def _fmt(v) -> str:
    return "" if v is None else (f"{v}" if not isinstance(v, float) else f"{round(v, 4)}")


def _causal_table(by_cat: dict) -> list[str]:
    a = by_cat.get("causal_relation", {})
    lines = [
        "## Causal relation (treatment + confounders)",
        "",
        "| Variant | n | Adherence | Treatment-present | Confounder-present | Mean #conf | Conf. quality |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for v in ("skill_off", "skill_on", "skill_on_e2e"):
        r = a.get(v)
        if not r:
            continue
        lines.append(
            f"| {v} | {r['n']} | {_fmt(r.get('adherence'))} | {_fmt(r.get('treatment_present_rate'))} | "
            f"{_fmt(r.get('confounder_present_rate'))} | {_fmt(r.get('mean_n_confounders'))} | {_fmt(r.get('confounder_quality'))} |"
        )
    lines.append("")
    return lines


def _focus_relation_table(by_cat: dict) -> list[str]:
    a = by_cat.get("focus_relation", {})
    lines = [
        "## Focus relation (correlational X)",
        "",
        "| Variant | n | Adherence | Predictor fraction |",
        "| --- | ---: | ---: | ---: |",
    ]
    for v in ("skill_off", "skill_on", "skill_on_e2e"):
        r = a.get(v)
        if not r:
            continue
        lines.append(f"| {v} | {r['n']} | {_fmt(r.get('adherence'))} | {_fmt(r.get('predictor_fraction'))} |")
    lines.append("")
    return lines


def _focus_internal_tables(by_cat_model: dict) -> list[str]:
    models = ("substrate-claude-haiku-4-5", "substrate-claude-sonnet-4-6")
    lines: list[str] = []

    inf = by_cat_model.get("focus_inference", {})
    if inf:
        lines += [
            "## Focus internal structure / focus inference (no given focus)",
            "",
            "| Model | Variant | n | Adherence | Focus coherence | Structure quality | Redundancy |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
        for m in models:
            for v in ("skill_off", "skill_on", "skill_on_e2e"):
                r = inf.get(m, {}).get(v)
                if not r:
                    continue
                lines.append(
                    f"| {m} | {v} | {r['n']} | {_fmt(r.get('adherence'))} | {_fmt(r.get('focus_coherence'))} | "
                    f"{_fmt(r.get('structure_quality'))} | {_fmt(r.get('redundancy'))} |"
                )
        lines.append("")

    fac = by_cat_model.get("focus_internal_structure", {})
    if fac:
        lines += [
            "## Focus internal structure / faceted decomposition (query-inferred concept)",
            "",
            "| Model | Variant | n | Adherence | Facet fraction | Coverage | Redundancy |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
        for m in models:
            for v in ("skill_off", "skill_on", "skill_on_e2e"):
                r = fac.get(m, {}).get(v)
                if not r:
                    continue
                lines.append(
                    f"| {m} | {v} | {r['n']} | {_fmt(r.get('adherence'))} | {_fmt(r.get('facet_fraction'))} | "
                    f"{_fmt(r.get('coverage'))} | {_fmt(r.get('redundancy'))} |"
                )
        lines.append("")
    return lines


def main() -> int:
    n = _copy_concept_results()
    final_sum = _load(FINAL / "SUMMARY.json")
    fair2_sum = _load(FAIR2 / "SUMMARY.json")

    by_cat = final_sum.get("by_category", {})
    by_cat_model = fair2_sum.get("by_category_model", {})

    merged = {
        "updated_at": final_sum.get("updated_at"),
        "note": "Three-category final: causal+correlational from fair (regenerated skill_off); "
                "focus_internal_structure from fair2 concept-inference method.",
        "by_category": by_cat,
        "focus_internal_structure_by_model": by_cat_model,
        "n_reports_causal_correlational": final_sum.get("n_reports"),
        "n_reports_focus_internal": fair2_sum.get("n_reports"),
    }
    (FINAL / "SUMMARY.json").write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")

    md = ["# Characteristic Adherence -- Final (three categories, regenerated skill_off)", ""]
    md += _causal_table(by_cat)
    md += _focus_relation_table(by_cat)
    md += _focus_internal_tables(by_cat_model)
    (FINAL / "SUMMARY.md").write_text("\n".join(md), encoding="utf-8")

    print(f"Merged {n} concept scenario dirs into final_result; SUMMARY rebuilt with three categories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
