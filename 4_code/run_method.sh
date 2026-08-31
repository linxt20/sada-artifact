#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: UPSTREAM_ROOT=/path/to/full/repository 4_code/run_method.sh <exp1_reports|exp3_augmentation|exp5_augmentation|exp5_evaluate|exp5_k64> [args...]

These commands invoke model-dependent generation code from a complete upstream
checkout. The compact artifact does not include all source datasets or model credentials.
EOF
}

if [[ $# -lt 1 ]]; then usage; exit 2; fi
: "${UPSTREAM_ROOT:?Set UPSTREAM_ROOT to the full repository root containing benchmark/ and TextTabBench/}"
ARTIFACT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

select_upstream_script() {
  local first="$1"
  local second="$2"
  if [[ -f "$first" ]]; then
    printf '%s\n' "$first"
  elif [[ -f "$second" ]]; then
    printf '%s\n' "$second"
  else
    echo "Missing upstream script: $first or $second" >&2
    exit 1
  fi
}

task="$1"
shift
case "$task" in
  exp1_reports)
    script="$(select_upstream_script "$UPSTREAM_ROOT/benchmark/_gen_update_reports.py" "$UPSTREAM_ROOT/benchmark/gen_update_reports.py")"
    exec python3 "$script" "$@"
    ;;
  exp3_augmentation)
    script="$(select_upstream_script "$UPSTREAM_ROOT/benchmark/_run_v11_update.py" "$UPSTREAM_ROOT/benchmark/run_v11_update.py")"
    exec python3 "$script" "$@"
    ;;
  exp5_augmentation)
    exec env \
      TEXTTABBENCH_ROOT="$UPSTREAM_ROOT/TextTabBench" \
      SADA_TAPP="$ARTIFACT_ROOT/2_operator/scripts/run_tapp.py" \
      python3 "$ARTIFACT_ROOT/4_code/TextTabBench/augment_process_result_v11_update/run_skillon_e2e_linux.py" "$@"
    ;;
  exp5_evaluate)
    exec env TEXTTABBENCH_ROOT="$UPSTREAM_ROOT/TextTabBench" \
      python3 "$ARTIFACT_ROOT/4_code/TextTabBench/augment_process_result_v11_update/eval_5seed.py" "$@"
    ;;
  exp5_k64)
    exec env TEXTTABBENCH_ROOT="$UPSTREAM_ROOT/TextTabBench" \
      python3 "$ARTIFACT_ROOT/4_code/TextTabBench/augment_process_result_v11_update/rerun_k64.py" "$@"
    ;;
  *)
    usage
    exit 2
    ;;
esac
