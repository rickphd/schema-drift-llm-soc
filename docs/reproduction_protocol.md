# Reproduction Protocol

This protocol describes how to reproduce the experimental conditions reported in the paper from the curated repository state. It specifies the environment, random seeds, component configurations, backend-swap procedure, schema-normalization settings, cache and memory conditions, aggregation scripts, and verification checks used to connect generated outputs to the reported claims. Provider-backed LLM runs require user-supplied credentials where applicable; no credentials, raw provider responses, raw logs, or historical execution traces are included in the public artifact.

## Environment

Use Python 3.11 or a compatible Python 3 release. Install runtime dependencies from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For local Qwen runs, install Ollama separately and pull the configured model:

```bash
ollama pull qwen3:8b
```

## Credential Boundary

Gemini and Anthropic runs require credentials supplied by the user through environment variables or a local `.env` file based on `.env.example`. Credentials, raw provider responses, and provider-side logs are outside the public release.

## Configuration Index

The curated configuration index is `data/processed/reproduction_manifest.csv`. It records provider, model, seed base, seed step, number of repetitions, episode count, `hard4` drift, schema-normalization threshold, cache scope, MCP setting, worker count, and the explicit memory condition where applicable for each released aggregate artifact.

## Main Experiment Families

The released aggregates cover these families:

- Cold-start F1/F2/F3 provider contrasts under `hard4` drift and minimal aliases.
- S0--S4 component configurations for static mapping, LLM-assisted normalization, FAISS memory, and direct backend access.
- S3 no-shared-cache ablations for Gemini, Haiku, and Qwen.
- S4 no-MCP component configurations.
- Gemini threshold sensitivity at the evaluated threshold condition.
- Recurrent benign-memory behavior.
- Latency and MTTD/MTTR summaries.

## Minimal-Alias Provider Contrast

Prepare the memory bundle used by the provider contrast:

```bash
./scripts/prepare_memory_bundle.sh
```

Then run the provider contrast with the generated bundle supplied through `TRAINED_MEM`:

```bash
TRAINED_MEM=/path/to/generated/memory_bundle \
  MAX_WORKERS_API=1 \
  ./scripts/run_minimal_aliases_contrast.sh
```

The script executes the controlled backend swap with backend A in the first phase and backend B in the second phase. Backend B uses the `hard4` drift profile and minimal aliases, which requires dynamic schema normalization for the decision path.

## Recurrent Benign-Memory Evaluation

```bash
./scripts/run_recurrent_benign_memory.sh
```

This protocol trains memory on recurrent benign traffic and evaluates seed-matched datasets with retrieval and online memory updates either disabled or enabled. The default run uses five repetition pairs, 20 benign episodes per repetition, evaluation seeds 11337--11737 in steps of 100, and local Qwen3:8b configuration. Because the static schema mapper resolves every event in this condition, the released RQ4 runs make zero LLM calls; the configured model is therefore not an experimental factor in this comparison.

## Aggregation

Each run invokes:

```bash
python -m src.eval.aggregate_results --manifest <run_manifest.json>
```

The public repository includes aggregate outputs rather than raw repetition directories. The principal comparison files are:

- `swap_phase_summary.csv`
- `summary_confusion.csv`
- `summary_mttd.csv`
- `latency_breakdown.csv`
- `schema_mapper_usage_summary.csv`
- `schema_fallback_summary.csv`
- `memory_coverage_summary.csv`
- `tradeoff_fp_fn_action.csv`

## Verification

Use `docs/claim_to_artifact_map.md` to identify the artifact, script, metric, scope, and limitation for each paper claim. Use `data/processed/reproduction_manifest.csv` to confirm that a reported aggregate corresponds to the intended provider, drift profile, seed condition, threshold, cache setting, and component configuration.

## Non-Deterministic Elements

Synthetic episode generation is seed-controlled. Provider-backed LLM responses may vary over time because model serving is external to the repository. For that reason, repeat executions of Gemini and Anthropic conditions should be interpreted as procedural reproduction of the reported protocol, with the released aggregate artifacts serving as the reference results for the paper.
