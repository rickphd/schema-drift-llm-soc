# Evaluation Summary

## Confusion Matrices (mean +/- std across runs)

- baseline / containment: TP 0.0000 +/- 0.0000, FP 8.4000 +/- 1.5166, TN 3.6000 +/- 1.5166, FN 0.0000 +/- 0.0000, recall  +/- 0.0000, n_runs 5, episodes/run 12.0000
- blue / containment: TP 0.0000 +/- 0.0000, FP 2.4000 +/- 2.1909, TN 9.6000 +/- 2.1909, FN 0.0000 +/- 0.0000, recall  +/- 0.0000, n_runs 5, episodes/run 12.0000
- baseline / detection: TP 0.0000 +/- 0.0000, FP 8.4000 +/- 1.5166, TN 3.6000 +/- 1.5166, FN 0.0000 +/- 0.0000, recall  +/- 0.0000, n_runs 5, episodes/run 12.0000
- blue / detection: TP 0.0000 +/- 0.0000, FP 2.4000 +/- 2.1909, TN 9.6000 +/- 2.1909, FN 0.0000 +/- 0.0000, recall  +/- 0.0000, n_runs 5, episodes/run 12.0000

## FP/FN vs Action Tradeoff (mean +/- std across runs)

- baseline: FP 8.4000 +/- 1.5166, FN 0.0000 +/- 0.0000, recall_cont  +/- 0.0000, recall_det  +/- 0.0000, action_total 0.7000 +/- 0.1264, action_attack  +/- 0.0000, attack_no_block  +/- 0.0000
- blue: FP 2.4000 +/- 2.1909, FN 0.0000 +/- 0.0000, recall_cont  +/- 0.0000, recall_det  +/- 0.0000, action_total 0.2000 +/- 0.1826, action_attack  +/- 0.0000, attack_no_block  +/- 0.0000

## MTTD (mean +/- std across runs)

- baseline: MTTD  +/- 0.0000, detected episodes/run 0.0000 +/- 0.0000, negative MTTD/run 0.0000 +/- 0.0000
- blue: MTTD  +/- 0.0000, detected episodes/run 0.0000 +/- 0.0000, negative MTTD/run 0.0000 +/- 0.0000

## Latency Breakdown (mean +/- std across runs)

- baseline: pipeline_ms  +/- 0.0000, timed_decisions/run 0.0000 +/- 0.0000, observe  +/- 0.0000, retrieve_memory  +/- 0.0000, correlate  +/- 0.0000, decide  +/- 0.0000, act  +/- 0.0000, log  +/- 0.0000
- blue: pipeline_ms 233.9666 +/- 6.3010, timed_decisions/run 7.2000 +/- 6.5727, observe 8.2684 +/- 0.2888, retrieve_memory 213.7964 +/- 3.5319, correlate 2.4447 +/- 0.5339, decide 0.0090 +/- 0.0019, act 0.0411 +/- 0.0007, log 8.6145 +/- 3.2532

## Recall Diagnosis (memory run)

- blue: attack_block_ip 0.0000 +/- 0.0000, attack_escalate 0.0000 +/- 0.0000, attack_no_block 0.0000 +/- 0.0000, attack_with_memory_hits 0.0000 +/- 0.0000, attack_top_fp_hit 0.0000 +/- 0.0000, benign_block_ip 2.4000 +/- 2.1909

## Swap Phase Metrics (blue)

- runs_with_swap: 0 / 5, phase1_recall_cont  +/- , phase2_recall_cont  +/- , delta_recall_cont  +/- , phase1_mttd  +/- , phase2_mttd  +/- , delta_mttd  +/- 

## Schema Fallback Impact (blue)

- fallback_rate 0.0000 +/- 0.0000, fallback_recall  +/- 0.0000, non_fallback_recall  +/- 0.0000, fallback_fpr  +/- 0.0000, non_fallback_fpr 0.2000 +/- 0.1826, delta_recall(nonfb-fb)  +/- 0.0000

## Memory Coverage & Override (blue)

- memory_coverage_rate 0.6389 +/- 0.1273, memory_override_rate 0.3056 +/- 0.1273, override_given_hit_rate 0.4630 +/- 0.1157, memory_influence_rate 0.6389 +/- 0.1273, influence_given_hit_rate 1.0000 +/- 0.0000, promote_episodes/run 0.0000 +/- 0.0000, downgrade_episodes/run 2.2000 +/- 2.2804

## Schema Mapper Usage (blue)

- llm_call_rate 0.0000 +/- 0.0000, cache_hit_rate 1.0000 +/- 0.0000, gemini_source_rate 0.0000 +/- 0.0000, ollama_source_rate 0.0000 +/- 0.0000, fallback_source_rate 0.0000 +/- 0.0000, none_source_rate 0.0000 +/- 0.0000
