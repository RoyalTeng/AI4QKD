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
    """E_R(ρ_choi) for qubit depolarizing isotropic Choi state.

    Reference: Vollbrecht-Werner 2001; Plenio-Virmani 2007 §V.E Eq. (V.86).
    For d⊗d isotropic with fidelity F > 1/d:
        E_R = log₂ d + F·log₂ F + (1 − F)·log₂((1 − F)/(d − 1))

    For qubit (d = 2): (d − 1) = 1, so log₂(d − 1) = 0, giving:
        E_R(ρ_iso(F)) = 1 − h₂(F)    for F > 1/2
        E_R(ρ_iso(F)) = 0             for F ≤ 1/2 (separable / Werner threshold)

    Qubit depolarizing channel N_p: ρ → (1 − p)·ρ + p·I/2.
    Choi state ρ_choi = (I ⊗ N_p)(|Φ⁺⟩⟨Φ⁺|) is isotropic with
        F(p) = ⟨Φ⁺|ρ_choi|Φ⁺⟩ = (1 − p) + p/4 = 1 − 3p/4

    For 2 ⊗ 2: PPT = SEP (Horodecki et al. 1996), so this also equals E_R^PPT.

    Reference values:
        p = 0 → F = 1: E_R = 1 bit (maximally entangled identity channel)
        p = 2/3 → F = 1/2: E_R = 0 (Werner separability boundary)
        p = 1 → F = 1/4: E_R = 0

    HISTORY (2026-04-23 bug-catch): previous version of this function
    incorrectly subtracted an extra (1 − F)·log₂(3) term (mistakenly using
    d² − 1 = 3 instead of d − 1 = 1 in the Vollbrecht-Werner formula).
    The bug caused early zero-crossing at p ≈ 0.27 instead of correct p = 2/3,
    underestimating E_R by 0.03 to 0.40 bits across the entangled regime.
    Detected by MOSEK E_R^PPT SDP cross-validation; fixed in this commit.
    See `docs/findings/qubit_E_R_PPT_hierarchy_2026-04-23.md`.
    """
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"p must be in [0, 1], got {p}")
    F = 1.0 - 3.0 * p / 4.0
    if F <= 0.5:
        return 0.0  # isotropic state is separable for F ≤ 1/2 (qubit case)
    if F >= 1.0:
        return 1.0  # identity channel
    h2_F = -F * math.log2(F) - (1.0 - F) * math.log2(1.0 - F)
    return max(0.0, 1.0 - h2_F)


# ---------------------------------------------------------------------------
# Analytic log-negativity for qubit channel Choi states
# ---------------------------------------------------------------------------
# SymPy-verified (2026-04-23): docs/workflow/beta-G3-analytic-proof-review/sympy-c1c-verification.md
# Memo: docs/findings/beta_G3_golden_ratio_crossover_2026-04-23.md §2 (AD)
# These are [SYN] — standard textbook-level calculations; R0.2 triple verification
# applies for any label upgrade.

def K_D_amplitude_damping_degradable(gamma: float) -> float:
    """K_D = Q (quantum capacity) of qubit amplitude damping for γ ≤ 1/2.

    AD channel is **degradable** for γ ≤ 1/2 (Caruso-Giovannetti-Holevo 2014;
    standard textbook result, e.g., Khatri-Wilde 2020 §17.4). For degradable
    channels: K_D = P = Q = single-letter regularized coherent information.

        Q(N_AD, γ) = max_{p ∈ [0,1]} [h₂((1-γ)·p) − h₂(γ·p)]   for γ ≤ 1/2
                   = 0                                            for γ > 1/2

    For γ > 1/2: AD is anti-degradable, Q = 0. K_D could still be > 0 via
    two-way LOCC, but no closed form is known.

    Returns:
        Quantum capacity in bits/use. Only equals K_D in degradable regime.

    Reference values:
        γ = 0:    Q = 1 bit (identity)
        γ = 0.5:  Q = 0 (degradability boundary)
        γ → 1:    Q = 0 (no information transmission)
    """
    if not (0.0 <= gamma <= 1.0):
        raise ValueError(f"gamma must be in [0, 1], got {gamma}")
    if gamma >= 0.5:
        return 0.0

    def h2(x: float) -> float:
        if x <= 1e-15 or x >= 1.0 - 1e-15:
            return 0.0
        return -x * math.log2(x) - (1.0 - x) * math.log2(1.0 - x)

    # Maximize over p ∈ [0, 1] via golden-section search (no scipy dep here).
    # Coherent info I_c(p) = h₂((1-γ)·p) − h₂(γ·p) is concave in p for γ < 1/2.
    phi = (1 + math.sqrt(5)) / 2
    a, b = 0.0, 1.0
    for _ in range(80):
        d = (b - a) / phi
        x1 = b - d
        x2 = a + d
        f1 = h2((1 - gamma) * x1) - h2(gamma * x1)
        f2 = h2((1 - gamma) * x2) - h2(gamma * x2)
        if f1 > f2:
            b = x2
        else:
            a = x1
    p_opt = (a + b) / 2
    return max(0.0, h2((1 - gamma) * p_opt) - h2(gamma * p_opt))


def analytic_log_neg_amplitude_damping(gamma: float) -> float:
    """log-negativity of Choi state of qubit amplitude damping channel (γ = damping prob).

    Kraus: K₀=[[1,0],[0,√(1-γ)]], K₁=[[0,√γ],[0,0]].
    Choi PT eigenvalue set: {1/2, (1-γ)/2, ±(√(1-γ))/... } — full derivation
    in β.G3 memo §2 uses transmission parameter η=1-γ, giving:
        ||ρ^T_B||₁ = 1 + η = 2 - γ
        log_neg(γ) = log₂(2 - γ)

    Boundary: γ=0 (identity) → log_neg=1 bit; γ=1 (fully damping) → log_neg=0.
    """
    if not (0.0 <= gamma <= 1.0):
        raise ValueError(f"gamma must be in [0, 1], got {gamma}")
    return math.log2(2.0 - gamma)


def analytic_log_neg_dephasing(p: float) -> float:
    """log-negativity of Choi state of qubit dephasing channel.

    Channel: E(ρ) = (1-p)ρ + p·Z·ρ·Z.
    Choi = (1-p)|Φ⁺⟩⟨Φ⁺| + p|Φ⁻⟩⟨Φ⁻|.
    PT eigenvalues: {1/2, 1/2, 1/2 - p, p - 1/2}; trace norm = 1 + |1 - 2p|.

        log_neg(p) = log₂(1 + |1 - 2p|)

    Boundary: p=0 → log_neg=1 bit (identity); p=1/2 → log_neg=0 (full dephase);
    p=1 → log_neg=1 bit (pure Z flip, still correlated).
    Symmetric: log_neg(p) = log_neg(1-p).
    """
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"p must be in [0, 1], got {p}")
    return math.log2(1.0 + abs(1.0 - 2.0 * p))


def analytic_log_neg_erasure(p: float) -> float:
    """log-negativity of Choi state of qubit erasure channel.

    Channel: |i⟩ → √(1-p)|i⟩ + √p|e⟩ (|e⟩ ⊥ qubit space, dim_B = 3).
    Choi = (1-p)·|Φ⁺⟩⟨Φ⁺| (in 2⊗2 sub-block, padded by zeros)
         + p·(I_A/2) ⊗ |e⟩⟨e|
    PT eigenvalues: {(1-p)/2 × 3, -(1-p)/2 × 1, p/2 × 2}
    Trace norm = 2 - p.

        log_neg(p) = log₂(2 - p)

    Boundary: p=0 → log_neg=1 bit (identity); p=1 → log_neg=0 (full erasure).
    Note: K_D(erasure, p) = 1 - p (PLOB Eq.43, exact).
    """
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"p must be in [0, 1], got {p}")
    return math.log2(2.0 - p)


def analytic_log_neg_depolarizing(p: float) -> float:
    """log-negativity of Choi state of qubit depolarizing channel.

    Channel: E(ρ) = (1-p)ρ + p·I/2. Choi is isotropic with Bell fidelity
    F(p) = 1 − 3p/4. PT eigenvalues: (1/2 − p/4) with multiplicity 3, and
    (3p/4 − 1/2) with multiplicity 1.

    For p ∈ [0, 2/3] (entangled regime, F > 1/2):
        trace norm = 2 − 3p/2 = 2F
        log_neg = log₂(2 − 3p/2) = 1 + log₂(F)

    For p ∈ [2/3, 1] (PPT/separable regime): log_neg = 0.
    """
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"p must be in [0, 1], got {p}")
    F = 1.0 - 3.0 * p / 4.0
    if F <= 0.5:
        return 0.0
    return math.log2(2.0 * F)


# ---------------------------------------------------------------------------
# DV-gap analysis: compare E_R^PPT vs Kamin achievable rate
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Max-Rains information R_max(N) via Wang-Duan 2016b SDP
# ---------------------------------------------------------------------------

def log_negativity_channel_sdp(
    kraus_ops: list[np.ndarray],
    dim_A: int,
    solver: str = "MOSEK",
    verbose: bool = False,
) -> dict:
    """Log-negativity of the Choi state via SDP (upper bound on max-Rains).

    References:
        - Vidal-Werner 2002, PRA 65:032314 (logarithmic negativity)
        - Wang-Duan 2016b, PRA 94:050301 (full two-cone max-Rains SDP)
        - Berta-Wilde 2018, PRL 117:200501
        - Khatri-Wilde 2024 §19.2.1 Thm 19.8

    **Scope clarification** (per audit 2026-04-21):
        This function computes the LOGARITHMIC NEGATIVITY of the channel's
        Choi state, NOT the strict Wang-Duan 2016b two-cone max-Rains SDP:
            E_N(N) = log_2 ‖ρ_N^{T_B}‖_1
        Wang-Duan 2016b Eq. (9) defines R_max(N) via a two-operator form
        Γ(N) = min{‖Tr_B[V+W]‖_∞ : V, W ≥ 0, (V−W)^{T_B} = ρ^N}.
        For 2-qubit Choi states, E_N and R_max COINCIDE on identity,
        fully-depolarizing, and Bell states; for general channels
        E_N ≥ R_max (log-negativity is a LOOSER upper bound).

    Thm 19.8 strong-converse rate uses R_max; using E_N as a substitute
    still gives a VALID strong-converse upper bound (since E_N ≥ R_max),
    just not the tightest possible.

    SDP form used here:
        E_N(ρ) = log_2 min Tr[V]
        s.t. V ≥ +ρ^{T_B},  V ≥ −ρ^{T_B},  V Hermitian
        (V ≥ 0 implied by V ≥ ρ^{T_B} + V ≥ −ρ^{T_B} when trace minimized)

    Validation:
        Identity qubit: eigenvalues of |Φ⁺⟩⟨Φ⁺|^{T_B} = {1/2, 1/2, 1/2, −1/2}
        min Tr[V] = Σ|λ| = 2, E_N = log_2(2) = 1 bit ✓

    Args:
        kraus_ops: channel Kraus operators.
        dim_A: input dimension.

    Returns:
        dict with:
          log_negativity_bits: E_N = log_2(Tr[V]) in bits (upper bounds R_max)
          R_max_bits: alias for log_negativity_bits (backward compat)
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
            "log_negativity_bits": 0.0,
            "R_max_bits": 0.0,  # alias for backward compat
            "V_opt": np.array(V.value, dtype=np.complex128),
            "status": prob.status,
            "rho_choi": rho_choi,
        }
    E_N = max(0.0, math.log2(trace_val))
    return {
        "log_negativity_bits": E_N,
        "R_max_bits": E_N,  # alias (log-neg upper-bounds strict R_max)
        "V_opt": np.array(V.value, dtype=np.complex128),
        "status": prob.status,
        "rho_choi": rho_choi,
    }


# Backward-compat alias: previous API name
r_max_channel_sdp = log_negativity_channel_sdp


def max_rains_wang_duan_channel_sdp(
    kraus_ops: list[np.ndarray],
    dim_A: int,
    solver: str = "MOSEK",
    verbose: bool = False,
) -> dict:
    """Max-Rains info R_max(N) via Wang-Duan 2016b 2-cone SDP — STUB.

    **Status: NotImplementedError [UNVERIFIED Wang-Duan form]**

    AI autonomous 2026-04-23 attempted 2 variants of Wang-Duan 2-cone SDP:
        Variant 1: min ||Tr_B[V+W]||_∞  s.t. V,W ≥ 0, (V−W)^{T_B} = ρ^N
        Variant 2: min ||V+W||_∞       s.t. V,W ≥ 0, (V−W)^{T_B} = ρ^N

    Both variants **failed validation** on simple cases:
        - Identity qubit: should give R_max ≥ 1 (Bell Choi), got 0 or −1
        - Full depolarizing: should give R_max = 0, got 0 or −2
        - Amp-damp 0.9: should satisfy R_max ≤ log-neg, gave structurally
          inconsistent sign

    **Root cause**: exact Wang-Duan 2016b Eq. (9) form cannot be reliably
    reconstructed from local memo docstring alone. User must consult
    Wang-Duan 2016b (PRA 94:050301) or Khatri-Wilde 2020 §19.2.1 Thm 19.8 PDF
    to verify:
        - Correct norm type (||·||_∞ operator infinity vs ||·||_1 trace norm)
        - Whether Tr_B or no partial trace
        - Constraint sign convention

    Until user-verified, use `log_negativity_channel_sdp` which is a valid
    (looser) upper bound on max-Rains for strong-converse purposes.

    [TODO for user]: After Wang-Duan PDF verify, rewrite this function with
    correct SDP form and validate against:
        - Identity qubit → R_max = 1 bit
        - Bell-preparing channel → R_max = log_2(dim)
        - Fully depolarizing → R_max = 0
        - Should satisfy R_max ≤ log-neg universally
    """
    raise NotImplementedError(
        "Wang-Duan max-Rains SDP AI draft failed validation (2026-04-23). "
        "User must verify Wang-Duan 2016b Eq. (9) exact form from PDF "
        "before implementing. Use log_negativity_channel_sdp as valid "
        "(looser) upper bound in the meantime."
    )


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
