# Evaluation Summary

## Confusion Matrices (mean +/- std across runs)

- baseline / containment: TP 0.0000 +/- 0.0000, FP 19.8000 +/- 0.4472, TN 0.2000 +/- 0.4472, FN 0.0000 +/- 0.0000, recall  +/- 0.0000, n_runs 5, episodes/run 20.0000
- blue / containment: TP 0.0000 +/- 0.0000, FP 20.0000 +/- 0.0000, TN 0.0000 +/- 0.0000, FN 0.0000 +/- 0.0000, recall  +/- 0.0000, n_runs 5, episodes/run 20.0000
- baseline / detection: TP 0.0000 +/- 0.0000, FP 19.8000 +/- 0.4472, TN 0.2000 +/- 0.4472, FN 0.0000 +/- 0.0000, recall  +/- 0.0000, n_runs 5, episodes/run 20.0000
- blue / detection: TP 0.0000 +/- 0.0000, FP 20.0000 +/- 0.0000, TN 0.0000 +/- 0.0000, FN 0.0000 +/- 0.0000, recall  +/- 0.0000, n_runs 5, episodes/run 20.0000

## FP/FN vs Action Tradeoff (mean +/- std across runs)

- baseline: FP 19.8000 +/- 0.4472, FN 0.0000 +/- 0.0000, recall_cont  +/- 0.0000, recall_det  +/- 0.0000, action_total 0.9900 +/- 0.0224, action_attack  +/- 0.0000, attack_no_block  +/- 0.0000
- blue: FP 20.0000 +/- 0.0000, FN 0.0000 +/- 0.0000, recall_cont  +/- 0.0000, recall_det  +/- 0.0000, action_total 1.0000 +/- 0.0000, action_attack  +/- 0.0000, attack_no_block  +/- 0.0000

## MTTD (mean +/- std across runs)

- baseline: MTTD  +/- 0.0000, detected episodes/run 0.0000 +/- 0.0000, negative MTTD/run 0.0000 +/- 0.0000
- blue: MTTD  +/- 0.0000, detected episodes/run 0.0000 +/- 0.0000, negative MTTD/run 0.0000 +/- 0.0000

## Latency Breakdown (mean +/- std across runs)

- baseline: pipeline_ms  +/- 0.0000, timed_decisions/run 0.0000 +/- 0.0000, observe  +/- 0.0000, retrieve_memory  +/- 0.0000, correlate  +/- 0.0000, decide  +/- 0.0000, act  +/- 0.0000, log  +/- 0.0000
- blue: pipeline_ms 12.0067 +/- 0.1677, timed_decisions/run 20.0000 +/- 0.0000, observe 7.1188 +/- 0.0661, retrieve_memory 0.0083 +/- 0.0004, correlate 3.9784 +/- 0.0840, decide 0.0034 +/- 0.0003, act 0.1215 +/- 0.0061, log 0.0021 +/- 0.0001

## Recall Diagnosis (memory run)

- blue: attack_block_ip 0.0000 +/- 0.0000, attack_escalate 0.0000 +/- 0.0000, attack_no_block 0.0000 +/- 0.0000, attack_with_memory_hits 0.0000 +/- 0.0000, attack_top_fp_hit 0.0000 +/- 0.0000, benign_block_ip 20.0000 +/- 0.0000

## Swap Phase Metrics (blue)

- runs_with_swap: 0 / 5, phase1_recall_cont  +/- , phase2_recall_cont  +/- , delta_recall_cont  +/- , phase1_mttd  +/- , phase2_mttd  +/- , delta_mttd  +/-

## Schema Fallback Impact (blue)

- fallback_rate 0.0000 +/- 0.0000, fallback_recall  +/- 0.0000, non_fallback_recall  +/- 0.0000, fallback_fpr  +/- 0.0000, non_fallback_fpr 1.0000 +/- 0.0000, delta_recall(nonfb-fb)  +/- 0.0000

## Memory Coverage & Override (blue)

- memory_coverage_rate 0.0000 +/- 0.0000, memory_override_rate 0.0000 +/- 0.0000, override_given_hit_rate  +/- 0.0000, memory_influence_rate 0.0000 +/- 0.0000, influence_given_hit_rate  +/- 0.0000, promote_episodes/run 0.0000 +/- 0.0000, downgrade_episodes/run 0.0000 +/- 0.0000

## Schema Mapper Usage (blue)

- llm_call_rate 0.0000 +/- 0.0000, cache_hit_rate 1.0000 +/- 0.0000, gemini_source_rate 0.0000 +/- 0.0000, ollama_source_rate 0.0000 +/- 0.0000, fallback_source_rate 0.0000 +/- 0.0000, none_source_rate 0.0000 +/- 0.0000
