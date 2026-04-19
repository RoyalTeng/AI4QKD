"""Quantum channels: Kraus maps and POVMs."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from qkdx.core.hilbert import Matrix


@dataclass(frozen=True)
class KrausMap:
    """Completely-positive (trace-non-increasing) map via Kraus operators.

    Attributes:
        kraus: sequence of matrices K_i, shape (dim_out, dim_in).
        dim_in:  input Hilbert space dimension.
        dim_out: output Hilbert space dimension.

    Invariant: Σ_i K_i† K_i ⪯ I_{dim_in}  (CPTNI).
    """
    kraus: tuple[Matrix, ...]
    dim_in: int
    dim_out: int

    def __post_init__(self) -> None:
        for K in self.kraus:
            if K.shape != (self.dim_out, self.dim_in):
                raise ValueError(
                    f"Kraus shape {K.shape} != (dim_out={self.dim_out}, dim_in={self.dim_in})"
                )

    def apply(self, rho: Matrix) -> Matrix:
        """Return Σ_i K_i ρ K_i†."""
        out = np.zeros((self.dim_out, self.dim_out), dtype=np.complex128)
        for K in self.kraus:
            out += K @ rho @ K.conj().T
        return out

    @staticmethod
    def identity(dim: int) -> "KrausMap":
        """Identity channel on C^dim."""
        return KrausMap(kraus=(np.eye(dim, dtype=np.complex128),), dim_in=dim, dim_out=dim)

    @staticmethod
    def from_unitary(U: Matrix) -> "KrausMap":
        d_out, d_in = U.shape
        return KrausMap(kraus=(np.asarray(U, dtype=np.complex128),), dim_in=d_in, dim_out=d_out)


@dataclass(frozen=True)
class POVM:
    """Positive-operator valued measure {M_k}.

    Invariant: Σ_k M_k = I (completeness).
    """
    elements: tuple[Matrix, ...]
    dim: int

    def __post_init__(self) -> None:
        total = sum(self.elements)
        if not np.allclose(total, np.eye(self.dim), atol=1e-10):
            raise ValueError("POVM elements do not sum to identity")
