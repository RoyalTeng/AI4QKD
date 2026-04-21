"""Tests for numerical E_R^PPT upper bound (Phase 2 U3.7 Layer 5.3 SDP)."""
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
    not _MOSEK_AVAILABLE, reason="MOSEK required for E_R PPT SDP"
)


class TestPartialTranspose:
    def test_partial_transpose_product_state(self):
        """For product state ρ_A ⊗ ρ_B, ρ^{T_B} = ρ_A ⊗ ρ_B^T (same since real)."""
        from qkdx.numerics.upper_bound import partial_transpose_B
        rho_A = np.array([[0.6, 0.2], [0.2, 0.4]], dtype=np.complex128)
        rho_B = np.array([[0.7, 0.1j], [-0.1j, 0.3]], dtype=np.complex128)
        rho = np.kron(rho_A, rho_B)
        rho_TB_expected = np.kron(rho_A, rho_B.T)
        rho_TB = partial_transpose_B(rho, 2, 2)
        assert np.allclose(rho_TB, rho_TB_expected, atol=1e-12)

    def test_partial_transpose_bell_state_detects(self):
        """Bell state ρ has ρ^{T_B} with a negative eigenvalue (PPT criterion)."""
        from qkdx.numerics.upper_bound import partial_transpose_B
        # |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
        phi = np.array([1, 0, 0, 1], dtype=np.complex128) / math.sqrt(2)
        rho = np.outer(phi, phi.conj())
        rho_TB = partial_transpose_B(rho, 2, 2)
        eigs = np.linalg.eigvalsh(rho_TB)
        assert eigs.min() < -0.4, (
            f"Bell state should have ρ^{{T_B}} eigenvalue < -0.4, got {eigs.min()}"
        )


class TestChoiStateConstruction:
    def test_identity_channel_gives_bell_state(self):
        from qkdx.numerics.upper_bound import (
            choi_state_from_kraus, kraus_identity_qubit,
        )
        rho = choi_state_from_kraus(kraus_identity_qubit(), dim_A=2)
        # Should be |Φ⁺⟩⟨Φ⁺|
        phi = np.array([1, 0, 0, 1], dtype=np.complex128) / math.sqrt(2)
        expected = np.outer(phi, phi.conj())
        assert np.allclose(rho, expected, atol=1e-12)

    def test_depolarizing_channel_choi_trace_1(self):
        from qkdx.numerics.upper_bound import (
            choi_state_from_kraus, kraus_depolarizing_qubit,
        )
        for p in [0.0, 0.25, 0.5, 0.75, 1.0]:
            rho = choi_state_from_kraus(
                kraus_depolarizing_qubit(p), dim_A=2,
            )
            assert abs(np.trace(rho) - 1.0) < 1e-10

    def test_full_depolarizing_is_separable(self):
        """At p=1, depol channel sends ρ → I/2, Choi = I/4 (separable)."""
        from qkdx.numerics.upper_bound import (
            choi_state_from_kraus, kraus_depolarizing_qubit,
            partial_transpose_B,
        )
        rho = choi_state_from_kraus(kraus_depolarizing_qubit(1.0), dim_A=2)
        # At p=1, ρ_choi should be I/4 + depolarization
        rho_TB = partial_transpose_B(rho, 2, 2)
        eigs = np.linalg.eigvalsh(rho_TB)
        assert eigs.min() > -1e-8, (
            f"Fully depolarizing Choi should be PPT-positive, got min eig {eigs.min()}"
        )


class TestE_R_PPT_SDP:
    def test_identity_channel_gives_log_d(self):
        """E_R(identity channel) = log(dim_A) for qubit, = 1 bit."""
        from qkdx.numerics.upper_bound import e_r_channel_ppt, kraus_identity_qubit
        r = e_r_channel_ppt(kraus_identity_qubit(), dim_A=2)
        assert r["status"] in ("optimal", "optimal_inaccurate")
        assert r["E_R_channel_bits"] == pytest.approx(1.0, abs=0.01), (
            f"E_R(id qubit) should be 1 bit, got {r['E_R_channel_bits']:.4f}"
        )

    def test_fully_depolarizing_E_R_zero(self):
        """At p=1, Choi state is PPT → E_R^PPT ≈ 0."""
        from qkdx.numerics.upper_bound import e_r_channel_ppt, kraus_depolarizing_qubit
        r = e_r_channel_ppt(kraus_depolarizing_qubit(1.0), dim_A=2)
        assert r["status"] in ("optimal", "optimal_inaccurate")
        assert r["E_R_channel_bits"] < 0.05, (
            f"Fully depolarizing should give E_R ≈ 0, got {r['E_R_channel_bits']:.4f}"
        )

    def test_depolarizing_monotone_in_p(self):
        """E_R decreasing with p (more noise → less distillable)."""
        from qkdx.numerics.upper_bound import e_r_channel_ppt, kraus_depolarizing_qubit
        rates = []
        for p in [0.0, 0.1, 0.3, 0.5]:
            r = e_r_channel_ppt(kraus_depolarizing_qubit(p), dim_A=2)
            rates.append(r["E_R_channel_bits"])
            print(f"p={p}: E_R^PPT = {r['E_R_channel_bits']:.4f}")
        for i in range(len(rates) - 1):
            assert rates[i + 1] <= rates[i] + 1e-4

    def test_amplitude_damping_gives_finite(self):
        """E_R of amplitude-damping channel is finite for γ < 1."""
        from qkdx.numerics.upper_bound import (
            e_r_channel_ppt, kraus_amplitude_damping_qubit,
        )
        for gamma in [0.1, 0.3, 0.5, 0.7]:
            r = e_r_channel_ppt(kraus_amplitude_damping_qubit(gamma), dim_A=2)
            assert r["status"] in ("optimal", "optimal_inaccurate")
            assert math.isfinite(r["E_R_channel_bits"])
            assert 0.0 <= r["E_R_channel_bits"] <= 1.0


class TestRmaxSDP:
    """Wang-Duan 2016b max-Rains SDP (Khatri-Wilde Thm 19.8)."""

    def test_r_max_identity_channel(self):
        """R_max(identity qubit) = 1 bit (maximally entangled limit)."""
        from qkdx.numerics.upper_bound import r_max_channel_sdp, kraus_identity_qubit
        r = r_max_channel_sdp(kraus_identity_qubit(), dim_A=2)
        assert r["status"] in ("optimal", "optimal_inaccurate")
        assert r["R_max_bits"] == pytest.approx(1.0, abs=0.01)

    def test_r_max_fully_depolarizing(self):
        """R_max(fully depol) ≈ 0 (no entanglement preserved)."""
        from qkdx.numerics.upper_bound import r_max_channel_sdp, kraus_depolarizing_qubit
        r = r_max_channel_sdp(kraus_depolarizing_qubit(1.0), dim_A=2)
        assert r["R_max_bits"] < 0.05

    def test_r_max_monotone_in_depol(self):
        """R_max monotone decreasing with depolarizing noise."""
        from qkdx.numerics.upper_bound import r_max_channel_sdp, kraus_depolarizing_qubit
        rates = []
        for p in [0.0, 0.2, 0.5, 0.8]:
            r = r_max_channel_sdp(kraus_depolarizing_qubit(p), dim_A=2)
            rates.append(r["R_max_bits"])
        for i in range(len(rates) - 1):
            assert rates[i + 1] <= rates[i] + 1e-4

    def test_r_max_vs_e_r_ppt_ordering(self):
        """On toy channels, both R_max and E_R^PPT should be 0 ≤ ... ≤ 1."""
        from qkdx.numerics.upper_bound import (
            r_max_channel_sdp, e_r_channel_ppt, kraus_depolarizing_qubit,
        )
        for p in [0.1, 0.3]:
            r_max = r_max_channel_sdp(kraus_depolarizing_qubit(p), dim_A=2)
            e_r = e_r_channel_ppt(kraus_depolarizing_qubit(p), dim_A=2)
            assert 0.0 <= r_max["R_max_bits"] <= 1.0
            assert 0.0 <= e_r["E_R_channel_bits"] <= 1.0


class TestDVGapAnalysis:
    def test_dv_gap_ratio(self):
        from qkdx.numerics.upper_bound import dv_gap_from_achievable
        r = dv_gap_from_achievable(upper_bound_bits=0.5, achievable_rate_bits=0.1)
        assert r["abs_gap_bits"] == pytest.approx(0.4, abs=1e-12)
        assert r["ratio"] == pytest.approx(5.0, abs=1e-10)

    def test_dv_gap_inf_when_achievable_zero(self):
        from qkdx.numerics.upper_bound import dv_gap_from_achievable
        r = dv_gap_from_achievable(upper_bound_bits=0.1, achievable_rate_bits=0.0)
        assert r["ratio"] == float("inf")
