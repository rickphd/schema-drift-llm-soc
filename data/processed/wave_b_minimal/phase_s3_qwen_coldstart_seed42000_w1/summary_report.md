# Evaluation Summary

## Confusion Matrices (mean +/- std across runs)

- baseline / containment: TP 26.0000 +/- 2.3570, FP 0.7000 +/- 0.6749, TN 13.0000 +/- 2.5820, FN 0.3000 +/- 0.6749, recall 0.9892 +/- 0.0243, n_runs 10, episodes/run 40.0000
- blue / containment: TP 24.9000 +/- 4.8408, FP 0.0000 +/- 0.0000, TN 13.7000 +/- 2.4518, FN 1.4000 +/- 4.4272, recall 0.9481 +/- 0.1640, n_runs 10, episodes/run 40.0000
- baseline / detection: TP 26.0000 +/- 2.3570, FP 0.7000 +/- 0.6749, TN 13.0000 +/- 2.5820, FN 0.3000 +/- 0.6749, recall 0.9892 +/- 0.0243, n_runs 10, episodes/run 40.0000
- blue / detection: TP 24.9000 +/- 4.8408, FP 0.0000 +/- 0.0000, TN 13.7000 +/- 2.4518, FN 1.4000 +/- 4.4272, recall 0.9481 +/- 0.1640, n_runs 10, episodes/run 40.0000

## FP/FN vs Action Tradeoff (mean +/- std across runs)

- baseline: FP 0.7000 +/- 0.6749, FN 0.3000 +/- 0.6749, recall_cont 0.9892 +/- 0.0243, recall_det 0.9892 +/- 0.0243, action_total 0.6675 +/- 0.0624, action_attack 0.9892 +/- 0.0243, attack_no_block 0.0108 +/- 0.0243
- blue: FP 0.0000 +/- 0.0000, FN 1.4000 +/- 4.4272, recall_cont 0.9481 +/- 0.1640, recall_det 0.9481 +/- 0.1640, action_total 0.6225 +/- 0.1210, action_attack 0.9481 +/- 0.1640, attack_no_block 0.0000 +/- 0.0000

## MTTD (mean +/- std across runs)

- baseline: MTTD 6.2894 +/- 1.2834, detected episodes/run 26.3000 +/- 2.4518, negative MTTD/run 1.4000 +/- 1.0750
- blue: MTTD 13.2493 +/- 3.2729, detected episodes/run 24.9000 +/- 4.8408, negative MTTD/run 0.3000 +/- 0.6749

## Latency Breakdown (mean +/- std across runs)

- baseline: pipeline_ms  +/- 0.0000, timed_decisions/run 0.0000 +/- 0.0000, observe  +/- 0.0000, retrieve_memory  +/- 0.0000, correlate  +/- 0.0000, decide  +/- 0.0000, act  +/- 0.0000, log  +/- 0.0000
- blue: pipeline_ms 177.1507 +/- 73.7339, timed_decisions/run 38.0000 +/- 6.3246, observe 13.3293 +/- 1.8455, retrieve_memory 122.0685 +/- 4.6369, correlate 4.4132 +/- 0.7952, decide 0.0084 +/- 0.0008, act 0.1033 +/- 0.0504, log 10.3451 +/- 0.9427

## Recall Diagnosis (memory run)

- blue: attack_block_ip 24.9000 +/- 4.8408, attack_escalate 0.0000 +/- 0.0000, attack_no_block 0.0000 +/- 0.0000, attack_with_memory_hits 24.4000 +/- 4.7889, attack_top_fp_hit 0.0000 +/- 0.0000, benign_block_ip 0.0000 +/- 0.0000

## Swap Phase Metrics (blue)

- runs_with_swap: 9 / 10, phase1_recall_cont 1.0000 +/- 0.0000, phase2_recall_cont 1.0000 +/- 0.0000, delta_recall_cont 0.0000 +/- 0.0000, phase1_mttd 6.5119 +/- 1.3303, phase2_mttd 21.8877 +/- 3.9323, delta_mttd 15.3758 +/- 4.3786

## Schema Fallback Impact (blue)

- fallback_rate 0.0000 +/- 0.0000, fallback_recall  +/- 0.0000, non_fallback_recall 0.9482 +/- 0.1640, fallback_fpr  +/- 0.0000, non_fallback_fpr 0.0000 +/- 0.0000, delta_recall(nonfb-fb)  +/- 0.0000

## Memory Coverage & Override (blue)

- memory_coverage_rate 0.6425 +/- 0.0657, memory_override_rate 0.2175 +/- 0.0472, override_given_hit_rate 0.3382 +/- 0.0635, memory_influence_rate 0.6400 +/- 0.0699, influence_given_hit_rate 0.9954 +/- 0.0144, promote_episodes/run 8.3000 +/- 2.4060, downgrade_episodes/run 0.0000 +/- 0.0000

## Schema Mapper Usage (blue)

- llm_call_rate 0.0150 +/- 0.0394, cache_hit_rate 0.8225 +/- 0.0803, gemini_source_rate 0.0000 +/- 0.0000, ollama_source_rate 0.0375 +/- 0.1101, fallback_source_rate 0.0000 +/- 0.0000, none_source_rate 0.0000 +/- 0.0000
