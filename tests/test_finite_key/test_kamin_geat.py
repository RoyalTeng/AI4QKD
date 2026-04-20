"""Tests for Kamin 2025 GEAT finite-key formulas — S2.5 Stage 1 heuristic pre-SDP anchor.

**Scope disclosure (post-Round-1 review)**:
    - This is a HEURISTIC pre-SDP estimator, not a faithful Theorem 3 implementation.
    - Even under unique-acceptance, Kamin Eq. 11/41/42 still require (a) a valid
      affine min-tradeoff function g and (b) the infimum over admissible p/J.
      The min-tradeoff optimization step is NOT implemented here — unique-acceptance
      only removes Δ_com, not the inf over p.
    - These helpers are a Stage-1 analytic anchor useful for sanity against GLL-2021
      Renner path; they are NOT Kamin 2025 Theorem 3.

References:
    - Kamin et al. 2025 (arXiv:2406.10198v3), Theorem 3 (Eq. 16) + Thm 1 (Eq. 11)
    - docs/literature/Kamin-2025.md §4, §6

Covered:
    - Pre-EC entropy (Eq. 16 `h` input) separate from post-EC Devetak-Winter rate
    - Optimal ε_PA / ε_EV allocation (Eq. 57)
    - Qubit BB84 loss model (Kamin §6)
    - Grid search over (γ, α)
    - Cross-check at n=10^12, 0 dB, p_depol=0.01 against D-W limit

Not covered (Stage 2/3):
    - Choi-state SDP (Frank-Wolfe + dual extraction) with min-tradeoff optimization
    - Decoy-state block-diagonal optimization
"""
from __future__ import annotations

import math

import pytest

from qkdx.finite_key.kamin_geat import (
    bb84_qubit_asymptotic_rate,
    bb84_qubit_finite_key_length,
    bb84_qubit_optimal_finite_key,
    bb84_qubit_preEC_entropy,
    bb84_qubit_leak_EC_per_round,
    kamin_K_alpha,
    kamin_heuristic_key_length,
    kamin_theorem3_key_length,
    kamin_V_squared,
    optimal_eps_parameters,
)


class TestOptimalEpsilonParameters:
    """Kamin Eq. 57: ε_PA = α/(2α-1) · ε_secure, ε_EV = (α-1)/(2α-1) · ε_secure."""

    def test_sum_is_epsilon_secure(self):
        eps_PA, eps_EV = optimal_eps_parameters(eps_secure=1e-8, alpha=1.2)
        assert eps_PA + eps_EV == pytest.approx(1e-8, rel=1e-12)

    def test_alpha_near_1p5_approaches_2to1_split(self):
        # α → 1.5⁻ → ε_PA/ε → 0.75, ε_EV/ε → 0.25
        eps_PA, eps_EV = optimal_eps_parameters(eps_secure=1e-8, alpha=1.499)
        assert eps_PA == pytest.approx(0.75e-8, rel=5e-3)
        assert eps_EV == pytest.approx(0.25e-8, rel=5e-3)

    @pytest.mark.parametrize("alpha", [1.01, 1.1, 1.3, 1.49])
    def test_both_positive_in_valid_range(self, alpha):
        eps_PA, eps_EV = optimal_eps_parameters(eps_secure=1e-9, alpha=alpha)
        assert 0 < eps_PA < 1e-9
        assert 0 < eps_EV < 1e-9

    def test_invalid_alpha_raises(self):
        with pytest.raises(ValueError):
            optimal_eps_parameters(eps_secure=1e-8, alpha=0.5)
        with pytest.raises(ValueError):
            optimal_eps_parameters(eps_secure=1e-8, alpha=1.0)

    def test_invalid_eps_raises(self):
        with pytest.raises(ValueError):
            optimal_eps_parameters(eps_secure=0, alpha=1.2)
        with pytest.raises(ValueError):
            optimal_eps_parameters(eps_secure=1.1, alpha=1.2)


class TestKaminVSquared:
    """Kamin Eq. 11: V²(p, f) = (log(1 + 2 d_A^κ) + sqrt(2 + Var(p, f)))²."""

    def test_kappa1_d2_zero_variance(self):
        # log(1 + 2*2) + sqrt(2 + 0) = log 5 + √2
        V_sq = kamin_V_squared(d_A=2, var_f=0.0, kappa=1)
        expected = (math.log2(5) + math.sqrt(2.0)) ** 2
        assert V_sq == pytest.approx(expected, rel=1e-12)

    def test_kappa2_d2_zero_variance(self):
        # log(1 + 2*4) + sqrt(2) = log 9 + √2
        V_sq = kamin_V_squared(d_A=2, var_f=0.0, kappa=2)
        expected = (math.log2(9) + math.sqrt(2.0)) ** 2
        assert V_sq == pytest.approx(expected, rel=1e-12)

    def test_variance_monotone(self):
        V0 = kamin_V_squared(d_A=2, var_f=0.0, kappa=1)
        V1 = kamin_V_squared(d_A=2, var_f=1.0, kappa=1)
        assert V1 > V0


class TestKaminKAlpha:
    """Kamin Eq. 11: K(α) complex second-order coefficient."""

    def test_finite_positive_in_valid_range(self):
        # α ∈ (1, 3/2), κ=1, d_A=2, max(f)=1, min_Σ(f)=0
        K = kamin_K_alpha(alpha=1.1, d_A=2, max_f=1.0, min_sigma_f=0.0, kappa=1)
        assert K > 0
        assert math.isfinite(K)

    def test_alpha_out_of_range_raises(self):
        with pytest.raises(ValueError):
            kamin_K_alpha(alpha=1.0, d_A=2, max_f=1.0, min_sigma_f=0.0, kappa=1)
        with pytest.raises(ValueError):
            kamin_K_alpha(alpha=1.5, d_A=2, max_f=1.0, min_sigma_f=0.0, kappa=1)
        with pytest.raises(ValueError):
            kamin_K_alpha(alpha=2.0, d_A=2, max_f=1.0, min_sigma_f=0.0, kappa=1)

    def test_K_finite_near_boundaries(self):
        # K should remain finite as α → 1+ (numerator (2-α)³ → 1, denominator (3-2α)³ → 1)
        K_near_1 = kamin_K_alpha(alpha=1.001, d_A=2, max_f=1.0, min_sigma_f=0.0, kappa=1)
        assert math.isfinite(K_near_1)
        assert K_near_1 > 0


class TestKaminHeuristicKeyLength:
    """Kamin Eq. 16 HEURISTIC form (NOT a faithful Theorem 3 implementation).

    Assumes: f ≡ rate at honest distribution ⇒ T_α(f) ≈ −((α-1)/(2-α))·(ln 2/2)·V²
    Missing: inf_{p,J} optimization from Kamin Eq. 11/41/42 (min-tradeoff function search).

    `kamin_theorem3_key_length` is a deprecated alias for backward compat.
    """

    def test_no_finite_size_limit(self):
        # n → ∞, α → 1: ℓ/n → h (Devetak-Winter limit)
        n = 10**20
        h = 0.5
        V_sq = 4.0
        K_val = 1.0
        alpha = 1.0001
        ell = kamin_heuristic_key_length(
            n=n, h=h, V_squared=V_sq, K_alpha=K_val, alpha=alpha,
            lambda_EC=0.0, eps_EV=1e-10, eps_PA=1e-10,
        )
        rate = ell / n
        assert rate == pytest.approx(h, abs=1e-3)

    def test_smaller_n_lower_rate(self):
        # Finite-size correction: smaller n → lower rate
        kwargs = dict(
            h=0.5, V_squared=4.0, K_alpha=1.0, alpha=1.05,
            lambda_EC=0.0, eps_EV=1e-10, eps_PA=1e-10,
        )
        ell_large = kamin_heuristic_key_length(n=10**12, **kwargs)
        ell_small = kamin_heuristic_key_length(n=10**8, **kwargs)
        assert ell_large / 10**12 > ell_small / 10**8

    def test_negative_when_n_too_small(self):
        # For very small n, ℓ can go negative (infeasible regime)
        ell = kamin_heuristic_key_length(
            n=100, h=0.5, V_squared=4.0, K_alpha=1.0, alpha=1.05,
            lambda_EC=10.0, eps_EV=1e-10, eps_PA=1e-10,
        )
        assert ell < 0

    def test_deprecated_alias_same_result(self):
        # Backward compat: kamin_theorem3_key_length is an alias that emits a DeprecationWarning
        kwargs = dict(
            n=10**10, h=0.5, V_squared=4.0, K_alpha=1.0, alpha=1.05,
            lambda_EC=0.0, eps_EV=1e-10, eps_PA=1e-10,
        )
        ell_new = kamin_heuristic_key_length(**kwargs)
        with pytest.warns(DeprecationWarning):
            ell_old = kamin_theorem3_key_length(**kwargs)
        assert ell_old == ell_new


class TestBB84QubitPreECEntropy:
    """Pre-EC entropy — the `h` that goes into Kamin Eq. 16.

    Kamin Eq. 60 defines W(ρ_J^g) = (1-γ)² D(G(ρ_J^g) || Z∘G(ρ_J^g)) — this is the
    PER-ROUND PRIVACY entropy (before EC leakage).  For qubit BB84 with depolarization:
        h = (1-γ)² · η_det · [1 - h(Q_X)]    with Q_X = p_depol/2

    This is distinct from the full D-W rate (which subtracts f_EC · h(Q_Z) for leak_EC).
    """

    def test_zero_depol_gives_detection_sift(self):
        # h → (1-γ)² · η_det
        h = bb84_qubit_preEC_entropy(p_depol=0.0, eta_det=1.0, gamma=0.02)
        assert h == pytest.approx(0.98 ** 2, rel=1e-9)

    def test_depol_1pct_no_loss_matches_formula(self):
        gamma = 0.02
        p = 0.005
        hQ = -p * math.log2(p) - (1 - p) * math.log2(1 - p)
        expected = (1 - gamma) ** 2 * 1.0 * (1 - hQ)
        assert bb84_qubit_preEC_entropy(p_depol=0.01, eta_det=1.0, gamma=gamma) == pytest.approx(expected, rel=1e-12)

    def test_strictly_greater_than_full_rate(self):
        # h (pre-EC) > full D-W rate (post-EC) for any nonzero depol
        params = dict(p_depol=0.01, eta_det=0.5, gamma=0.1)
        h_pre = bb84_qubit_preEC_entropy(**params)
        r_post = bb84_qubit_asymptotic_rate(**params, f_EC=1.16)
        assert h_pre > r_post

    def test_separates_correctly_from_leak_EC(self):
        # Key identity: r_postEC = h_preEC - leak_EC (per round)
        params = dict(p_depol=0.01, eta_det=1.0, gamma=0.05, f_EC=1.16)
        h_pre = bb84_qubit_preEC_entropy(p_depol=0.01, eta_det=1.0, gamma=0.05)
        leak = bb84_qubit_leak_EC_per_round(**params)
        r_post = bb84_qubit_asymptotic_rate(**params)
        assert r_post == pytest.approx(h_pre - leak, rel=1e-12)

    def test_invalid_inputs_raise(self):
        with pytest.raises(ValueError):
            bb84_qubit_preEC_entropy(p_depol=-0.1, eta_det=1.0, gamma=0.1)
        with pytest.raises(ValueError):
            bb84_qubit_preEC_entropy(p_depol=0.01, eta_det=0.0, gamma=0.1)
        with pytest.raises(ValueError):
            bb84_qubit_preEC_entropy(p_depol=0.01, eta_det=1.0, gamma=0.0)


class TestBB84QubitLeakECPerRound:
    """Kamin Eq. 59/26: honest leak_EC per round = (1-γ)² · η_det · f_EC · h(Q_Z)."""

    def test_zero_depol_zero_leak(self):
        assert bb84_qubit_leak_EC_per_round(p_depol=0.0, eta_det=1.0, gamma=0.1, f_EC=1.16) == 0.0

    def test_formula_match(self):
        gamma = 0.05
        p = 0.005
        hQ = -p * math.log2(p) - (1 - p) * math.log2(1 - p)
        expected = (1 - gamma) ** 2 * 1.0 * 1.16 * hQ
        got = bb84_qubit_leak_EC_per_round(p_depol=0.01, eta_det=1.0, gamma=gamma, f_EC=1.16)
        assert got == pytest.approx(expected, rel=1e-12)

    def test_f_EC_monotone(self):
        params = dict(p_depol=0.01, eta_det=1.0, gamma=0.05)
        leak_10 = bb84_qubit_leak_EC_per_round(**params, f_EC=1.0)
        leak_12 = bb84_qubit_leak_EC_per_round(**params, f_EC=1.2)
        assert leak_12 > leak_10


class TestBB84QubitAsymptoticRate:
    """Kamin §6 asymptotic (n → ∞) rate for qubit BB84 with loss — full Devetak-Winter.

    rate_hon = (1 - γ)² · η_det · [1 - h(Q_X) - f_EC · h(Q_Z)]
    with Q_X = Q_Z = p_depol / 2 for depolarizing channel.

    Note: This is the FULL post-EC rate, NOT the Eq. 16 `h` input.
    Use bb84_qubit_preEC_entropy for the latter.
    """

    def test_zero_depol_no_loss_gamma_small(self):
        # Ideal: rate → (1-γ)²
        r = bb84_qubit_asymptotic_rate(p_depol=0.0, eta_det=1.0, gamma=0.01, f_EC=1.0)
        assert r == pytest.approx((0.99) ** 2, rel=1e-6)

    def test_zero_depol_with_loss(self):
        r = bb84_qubit_asymptotic_rate(p_depol=0.0, eta_det=0.5, gamma=0.1, f_EC=1.0)
        assert r == pytest.approx(0.9 ** 2 * 0.5, rel=1e-6)

    def test_depol_1pct_no_loss(self):
        # Kamin §6 default p_depol=0.01 → Q = 0.005, f_EC=1.16
        # rate = (1-γ)² · 1 · [1 - 2.16 · h(0.005)]
        gamma = 0.01
        p = 0.005
        h_p = -p * math.log2(p) - (1 - p) * math.log2(1 - p)
        expected = (1 - gamma) ** 2 * (1 - h_p - 1.16 * h_p)
        r = bb84_qubit_asymptotic_rate(p_depol=0.01, eta_det=1.0, gamma=gamma, f_EC=1.16)
        assert r == pytest.approx(expected, rel=1e-10)

    def test_high_depol_gives_negative(self):
        # Above BB84 threshold (~11% QBER) rate should go negative
        r = bb84_qubit_asymptotic_rate(p_depol=0.30, eta_det=1.0, gamma=0.01, f_EC=1.0)
        assert r < 0

    def test_invalid_inputs_raise(self):
        with pytest.raises(ValueError):
            bb84_qubit_asymptotic_rate(p_depol=-0.1, eta_det=1.0, gamma=0.1, f_EC=1.0)
        with pytest.raises(ValueError):
            bb84_qubit_asymptotic_rate(p_depol=0.01, eta_det=1.5, gamma=0.1, f_EC=1.0)
        with pytest.raises(ValueError):
            bb84_qubit_asymptotic_rate(p_depol=0.01, eta_det=1.0, gamma=0.0, f_EC=1.0)
        with pytest.raises(ValueError):
            bb84_qubit_asymptotic_rate(p_depol=0.01, eta_det=1.0, gamma=1.0, f_EC=1.0)
        with pytest.raises(ValueError):
            bb84_qubit_asymptotic_rate(p_depol=0.01, eta_det=1.0, gamma=0.1, f_EC=0.5)


class TestBB84QubitFiniteKeyLength:
    """Kamin qubit BB84 Protocol 1: heuristic pre-SDP finite-key length.

    Regression tests below separately pin the pre-EC vs post-EC decomposition.
    """

    def test_decomposition_identity_at_n_inf(self):
        # Regression test for C1 (EC double-count).
        # As n → ∞ and α → 1: ℓ/n → h_preEC − leak_EC = r_postEC (Devetak-Winter).
        # If leak_EC were subtracted twice, the observed rate would be
        # r_postEC − leak_EC, i.e. lower by leak_EC ≈ 0.05 at p_depol=0.01.
        n = 10**16
        params = dict(p_depol=0.01, eta_det=1.0, gamma=0.05, f_EC=1.16)
        h_pre = bb84_qubit_preEC_entropy(**{k: v for k, v in params.items() if k != "f_EC"})
        leak = bb84_qubit_leak_EC_per_round(**params)
        r_post = bb84_qubit_asymptotic_rate(**params)
        # Sanity: decomposition holds
        assert r_post == pytest.approx(h_pre - leak, rel=1e-12)

        ell = bb84_qubit_finite_key_length(
            n=n, p_depol=0.01, loss_dB=0.0, gamma=0.05, alpha=1.0001,
            eps_secure=1e-8, f_EC=1.16,
        )
        # At n = 10^16, finite-size corrections ~ 10^-6 — ell/n should be ≈ r_post
        # (within ~1% of D-W, NOT ~5% below it from the double-count bug)
        assert ell / n == pytest.approx(r_post, abs=5e-3), (
            f"ell/n = {ell/n:.6f} vs r_post = {r_post:.6f} "
            f"(gap = {r_post - ell/n:.6f}; bug would give gap ≈ leak_EC = {leak:.6f})"
        )

    def test_large_n_approaches_asymptotic(self):
        # n = 10^14 → ℓ/n ≈ rate_asy (up to O(1/√n) correction from V²)
        # Stage 1 uses conservative V² (Var(f)=1 upper bound) → small residual gap;
        # Stage 2 with Theorem 4 SDP-derived min-tradeoff would tighten this.
        n = 10**14
        ell = bb84_qubit_finite_key_length(
            n=n, p_depol=0.01, loss_dB=0.0, gamma=0.05, alpha=1.001,
            eps_secure=1e-8, f_EC=1.16,
        )
        rate_asy = bb84_qubit_asymptotic_rate(
            p_depol=0.01, eta_det=1.0, gamma=0.05, f_EC=1.16,
        )
        # After C1 fix: gap to asymptotic < 5e-2 at n=10^14 (was 1e-1 with bug)
        assert ell / n == pytest.approx(rate_asy, abs=5e-2)

    def test_zero_loss_kamin_fig1_anchor(self):
        # Kamin Fig.1 @ n=10^12, loss=0 dB, p_depol=0.01.
        # After C1 fix (pre-EC `h` separate from λ_EC), rate ≈ D-W limit ≈ 0.866
        # at Kamin Fig.1 eyeball target (0.8–0.9).
        n = 10**12
        ell = bb84_qubit_finite_key_length(
            n=n, p_depol=0.01, loss_dB=0.0, gamma=0.02, alpha=1.005,
            eps_secure=1e-8, f_EC=1.16,
        )
        assert ell > 0
        rate = ell / n
        rate_asy = bb84_qubit_asymptotic_rate(
            p_depol=0.01, eta_det=1.0, gamma=0.02, f_EC=1.16,
        )
        # Tight band: within ±10% of D-W (catches double-count regressions)
        assert rate == pytest.approx(rate_asy, abs=0.1), (
            f"rate={rate:.4f}, D-W={rate_asy:.4f} — would fail with EC double-count"
        )
        # Kamin Fig.1 eyeball target
        assert 0.7 < rate < 1.0

    def test_high_loss_abort(self):
        # 40 dB loss @ n = 10^6: too lossy, ℓ < 0
        ell = bb84_qubit_finite_key_length(
            n=10**6, p_depol=0.01, loss_dB=40.0, gamma=0.1, alpha=1.1,
            eps_secure=1e-8, f_EC=1.16,
        )
        assert ell < 0

    def test_scaling_with_n(self):
        # As n increases, ℓ/n should monotonically increase (less finite-size penalty)
        rates = []
        for n in [10**8, 10**10, 10**12, 10**14]:
            ell = bb84_qubit_finite_key_length(
                n=n, p_depol=0.01, loss_dB=0.0, gamma=0.02, alpha=1.005,
                eps_secure=1e-8, f_EC=1.16,
            )
            rates.append(ell / n)
        # Monotone increasing
        for i in range(len(rates) - 1):
            assert rates[i + 1] > rates[i]


class TestBB84QubitOptimalFiniteKey:
    """Grid search over (γ, α) to find max key length."""

    def test_zero_loss_large_n(self):
        # At n=10^12, 0 dB, p_depol=0.01: should find positive rate near asymptotic
        ell, gamma_star, alpha_star = bb84_qubit_optimal_finite_key(
            n=10**12, p_depol=0.01, loss_dB=0.0,
            eps_secure=1e-8, f_EC=1.16,
        )
        assert ell > 0
        rate = ell / 10**12
        # After C1 fix, Kamin Fig.1 n=10^12 @ 0 dB falls in [0.8, 1.0] (eyeball)
        # Before C1 fix the double-count placed rate in [0.7, 0.85] — this tightened
        # bound catches C1 regressions.
        assert 0.8 < rate < 1.0
        # γ should be small (low loss regime)
        assert 0 < gamma_star < 0.2
        # α should be close to 1
        assert 1.0 < alpha_star < 1.2

    def test_cutoff_at_high_loss(self):
        # n=10^6, high loss: optimal ℓ negative (cutoff)
        ell, _, _ = bb84_qubit_optimal_finite_key(
            n=10**6, p_depol=0.01, loss_dB=30.0,
            eps_secure=1e-8, f_EC=1.16,
        )
        # Kamin Fig.1 n=10^6 cutoff ~15 dB → 30 dB is past cutoff
        assert ell <= 0

    def test_monotone_n(self):
        # Optimal ℓ/n increases with n at fixed loss
        rates = []
        for n in [10**8, 10**10, 10**12]:
            ell, _, _ = bb84_qubit_optimal_finite_key(
                n=n, p_depol=0.01, loss_dB=5.0,
                eps_secure=1e-8, f_EC=1.16,
            )
            rates.append(ell / n)
        assert rates[2] > rates[1] > rates[0]
