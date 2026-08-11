# Evaluation Summary

## Confusion Matrices (mean +/- std across runs)

- baseline / containment: TP 24.4000 +/- 1.8974, FP 1.1000 +/- 0.8756, TN 14.1000 +/- 1.7920, FN 0.4000 +/- 0.8433, recall 0.9840 +/- 0.0338, n_runs 10, episodes/run 40.0000
- blue / containment: TP 24.6000 +/- 2.0111, FP 0.0000 +/- 0.0000, TN 15.2000 +/- 1.7512, FN 0.2000 +/- 0.4216, recall 0.9913 +/- 0.0184, n_runs 10, episodes/run 40.0000
- baseline / detection: TP 24.4000 +/- 1.8974, FP 1.1000 +/- 0.8756, TN 14.1000 +/- 1.7920, FN 0.4000 +/- 0.8433, recall 0.9840 +/- 0.0338, n_runs 10, episodes/run 40.0000
- blue / detection: TP 24.8000 +/- 1.7512, FP 0.0000 +/- 0.0000, TN 15.2000 +/- 1.7512, FN 0.0000 +/- 0.0000, recall 1.0000 +/- 0.0000, n_runs 10, episodes/run 40.0000

## FP/FN vs Action Tradeoff (mean +/- std across runs)

- baseline: FP 1.1000 +/- 0.8756, FN 0.4000 +/- 0.8433, recall_cont 0.9840 +/- 0.0338, recall_det 0.9840 +/- 0.0338, action_total 0.6375 +/- 0.0489, action_attack 0.9840 +/- 0.0338, attack_no_block 0.0160 +/- 0.0338
- blue: FP 0.0000 +/- 0.0000, FN 0.2000 +/- 0.4216, recall_cont 0.9913 +/- 0.0184, recall_det 1.0000 +/- 0.0000, action_total 0.6200 +/- 0.0438, action_attack 1.0000 +/- 0.0000, attack_no_block 0.0000 +/- 0.0000

## MTTD (mean +/- std across runs)

- baseline: MTTD 5.9607 +/- 1.2170, detected episodes/run 24.8000 +/- 1.7512, negative MTTD/run 1.1000 +/- 0.9944
- blue: MTTD 14.7127 +/- 2.2093, detected episodes/run 24.8000 +/- 1.7512, negative MTTD/run 0.1000 +/- 0.3162

## Latency Breakdown (mean +/- std across runs)

- baseline: pipeline_ms  +/- 0.0000, timed_decisions/run 0.0000 +/- 0.0000, observe  +/- 0.0000, retrieve_memory  +/- 0.0000, correlate  +/- 0.0000, decide  +/- 0.0000, act  +/- 0.0000, log  +/- 0.0000
- blue: pipeline_ms 366.7215 +/- 351.9818, timed_decisions/run 40.0000 +/- 0.0000, observe 13.9299 +/- 0.5669, retrieve_memory 133.3817 +/- 5.9466, correlate 4.6294 +/- 0.4710, decide 0.0085 +/- 0.0004, act 0.0844 +/- 0.0077, log 10.4075 +/- 1.4237

## Recall Diagnosis (memory run)

- blue: attack_block_ip 24.6000 +/- 2.0111, attack_escalate 0.2000 +/- 0.4216, attack_no_block 0.0000 +/- 0.0000, attack_with_memory_hits 24.3000 +/- 1.4181, attack_top_fp_hit 0.0000 +/- 0.0000, benign_block_ip 0.0000 +/- 0.0000

## Swap Phase Metrics (blue)

- runs_with_swap: 10 / 10, phase1_recall_cont 1.0000 +/- 0.0000, phase2_recall_cont 0.9832 +/- 0.0355, delta_recall_cont -0.0168 +/- 0.0355, phase1_mttd 6.5243 +/- 1.6533, phase2_mttd 21.5476 +/- 3.2347, delta_mttd 15.0232 +/- 4.2106

## Schema Fallback Impact (blue)

- fallback_rate 0.0000 +/- 0.0000, fallback_recall  +/- 0.0000, non_fallback_recall 0.9913 +/- 0.0184, fallback_fpr  +/- 0.0000, non_fallback_fpr 0.0000 +/- 0.0000, delta_recall(nonfb-fb)  +/- 0.0000

## Memory Coverage & Override (blue)

- memory_coverage_rate 0.6075 +/- 0.0355, memory_override_rate 0.1950 +/- 0.0387, override_given_hit_rate 0.3213 +/- 0.0631, memory_influence_rate 0.6025 +/- 0.0343, influence_given_hit_rate 0.9920 +/- 0.0169, promote_episodes/run 8.0000 +/- 1.4142, downgrade_episodes/run 0.0000 +/- 0.0000

## Schema Mapper Usage (blue)

- llm_call_rate 0.0200 +/- 0.0329, cache_hit_rate 0.8150 +/- 0.0580, gemini_source_rate 0.0400 +/- 0.0929, ollama_source_rate 0.0000 +/- 0.0000, fallback_source_rate 0.0000 +/- 0.0000, none_source_rate 0.0000 +/- 0.0000
