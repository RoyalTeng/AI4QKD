# F6 PM-QKD Analytic Review — Workflow Log

**Mode**: review-only
**Base**: 6db6d97^ (= d967187, fix(phase1): Round 2-4 dev-reviewer response)
**Head**: HEAD (= 6db6d97, feat(analytic): PM-QKD analytic key rate)
**Scope**: 1 commit — F6 §7.3 PM-QKD analytic first pass

## Commit under review

- 6db6d97 feat(analytic): PM-QKD analytic key rate (F6 §7.3 first pass)

## Patch summary (v1)

- 4 files, 612 insertions, 5 deletions
- Code: qkdx/analytic/pm_qkd.py (328 lines), tests/test_analytic/test_pm_qkd.py (226 lines)
- Docs: docs/families/tfqkd_family.md (§5.2 update), docs/PHASE1_LOG.md (§4.11 new entry)

## Round 1 (base = 6db6d97^)

- Agent 1 diff: **FAIL** — 2 major (M1 E_Z BB84-style vs Ma B22; M2 Y_1 override unsafe) + 2 minor
- Agent 2 holistic: architecture fit OK for analytic helper; plan-row downgrade not marked; Eq.2 fidelity weak

### Round 2 fixes

- M1: Rewrote to Ma Appendix B exact forms
  - Q_μ = (1-p_d)·[1 − (1-2p_d)·e^{-η·μ}]  (B14)
  - Y_k = 1 − (1-2p_d)·(1-η)^k  (B13; new helper pm_k_photon_yield)
  - e_δ = π/M − (M²/π²)·sin³(π/M)  (B19; new helper pm_phase_slice_error_rate)
  - E_Z = (p_d + η·μ·e_δ)·e^{-η·μ} / Q_μ  (B22)
  - e_d → e_delta renamed to match Ma convention
- M2 (Round 2 try): renamed Y_1 → Y_1_lower with optional Y_1_honest_check
- minor-1: +15 formula-pinned regression tests
- minor-2: docstrings synced
- holistic: tfqkd_family.md PM row marked 🟡 partial (下调口径), not hard-pass
- Tests: 20 → 35 pass; log-log slope 0.5393

## Round 2 review

Verdict: **REJECTED** (1 critical + 1 minor)
- CRITICAL M2 residual: Y_1_honest_check optional → caller could still break UB by
  passing optimistic Y_1_lower without check. At 100 km, Y_1_lower=10·honest drops
  E_X 0.270 → 0.111.
- MINOR: mu≤0 early return didn't clamp e_0 → documented [0, 0.5] UB violated if caller passes e_0 > 0.5.

### Round 3 fixes

- M2 (Round 3 try): Y_1_honest_check → Y_1_upper_check renamed and made MANDATORY when Y_1_lower non-None. Reject ValueError if upper_check missing.
- Added +3 regression tests (mandatory check, clamp fix, "optimistic rejected" test)
- Fixed mu≤0 clamp: return min(max(e_0, 0.0), 0.5)
- Tests: 35 → 38 pass

## Round 3 review

Verdict: **REJECTED** (1 critical)
- CRITICAL: Mandatory Y_1_upper_check is VACUOUS — caller can trivially pass Y_1_upper_check=1.0 (Y_1 ≤ 1 always) and then any Y_1_lower ∈ [0, 1] passes.
  Concrete exploit at 100 km: Y_1_lower=1e-3, Y_1_upper_check=1.0 → E_X 0.270 → 0.025 (10× reduction below fallback).

### Round 4 fixes (definitive)

Removed Y_1_lower and Y_1_upper_check entirely from public API of pm_phase_error_upper. The library now ALWAYS uses the internal conservative fallback Y_1 ≈ max(0, (Q_μ - Y_0)/μ). Decoy-state tighter bounds move to §7.5+ separate module.
- New public signature: pm_phase_error_upper(mu, Q_mu, Y_0, e_0=0.5, e_delta=0.0)
- Full input validation
- pm_asymptotic_rate updated to match
- Replaced 3 old Y_1_lower tests with 3 new: test_no_y1_lower_public_param (signature check), test_fallback_is_single_return_path, test_input_validation_complete
- Class docstring updated
- Tests: 38 → 37 pass
- Numerical sanity: log-log slope 0.519 (target 0.5 ± 0.05 ✓)

## Round 4 review

Verdict: **PASS** ✓
- Round 3 bypass closed; no caller-controlled Y_1 path remains
- Minor: stale class docstring (fixed post-review)

## Codex review infrastructure notes (Round 3 incidents)

Two 45+ minute codex `codex exec` hangs while running Round 3 review. Killed via pkill after ~1 hour each. Root cause unclear (possibly Anthropic API rate limiting / backend issue). Pivoted to minimal config (no -m, no --output-schema, no -c reasoning_effort) which completed in < 2 min. Recommend keeping minimal config as the default for review retries.

## Final status

4 rounds total (1 initial + 3 fix rounds). Verdict: **PASS**.
Tests: 37 pm_qkd tests all pass. log-log slope 0.519. No regressions.

Path taken:
- Round 1-2: research formulas alignment (Ma Appendix B structure)
- Round 3-4: public API safety (removed unsafe Y_1_lower override)

Stage 2 (full multi-intensity decoy inversion + protocol builder) deferred to §7.5+ per tfqkd_family.md upgrade path.
