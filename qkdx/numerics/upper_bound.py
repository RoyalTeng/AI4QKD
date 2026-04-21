"""Numerical upper bound via Relative Entropy of Entanglement (Phase 2 U3.7).

Reference:
    - Vidal-Werner 2002, PRA 65:032314 (E_R as PPT-relaxed SDP for 2-qubit)
    - Horodecki-Horodecki-Horodecki 1996, PLA 223:1 (PPT = SEP for 2⊗2)
    - PLOB 2017 Eq. 19 (bosonic closed forms)
    - RESEARCH_PLAN §4.4 U3.7 Layer 5.3 SDP

Core formula (Vidal-Werner 2002):
    E_R(ρ) = inf_{σ ∈ SEP}  D(ρ ‖ σ)
    E_R^PPT(ρ) = inf_{σ ∈ PPT}  D(ρ ‖ σ)     (upper bound; equal for 2⊗2)
    where PPT = {σ ≥ 0 : Tr[σ] = 1, σ^{T_B} ≥ 0}

Channel capacity (tele-simulable channels):
    E_R(N) = E_R(J_N / dim_A)    where J_N is Choi matrix of N
    For the relaxed PPT form:
        E_R^PPT(N) = E_R^PPT(J_N / dim_A)

Quantum relative entropy D(ρ ‖ σ) is convex; with CVXPY
`cp.quantum_rel_entr(ρ, σ)` + MOSEK solver, the above SDP is directly
solvable for small dimensions (typically dim_A⊗dim_B ≤ 16).

Module scope:
    - e_r_ppt_2qubit(rho): PPT-relaxed E_R for 2-qubit states
    - e_r_channel_ppt(kraus_ops, dim_A, dim_B): channel E_R^PPT via Choi
    - Validation helpers against known closed forms (depolarizing, amplitude
      damping, identity)
    - DV-gap analysis: compare against Kamin achievable rates
"""
from __future__ import annotations

import math
import os

import cvxpy as cp
import numpy as np

_DEFAULT_MOSEK_LIC = os.path.expanduser("~/mosek/mosek.lic")
if os.path.exists(_DEFAULT_MOSEK_LIC) and "MOSEKLM_LICENSE_FILE" not in os.environ:
    os.environ["MOSEKLM_LICENSE_FILE"] = _DEFAULT_MOSEK_LIC


# ---------------------------------------------------------------------------
# Partial transpose (on system B of bipartite state)
# ---------------------------------------------------------------------------

def partial_transpose_B(rho: np.ndarray, dim_A: int, dim_B: int) -> np.ndarray:
    """Compute ρ^{T_B} for a bipartite state on H_A ⊗ H_B.

    Reshape to (dim_A, dim_B, dim_A, dim_B), transpose last two indices (B
    subsystem), reshape back.
    """
    if rho.shape != (dim_A * dim_B, dim_A * dim_B):
        raise ValueError(
            f"rho shape {rho.shape} != {(dim_A * dim_B,)*2}"
        )
    rho_4 = rho.reshape(dim_A, dim_B, dim_A, dim_B)
    rho_TB = rho_4.transpose(0, 3, 2, 1)  # swap B indices only
    return rho_TB.reshape(dim_A * dim_B, dim_A * dim_B)


def partial_transpose_B_cvxpy(
    rho_expr: cp.Expression, dim_A: int, dim_B: int,
) -> cp.Expression:
    """CVXPY-friendly partial transpose on B subsystem.

    Works for symbolic rho_expr by building index permutation explicitly.
    For dim_A · dim_B × dim_A · dim_B matrix, PT_B swaps (a,b,a',b') →
    (a,b',a',b).
    """
    d = dim_A * dim_B
    # Build permutation matrix P such that P ρ P^T = ρ^{T_B} (operator level)
    # Actually PT isn't a similarity transform — it's an element-wise
    # reshuffle. Build via explicit index assignment.
    # For CVXPY, we can construct the result by summing projector terms.
    blocks = []
    for a in range(dim_A):
        row_blocks = []
        for a_p in range(dim_A):
            # sub-block (dim_B × dim_B) for (a, a')
            sub = rho_expr[
                a * dim_B:(a + 1) * dim_B,
                a_p * dim_B:(a_p + 1) * dim_B,
            ]
            # transpose the B-subblock
            row_blocks.append(cp.transpose(sub))
        blocks.append(cp.hstack(row_blocks))
    return cp.vstack(blocks)


# ---------------------------------------------------------------------------
# E_R^PPT SDP for 2-qubit (and small dim) states
# ---------------------------------------------------------------------------

def e_r_ppt(
    rho: np.ndarray,
    dim_A: int,
    dim_B: int,
    solver: str = "MOSEK",
    epsilon_regularization: float = 1e-9,
    verbose: bool = False,
) -> dict:
    """Relative entropy of entanglement under PPT-relaxed separable cone.

    Solves:
        min_σ  D(ρ ‖ σ)
        s.t. σ ≥ 0, Tr[σ] = 1, σ^{T_B} ≥ 0

    For 2⊗2, PPT = SEP (Horodecki 1996) so result is exactly E_R(ρ).
    For higher dims, gives an UPPER BOUND on E_R(ρ).

    Args:
        rho: d_A·d_B × d_A·d_B Hermitian PSD unit-trace state.
        dim_A, dim_B: subsystem dimensions.
        solver: CVXPY solver (MOSEK required for quantum_rel_entr).
        epsilon_regularization: (1-ε)·σ + ε·I/d for numerical stability.
        verbose: solver verbosity.

    Returns:
        dict with keys:
          E_R_ppt_bits: E_R^PPT in bits
          E_R_ppt_nats: raw nats value
          sigma_opt: optimal closest PPT state
          status: solver status
    """
    d = dim_A * dim_B
    if rho.shape != (d, d):
        raise ValueError(f"rho shape {rho.shape} != ({d}, {d})")
    # Symmetrize (numerical hygiene)
    rho = 0.5 * (rho + rho.conj().T)

    sigma = cp.Variable((d, d), hermitian=True)
    constraints = [
        sigma >> 0,
        cp.trace(sigma) == 1.0,
    ]
    # PPT constraint: sigma^{T_B} >> 0
    sigma_TB = partial_transpose_B_cvxpy(sigma, dim_A, dim_B)
    constraints.append(sigma_TB >> 0)

    # Regularize sigma for strict positivity in quantum_rel_entr
    tau_I = np.eye(d, dtype=np.complex128) / d
    sigma_reg = (1.0 - epsilon_regularization) * sigma + cp.Constant(
        epsilon_regularization * tau_I
    )

    # Similarly regularize rho if near-rank-deficient
    rho_reg = (
        (1.0 - epsilon_regularization) * rho
        + epsilon_regularization * (np.eye(d) / d)
    )
    rho_reg = np.asarray(rho_reg, dtype=np.complex128)

    # cp.quantum_rel_entr requires explicit hermitian aux variables
    rho_aux = cp.Variable((d, d), hermitian=True)
    sigma_aux = cp.Variable((d, d), hermitian=True)
    constraints.append(rho_aux == cp.Constant(rho_reg))
    constraints.append(sigma_aux == sigma_reg)

    prob = cp.Problem(
        cp.Minimize(cp.quantum_rel_entr(rho_aux, sigma_aux)),
        constraints,
    )
    mosek_params = {
        "MSK_DPAR_INTPNT_CO_TOL_REL_GAP": 1e-8,
        "MSK_DPAR_INTPNT_CO_TOL_PFEAS": 1e-8,
        "MSK_DPAR_INTPNT_CO_TOL_DFEAS": 1e-8,
        "MSK_IPAR_INTPNT_MAX_ITERATIONS": 2000,
    }
    prob.solve(solver=solver, verbose=verbose,
               mosek_params=mosek_params if solver == "MOSEK" else {})

    if prob.status not in {"optimal", "optimal_inaccurate"}:
        raise cp.SolverError(
            f"E_R PPT SDP failed: status={prob.status}, value={prob.value}"
        )

    value_nat = float(prob.value)
    E_R_bits = value_nat / math.log(2.0)

    return {
        "E_R_ppt_bits": E_R_bits,
        "E_R_ppt_nats": value_nat,
        "sigma_opt": np.array(sigma.value, dtype=np.complex128),
        "status": prob.status,
    }


# ---------------------------------------------------------------------------
# Channel capacity via Choi matrix
# ---------------------------------------------------------------------------

def choi_state_from_kraus(
    kraus_ops: list[np.ndarray], dim_A: int,
) -> np.ndarray:
    """Build Choi state ρ_{N} = (I ⊗ N)(|Φ⁺⟩⟨Φ⁺|) with |Φ⁺⟩ = Σ|ii⟩/√d_A.

    For a channel N: L(H_in) → L(H_out), the Choi STATE (normalized so
    Tr = 1) is:
        ρ_N = (I ⊗ N)(|Φ⁺⟩⟨Φ⁺|)
    This is trace-1 iff N is TP.  The Choi MATRIX (unnormalized) is
    d_A · ρ_N; channel capacity uses the normalized state.
    """
    phi = np.zeros(dim_A * dim_A, dtype=np.complex128)
    for i in range(dim_A):
        phi[i * dim_A + i] = 1.0
    phi /= math.sqrt(dim_A)
    phi_proj = np.outer(phi, phi.conj())  # |Φ⁺⟩⟨Φ⁺| on H_A ⊗ H_A'

    # Apply N to second subsystem
    # (I ⊗ N)(|Φ⁺⟩⟨Φ⁺|) = Σ_k (I ⊗ K_k) |Φ⁺⟩⟨Φ⁺| (I ⊗ K_k†)
    dim_out = kraus_ops[0].shape[0]
    rho = np.zeros((dim_A * dim_out, dim_A * dim_out), dtype=np.complex128)
    for K in kraus_ops:
        IK = np.kron(np.eye(dim_A), K)
        rho += IK @ phi_proj @ IK.conj().T
    return 0.5 * (rho + rho.conj().T)  # symmetrize


def e_r_channel_ppt(
    kraus_ops: list[np.ndarray],
    dim_A: int,
    solver: str = "MOSEK",
    **kwargs,
) -> dict:
    """E_R^PPT of a channel via its Choi state.

    Args:
        kraus_ops: list of Kraus operators K_k (each d_out × d_in).
        dim_A: input dimension d_in.

    Returns:
        dict with:
          E_R_channel_bits: channel E_R^PPT bound (bits/channel use)
          rho_choi: Choi state
          sigma_opt, status: from e_r_ppt
    """
    dim_out = kraus_ops[0].shape[0]
    rho = choi_state_from_kraus(kraus_ops, dim_A)
    result = e_r_ppt(rho, dim_A=dim_A, dim_B=dim_out, solver=solver, **kwargs)
    result["rho_choi"] = rho
    result["E_R_channel_bits"] = result["E_R_ppt_bits"]
    return result


# ---------------------------------------------------------------------------
# Standard qubit channels (Kraus operators)
# ---------------------------------------------------------------------------

def kraus_identity_qubit() -> list[np.ndarray]:
    return [np.eye(2, dtype=np.complex128)]


def kraus_depolarizing_qubit(p: float) -> list[np.ndarray]:
    """Qubit depolarizing channel: ρ → (1-p)·ρ + p·I/2.

    Kraus ops: √(1-3p/4)·I, √(p/4)·X, √(p/4)·Y, √(p/4)·Z.
    """
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"p must be in [0, 1], got {p}")
    I = np.eye(2, dtype=np.complex128)
    X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    q0 = math.sqrt(1.0 - 3.0 * p / 4.0)
    q1 = math.sqrt(p / 4.0)
    return [q0 * I, q1 * X, q1 * Y, q1 * Z]


def kraus_dephasing_qubit(p: float) -> list[np.ndarray]:
    """Qubit dephasing: ρ → (1-p)·ρ + p·Z·ρ·Z."""
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"p must be in [0, 1], got {p}")
    I = np.eye(2, dtype=np.complex128)
    Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    return [math.sqrt(1.0 - p) * I, math.sqrt(p) * Z]


def kraus_amplitude_damping_qubit(gamma: float) -> list[np.ndarray]:
    """Qubit amplitude damping channel (γ = damping probability)."""
    if not (0.0 <= gamma <= 1.0):
        raise ValueError(f"gamma must be in [0, 1], got {gamma}")
    K0 = np.array([[1, 0], [0, math.sqrt(1 - gamma)]], dtype=np.complex128)
    K1 = np.array([[0, math.sqrt(gamma)], [0, 0]], dtype=np.complex128)
    return [K0, K1]


# ---------------------------------------------------------------------------
# Reference closed forms for validation
# ---------------------------------------------------------------------------

def e_r_depolarizing_analytic(p: float) -> float:
    """E_R(depolarizing channel) for qubit depolarizing with probability p.

    Rains 1999 / Vidal-Werner 2002: for qubit depol p in [0, 4/5]:
        E_R(N_p) = 1 - H_2((1+3p/4)/2) + (arbitrary; tighter by Bose 99)

    For p = 0 (identity): E_R = 1.
    For p → 4/5 (entanglement-breaking): E_R → 0.

    Exact closed form (Vidal-Werner 2002 Eq. (I)):
        E_R(ρ_depol) = 1 - H_2((1-p')/2) + h((1-p')/2, (1+p')/2; 1/2, 1/2)
    where p' = 1 - 4p/3 is "effective transmission" — BUT this is for
    BIPARTITE STATE, not channel.

    Simpler validation: at p=0 (identity), E_R = 1 bit.
    For small p, E_R ≈ 1 - O(p²).
    """
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"p must be in [0, 1], got {p}")
    # For identity channel (p=0): E_R = log(dim) = 1 bit.
    # For depolarizing with effective Fidelity F:
    # F = 1 - 3p/4 + p/4 · 1 = 1 - p/2 (probability |Φ⁺⟩ state passes)
    # E_R(ρ_depol bipartite) = 1 - H_2(F) - (1-F)·log(3) for isotropic states
    # with F > 1/2 (entangled regime).
    # This is specifically Vollbrecht-Werner 2001 / Vidal-Werner 2002.
    F = 1.0 - p / 2.0
    if F <= 0.25:
        return 0.0
    if F >= 1.0:
        return 1.0  # identity → maximally entangled → E_R = 1
    # Isotropic state E_R formula:
    h2 = (
        -F * math.log2(F) - (1.0 - F) * math.log2(1.0 - F)
        if 0.0 < F < 1.0 else 0.0
    )
    return max(0.0, 1.0 - h2 - (1.0 - F) * math.log2(3.0))


# ---------------------------------------------------------------------------
# DV-gap analysis: compare E_R^PPT vs Kamin achievable rate
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Max-Rains information R_max(N) via Wang-Duan 2016b SDP
# ---------------------------------------------------------------------------

def r_max_channel_sdp(
    kraus_ops: list[np.ndarray],
    dim_A: int,
    solver: str = "MOSEK",
    verbose: bool = False,
) -> dict:
    """Max-Rains information R_max(N) of a quantum channel via Wang-Duan SDP.

    Reference:
        - Wang-Duan 2016b, PRA 94:050301 (max-Rains as SDP)
        - Berta-Wilde 2018, Phys. Rev. Lett. 117:200501
        - Khatri-Wilde 2024 §19.2.1 Thm 19.8 (strong converse for PPT-assisted Q)

    R_max provides a STRONG CONVERSE upper bound on the n-shot
    LOCC/PPT-assisted quantum (or private) communication rate:
        log_2 M ≤ n·R_max(N) + log_2(1/(1-ε))

    Wang-Duan 2016b SDP (corrected to match log-negativity / max-Rains
    for Choi state):
        2^{R_max(N)} = min Tr[V]
        s.t. V ≥ +ρ^{T_B},  V ≥ -ρ^{T_B},  V ≥ 0  (operator inequalities)

    For identity qubit channel, eigenvalues of ρ^{T_B} = (1/2)·SWAP are
    {1/2, 1/2, 1/2, -1/2}, so min Tr[V] = Σ|eigenvalue| = 2 → R_max = 1 bit.

    Args:
        kraus_ops: channel Kraus operators.
        dim_A: input dimension.

    Returns:
        dict with:
          R_max_bits: log_2(optimal trace) in bits
          V_opt: optimal V variable
          status: solver status
          rho_choi: Choi state used
    """
    dim_out = kraus_ops[0].shape[0]
    rho_choi = choi_state_from_kraus(kraus_ops, dim_A)
    dim_R = dim_A
    dim_B = dim_out

    # Partial transpose on B
    rho_TB = partial_transpose_B(rho_choi, dim_R, dim_B)

    # SDP: min Tr[V]  s.t.  V ≥ ±ρ^{T_B}, V ≥ 0
    d = dim_R * dim_B
    V = cp.Variable((d, d), hermitian=True)
    constraints = [V >> 0, V >> rho_TB, V >> -rho_TB]
    prob = cp.Problem(cp.Minimize(cp.real(cp.trace(V))), constraints)
    prob.solve(solver=solver, verbose=verbose)
    if prob.status not in {"optimal", "optimal_inaccurate"}:
        raise cp.SolverError(
            f"R_max SDP failed: status={prob.status}, value={prob.value}"
        )

    trace_val = float(prob.value)
    if trace_val <= 0:
        return {
            "R_max_bits": 0.0,
            "V_opt": np.array(V.value, dtype=np.complex128),
            "status": prob.status,
            "rho_choi": rho_choi,
        }
    R_max = math.log2(trace_val)
    return {
        "R_max_bits": max(0.0, R_max),
        "V_opt": np.array(V.value, dtype=np.complex128),
        "status": prob.status,
        "rho_choi": rho_choi,
    }


def dv_gap_from_achievable(
    upper_bound_bits: float, achievable_rate_bits: float,
) -> dict:
    """Simple gap helper: ratio + absolute difference."""
    if achievable_rate_bits < 0:
        raise ValueError(f"achievable rate must be ≥ 0, got {achievable_rate_bits}")
    if upper_bound_bits < 0:
        raise ValueError(f"upper bound must be ≥ 0, got {upper_bound_bits}")
    abs_gap = upper_bound_bits - achievable_rate_bits
    ratio = (
        upper_bound_bits / achievable_rate_bits
        if achievable_rate_bits > 0 else float("inf")
    )
    return {
        "upper_bound_bits": upper_bound_bits,
        "achievable_rate_bits": achievable_rate_bits,
        "abs_gap_bits": abs_gap,
        "ratio": ratio,
    }
