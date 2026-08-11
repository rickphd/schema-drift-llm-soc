# Evaluating Confidence-Gated Schema Normalization Under Telemetry Schema Drift

This repository provides the reproducibility artifacts for a cybersecurity study of an LLM-assisted blue-team agent under controlled telemetry schema drift. The released code and curated artifacts support the paper's evaluation of a controlled backend swap, schema normalization under the `hard4` drift profile, S0-S4 component configurations, cold-start F1/F2/F3 seed conditions, no-shared-cache ablations, threshold sensitivity for Gemini, recurrent benign-memory behavior, MTTD/MTTR, and latency. The repository is scoped to reproducible scientific evaluation: it includes executable protocols, aggregate outputs, and claim-to-artifact mappings, but excludes API keys, raw provider responses, raw logs, local caches, and development history.

## Repository Contents

| Path | Purpose |
|---|---|
| `src/` | Experiment code for episode generation, backend A/B telemetry, schema normalization, memory, local MCP-style tool access, judging, and aggregation. |
| `scripts/` | Entry points for the minimal-alias provider contrast, recurrent benign-memory evaluation, and evidence-backed figure generation. |
| `data/processed/` | Curated aggregate CSV and summary artifacts used to verify the paper claims. |
| `data/processed/reproduction_manifest.csv` | Canonical manifest of configurations, seeds, providers, models, drift settings, cache settings, and worker counts used in manuscript results. |
| `data/processed/excluded_runs.csv` | Provenance registry for retained artifacts that failed execution-validity checks and are excluded from manuscript aggregation. |
| `docs/reproduction_protocol.md` | Procedure for environment setup, experiment execution, aggregation, and verification. |
| `docs/data_dictionary.md` | Definitions for metrics and artifact columns used by the released outputs. |
| `docs/claim_to_artifact_map.md` | Mapping from paper claims to scripts, artifacts, metrics, scope, and limitations. |
| `figures/README.md` | Mapping from the current paper figure numbers to the released publication artifacts and their evidence sources. |

## What Is Not Included

The public artifact does not include API keys, raw provider responses, raw telemetry logs, local FAISS indexes, schema caches, `.env` files, exploratory outputs, or development history. Provider-backed LLM runs require user-supplied credentials where applicable. The included aggregate artifacts provide reference outputs for verifying the reported results without exposing local execution state. RQ4 is released as seed-matched no-memory and with-memory Qwen aggregate conditions; the static mapper generated zero LLM calls in those runs.

## Quick Reproduction Path

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Add provider credentials only if running Gemini or Anthropic experiments.

TRAINED_MEM="$(./scripts/prepare_memory_bundle.sh)" \
  MAX_WORKERS_API=1 \
  ./scripts/run_minimal_aliases_contrast.sh
./scripts/run_recurrent_benign_memory.sh
```

The full protocol is described in `docs/reproduction_protocol.md`. Numerical comparisons should be made against the aggregate artifacts under `data/processed/`, using `data/processed/reproduction_manifest.csv` as the canonical configuration index. Artifacts listed in `data/processed/excluded_runs.csv` are retained for provenance and must not enter manuscript metric aggregation. Because Gemini and Anthropic are external services, provider-backed repeat executions support procedural reproducibility rather than bit-for-bit identity with the released reference aggregates.

## Citation

Citation metadata for this companion artifact is provided in `CITATION.cff`.
