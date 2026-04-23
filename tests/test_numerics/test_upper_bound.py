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

_MOSEK_SKIP = pytest.mark.skipif(
    not _MOSEK_AVAILABLE, reason="MOSEK required for E_R PPT SDP"
)


@_MOSEK_SKIP
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


@_MOSEK_SKIP
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


@_MOSEK_SKIP
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


@_MOSEK_SKIP
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


class TestLogNegAmplitudeDampingAnalytic:
    """Analytic formula: log_neg(E_AD(η)) = log₂(1+η) for all η.

    Proof: ||ρ_Choi^{T_B}||₁ = 1+η (eigenvalue calculation).
    No MOSEK required — pure numpy trace norm.
    Crossover with Pirandola: η² + η - 1 = 0 → η_c = 1/φ.
    Memo: docs/findings/beta_G3_golden_ratio_crossover_2026-04-23.md §2.
    """

    @staticmethod
    def _trace_norm_partial_transpose(eta: float) -> float:
        """||ρ_AD(η)^{T_B}||₁ via eigenvalues of partial transpose."""
        from qkdx.numerics.upper_bound import choi_state_from_kraus
        K0 = np.array([[1, 0], [0, eta**0.5]])
        K1 = np.array([[0, (1 - eta)**0.5], [0, 0]])
        rho = choi_state_from_kraus([K0, K1], dim_A=2)
        d = 2
        n = d * d
        rho_TB = np.zeros((n, n), dtype=complex)
        for i in range(d):
            for j in range(d):
                for k in range(d):
                    for ll in range(d):
                        rho_TB[i * d + ll, k * d + j] = rho[i * d + j, k * d + ll]
        return float(np.sum(np.abs(np.linalg.eigvalsh(rho_TB))))

    def test_trace_norm_equals_1_plus_eta(self):
        """||ρ^{T_B}||₁ = 1 + η for each test point (machine precision)."""
        for eta in [0.1, 0.3, 0.5, 0.7, 0.9]:
            tn = self._trace_norm_partial_transpose(eta)
            print(f"  eta={eta:.1f}: ||ρ^T_B||₁={tn:.10f}, 1+η={1+eta:.10f}")
            assert tn == pytest.approx(1 + eta, abs=1e-10), (
                f"eta={eta}: expected trace norm={1+eta}, got {tn}"
            )

    def test_log_neg_equals_log2_1_plus_eta(self):
        """log_neg(E_AD(η)) = log₂(1+η) for each test point."""
        for eta in [0.1, 0.5, 0.9, 0.95]:
            tn = self._trace_norm_partial_transpose(eta)
            log_neg = math.log2(tn)
            expected = math.log2(1 + eta)
            print(f"  eta={eta}: log_neg={log_neg:.8f}, log₂(1+η)={expected:.8f}")
            assert log_neg == pytest.approx(expected, abs=1e-9)

    def test_golden_ratio_crossover_exact(self):
        """At η_c = 1/φ: ||ρ^{T_B}||₁ = φ exactly (crossover with Pirandola)."""
        phi = (1 + 5**0.5) / 2
        eta_c = 1 / phi  # golden ratio property: 1/φ satisfies η²+η-1=0
        tn = self._trace_norm_partial_transpose(eta_c)
        print(f"  η_c=1/φ={eta_c:.10f}: ||ρ^T_B||₁={tn:.10f}, φ={phi:.10f}")
        assert tn == pytest.approx(phi, abs=1e-9), (
            f"Trace norm at η_c=1/φ should equal φ, got {tn}"
        )

    def test_crossover_satisfies_quadratic(self):
        """η_c = 1/φ satisfies η²+η-1=0 (algebraic root of crossover equation)."""
        phi = (1 + 5**0.5) / 2
        eta_c = 1 / phi
        assert eta_c**2 + eta_c - 1 == pytest.approx(0.0, abs=1e-14)

    def test_2x_log_neg_equals_pirandola_at_crossover(self):
        """2·log_neg(E₁) = Pirandola exactly at η = 1/φ."""
        phi = (1 + 5**0.5) / 2
        eta_c = 1 / phi
        tn = self._trace_norm_partial_transpose(eta_c)
        two_log_neg = 2 * math.log2(tn)
        pirandola = -math.log2(1 - eta_c)
        print(f"  2·log_neg={two_log_neg:.8f}, Pirandola={pirandola:.8f}")
        assert two_log_neg == pytest.approx(pirandola, abs=1e-8)

    def test_choi_matrix_entries(self):
        """Verify Choi state entries match ρ_AD(η) = (1/2)[[1,0,0,√η],[0,0,0,0],[0,0,1-η,0],[√η,0,0,η]].

        Basis: |00⟩,|01⟩,|10⟩,|11⟩. Tests §2 Step 1 of the derivation.
        """
        from qkdx.numerics.upper_bound import choi_state_from_kraus
        for eta in [0.3, 0.618, 0.9]:
            K0 = np.array([[1, 0], [0, eta**0.5]])
            K1 = np.array([[0, (1 - eta)**0.5], [0, 0]])
            rho = choi_state_from_kraus([K0, K1], dim_A=2)
            print(f"  eta={eta}: rho diag={np.diag(rho).real}")
            # Diagonal: [1/2, 0, (1-η)/2, η/2]
            assert rho[0, 0].real == pytest.approx(0.5, abs=1e-12)
            assert rho[1, 1].real == pytest.approx(0.0, abs=1e-12)
            assert rho[2, 2].real == pytest.approx((1 - eta) / 2, abs=1e-12)
            assert rho[3, 3].real == pytest.approx(eta / 2, abs=1e-12)
            # Off-diagonal: rho[0,3] = rho[3,0] = √η/2
            assert rho[0, 3].real == pytest.approx(eta**0.5 / 2, abs=1e-12)
            assert rho[3, 0].real == pytest.approx(eta**0.5 / 2, abs=1e-12)
            # All other entries zero
            for i, j in [(0,1),(0,2),(1,2),(1,3),(2,3)]:
                assert abs(rho[i, j]) < 1e-12, f"rho[{i},{j}] should be 0"

    def test_partial_transpose_block_structure(self):
        """ρ^{T_B} is block-diagonal with blocks {|00⟩,|11⟩} and {|01⟩,|10⟩}.

        Block A (0,3): diag(1/2, η/2). Block B (1,2): [[0,√η/2],[√η/2,(1-η)/2]].
        Tests §2 Step 2 of the derivation.
        """
        from qkdx.numerics.upper_bound import choi_state_from_kraus
        for eta in [0.3, 0.618, 0.9]:
            K0 = np.array([[1, 0], [0, eta**0.5]])
            K1 = np.array([[0, (1 - eta)**0.5], [0, 0]])
            rho = choi_state_from_kraus([K0, K1], dim_A=2)
            d = 2
            rho_TB = np.zeros((4, 4), dtype=complex)
            for i in range(d):
                for j in range(d):
                    for k in range(d):
                        for ll in range(d):
                            rho_TB[i*d+ll, k*d+j] = rho[i*d+j, k*d+ll]
            print(f"  eta={eta}: rho_TB[1,2]={rho_TB[1,2].real:.6f} (expect {eta**0.5/2:.6f})")
            # Block A: (0,0)=1/2, (3,3)=η/2, (0,3)=(3,0)=0
            assert rho_TB[0, 0].real == pytest.approx(0.5, abs=1e-12)
            assert rho_TB[3, 3].real == pytest.approx(eta / 2, abs=1e-12)
            assert abs(rho_TB[0, 3]) < 1e-12
            # Block B: (1,1)=0, (2,2)=(1-η)/2, (1,2)=(2,1)=√η/2
            assert rho_TB[1, 1].real == pytest.approx(0.0, abs=1e-12)
            assert rho_TB[2, 2].real == pytest.approx((1 - eta) / 2, abs=1e-12)
            assert rho_TB[1, 2].real == pytest.approx(eta**0.5 / 2, abs=1e-12)
            # Cross-block entries zero
            for i, j in [(0,1),(0,2),(1,3),(2,3)]:
                assert abs(rho_TB[i, j]) < 1e-12

    def test_eigenvalue_set(self):
        """ρ^{T_B} has eigenvalues {1/2, η/2, 1/2, -η/2} (sorted).

        Tests §2 Step 3: Block B quadratic → λ₋ = -η/2.
        """
        from qkdx.numerics.upper_bound import choi_state_from_kraus
        for eta in [0.3, 0.618, 0.9]:
            K0 = np.array([[1, 0], [0, eta**0.5]])
            K1 = np.array([[0, (1 - eta)**0.5], [0, 0]])
            rho = choi_state_from_kraus([K0, K1], dim_A=2)
            d = 2
            rho_TB = np.zeros((4, 4), dtype=complex)
            for i in range(d):
                for j in range(d):
                    for k in range(d):
                        for ll in range(d):
                            rho_TB[i*d+ll, k*d+j] = rho[i*d+j, k*d+ll]
            eigs = sorted(np.linalg.eigvalsh(rho_TB))
            expected = sorted([-eta/2, eta/2, 0.5, 0.5])
            print(f"  eta={eta}: eigs={[f'{e:.6f}' for e in eigs]}, expected={[f'{e:.6f}' for e in expected]}")
            for got, exp in zip(eigs, expected):
                assert got == pytest.approx(exp, abs=1e-10), (
                    f"eta={eta}: eigenvalue {got} != expected {exp}"
                )


class TestAnalyticLogNegFormulas:
    """Analytic log-neg for three qubit channel families (SymPy-verified 2026-04-23).

    Each formula verified against numerical PT+eigenvalue computation.
    Reference: docs/workflow/beta-G3-analytic-proof-review/sympy-c1c-verification.md
    """

    @staticmethod
    def _numerical_log_neg(kraus_ops, dim_A=2):
        """Compute log_neg numerically via Choi + PT + |eigenvalues|."""
        from qkdx.numerics.upper_bound import choi_state_from_kraus
        rho = choi_state_from_kraus(kraus_ops, dim_A=dim_A)
        d = dim_A
        n = d * d
        rho_TB = np.zeros((n, n), dtype=complex)
        for i in range(d):
            for j in range(d):
                for k in range(d):
                    for ll in range(d):
                        rho_TB[i * d + ll, k * d + j] = rho[i * d + j, k * d + ll]
        trace_norm = float(np.sum(np.abs(np.linalg.eigvalsh(rho_TB))))
        return math.log2(trace_norm) if trace_norm > 1.0 else 0.0

    def test_amplitude_damping_analytic_matches_numerical(self):
        """analytic_log_neg_amplitude_damping(γ) == log₂(2-γ) vs numerical."""
        from qkdx.numerics.upper_bound import (
            analytic_log_neg_amplitude_damping, kraus_amplitude_damping_qubit,
        )
        for gamma in [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
            analytic = analytic_log_neg_amplitude_damping(gamma)
            numerical = self._numerical_log_neg(kraus_amplitude_damping_qubit(gamma))
            expected = math.log2(2.0 - gamma)
            print(f"  γ={gamma}: analytic={analytic:.8f}, numerical={numerical:.8f}, log₂(2-γ)={expected:.8f}")
            assert analytic == pytest.approx(expected, abs=1e-12)
            assert analytic == pytest.approx(numerical, abs=1e-9)

    def test_dephasing_analytic_matches_numerical(self):
        """analytic_log_neg_dephasing(p) == log₂(1+|1-2p|) vs numerical."""
        from qkdx.numerics.upper_bound import (
            analytic_log_neg_dephasing, kraus_dephasing_qubit,
        )
        for p in [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]:
            analytic = analytic_log_neg_dephasing(p)
            numerical = self._numerical_log_neg(kraus_dephasing_qubit(p))
            expected = math.log2(1.0 + abs(1.0 - 2.0 * p))
            print(f"  p={p}: analytic={analytic:.8f}, numerical={numerical:.8f}, expected={expected:.8f}")
            assert analytic == pytest.approx(expected, abs=1e-12)
            assert analytic == pytest.approx(numerical, abs=1e-9)

    def test_depolarizing_analytic_matches_numerical(self):
        """analytic_log_neg_depolarizing(p): 1+log₂(1-3p/4) for p<2/3, else 0."""
        from qkdx.numerics.upper_bound import (
            analytic_log_neg_depolarizing, kraus_depolarizing_qubit,
        )
        # Include p < 2/3 (entangled), p = 2/3 (threshold), p > 2/3 (PPT/sep)
        for p in [0.0, 0.1, 0.3, 0.5, 2.0/3.0, 0.7, 0.9, 1.0]:
            analytic = analytic_log_neg_depolarizing(p)
            numerical = self._numerical_log_neg(kraus_depolarizing_qubit(p))
            F = 1.0 - 3.0 * p / 4.0
            expected = math.log2(2.0 * F) if F > 0.5 else 0.0
            print(f"  p={p:.5f}: F={F:.4f}, analytic={analytic:.8f}, numerical={numerical:.8f}")
            assert analytic == pytest.approx(expected, abs=1e-12)
            assert analytic == pytest.approx(numerical, abs=1e-9)

    def test_boundary_values(self):
        """Identity-channel boundary: all three channels give log_neg=1 at noise=0."""
        from qkdx.numerics.upper_bound import (
            analytic_log_neg_amplitude_damping,
            analytic_log_neg_dephasing,
            analytic_log_neg_depolarizing,
        )
        assert analytic_log_neg_amplitude_damping(0.0) == pytest.approx(1.0, abs=1e-15)
        assert analytic_log_neg_dephasing(0.0) == pytest.approx(1.0, abs=1e-15)
        assert analytic_log_neg_depolarizing(0.0) == pytest.approx(1.0, abs=1e-15)

    def test_full_noise_boundary(self):
        """Full-noise boundary: AD(γ=1)=0, dephase(p=1/2)=0, depol(p≥2/3)=0."""
        from qkdx.numerics.upper_bound import (
            analytic_log_neg_amplitude_damping,
            analytic_log_neg_dephasing,
            analytic_log_neg_depolarizing,
        )
        assert analytic_log_neg_amplitude_damping(1.0) == pytest.approx(0.0, abs=1e-15)
        assert analytic_log_neg_dephasing(0.5) == pytest.approx(0.0, abs=1e-15)
        assert analytic_log_neg_depolarizing(2.0/3.0) == pytest.approx(0.0, abs=1e-12)
        assert analytic_log_neg_depolarizing(0.8) == 0.0  # fully in PPT regime
        assert analytic_log_neg_depolarizing(1.0) == 0.0

    def test_dephasing_symmetry(self):
        """Dephasing log-neg is symmetric under p ↔ 1-p."""
        from qkdx.numerics.upper_bound import analytic_log_neg_dephasing
        for p in [0.1, 0.2, 0.3, 0.4]:
            assert analytic_log_neg_dephasing(p) == pytest.approx(
                analytic_log_neg_dephasing(1.0 - p), abs=1e-15
            )

    def test_invalid_parameter_raises(self):
        """Out-of-range parameters raise ValueError."""
        from qkdx.numerics.upper_bound import (
            analytic_log_neg_amplitude_damping,
            analytic_log_neg_dephasing,
            analytic_log_neg_depolarizing,
            analytic_log_neg_erasure,
        )
        for fn in [analytic_log_neg_amplitude_damping, analytic_log_neg_dephasing,
                   analytic_log_neg_depolarizing, analytic_log_neg_erasure]:
            with pytest.raises(ValueError):
                fn(-0.1)
            with pytest.raises(ValueError):
                fn(1.1)

    def test_erasure_log_neg_formula(self):
        """log_neg(erasure, p) = log₂(2-p). Verified by SymPy + direct PT computation.

        Erasure channel has dim_B=3, so we directly compute Choi+PT here in 2⊗3 space.
        """
        from qkdx.numerics.upper_bound import analytic_log_neg_erasure

        def erasure_choi_pt_eigvals(p):
            """6x6 PT eigenvalues for qubit erasure channel."""
            # |Φ⁺⟩ = (|00⟩+|11⟩)/√2 in C^2 ⊗ C^2 (input space)
            phi_plus = np.zeros(4, dtype=complex)
            phi_plus[0] = phi_plus[3] = 1.0 / math.sqrt(2)
            # Kraus: K0 = √(1-p)·[[1,0],[0,1],[0,0]] (3x2, identity on qubit→qubit)
            # Ke0 = √p·[[0,0],[0,0],[1,0]] (3x2, |0⟩→|e⟩)
            # Ke1 = √p·[[0,0],[0,0],[0,1]] (3x2, |1⟩→|e⟩)
            K0 = math.sqrt(1.0 - p) * np.array([[1, 0], [0, 1], [0, 0]], dtype=complex)
            Ke0 = math.sqrt(p) * np.array([[0, 0], [0, 0], [1, 0]], dtype=complex)
            Ke1 = math.sqrt(p) * np.array([[0, 0], [0, 0], [0, 1]], dtype=complex)
            I_A = np.eye(2, dtype=complex)
            rho = np.zeros((6, 6), dtype=complex)
            for K in [K0, Ke0, Ke1]:
                M = np.kron(I_A, K)  # (2*3) x (2*2) = 6x4
                v = M @ phi_plus
                rho += np.outer(v, v.conj())
            # PT on B (dim 3): index = 3*a + b
            rho_TB = np.zeros((6, 6), dtype=complex)
            for a in range(2):
                for b in range(3):
                    for c in range(2):
                        for d in range(3):
                            rho_TB[3*a+d, 3*c+b] = rho[3*a+b, 3*c+d]
            return np.linalg.eigvalsh(rho_TB)

        for p in [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
            eigs = erasure_choi_pt_eigvals(p)
            tn = float(np.sum(np.abs(eigs)))
            log_neg_num = math.log2(tn) if tn > 1.0 else 0.0
            analytic = analytic_log_neg_erasure(p)
            expected = math.log2(2.0 - p)
            print(f"  p={p}: trace_norm={tn:.6f}, analytic={analytic:.6f}, expected log₂(2-p)={expected:.6f}")
            assert analytic == pytest.approx(expected, abs=1e-12)
            assert analytic == pytest.approx(log_neg_num, abs=1e-9)


@_MOSEK_SKIP
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
