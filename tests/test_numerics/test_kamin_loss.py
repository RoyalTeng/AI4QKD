"""Tests for Kamin full Thm 3 key-length WITH LOSS (S2.5 Stage 2 A4a).

Reference:
    - Kamin et al. 2025 §6.3 Eq. 58 (loss model: η_det · (1-γ)² sifting factor)
    - docs/literature/Kamin-2025.md §6.3 Fig. 1 multi-distance

Scope (A4a):
    - No-loss consistency: kamin_full_key_length_bb84_loss(loss_dB=0)
      must equal kamin_full_key_length_bb84(...) exactly (both fixed and
      optimized variants).
    - Loss scaling: rate at loss_dB > 0 is strictly lower than no-loss.
    - Monotonicity: rate is non-increasing in loss_dB at fixed (n, qber).
    - Asymptotic-limit check: at n → ∞, loss ≠ 0, rate/n → η_det · (DW rate).
    - Input validation.

Not in scope (A4b):
    - Kamin Fig. 1 multi-n × multi-distance reproduction (separate sweep).
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


class TestLossNoLossConsistency:
    """At loss_dB = 0, loss variant MUST equal no-loss variant."""

    def test_fixed_loss0_matches_no_loss(self):
        from qkdx.numerics.kamin_sdp import (
            kamin_full_key_length_bb84,
            kamin_full_key_length_bb84_loss,
        )
        kw = dict(qber=0.01, n=10**10, gamma=0.01, alpha=1.0 + 1e-5,
                  eps_secure=1e-8, f_EC=1.16)
        r_ref = kamin_full_key_length_bb84(**kw)
        r_loss = kamin_full_key_length_bb84_loss(loss_dB=0.0, **kw)
        assert r_loss["eta_det"] == 1.0
        # ell match to full solver precision (same SDP input)
        assert r_loss["ell"] == pytest.approx(r_ref["ell"], rel=1e-8, abs=1e-3)
        assert r_loss["h_per_sift"] == pytest.approx(r_ref["h_per_sift"], abs=1e-6)
        assert r_loss["lambda_EC"] == pytest.approx(r_ref["lambda_EC"], rel=1e-10)

    def test_optimized_loss0_matches_no_loss(self):
        from qkdx.numerics.kamin_sdp import (
            kamin_full_key_length_bb84_optimized,
            kamin_full_key_length_bb84_loss_optimized,
        )
        qber, n = 0.01, 10**12
        r_ref = kamin_full_key_length_bb84_optimized(
            qber=qber, n=n, eps_secure=1e-8, f_EC=1.16,
        )
        r_loss = kamin_full_key_length_bb84_loss_optimized(
            qber=qber, n=n, loss_dB=0.0, eps_secure=1e-8, f_EC=1.16,
        )
        assert r_loss["eta_det"] == 1.0
        # Both grids same structure → ell_star must match
        assert r_loss["ell_star"] == pytest.approx(r_ref["ell_star"], rel=1e-6, abs=1e-2)


class TestLossReducesRate:
    """loss_dB > 0 ⇒ rate strictly lower than no-loss."""

    def test_5dB_loss_reduces_rate(self):
        from qkdx.numerics.kamin_sdp import kamin_full_key_length_bb84_loss_optimized
        qber, n = 0.01, 10**12
        r0 = kamin_full_key_length_bb84_loss_optimized(
            qber=qber, n=n, loss_dB=0.0,
        )
        r5 = kamin_full_key_length_bb84_loss_optimized(
            qber=qber, n=n, loss_dB=5.0,
        )
        assert r5["ell_star"] < r0["ell_star"]
        # η_det(5dB) ≈ 0.316 → rate drops roughly 3×
        assert r5["eta_det"] == pytest.approx(10 ** (-0.5), rel=1e-10)

    def test_rate_monotone_in_loss(self):
        from qkdx.numerics.kamin_sdp import kamin_full_key_length_bb84_loss_optimized
        qber, n = 0.005, 10**12
        rates = []
        for L in [0.0, 3.0, 6.0, 10.0]:
            r = kamin_full_key_length_bb84_loss_optimized(
                qber=qber, n=n, loss_dB=L,
            )
            rates.append(r["ell_star"] / n)
        for i in range(len(rates) - 1):
            assert rates[i + 1] <= rates[i] + 1e-6, (
                f"non-monotone loss curve at step {i}: "
                f"{rates[i]:.4f} → {rates[i+1]:.4f}"
            )


class TestLossAsymptoticScaling:
    """At large n, rate/n → η_det · (1-γ*)² · (h/sift − f_EC·H(q))."""

    def test_asymptotic_eta_scaling(self):
        from qkdx.numerics.kamin_sdp import kamin_full_key_length_bb84_loss_optimized
        qber, n = 0.01, 10**15
        loss_dB = 3.0
        eta_det = 10.0 ** (-loss_dB / 10.0)
        r = kamin_full_key_length_bb84_loss_optimized(
            qber=qber, n=n, loss_dB=loss_dB, eps_secure=1e-10, f_EC=1.16,
        )
        rate = r["ell_star"] / n

        H_q = -qber * math.log2(qber) - (1 - qber) * math.log2(1 - qber)
        h_per_sift_DW = 1.0 - H_q
        leak_per_sift = 1.16 * H_q
        gamma_star = r["gamma_star"]
        expected = (1 - gamma_star) ** 2 * eta_det * (h_per_sift_DW - leak_per_sift)
        # ~5% absolute tolerance (finite-size correction ~ 1/√n at n=10^15)
        assert rate == pytest.approx(expected, abs=5e-2), (
            f"Asymptotic rate {rate:.4f} vs η·DW {expected:.4f} at "
            f"γ*={gamma_star}, eta_det={eta_det:.4f}"
        )


class TestLossFig1MidRange:
    """Kamin Fig. 1 @ 10 dB, qber=0.005, n=10^12 — should be positive
    and well below no-loss (~0.9)."""

    def test_10dB_n12_positive_and_below_no_loss(self):
        from qkdx.numerics.kamin_sdp import kamin_full_key_length_bb84_loss_optimized
        r = kamin_full_key_length_bb84_loss_optimized(
            qber=0.005, n=10**12, loss_dB=10.0, eps_secure=1e-8, f_EC=1.16,
        )
        rate = r["ell_star"] / 10**12
        assert rate > 0, f"10dB n=10^12 rate should be positive, got {rate}"
        # η_det = 0.1, so rate upper-bounded by ~0.1 · asymptotic ≈ 0.09
        assert rate < 0.15, (
            f"Fig.1 10dB n=10^12 rate {rate:.4f} implausibly large "
            f"(η_det=0.1 ⇒ ≲ 0.09 expected)"
        )


class TestInputValidation:
    def test_negative_loss_raises(self):
        from qkdx.numerics.kamin_sdp import (
            kamin_full_key_length_bb84_loss,
            kamin_full_key_length_bb84_loss_optimized,
        )
        with pytest.raises(ValueError, match="loss_dB"):
            kamin_full_key_length_bb84_loss(
                qber=0.01, n=10**10, loss_dB=-1.0, gamma=0.01, alpha=1.001,
            )
        with pytest.raises(ValueError, match="loss_dB"):
            kamin_full_key_length_bb84_loss_optimized(
                qber=0.01, n=10**10, loss_dB=-1.0,
            )
