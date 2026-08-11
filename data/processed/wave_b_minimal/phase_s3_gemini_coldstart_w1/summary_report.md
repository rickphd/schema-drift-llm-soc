# Evaluation Summary

## Confusion Matrices (mean +/- std across runs)

- baseline / containment: TP 28.2000 +/- 3.2592, FP 1.2000 +/- 1.0328, TN 10.4000 +/- 3.0984, FN 0.2000 +/- 0.6325, recall 0.9923 +/- 0.0243, n_runs 10, episodes/run 40.0000
- blue / containment: TP 27.9000 +/- 2.9609, FP 0.0000 +/- 0.0000, TN 11.6000 +/- 3.0258, FN 0.5000 +/- 0.7071, recall 0.9828 +/- 0.0244, n_runs 10, episodes/run 40.0000
- baseline / detection: TP 28.2000 +/- 3.2592, FP 1.2000 +/- 1.0328, TN 10.4000 +/- 3.0984, FN 0.2000 +/- 0.6325, recall 0.9923 +/- 0.0243, n_runs 10, episodes/run 40.0000
- blue / detection: TP 28.4000 +/- 3.0258, FP 0.0000 +/- 0.0000, TN 11.6000 +/- 3.0258, FN 0.0000 +/- 0.0000, recall 1.0000 +/- 0.0000, n_runs 10, episodes/run 40.0000

## FP/FN vs Action Tradeoff (mean +/- std across runs)

- baseline: FP 1.2000 +/- 1.0328, FN 0.2000 +/- 0.6325, recall_cont 0.9923 +/- 0.0243, recall_det 0.9923 +/- 0.0243, action_total 0.7350 +/- 0.0801, action_attack 0.9923 +/- 0.0243, attack_no_block 0.0077 +/- 0.0243
- blue: FP 0.0000 +/- 0.0000, FN 0.5000 +/- 0.7071, recall_cont 0.9828 +/- 0.0244, recall_det 1.0000 +/- 0.0000, action_total 0.7100 +/- 0.0756, action_attack 1.0000 +/- 0.0000, attack_no_block 0.0000 +/- 0.0000

## MTTD (mean +/- std across runs)

- baseline: MTTD 6.3468 +/- 1.1995, detected episodes/run 28.4000 +/- 3.0258, negative MTTD/run 0.4000 +/- 0.6992
- blue: MTTD 14.1417 +/- 1.8582, detected episodes/run 28.4000 +/- 3.0258, negative MTTD/run 0.1000 +/- 0.3162

## Latency Breakdown (mean +/- std across runs)

- baseline: pipeline_ms  +/- 0.0000, timed_decisions/run 0.0000 +/- 0.0000, observe  +/- 0.0000, retrieve_memory  +/- 0.0000, correlate  +/- 0.0000, decide  +/- 0.0000, act  +/- 0.0000, log  +/- 0.0000
- blue: pipeline_ms 354.4762 +/- 329.7572, timed_decisions/run 40.0000 +/- 0.0000, observe 13.1008 +/- 0.9222, retrieve_memory 141.1327 +/- 4.9546, correlate 5.1694 +/- 0.5657, decide 0.0088 +/- 0.0007, act 0.1233 +/- 0.0870, log 9.7917 +/- 0.8846

## Recall Diagnosis (memory run)

- blue: attack_block_ip 27.9000 +/- 2.9609, attack_escalate 0.5000 +/- 0.7071, attack_no_block 0.0000 +/- 0.0000, attack_with_memory_hits 27.9000 +/- 3.0350, attack_top_fp_hit 0.0000 +/- 0.0000, benign_block_ip 0.0000 +/- 0.0000

## Swap Phase Metrics (blue)

- runs_with_swap: 10 / 10, phase1_recall_cont 1.0000 +/- 0.0000, phase2_recall_cont 0.9668 +/- 0.0460, delta_recall_cont -0.0332 +/- 0.0460, phase1_mttd 6.4129 +/- 1.5787, phase2_mttd 21.5527 +/- 2.4516, delta_mttd 15.1398 +/- 2.9519

## Schema Fallback Impact (blue)

- fallback_rate 0.0000 +/- 0.0000, fallback_recall  +/- 0.0000, non_fallback_recall 0.9828 +/- 0.0244, fallback_fpr  +/- 0.0000, non_fallback_fpr 0.0000 +/- 0.0000, delta_recall(nonfb-fb)  +/- 0.0000

## Memory Coverage & Override (blue)

- memory_coverage_rate 0.6975 +/- 0.0759, memory_override_rate 0.2300 +/- 0.0587, override_given_hit_rate 0.3281 +/- 0.0676, memory_influence_rate 0.6975 +/- 0.0759, influence_given_hit_rate 1.0000 +/- 0.0000, promote_episodes/run 9.7000 +/- 2.5841, downgrade_episodes/run 0.0000 +/- 0.0000

## Schema Mapper Usage (blue)

- llm_call_rate 0.0250 +/- 0.0312, cache_hit_rate 0.8375 +/- 0.0580, gemini_source_rate 0.0350 +/- 0.1022, ollama_source_rate 0.0000 +/- 0.0000, fallback_source_rate 0.0000 +/- 0.0000, none_source_rate 0.0000 +/- 0.0000
