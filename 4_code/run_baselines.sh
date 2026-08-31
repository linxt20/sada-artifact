#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: UPSTREAM_ROOT=/path/to/full/repository 4_code/run_baselines.sh <exp4_skill_off|exp5_skill_off> [args...]

Baseline generation requires the complete upstream data layout and model access.
EOF
}

if [[ $# -lt 1 ]]; then usage; exit 2; fi
: "${UPSTREAM_ROOT:?Set UPSTREAM_ROOT to the full repository root containing benchmark/ and TextTabBench/}"
ARTIFACT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

task="$1"
shift
case "$task" in
  exp4_skill_off)
    exec python3 "$UPSTREAM_ROOT/benchmark/augmenter/run_skill_off_agentic_augment.py" "$@"
    ;;
  exp5_skill_off)
    exec env TEXTTABBENCH_ROOT="$UPSTREAM_ROOT/TextTabBench" \
      python3 "$ARTIFACT_ROOT/4_code/TextTabBench/augment_process_result_v11_update/run_skilloff_augment.py" "$@"
    ;;
  *)
    usage
    exit 2
    ;;
esac
