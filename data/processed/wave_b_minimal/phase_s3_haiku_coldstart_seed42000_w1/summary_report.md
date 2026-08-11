# Evaluation Summary

## Confusion Matrices (mean +/- std across runs)

- baseline / containment: TP 26.0000 +/- 2.3570, FP 0.7000 +/- 0.6749, TN 13.0000 +/- 2.5820, FN 0.3000 +/- 0.6749, recall 0.9892 +/- 0.0243, n_runs 10, episodes/run 40.0000
- blue / containment: TP 26.3000 +/- 2.4518, FP 0.0000 +/- 0.0000, TN 13.7000 +/- 2.4518, FN 0.0000 +/- 0.0000, recall 1.0000 +/- 0.0000, n_runs 10, episodes/run 40.0000
- baseline / detection: TP 26.0000 +/- 2.3570, FP 0.7000 +/- 0.6749, TN 13.0000 +/- 2.5820, FN 0.3000 +/- 0.6749, recall 0.9892 +/- 0.0243, n_runs 10, episodes/run 40.0000
- blue / detection: TP 26.3000 +/- 2.4518, FP 0.0000 +/- 0.0000, TN 13.7000 +/- 2.4518, FN 0.0000 +/- 0.0000, recall 1.0000 +/- 0.0000, n_runs 10, episodes/run 40.0000

## FP/FN vs Action Tradeoff (mean +/- std across runs)

- baseline: FP 0.7000 +/- 0.6749, FN 0.3000 +/- 0.6749, recall_cont 0.9892 +/- 0.0243, recall_det 0.9892 +/- 0.0243, action_total 0.6675 +/- 0.0624, action_attack 0.9892 +/- 0.0243, attack_no_block 0.0108 +/- 0.0243
- blue: FP 0.0000 +/- 0.0000, FN 0.0000 +/- 0.0000, recall_cont 1.0000 +/- 0.0000, recall_det 1.0000 +/- 0.0000, action_total 0.6575 +/- 0.0613, action_attack 1.0000 +/- 0.0000, attack_no_block 0.0000 +/- 0.0000

## MTTD (mean +/- std across runs)

- baseline: MTTD 6.2894 +/- 1.2834, detected episodes/run 26.3000 +/- 2.4518, negative MTTD/run 1.4000 +/- 1.0750
- blue: MTTD 14.0229 +/- 2.1210, detected episodes/run 26.3000 +/- 2.4518, negative MTTD/run 0.3000 +/- 0.6749

## Latency Breakdown (mean +/- std across runs)

- baseline: pipeline_ms  +/- 0.0000, timed_decisions/run 0.0000 +/- 0.0000, observe  +/- 0.0000, retrieve_memory  +/- 0.0000, correlate  +/- 0.0000, decide  +/- 0.0000, act  +/- 0.0000, log  +/- 0.0000
- blue: pipeline_ms 194.6830 +/- 77.1734, timed_decisions/run 40.0000 +/- 0.0000, observe 13.4234 +/- 1.4474, retrieve_memory 137.4670 +/- 6.3141, correlate 4.5382 +/- 0.4146, decide 0.0081 +/- 0.0007, act 0.0886 +/- 0.0088, log 10.5729 +/- 1.6247

## Recall Diagnosis (memory run)

- blue: attack_block_ip 26.3000 +/- 2.4518, attack_escalate 0.0000 +/- 0.0000, attack_no_block 0.0000 +/- 0.0000, attack_with_memory_hits 25.8000 +/- 2.6583, attack_top_fp_hit 0.0000 +/- 0.0000, benign_block_ip 0.0000 +/- 0.0000

## Swap Phase Metrics (blue)

- runs_with_swap: 10 / 10, phase1_recall_cont 1.0000 +/- 0.0000, phase2_recall_cont 1.0000 +/- 0.0000, delta_recall_cont 0.0000 +/- 0.0000, phase1_mttd 6.4761 +/- 1.2593, phase2_mttd 21.8060 +/- 3.7163, delta_mttd 15.3300 +/- 4.1307

## Schema Fallback Impact (blue)

- fallback_rate 0.0000 +/- 0.0000, fallback_recall  +/- 0.0000, non_fallback_recall 1.0000 +/- 0.0000, fallback_fpr  +/- 0.0000, non_fallback_fpr 0.0000 +/- 0.0000, delta_recall(nonfb-fb)  +/- 0.0000

## Memory Coverage & Override (blue)

- memory_coverage_rate 0.6450 +/- 0.0665, memory_override_rate 0.2200 +/- 0.0468, override_given_hit_rate 0.3408 +/- 0.0626, memory_influence_rate 0.6425 +/- 0.0708, influence_given_hit_rate 0.9954 +/- 0.0144, promote_episodes/run 8.8000 +/- 1.8738, downgrade_episodes/run 0.0000 +/- 0.0000

## Schema Mapper Usage (blue)

- llm_call_rate 0.0150 +/- 0.0394, cache_hit_rate 0.8075 +/- 0.0528, gemini_source_rate 0.0000 +/- 0.0000, ollama_source_rate 0.0000 +/- 0.0000, fallback_source_rate 0.0000 +/- 0.0000, none_source_rate 0.0000 +/- 0.0000
