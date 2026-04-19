"""Hilbert space primitives: vectors, matrices, common operators."""
from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

# Type alias used throughout the codebase.
Matrix = NDArray[np.complex128]

# ----- Standard qubit kets --------------------------------------------------
KET_0: Matrix = np.array([[1.0], [0.0]], dtype=np.complex128)
KET_1: Matrix = np.array([[0.0], [1.0]], dtype=np.complex128)
KET_PLUS: Matrix = np.array([[1.0], [1.0]], dtype=np.complex128) / np.sqrt(2)
KET_MINUS: Matrix = np.array([[1.0], [-1.0]], dtype=np.complex128) / np.sqrt(2)

# ----- Single-qubit gates ---------------------------------------------------
SIGMA_X: Matrix = np.array([[0, 1], [1, 0]], dtype=np.complex128)
SIGMA_Y: Matrix = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
SIGMA_Z: Matrix = np.array([[1, 0], [0, -1]], dtype=np.complex128)
IDENTITY_2: Matrix = np.eye(2, dtype=np.complex128)
HADAMARD: Matrix = np.array([[1, 1], [1, -1]], dtype=np.complex128) / np.sqrt(2)


def ket(index: int, dim: int) -> Matrix:
    """Return |index⟩ in C^dim as a column vector."""
    v = np.zeros((dim, 1), dtype=np.complex128)
    v[index, 0] = 1.0
    return v


def proj(v: Matrix) -> Matrix:
    """Return |v⟩⟨v|.  v may be a column vector or 1-D array."""
    v = np.asarray(v, dtype=np.complex128).reshape(-1, 1)
    v = v / np.linalg.norm(v)
    return v @ v.conj().T


def tensor(*arrays: Matrix) -> Matrix:
    """Kronecker (tensor) product of ≥1 matrices."""
    result = arrays[0]
    for a in arrays[1:]:
        result = np.kron(result, a)
    return result


def is_hermitian(A: Matrix, atol: float = 1e-10) -> bool:
    return bool(np.allclose(A, A.conj().T, atol=atol))


def is_density(rho: Matrix, atol: float = 1e-8) -> bool:
    """Check ρ is positive semidefinite with unit trace."""
    if not is_hermitian(rho, atol=atol):
        return False
    eigvals = np.linalg.eigvalsh(rho)
    if np.any(eigvals < -atol):
        return False
    return bool(np.isclose(np.trace(rho).real, 1.0, atol=atol))
