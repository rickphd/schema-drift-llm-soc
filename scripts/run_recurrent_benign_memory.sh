#!/usr/bin/env bash
# Paired RQ4 experiment for recurrent benign traffic.
# The control disables both FAISS retrieval and online memory updates.

set -Eeuo pipefail
shopt -s inherit_errexit 2>/dev/null || true

PYTHON_EXE="${PYTHON_EXE:-./.venv/bin/python}"
OUT_DIR="${OUT_DIR:-data/rq4_qwen_paired}"
EXPERIMENT_TAG="${EXPERIMENT_TAG:-qwen3_8b_paired_v1}"
REPETITIONS="${REPETITIONS:-5}"
EPISODES="${EPISODES:-20}"
TRAIN_BASE_SEED="${TRAIN_BASE_SEED:-1337}"
EVAL_BASE_SEED="${EVAL_BASE_SEED:-11337}"
SEED_STEP="${SEED_STEP:-100}"
BENIGN_RATE="${BENIGN_RATE:-1.0}"
RECURRENT_BENIGN_RATE="${RECURRENT_BENIGN_RATE:-1.0}"
RECURRENT_BENIGN_PROFILES="${RECURRENT_BENIGN_PROFILES:-3}"
NOISE_PER_EPISODE="${NOISE_PER_EPISODE:-2000}"
MAX_WORKERS="${MAX_WORKERS:-1}"
LLM_PROVIDER="${LLM_PROVIDER:-ollama}"
OLLAMA_URL="${OLLAMA_URL:-http://127.0.0.1:11434}"
OLLAMA_MODEL="${OLLAMA_MODEL:-qwen3:8b}"
RUNS_DIR="${RUNS_DIR:-$OUT_DIR/_runs}"
PAPER_AHMED_FORCE_CPU="${PAPER_AHMED_FORCE_CPU:-1}"

[[ -x "$PYTHON_EXE" ]] || { echo "Python not found at $PYTHON_EXE" >&2; exit 1; }
mkdir -p "$RUNS_DIR"
export CYBER_RANGE_RUNS_DIR="$RUNS_DIR"
export PAPER_AHMED_FORCE_CPU

tag_id() {
  if [[ -z "$EXPERIMENT_TAG" ]]; then echo "$1"; else echo "${1}_${EXPERIMENT_TAG}"; fi
}
ts() { date -u +"%Y%m%d_%H%M%S"; }

EMPTY_SEED_DIR="$OUT_DIR/_memory_seed_empty_recurrent_$(ts)"
mkdir -p "$EMPTY_SEED_DIR"

run_step() {
  local exp_id="$1"; shift
  local base_seed="$1"; shift
  local memory_dir="$1"; shift
  local memory_enabled="$1"; shift
  local memory_flag="--memory-enabled"
  if [[ "$memory_enabled" != "1" ]]; then
    memory_flag="--no-memory"
  fi
  "$PYTHON_EXE" -m src.eval.run_experiments \
    --experiment-id "$exp_id" \
    --repetitions "$REPETITIONS" \
    --episodes "$EPISODES" \
    --base-seed "$base_seed" \
    --seed-step "$SEED_STEP" \
    --benign-rate "$BENIGN_RATE" \
    --recurrent-benign-rate "$RECURRENT_BENIGN_RATE" \
    --recurrent-benign-profiles "$RECURRENT_BENIGN_PROFILES" \
    --noise-per-episode "$NOISE_PER_EPISODE" \
    --out-dir "$OUT_DIR" \
    --memory-seed-dir "$memory_dir" \
    --blue-backend backend_a \
    --blue-schema-mapper static \
    --mcp-enabled \
    --llm-provider "$LLM_PROVIDER" \
    --ollama-url "$OLLAMA_URL" \
    --ollama-model "$OLLAMA_MODEL" \
    --no-llm-prewarm \
    --max-workers "$MAX_WORKERS" \
    "$memory_flag"
  "$PYTHON_EXE" -m src.eval.aggregate_results --manifest "$OUT_DIR/$exp_id/manifest.json"
}

bundle_memory_from() {
  local source_id="$1"
  local bundle="$OUT_DIR/_memory_seed_bundle_${source_id}_$(ts)"
  mkdir -p "$bundle"
  local runs_roots=()
  if [[ -n "${CYBER_RANGE_RUNS_DIR:-}" ]]; then
    runs_roots+=("$CYBER_RANGE_RUNS_DIR")
  fi
  runs_roots+=("data/runs" "data/experiments/_runs")
  for rep in $(seq 1 "$REPETITIONS"); do
    local rep_name=$(printf "rep_%02d" "$rep")
    local src=""
    for root in "${runs_roots[@]}"; do
      local candidate="$root/blue_mem_${source_id}_${rep_name}/memory"
      if [[ -d "$candidate" ]]; then src="$candidate"; break; fi
    done
    [[ -n "$src" ]] || { echo "Missing trained memory for $rep_name (searched: ${runs_roots[*]})" >&2; exit 1; }
    mkdir -p "$bundle/$rep_name"
    for name in cases.jsonl index.faiss; do
      [[ -f "$src/$name" ]] && cp -f "$src/$name" "$bundle/$rep_name/$name"
    done
  done
  echo "$bundle"
}

analyze_recurrent() {
  local exp_id="$1"; shift
  local out_name="$1"; shift
  "$PYTHON_EXE" -m src.eval.analyze_recurrent_benign \
    --manifest "$OUT_DIR/$exp_id/manifest.json" \
    --out-csv "$OUT_DIR/$exp_id/${out_name}.csv" \
    --out-summary-csv "$OUT_DIR/$exp_id/${out_name}_summary.csv"
}

TRAIN_ID=$(tag_id recurrent_benign_train_mem)
EVAL_NO_MEM_ID=$(tag_id recurrent_benign_eval_nomem)
EVAL_WITH_MEM_ID=$(tag_id recurrent_benign_eval_withmem)

run_step "$TRAIN_ID" "$TRAIN_BASE_SEED" "$EMPTY_SEED_DIR" 1
MEMORY_BUNDLE=$(bundle_memory_from "$TRAIN_ID")
echo "Memory bundle: $MEMORY_BUNDLE"

run_step "$EVAL_NO_MEM_ID" "$EVAL_BASE_SEED" "$EMPTY_SEED_DIR" 0
analyze_recurrent "$EVAL_NO_MEM_ID" "recurrent_benign_analysis_nomem"

run_step "$EVAL_WITH_MEM_ID" "$EVAL_BASE_SEED" "$MEMORY_BUNDLE" 1
analyze_recurrent "$EVAL_WITH_MEM_ID" "recurrent_benign_analysis_withmem"

echo ""
echo "Done."
echo "  $OUT_DIR/$EVAL_NO_MEM_ID/recurrent_benign_analysis_nomem_summary.csv"
echo "  $OUT_DIR/$EVAL_WITH_MEM_ID/recurrent_benign_analysis_withmem_summary.csv"
