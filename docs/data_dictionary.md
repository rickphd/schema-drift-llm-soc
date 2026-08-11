# Data Dictionary

This document defines the principal released artifacts. Column availability can vary by experiment family; empty values indicate that the metric is not applicable for that configuration.

## Configuration Fields

| Field | Meaning |
|---|---|
| `experiment_id` | Identifier of the executed experimental condition. |
| `artifact_dir` | Public path containing the aggregate artifacts for the condition. |
| `repetitions` | Number of repeated runs included in the aggregate. |
| `episodes` | Number of episodes per repetition. |
| `base_seed` | Initial random seed for the condition. |
| `seed_step` | Increment applied across repetitions. |
| `backend_b_drift_profile` | Drift profile used by backend B; the paper uses `hard4` for the reported backend-swap evaluation. |
| `backend_b_alias_mode` | Alias regime used by backend B; `minimal` restricts direct aliases to critical fields. |
| `schema_map_min_confidence` | Confidence threshold used by dynamic schema normalization. |
| `schema_cache_scope` | Scope of schema mapping cache reuse. |
| `mcp_enabled` | Whether tool access through the local MCP-style client is enabled. |
| `memory_enabled` | Whether FAISS retrieval and online memory updates are enabled. Empty values denote legacy families for which this field was not recorded in the curated index. |
| `llm_provider` | Provider used by dynamic schema normalization. |
| `max_workers` | Worker count used for the execution condition. |

## Outcome Metrics

| Artifact | Key Fields | Interpretation |
|---|---|---|
| `summary_confusion.csv` | detection and containment confusion counts and derived rates | Classification and containment outcomes aggregated over repetitions. |
| `swap_phase_summary.csv` | phase-specific recall, precision, and count summaries | Backend-swap performance before and after the schema change. |
| `swap_phase_metrics.csv` | repetition-level phase metrics | Per-repetition basis for swap-phase aggregation. |
| `summary_mttd.csv` | MTTD and MTTR summaries | Mean time to detection and mean time to response under the evaluated condition. |
| `latency_breakdown.csv` | latency components and totals | Runtime cost attributed to the evaluated decision path and supporting components. |
| `schema_mapper_usage.csv` | repetition-level mapper calls, cache hits, and fallback behavior | Operational use of dynamic schema normalization. |
| `schema_mapper_usage_summary.csv` | aggregate mapper usage rates | Summary view of LLM call rate, cache behavior, and mapping outcomes. |
| `schema_fallback_summary.csv` | fallback counts and rates | Frequency of schema-normalization fallback behavior. |
| `memory_coverage_summary.csv` | memory hit and coverage summaries | Coverage of the memory mechanism over evaluated episodes. |
| `tradeoff_fp_fn_action.csv` | false-positive, false-negative, and action trade-off summaries | Decision trade-offs relevant to containment behavior. |
| `recurrent_benign_analysis_nomem_summary.csv` | action and memory rates for the memory-disabled condition | Seed-matched RQ4 control with FAISS retrieval and online memory updates disabled. |
| `recurrent_benign_analysis_withmem_summary.csv` | action and memory rates for the memory-enabled condition | Seed-matched RQ4 condition using the trained recurrent-benign memory bundle. |

## Temporal Metrics

MTTD is mean time to detection. MTTR is mean time to response. Both are computed from the generated episode ground truth and the blue-agent decision outputs by the judge modules in `src/judge/`.

## Scope

The released artifacts are scoped to the synthetic cyber-range setting, the controlled backend swap, the `hard4` drift profile, the configured provider/model set, and the component configurations described in the paper. They should not be interpreted as a general benchmark of all SOC workflows, all telemetry schemas, or all LLM providers.
