# Evaluation Summary

## Confusion Matrices (mean +/- std across runs)

- baseline / containment: TP 28.2000 +/- 3.2592, FP 1.2000 +/- 1.0328, TN 10.4000 +/- 3.0984, FN 0.2000 +/- 0.6325, recall 0.9923 +/- 0.0243, n_runs 10, episodes/run 40.0000
- blue / containment: TP 27.6000 +/- 3.3400, FP 0.0000 +/- 0.0000, TN 11.6000 +/- 3.0258, FN 0.8000 +/- 0.7888, recall 0.9709 +/- 0.0289, n_runs 10, episodes/run 40.0000
- baseline / detection: TP 28.2000 +/- 3.2592, FP 1.2000 +/- 1.0328, TN 10.4000 +/- 3.0984, FN 0.2000 +/- 0.6325, recall 0.9923 +/- 0.0243, n_runs 10, episodes/run 40.0000
- blue / detection: TP 28.4000 +/- 3.0258, FP 0.0000 +/- 0.0000, TN 11.6000 +/- 3.0258, FN 0.0000 +/- 0.0000, recall 1.0000 +/- 0.0000, n_runs 10, episodes/run 40.0000

## FP/FN vs Action Tradeoff (mean +/- std across runs)

- baseline: FP 1.2000 +/- 1.0328, FN 0.2000 +/- 0.6325, recall_cont 0.9923 +/- 0.0243, recall_det 0.9923 +/- 0.0243, action_total 0.7350 +/- 0.0801, action_attack 0.9923 +/- 0.0243, attack_no_block 0.0077 +/- 0.0243
- blue: FP 0.0000 +/- 0.0000, FN 0.8000 +/- 0.7888, recall_cont 0.9709 +/- 0.0289, recall_det 1.0000 +/- 0.0000, action_total 0.7100 +/- 0.0756, action_attack 1.0000 +/- 0.0000, attack_no_block 0.0000 +/- 0.0000

## MTTD (mean +/- std across runs)

- baseline: MTTD 6.3468 +/- 1.1995, detected episodes/run 28.4000 +/- 3.0258, negative MTTD/run 0.4000 +/- 0.6992
- blue: MTTD 14.1417 +/- 1.8582, detected episodes/run 28.4000 +/- 3.0258, negative MTTD/run 0.1000 +/- 0.3162

## Latency Breakdown (mean +/- std across runs)

- baseline: pipeline_ms  +/- 0.0000, timed_decisions/run 0.0000 +/- 0.0000, observe  +/- 0.0000, retrieve_memory  +/- 0.0000, correlate  +/- 0.0000, decide  +/- 0.0000, act  +/- 0.0000, log  +/- 0.0000
- blue: pipeline_ms 358.3410 +/- 370.8121, timed_decisions/run 40.0000 +/- 0.0000, observe 13.4762 +/- 0.9244, retrieve_memory 140.6060 +/- 5.7194, correlate 5.1649 +/- 0.6853, decide 0.0092 +/- 0.0009, act 0.1215 +/- 0.0981, log 12.9536 +/- 1.0412

## Recall Diagnosis (memory run)

- blue: attack_block_ip 27.6000 +/- 3.3400, attack_escalate 0.8000 +/- 0.7888, attack_no_block 0.0000 +/- 0.0000, attack_with_memory_hits 27.4000 +/- 3.0258, attack_top_fp_hit 0.0000 +/- 0.0000, benign_block_ip 0.0000 +/- 0.0000

## Swap Phase Metrics (blue)

- runs_with_swap: 10 / 10, phase1_recall_cont 1.0000 +/- 0.0000, phase2_recall_cont 0.9436 +/- 0.0563, delta_recall_cont -0.0564 +/- 0.0563, phase1_mttd 6.4129 +/- 1.5787, phase2_mttd 21.5527 +/- 2.4516, delta_mttd 15.1398 +/- 2.9519

## Schema Fallback Impact (blue)

- fallback_rate 0.0000 +/- 0.0000, fallback_recall  +/- 0.0000, non_fallback_recall 0.9709 +/- 0.0289, fallback_fpr  +/- 0.0000, non_fallback_fpr 0.0000 +/- 0.0000, delta_recall(nonfb-fb)  +/- 0.0000

## Memory Coverage & Override (blue)

- memory_coverage_rate 0.6850 +/- 0.0756, memory_override_rate 0.2300 +/- 0.0587, override_given_hit_rate 0.3332 +/- 0.0645, memory_influence_rate 0.6850 +/- 0.0756, influence_given_hit_rate 1.0000 +/- 0.0000, promote_episodes/run 10.0000 +/- 2.0548, downgrade_episodes/run 0.0000 +/- 0.0000

## Schema Mapper Usage (blue)

- llm_call_rate 0.0350 +/- 0.0376, cache_hit_rate 0.8275 +/- 0.0661, gemini_source_rate 0.0350 +/- 0.0937, ollama_source_rate 0.0000 +/- 0.0000, fallback_source_rate 0.0000 +/- 0.0000, none_source_rate 0.0000 +/- 0.0000
