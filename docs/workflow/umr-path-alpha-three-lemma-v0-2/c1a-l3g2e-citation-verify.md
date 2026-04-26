**Verdict: FAIL**

**A. Cui per-trial verbatim accuracy**

[Cui PDF](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/pdfs/Cui 等 - 2019 - Twin-Field Quantum Key Distribution without Phase .pdf>) p. 2 does explicitly say `"per trial in a code mode"` before Eq. (3), so Cui’s `R` denominator is per trial.

But [path_alpha_l3g2e_closure_v0_1.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/path_alpha_l3g2e_closure_v0_1.md:85>) is not verbatim-clean on the Step 2-3 quote. Direct PDF read gives:
- Step 2.a: `If code mode is selected, Alice (Bob) ... sends ...`
- Step 3: `For each trial, the middle receiver Eve must publicly announce ...`

So the denominator claim is correct, but the stitched `"For each trial, ... Alice (Bob) sends ..."` quote is not an exact verbatim sentence from Cui.

**B. Pirandola per-network-use verbatim accuracy**

[Pirandola PDF](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/pdfs/Pirandola-2019-EndToEndCapacities.pdf>) main p. 2 says `"all the channels are used exactly once"` in a single end-to-end chain use.

SI Note 1 p. 15 says:
- `"The most general distribution protocol over the chain is based on adaptive LOs and unlimited two-way CC involving all the points in the chain"`
- `"This procedure completes the first use of the chain"`
- QKD rate is in `"bits per chain use"`.

SI Note 2 p. 20 says `"memoryless quantum channels"`, and p. 21 defines capacity per `"sequential use of the network or single-path transmission"`.

So B passes: Pirandola’s denominator is per chain/network use. For `N=1`, one use means one `A-C` transmission plus one `C-B` transmission, with Charlie’s processing inside the allowed LOCC structure.

**C. §2.3 resource table**

The first two rows are clean:
- `A→Charlie transmission` ↔ one `A-C` edge use
- `B→Charlie transmission` ↔ one `B-C` edge use

The last two rows are only partially faithful:
- Charlie’s measurement is admissible as a local operation inside Pirandola LOCCs.
- The announcement broadcast is admissible under unlimited two-way CC.

But Pirandola does not separately meter `"1 local op"` or `"1 CC use"` as denominator units. So [path_alpha_l3g2e_closure_v0_1.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/path_alpha_l3g2e_closure_v0_1.md:119>) is acceptable only as an implementation witness, not as exact counted-resource equality.

**D. Boundary with L3.G3 sub-residual 4**

This is the main failure.

The source workflow note says residual 4 is:
`one Cui trial is one Pirandola chain use / single-path network use`
and says it is `"about operational counting only"` [c1a-l3g3-gap-identification-round1.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/workflow/umr-path-alpha-three-lemma-v0-2/c1a-l3g3-gap-identification-round1.md:56>).

That is the same issue L3.G2.E is closing. So [path_alpha_l3g2e_closure_v0_1.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/path_alpha_l3g2e_closure_v0_1.md:140>) overstates the distinction. L3.G2.E is better described as splitting out former L3.G3 item 4, not as a non-equivalent precondition to it.

**E. §1.3 strict scope**

This part passes. [path_alpha_l3g2e_closure_v0_1.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/path_alpha_l3g2e_closure_v0_1.md:58>) keeps scope narrow, and §3 does not itself prove:
- `R_Cui ≤ R_Pirandola`
- the `ε` bridge
- LOPC syntax
- Eq. 11 specialization
- the final security conclusion

**F. Adjacent-gap smuggling**

Mostly clean.

§2/§3 do not derive `ι` legality, do not reopen L3.G2, and do not close the rest of L3.G3. [path_alpha_l3g2e_closure_v0_1.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/proofs/path_alpha_l3g2e_closure_v0_1.md:49>) assumes an already-given `ι(Π)=Π_tr` as framing, but does not try to prove it here.

The only real adjacent-gap problem is the bookkeeping in §2.4: it misclassifies former L3.G3 residual 4 rather than cleanly naming it as the issue being split out.

Concise summary: the underlying counting-unit alignment is supported by Cui and Pirandola, but the candidate is not source-clean yet. It needs three fixes before C1(a) PASS: correct the non-verbatim Cui Step 2-3 quote, weaken the LOCC/CC rows in the §2.3 table, and rewrite §2.4 so L3.G2.E is presented as the split-out former L3.G3 residual 4 rather than a distinct non-equivalent precondition.