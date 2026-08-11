# Processed experimental artifacts

`reproduction_manifest.csv` lists only the canonical experiment artifacts used
to reproduce manuscript results. Artifacts retained solely for provenance after
failing an execution-validity check are listed separately in
`excluded_runs.csv` and must not be included in metric aggregation.

The S0--S4 component analysis uses the canonical S0, S1, and S2 aggregate
directories under `wave_b_ablation/`, the S3 provider conditions under
`wave_b_minimal/`, and the valid S4 direct-access conditions under
`wave_b_ablation/`. These directories contain aggregate CSV files rather than
raw repetition logs.

For Gemini S4, the canonical source is
`wave_b_ablation/phase_s4_gemini_nomcp_tier1_w1`. The historical
`phase_s4_ablation_gemini_nomcp_w1` artifact is retained only to document a
provider-transport failure and is excluded from the manuscript analysis.

For RQ4, the canonical sources are the paired Qwen conditions
`recurrent_benign_eval_nomem_qwen3_8b_paired_v1` and
`recurrent_benign_eval_withmem_qwen3_8b_paired_v1`. They use identical
evaluation seeds and 20 benign episodes per repetition. The historical
12-episode Haiku aggregate is retained only for provenance and is listed in
`excluded_runs.csv`.
