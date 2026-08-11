# Excluded from manuscript analysis

This historical Gemini S4 artifact is not a canonical manuscript result. It is
retained only for provenance because provider-transport failures (HTTP 429)
affected 16 episodes across 8 of the 10 repetitions. Those episodes account for
all 16 false-negative containment outcomes in this artifact.

The canonical Gemini S4 source is the complete corrected execution at
`../phase_s4_gemini_nomcp_tier1_w1`, which used the same experiment parameters,
seeds, and byte-identical datasets and completed without provider-transport
errors. Its post-swap containment recall is 1.0000 +/- 0.0000 across 10
repetitions.

Do not include this directory in aggregate manuscript metrics.
