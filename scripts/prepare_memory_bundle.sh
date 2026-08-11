#!/usr/bin/env bash
# Prepares the memory bundle used by backend-swap experiments.

set -Eeuo pipefail
shopt -s inherit_errexit 2>/dev/null || true

PYTHON_EXE="${PYTHON_EXE:-./.venv/bin/python}"
OUT_DIR="${OUT_DIR:-data/experiments}"
EXPERIMENT_ID="${EXPERIMENT_ID:-phase_a1_backend_a_train_mem}"
REPETITIONS="${REPETITIONS:-5}"
EPISODES="${EPISODES:-40}"
BASE_SEED="${BASE_SEED:-1337}"
SEED_STEP="${SEED_STEP:-100}"
BENIGN_RATE="${BENIGN_RATE:-0.35}"
NOISE_PER_EPISODE="${NOISE_PER_EPISODE:-2000}"
MAX_WORKERS="${MAX_WORKERS:-1}"

[[ -x "$PYTHON_EXE" ]] || { echo "Python not found at $PYTHON_EXE" >&2; exit 1; }

ts() { date -u +"%Y%m%d_%H%M%S"; }

EMPTY_SEED_DIR="$OUT_DIR/_memory_seed_empty_$(ts)"
mkdir -p "$EMPTY_SEED_DIR"

"$PYTHON_EXE" -m src.eval.run_experiments \
  --experiment-id "$EXPERIMENT_ID" \
  --repetitions "$REPETITIONS" \
  --episodes "$EPISODES" \
  --base-seed "$BASE_SEED" \
  --seed-step "$SEED_STEP" \
  --benign-rate "$BENIGN_RATE" \
  --noise-per-episode "$NOISE_PER_EPISODE" \
  --memory-seed-dir "$EMPTY_SEED_DIR" \
  --out-dir "$OUT_DIR" \
  --blue-backend backend_a \
  --blue-schema-mapper static \
  --mcp-enabled \
  --max-workers "$MAX_WORKERS"

"$PYTHON_EXE" -m src.eval.aggregate_results --manifest "$OUT_DIR/$EXPERIMENT_ID/manifest.json"

BUNDLE="$OUT_DIR/_memory_seed_bundle_${EXPERIMENT_ID}_$(ts)"
mkdir -p "$BUNDLE"

for rep in $(seq 1 "$REPETITIONS"); do
  rep_name=$(printf "rep_%02d" "$rep")
  src=""
  for root in data/runs data/experiments/_runs; do
    candidate="$root/blue_mem_${EXPERIMENT_ID}_${rep_name}/memory"
    if [[ -d "$candidate" ]]; then src="$candidate"; break; fi
  done
  [[ -n "$src" ]] || { echo "Missing trained memory for $rep_name" >&2; exit 1; }
  mkdir -p "$BUNDLE/$rep_name"
  for name in cases.jsonl index.faiss; do
    [[ -f "$src/$name" ]] && cp -f "$src/$name" "$BUNDLE/$rep_name/$name"
  done
done

echo "$BUNDLE"
