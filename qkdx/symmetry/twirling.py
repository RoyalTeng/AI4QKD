"""Twirling maps for symmetry reduction.

Reference: Ferenczi-Lütkenhaus 2012 §III.

Implements:
    twirl(rho, group): ρ ↦ (1/|G|) Σ_g U_g ρ U_g†
    werner_parameters(rho_bell_diag): extract (F, μ) from Bell-diagonal ρ
    werner_state(F, mu): construct Bell-diagonal ρ from (F, μ)
    check_invariant(rho, group, atol): verify ρ = twirl(ρ, group)
"""
from __future__ import annotations

import numpy as np

from qkdx.core.hilbert import Matrix


# Bell basis in 2-qubit standard basis {|00⟩,|01⟩,|10⟩,|11⟩}
BELL_PHI_PLUS: Matrix = np.array([1, 0, 0, 1], dtype=np.complex128).reshape(4, 1) / np.sqrt(2)
BELL_PHI_MINUS: Matrix = np.array([1, 0, 0, -1], dtype=np.complex128).reshape(4, 1) / np.sqrt(2)
BELL_PSI_PLUS: Matrix = np.array([0, 1, 1, 0], dtype=np.complex128).reshape(4, 1) / np.sqrt(2)
BELL_PSI_MINUS: Matrix = np.array([0, 1, -1, 0], dtype=np.complex128).reshape(4, 1) / np.sqrt(2)

# Change-of-basis matrix: columns are Bell kets in standard basis.
BELL_BASIS: Matrix = np.hstack([BELL_PHI_PLUS, BELL_PHI_MINUS, BELL_PSI_PLUS, BELL_PSI_MINUS])


def twirl(rho: Matrix, group: tuple[Matrix, ...]) -> Matrix:
    """Group average: (1/|G|) Σ_g U_g · ρ · U_g†.

    Args:
        rho: d × d density matrix (or Hermitian operator).
        group: tuple of d × d unitaries representing the group action.

    Returns:
        G-invariant d × d matrix.
    """
    n = len(group)
    if n == 0:
        raise ValueError("group must be non-empty")
    d = rho.shape[0]
    if rho.shape != (d, d):
        raise ValueError(f"rho must be square, got {rho.shape}")

    out = np.zeros_like(rho, dtype=np.complex128)
    for U in group:
        if U.shape != (d, d):
            raise ValueError(f"group element shape {U.shape} != ({d},{d})")
        out += U @ rho @ U.conj().T
    return out / n


def to_bell_basis(rho_std: Matrix) -> Matrix:
    """Transform 4×4 matrix from standard basis to Bell basis."""
    return BELL_BASIS.conj().T @ rho_std @ BELL_BASIS


def from_bell_basis(rho_bell: Matrix) -> Matrix:
    """Transform 4×4 matrix from Bell basis to standard basis."""
    return BELL_BASIS @ rho_bell @ BELL_BASIS.conj().T


def werner_state(F: float, mu: float) -> Matrix:
    """Construct a BB84-symmetric Werner state with 2 free parameters.

        ρ = F·|Φ+⟩⟨Φ+| + μ·(|Φ-⟩⟨Φ-| + |Ψ+⟩⟨Ψ+|) + (1-F-2μ)·|Ψ-⟩⟨Ψ-|

    Args:
        F: weight on |Φ+⟩ (dominant Bell component; 0 ≤ F ≤ 1)
        mu: weight on |Φ-⟩ = weight on |Ψ+⟩ (BB84 symmetry).

    Returns:
        4×4 Hermitian PSD density matrix in standard basis.
    """
    if not (0.0 <= F <= 1.0):
        raise ValueError(f"F must be in [0,1], got {F}")
    lam_psi_minus = 1.0 - F - 2.0 * mu
    if mu < -1e-12 or lam_psi_minus < -1e-12:
        raise ValueError(
            f"(F, μ) = ({F}, {mu}) not PSD: λ_Ψ- = {lam_psi_minus}"
        )
    rho_bell = np.diag([F, mu, mu, lam_psi_minus]).astype(np.complex128)
    return from_bell_basis(rho_bell)


def werner_parameters(rho: Matrix, atol: float = 1e-8) -> tuple[float, float, float]:
    """Extract (F, μ, λ_Ψ-) from a Bell-diagonal ρ in standard basis.

    Assumes ρ is BB84-symmetric: Bell-diagonal AND λ_Φ- = λ_Ψ+.
    Raises AssertionError if this symmetry is not satisfied within atol.

    Returns: (F, μ, λ_Ψ-) where F = λ_Φ+, μ = λ_Φ- = λ_Ψ+, λ_Ψ- = 1-F-2μ.
    """
    rho_bell = to_bell_basis(rho)
    # Off-diagonal in Bell basis should be ≈ 0
    off = rho_bell - np.diag(np.diag(rho_bell))
    if np.max(np.abs(off)) > atol:
        raise ValueError(
            f"ρ not Bell-diagonal: max off-diagonal = {np.max(np.abs(off))}"
        )
    F = rho_bell[0, 0].real
    lam_phi_minus = rho_bell[1, 1].real
    lam_psi_plus = rho_bell[2, 2].real
    lam_psi_minus = rho_bell[3, 3].real
    if abs(lam_phi_minus - lam_psi_plus) > atol:
        raise ValueError(
            f"ρ not BB84-symmetric: λ_Φ-={lam_phi_minus}, λ_Ψ+={lam_psi_plus}"
        )
    mu = (lam_phi_minus + lam_psi_plus) / 2.0
    return F, mu, lam_psi_minus


def check_invariant(
    rho: Matrix, group: tuple[Matrix, ...], atol: float = 1e-9,
) -> bool:
    """Verify ρ = twirl(ρ, group)."""
    return bool(np.allclose(rho, twirl(rho, group), atol=atol))
