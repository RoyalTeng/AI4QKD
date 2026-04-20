"""Tests for Kamin 2025 Choi-state SDP infrastructure (S2.5 Stage 2 A1).

Reference:
    - Kamin et al. 2025, arXiv:2406.10198v3, §4.3 (Eq. 30-31), §5.1 (Eq. 41-42)
    - docs/literature/Kamin-2025.md §5.1 + §6.3
    - Existing WLC SDP: qkdx/numerics/wlc.py (cross-validation target)

Scope (A1):
    - kamin_choi_sdp_qubit_bb84: qubit BB84 Choi-state SDP reproducing
      Kamin Eq. 42 rate function (inf_J W(ρ_J^g) with sifting constraint)
    - Verify Choi parametrization gives same answer as direct WLC SDP over ρ
    - Cross-check at multiple QBER values (0.01, 0.05, 0.10)

Not in scope (A2+):
    - Lagrange dual extraction (A2)
    - Full Theorem 3 key length formula (A3)
    - decoy-state extension (Kamin Eq. 80) — A4 stretch goal
"""
from __future__ import annotations

import math
import os

import numpy as np
import pytest

# Point mosek license if available
_MOSEK_LIC = os.path.expanduser("~/mosek/mosek.lic")
if os.path.exists(_MOSEK_LIC):
    os.environ.setdefault("MOSEKLM_LICENSE_FILE", _MOSEK_LIC)

try:
    import cvxpy as cp
    _MOSEK_AVAILABLE = "MOSEK" in cp.installed_solvers()
except Exception:
    _MOSEK_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not _MOSEK_AVAILABLE,
    reason="MOSEK unavailable; Kamin SDP requires cp.quantum_rel_entr which needs MOSEK",
)


class TestChoiMatrixConstruction:
    """Validate Choi matrix parametrization primitives (Kamin Eq. 31)."""

    def test_choi_from_identity_channel(self):
        # Identity channel J = |Φ⟩⟨Φ|·d_A' where |Φ⟩ = Σ|i⟩_A'|i⟩_B / √d_A'
        from qkdx.numerics.kamin_sdp import choi_of_identity_channel
        J = choi_of_identity_channel(dim=2)
        # J should be PSD and Tr_B(J) = I_{A'}
        assert J.shape == (4, 4)
        # Eigenvalues: one eigenvalue = 2, three = 0 (unnormalized pure state of rank 1)
        eigs = np.linalg.eigvalsh(J)
        assert np.all(eigs >= -1e-12)  # PSD
        # Tr_B(J) = Σ_j ⟨j|_B J |j⟩_B should give I_{A'}
        from qkdx.numerics.kamin_sdp import partial_trace_B
        tr_B_J = partial_trace_B(J, dim_A=2, dim_B=2)
        assert np.allclose(tr_B_J, np.eye(2), atol=1e-12)

    def test_partial_trace_B_on_product(self):
        from qkdx.numerics.kamin_sdp import partial_trace_B
        # J = I_A ⊗ |0⟩⟨0|_B has Tr_B = I_A
        dim_A, dim_B = 2, 2
        M_B = np.array([[1, 0], [0, 0]], dtype=np.complex128)
        J = np.kron(np.eye(dim_A), M_B)
        tr_B = partial_trace_B(J, dim_A=dim_A, dim_B=dim_B)
        assert np.allclose(tr_B, np.eye(dim_A), atol=1e-12)

    def test_partial_trace_A_prime(self):
        from qkdx.numerics.kamin_sdp import partial_trace_A_prime
        # Tr_{A'} of |0⟩⟨0|_{A'} ⊗ M_B = M_B
        dim_A_prime, dim_B = 2, 2
        M_B = np.array([[1, 2], [3, 4]], dtype=np.complex128)
        rho = np.kron(np.array([[1, 0], [0, 0]], dtype=np.complex128), M_B)
        tr_Ap = partial_trace_A_prime(rho, dim_A_prime=dim_A_prime, dim_B=dim_B)
        # Tr_{A'}[|0⟩⟨0| ⊗ M_B] = M_B (when A' is the first subsystem traced)
        assert np.allclose(tr_Ap, M_B, atol=1e-12)


class TestChoiRhoGeneration:
    """Test Kamin Eq. 31: ρ_J^g = Tr_{A'}[(I_A ⊗ J)(|ξ^g⟩⟨ξ^g|^{T_{A'}} ⊗ I_B)]."""

    def test_rho_J_for_identity_channel(self):
        # |ξ⟩ = (|00⟩ + |11⟩)/√2 on A ⊗ A', identity channel J
        # Then ρ_J = |ξ⟩⟨ξ| on A ⊗ B (A' → B identity)
        from qkdx.numerics.kamin_sdp import choi_of_identity_channel, rho_J_from_choi
        xi = np.array([1, 0, 0, 1], dtype=np.complex128) / math.sqrt(2)
        J = choi_of_identity_channel(dim=2)
        rho_J = rho_J_from_choi(J=J, xi=xi, dim_A=2, dim_A_prime=2, dim_B=2)
        expected = np.outer(xi, xi.conj())
        assert np.allclose(rho_J, expected, atol=1e-10), (
            f"rho_J_from_choi(identity) should give |ξ⟩⟨ξ|, "
            f"max diff = {np.abs(rho_J - expected).max():.3e}"
        )

    def test_rho_J_normalization(self):
        # Tr(ρ_J) = 1 for any valid Choi matrix (trace-preserving channel)
        from qkdx.numerics.kamin_sdp import choi_of_identity_channel, rho_J_from_choi
        xi = np.array([1, 0, 0, 1], dtype=np.complex128) / math.sqrt(2)
        J = choi_of_identity_channel(dim=2)
        rho_J = rho_J_from_choi(J=J, xi=xi, dim_A=2, dim_A_prime=2, dim_B=2)
        assert abs(np.trace(rho_J) - 1.0) < 1e-10

    def test_rho_J_hermitian(self):
        from qkdx.numerics.kamin_sdp import choi_of_identity_channel, rho_J_from_choi
        xi = np.array([1, 0, 0, 1], dtype=np.complex128) / math.sqrt(2)
        J = choi_of_identity_channel(dim=2)
        rho_J = rho_J_from_choi(J=J, xi=xi, dim_A=2, dim_A_prime=2, dim_B=2)
        assert np.allclose(rho_J, rho_J.conj().T, atol=1e-12)


class TestKaminChoiSdpQubitBB84:
    """Kamin Choi SDP for qubit BB84 — cross-validate vs direct WLC SDP."""

    def test_kamin_matches_wlc_at_qber_zero(self):
        # At QBER = 0, the optimal single-photon privacy is 1 bit/sift
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84
        result = kamin_choi_sdp_qubit_bb84(qber=0.0, gamma=0.01, solver="MOSEK")
        # h(X|E) ≈ 1 - 2*h(γ/2) at QBER=0, but the *asymptotic Devetak-Winter* rate
        # (ignoring sifting) is 1.  With γ=0.01 test rounds, privacy-per-sift = 1.
        assert result["h_per_sift"] == pytest.approx(1.0, abs=1e-4), (
            f"QBER=0 should give h/sift ≈ 1, got {result['h_per_sift']}"
        )

    def test_kamin_matches_wlc_at_qber_005(self):
        # Cross-validate against existing WLC SDP at QBER=0.05
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84
        from qkdx.numerics.wlc import wlc_key_rate
        from qkdx.protocols.bb84 import build_bb84_protocol

        qber = 0.05
        # WLC direct SDP
        proto = build_bb84_protocol(qber=qber)
        wlc_result = wlc_key_rate(
            proto, {"qber_Z": qber, "qber_X": qber, "p_sift": 0.5},
            solver="MOSEK",
        )
        # Kamin Choi SDP
        kamin_result = kamin_choi_sdp_qubit_bb84(qber=qber, gamma=0.01, solver="MOSEK")

        # Both compute h(X|E) per sift.  Should match within solver tolerance.
        assert kamin_result["h_per_sift"] == pytest.approx(
            wlc_result.h_bits_per_sift, abs=1e-3
        ), (
            f"Kamin h/sift = {kamin_result['h_per_sift']:.6f} vs "
            f"WLC h/sift = {wlc_result.h_bits_per_sift:.6f}"
        )

    def test_kamin_monotone_in_qber(self):
        # Higher QBER → lower h(X|E)
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84
        h_001 = kamin_choi_sdp_qubit_bb84(qber=0.01, gamma=0.01, solver="MOSEK")["h_per_sift"]
        h_005 = kamin_choi_sdp_qubit_bb84(qber=0.05, gamma=0.01, solver="MOSEK")["h_per_sift"]
        h_010 = kamin_choi_sdp_qubit_bb84(qber=0.10, gamma=0.01, solver="MOSEK")["h_per_sift"]
        assert h_001 > h_005 > h_010

    def test_kamin_choi_matrix_valid(self):
        # Solver should return a valid Choi matrix: PSD, Tr-preserving
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84
        from qkdx.numerics.kamin_sdp import partial_trace_B
        result = kamin_choi_sdp_qubit_bb84(qber=0.05, gamma=0.01, solver="MOSEK", return_J=True)
        J = result["J"]
        # PSD
        eigs = np.linalg.eigvalsh(J)
        assert np.all(eigs >= -1e-6), f"J not PSD: min eig = {eigs.min()}"
        # Trace-preserving on A': Tr_B(J) = I_{A'}
        tr_B_J = partial_trace_B(J, dim_A=2, dim_B=2)
        assert np.allclose(tr_B_J, np.eye(2), atol=1e-4), (
            f"Tr_B(J) should be I_2, got: {tr_B_J}"
        )


class TestKaminSdpInvariants:
    """Invariance checks."""

    def test_kamin_independent_of_gamma_at_fixed_qber(self):
        # h(X|E) per sift should be independent of γ (sifting factor is external)
        # Kamin's W = (1-γ)² factor is handled separately; inf_J is over the
        # *per-round privacy* and shouldn't depend on γ structurally.
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84
        h_001 = kamin_choi_sdp_qubit_bb84(qber=0.05, gamma=0.01, solver="MOSEK")["h_per_sift"]
        h_010 = kamin_choi_sdp_qubit_bb84(qber=0.05, gamma=0.10, solver="MOSEK")["h_per_sift"]
        assert h_001 == pytest.approx(h_010, abs=1e-3), (
            f"h/sift should be γ-independent; got {h_001:.4f} vs {h_010:.4f}"
        )

    def test_kamin_invalid_qber_raises(self):
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84
        with pytest.raises(ValueError):
            kamin_choi_sdp_qubit_bb84(qber=-0.01, gamma=0.01, solver="MOSEK")
        with pytest.raises(ValueError):
            kamin_choi_sdp_qubit_bb84(qber=0.6, gamma=0.01, solver="MOSEK")

    def test_kamin_invalid_gamma_raises(self):
        from qkdx.numerics.kamin_sdp import kamin_choi_sdp_qubit_bb84
        with pytest.raises(ValueError):
            kamin_choi_sdp_qubit_bb84(qber=0.05, gamma=0.0, solver="MOSEK")
        with pytest.raises(ValueError):
            kamin_choi_sdp_qubit_bb84(qber=0.05, gamma=1.0, solver="MOSEK")
