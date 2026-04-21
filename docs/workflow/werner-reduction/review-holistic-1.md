**ALIGNMENT_WITH_RESEARCH_PLAN**
- Partial only. The memo does behave like a `proofs/<topic>.md` deliverable under [docs/RESEARCH_PLAN.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/RESEARCH_PLAN.md:39>): it has explicit assumptions, a push-through proof chain, limitations, bearing, and sanity checks.
- It does **not** cleanly complete the advertised “Level 3 → Level 4” jump in [docs/RESEARCH_PLAN.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/RESEARCH_PLAN.md:145>) because the core swap step W2 is still recalled rather than rederived in [docs/proofs/mdi_werner_reduction.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/mdi_werner_reduction.md:101>).
- Against the §7.1 literature-template yardstick, it has proof notes / limitations / bearing, but it lacks an explicit concept map and explicit “key results” section; that is a structure gap, not a fatal one.

**RIGOR_DISCIPLINE**
- Overall label **[CONJ]** is correct and appropriately conservative in [mdi_werner_reduction.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/mdi_werner_reduction.md:3>) and [mdi_werner_reduction.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/mdi_werner_reduction.md:198>).
- W2 as **[RECALLED]** is appropriate.
- W1 and W3 as **[THM]** are **not** appropriate under [CLAUDE.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/CLAUDE.md:52>) / [CLAUDE.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/CLAUDE.md:64>): they are AI-session derivations or textbook facts, not already-upgraded theorem-grade claims.
- The memo also muddies the invariant by saying existing tests “已提供 C1(c)” in [mdi_werner_reduction.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/mdi_werner_reduction.md:236>). That is too strong: those tests are same-codebase consistency checks, not clearly an independent non-AI reproduction per [docs/RESEARCH_PLAN.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/RESEARCH_PLAN.md:63>) and [docs/research/RETRACTION.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/research/RETRACTION.md:141>).

**SCOPE_HYGIENE**
- A1-A5 are mostly intelligible and bounded.
- A6 is not auditable as written. [mdi_werner_reduction.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/mdi_werner_reduction.md:33>) says diagonal basis “仅接受 `Ψ^-`”, but Table I in [LoCurtyQi-2012-MDI-QKD.pdf](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/literature/pdfs/LoCurtyQi-2012-MDI-QKD.pdf>) keeps successful `Ψ^-` and `Ψ^+` outcomes and changes the flip rule, matching [docs/literature/MDI-QKD.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/literature/MDI-QKD.md:89>) and [docs/literature/MDI-QKD.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/literature/MDI-QKD.md:104>).
- A4 compresses too much experimental detail into “ideal BSM”. For an experimentalist, detector efficiency, dark counts, HOM indistinguishability, and polarization alignment should be broken out separately.

**CITATION_TRUSTWORTHINESS**
- The Lo-Curty-Qi Appendix A virtual-EB support is verifiable. The quoted Appendix A language in [mdi_werner_reduction.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/mdi_werner_reduction.md:58>) is present in the local PDF’s Appendix A.
- However, the implementation docstring cites “Lo-Curty-Qi §II” in [qkdx/numerics/kamin_sdp_mdi.py](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/qkdx/numerics/kamin_sdp_mdi.py:24>), while the memo’s actual support comes from Appendix A. That mismatch should be called out explicitly.
- The repeater-literature family is a reasonable place to look for the Werner-under-swap formula, but the memo’s **exact equation pointers are not trustworthy**. External check shows the relevant Briegel 1998 expression is Eq. (5) specialized to perfect operations and `L=2`, not Eq. (8); and Dür et al. 1999 Eq. (12) is a purification-fixpoint formula, not the cited swap formula. So W2 should remain `[RECALLED]` until the exact supporting equation is corrected and verified.

**UPGRADE_PATH_CLARITY**
- §7.2 in [mdi_werner_reduction.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/mdi_werner_reduction.md:251>) mostly matches the R0.2 invariant: C1 plus C2 plus C3, with C1 satisfied by one of `(a)/(b)/(c)`.
- It is not fully clean because the memo elsewhere suggests C1(c) may already be partially satisfied, which weakens the exact “current state” picture.
- The phrase “用户 2026-04-21 session 签字” in [mdi_werner_reduction.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/mdi_werner_reduction.md:20>) should be changed; under [CLAUDE.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/CLAUDE.md:35>), “签字” is loaded C2 language.

**PROJECT_CONTEXT**
- This part is mostly correct. The memo keeps itself in Sub-Q1/Sub-Q2 infrastructure territory and says it does not change the umr upper-bound status in [mdi_werner_reduction.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/mdi_werner_reduction.md:272>) and [mdi_werner_reduction.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/mdi_werner_reduction.md:278>).
- It does not misstate FINDINGS v2’s umr upper bound; that remains **[CONJ]** in [docs/research/FINDINGS.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/research/FINDINGS.md:47>) and [docs/research/FINDINGS.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/research/FINDINGS.md:58>).

**NEW_REGRESSIONS**
- A6 introduces a new inconsistency against both the primary source and the prior literature memo.
- The memo cites a nonexistent test file at [mdi_werner_reduction.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/proofs/mdi_werner_reduction.md:232>): `tests/test_numerics/test_kamin_mdi.py` should be `tests/test_numerics/test_kamin_sdp_mdi.py`.
- The `[THM]` self-grading on W1/W3 and the “已提供 C1(c)” wording reintroduce the same kind of premature-upgrade pressure that [docs/research/RETRACTION.md](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/research/RETRACTION.md:32>) warns against.

**VERDICT**
FAIL. The memo is directionally good and substantially more honest than the project’s retracted overclaim precedents: the overall `[CONJ]` label is right, the document clearly limits its scope, and it does not disturb FINDINGS v2 / Log 07 on umr upper bounds. But it is not yet ready for the “pending user review for C1 + C2” state because several audit-critical details are still wrong or too loose: A6 misreads Table I, the W2 supporting citations use incorrect equation pointers, W1/W3 are graded too high under R0.3, the memo overstates same-code numerical checks as possible C1(c), and one evidence link is broken.

**RECOMMENDATIONS**
- Fix A6 to reflect Table I exactly: same-basis + successful Bell outcome kept; classical flip rule depends on `Ψ^-` vs `Ψ^+`.
- Downgrade W1/W3 from `[THM]` to a non-upgraded label unless you can tie them to verified theorem-grade source statements and still keep the overall file at `[CONJ]`.
- Replace the W2 citation trail with exact verified support: Briegel 1998 Eq. (5) with perfect operations and `L=2`, and if keeping Dür 1999, use the actual connection formula rather than Eq. (12).
- Remove or soften all “C1(c) already provided” wording; say “same-code numerical consistency only, not independent validation.”
- Replace “用户签字” at line 20 with wording that cannot be confused with C2.
- Correct the broken test-file path.

**Sources**
- [LoCurtyQi-2012-MDI-QKD.pdf](</Users/tengjun/Desktop/ai4qkd%20(1)/AI4QKD/docs/literature/pdfs/LoCurtyQi-2012-MDI-QKD.pdf>)
- [Briegel et al. 1998 PDF](https://people.ee.duke.edu/~jungsang/ECE590_01/BriegelPRL1998.pdf)
- [Dür et al. 1999 PDF](https://arxiv.org/pdf/quant-ph/9808065)