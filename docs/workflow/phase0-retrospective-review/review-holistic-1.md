**Findings**
1. `FAIL` Milestone/scope coherence: the plan still hard-accepts MDI as `covered` (`docs/RESEARCH_PLAN.md:136`), but the implementation intentionally downgrades it to `partial` because generic multi-source state queries are missing (`qkdx/protocols/mdi.py:107`, `qkdx/protocol/base.py:160`, `183`). The `out_of_scope` hard gate itself is correct (`qkdx/numerics/wlc.py:105`; `tests/test_protocol/test_scope.py:146`), but M1-M2 scope discipline is not internally consistent until either the plan is updated or true multi-source support lands.

2. `FAIL` MDI five-tuple fidelity: the formulation doc says sifting requires basis match and Charlie success (`docs/msen/mdi-formulation.md:52`), but `_mdi_sift_keep` only checks Alice/Bob basis equality (`qkdx/protocols/mdi.py:82`). So `A` is not faithfully encoded; `p_sift=0.25` is injected separately instead of arising from the announcement rule.

3. `FAIL` WLC MOSEK-path exactness: the comment states regularization should be `(1-ε)G(ρ)+ετ`, but the code implements `G(ρ)+ετ` (`qkdx/numerics/wlc.py:173`). That changes trace and scales `D(G(ρ)\|\|Z(G(ρ)))`. The numerical impact is tiny at `1e-9`, but it is not the stated WLC formula and is untested here because MOSEK tests were skipped.

**Verdicts**
- **SCOPE_DISCIPLINE: FAIL**  
  `out_of_scope` blocking is correct and tested, but `covered` vs `partial` is not coherent across `RESEARCH_PLAN.md` and the current MDI implementation.

- **SCIENTIFIC_EVIDENCE: FAIL**  
  The Frank-Wolfe/BB84 Shor-Preskill comparison is valid for the symmetric model (`tests/test_numerics/test_wlc_bb84.py:35`, `87`, `128`), but the MOSEK branch is mathematically off at the regularization step.

- **MDI_FORMULATION: FAIL**  
  The virtual-EB `conditional_alice_bob` shortcut is acceptable for ideal M2, and `scope_tag="partial"` is defensible, but the announcement rule is semantically incomplete.

- **TEST_COVERAGE: FAIL**  
  Coverage is decent for fallback WLC and multi-source raises (`tests/test_protocols/test_mdi.py:32`, `79`; `tests/test_numerics/test_wlc_bb84.py:128`), but there is no regression on `_mdi_sift_keep`, no MOSEK-path test for the regularization bug, and no exact-value pinning beyond analytic `approx` checks.

- **ARCHITECTURE: FAIL**  
  The five-tuple is not cleanly separated from solver logic: protocols inject solver-private hooks (`qkdx/protocol/base.py:112`, `206`), while `wlc.py` derives `G` heuristically from `key_map` and ignores actual `network`/`announcement` semantics (`qkdx/numerics/wlc.py:151`, `215`, `528`).

Targeted execution in this environment: `tests/test_protocol/test_scope.py` passed `11/11`; `tests/test_protocols/test_mdi.py` passed `16/16`; `tests/test_numerics/test_wlc_bb84.py` passed `8`, skipped `9` because MOSEK was unavailable.