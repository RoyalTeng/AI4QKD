Could not write `docs/findings/path_alpha_l1g4_c1a_codex_verify.md` because this session is running in a read-only workspace. Report body:

# C1(a) Citation Verify for L1.G4 — Codex (gpt-5.4)
**Date**: 2026-04-26  
**Reviewer**: Codex (independent of Claude)  
**PDF**: arXiv:2011.04672, Chapters 9 + 4

## Per-Citation Verdict
1. Trace-distance DPI in KW Ch 9: **FAIL**

   Chapter 9 does not contain the trace-distance DPI theorem. Chapter 9 is **“Entanglement Measures”** on PDF p. 517 (printed p. 504), and on PDF p. 543 (printed p. 530) it only refers back to the earlier trace-distance DPI as Theorem 6.3.

   The actual theorem is **Theorem 6.3, “Data-Processing Inequality for Trace Distance”** in **Chapter 6**, PDF p. 278 (printed p. 265): "`let N be a positive, trace-non-increasing map`", followed by (6.1.9)
   \[
   \|\rho-\sigma\|_1 \ge \|N(\rho)-N(\sigma)\|_1.
   \]

   So the book supports the contraction fact, but the specific **Chapter 9** citation in §2 is inaccurate.

2. Partial trace is CPTP in KW Ch 4: **PASS**

   In **§4.4.2, “Trace and Partial-Trace Channels”**, PDF p. 171 (printed p. 158), the text states "`Tr_B is completely positive.`" The next sentence proves it is trace preserving via (4.4.7), so this is direct textual support that partial trace is CPTP.

3. Combination → L1.G4: **PASS**

   Taking \(N=\mathrm{Tr}_C\) in Theorem 6.3 and using §4.4.2 that partial trace is CPTP immediately gives
   \[
   \|\mathrm{Tr}_C(\rho)-\mathrm{Tr}_C(\sigma)\|_1 \le \|\rho-\sigma\|_1.
   \]

   This inference is immediate, but it uses **Chapter 6 + Chapter 4**, not **Chapter 9 + Chapter 4**.

## Aggregate Verdict for L1.G4 C1(a)
**FAIL**

The mathematical claim is supported by Khatri-Wilde, but the citation as written in [path_alpha_l1g4_closure_v0_1.md](/Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/path_alpha_l1g4_closure_v0_1.md:71) is not accurate: the relevant trace-distance DPI theorem is in **Chapter 6**, not **Chapter 9**.

## Note on Lemma Scope
The lemma statement itself stays within the trace-distance contraction claim: see [path_alpha_l1g4_closure_v0_1.md](/Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/path_alpha_l1g4_closure_v0_1.md:32) and [path_alpha_l1g4_closure_v0_1.md](/Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/path_alpha_l1g4_closure_v0_1.md:40). The scope carve-out is explicit at [path_alpha_l1g4_closure_v0_1.md](/Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/path_alpha_l1g4_closure_v0_1.md:58).

The application paragraph does rely on external assumptions such as \(\rho^{\Pi_{tr}}_{ABE'}=\mathrm{Tr}_C(\rho^\Pi_{ABCE})\) and \(\tau_E=\mathrm{Tr}_C(\tau_{CE})\), at [path_alpha_l1g4_closure_v0_1.md](/Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/path_alpha_l1g4_closure_v0_1.md:48) and [path_alpha_l1g4_closure_v0_1.md](/Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/path_alpha_l1g4_closure_v0_1.md:52), but those dependencies are named rather than silently discharged here. So this closure candidate does **not** close other path α sub-gaps and does **not** upgrade them from `[UNKNOWN]`.