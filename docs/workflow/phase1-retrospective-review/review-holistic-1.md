`CLAUDE.md` is not present in the workspace, so this review is based on the other requested docs, the touched files, and the primary PDFs in `docs/literature/pdfs/`.

## ARCHITECTURE_FIT

- High: `[kamin_geat.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/finite_key/kamin_geat.py:194>)` does not cleanly match the existing `finite_key` role yet, because `bb84_qubit_finite_key_length()` sets `h` to a net asymptotic key rate that already includes EC leakage, then subtracts `lambda_EC` again in Theorem 3 form (`[kamin_geat.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/finite_key/kamin_geat.py:249>)`). That is a semantic mismatch with the paper formula and likely explains the overly pessimistic cutoffs and the optimizer collapsing to the grid boundary.
- Medium: the file placement itself is reasonable. A paper-scoped analytic module next to `[gll_renner.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/finite_key/gll_renner.py:1>)` is consistent with the current repo style: flat functional helpers, explicit scope notes, no premature abstractions.
- Medium: the naming is architecturally muddy. `[kamin_geat.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/finite_key/kamin_geat.py:1>)` and `[Kamin-2025.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/Kamin-2025.md:32>)` use “PM-QKD” to mean prepare-and-measure, while F6 uses PM-QKD to mean phase-matching QKD. In this codebase that collision is costly.
- Positive: `[pm_qkd_formulation.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/msen/pm_qkd_formulation.md:10>)` largely follows the pattern of `[mdi-formulation.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/msen/mdi-formulation.md:10>)`: scope box, five-tuple mapping, sift derivation, WLC interface, limitations, and next steps. Structurally it fits.

## RESEARCH_PLAN_COMPLIANCE

- S2.4 is on-plan. The Metger memo in `[GEAT-2024.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/GEAT-2024.md:1>)` covers the plan’s requested theorem assumptions, EAT comparison, and QKD applicability path, matching `RESEARCH_PLAN §3.3 S2.4` (`[RESEARCH_PLAN.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/RESEARCH_PLAN.md:292>)`).
- S2.5 is only partial progress, not closure. The new `qkdx/finite_key/` layer is a valid preparation step, but the hard acceptance in `RESEARCH_PLAN §3.3 S2.5` is still decoy-state BB84 reproduction with `< 5%` error plus a notebook (`[RESEARCH_PLAN.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/RESEARCH_PLAN.md:301>)`). Those are not present.
- Medium: `[PHASE1_LOG.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/PHASE1_LOG.md:494>)` overstates alignment by arguing qubit Fig. 1 can satisfy the S2.5 acceptance “in spirit.” The plan text is more specific than that.
- F6 work is sensible groundwork, but still groundwork. `RESEARCH_PLAN §2.7` asks for `tfqkd-formulation.md` plus protocol code and slope validation (`[RESEARCH_PLAN.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/RESEARCH_PLAN.md:244>)`). This patch adds a TF-family memo and a PM-specific formulation doc, which is useful, but it is not the planned M4B closure.

## LITERATURE_FIDELITY

- High: `[GEAT-2024.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/GEAT-2024.md:4>)` mis-cites the companion paper. It says `[MR22]` is the “same arXiv number” as GEAT, but the two are distinct papers. That is a factual citation error, not just formatting.
- High: `[Kamin-2025.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/Kamin-2025.md:34>)` is materially confusing because it frames Kamin 2025 as “PM-QKD” in the phase-matching sense, while the paper is about prepare-and-measure and decoy-state BB84. In this repo, that wording bleeds into F6 semantics.
- Medium: `[Kamin-2025.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/Kamin-2025.md:311>)` and `[PHASE1_LOG.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/PHASE1_LOG.md:494>)` say the paper has no Table 1. The PRX Quantum paper does have a Table 1; it is just not a benchmark table. The current wording is too absolute.
- Medium: `[TF-QKD.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/TF-QKD.md:223>)` attributes a round-independence limitation to Wang-Yu-Hu 2018 that I could not substantiate from the paper passages I checked. Safer wording would be that the paper resolves the original phase-announcement issue by removing Z-basis postselection and using a virtual-protocol argument, without adding an unsupported attack-class claim.
- Positive: the Lucamarini “security beyond scope,” Wang’s “traditional decoy-state method does not apply to the original protocol / >45% misalignment tolerance,” and Ma’s `d=2 + phase randomization` / Eq. 4 / “far away from single-repeater bound” readings are faithful.

## COMPLETENESS

- Positive: the Stage 1 scope boundary is explicit in code and log. `[kamin_geat.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/finite_key/kamin_geat.py:15>)` clearly excludes Theorem 4 SDP and decoy-state SDP, and `[PHASE1_LOG.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/PHASE1_LOG.md:617>)` explicitly records `var_f = 1` and boundary-grid conservatism.
- High: the limitation story is still incomplete. The log currently attributes the high-loss gap mainly to `var_f = 1` (`[PHASE1_LOG.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/PHASE1_LOG.md:617>)`), but the code likely also double-counts EC leakage. That second source of conservatism is more consequential and should be documented or corrected before treating Stage 1 numbers as a clean baseline.
- Medium: the tests are broad sanity tests, not formula-pin tests. `[test_kamin_geat.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/tests/test_finite_key/test_kamin_geat.py:213>)` allows wide rate bands and does not guard the `h`/`λ_EC` separation. That is not enough for a research anchor.
- Verification note: `pytest` could not run in this sandbox because no writable temp directory exists, but direct Python imports and function evaluation succeeded.

## PROSPECTUS_BEARING

- Sub-Q1/Sub-Q2: the F6 memo plus PM formulation materially help the “can MS-EB express the TF family?” and “how do we parameterize the TF family?” questions in `[PROSPECTUS.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/PROSPECTUS.md:170>)` and `[PROSPECTUS.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/PROSPECTUS.md:195>)`.
- Sub-Q2 finite-key bridge: the new `finite_key` layer is the right architectural slot for Prospectus Phase 1 finite-key work (`[PROSPECTUS.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/PROSPECTUS.md:152>)`), but the bridge is not yet reliable enough for family-level finite-key comparison because S2.5 hard reproduction is unfinished and the Stage 1 BB84 semantics likely need correction.
- Sub-Q3/Sub-Q4: the TF/PM documents correctly point toward PLOB/Pirandola gap work, but the bridge the Prospectus actually needs is still missing: a topology-specific applicability argument for “two parties + untrusted relay,” not just reuse of direct-link bounds (`[PROSPECTUS.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/PROSPECTUS.md:221>)`).
- Net: this patch improves the lower-bound side and the family-coverage side, but the upper-bound/topology seam remains open. That is the main Phase-bridging gap.

## RECOMMENDATIONS

- 1. Stage 2 SDP first. Fix the `kamin_geat.py` semantics, then implement Theorem 4 / dual-derived min-tradeoff machinery. That is the shortest path to a defensible S2.5 acceptance result.
- 2. PM-QKD implementation second. `[pm_qkd_formulation.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/msen/pm_qkd_formulation.md:199>)` is detailed enough that `qkdx/protocols/pm_qkd.py` is the natural next executable milestone for F6.
- 3. Sub-Q3 PLOB third. Start with a topology-admissibility memo or lemma before any upper-bound numerics; otherwise the Prospectus bridge to Sub-Q3/Sub-Q4 stays speculative.

Sources used for literature checks: [Metger et al. 2024](https://link.springer.com/article/10.1007/s00220-024-05121-4), [Kamin et al. 2025 / PRX Quantum 6:020342](https://journals.aps.org/prxquantum/abstract/10.1103/PRXQuantum.6.020342), [Ma-Zeng-Zhou 2018](https://journals.aps.org/prx/abstract/10.1103/PhysRevX.8.031043), [Wang-Yu-Hu 2018](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.98.062323), [Lucamarini et al. 2018](https://www.nature.com/articles/s41586-018-0066-6).