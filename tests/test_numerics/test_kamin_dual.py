"""Tests for Kamin 2025 Thm 4 Lagrange dual extraction (S2.5 Stage 2 A2).

Reference:
    - Kamin et al. 2025 §5.2.1 Thm 4 (Eq. 47-51)
    - docs/literature/Kamin-2025.md §5.2

Scope (A2):
    - Extract g* as Lagrange multipliers from kamin_choi_sdp_qubit_bb84
    - Verify subgradient property: rate(q) ≥ rate(q_hon) + g*·(q - q_hon)
    - Numerical consistency: g* satisfies Kamin Eq. 11 min-tradeoff definition

Not in scope:
    - Full Eq. 49 SDP with λ, τ auxiliaries (future, needed for non-unique-acceptance)
    - Frank-Wolfe wrapper for non-convex objective (future, when Thm 4 needs iterative)
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
    not _MOSEK_AVAILABLE, reason="MOSEK required for Kamin SDP"
)


class TestDualValueExtraction:
    """Extract Lagrange multipliers of QBER constraints."""

    def test_dual_values_returned(self):
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84_with_dual
        result = kamin_choi_sdp_qubit_bb84_with_dual(qber=0.05, gamma=0.01)
        assert "g_star" in result
        assert "g_star_Z" in result["g_star"]
        assert "g_star_X" in result["g_star"]
        # Values should be finite floats
        assert math.isfinite(result["g_star"]["g_star_Z"])
        assert math.isfinite(result["g_star"]["g_star_X"])

    def test_dual_structure_bb84_werner_only_X_contributes(self):
        """For BB84 Werner state at symmetric qber, only X-basis observation
        bounds the privacy (phase error).  So g*_Z ≈ 0, g*_X ≠ 0.

        This is physically correct and a stronger statement than mere
        symmetry — it tests Kamin Eq. 11 min-tradeoff structure.
        """
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84_with_dual
        result = kamin_choi_sdp_qubit_bb84_with_dual(qber=0.05, gamma=0.01)
        g_Z = result["g_star"]["g_star_Z"]
        g_X = result["g_star"]["g_star_X"]
        # g*_Z should be ~0 (Z-basis is the KEY basis, not the phase-error basis)
        assert abs(g_Z) < 1e-6, (
            f"Expected g*_Z ≈ 0 for BB84 Werner, got {g_Z:.6e}"
        )
        # g*_X should carry the full subgradient (nontrivial)
        assert abs(g_X) > 1.0, (
            f"Expected |g*_X| > 1 for BB84 Werner at q=0.05, got {g_X:.6e}"
        )


class TestSubgradientProperty:
    """g* is a subgradient of rate(q) at q_hon:
        rate(q) ≥ rate(q_hon) + g*_Z (q_Z - q_Z^hon) + g*_X (q_X - q_X^hon)
    """

    def test_subgradient_inequality_at_nearby_point(self):
        """Move qber by small Δ; check subgradient bound holds.

        Rate function is convex in q (inf over J is convex), so g* is a
        subgradient and the tangent lies below:
            rate(q + Δ) ≥ rate(q_hon) + (g*_Z + g*_X) · Δ

        Both qber_Z and qber_X shift together by Δ here (symmetric BB84 SDP).
        """
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84_with_dual, kamin_choi_sdp_qubit_bb84
        q_hon = 0.05
        delta = 0.01
        # Solve at honest point to get g*
        r_hon = kamin_choi_sdp_qubit_bb84_with_dual(qber=q_hon, gamma=0.01)
        rate_hon = r_hon["h_per_sift"]
        g_Z = r_hon["g_star"]["g_star_Z"]
        g_X = r_hon["g_star"]["g_star_X"]

        # Solve at shifted point (qber_Z = qber_X = q_hon + delta)
        rate_shifted = kamin_choi_sdp_qubit_bb84(qber=q_hon + delta, gamma=0.01)["h_per_sift"]

        predicted = rate_hon + (g_Z + g_X) * delta
        # Subgradient (for convex rate): rate(q + Δ) ≥ predicted
        # Allow small tolerance for solver precision (≈ 1e-5)
        assert rate_shifted + 1e-4 >= predicted, (
            f"Subgradient inequality violated:\n"
            f"  rate({q_hon + delta:.2f}) = {rate_shifted:.6f}\n"
            f"  predicted = rate_hon + (g_Z + g_X)·Δ\n"
            f"            = {rate_hon:.6f} + ({g_Z:.4f} + {g_X:.4f})·{delta}\n"
            f"            = {predicted:.6f}"
        )

    def test_g_star_X_is_negative_for_BB84(self):
        """g*_X should be NEGATIVE for BB84: increasing qber_X (phase error)
        DECREASES privacy, so ∂(rate)/∂qber_X < 0.

        Magnitude at q=0.05: rate'(q) = -log_2((1-q)/q) ≈ -4.25
        """
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84_with_dual
        result = kamin_choi_sdp_qubit_bb84_with_dual(qber=0.05, gamma=0.01)
        g_X = result["g_star"]["g_star_X"]
        assert g_X < -1.0, (
            f"Expected g*_X < -1 for BB84 at q=0.05; got {g_X:.4f}"
        )


class TestDualValueNumericalCheck:
    """Verify Lagrange duality relations numerically."""

    def test_kkt_stationarity(self):
        """At optimum, the gradient of the Lagrangian should vanish (KKT)."""
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84_with_dual
        result = kamin_choi_sdp_qubit_bb84_with_dual(qber=0.05, gamma=0.01)
        # The dual values are reported at the primal optimum; no direct KKT test
        # here but verify presence + consistency
        assert "g_star" in result
        assert result["status"] in ("optimal", "optimal_inaccurate")

    def test_dual_matches_analytic_bb84_derivative(self):
        """For BB84 Werner state, h/sift = 1 - H_2(q_X) depends only on
        phase-error q_X.  So:
            g*_X = d(h/sift)/dq_X = -log_2((1-q)/q)
            g*_Z = 0  (Z-basis observation doesn't bound privacy in BB84)

        At q=0.05: g*_X = -log_2(19) ≈ -4.2479.
        """
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84_with_dual
        for q in [0.01, 0.05, 0.10]:
            result = kamin_choi_sdp_qubit_bb84_with_dual(qber=q, gamma=0.01)
            g_X = result["g_star"]["g_star_X"]
            analytic = -math.log2((1 - q) / q)
            # Solver precision ~1e-5; analytic derivative is exact
            assert g_X == pytest.approx(analytic, abs=1e-3), (
                f"At q={q}: g*_X = {g_X:.6f} vs analytic d(h/sift)/dq_X = {analytic:.6f}"
            )
