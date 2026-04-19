"""Facial reduction for WLC SDP.

Reference: Hu-Im-Lin-Lütkenhaus-Wolkowicz 2022. *Robust Interior Point Method
for QKD Rate Computation.* Quantum 6:792. arXiv:2104.03847.

Scope of this module (M3 Level 2-3):
    * compute_face_projector: identify kernel of PSD equality constraints
      Tr(A_k · ρ) = 0 with A_k ⪰ 0  ⇒  supp(ρ) ⊆ ker(A_k). The minimal face
      is the PSD cone on the intersection of these kernels.
    * FacialReductionResult: data container for the projector + rank.
    * (legacy) detect_face / reduce_problem: pre-M3 stubs kept for
      backward compatibility with wlc.py epsilon-regularisation fallback.

Not in scope (deferred — see docs/literature/facial-reduction.md §6):
    * Hu 2022 robust IPM full algorithm
    * Dual LMI feasibility probe for implicit rank deficiency
    * Integration with CVXPY warm-start
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import cvxpy as cp
import numpy as np

from qkdx.core.hilbert import Matrix


# ---------------------------------------------------------------------------
# Primary API: explicit face projector from PSD equality constraints
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FacialReductionResult:
    """Result of facial reduction analysis."""
    projector: Matrix  # d × r isometry P such that supp(ρ) ⊆ range(P)
    rank: int          # r = dimension of the minimal face
    ambient_dim: int   # d = original SDP variable dimension

    def project(self, rho_full: Matrix) -> Matrix:
        """Project ambient ρ onto the face: P† ρ P (r × r)."""
        return self.projector.conj().T @ rho_full @ self.projector

    def lift(self, rho_reduced: Matrix) -> Matrix:
        """Lift r × r ρ back to ambient: P ρ_reduced P† (d × d)."""
        return self.projector @ rho_reduced @ self.projector.conj().T


def compute_face_projector(
    constraint_matrices: list[Matrix],
    targets: list[float],
    ambient_dim: int,
    atol: float = 1e-10,
) -> FacialReductionResult:
    """Compute the minimal-face projector for a set of PSD equality constraints.

    For each (A_k, b_k) with A_k ⪰ 0 and b_k == 0, feasibility forces
    supp(ρ) ⊆ ker(A_k).  The minimal face is the PSD cone restricted to the
    intersection of all such kernels.

    Constraints with b_k != 0 or A_k not PSD are skipped (they do not imply
    a rank reduction via this mechanism — cf. Hu 2022 §III which handles
    more general implicit reductions via dual LMI, deferred here).

    Args:
        constraint_matrices: list of d × d Hermitian matrices {A_k}
        targets: list of scalar values {b_k}
        ambient_dim: d (should match the square matrix size)
        atol: tolerance for PSD check and kernel extraction

    Returns:
        FacialReductionResult with d × r isometry P (r = face rank).
        When no constraint forces rank reduction, returns the identity
        projector (P = I_d, rank = d).
    """
    d = ambient_dim
    # Start with full space basis
    current_kernel_basis = np.eye(d, dtype=np.complex128)
    current_rank = d

    for A, b in zip(constraint_matrices, targets):
        if A.shape != (d, d):
            raise ValueError(f"Constraint matrix shape {A.shape} != ({d},{d})")
        if abs(b) > atol:
            continue  # Only target-zero constraints induce face reduction
        # Check A is Hermitian
        if not np.allclose(A, A.conj().T, atol=atol):
            continue
        # Check A is PSD
        eigvals = np.linalg.eigvalsh(A)
        if np.any(eigvals < -atol):
            continue  # Not PSD → skip
        # supp(ρ) ⊆ ker(A): restrict current_kernel_basis to ker(A)
        # Let B = current_kernel_basis (d × r_current).
        # A restricted to range(B): B† A B  (r_current × r_current Hermitian PSD).
        # Its kernel gives the new face subspace within range(B).
        A_restricted = current_kernel_basis.conj().T @ A @ current_kernel_basis
        eigvals_r, eigvecs_r = np.linalg.eigh(A_restricted)
        # Keep eigenvectors with eigenvalue ≈ 0
        kernel_mask = np.abs(eigvals_r) < atol
        if not np.any(kernel_mask):
            # A has no kernel within current face: contradicts b=0 constraint ⇒
            # only ρ=0 satisfies, but Tr(ρ)=1 rules it out. Return current state;
            # downstream solver should detect infeasibility.
            continue
        new_basis_in_current = eigvecs_r[:, kernel_mask]  # r_current × r_new
        current_kernel_basis = current_kernel_basis @ new_basis_in_current
        current_rank = current_kernel_basis.shape[1]
        if current_rank == 0:
            break

    return FacialReductionResult(
        projector=current_kernel_basis,
        rank=current_rank,
        ambient_dim=d,
    )


# ---------------------------------------------------------------------------
# Legacy stubs (kept for wlc.py epsilon-regularisation fallback)
# ---------------------------------------------------------------------------

def detect_face(
    constraints: list[cp.Constraint],
    variable: cp.Variable,
    atol: float = 1e-8,
) -> tuple[Matrix, int]:
    """DEPRECATED: heuristic face detection from CVXPY constraints.

    Use compute_face_projector directly with explicit constraint matrices
    for reliable results.  This stub is kept only to not break any
    pre-M3 callers.
    """
    d = variable.shape[0]
    face = np.eye(d, dtype=np.complex128)
    rank = int(np.round(np.trace(face).real))
    return face, rank


def reduce_problem(
    prob: cp.Problem,
    variable: cp.Variable,
) -> tuple[cp.Problem, Callable[[], Matrix]]:
    """Fallback Tikhonov regularisation: add ε·I to the SDP interior.

    Used by wlc.py _wlc_mosek epsilon_regularization path.  For a principled
    facial reduction, call compute_face_projector with the explicit
    constraint data (see qkdx.numerics.wlc._init_feasible for the pattern).
    """
    d = variable.shape[0]
    eps_feas = 1e-7
    new_constraints: list[cp.Constraint] = list(prob.constraints)
    identity_term = cp.Constant(eps_feas * np.eye(d, dtype=np.complex128))
    new_constraints_relaxed = [
        c for c in new_constraints if not _is_trace_zero_constraint(c)
    ]
    relaxed_prob = cp.Problem(
        prob.objective,
        new_constraints_relaxed + [variable >> identity_term],
    )

    def lift() -> Matrix:
        return variable.value  # type: ignore[return-value]

    return relaxed_prob, lift


def _is_trace_zero_constraint(con: cp.Constraint) -> bool:
    try:
        if isinstance(con, cp.constraints.zero.Zero):
            return True
    except Exception:
        pass
    return False
