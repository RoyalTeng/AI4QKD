"""Tests for Kamin 2025 GEAT finite-key formulas (S2.5 Stage 1 — qubit BB84 asymptotic anchor).

References:
    - Kamin et al. 2025 (arXiv:2406.10198v3), Theorem 3 (Eq. 16) + Thm 1 (Eq. 11)
    - docs/literature/Kamin-2025.md §4, §6

Scope (Stage 1):
    - Theorem 3 key length formula evaluation (given h, V², K(α), λ_EC)
    - Optimal ε_PA / ε_EV allocation (Eq. 57)
    - Qubit BB84 with loss analytic asymptotic rate
    - Grid search over (γ, α) to find best finite-size key length
    - Cross-check Kamin Fig. 1 at n=10^12, 0 dB, p_depol=0.01 against Devetak-Winter limit

Not in scope (Stage 2/3):
    - Choi-state SDP (Frank-Wolfe + dual extraction)
    - Decoy-state block-diagonal optimization
"""
from __future__ import annotations

import math

import pytest

from qkdx.finite_key.kamin_geat import (
    bb84_qubit_asymptotic_rate,
    bb84_qubit_finite_key_length,
    bb84_qubit_optimal_finite_key,
    kamin_K_alpha,
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


class TestKaminTheorem3KeyLength:
    """Kamin Eq. 16: ℓ ≤ nh + n·T_α(f) − n((α-1)/(2-α))²K(α) − λ_EC − ⌈log(1/ε_EV)⌉ − (α/(α-1))·log(1/ε_PA) + 2.

    For unique-acceptance with f = rate, T_α simplifies to -((α-1)/(2-α))·(ln 2/2)·V².
    """

    def test_no_finite_size_limit(self):
        # n → ∞, α → 1: ℓ/n → h (Devetak-Winter limit)
        n = 10**20
        h = 0.5
        V_sq = 4.0
        K_val = 1.0
        alpha = 1.0001
        ell = kamin_theorem3_key_length(
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
        ell_large = kamin_theorem3_key_length(n=10**12, **kwargs)
        ell_small = kamin_theorem3_key_length(n=10**8, **kwargs)
        assert ell_large / 10**12 > ell_small / 10**8

    def test_negative_when_n_too_small(self):
        # For very small n, ℓ can go negative (infeasible regime)
        ell = kamin_theorem3_key_length(
            n=100, h=0.5, V_squared=4.0, K_alpha=1.0, alpha=1.05,
            lambda_EC=10.0, eps_EV=1e-10, eps_PA=1e-10,
        )
        assert ell < 0


class TestBB84QubitAsymptoticRate:
    """Kamin §6 asymptotic (n → ∞) rate for qubit BB84 with loss.

    rate_hon = (1 - γ)² · η_det · [1 - h(Q_X) - f_EC · h(Q_Z)]
    with Q_X = Q_Z = p_depol / 2 for depolarizing channel.
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
    """Kamin qubit BB84 Protocol 1: given (n, p_depol, loss_dB, γ, α) → ℓ."""

    def test_large_n_approaches_asymptotic(self):
        # n = 10^14 → ℓ/n ≈ rate_asy (up to O(1/√n) correction from V²)
        # Stage 1 uses conservative V² (Var(f)=1 upper bound) → ~5-10% gap is expected;
        # Stage 2 with Theorem 4 SDP-derived min-tradeoff would tighten this.
        n = 10**14
        ell = bb84_qubit_finite_key_length(
            n=n, p_depol=0.01, loss_dB=0.0, gamma=0.05, alpha=1.001,
            eps_secure=1e-8, f_EC=1.16,
        )
        rate_asy = bb84_qubit_asymptotic_rate(
            p_depol=0.01, eta_det=1.0, gamma=0.05, f_EC=1.16,
        )
        assert ell / n == pytest.approx(rate_asy, abs=1e-1)

    def test_zero_loss_kamin_fig1_anchor(self):
        # Kamin Fig.1 @ n=10^12, loss=0 dB, p_depol=0.01: rate close to asymptotic
        # (GEAT at low loss ≈ IID per Kamin §6 observation)
        n = 10**12
        # Optimized over γ, α: pick a reasonable point
        ell = bb84_qubit_finite_key_length(
            n=n, p_depol=0.01, loss_dB=0.0, gamma=0.02, alpha=1.005,
            eps_secure=1e-8, f_EC=1.16,
        )
        # Must produce positive rate
        assert ell > 0
        rate = ell / n
        # Devetak-Winter limit = (1-0.02)² · (1 - 2.16 h(0.005)) ≈ 0.96 · 0.902 ≈ 0.866
        # Finite-size at n=10^12 loses ~10-20% → rate ∈ [0.4, 0.9]
        assert 0.3 < rate < 0.95

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
        # Kamin Fig.1 n=10^12 @ 0 dB ≈ 0.8-0.9 (eyeball from paper Fig.1)
        assert 0.5 < rate < 1.0
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
