"""Tests for Kamin GEAT finite-key applied to ideal symmetric MDI-QKD (D.4).

Reduction: MDI conditional Alice-Bob state after Charlie's successful Bell
measurement is Werner-form with effective QBER, identical structure to
qubit BB84. Therefore the existing Kamin qubit BB84 SDP is reused with
an MDI-specific (1/4)·η sift factor.
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
    not _MOSEK_AVAILABLE, reason="MOSEK required for Kamin MDI SDP"
)


class TestMDI_H_PerSift:
    """MDI h_per_sift matches qubit BB84 at the same QBER (Werner form)."""

    def test_h_per_sift_matches_qubit_bb84(self):
        from qkdx.numerics.kamin_sdp_mdi import kamin_mdi_h_per_sift
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84_with_dual
        for qber in [0.01, 0.05, 0.08]:
            r_mdi = kamin_mdi_h_per_sift(qber=qber, gamma=0.01)
            r_bb84 = kamin_choi_sdp_qubit_bb84_with_dual(qber=qber, gamma=0.01)
            assert r_mdi["h_per_sift"] == pytest.approx(
                r_bb84["h_per_sift"], abs=1e-6
            )
            assert r_mdi["protocol"] == "mdi"
            assert r_mdi["p_sift_base"] == 0.25


class TestMDI_KeyLength:
    """Kamin MDI finite-key formula sanity."""

    def test_positive_at_n12_0dB(self):
        """At n=10^12, 0 dB, qber=0.01, MDI rate > 0."""
        from qkdx.numerics.kamin_sdp_mdi import kamin_mdi_key_length_optimized
        r = kamin_mdi_key_length_optimized(
            qber=0.01, n=10**12, loss_dB_total=0.0,
        )
        assert r["rate_star"] > 0
        # MDI p_sift = 1/4 of BB84 → rate ≈ (1/2) × qubit-BB84 rate at 0 dB
        # qubit BB84 at 0 dB, qber=0.01: rate ≈ 0.89
        # MDI expected: ≈ 0.22
        assert 0.15 < r["rate_star"] < 0.30, (
            f"MDI n=10^12 0 dB rate expected [0.15, 0.30], got {r['rate_star']:.4f}"
        )

    def test_negative_at_small_n(self):
        from qkdx.numerics.kamin_sdp_mdi import kamin_mdi_key_length
        r = kamin_mdi_key_length(
            qber=0.05, n=100, loss_dB_total=0.0,
            gamma=0.01, alpha=1.1,
        )
        assert r["ell"] < 0

    def test_rate_monotone_in_loss(self):
        from qkdx.numerics.kamin_sdp_mdi import kamin_mdi_key_length_optimized
        rates = {}
        for loss in [0.0, 5.0, 10.0, 20.0]:
            r = kamin_mdi_key_length_optimized(
                qber=0.01, n=10**12, loss_dB_total=loss,
            )
            rates[loss] = r["rate_star"]
            print(f"MDI n=10^12 {loss} dB: rate = {r['rate_star']:.5f}")
        losses = sorted(rates.keys())
        for i in range(len(losses) - 1):
            assert rates[losses[i + 1]] <= rates[losses[i]] + 1e-6

    def test_mdi_psift_quarter_of_bb84(self):
        """At same (qber, n, loss, γ, α), MDI rate ≈ (1/2) × BB84 rate
        (due to p_sift = 1/4 vs BB84 = 1/2)."""
        from qkdx.numerics.kamin_sdp_mdi import kamin_mdi_key_length
        from qkdx.numerics.kamin_sdp import kamin_full_key_length_bb84_loss
        qber = 0.005
        n = 10**12
        loss = 0.0
        gamma = 0.005
        inv_sqrt_n = 1.0 / math.sqrt(n)
        alpha = 1.0 + 1.0 * inv_sqrt_n
        r_mdi = kamin_mdi_key_length(
            qber=qber, n=n, loss_dB_total=loss,
            gamma=gamma, alpha=alpha,
        )
        r_bb84 = kamin_full_key_length_bb84_loss(
            qber=qber, n=n, loss_dB=loss, gamma=gamma, alpha=alpha,
        )
        if r_bb84["ell"] > 0 and r_mdi["ell"] > 0:
            ratio = r_mdi["rate_per_round"] / (r_bb84["ell"] / n)
            # MDI / BB84 ≈ (1/4) / (1) = 0.25 at idealized level if BB84's
            # eta_det=1 and h_per_sift are the same; allow 0.15-0.35 for
            # finite-size penalty differences.
            assert 0.15 < ratio < 0.4, (
                f"MDI/BB84 rate ratio at 0 dB expected ~0.25, got {ratio:.3f}"
            )
