"""Tests for qkdx/numerics/facial.py (facial reduction)."""
from __future__ import annotations

import numpy as np
import pytest

from qkdx.core.hilbert import HADAMARD
from qkdx.numerics.facial import (
    FacialReductionResult, compute_face_projector,
)
from qkdx.protocols.bb84 import _gamma_qber_Z, _gamma_qber_X


# ---- No constraints → identity projector -------------------------------------

def test_no_constraints_returns_identity_projector() -> None:
    """Empty constraint list → full-space projector (no reduction)."""
    result = compute_face_projector([], [], ambient_dim=4)
    assert result.rank == 4
    assert np.allclose(result.projector, np.eye(4))


# ---- BB84 QBER=0 → rank 2 face ----------------------------------------------

def test_bb84_qber_Z_zero_rank_2() -> None:
    """Γ_Z = diag(0,1,1,0) with target 0 ⇒ supp(ρ) ⊆ ker(Γ_Z) = span{|00⟩,|11⟩}.

    Face rank should be 2.
    """
    Gamma_Z = _gamma_qber_Z()  # diag(0,1,1,0)
    result = compute_face_projector([Gamma_Z], [0.0], ambient_dim=4)
    assert result.rank == 2
    # Projector columns should span {|00⟩, |11⟩}
    P = result.projector  # 4 × 2
    # Check orthonormality
    assert np.allclose(P.conj().T @ P, np.eye(2), atol=1e-10)
    # Project a test density matrix in span{|00⟩,|11⟩}: should preserve trace
    rho_diag = np.diag([0.5, 0, 0, 0.5]).astype(np.complex128)
    rho_reduced = result.project(rho_diag)
    assert np.isclose(np.trace(rho_reduced).real, 1.0, atol=1e-12)
    # Lift back should recover (approximately) the same matrix
    rho_lifted = result.lift(rho_reduced)
    # Since rho_diag was already in the face, lift(project(rho_diag)) = rho_diag
    assert np.allclose(rho_lifted, rho_diag, atol=1e-10)


# ---- BB84 + X basis QBER=0: rank-1 face -------------------------------------

def test_bb84_qber_both_zero_rank_1() -> None:
    """Both Γ_Z=0 and Γ_X=0 ⇒ supp(ρ) must be in |Φ+⟩=(|00⟩+|11⟩)/√2 only.

    (Γ_X at target 0 restricts further: the intersection of ker(Γ_Z)
    and ker(Γ_X) inside span{|00⟩,|11⟩} is 1-dimensional, spanned by |Φ+⟩.)
    """
    Gamma_Z = _gamma_qber_Z()
    Gamma_X = _gamma_qber_X()
    result = compute_face_projector(
        [Gamma_Z, Gamma_X], [0.0, 0.0], ambient_dim=4,
    )
    assert result.rank == 1
    P = result.projector  # 4 × 1
    # Should be (a phase of) |Φ+⟩ = (|00⟩ + |11⟩)/√2
    v = P[:, 0]
    # Fix the global phase by requiring first nonzero entry real positive
    if v[0].real < 0:
        v = -v
    phi_plus = np.array([1, 0, 0, 1], dtype=np.complex128) / np.sqrt(2)
    # Check |<v|Φ+>| = 1
    overlap = abs(v.conj() @ phi_plus)
    assert overlap == pytest.approx(1.0, abs=1e-9)


# ---- Positive target values are skipped --------------------------------------

def test_positive_target_does_not_reduce_face() -> None:
    """Γ_Z with target 0.05 should NOT force rank reduction (Tr(Γ_Z ρ)=0.05 > 0)."""
    Gamma_Z = _gamma_qber_Z()
    result = compute_face_projector([Gamma_Z], [0.05], ambient_dim=4)
    assert result.rank == 4  # no reduction


# ---- Non-PSD constraint matrices are skipped --------------------------------

def test_non_psd_constraint_is_skipped() -> None:
    """A constraint matrix with negative eigenvalues shouldn't force reduction."""
    non_psd = np.array([
        [1.0, 0, 0, 0],
        [0, -1.0, 0, 0],
        [0, 0, 1.0, 0],
        [0, 0, 0, 1.0],
    ], dtype=np.complex128)
    result = compute_face_projector([non_psd], [0.0], ambient_dim=4)
    assert result.rank == 4  # no reduction because A not PSD


# ---- Lift and project are inverse on the face -------------------------------

def test_lift_project_inverse_on_face() -> None:
    """For ρ_reduced ∈ face, project(lift(ρ_reduced)) = ρ_reduced."""
    Gamma_Z = _gamma_qber_Z()
    result = compute_face_projector([Gamma_Z], [0.0], ambient_dim=4)
    rho_reduced = np.array([[0.3, 0.1j], [-0.1j, 0.7]], dtype=np.complex128)
    rho_lifted = result.lift(rho_reduced)
    rho_back = result.project(rho_lifted)
    assert np.allclose(rho_back, rho_reduced, atol=1e-10)


# ---- Shape validation --------------------------------------------------------

def test_shape_mismatch_raises() -> None:
    bad = np.eye(3, dtype=np.complex128)
    with pytest.raises(ValueError, match="shape"):
        compute_face_projector([bad], [0.0], ambient_dim=4)
