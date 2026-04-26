No output file was written: no output path was provided, and this workspace is read-only.

# C1(a) Cross-Family AI Direct-PDF Verification — Codex (gpt-5.4)
**Date**: 2026-04-26  
**Reviewer**: Codex (independent of Claude)  
**PDFs read directly via `pdftotext`**:
- [Cui 2019 PDF](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/pdfs/Cui 等 - 2019 - Twin-Field Quantum Key Distribution without Phase .pdf>): pp. 1-6, focused on p. 2 Step 3 / Section III / Eq. (1) / Eq. (3), and Appendix A on pp. 5-6
- [Pirandola 2019 PDF](/Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/literature/pdfs/Pirandola-2019-EndToEndCapacities.pdf): pp. 2-3, 7-8, 15-21, focused on Eq. (11), Eq. (36), SI Note 1 Eq. (91)-(92), and SI Note 2 network model
- [Curty-Azuma-Lo 2018 PDF](/Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/literature/pdfs/Curty-Azuma-Lo-2018-SimpleSecurityTwinField.pdf): pp. 3-5, focused on Eq. (10), Eq. (11), and the Conclusion

Short verbatim excerpts below are quote-limit-compliant fragments, not full sentences.

## Per-Point Verdict
1. **PASS**. Cui p. 2, Step 3 paragraph says Charlie must “publicly announce” success/failure and detector label; Pirandola SI Note 1 p. 15, opening paragraph says each point “broadcasts classical information” and performs “conditional LOs.” Textual alignment is direct.

2. **PASS**. Pirandola SI Note 1 p. 15 defines the chain protocol by “adaptive LOs” plus broadcast/feedback by all points. That text covers Charlie’s measurement-plus-broadcast at the LOCC level. The parenthetical “not just unitary + CC” is an inference from LOCC terminology, not a separate explicit contrast in the paper.

3. **PASS**. Pirandola SI Note 1 p. 15 models a chain with channels `E_i`; Supplementary Note 2 p. 20 says points are connected by “memoryless quantum channels” along edges. A trusted two-edge `A-C-B` chain fits that model.

4. **FAIL**. Cui p. 2, Section III ends only with a claim that the proof can “guarantee security against the coherent attacks asymptotically.” Appendix A pp. 5-6 develops a Holevo/Devetak-Winter bound. I found no explicit `ε`, `composable`, trace-norm, or private-state criterion in Cui.

5. **PASS**. Curty p. 3 states node C is under Eve’s “full control”; p. 4, paragraph above Eq. (10), defines the announcement-conditioned state `|χ_{k_c,k_d}>`, and Eq. (11) computes the phase-error rate from that reduced state. That is direct citation support for the reduced-state / partial-trace style argument needed for Lemma B.

6. **UNCERTAIN**. KW Ch. 20 §20.2 is not available in `docs/literature/pdfs/`, and I did not find an equivalent passage in Cui / Pirandola / Curty that directly states the SKA ↔ private-state purification trick under Cui’s Eve model.

7. **PASS**. Cui p. 2 Eq. (3) gives a rate “per trial”; Pirandola SI Note 1 p. 15 defines the chain rate in “bits per chain use” via Eq. (91), after explicitly describing what one use of the chain is. For the `N=1` lockstep chain, one Cui trial uses each edge once, so the normalizations align at the chain-use level.

8. **FAIL**. Cui p. 2 Eq. (3) / Appendix A Eq. (A6) use an asymptotic Devetak-Winter/Holevo rate; Pirandola Methods pp. 7-8 define success by trace-norm `ε`-closeness to a target private state. Cui does not textually equate its rate formula with that criterion.

## Trap Memory Cross-Check
- **5th trap (AI structural gaps)**: Curty 2018 stays in the untrusted-Charlie picture. It gives a virtual-state / announcement-conditioned reduced-state argument, but it does **not** textually walk `Π -> ι(Π) = Π_tr`.
- **6th trap (channel-vs-state)**: Pirandola explicitly defines rates in “bits per chain use” and, for networks, per “sequential use of the network.” It does **not** explicitly say “per bottleneck-link use.” That stronger wording is an `N=1` counting inference.

## Aggregate Verdict
**PARTIAL**.

PASS: 1, 2, 3, 5, 7.  
FAIL: 4, 8.  
UNCERTAIN: 6.

So the eight-point cross-reference bundle is **not** fully supported by direct-PDF text.

## Recommendations to User
- Human paper formalization is still needed for the structural embedding `Π -> Π_tr`; Curty 2018 does not close that gap.
- Add a primary composable-security citation that explicitly maps Cui-style asymptotic security to an `ε`-private-state / composable definition, or treat points 4 and 8 as unsupported.
- Obtain KW Ch. 20 §20.2, or another primary source, for the SKA/private-state purification step behind point 6.
- State normalization explicitly as `per trial = per chain use` for the `N=1` lockstep chain, and avoid the stronger “per bottleneck-link use” wording unless separately formalized.
- Keep all 11 path α sub-gaps at `[UNKNOWN]`; nothing in this C1(a) pass upgrades `[SYN]` or closes a lemma.