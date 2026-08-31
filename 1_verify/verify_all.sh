#!/usr/bin/env bash
# Offline reproduction of the paper's Experiment 1-5 tables. No model calls, no
# network, Python standard library only.
set -euo pipefail

ARTIFACT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ARTIFACT_ROOT/1_verify/reproduce_paper_results.py" --root "$ARTIFACT_ROOT" "$@"
