#!/usr/bin/env python3
"""Rebuild the paper's Experiment 1--5 tables without model calls.

Only Python's standard library is required. The script reads the archived raw
outputs under 3_experiments/*/raw/, writes freshly aggregated CSV files into
3_experiments/*/tables/, and verifies them against the paper-facing values.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import statistics
import sys
from collections import Counter, defaultdict
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


# Artifact layout. Each experiment owns one directory holding its raw per-item
# outputs (raw/) and its regenerated tables (tables/).
EXP_DIRS = {
    1: "3_experiments/exp1_end_to_end_utility",
    2: "3_experiments/exp2_analysis_form",
    3: "3_experiments/exp3_schema_suitability",
    4: "3_experiments/exp4_scale_and_grounding",
    5: "3_experiments/exp5_predictive_features",
}
SCOPE_CONFIG = "5_reference/configs/experiment_scope.json"
REPORT_DIR = "1_verify/report"


VARIANTS_4 = ("original", "skill_off", "skill_on", "skill_on_e2e")
VARIANTS_3 = ("skill_off", "skill_on", "skill_on_e2e")
CATEGORIES = (
    "C1_all_qualitative",
    "C2_text_qual_numeric_quant",
    "C3_text_augmented_quant",
)

EXPECTED_EXP1 = {
    "haiku": {"original": "-6.48", "skill_off": "-1.98", "skill_on": "1.38", "skill_on_e2e": "7.17"},
    "sonnet": {"original": "-4.60", "skill_off": "-5.29", "skill_on": "1.43", "skill_on_e2e": "8.45"},
}

EXPECTED_EXP2 = {
    ("haiku", "original"): ("23.1", "13.0", "63.9"),
    ("haiku", "skill_off"): ("0.0", "9.3", "90.7"),
    ("haiku", "skill_on"): ("0.0", "1.9", "98.1"),
    ("haiku", "skill_on_e2e"): ("0.0", "0.0", "100.0"),
    ("sonnet", "original"): ("27.8", "19.4", "52.8"),
    ("sonnet", "skill_off"): ("0.0", "9.3", "90.7"),
    ("sonnet", "skill_on"): ("0.9", "1.9", "97.2"),
    ("sonnet", "skill_on_e2e"): ("0.0", "0.0", "100.0"),
}

EXPECTED_EXP3 = {
    ("predictive_feature_engineering", "haiku"): ("0.32", "0.45", "0.37"),
    ("predictive_feature_engineering", "sonnet"): ("0.32", "0.47", "0.49"),
    ("exploratory_data_analysis", "haiku"): ("0.40", "0.70", "0.68"),
    ("exploratory_data_analysis", "sonnet"): ("0.31", "0.71", "0.66"),
    ("what_if", "haiku"): ("0.06", "0.38", "0.44"),
    ("what_if", "sonnet"): ("0.18", "0.39", "0.47"),
    ("causal_attribution", "haiku"): ("0.14", "0.34", "0.41"),
    ("causal_attribution", "sonnet"): ("0.30", "0.38", "0.47"),
    ("faceted_decomposition", "haiku"): ("0.13", "0.38", "0.43"),
    ("faceted_decomposition", "sonnet"): ("0.30", "0.36", "0.34"),
    ("focus_inference", "haiku"): ("0.60", "0.60", "0.60"),
    ("focus_inference", "sonnet"): ("0.63", "0.68", "0.65"),
}

EXPECTED_EXP4 = {
    "haiku__skill_off_update": (98100, "67.31", "19.70", "12.98"),
    "haiku__skill_on-v11": (70625, "72.66", "16.97", "10.29"),
    "haiku__skill_on_e2e-v11": (33639, "61.01", "26.59", "12.40"),
    "sonnet__skill_off_update": (125351, "30.76", "44.93", "24.29"),
    "sonnet__skill_on-v11": (95849, "73.78", "20.70", "5.47"),
    "sonnet__skill_on_e2e-v11": (47636, "76.48", "15.01", "8.50"),
}

EXP5_COLUMNS = (
    ("baseline_notext", "baseline", "xgb_results_{ds}_no_text.json"),
    ("haiku_skilloff_notext", "skill_off", "xgb_results_{ds}_no_text_haiku.json"),
    ("haiku_skillon_notext", "skill_on_e2e", "xgb_results_{ds}_no_text_haiku.json"),
    ("sonnet_skilloff_notext", "skill_off", "xgb_results_{ds}_no_text_sonnet.json"),
    ("sonnet_skillon_notext", "skill_on_e2e", "xgb_results_{ds}_no_text_sonnet.json"),
    ("baseline_text", "baseline", "xgb_results_{ds}_text_skrub_shap_k64.json"),
    ("haiku_skilloff_text", "skill_off", "xgb_results_{ds}_text_skrub_shap_haiku_k64.json"),
    ("haiku_skillon_text", "skill_on_e2e", "xgb_results_{ds}_text_skrub_shap_haiku_k64.json"),
    ("sonnet_skilloff_text", "skill_off", "xgb_results_{ds}_text_skrub_shap_sonnet_k64.json"),
    ("sonnet_skillon_text", "skill_on_e2e", "xgb_results_{ds}_text_skrub_shap_sonnet_k64.json"),
)


# Table 4(b): causal component signals, averaged over both substrates.
# Appendix Table 1: the remaining component signals, same averaging.
# (subtype, metric) -> {variant: paper value}
EXPECTED_EXP3_SIGNALS = {
    ("causal_attribution", "treatment_present"): ("Table 4(b)", {"skill_off": "0.84", "skill_on": "0.89", "skill_on_e2e": "1.00"}),
    ("causal_attribution", "confounder_present"): ("Table 4(b)", {"skill_off": "0.61", "skill_on": "0.84", "skill_on_e2e": "0.84"}),
    ("causal_attribution", "confounder_quality"): ("Table 4(b)", {"skill_off": "0.23", "skill_on": "0.41", "skill_on_e2e": "0.44"}),
    ("what_if", "treatment_present"): ("Table 4(b)", {"skill_off": "0.85", "skill_on": "0.91", "skill_on_e2e": "0.97"}),
    ("what_if", "confounder_present"): ("Table 4(b)", {"skill_off": "0.35", "skill_on": "0.85", "skill_on_e2e": "0.88"}),
    ("what_if", "confounder_quality"): ("Table 4(b)", {"skill_off": "0.17", "skill_on": "0.44", "skill_on_e2e": "0.49"}),
    ("exploratory_data_analysis", "predictor_fraction"): ("Appendix Table 1", {"skill_off": "0.55", "skill_on": "0.91", "skill_on_e2e": "0.89"}),
    ("exploratory_data_analysis", "interpretable_fraction"): ("Appendix Table 1", {"skill_off": "0.56", "skill_on": "0.96", "skill_on_e2e": "0.94"}),
    ("predictive_feature_engineering", "predictor_fraction"): ("Appendix Table 1", {"skill_off": "0.61", "skill_on": "0.73", "skill_on_e2e": "0.71"}),
    ("predictive_feature_engineering", "predictive_utility"): ("Appendix Table 1", {"skill_off": "0.47", "skill_on": "0.59", "skill_on_e2e": "0.56"}),
    ("predictive_feature_engineering", "leakage_rate"): ("Appendix Table 1", {"skill_off": "0.20", "skill_on": "0.18", "skill_on_e2e": "0.18"}),
    ("faceted_decomposition", "facet_fraction"): ("Appendix Table 1", {"skill_off": "0.37", "skill_on": "0.61", "skill_on_e2e": "0.65"}),
    ("faceted_decomposition", "mece"): ("Appendix Table 1", {"skill_off": "0.37", "skill_on": "0.50", "skill_on_e2e": "0.53"}),
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def mean_2dp_half_up(values: list[float]) -> str:
    """Mean rounded to two decimals, half away from zero.

    The paper rounds half up. One value (PFE `predictive_utility` under
    `skill_on_e2e`) has an exact mean of 0.555, so `f"{x:.2f}"` on the binary
    float gives 0.55 while the paper shows 0.56. Averaging exact fractions and
    rounding half up reproduces the paper for that value and leaves every other
    value unchanged.
    """
    if not values:
        raise ValueError("cannot average an empty list")
    total = sum(Fraction(str(v)) for v in values)
    exact = total / len(values)
    return str(
        (Decimal(exact.numerator) / Decimal(exact.denominator)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    )


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("cannot average an empty list")
    return statistics.fmean(values)


def reproduce_exp1(root: Path, excluded: set[str]) -> tuple[list[dict[str, Any]], list[str]]:
    source = root / EXP_DIRS[1] / "raw/bt"
    buckets: dict[tuple[str, str], list[float]] = defaultdict(list)
    files = 0
    for path in sorted(source.rglob("bt_4way.json")):
        dataset = path.relative_to(source).parts[0]
        if dataset in excluded:
            continue
        meta = read_json(path.parent / "meta.json")
        payload = read_json(path)
        for variant, value in (payload.get("bt_score") or {}).items():
            if variant in VARIANTS_4 and value is not None:
                buckets[(meta["model"], variant)].append(float(value))
        files += 1

    rows, failures = [], []
    for model in ("haiku", "sonnet"):
        for variant in VARIANTS_4:
            values = buckets[(model, variant)]
            value = mean(values)
            shown = f"{value:.2f}"
            expected = EXPECTED_EXP1[model][variant]
            passed = shown == expected
            if not passed:
                failures.append(f"exp1:{model}:{variant} expected={expected} actual={shown}")
            rows.append({
                "model": model,
                "condition": variant,
                "n": len(values),
                "mean_bt": f"{value:.6f}",
                "paper_value": expected,
                "status": "PASS" if passed else "FAIL",
            })
    rows.append({"model": "_meta", "condition": "input_bt_files", "n": files, "mean_bt": "", "paper_value": "", "status": ""})
    return rows, failures


def reproduce_exp2(root: Path, excluded: set[str]) -> tuple[list[dict[str, Any]], list[str]]:
    source = root / EXP_DIRS[2] / "raw/form_class"
    counts: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for path in sorted(source.rglob("*.json")):
        payload = read_json(path)
        if payload.get("dataset") in excluded:
            continue
        category = payload.get("category")
        if category in CATEGORIES:
            counts[(payload["model"], payload["variant"])][category] += 1

    rows, failures = [], []
    for model in ("haiku", "sonnet"):
        for variant in VARIANTS_4:
            counter = counts[(model, variant)]
            total = sum(counter.values())
            actual = tuple(f"{100 * counter[c] / total:.1f}" for c in CATEGORIES)
            expected = EXPECTED_EXP2[(model, variant)]
            passed = actual == expected
            if not passed:
                failures.append(f"exp2:{model}:{variant} expected={expected} actual={actual}")
            rows.append({
                "model": model,
                "condition": variant,
                "n": total,
                "C1_percent": actual[0],
                "C2_percent": actual[1],
                "C3_percent": actual[2],
                "status": "PASS" if passed else "FAIL",
            })
    return rows, failures


def variant_from_b2(path: Path) -> str | None:
    for variant in ("skill_on_e2e", "skill_off", "skill_on"):
        if path.name.endswith(f"__{variant}_b2.json"):
            return variant
    return None


def reproduce_exp3(
    root: Path, excluded: set[str], subtypes: list[str]
) -> tuple[list[dict[str, Any]], list[str]]:
    source = root / EXP_DIRS[3] / "raw/characteristic_adherence"
    buckets: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    for path in sorted(source.rglob("*_b2.json")):
        relative = path.relative_to(source)
        dataset, model = relative.parts[0], relative.parts[1]
        if dataset in excluded:
            continue
        variant = variant_from_b2(path)
        if variant is None:
            continue
        payload = read_json(path)
        buckets[(payload["subtype"], model, variant)].append(float(payload["metrics"]["adherence"]))

    rows, failures = [], []
    for subtype in subtypes:
        for model in ("haiku", "sonnet"):
            expected = EXPECTED_EXP3[(subtype, model)]
            row: dict[str, Any] = {"subtype": subtype, "model": model}
            actual = []
            for variant in VARIANTS_3:
                values = buckets[(subtype, model, variant)]
                value = mean(values)
                shown = f"{value:.2f}"
                row[f"{variant}_n"] = len(values)
                row[variant] = shown
                actual.append(shown)
            passed = tuple(actual) == expected
            row["status"] = "PASS" if passed else "FAIL"
            if not passed:
                failures.append(f"exp3:{subtype}:{model} expected={expected} actual={tuple(actual)}")
            rows.append(row)
    return rows, failures


def reproduce_exp3_signals(root: Path, excluded: set[str]) -> tuple[list[dict[str, Any]], list[str]]:
    """Table 4(b) and Appendix Table 1: the component signals behind adherence.

    Both are averaged over both substrates, so units from Haiku and Sonnet are
    pooled. Every metric here comes from the same `metrics` block of the same
    per-unit judge output that Table 4(a) is computed from.
    """
    source = root / EXP_DIRS[3] / "raw/characteristic_adherence"
    buckets: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    for path in sorted(source.rglob("*_b2.json")):
        if path.relative_to(source).parts[0] in excluded:
            continue
        variant = variant_from_b2(path)
        if variant is None:
            continue
        payload = read_json(path)
        subtype = payload["subtype"]
        for metric, value in (payload.get("metrics") or {}).items():
            # Booleans are included on purpose: the presence signals
            # (`treatment_present`, `confounder_present`) are per-unit booleans
            # that the paper reports as the fraction of units where they hold.
            if isinstance(value, (int, float, bool)):
                buckets[(subtype, variant, metric)].append(float(value))

    rows, failures = [], []
    for (subtype, metric), (where, expected_by_variant) in EXPECTED_EXP3_SIGNALS.items():
        row: dict[str, Any] = {"paper_table": where, "subtype": subtype, "signal": metric}
        actual, ok = [], True
        for variant in VARIANTS_3:
            values = buckets[(subtype, variant, metric)]
            shown = mean_2dp_half_up(values)
            expected = expected_by_variant[variant]
            row[f"{variant}_n"] = len(values)
            row[variant] = shown
            row[f"{variant}_paper"] = expected
            actual.append(shown)
            if shown != expected:
                ok = False
                failures.append(
                    f"exp3signals:{subtype}:{metric}:{variant} expected={expected} actual={shown}"
                )
        row["status"] = "PASS" if ok else "FAIL"
        rows.append(row)
    return rows, failures


def reproduce_exp4(root: Path, units: list[str]) -> tuple[list[dict[str, Any]], list[str]]:
    source = root / EXP_DIRS[4] / "raw/grounding/_cache/amazon_fine_food_review"
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    jsonl_files = 0
    for unit in units:
        paths = sorted((source / unit).glob("*/opus.jsonl")) or sorted((source / unit).glob("*/opus.jsonl.gz"))
        for path in paths:
            jsonl_files += 1
            variant = path.parent.name
            opener = (lambda p: gzip.open(p, "rt", encoding="utf-8")) if path.suffix == ".gz" else (
                lambda p: p.open(encoding="utf-8"))
            with opener(path) as handle:
                for line in handle:
                    if not line.strip():
                        continue
                    for result in (json.loads(line).get("verdicts") or {}).values():
                        counts[variant][str(result.get("verdict") or "").upper()] += 1

    rows, failures = [], []
    for variant in EXPECTED_EXP4:
        counter = counts[variant]
        total = sum(counter.values())
        percentages = tuple(f"{100 * counter[name] / total:.2f}" for name in ("SUPPORTED", "INFERABLE", "HALLUCINATED"))
        expected_total, *expected_pct = EXPECTED_EXP4[variant]
        passed = total == expected_total and percentages == tuple(expected_pct)
        if not passed:
            failures.append(
                f"exp4:{variant} expected={(expected_total, *expected_pct)} actual={(total, *percentages)}"
            )
        known = sum(counter[name] for name in ("SUPPORTED", "INFERABLE", "HALLUCINATED"))
        rows.append({
            "condition": variant,
            "cells": total,
            "supported_percent": percentages[0],
            "inferable_percent": percentages[1],
            "hallucinated_percent": percentages[2],
            "other_verdicts": total - known,
            "status": "PASS" if passed else "FAIL",
        })
    rows.append({"condition": "_meta_jsonl_files", "cells": jsonl_files, "supported_percent": "", "inferable_percent": "", "hallucinated_percent": "", "other_verdicts": "", "status": ""})
    return rows, failures


def xgb_metric(path: Path) -> tuple[float, float]:
    payload = read_json(path)
    means, stds = [], []
    for run in payload.values():
        for dataset_result in run.values():
            for result in (dataset_result.get("xgb") or {}).values():
                means.append(float(result["mean"]["accuracy"]))
                stds.append(float(result["std"]["accuracy"]))
    return mean(means), mean(stds)


def reproduce_exp5(root: Path, datasets: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    source = root / EXP_DIRS[5] / "raw/xgboost"
    summary_path = root / EXP_DIRS[5] / "tables/summary_v11_update_k64.csv"
    expected_rows = {row["dataset"]: row for row in csv.DictReader(summary_path.open(encoding="utf-8"))}
    no_text_rows, text_rows, failures = [], [], []

    for dataset in datasets:
        expected = expected_rows[dataset]
        calculated: dict[str, tuple[float, float]] = {}
        for column, variant, filename in EXP5_COLUMNS:
            result_path = source / dataset / variant / filename.format(ds=dataset)
            calculated[column] = xgb_metric(result_path)
            actual_mean, actual_std = calculated[column]
            if f"{actual_mean:.4f}" != expected[column] or f"{actual_std:.4f}" != expected[f"{column}_std"]:
                failures.append(
                    f"exp5:{dataset}:{column} expected=({expected[column]},{expected[f'{column}_std']}) "
                    f"actual=({actual_mean:.4f},{actual_std:.4f})"
                )

        base = {"dataset": dataset, "task": expected["task"]}
        no_text = dict(base)
        text = dict(base)
        for column, _, _ in EXP5_COLUMNS:
            value, std = calculated[column]
            target = no_text if column.endswith("_notext") else text
            clean = column.removesuffix("_notext").removesuffix("_text")
            target[f"{clean}_mean"] = f"{value:.4f}"
            target[f"{clean}_std"] = f"{std:.4f}"
        no_text["status"] = "PASS" if not any(x.startswith(f"exp5:{dataset}:") for x in failures) else "FAIL"
        text["status"] = no_text["status"]
        no_text_rows.append(no_text)
        text_rows.append(text)
    return no_text_rows, text_rows, failures


def markdown_report(checks: dict[str, dict[str, Any]]) -> str:
    lines = [
        "# Paper Result Reproduction Report",
        "",
        "This report was generated exclusively from archived raw outputs. No model was called.",
        "",
        "| Experiment | Paper location | Status | Checked values |",
        "|---|---|---:|---:|",
    ]
    order = (
        "experiment_1", "experiment_2", "experiment_3",
        "experiment_3_signals", "experiment_4", "experiment_5",
    )
    total = 0
    for name in order:
        block = checks[name]
        total += block["checked"]
        label = name.replace("_", " ").title().replace("Experiment 3 Signals", "Experiment 3 (signals)")
        lines.append(f"| {label} | {block['paper']} | {block['status']} | {block['checked']} |")
    lines.extend([
        f"| **Total** | | **{checks['overall']['status']}** | **{total}** |",
        "",
        f"Overall: **{checks['overall']['status']}**",
        "",
        "Paper scope: Experiments 1--3 exclude `airlines_review_full`; Experiment 4 uses the two common units; Experiment 5 excludes `mercari` and uses SHAP top-k=64 for the embedding table.",
        "",
    ])
    failures = checks["overall"]["failures"]
    if failures:
        lines.extend(["## Failures", ""] + [f"- {item}" for item in failures] + [""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    config = read_json(root / SCOPE_CONFIG)
    excluded = set(config["exclude_datasets_exp1_to_exp3"])

    exp1, fail1 = reproduce_exp1(root, excluded)
    exp2, fail2 = reproduce_exp2(root, excluded)
    exp3, fail3 = reproduce_exp3(root, excluded, config["experiment_3_subtypes"])
    exp3s, fail3s = reproduce_exp3_signals(root, excluded)
    exp4, fail4 = reproduce_exp4(root, config["experiment_4_common_units"])
    exp5_no_text, exp5_text, fail5 = reproduce_exp5(root, config["experiment_5_datasets"])

    report = root / REPORT_DIR
    write_csv(root / EXP_DIRS[1] / "tables/exp1_bt.csv", ["model", "condition", "n", "mean_bt", "paper_value", "status"], exp1)
    write_csv(root / EXP_DIRS[2] / "tables/exp2_form.csv", ["model", "condition", "n", "C1_percent", "C2_percent", "C3_percent", "status"], exp2)
    write_csv(root / EXP_DIRS[3] / "tables/exp3_table4a.csv", ["subtype", "model", "skill_off_n", "skill_off", "skill_on_n", "skill_on", "skill_on_e2e_n", "skill_on_e2e", "status"], exp3)
    signal_fields = ["paper_table", "subtype", "signal"]
    for variant in VARIANTS_3:
        signal_fields.extend([f"{variant}_n", variant, f"{variant}_paper"])
    signal_fields.append("status")
    write_csv(root / EXP_DIRS[3] / "tables/exp3_table4b_and_appendix_table1.csv", signal_fields, exp3s)
    write_csv(root / EXP_DIRS[4] / "tables/exp4_grounding.csv", ["condition", "cells", "supported_percent", "inferable_percent", "hallucinated_percent", "other_verdicts", "status"], exp4)

    exp5_fields = ["dataset", "task"]
    for prefix in ("baseline", "haiku_skilloff", "haiku_skillon", "sonnet_skilloff", "sonnet_skillon"):
        exp5_fields.extend([f"{prefix}_mean", f"{prefix}_std"])
    exp5_fields.append("status")
    write_csv(root / EXP_DIRS[5] / "tables/table5_no_text.csv", exp5_fields, exp5_no_text)
    write_csv(root / EXP_DIRS[5] / "tables/table6_text_k64.csv", exp5_fields, exp5_text)

    all_failures = fail1 + fail2 + fail3 + fail3s + fail4 + fail5
    n_signals = 3 * len(EXPECTED_EXP3_SIGNALS)
    checks = {
        "experiment_1": {"status": "PASS" if not fail1 else "FAIL", "checked": 8, "paper": "Table 2", "failures": fail1},
        "experiment_2": {"status": "PASS" if not fail2 else "FAIL", "checked": 24, "paper": "Table 3", "failures": fail2},
        "experiment_3": {"status": "PASS" if not fail3 else "FAIL", "checked": 36, "paper": "Table 4(a)", "failures": fail3},
        "experiment_3_signals": {"status": "PASS" if not fail3s else "FAIL", "checked": n_signals, "paper": "Table 4(b) + Appendix Table 1", "failures": fail3s},
        "experiment_4": {"status": "PASS" if not fail4 else "FAIL", "checked": 18, "paper": "Section 5.5 prose", "failures": fail4},
        "experiment_5": {"status": "PASS" if not fail5 else "FAIL", "checked": 110, "paper": "Tables 5-6", "failures": fail5},
        "overall": {"status": "PASS" if not all_failures else "FAIL", "failures": all_failures},
    }
    (report / "verification.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (report / "REPRODUCTION_REPORT.md").write_text(markdown_report(checks), encoding="utf-8")
    print(f"Reproduction status: {checks['overall']['status']}")
    print(f"Report: {report / 'REPRODUCTION_REPORT.md'}")
    return 0 if not all_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
