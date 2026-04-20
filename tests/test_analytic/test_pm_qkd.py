"""Tests for PM-QKD analytic key-rate helpers (Ma-Zeng-Zhou 2018).

Reference:
    - Ma, X., Zeng, P., Zhou, H. (2018). Phase-Matching Quantum Key Distribution.
      PRX 8:031043.  arXiv:1805.05538v3.
    - docs/literature/TF-QKD.md §4.3 (Level 3 memo)
    - docs/msen/pm_qkd_formulation.md (v0.1 Round 4)

Scope (F6 §7.3 first pass):
    - Ma Eq. 4 asymptotic per-pulse key rate
    - Ma Eq. 2 decoy-based phase-error upper bound
    - log-log R ∝ √η acceptance (tfqkd_family.md §5.2, slope 0.5 ± 0.05)
    - Ma Fig. 3a spot-check at 100-300 km

Not in scope (§7.5+):
    - Protocol builder `build_pm_qkd_protocol` (separate module)
    - Discrete phase slicing effects on source state
    - Asymmetric μ_a ≠ μ_b
"""
from __future__ import annotations

import math

import pytest

from qkdx.analytic.pm_qkd import (
    PmQkdParams,
    pm_asymptotic_rate,
    pm_charlie_gain,
    pm_k_photon_yield,
    pm_phase_error_upper,
    pm_phase_slice_error_rate,
    pm_qkd_sweep_vs_loss,
    pm_single_photon_yield,
)


class TestPmQkdParams:
    def test_defaults_match_ma_fig3b(self):
        # Ma Fig. 3b: p_d = 8e-8, η_d = 14.5%, f = 1.15, M = 16, e_d = 1.5%
        p = PmQkdParams()
        assert p.p_d == pytest.approx(8e-8, rel=1e-12)
        assert p.eta_det == pytest.approx(0.145, rel=1e-12)
        assert p.f_ec == pytest.approx(1.15, rel=1e-12)
        assert p.M == 16
        assert p.e_delta == pytest.approx(0.015, rel=1e-12)

    def test_invalid_eta_rejected(self):
        with pytest.raises(ValueError):
            PmQkdParams(eta_det=1.5)

    def test_invalid_M_rejected(self):
        with pytest.raises(ValueError):
            PmQkdParams(M=3)  # need M ≥ 4 and even

    def test_f_ec_below_one_rejected(self):
        with pytest.raises(ValueError):
            PmQkdParams(f_ec=0.9)


class TestPmCharlieGain:
    """Ma Appendix B Eq. B14 (exact form):
        Q_μ = (1 − p_d) · [1 − (1 − 2·p_d) · e^{−η·μ}]

    Limits:
        - η → 0: Q_μ → (1-p_d)·[1 - (1-2p_d)] = 2·p_d·(1-p_d) = Y_0 (Eq. B13 k=0)
        - η·μ → ∞: Q_μ → (1-p_d) (saturated, not 1 since p_d can suppress one detector)
        - Small (η·μ, p_d): Q_μ ≈ η·μ + 2·p_d (linear leading-order)
    """

    def test_ma_B14_exact_form(self):
        # Formula-pinned regression test against Ma Eq. B14
        mu, eta, p_d = 0.3, 1e-3, 1e-6
        expected = (1.0 - p_d) * (1.0 - (1.0 - 2.0 * p_d) * math.exp(-eta * mu))
        assert pm_charlie_gain(mu=mu, eta_total=eta, p_d=p_d) == pytest.approx(expected, rel=1e-12)

    def test_zero_dark_zero_loss(self):
        q = pm_charlie_gain(mu=0.1, eta_total=1.0, p_d=0.0)
        assert 0.0 < q <= 1.0

    def test_saturates_at_high_eta_mu(self):
        # Ma B14: η·μ → ∞ gives Q_μ → (1 − p_d), not 1
        p_d = 1e-5
        q = pm_charlie_gain(mu=100.0, eta_total=1.0, p_d=p_d)
        assert q == pytest.approx(1.0 - p_d, rel=1e-8)

    def test_monotone_mu(self):
        q_small = pm_charlie_gain(mu=0.01, eta_total=1e-3, p_d=1e-8)
        q_big = pm_charlie_gain(mu=0.1, eta_total=1e-3, p_d=1e-8)
        assert q_big > q_small

    def test_zero_mu_reduces_to_y0(self):
        # μ = 0: Q_μ → Y_0 (Ma B13 k=0) = 2·p_d·(1-p_d)
        q = pm_charlie_gain(mu=0.0, eta_total=0.5, p_d=1e-5)
        expected = 2.0 * 1e-5 * (1.0 - 1e-5)
        assert q == pytest.approx(expected, rel=1e-6)

    def test_invalid_eta_raises(self):
        with pytest.raises(ValueError):
            pm_charlie_gain(mu=0.1, eta_total=1.5, p_d=0.0)


class TestPmKPhotonYield:
    """Ma Eq. B13: Y_k = 1 − (1 − 2·p_d) · (1 − η)^k.

    Limits:
        - k = 0: Y_0 = 2·p_d (vacuum yield; only dark counts contribute)
        - k = 1: Y_1 = 1 - (1-2p_d)·(1-η) = η + 2p_d·(1-η)
        - η → 0: Y_k → 2·p_d for all k
        - η → 1: Y_k → 1
    """

    def test_k_zero_gives_dark(self):
        p_d = 1e-5
        assert pm_k_photon_yield(k=0, eta_total=0.5, p_d=p_d) == pytest.approx(2.0 * p_d, rel=1e-9)

    def test_k_one_matches_B13(self):
        eta, p_d = 1e-3, 1e-6
        expected = 1.0 - (1.0 - 2.0 * p_d) * (1.0 - eta)
        assert pm_k_photon_yield(k=1, eta_total=eta, p_d=p_d) == pytest.approx(expected, rel=1e-12)

    def test_high_eta_saturates(self):
        # η → 1: Y_k → 1 for all k (≥ 1)
        assert pm_k_photon_yield(k=3, eta_total=1.0, p_d=0.0) == pytest.approx(1.0, rel=1e-12)

    def test_k_monotone_eta(self):
        y1 = pm_k_photon_yield(k=1, eta_total=0.1, p_d=1e-6)
        y1_bigger = pm_k_photon_yield(k=1, eta_total=0.5, p_d=1e-6)
        assert y1_bigger > y1


class TestPmPhaseSliceErrorRate:
    """Ma Eq. B19: e_δ = π/M − (M²/π²) · sin³(π/M) — phase-slice discretization error."""

    def test_M_16_matches_ma_formula(self):
        # For M=16: π/M ≈ 0.1963, sin³(π/M) ≈ 0.00743, M²/π² ≈ 25.94
        # e_δ = 0.1963 − 25.94·0.00743 ≈ 0.0035
        e = pm_phase_slice_error_rate(M=16)
        expected = math.pi / 16 - (16 ** 2 / math.pi ** 2) * math.sin(math.pi / 16) ** 3
        assert e == pytest.approx(expected, rel=1e-12)
        # Sanity: small positive for M=16
        assert 0.0 < e < 0.01

    def test_large_M_vanishes(self):
        # M → ∞: π/M → 0, sin³(π/M) ≈ (π/M)³, so e_δ → π/M − M²/π²·(π/M)³
        # = π/M − π/M = 0 → e_δ → 0 quickly
        e_small = pm_phase_slice_error_rate(M=256)
        assert e_small < 1e-5

    def test_invalid_M_raises(self):
        with pytest.raises(ValueError):
            pm_phase_slice_error_rate(M=3)


class TestPmBitErrorRate:
    """Ma Eq. B22 (honest-behavior approximation):
        E_μ^Z ≈ (p_d + η·μ·e_δ) · e^{-η·μ} / Q_μ
    """

    def test_ma_B22_exact_form(self):
        # Formula-pinned at concrete operating point
        from qkdx.analytic.pm_qkd import pm_bit_error_rate
        mu, eta, p_d, e_delta = 0.3, 4.58e-4, 8e-8, 0.015
        Q_mu = (1 - p_d) * (1 - (1 - 2 * p_d) * math.exp(-eta * mu))
        expected = (p_d + eta * mu * e_delta) * math.exp(-eta * mu) / Q_mu
        got = pm_bit_error_rate(mu=mu, eta_total=eta, p_d=p_d, e_delta=e_delta)
        assert got == pytest.approx(expected, rel=1e-10)

    def test_zero_misalignment_dark_limit(self):
        # e_δ = 0, μ small: E_Z = p_d·e^{-η·μ} / Q_μ ≈ p_d / (η·μ + 2·p_d)
        from qkdx.analytic.pm_qkd import pm_bit_error_rate
        e = pm_bit_error_rate(mu=1e-3, eta_total=0.5, p_d=1e-4, e_delta=0.0)
        # Q_μ ≈ η·μ + 2·p_d = 5e-4 + 2e-4 = 7e-4
        # E_Z ≈ 1e-4 / 7e-4 ≈ 0.143
        assert e == pytest.approx(1e-4 / (5e-4 + 2e-4), rel=5e-2)

    def test_bounded_by_half(self):
        # Ma Appendix B: E_Z should be clamped to ≤ 0.5 for entropy input
        from qkdx.analytic.pm_qkd import pm_bit_error_rate
        # At high loss + large e_δ, E_Z could exceed 0.5 — must clamp
        e = pm_bit_error_rate(mu=0.01, eta_total=1e-6, p_d=0.3, e_delta=0.4)
        assert 0.0 <= e <= 0.5


class TestPmSinglePhotonYield:
    """Ma Appendix B / §V: Y_1 = single-photon yield at BS.

    Single-photon sent by Alice + vacuum from Bob (or vice versa); probability
    of exactly-one-click at Charlie.
    """

    def test_zero_dark_gives_y1_half_eta(self):
        # Single photon from Alice, vacuum from Bob: BS routes to either D_L or D_R
        # with probability η/2 each (total η detected); single-click = total event.
        y1 = pm_single_photon_yield(eta_total=0.01, p_d=0.0)
        assert y1 == pytest.approx(0.01, rel=1e-9)

    def test_positive_dark(self):
        y1 = pm_single_photon_yield(eta_total=0.01, p_d=1e-6)
        # Should be close to η + small dark-count contribution
        assert y1 == pytest.approx(0.01, abs=5e-6)

    def test_zero_eta_gives_dark_only(self):
        y1 = pm_single_photon_yield(eta_total=0.0, p_d=1e-5)
        # Only dark counts, no signal photon detected
        assert y1 == pytest.approx(2.0 * 1e-5, abs=1e-8)


class TestPmPhaseErrorUpper:
    """Ma Eq. 2: E_μ^X ≤ e_0·q_0 + Σ_k e_{2k+1}·q_{2k+1} + (1 − q_0 − Σ q_{2k+1}).

    The phase error is upper-bounded by the even-photon-number complement,
    reflecting Ma Lemma 1 that only odd-photon components carry phase info.

    **Safety design (Round-4 final, post-dev-reviewer)**:
        Caller-controlled `Y_1_lower` / `Y_1_upper_check` parameters were
        REMOVED from the public API after Rounds 2-3 showed no library-side
        check can prove a caller's Y_1_lower is genuinely a lower bound
        (trivially `Y_1_upper_check = 1.0` let any Y_1_lower slip through).
        Public signature is now only `(mu, Q_mu, Y_0, e_0, e_delta)`, always
        routed through the conservative internal fallback Y_1 = max(0,
        (Q_μ - Y_0)/μ).  Decoy-state-derived tighter bounds belong in a
        separate §7.5+ module (not implemented in this commit).
    """

    def test_zero_mu_reduces_to_e0(self):
        # μ → 0: all weight on k=0 vacuum → E_X ≤ e_0, clamped to [0, 0.5]
        e_x = pm_phase_error_upper(mu=1e-9, Q_mu=1e-9, Y_0=1e-9, e_0=0.5)
        assert e_x == pytest.approx(0.5, rel=1e-3)

    def test_mu_zero_early_return_clamped(self):
        # Round 3 fix for minor clamp bug: mu <= 0 path must clamp e_0 to 0.5
        # even if caller supplied e_0 = 1.0 (would otherwise violate [0, 0.5] UB)
        e_x = pm_phase_error_upper(mu=0.0, Q_mu=1.0, Y_0=0.0, e_0=1.0)
        assert 0.0 <= e_x <= 0.5, (
            f"mu <= 0 early return must clamp to [0, 0.5]; got {e_x} for e_0=1.0"
        )

    def test_upper_bound_in_unit_interval(self):
        e_x = pm_phase_error_upper(mu=0.3, Q_mu=1e-4, Y_0=2e-8, e_0=0.5)
        assert 0.0 <= e_x <= 1.0

    def test_bounded_above_by_half_for_entropy(self):
        # Must be clamped to ≤ 0.5 before feeding into binary entropy
        e_x = pm_phase_error_upper(mu=0.3, Q_mu=1e-5, Y_0=2e-8, e_0=0.5)
        assert 0.0 <= e_x <= 0.5, (
            f"E_X must clamp to ≤ 0.5 before entropy (got {e_x}); "
            "otherwise H(E_X > 0.5) becomes non-monotonic."
        )

    def test_increases_with_zero_prob(self):
        # Higher dark count Y_0 → higher E_μ^X
        e1 = pm_phase_error_upper(mu=0.3, Q_mu=1e-4, Y_0=1e-8, e_0=0.5)
        e2 = pm_phase_error_upper(mu=0.3, Q_mu=1e-4, Y_0=1e-7, e_0=0.5)
        assert e2 > e1

    def test_no_y1_lower_public_param(self):
        """Round 4 safety decision: Y_1_lower / Y_1_upper_check removed from public API.

        Rationale (from Round 3 Codex review):
        No library-side check can prove a caller-supplied Y_1_lower is truly a
        lower bound — passing Y_1_upper_check = 1.0 (trivially true since Y_1 ≤ 1)
        would let any Y_1_lower ∈ [0, 1] through, silently breaking the UB.
        The only safe design is to use the internal conservative fallback for
        all honest-behavior callers; decoy-state-derived tighter bounds move to
        a future separate module (§7.5+).
        """
        import inspect
        sig = inspect.signature(pm_phase_error_upper)
        params = set(sig.parameters.keys())
        assert "Y_1_lower" not in params, (
            f"Y_1_lower must not be a public parameter (got {params}); "
            "it enabled a vacuous safety bypass via Y_1_upper_check=1.0."
        )
        assert "Y_1_upper_check" not in params
        assert "Y_1_honest_check" not in params
        # Acceptable public params
        assert params == {"mu", "Q_mu", "Y_0", "e_0", "e_delta"}

    def test_fallback_is_single_return_path(self):
        """Round 4: internal fallback is the only Y_1 path — result reproducible."""
        # Same inputs must give same E_X every call (no hidden dependency on
        # removed Y_1_lower argument)
        e1 = pm_phase_error_upper(mu=0.3, Q_mu=1e-4, Y_0=1e-8, e_0=0.5, e_delta=0.015)
        e2 = pm_phase_error_upper(mu=0.3, Q_mu=1e-4, Y_0=1e-8, e_0=0.5, e_delta=0.015)
        assert e1 == e2

    def test_input_validation_complete(self):
        """Round 4: all public inputs validated with ValueError."""
        # Invalid mu (negative)
        with pytest.raises(ValueError):
            pm_phase_error_upper(mu=-0.1, Q_mu=1e-4, Y_0=0.0, e_0=0.5, e_delta=0.0)
        # Invalid Q_mu
        with pytest.raises(ValueError):
            pm_phase_error_upper(mu=0.3, Q_mu=1.5, Y_0=0.0, e_0=0.5, e_delta=0.0)
        with pytest.raises(ValueError):
            pm_phase_error_upper(mu=0.3, Q_mu=-0.1, Y_0=0.0, e_0=0.5, e_delta=0.0)
        # Invalid Y_0
        with pytest.raises(ValueError):
            pm_phase_error_upper(mu=0.3, Q_mu=1e-4, Y_0=1.5, e_0=0.5, e_delta=0.0)
        # Invalid e_0
        with pytest.raises(ValueError):
            pm_phase_error_upper(mu=0.3, Q_mu=1e-4, Y_0=0.0, e_0=1.5, e_delta=0.0)
        # Invalid e_delta
        with pytest.raises(ValueError):
            pm_phase_error_upper(mu=0.3, Q_mu=1e-4, Y_0=0.0, e_0=0.5, e_delta=0.6)


class TestPmAsymptoticRate:
    """Ma Eq. 4: R_PM ≥ (2/M) · Q_μ · [1 − H(E_μ^X) − f · H(E_μ^Z)].

    Key acceptance: log-log slope 0.5 vs loss (√η scaling).
    """

    def test_zero_noise_positive_rate(self):
        # Ideal: no dark counts, no misalignment, 0 dB loss → rate > 0
        p = PmQkdParams(p_d=0.0, e_delta=0.0, eta_det=1.0)
        r = pm_asymptotic_rate(mu=0.3, eta_channel=1.0, params=p)
        assert r > 0

    def test_high_loss_gives_abort(self):
        # Very large loss: rate drops below zero eventually
        p = PmQkdParams()
        r = pm_asymptotic_rate(mu=0.3, eta_channel=1e-8, params=p)
        assert r < 0

    def test_sqrt_eta_scaling(self):
        """Core tfqkd_family.md §5.2 验收:log-log R vs η 斜率 ≈ 0.5.

        At medium loss (η ∈ [1e-4, 1e-2]) with small misalignment, PM-QKD
        should show R ∝ √η_arm = η_arm^(1/2) = η_total^(1/2).  Wait — Ma
        §V Fig. 3a uses **total loss Alice-Bob**; η_total means end-to-end
        efficiency (Alice→Bob = product of two arms in direct QKD; but in
        PM-QKD each arm is half-distance).  Convention in this test: η_total
        is *per-arm* (each arm sees √η_ab from the total Alice-Bob loss).
        """
        p = PmQkdParams()
        mu_opt = 0.3  # approximately optimal per Ma §V
        eta_values = [1e-2, 3e-3, 1e-3, 3e-4, 1e-4]
        # η here is total Alice-Bob transmittance; per-arm transmittance is √η.
        # Q_μ ≈ μ · √η so R ∝ √η.
        rates = [
            pm_asymptotic_rate(mu=mu_opt, eta_channel=eta, params=p)
            for eta in eta_values
        ]
        # All positive at these intermediate losses
        for r, eta in zip(rates, eta_values):
            assert r > 0, f"R should be positive at η={eta:.2e}, got {r:.3e}"
        # Log-log linear regression: slope
        log_eta = [math.log10(eta) for eta in eta_values]
        log_r = [math.log10(r) for r in rates]
        n = len(eta_values)
        mean_x = sum(log_eta) / n
        mean_y = sum(log_r) / n
        num = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_eta, log_r))
        den = sum((x - mean_x) ** 2 for x in log_eta)
        slope = num / den
        print(f"PM-QKD log-log slope (vs total η): {slope:.4f} "
              f"(target 0.5 ± 0.05)")
        assert slope == pytest.approx(0.5, abs=0.05), (
            f"Expected √η slope 0.5, got {slope:.4f}"
        )

    def test_misalignment_increases_rate_drop(self):
        # Higher e_d → lower rate at same η
        p_low = PmQkdParams(e_delta=0.005)
        p_hi = PmQkdParams(e_delta=0.03)
        r_low = pm_asymptotic_rate(mu=0.3, eta_channel=1e-3, params=p_low)
        r_hi = pm_asymptotic_rate(mu=0.3, eta_channel=1e-3, params=p_hi)
        assert r_low > r_hi


class TestPmQkdSweep:
    """Convenience sweep over loss values (Ma Fig. 3a style)."""

    def test_produces_monotone_decreasing_rate(self):
        p = PmQkdParams()
        losses_db, rates = pm_qkd_sweep_vs_loss(
            mu=0.3, loss_db_values=[0, 10, 20, 30, 40, 50], params=p,
        )
        assert len(rates) == 6
        # Positive at low loss
        assert rates[0] > 0
        # Monotone decreasing (or collapsing to negative)
        valid = [r for r in rates if r > 0]
        assert all(valid[i] > valid[i + 1] for i in range(len(valid) - 1))

    def test_sweep_matches_ma_fig3a_order_of_magnitude(self):
        # Ma Fig. 3a: at L ≈ 250 km (loss ≈ 50 dB @ 0.2 dB/km),
        # rate ≈ 1e-7 - 1e-8 bit/pulse (eyeball; cutoff at 418 km → loss ≈ 83 dB)
        p = PmQkdParams()
        losses_db, rates = pm_qkd_sweep_vs_loss(
            mu=0.3, loss_db_values=[50], params=p,
        )
        # Should be positive but small at 50 dB
        assert 0 < rates[0] < 1e-5, f"Expected order 1e-7 to 1e-5, got {rates[0]:.3e}"
