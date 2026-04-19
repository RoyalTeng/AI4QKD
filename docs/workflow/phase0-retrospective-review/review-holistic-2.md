**Overall: FAIL**

| Dimension | Verdict | Evidence |
|---|---|---|
| `RESEARCH_PLAN` alignment | PASS | `docs/RESEARCH_PLAN.md:137` now marks MDI as `partial`, matching `qkdx/protocols/mdi.py:107-113,153-160` and `tests/test_protocols/test_mdi.py:22-26`. |
| Scope-doc propagation | FAIL | The downgrade did not propagate to other scope docs: `docs/framework_coverage.md:36,139` still says MDI is `covered`, and `docs/PHASE0_REPORT.md:79,110` still says `covered` / “4 协议族 covered”. |
| WLC regularization fix | PARTIAL | `qkdx/numerics/wlc.py:173-176` now uses `(1-eps)G(ρ)+eps·τ`, which is the correct trace-preserving convex combination. But `wlc_key_rate()` still has no explicit `0 <= epsilon_regularization < 1` validation at `qkdx/numerics/wlc.py:81-89`, and I found no regression test that would catch a reversion. |
| `_mdi_sift_keep` branch coverage | PASS | The new tests in `tests/test_protocols/test_mdi.py:139-155` correctly cover same-basis, different-basis, and too-short tuples. |
| `_mdi_sift_keep` semantics | FAIL | The helper itself (`qkdx/protocols/mdi.py:82-86`) only checks `θ_A == θ_B`. The formulation doc requires `θ_A == θ_B` **and** Charlie success `r != fail` (`docs/msen/mdi-formulation.md:52-55`). So the helper is not semantically complete; Charlie’s announcement is being ignored and only compensated indirectly via `p_sift=0.25` / `_conditional_alice_bob` (`qkdx/protocols/mdi.py:68-73`). |

Runtime note: I could not run `pytest` in this sandbox because no usable temporary directory exists, so this review is source-based.