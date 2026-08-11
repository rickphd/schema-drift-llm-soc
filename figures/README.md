# Manuscript figure map

`figures/generated/` contains the publication PDFs used by the current IEEE
Access manuscript. Filenames are stable artifact identifiers and are
intentionally decoupled from rendered paper numbers; the mapping below is
authoritative.

| Paper figure | Publication artifact | Primary evidence or source |
|---|---|---|
| 1 | `generated/fig1_architecture.pdf` | System architecture described in `src/` |
| 2 | `generated/fig2_schema_change_flow.pdf` | Backend A/B schemas and `hard4` drift implementation |
| 3 | `generated/fig3_schema_mapper_5steps.pdf` | `src/blue/schema_mapper.py` |
| 4 | `generated/fig4_bluegraph.pdf` | `src/blue/blue_agent_graph.py` |
| 5 | `generated/fig5_recall_three_models.pdf` | S3 `swap_phase_metrics.csv` and `swap_phase_summary.csv` |
| 6 | `generated/fig6_llm_rate_vs_cache_hit.pdf` | S3 `schema_mapper_usage_summary.csv` |
| 7 | `generated/fig7_cache_warmup.pdf` | S3 per-repetition mapper-usage aggregates |
| 8 | `generated/fig9_latency_breakdown.pdf` | S3 `latency_breakdown.csv` |
| 9 | `generated/fig10_memory_fp_bar.pdf` | Paired recurrent-benign aggregates; `scripts/generate_fig10_rq4_paired.py` |
| 10 | `generated/fig11_ablation_recall.pdf` | S3 cold-start and no-shared-cache aggregates |
| 11 | `generated/fig13_ablation_heatmap.pdf` | S0--S4 `swap_phase_metrics.csv` and `swap_phase_summary.csv` |
| 12 | `generated/fig14_ablation_latency.pdf` | S0--S4 `latency_breakdown.csv` |

The MTTD/MTTR values remain reproducible from `summary_mttd.csv` and are
reported in the manuscript table and text. Per-repetition S1/S3 recall remains
available in the corresponding `swap_phase_metrics.csv` files. These numerical
artifacts are retained even when a separate visualization is not part of the
paper.
