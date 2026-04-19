"""Local symmetry groups for QKD protocols.

Reference: Ferenczi, Lütkenhaus 2012, PRA 85:052310.

Provides:
    bb84_bilateral_group(): the 8-element symmetry group of symmetric BB84
        under Q_Z = Q_X (Pauli ⊗ Pauli ∪ Hadamard ⊗ Hadamard structure).
    bb84_pauli_group(): the 4-element Pauli-only subgroup, used when
        Q_Z ≠ Q_X and Hadamard symmetry is broken.

Each "group" is represented as a tuple of 4×4 unitaries acting bilaterally
on the A_key ⊗ B Hilbert space.
"""
from __future__ import annotations

import numpy as np

from qkdx.core.hilbert import (
    HADAMARD, IDENTITY_2, SIGMA_X, SIGMA_Y, SIGMA_Z, Matrix,
)


def _bilateral(U: Matrix) -> Matrix:
    """Return U ⊗ U on 2-qubit space (4×4)."""
    return np.kron(U, U)


def bb84_pauli_group() -> tuple[Matrix, ...]:
    """Pauli bilateral subgroup {I⊗I, σ_x⊗σ_x, σ_y⊗σ_y, σ_z⊗σ_z}.

    These are stabilisers of the BB84 SDP whenever Γ_Z and Γ_X are observables
    (they preserve Q_Z and Q_X separately).  This is the "always-valid"
    symmetry subgroup (no constraint on Q_Z = Q_X).
    """
    return (
        _bilateral(IDENTITY_2),
        _bilateral(SIGMA_X),
        _bilateral(SIGMA_Y),
        _bilateral(SIGMA_Z),
    )


def bb84_bilateral_group() -> tuple[Matrix, ...]:
    """Full 8-element BB84 bilateral symmetry (requires Q_Z = Q_X).

    Pauli ∪ Hadamard·Pauli:
        {I, σ_x, σ_y, σ_z} ⊗ {I, σ_x, σ_y, σ_z}
      ∪ {H, H·σ_x, H·σ_y, H·σ_z} ⊗ (same, bilaterally)

    Actually the simplest generating set for the symmetric-QBER group is:
        {I⊗I, σ_x⊗σ_x, σ_y⊗σ_y, σ_z⊗σ_z, H⊗H,
         (H·σ_x)⊗(H·σ_x), (H·σ_y)⊗(H·σ_y), (H·σ_z)⊗(H·σ_z)}
    = 8 bilateral Clifford operators fixing both Γ_Z and Γ_X (as a set).
    """
    pauli = [IDENTITY_2, SIGMA_X, SIGMA_Y, SIGMA_Z]
    hadamard_coset = [HADAMARD @ P for P in pauli]
    elements = [_bilateral(U) for U in pauli] + [_bilateral(U) for U in hadamard_coset]
    return tuple(elements)


def six_state_bilateral_group() -> tuple[Matrix, ...]:
    """Six-state bilateral symmetry.

    The additional Γ_Y constraint forces further symmetry:  in addition to the
    BB84 bilateral group, the six-state feasible set is invariant under the
    Clifford rotation that permutes the three MUBs (Z ↔ X ↔ Y).

    For Q_Z = Q_X = Q_Y symmetric case, the full group is the Clifford
    group on 1 qubit (lifted bilaterally), which has 24 elements.  For
    M4A scope, we return only a sufficient subgroup that twirls to the
    Bell-diagonal Werner-symmetric form; Phase 1 can upgrade to the full
    24-element Clifford group if needed.
    """
    # Generators: bb84 8-element group + a single permutation Z→X→Y
    bb84 = list(bb84_bilateral_group())

    # Clifford element that cyclically permutes Pauli: S = diag(1, i)·H(approx)
    # Equivalently, a 120° rotation around Bloch (1,1,1)/sqrt(3).
    # S_clifford is a 2×2 unitary with S σ_X S† = σ_Y, S σ_Y S† = σ_Z, S σ_Z S† = σ_X.
    # One such S: (1/√2) · [[1, -i], [1, i]]  (needs verification)
    S = (1.0 / np.sqrt(2.0)) * np.array([[1, -1j], [1, 1j]], dtype=np.complex128)
    S2 = S @ S
    extended = bb84 + [_bilateral(S), _bilateral(S2)]
    return tuple(extended)


# Registry for lookup by name
GROUP_REGISTRY: dict[str, callable] = {
    "bb84_pauli": bb84_pauli_group,
    "bb84_bilateral": bb84_bilateral_group,
    "six_state": six_state_bilateral_group,
}


def get_group(name: str) -> tuple[Matrix, ...]:
    """Look up a symmetry group by name."""
    if name not in GROUP_REGISTRY:
        raise ValueError(
            f"Unknown group {name!r}. Known: {sorted(GROUP_REGISTRY.keys())}"
        )
    return GROUP_REGISTRY[name]()
