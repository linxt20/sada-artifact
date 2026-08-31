#!/usr/bin/env python3
"""Audit an upstream checkout for inputs needed to rerun Experiments 1--5."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


EXP5_DATASETS = (
    "airbnb", "beer", "laptops", "sf_permits", "wine",
    "customer_complaints", "hs_cards", "job_frauds", "kickstarter",
    "osha_accidents", "spotify",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    root = args.upstream_root.resolve()

    checks = {
        "benchmark_augment_table": root / "benchmark/augment_table",
        "benchmark_gt_annotations": root / "benchmark/gt_annotations",
        "benchmark_dataset_portion_1": root / "benchmark/dataset_portion_1",
        "benchmark_dataset_portion_2": root / "benchmark/dataset_portion_2",
        "texttabbench_raw_data": root / "TextTabBench/datasets_notebooks/datasets_files/raw",
        "texttabbench_result_inputs": root / "TextTabBench/augment_process_result_v11_update",
        "texttabbench_pipeline": root / "TextTabBench/pipelines/main_pipeline.py",
    }
    report = {
        "upstream_root": str(root),
        "required_paths": {name: {"path": str(path), "exists": path.exists()} for name, path in checks.items()},
        "experiment_5_processed_pickles": {},
    }
    raw_root = checks["texttabbench_raw_data"]
    for dataset in EXP5_DATASETS:
        matches = sorted(str(path) for path in raw_root.rglob(f"{dataset}_processed.pkl")) if raw_root.exists() else []
        report["experiment_5_processed_pickles"][dataset] = matches

    complete = all(item["exists"] for item in report["required_paths"].values()) and all(
        report["experiment_5_processed_pickles"].values()
    )
    report["complete"] = complete
    output = args.output or Path(__file__).resolve().parent / "data_manifest.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Input audit: {'PASS' if complete else 'INCOMPLETE'}")
    print(f"Manifest: {output}")
    return 0 if complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
