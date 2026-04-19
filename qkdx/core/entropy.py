"""Information-theoretic utility functions."""
from __future__ import annotations

import numpy as np


def binary_entropy(p: float) -> float:
    """h(p) = -p log2(p) - (1-p) log2(1-p).  Returns 0 for p in {0,1}."""
    if p <= 0.0:
        return 0.0
    if p >= 1.0:
        return 0.0
    return float(-p * np.log2(p) - (1.0 - p) * np.log2(1.0 - p))


def von_neumann_entropy(rho: "np.ndarray[np.complex128]", base: float = 2.0) -> float:  # type: ignore[type-arg]
    """S(ρ) = -Tr(ρ log ρ) in given base (default: bits)."""
    eigvals = np.linalg.eigvalsh(rho)
    eigvals = eigvals[eigvals > 0]
    return float(-np.sum(eigvals * np.log(eigvals)) / np.log(base))
