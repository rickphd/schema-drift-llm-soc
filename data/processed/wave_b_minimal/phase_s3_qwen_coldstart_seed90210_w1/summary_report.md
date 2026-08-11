# Evaluation Summary

## Confusion Matrices (mean +/- std across runs)

- baseline / containment: TP 24.4000 +/- 1.8974, FP 1.1000 +/- 0.8756, TN 14.1000 +/- 1.7920, FN 0.4000 +/- 0.8433, recall 0.9840 +/- 0.0338, n_runs 10, episodes/run 40.0000
- blue / containment: TP 24.8000 +/- 1.7512, FP 0.0000 +/- 0.0000, TN 15.2000 +/- 1.7512, FN 0.0000 +/- 0.0000, recall 1.0000 +/- 0.0000, n_runs 10, episodes/run 40.0000
- baseline / detection: TP 24.4000 +/- 1.8974, FP 1.1000 +/- 0.8756, TN 14.1000 +/- 1.7920, FN 0.4000 +/- 0.8433, recall 0.9840 +/- 0.0338, n_runs 10, episodes/run 40.0000
- blue / detection: TP 24.8000 +/- 1.7512, FP 0.0000 +/- 0.0000, TN 15.2000 +/- 1.7512, FN 0.0000 +/- 0.0000, recall 1.0000 +/- 0.0000, n_runs 10, episodes/run 40.0000

## FP/FN vs Action Tradeoff (mean +/- std across runs)

- baseline: FP 1.1000 +/- 0.8756, FN 0.4000 +/- 0.8433, recall_cont 0.9840 +/- 0.0338, recall_det 0.9840 +/- 0.0338, action_total 0.6375 +/- 0.0489, action_attack 0.9840 +/- 0.0338, attack_no_block 0.0160 +/- 0.0338
- blue: FP 0.0000 +/- 0.0000, FN 0.0000 +/- 0.0000, recall_cont 1.0000 +/- 0.0000, recall_det 1.0000 +/- 0.0000, action_total 0.6200 +/- 0.0438, action_attack 1.0000 +/- 0.0000, attack_no_block 0.0000 +/- 0.0000

## MTTD (mean +/- std across runs)

- baseline: MTTD 5.9607 +/- 1.2170, detected episodes/run 24.8000 +/- 1.7512, negative MTTD/run 1.1000 +/- 0.9944
- blue: MTTD 14.7127 +/- 2.2093, detected episodes/run 24.8000 +/- 1.7512, negative MTTD/run 0.1000 +/- 0.3162

## Latency Breakdown (mean +/- std across runs)

- baseline: pipeline_ms  +/- 0.0000, timed_decisions/run 0.0000 +/- 0.0000, observe  +/- 0.0000, retrieve_memory  +/- 0.0000, correlate  +/- 0.0000, decide  +/- 0.0000, act  +/- 0.0000, log  +/- 0.0000
- blue: pipeline_ms 190.5492 +/- 58.3702, timed_decisions/run 40.0000 +/- 0.0000, observe 13.3383 +/- 0.7260, retrieve_memory 134.9965 +/- 3.2512, correlate 4.5090 +/- 0.3179, decide 0.0079 +/- 0.0005, act 0.1474 +/- 0.1768, log 9.8292 +/- 1.5179

## Recall Diagnosis (memory run)

- blue: attack_block_ip 24.8000 +/- 1.7512, attack_escalate 0.0000 +/- 0.0000, attack_no_block 0.0000 +/- 0.0000, attack_with_memory_hits 24.3000 +/- 1.4181, attack_top_fp_hit 0.0000 +/- 0.0000, benign_block_ip 0.0000 +/- 0.0000

## Swap Phase Metrics (blue)

- runs_with_swap: 10 / 10, phase1_recall_cont 1.0000 +/- 0.0000, phase2_recall_cont 1.0000 +/- 0.0000, delta_recall_cont 0.0000 +/- 0.0000, phase1_mttd 6.5243 +/- 1.6533, phase2_mttd 21.5476 +/- 3.2347, delta_mttd 15.0232 +/- 4.2106

## Schema Fallback Impact (blue)

- fallback_rate 0.0000 +/- 0.0000, fallback_recall  +/- 0.0000, non_fallback_recall 1.0000 +/- 0.0000, fallback_fpr  +/- 0.0000, non_fallback_fpr 0.0000 +/- 0.0000, delta_recall(nonfb-fb)  +/- 0.0000

## Memory Coverage & Override (blue)

- memory_coverage_rate 0.6075 +/- 0.0355, memory_override_rate 0.1975 +/- 0.0362, override_given_hit_rate 0.3255 +/- 0.0591, memory_influence_rate 0.6025 +/- 0.0343, influence_given_hit_rate 0.9920 +/- 0.0169, promote_episodes/run 7.9000 +/- 1.4491, downgrade_episodes/run 0.0000 +/- 0.0000

## Schema Mapper Usage (blue)

- llm_call_rate 0.0150 +/- 0.0316, cache_hit_rate 0.8200 +/- 0.0550, gemini_source_rate 0.0000 +/- 0.0000, ollama_source_rate 0.0400 +/- 0.1015, fallback_source_rate 0.0000 +/- 0.0000, none_source_rate 0.0000 +/- 0.0000
