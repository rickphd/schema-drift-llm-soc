#!/usr/bin/env bash
# Minimal-alias contrast across three LLM providers.
#
# Forces dynamic LLM invocation by restricting backend_b aliases to critical
# fields only. The protocol evaluates schema normalization under the controlled
# backend swap used in the paper.
#
# Reuses a trained memory bundle via TRAINED_MEM.

set -Eeuo pipefail
shopt -s inherit_errexit 2>/dev/null || true

PYTHON_EXE="${PYTHON_EXE:-./.venv/bin/python}"
OUT_DIR="${OUT_DIR:-data/wave_b_minimal}"
EXPERIMENT_TAG="${EXPERIMENT_TAG:-minimal}"
REPETITIONS="${REPETITIONS:-5}"
ROBUST_REPETITIONS="${ROBUST_REPETITIONS:-10}"
EPISODES="${EPISODES:-40}"
BASE_SEED="${BASE_SEED:-1337}"
TRAIN_EVAL_SEED_OFFSET="${TRAIN_EVAL_SEED_OFFSET:-10000}"
SEED_STEP="${SEED_STEP:-100}"
BENIGN_RATE="${BENIGN_RATE:-0.35}"
NOISE_PER_EPISODE="${NOISE_PER_EPISODE:-2000}"
DRIFT_PROFILE="${DRIFT_PROFILE:-hard4}"
SCHEMA_MIN_CONF="${SCHEMA_MIN_CONF:-0.70}"
LLM_TIMEOUT_SEC="${LLM_TIMEOUT_SEC:-30.0}"

GEMINI_MODEL="${GEMINI_MODEL:-gemini-2.5-flash}"
ANTHROPIC_MODEL="${ANTHROPIC_MODEL:-claude-haiku-4-5}"
OLLAMA_URL="${OLLAMA_URL:-http://127.0.0.1:11434}"
OLLAMA_MODEL="${OLLAMA_MODEL:-qwen3:8b}"

MAX_WORKERS_API="${MAX_WORKERS_API:-2}"
TRAINED_MEM="${TRAINED_MEM:-}"

# Phase selectors — set to "0" to skip
RUN_GEMINI="${RUN_GEMINI:-1}"
RUN_ANTHROPIC="${RUN_ANTHROPIC:-1}"
RUN_QWEN="${RUN_QWEN:-1}"
INCLUDE_ROBUST="${INCLUDE_ROBUST:-1}"
# Optional: clear shared schema caches so each model is forced to call its LLM
# from a cold state. Default 0 (reuse cache for production-realistic behavior).
RESET_SCHEMA_CACHE="${RESET_SCHEMA_CACHE:-0}"

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------
[[ -x "$PYTHON_EXE" ]] || { echo "ERROR: Python not found at $PYTHON_EXE" >&2; exit 1; }
[[ -n "$TRAINED_MEM" && -d "$TRAINED_MEM" ]] || {
  echo "ERROR: TRAINED_MEM must point to an existing memory bundle dir." >&2
  echo "  Example: TRAINED_MEM=data/ola3_anthropic/_memory_seed_bundle_phase_train_mem_anthropic_haiku_45_manual" >&2
  exit 1
}

ENV_FILE="${ENV_FILE:-$PWD/.env}"
key_present() {
  local name="$1"
  local current
  current="$(eval echo \"\${$name:-}\")"
  if [[ -n "$current" ]]; then return 0; fi
  grep -q "^${name}=." "$ENV_FILE" 2>/dev/null
}

[[ "$RUN_GEMINI"    != "1" ]] || key_present GEMINI_API_KEY    || { echo "ERROR: GEMINI_API_KEY missing in env and .env"    >&2; exit 1; }
[[ "$RUN_ANTHROPIC" != "1" ]] || key_present ANTHROPIC_API_KEY || { echo "ERROR: ANTHROPIC_API_KEY missing in env and .env" >&2; exit 1; }
if [[ "$RUN_QWEN" == "1" ]]; then
  curl -fsS --max-time 5 "$OLLAMA_URL/api/tags" >/dev/null || {
    echo "ERROR: Ollama daemon not reachable at $OLLAMA_URL" >&2; exit 1; }
  # Sanity-check that qwen3:8b is locally available
  if ! curl -fsS "$OLLAMA_URL/api/tags" | grep -q "\"$OLLAMA_MODEL\""; then
    echo "ERROR: Model $OLLAMA_MODEL not pulled. Run: ollama pull $OLLAMA_MODEL" >&2
    exit 1
  fi
fi

if [[ "$RESET_SCHEMA_CACHE" == "1" ]]; then
  echo "Clearing shared schema caches for minimal-alias keys..."
  find data/experiments/_shared_schema_cache -name "schema_map_cache_shared_*_minimal.json" -delete 2>/dev/null || true
fi

tag_id() { echo "${1}_${EXPERIMENT_TAG}"; }

SWAP_EPISODE=$(( EPISODES / 2 ))
[[ $SWAP_EPISODE -lt 1 ]] && SWAP_EPISODE=1
[[ $SWAP_EPISODE -ge $EPISODES ]] && SWAP_EPISODE=$(( EPISODES - 1 ))
EVAL_SEED=$(( BASE_SEED + 2 * TRAIN_EVAL_SEED_OFFSET ))

echo "OutDir=$OUT_DIR  Episodes=$EPISODES  Swap@$SWAP_EPISODE  Drift=$DRIFT_PROFILE  Conf=$SCHEMA_MIN_CONF"
echo "Memory bundle: $TRAINED_MEM"
echo "Reset cache: $RESET_SCHEMA_CACHE"
echo ""

# ---------------------------------------------------------------------------
# Run helper
# ---------------------------------------------------------------------------
run_phase() {
  local provider="$1"; shift
  local exp_id="$1"; shift
  local reps="$1"; shift
  local workers="$1"; shift

  echo ""
  echo "================================================================================"
  echo "$exp_id  provider=$provider  reps=$reps  alias_mode=minimal  workers=$workers"
  echo "================================================================================"
  "$PYTHON_EXE" -m src.eval.run_experiments \
    --experiment-id "$exp_id" \
    --repetitions "$reps" \
    --episodes "$EPISODES" \
    --base-seed "$EVAL_SEED" \
    --seed-step "$SEED_STEP" \
    --benign-rate "$BENIGN_RATE" \
    --noise-per-episode "$NOISE_PER_EPISODE" \
    --backend-b-drift-profile "$DRIFT_PROFILE" \
    --backend-b-alias-mode minimal \
    --schema-adapt-mode contract_first \
    --memory-seed-dir "$TRAINED_MEM" \
    --out-dir "$OUT_DIR" \
    --schema-map-min-confidence "$SCHEMA_MIN_CONF" \
    --llm-provider "$provider" \
    --gemini-model "$GEMINI_MODEL" \
    --anthropic-model "$ANTHROPIC_MODEL" \
    --ollama-url "$OLLAMA_URL" \
    --ollama-model "$OLLAMA_MODEL" \
    --llm-timeout-sec "$LLM_TIMEOUT_SEC" \
    --max-workers "$workers" \
    --blue-schema-mapper dynamic \
    --mcp-enabled \
    --swap-episode "$SWAP_EPISODE" \
    --swap-phase1-backend backend_a \
    --swap-phase2-backend backend_b
  "$PYTHON_EXE" -m src.eval.aggregate_results --manifest "$OUT_DIR/$exp_id/manifest.json"
}

# ---------------------------------------------------------------------------
# Execute
# ---------------------------------------------------------------------------
if [[ "$RUN_GEMINI" == "1" ]]; then
  run_phase gemini "$(tag_id phase_s3_gemini)" "$REPETITIONS" "$MAX_WORKERS_API"
  [[ "$INCLUDE_ROBUST" == "1" ]] && run_phase gemini "$(tag_id phase_s3r_gemini)" "$ROBUST_REPETITIONS" "$MAX_WORKERS_API"
fi

if [[ "$RUN_ANTHROPIC" == "1" ]]; then
  run_phase anthropic "$(tag_id phase_s3_anthropic)" "$REPETITIONS" "$MAX_WORKERS_API"
  [[ "$INCLUDE_ROBUST" == "1" ]] && run_phase anthropic "$(tag_id phase_s3r_anthropic)" "$ROBUST_REPETITIONS" "$MAX_WORKERS_API"
fi

if [[ "$RUN_QWEN" == "1" ]]; then
  # Ollama serializes on the local Metal GPU; workers=1 avoids contention.
  run_phase ollama "$(tag_id phase_s3_qwen)" "$REPETITIONS" 1
  [[ "$INCLUDE_ROBUST" == "1" ]] && run_phase ollama "$(tag_id phase_s3r_qwen)" "$ROBUST_REPETITIONS" 1
fi

echo ""
echo "Minimal-alias contrast done."
echo ""
echo "Generated manifests:"
for stem in phase_s3_gemini phase_s3r_gemini phase_s3_anthropic phase_s3r_anthropic phase_s3_qwen phase_s3r_qwen; do
  m="$OUT_DIR/$(tag_id $stem)/manifest.json"
  [[ -f "$m" ]] && echo "  $m"
done
echo ""
echo "Headline metrics per phase: $OUT_DIR/<phase>/swap_phase_summary.csv"
echo "LLM call rates:             $OUT_DIR/<phase>/schema_mapper_usage_summary.csv"
