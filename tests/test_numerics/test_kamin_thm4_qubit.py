"""Tests for Kamin Thm 4 τ-slack SDP applied to qubit BB84 (D.1).

Goal: close the §4.1 residual n=10^12 ±6 dB cutoff gap by using Thm 4
optimal-g trade-off instead of hard-constraint dual g.

Reference:
    - Kamin et al. 2025 §5.2.1 (Thm 4 Eq. 46-55)
    - docs/PHASE_A_STAGE2_KAMIN_SUMMARY_2026-04-20_to_21.md §3.2, §5.1
"""
from __future__ import annotations

import math
import os

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
    not _MOSEK_AVAILABLE, reason="MOSEK required for Kamin Thm 4 SDP"
)


class TestThm4PhiCoefficients:
    """Kamin Eq. 45 φ_0, φ_1, φ_2 sanity checks."""

    def test_phi_0_scales_inv_gamma(self):
        from qkdx.numerics.kamin_sdp import _thm4_phi_coefficients_qubit
        p0_a, _, _ = _thm4_phi_coefficients_qubit(alpha=1.01, gamma=0.01)
        p0_b, _, _ = _thm4_phi_coefficients_qubit(alpha=1.01, gamma=0.001)
        # φ_0 = (β_factor)/γ, so γ=0.001 gives 10× larger φ_0
        assert p0_b == pytest.approx(10.0 * p0_a, rel=1e-10)

    def test_phi_1_scales_inv_sqrt_gamma(self):
        from qkdx.numerics.kamin_sdp import _thm4_phi_coefficients_qubit
        _, p1_a, _ = _thm4_phi_coefficients_qubit(alpha=1.01, gamma=0.01)
        _, p1_b, _ = _thm4_phi_coefficients_qubit(alpha=1.01, gamma=0.04)
        # φ_1 ∝ 1/√γ, so γ=0.04 gives p1/2× of p1 at γ=0.01
        assert p1_b == pytest.approx(p1_a / 2.0, rel=1e-10)

    def test_phi_2_no_gamma_dep(self):
        from qkdx.numerics.kamin_sdp import _thm4_phi_coefficients_qubit
        _, _, p2_a = _thm4_phi_coefficients_qubit(alpha=1.01, gamma=0.01)
        _, _, p2_b = _thm4_phi_coefficients_qubit(alpha=1.01, gamma=0.1)
        assert p2_a == pytest.approx(p2_b, rel=1e-10)


class TestThm4SDPShape:
    """Thm 4 τ-slack SDP runs + returns expected structure."""

    def test_thm4_runs_no_loss_trivial_qber(self):
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84
        r = kamin_choi_sdp_qubit_bb84(
            qber=0.005, gamma=0.01, use_thm4=True, alpha_thm4=1.001,
        )
        assert r["status"] in ("optimal", "optimal_inaccurate")
        assert r["use_thm4"] is True
        assert "tau" in r
        assert len(r["tau"]) == 2  # τ_Z, τ_X
        assert math.isfinite(r["h_per_sift"])

    def test_thm4_r_best_below_or_equal_w_hard(self):
        """Kamin Eq. 47: r_best = inf_{J,τ}[W + s(Στ/2)] ≤ W_hard.

        Slack τ > 0 allows J matching qber_hon+τ (not strictly honest) → lower
        W.  r_best combines lower W + positive s penalty; the inf trades off.
        Always r_best ≤ W at honest point (hard).
        """
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84
        r_hard = kamin_choi_sdp_qubit_bb84(
            qber=0.005, gamma=0.01, use_thm4=False,
        )
        r_thm4 = kamin_choi_sdp_qubit_bb84(
            qber=0.005, gamma=0.01, use_thm4=True, alpha_thm4=1.001,
        )
        # r_best CAN be lower than W_hard (by Eq. 47 sup-form)
        assert r_thm4["h_per_sift"] <= r_hard["h_per_sift"] + 1e-6


class TestThm4KeyLengthQubit:
    """Thm 4 qubit BB84 finite-key — documents that 2-cell τ-slack is NOT
    sufficient to close §4.1 n=10^12 ±6 dB residual.

    Finding: for qubit BB84 with only (qber_Z, qber_X) observations, Thm 4
    τ-slack gives essentially same rates as hard constraint.  The residual
    cutoff gap requires expanding to Kamin's full 5-cell observation alphabet
    (Z-correct, Z-error, X-correct, X-error, no-det), which is a larger
    refactor (documented as future work).
    """

    def test_thm4_n12_0dB_positive_near_asymptotic(self):
        from qkdx.numerics.kamin_sdp import kamin_thm4_key_length_bb84_optimized
        r = kamin_thm4_key_length_bb84_optimized(
            qber=0.005, n=10**12, loss_dB=0.0,
        )
        print(f"Thm 4 n=10^12 0 dB: rate={r['rate_star']:.4f}, "
              f"γ*={r['gamma_star']}, α*={r['alpha_star']:.10f}")
        # Kamin §6.3 "n=10^12 0 dB ≈ 0.9". Allow 0.85-0.95 (Thm 4 might be
        # slightly lower than hard due to s penalty).
        assert 0.85 < r["rate_star"] < 0.95, (
            f"Thm 4 rate at n=10^12 0 dB should be ~0.9, got {r['rate_star']:.4f}"
        )

    @pytest.mark.parametrize("loss_dB", [0.0, 10.0, 20.0])
    def test_thm4_n12_positive_at_multiple_losses(self, loss_dB):
        """Thm 4 gives positive rate through 20+ dB at n=10^12.

        Kamin GEAT cutoff at n=10^12 is 26 dB; my Thm 4 qubit cutoff is still
        ~30 dB (not improved over hard-constraint) because the 2-cell
        observation doesn't exploit Thm 4's full-alphabet flexibility.
        """
        from qkdx.numerics.kamin_sdp import kamin_thm4_key_length_bb84_optimized
        r = kamin_thm4_key_length_bb84_optimized(
            qber=0.005, n=10**12, loss_dB=loss_dB,
        )
        print(f"Thm 4 n=10^12 {loss_dB} dB: rate={r['rate_star']:.5f}")
        assert r["rate_star"] > 0, (
            f"Thm 4 rate at n=10^12 {loss_dB} dB should be positive, "
            f"got {r['rate_star']:.5f}"
        )
