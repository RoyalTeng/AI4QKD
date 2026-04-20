"""Tests for Kamin full Thm 3 key-length formula (S2.5 Stage 2 A3).

Reference:
    - Kamin et al. 2025 Eq. 16 (key length), Eq. 44 (V² via max/min of g),
      Eq. 57 (optimal ε split)
    - docs/literature/Kamin-2025.md §4, §5.2

Scope (A3):
    - Wire SDP-derived g* (A2) into full Eq. 16 finite-key formula
    - Optimal ε_PA / ε_EV split (Eq. 57)
    - Cross-check vs existing heuristic pre-SDP anchor (kamin_geat.py)
    - Asymptotic n → ∞ recovers Devetak-Winter rate
    - Finite-n for qubit BB84 no-loss matches Kamin Fig. 1 eyeball
"""
from __future__ import annotations

import math
import os

import numpy as np
import pytest

_MOSEK_LIC = os.path.expanduser("~/mosek/mosek.lic")
if os.path.exists(_MOSEK_LIC):
    os.environ.setdefault("MOSEKLM_LICENSE_FILE", _MOSEK_LIC)

try:
    import cvxpy as cp
    _MOSEK_AVAILABLE = "MOSEK" in cp.installed_solvers()
except Exception:
    _MOSEK_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not _MOSEK_AVAILABLE, reason="MOSEK required for Kamin full SDP"
)


class TestKaminFullKeyLengthQubitBB84:
    """Full Eq. 16 evaluation: h + V² + K(α) + ε-split + λ_EC."""

    def test_positive_at_large_n_low_qber(self):
        # Kamin's key length at fixed (γ, α) may be NEGATIVE for suboptimal
        # (γ, α); the optimizer finds the best combination.
        from qkdx.numerics.kamin_sdp import (
            kamin_full_key_length_bb84,
            kamin_full_key_length_bb84_optimized,
        )
        result = kamin_full_key_length_bb84_optimized(
            qber=0.01, n=10**12, eps_secure=1e-8, f_EC=1.16,
        )
        assert result["ell_star"] > 0
        rate_per_pulse = result["ell_star"] / 10**12
        assert 0.5 < rate_per_pulse < 1.0, (
            f"Expected 0.5 < rate < 1 at n=10^12 qber=0.01, got {rate_per_pulse:.4f} "
            f"(γ*={result['gamma_star']}, α*={result['alpha_star']})"
        )

    def test_negative_at_small_n(self):
        from qkdx.numerics.kamin_sdp import (
            kamin_full_key_length_bb84,
            kamin_full_key_length_bb84_optimized,
        )
        # At n=100 with moderate QBER, finite-key corrections dominate → ℓ < 0
        result = kamin_full_key_length_bb84(
            qber=0.05, n=100, gamma=0.01, alpha=1.1,
            eps_secure=1e-8, f_EC=1.16,
        )
        assert result["ell"] < 0

    def test_asymptotic_matches_devetak_winter(self):
        """At n → ∞ optimized: ℓ/n → DW rate (privacy - leak_EC)."""
        from qkdx.numerics.kamin_sdp import kamin_full_key_length_bb84_optimized
        qber = 0.01
        n = 10**15
        result = kamin_full_key_length_bb84_optimized(
            qber=qber, n=n, eps_secure=1e-10, f_EC=1.16,
        )
        rate = result["ell_star"] / n

        # DW rate: at optimal γ_star, (1-γ_star)² · (h/sift − f_EC · H(qber))
        h_per_sift = 1.0 - (
            -qber * math.log2(qber) - (1 - qber) * math.log2(1 - qber)
        )
        leak_ec_per_sift = 1.16 * (
            -qber * math.log2(qber) - (1 - qber) * math.log2(1 - qber)
        )
        gamma_star = result["gamma_star"]
        expected_per_round = (1 - gamma_star) ** 2 * (h_per_sift - leak_ec_per_sift)

        # Finite-size penalty negligible at n=10^15, so rate should equal DW
        # within ~5% (conservative — could be tighter)
        assert rate == pytest.approx(expected_per_round, abs=5e-2), (
            f"Asymptotic rate {rate:.4f} vs DW {expected_per_round:.4f} "
            f"at γ*={gamma_star}"
        )

    def test_monotone_in_n(self):
        """Optimized ℓ/n monotone non-decreasing in n."""
        from qkdx.numerics.kamin_sdp import kamin_full_key_length_bb84_optimized
        rates = []
        for n_exp in [8, 10, 12, 14]:
            r = kamin_full_key_length_bb84_optimized(
                qber=0.03, n=10**n_exp, eps_secure=1e-8, f_EC=1.16,
            )
            rates.append(r["ell_star"] / 10**n_exp)
        # Each step should be ≥ previous (monotone non-decreasing)
        for i in range(len(rates) - 1):
            assert rates[i + 1] >= rates[i] - 1e-4, (
                f"non-monotone at step {i}: {rates[i]:.4f} → {rates[i+1]:.4f}"
            )


class TestKaminFullKeyVsHeuristic:
    """SDP-based Kamin should give rate >= heuristic pre-SDP (heuristic uses
    worst-case V²=1 + missing min-tradeoff)."""

    def test_sdp_gives_same_or_better_rate_than_heuristic(self):
        from qkdx.numerics.kamin_sdp import kamin_full_key_length_bb84_optimized
        from qkdx.finite_key.kamin_geat import bb84_qubit_optimal_finite_key
        qber = 0.01
        n = 10**12

        sdp_result = kamin_full_key_length_bb84_optimized(
            qber=qber, n=n, eps_secure=1e-8, f_EC=1.16,
        )
        ell_sdp = sdp_result["ell_star"]
        ell_heur, _, _ = bb84_qubit_optimal_finite_key(
            n=n, p_depol=2 * qber, loss_dB=0.0,
            eps_secure=1e-8, f_EC=1.16,
        )
        # SDP-derived V² (tight, via g*) should not be worse than heuristic (var_f=1 loose)
        # Allow tiny numerical slack
        assert ell_sdp >= ell_heur - 1e-3 * n, (
            f"SDP ℓ = {ell_sdp:.3e} should be ≥ heuristic ℓ = {ell_heur:.3e}"
        )


class TestKaminFullKeyFig1Anchor:
    """Qubit BB84 Fig. 1 at p_depol=0.01 → qber=0.005.  Kamin Fig. 1 at 0 dB,
    n=10^12 should give rate close to asymptotic ≈ 0.91 (see §6.3)."""

    def test_fig1_zero_loss_n10_12(self):
        from qkdx.numerics.kamin_sdp import kamin_full_key_length_bb84_optimized
        # Kamin Fig. 1: p_depol=0.01 → qber = p_depol/2 = 0.005
        result = kamin_full_key_length_bb84_optimized(
            qber=0.005, n=10**12, eps_secure=1e-8, f_EC=1.16,
        )
        rate = result["ell_star"] / 10**12
        # Kamin Fig. 1 eyeball at 0 dB, n=10^12: ≈ 0.8-0.9
        assert 0.7 < rate < 1.0, (
            f"Fig.1 n=10^12 0 dB rate {rate:.4f} outside [0.7, 1.0] "
            f"(γ*={result['gamma_star']}, α*={result['alpha_star']:.2e})"
        )
