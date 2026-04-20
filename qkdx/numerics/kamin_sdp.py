"""Kamin 2025 Choi-state SDP infrastructure (S2.5 Stage 2 A1).

Reference:
    - Kamin et al. 2025, arXiv:2406.10198v3, §4.3 (Eq. 30-31), §5.1 (Eq. 41-42),
      §6 (qubit BB84 specialization)
    - docs/literature/Kamin-2025.md §5.1 + §6.3

Core identity (Kamin Eq. 31):
    ρ_J^g = Tr_{A'}[(I_A ⊗ J) (|ξ^g⟩⟨ξ^g|^{T_{A'}} ⊗ I_B)]

where:
    - J ∈ Pos(A' ⊗ B) is the Choi matrix of channel ℰ: A' → B
    - |ξ^g⟩ ∈ H_A ⊗ H_{A'} is the (pure) source state
    - T_{A'} denotes partial transpose on A' subsystem
    - Tr_{A'} integrates out the A' subsystem, leaving ρ_J^g on H_A ⊗ H_B

CPTP constraint:   Tr_B(J) = I_{A'}   (trace-preserving on input)

Kamin's key-rate SDP (Eq. 42 simplified to W-unique + no acceptance-test slack):
    rate(p^hon) = inf_{J ≽ 0, Tr_B(J) = I_{A'}} W(ρ_J^g)
                  subject to observable constraints from honest distribution

For qubit BB84 with xi^g = xi^t = |Φ^+⟩ = (|00⟩ + |11⟩)/√2,
    W(ρ_J^g) = (1-γ)² · D(G(ρ_J^g) ‖ 𝒵 ∘ G(ρ_J^g))
where G is the key+sifting map (Eq. 63) and 𝒵 is the pinching map (Eq. 64).

This module provides:
    * partial_trace_B / partial_trace_A_prime  (numpy, Kraus-consistent)
    * partial_trace_B_cvxpy  (linear CVXPY variant for SDP constraints)
    * choi_of_identity_channel  (unit test primitive)
    * rho_J_from_choi           (numpy; Eq. 31 implementation)
    * rho_J_from_choi_cvxpy     (CVXPY; linear in J)
    * kamin_choi_sdp_qubit_bb84 (main entry — qubit BB84 Choi-state SDP)

Cross-validation: for qubit BB84 with symmetric QBER, Kamin SDP result
must match wlc_key_rate (qkdx/numerics/wlc.py) to solver tolerance
(~1e-3 bits/sift).  See tests/test_numerics/test_kamin_sdp.py.
"""
from __future__ import annotations

import math
import os
from typing import Any

import cvxpy as cp
import numpy as np

# Ensure MOSEK license is detected if user placed it at ~/mosek/mosek.lic
_DEFAULT_MOSEK_LIC = os.path.expanduser("~/mosek/mosek.lic")
if os.path.exists(_DEFAULT_MOSEK_LIC) and "MOSEKLM_LICENSE_FILE" not in os.environ:
    os.environ["MOSEKLM_LICENSE_FILE"] = _DEFAULT_MOSEK_LIC


# ---------------------------------------------------------------------------
# Partial trace helpers (numpy)
# ---------------------------------------------------------------------------

def partial_trace_B(M: np.ndarray, dim_A: int, dim_B: int) -> np.ndarray:
    """Compute Tr_B(M) where M lives on H_A ⊗ H_B (composite dim = dim_A·dim_B).

    Convention: the composite basis is indexed as |i⟩_A ⊗ |j⟩_B = |i·dim_B + j⟩.

    Formula:  [Tr_B(M)]_{ij} = Σ_k M[i·dim_B + k, j·dim_B + k]

    Args:
        M: square matrix of shape (dim_A·dim_B, dim_A·dim_B).
        dim_A: dimension of subsystem A (kept).
        dim_B: dimension of subsystem B (traced out).

    Returns:
        Tr_B(M), shape (dim_A, dim_A).
    """
    if M.shape != (dim_A * dim_B, dim_A * dim_B):
        raise ValueError(
            f"M shape {M.shape} incompatible with dim_A·dim_B = {dim_A * dim_B}"
        )
    # Reshape to 4-index tensor: M[i, k, j, l] with i,j ∈ A, k,l ∈ B
    M4 = M.reshape(dim_A, dim_B, dim_A, dim_B)
    # Tr_B: sum over k = l
    return np.einsum("ikjk->ij", M4)


def partial_trace_A_prime(M: np.ndarray, dim_A_prime: int, dim_B: int) -> np.ndarray:
    """Compute Tr_{A'}(M) where M lives on H_{A'} ⊗ H_B, A' being the FIRST
    subsystem in the tensor order (i.e., basis |k⟩_{A'} ⊗ |j⟩_B = |k·dim_B + j⟩).

    Formula:  [Tr_{A'}(M)]_{j,l} = Σ_k M[k·dim_B + j, k·dim_B + l]

    Args:
        M: square matrix of shape (dim_A'·dim_B, dim_A'·dim_B).
        dim_A_prime: dimension of A' (traced out, FIRST subsystem).
        dim_B: dimension of B (kept, SECOND subsystem).

    Returns:
        Tr_{A'}(M), shape (dim_B, dim_B).
    """
    if M.shape != (dim_A_prime * dim_B, dim_A_prime * dim_B):
        raise ValueError(
            f"M shape {M.shape} incompatible with d_A'·d_B = {dim_A_prime * dim_B}"
        )
    M4 = M.reshape(dim_A_prime, dim_B, dim_A_prime, dim_B)
    # Tr over first subsystem (i = k):
    return np.einsum("kjkl->jl", M4)


def partial_trace_AA_prime(M: np.ndarray, dim_A: int, dim_A_prime: int,
                           dim_B: int) -> np.ndarray:
    """Compute Tr_{A'}(M) where M lives on H_A ⊗ H_{A'} ⊗ H_B.

    Traces out middle subsystem A', leaving result on H_A ⊗ H_B.

    Convention: composite basis |i⟩_A ⊗ |k⟩_{A'} ⊗ |j⟩_B.

    Formula:
        [Tr_{A'}(M)]_{(i,j),(i',j')} = Σ_k M_{(i,k,j),(i',k,j')}
    """
    D = dim_A * dim_A_prime * dim_B
    if M.shape != (D, D):
        raise ValueError(
            f"M shape {M.shape} incompatible with d_A·d_A'·d_B = {D}"
        )
    M6 = M.reshape(dim_A, dim_A_prime, dim_B,
                   dim_A, dim_A_prime, dim_B)
    # Trace over A' indices (axis 1 and 4)
    # Result indexed (i, j, i', j')
    M4 = np.einsum("ikjlkm->ijlm", M6)
    return M4.reshape(dim_A * dim_B, dim_A * dim_B)


def partial_transpose_A_prime(M: np.ndarray, dim_A: int,
                              dim_A_prime: int) -> np.ndarray:
    """Partial transpose on the A' subsystem of M ∈ H_A ⊗ H_{A'}.

    Formula:  M^{T_{A'}}_{(i,k),(j,l)} = M_{(i,l),(j,k)}

    Used in Kamin Eq. 31 for |ξ^g⟩⟨ξ^g|^{T_{A'}}.
    """
    D = dim_A * dim_A_prime
    if M.shape != (D, D):
        raise ValueError(f"M shape {M.shape} incompatible with d_A·d_A' = {D}")
    M4 = M.reshape(dim_A, dim_A_prime, dim_A, dim_A_prime)
    # Swap A' indices: (i,k,j,l) → (i,l,j,k)
    M4_T = np.transpose(M4, axes=(0, 3, 2, 1))
    return M4_T.reshape(D, D)


# ---------------------------------------------------------------------------
# Choi matrix primitives
# ---------------------------------------------------------------------------

def choi_of_identity_channel(dim: int) -> np.ndarray:
    """Unnormalized identity-channel Choi matrix J_id = Σ_{ij} |i⟩⟨j|_{A'} ⊗ |i⟩⟨j|_B.

    Satisfies:
        - Tr_B(J_id) = I_{A'}           (trace-preserving)
        - J_id is rank-1, PSD, trace = dim

    Equivalent form:  J_id = dim · |Φ^+⟩⟨Φ^+| on (A', B) with
                       |Φ^+⟩ = Σ_i |i⟩_{A'}|i⟩_B / √dim.

    Args:
        dim: common dimension of A' and B (single channel).

    Returns:
        J_id of shape (dim², dim²).
    """
    if dim < 1:
        raise ValueError(f"dim must be ≥ 1, got {dim}")
    # Build |Ω⟩ = Σ_i |i⟩|i⟩ (unnormalized)
    omega = np.zeros(dim * dim, dtype=np.complex128)
    for i in range(dim):
        omega[i * dim + i] = 1.0
    return np.outer(omega, omega.conj())


def rho_J_from_choi(
    J: np.ndarray,
    xi: np.ndarray,
    dim_A: int,
    dim_A_prime: int,
    dim_B: int,
) -> np.ndarray:
    """Compute ρ_J^g = Tr_{A'}[(I_A ⊗ J) (|ξ⟩⟨ξ|^{T_{A'}} ⊗ I_B)]  (Kamin Eq. 31).

    Numpy implementation.  The CVXPY version `rho_J_from_choi_cvxpy` below
    mirrors this exactly but returns a CVXPY expression linear in J.

    Args:
        J: Choi matrix on A' ⊗ B, shape (d_A'·d_B, d_A'·d_B).
        xi: pure source state vector on A ⊗ A', shape (d_A·d_A',).
        dim_A, dim_A_prime, dim_B: subsystem dimensions.

    Returns:
        ρ_J on A ⊗ B, shape (d_A·d_B, d_A·d_B).
    """
    # 1) |ξ⟩⟨ξ|^{T_{A'}} on A ⊗ A'
    xi_xi = np.outer(xi, xi.conj())
    xi_xi_T = partial_transpose_A_prime(xi_xi, dim_A=dim_A,
                                        dim_A_prime=dim_A_prime)

    # 2) |ξ⟩⟨ξ|^{T_{A'}} ⊗ I_B on A ⊗ A' ⊗ B
    I_B = np.eye(dim_B, dtype=np.complex128)
    xi_xi_T_kron_I = np.kron(xi_xi_T, I_B)  # shape: (d_A·d_A'·d_B,)²

    # 3) I_A ⊗ J on A ⊗ A' ⊗ B
    I_A = np.eye(dim_A, dtype=np.complex128)
    IA_kron_J = np.kron(I_A, J)

    # 4) Product
    product = IA_kron_J @ xi_xi_T_kron_I

    # 5) Tr_{A'}: integrate middle subsystem
    return partial_trace_AA_prime(product, dim_A=dim_A,
                                  dim_A_prime=dim_A_prime, dim_B=dim_B)


# ---------------------------------------------------------------------------
# CVXPY variants (linear in J for SDP)
# ---------------------------------------------------------------------------

def partial_trace_B_cvxpy(J_expr: cp.Expression, dim_A: int,
                          dim_B: int) -> cp.Expression:
    """Partial trace over B as a CVXPY expression linear in J_expr.

    Uses explicit Σ_k (I_A ⊗ ⟨k|_B) J (I_A ⊗ |k⟩_B) form so the result is
    linear in J (CVXPY-supported).
    """
    result = cp.Constant(np.zeros((dim_A, dim_A), dtype=np.complex128))
    for k in range(dim_B):
        # Projector |k⟩⟨k|_B
        e_k = np.zeros(dim_B, dtype=np.complex128)
        e_k[k] = 1.0
        # Operator (I_A ⊗ ⟨k|_B): shape (dim_A, dim_A·dim_B)
        left = np.kron(np.eye(dim_A, dtype=np.complex128), e_k.conj()[None, :])
        right = np.kron(np.eye(dim_A, dtype=np.complex128), e_k[:, None])
        result = result + cp.Constant(left) @ J_expr @ cp.Constant(right)
    return result


def rho_J_from_choi_cvxpy(
    J_expr: cp.Expression,
    xi_xi_T_kron_I_const: np.ndarray,
    dim_A: int,
    dim_A_prime: int,
    dim_B: int,
) -> cp.Expression:
    """CVXPY expression for ρ_J^g (Kamin Eq. 31), linear in J.

    Args:
        J_expr: CVXPY Hermitian variable on A' ⊗ B.
        xi_xi_T_kron_I_const: precomputed |ξ⟩⟨ξ|^{T_{A'}} ⊗ I_B (numpy const).
        dim_A, dim_A_prime, dim_B: subsystem dimensions.

    Returns:
        ρ_J as a CVXPY expression of shape (d_A·d_B, d_A·d_B).
    """
    I_A = np.eye(dim_A, dtype=np.complex128)

    # (I_A ⊗ J): block structure of size dim_A × dim_A blocks of (A'B)
    # In CVXPY, build via cp.bmat.
    blocks: list[list[cp.Expression]] = []
    zero_block = cp.Constant(
        np.zeros((dim_A_prime * dim_B, dim_A_prime * dim_B), dtype=np.complex128)
    )
    for i in range(dim_A):
        row = []
        for j in range(dim_A):
            if i == j:
                row.append(J_expr)
            else:
                row.append(zero_block)
        blocks.append(row)
    IA_kron_J = cp.bmat(blocks)  # shape (d_A·d_A'·d_B, d_A·d_A'·d_B)

    # Product
    product = IA_kron_J @ cp.Constant(xi_xi_T_kron_I_const)

    # Tr_{A'}: Σ_k (I_A ⊗ ⟨k|_{A'} ⊗ I_B) · product · (I_A ⊗ |k⟩_{A'} ⊗ I_B)
    I_B = np.eye(dim_B, dtype=np.complex128)
    D_out = dim_A * dim_B
    result: cp.Expression = cp.Constant(np.zeros((D_out, D_out),
                                                  dtype=np.complex128))
    for k in range(dim_A_prime):
        e_k = np.zeros(dim_A_prime, dtype=np.complex128)
        e_k[k] = 1.0
        # Left: I_A ⊗ ⟨k|_{A'} ⊗ I_B, shape (d_A·d_B, d_A·d_A'·d_B)
        left_mat = np.kron(np.kron(I_A, e_k.conj()[None, :]), I_B)
        right_mat = np.kron(np.kron(I_A, e_k[:, None]), I_B)
        result = result + cp.Constant(left_mat) @ product @ cp.Constant(right_mat)
    return result


# ---------------------------------------------------------------------------
# qubit BB84 specialization: G-map and Z-pinching as CVXPY expressions
# ---------------------------------------------------------------------------

def _bb84_G_Z_expressions(rho_J_expr: cp.Expression) -> tuple[cp.Expression, cp.Expression]:
    """Apply BB84 G-map and Z-pinching to ρ_J (4×4 on A⊗B).

    The BB84 key+sifting map G: ρ_{AB} → X with X on key-register:
        For the Z-basis single-photon sifted state, X = ρ (the state ITSELF
        in key-register form, since A register is already the key bit).

    Actually for the simplest BB84 conditional state form (4×4 Werner on
    key_A ⊗ key_B), G is:
        G(ρ) = Σ_{i} |i⟩⟨i|_{key} ⊗ ⟨i|_A ρ |i⟩_A   (pinch Alice's key bit)

    But here we want matching with the existing WLC framework.  The existing
    BB84 protocol in this repo uses:
        ρ (4×4 Werner) → G(ρ) directly (identity-like; Alice register already classical)
        Z pinching: diagonal of G(ρ)

    To keep THIS first-pass implementation narrow and testable against WLC,
    we use the SAME G and Z as `_wlc_mosek` via `_construct_G_map` (from
    wlc.py).  That way kamin_choi_sdp and wlc_key_rate minimize the same
    objective over different variable sets.
    """
    # Here ρ_J_expr is 4×4 on A (key bit) ⊗ B (effective bit after Charlie).
    # G: 4×4 → 4×4 identity is used by the BB84 Z-basis conditional state
    # as implemented in wlc.py _construct_G_map.  We replicate.
    # Concretely: the BB84 G-map is 2-qubit key pinching (Eq. 63 of Kamin
    # is equivalent here after source-replacement).  X = diag-pinching of
    # key register; Y = further Z-pinching.
    # Using identity structure for cross-check:
    X_expr = rho_J_expr  # G is identity at the conditional-state level
    # Z pinching: keep diagonal blocks in key register (trivial for 2x2)
    # For BB84 EB Werner form, Y = diag(rho_J) pinched on key register.
    # Construct via explicit Kraus {|0⟩⟨0|⊗I, |1⟩⟨1|⊗I}:
    e0 = np.array([[1, 0], [0, 0]], dtype=np.complex128)
    e1 = np.array([[0, 0], [0, 1]], dtype=np.complex128)
    K_0 = np.kron(e0, np.eye(2, dtype=np.complex128))
    K_1 = np.kron(e1, np.eye(2, dtype=np.complex128))
    Y_expr = (cp.Constant(K_0) @ rho_J_expr @ cp.Constant(K_0.conj().T) +
              cp.Constant(K_1) @ rho_J_expr @ cp.Constant(K_1.conj().T))
    return X_expr, Y_expr


# ---------------------------------------------------------------------------
# Main SDP entry point
# ---------------------------------------------------------------------------

def kamin_choi_sdp_qubit_bb84(
    qber: float,
    gamma: float = 0.01,
    solver: str = "MOSEK",
    epsilon_regularization: float = 1e-9,
    return_J: bool = False,
    verbose: bool = False,
) -> dict[str, Any]:
    """Kamin Choi-state SDP for qubit BB84 — Stage 2 A1.

    Solves:
        min_J  D(G(ρ_J^g) ‖ 𝒵(G(ρ_J^g)))
        subject to:
            J ≽ 0
            Tr_B(J) = I_{A'}      (trace-preserving channel)
            Tr(Γ_Z · ρ_J^g) = qber
            Tr(Γ_X · ρ_J^g) = qber

    where:
        ρ_J^g = Tr_{A'}[(I_A ⊗ J)(|ξ⟩⟨ξ|^{T_{A'}} ⊗ I_B)],
        |ξ⟩ = (|00⟩ + |11⟩) / √2,
        Γ_Z, Γ_X are BB84 QBER observables.

    Cross-validates against wlc_key_rate: for symmetric QBER, result must
    match within solver tolerance (~1e-3 bits/sift).

    Args:
        qber: observed Z-basis AND X-basis QBER (symmetric BB84).
        gamma: test-round probability (used only for API compatibility;
               does not affect h_per_sift per Kamin §4.3).
        solver: CVXPY solver; "MOSEK" required for cp.quantum_rel_entr.
        epsilon_regularization: (1-ε) convex combination with I/d to avoid
                                strictly-rank-deficient G(ρ) (matches
                                wlc._wlc_mosek convention).
        return_J: if True, also return the optimal Choi matrix.
        verbose: pass to solver.

    Returns:
        dict with keys:
            h_per_sift : quantum relative entropy in bits (= objective / ln 2)
            status     : solver status string
            value_nat  : raw objective in nats (= cvxpy cp.quantum_rel_entr output)
            solver     : solver used
            J          : (only if return_J=True) optimal Choi matrix
    """
    if not (0.0 <= qber < 0.5):
        raise ValueError(f"qber must be in [0, 0.5), got {qber}")
    if not (0.0 < gamma < 1.0):
        raise ValueError(f"gamma must be in (0, 1), got {gamma}")

    dim_A = dim_A_prime = dim_B = 2

    # Source state |ξ⟩ = (|00⟩ + |11⟩)/√2 on A ⊗ A'
    xi = np.zeros(dim_A * dim_A_prime, dtype=np.complex128)
    xi[0] = 1.0 / math.sqrt(2)
    xi[3] = 1.0 / math.sqrt(2)
    xi_xi = np.outer(xi, xi.conj())
    xi_xi_T = partial_transpose_A_prime(xi_xi, dim_A=dim_A,
                                        dim_A_prime=dim_A_prime)
    # Precompute |ξ⟩⟨ξ|^{T_{A'}} ⊗ I_B  (constant, for CVXPY expression)
    xi_xi_T_kron_I = np.kron(xi_xi_T, np.eye(dim_B, dtype=np.complex128))

    # CVXPY variable: J on A' ⊗ B (complex Hermitian PSD)
    D_J = dim_A_prime * dim_B  # = 4
    J_var = cp.Variable((D_J, D_J), hermitian=True)

    # Constraints
    constraints: list[cp.Constraint] = [J_var >> 0]

    # Trace-preserving: Tr_B(J) = I_{A'}
    tr_B_J = partial_trace_B_cvxpy(J_var, dim_A=dim_A_prime, dim_B=dim_B)
    constraints.append(tr_B_J == np.eye(dim_A_prime, dtype=np.complex128))

    # ρ_J (4×4 on A ⊗ B) as linear CVXPY expression
    rho_J_expr = rho_J_from_choi_cvxpy(
        J_expr=J_var,
        xi_xi_T_kron_I_const=xi_xi_T_kron_I,
        dim_A=dim_A,
        dim_A_prime=dim_A_prime,
        dim_B=dim_B,
    )

    # BB84 QBER observables
    from qkdx.protocols.bb84 import _gamma_qber_Z, _gamma_qber_X
    Gamma_Z = _gamma_qber_Z()
    Gamma_X = _gamma_qber_X()
    constraints.append(
        cp.real(cp.trace(cp.Constant(Gamma_Z) @ rho_J_expr)) == float(qber)
    )
    constraints.append(
        cp.real(cp.trace(cp.Constant(Gamma_X) @ rho_J_expr)) == float(qber)
    )

    # Objective: D(G(ρ_J) ‖ 𝒵(G(ρ_J)))
    # Use regularization for numerical stability (match _wlc_mosek convention)
    d_X = dim_A * dim_B  # = 4
    tau_I = np.eye(d_X, dtype=np.complex128) / d_X  # maximally mixed
    X_expr, Y_expr = _bb84_G_Z_expressions(rho_J_expr)
    X_reg = (1.0 - epsilon_regularization) * X_expr + cp.Constant(
        epsilon_regularization * tau_I
    )

    # cp.quantum_rel_entr requires explicit Hermitian aux variables
    X_aux = cp.Variable((d_X, d_X), hermitian=True)
    Y_aux = cp.Variable((d_X, d_X), hermitian=True)
    constraints.append(X_aux == X_reg)
    constraints.append(Y_aux == Y_expr)

    objective = cp.Minimize(cp.quantum_rel_entr(X_aux, Y_aux))

    prob = cp.Problem(objective, constraints)
    mosek_params = {
        "MSK_DPAR_INTPNT_CO_TOL_REL_GAP": 1e-8,
        "MSK_DPAR_INTPNT_CO_TOL_PFEAS": 1e-8,
        "MSK_DPAR_INTPNT_CO_TOL_DFEAS": 1e-8,
        "MSK_IPAR_INTPNT_MAX_ITERATIONS": 1000,
    }
    prob.solve(solver=solver, verbose=verbose,
               mosek_params=mosek_params if solver == "MOSEK" else {})

    if prob.status not in {"optimal", "optimal_inaccurate"}:
        raise cp.SolverError(
            f"Kamin Choi SDP failed: status={prob.status}, value={prob.value}"
        )

    # cp.quantum_rel_entr returns in nats; convert to bits for h_per_sift
    value_nat = float(prob.value)
    h_per_sift = value_nat / math.log(2.0)

    result = {
        "h_per_sift": h_per_sift,
        "status": prob.status,
        "value_nat": value_nat,
        "solver": solver,
    }
    if return_J:
        result["J"] = np.array(J_var.value, dtype=np.complex128)
    return result
