#!/usr/bin/env bash
# Unpack every per-unit tagging-trace archive in place.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
for a in substrate-*/*.tar.gz; do
  sub="$(dirname "$a")"
  echo "extracting $a"
  tar xzf "$a" -C "$sub"
done
echo "done: $(find . -type f -name '*.json' | wc -l) trace files"
