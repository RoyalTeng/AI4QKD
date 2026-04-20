## ARCHITECTURE_FIT

- As a **module shape**, [pm_qkd.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/analytic/pm_qkd.py:1>) fits the existing `qkdx/analytic` pattern: immutable params, pure helper formulas, and a sweep helper, which is consistent with [decoy.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/analytic/decoy.py:1>), [mdi_decoy.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/analytic/mdi_decoy.py:248>), and [gllp.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/analytic/gllp.py:1>). It is the right abstraction level **for an analytic helper layer**.
- As an **F6 milestone artifact**, it does **not** match the planned layer. The surrounding docs expected `qkdx/protocols/pm_qkd.py`, not only an analytic surrogate: see [TF-QKD.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/TF-QKD.md:171>) and [pm_qkd_formulation.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/msen/pm_qkd_formulation.md:5>).
- The main architectural risk is semantic, not structural: [pm_phase_error_upper](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/analytic/pm_qkd.py:190>) is named like a rigorous decoy bound, but unlike [decoy.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/analytic/decoy.py:1>) it is an honest-behavior estimate with inferred `Y_1`, not a decoy inversion. That is acceptable for a temporary simulator, but dangerous as a reusable lower-bound primitive.

## RESEARCH_PLAN_COMPLIANCE

- This is legitimate **Sub-Q2 progress**: it advances the TF family from pure documentation toward executable lower-bound tooling, which is aligned with RESEARCH_PLAN Sub-Q2’s intent to map known family lower bounds.
- It is **not full compliance** with the F6 upgrade path in your own docs. The plan path was memo -> formulation -> protocol implementation -> slope/anchor acceptance -> broader family work, not “analytic helper alone closes §7.3”: [TF-QKD.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/literature/TF-QKD.md:165>) and [pm_qkd_formulation.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/msen/pm_qkd_formulation.md:223>).
- The patch introduces a mild scope drift by changing the PM row in [tfqkd_family.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/families/tfqkd_family.md:175>) from earlier literature-memo language of `rel=0.05` figure matching to a slope-only pass. That downgrade is defendable as “first pass,” but it should be recorded as a downgrade, not as a hard acceptance closure.

## LITERATURE_FIDELITY

- The **Eq. 4 composition** in [pm_asymptotic_rate](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/analytic/pm_qkd.py:265>) is faithful to Ma-Zeng-Zhou 2018’s asymptotic PM-QKD form ([PRX 2018](https://journals.aps.org/prx/abstract/10.1103/PhysRevX.8.031043)). The end-to-end `η_channel -> sqrt(η_channel)` handling is also conceptually right for the PM/TF topology.
- The **gain implementation** looks physically consistent after the dark-limit fix, but the prose is sloppy: the module header and test docstring still print the earlier wrong squared-factor formula at [pm_qkd.py:23](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/analytic/pm_qkd.py:23>) and [test_pm_qkd.py:60](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/tests/test_analytic/test_pm_qkd.py:60>).
- The weak point is **Eq. 2 fidelity**. Ma Eq. 2 is a decoy-state bound over odd/even photon components; your own formulation note says it requires decoy-estimated `q_k`/`Y_k` bounds, not just signal-gain back-substitution: [pm_qkd_formulation.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/msen/pm_qkd_formulation.md:113>). [pm_phase_error_upper](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/qkdx/analytic/pm_qkd.py:190>) truncates to `q0` and `q1`, infers `Y_1` from `Q_mu`, and absorbs the rest into a worst-case complement. That is a heuristic honest-behavior upper bound, not a faithful transcription of the paper’s decoy procedure.
- On the Round-4 formulation fix, the code is **not contradicting** the `R_A` conditioning-vs-tracing correction, but it also does not exercise it. The whole source-state layer is bypassed, so the fix lives only in [pm_qkd_formulation.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/msen/pm_qkd_formulation.md:46>), not in executable protocol semantics.

## COMPLETENESS

- The scope limit is stated in prose, but the presentation still over-signals completion. The PM row in [tfqkd_family.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/families/tfqkd_family.md:175>) is visually “passed,” while the same section admits a 1-2 order absolute-rate gap and defers the real work to §7.5.
- The implemented tests are materially weaker than the formulation doc’s original intent. [pm_qkd_formulation.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/msen/pm_qkd_formulation.md:177>) planned slope plus explicit Fig. 3a anchor checks; the actual test file only gives slope and a loose one-point order-of-magnitude check at 50 dB in [test_pm_qkd.py](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/tests/test_analytic/test_pm_qkd.py:218>).
- The real path to F6 status is still: `qkdx/protocols/pm_qkd.py` protocol builder, explicit decoy inversion, figure-anchor regression, and a documented decision on whether Fock-truncation ADR is a prerequisite for `covered`: [pm_qkd_formulation.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/msen/pm_qkd_formulation.md:232>).

## PROSPECTUS_BEARING

- This patch has real value for **Sub-Q2**: it gives F6 a coded `sqrt(η)` anchor, so the BB84/MDI `η` vs TF-family `sqrt(η)` narrative is no longer only documentary.
- It is **not yet sufficient** for quantitative **Sub-Q3** bridging. With the current heuristic `E_mu^X`, the PM curve is good enough for qualitative scaling discussion, but not good enough to support serious PLOB/Pirandola gap attribution.
- The bridge is therefore partial: it prepares the lower-bound side of the testbed described in [PROSPECTUS.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/PROSPECTUS.md:221>) and [pm_qkd_formulation.md](</Users/tengjun/Desktop/ai4qkd (1)/AI4QKD/docs/msen/pm_qkd_formulation.md:196>), but the benchmark is not yet numerically trustworthy.

## RECOMMENDATIONS

- **First priority:** do **F6 §7.5 depth-first**, meaning full PM decoy inversion and protocol-layer integration before anything else. That closes the biggest fidelity gap.
- **Do not do §7.6 Pareto yet.** Optimizing over a heuristic PM bound will produce attractive but unreliable family-frontier data.
- **SNS should come after PM rigor**, not before. Breadth is less valuable than turning PM into a trustworthy anchor.
- **Project-level pivot:** if solver access for Stage 2 can realistically be unblocked, Kamin/S2.5 is still the higher-value milestone because it closes a genuine hard acceptance. If that blocker remains real, stay on F6 but spend the next cycle on PM rigor, not SNS breadth or Pareto cosmetics.

Review based on patch and document inspection; I did not execute the test suite in this read-only sandbox.