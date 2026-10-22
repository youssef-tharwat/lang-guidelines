#!/usr/bin/env bash
# A/B a skill on its eval cases (evals/<skill>/cases).
#
#   evals/run-ab.sh <skill> <before-skill-dir> <output-dir>
#   evals/run-ab.sh rust-guidelines /tmp/old-rust-guidelines /tmp/ab-rust
#
# "before" is any earlier copy of the skill folder; "after" is <skill>/ in this working
# tree. Each arm runs from a scratch copy with the cases placed in its evals/, so the
# published skill folder never ships them. The no-skill baseline runs once, alongside the
# before arm. Env: RUNS (default 3), MODEL (default claude-opus-5-5), MAX_COST_USD per arm
# (default 40), CONCURRENCY (default 4), CASES (space-separated case names; default all).
#
# --keep-temp is required: token counts come from each run's trace. The kept
# directories land in $TMPDIR as e-*; remove them once compare.py has run.
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
root=$(cd "$here/.." && pwd)
skill=$1
before=$(cd "$2" && pwd)
out=$(mkdir -p "$3" && cd "$3" && pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

stage() { # <arm> <skill-dir>
  cp -R "$2" "$work/$1"
  mkdir -p "$work/$1/evals"
  local cases=${CASES:-$(ls "$here/$skill/cases")}
  for case in $cases; do
    cp -R "$here/$skill/cases/$case" "$work/$1/evals/$case"
  done
}

run_arm() { # <arm> <ablation>
  (cd "$work/$1" && claude plugin eval . \
    --ablation "$2" --runs "${RUNS:-3}" --model "${MODEL:-claude-opus-5-5}" \
    --allow-tools Write --keep-temp --no-publish --trust-plugin --concurrency "${CONCURRENCY:-4}" \
    --threshold 0 --max-cost-usd "${MAX_COST_USD:-40}" --output-dir "$out/$1")
}

stage before "$before"
stage after "$root/$skill"
run_arm before with-without
run_arm after none
python3 "$here/compare.py" "$out/before/aggregate-result.json" "$out/after/aggregate-result.json"
