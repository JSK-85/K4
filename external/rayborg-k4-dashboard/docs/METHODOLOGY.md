# K4 Research Methodology

## Objective

Recover a reproducible, period-plausible transformation that derives a coherent 97-letter K4 plaintext and matches every public plaintext position exactly. Possessing or guessing plaintext without a derivation is not a cryptanalytic solution.

## Immutable Inputs

- Canonical ciphertext: `OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR`
- Local indexing: one-based positions `1-97`, letters only
- Public block A: positions `22-34`, `EASTNORTHEAST`
- Public block B: positions `64-74`, `BERLINCLOCK`
- Standard alphabet: `ABCDEFGHIJKLMNOPQRSTUVWXYZ`
- Sculpture alphabet: `KRYPTOSABCDEFGHIJLMNQUVWXZ`

No experiment may silently alter the ciphertext, move a crib, switch index conventions, or change whether punctuation advances a key.

## Shadow-Run Gate

A new primitive must pass known-answer tests before entering a K4 pipeline:

1. K1 keyed-alphabet Vigenere decryption with `PALIMPSEST`
2. K2 physical-screen decryption with `ABSCISSA`, including the accidental `IDBYROWS` ending
3. K2 corrected decryption after the documented virtual `S`, yielding `XLAYERTWO`
4. K3 exact inverse route over 336 letters
5. Round-trip encryption back to the canonical ciphertext

Readable prefixes are insufficient. Full positional equality is required.

## Crib Holdout Protocol

1. Select parameters using `EASTNORTHEAST` only.
2. Freeze those parameters.
3. Test `BERLINCLOCK` without adjustment.
4. Repeat with training and holdout blocks reversed.
5. Only then fit both blocks together.
6. Compare the observed result with randomized 97-letter controls under the same search budget.

This prevents an unconstrained alphabet, route, or mask from merely memorizing all 24 known letters.

## Every Run Must Record

- exact normalized input and a content hash for larger artifacts
- local/global index convention
- algorithm and implementation revision
- operation order
- alphabet and numeric mapping
- key, primer, matrix, route, dimensions, padding, reversal, and offset
- punctuation/null advancement policy
- finite search space or stochastic budget
- corpus and scoring-function versions
- seed and random-number generator for stochastic work
- elapsed time and hardware for large searches
- candidates tested and filters applied
- train/holdout split
- negative-control distribution
- full 97-letter output, not selected words
- Paradigm verifier result, if a serious candidate is submitted manually

## Status Semantics

- **Not run:** no reproducible experiment recorded
- **Active:** currently scoped or executing
- **Tested:** executed with recorded parameters; no conclusion implied
- **Rejected:** failed a predeclared criterion for the tested parameter space
- **Promising:** survived a holdout or produced a calibrated anomaly worth follow-up
- **Validated:** exact known-answer or independently reproducible control result

Rejecting one parameterization does not reject an entire cipher family unless the declared family was exhaustively covered.

## Candidate Acceptance

A credible K4 candidate should:

- produce coherent full plaintext rather than isolated words
- match all 24 public positions exactly
- use one uniform, explicit rule
- avoid local patches and post-hoc exceptions
- be plausible for hand construction around 1988-1990, even if modern hardware searches it
- explain why earlier passages, physical features, or public clues supply its keys or operations
- survive independent reimplementation
- pass the owner-operated verifier

## Research Discipline

- Separate direct creator statements, institutional records, academic analysis, reporting, and community reconstruction.
- Preserve dated contradictions instead of rewriting older evidence.
- Label speculation explicitly.
- Do not automate or attempt to bypass Paradigm's paid verifier.
- Do not seek or redistribute leaked archival plaintext.
- Treat LLM output as hypothesis generation only; deterministic code must execute and verify every claim.
