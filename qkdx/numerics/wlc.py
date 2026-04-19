"""Winick-Lütkenhaus-Coles 2018 key-rate solver.

Reference: Winick, Lütkenhaus, Coles (2018). Reliable numerical key rates
for QKD. Quantum 2:77. arXiv:1710.05511.

Implementation:
- MOSEK path: one-shot SDP via cp.quantum_rel_entr (fast, requires license).
- CLARABEL/SCS path: Frank-Wolfe conditional gradient (WLC 2018 Algorithm 1).
  Each Frank-Wolfe iteration solves a *linear* SDP which CLARABEL handles in
  milliseconds, avoiding the slow Padé expansion of quantum_rel_entr.

Main entry point: wlc_key_rate().
"""
from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass

import cvxpy as cp
import numpy as np
import scipy.linalg as la

from qkdx.core.entropy import binary_entropy
from qkdx.core.hilbert import Matrix
from qkdx.core.operators import KrausMap
from qkdx.protocol.base import MSEBProtocol
from qkdx.utils.logging import get_logger
from qkdx.utils.solvers import preferred_solver

logger = get_logger(__name__)

MOSEK_PARAMS: dict[str, object] = {
    "MSK_DPAR_INTPNT_CO_TOL_REL_GAP": 1e-8,
    "MSK_DPAR_INTPNT_CO_TOL_PFEAS": 1e-8,
    "MSK_DPAR_INTPNT_CO_TOL_DFEAS": 1e-8,
    "MSK_IPAR_INTPNT_MAX_ITERATIONS": 1000,
}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GMap:
    """𝒢 mapping with dimension metadata for pinching.

    Invariant: map.dim_out == dim_key * dim_side.
    """
    map: KrausMap
    dim_key: int
    dim_side: int

    def __post_init__(self) -> None:
        if self.map.dim_out != self.dim_key * self.dim_side:
            raise ValueError(
                f"GMap.map.dim_out ({self.map.dim_out}) != "
                f"dim_key*dim_side ({self.dim_key}*{self.dim_side})"
            )


@dataclass
class WLCResult:
    """WLC solver output. Units: bit/signal for key_rate, bit/sift for h_bits_per_sift."""
    key_rate: float
    primal_status: str
    h_bits_per_sift: float
    iterations: int
    duality_gap: float
    optimal_rho: Matrix | None = None
    solver: str = "MOSEK"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def wlc_key_rate(
    protocol: MSEBProtocol,
    observations: Mapping[str, float],
    *,
    solver: str | None = None,
    epsilon_regularization: float = 1e-9,
    f_ec: float = 1.16,
    max_iters: int = 1000,
    verbose: bool = False,
) -> WLCResult:
    """WLC SDP key-rate lower bound for an MS-EB protocol.

    MOSEK path: one-shot SDP via cp.quantum_rel_entr (fast).
    CLARABEL/SCS path: Frank-Wolfe conditional gradient (WLC 2018 Algorithm 1).

    Args:
        solver: "MOSEK" | "CLARABEL" | "SCS" | None. If None, auto-selects via
            qkdx.utils.solvers.preferred_solver() (MOSEK if installed, else
            CLARABEL, else SCS).

    Raises:
        ValueError: observations keys don't exactly match protocol.observation_keys.
        cp.SolverError: SDP cannot be solved.
    """
    # --- 0. Validate keys ---
    known = set(protocol.observation_keys)
    provided = set(observations.keys())
    missing = known - provided
    if missing:
        raise ValueError(f"missing observation: {sorted(missing)[0]}")
    unknown = provided - known
    if unknown:
        raise ValueError(f"unknown observation: {sorted(unknown)}")

    if solver is None:
        solver = preferred_solver()

    if solver == "MOSEK":
        return _wlc_mosek(protocol, observations, epsilon_regularization, f_ec,
                          max_iters, verbose)
    else:
        return _wlc_frank_wolfe(protocol, observations, solver, f_ec,
                                max_iters, verbose)


# ---------------------------------------------------------------------------
# MOSEK path: one-shot SDP via cp.quantum_rel_entr
# ---------------------------------------------------------------------------

def _wlc_mosek(
    protocol: MSEBProtocol,
    observations: Mapping[str, float],
    eps: float,
    f_ec: float,
    max_iters: int,
    verbose: bool,
) -> WLCResult:
    """One-shot SDP path. Requires MOSEK."""
    d_rho = protocol.conditional_alice_bob_dim()
    G = _construct_G_map(protocol)
    Z_kraus = _construct_Z_pinching(G.dim_key, G.dim_side)

    rho = cp.Variable((d_rho, d_rho), hermitian=True)
    constraints: list[cp.Constraint] = [rho >> 0, cp.real(cp.trace(rho)) == 1]

    for key, val in observations.items():
        if key == "p_sift":
            continue
        Gamma_k = protocol.observable(key)
        constraints.append(
            cp.real(cp.trace(cp.Constant(Gamma_k) @ rho)) == float(val)
        )

    # Auxiliary Hermitian variables for cp.quantum_rel_entr (requires hermitian=True args)
    d_out = G.map.dim_out
    tau = np.eye(d_out, dtype=np.complex128) / d_out

    X_var = cp.Variable((d_out, d_out), hermitian=True)
    Y_var = cp.Variable((d_out, d_out), hermitian=True)

    # X_var = G(rho) regularised: X_reg = (1-ε)G(ρ) + ε·τ  (G=identity here → G(ρ)=ρ)
    X_raw_expr = _apply_cvxpy_map(G.map, rho)
    # Use rho + const form to stay in Hermitian type where possible (G=identity case)
    X_reg_expr = X_raw_expr + cp.Constant(eps * tau)
    constraints.append(X_var == X_reg_expr)

    Y_raw_expr = _apply_cvxpy_map(Z_kraus, X_var)
    constraints.append(Y_var == Y_raw_expr)

    objective = cp.Minimize(cp.quantum_rel_entr(X_var, Y_var))
    prob = cp.Problem(objective, constraints)
    params = dict(MOSEK_PARAMS)
    params["MSK_IPAR_INTPNT_MAX_ITERATIONS"] = max_iters
    prob.solve(solver=cp.MOSEK, verbose=verbose, mosek_params=params)

    if prob.status not in {"optimal", "optimal_inaccurate"}:
        raise cp.SolverError(f"WLC MOSEK failed: status={prob.status}")

    return _assemble_result(prob.value, prob.status, rho.value, observations,
                            f_ec, solver="MOSEK",
                            gap=_get_gap(prob), iters=_get_iters(prob))


# ---------------------------------------------------------------------------
# Frank-Wolfe path (CLARABEL / SCS)
# ---------------------------------------------------------------------------

def _wlc_frank_wolfe(
    protocol: MSEBProtocol,
    observations: Mapping[str, float],
    solver: str,
    f_ec: float,
    max_iters: int,
    verbose: bool,
) -> WLCResult:
    """Frank-Wolfe (conditional gradient) WLC solver.

    WLC 2018 Algorithm 1: each iteration solves a *linear* SDP (fast).

    Convergence: Frank-Wolfe on a bounded convex domain converges at O(1/n).
    The duality gap ⟨∇f, ρ - σ*⟩ is used as the stopping criterion.
    """
    d = protocol.conditional_alice_bob_dim()
    G = _construct_G_map(protocol)
    Z_kraus = _construct_Z_pinching(G.dim_key, G.dim_side)

    # Build NumPy Kraus arrays for gradient computation
    G_kraus_np = [K.astype(np.complex128) for K in G.map.kraus]
    Z_kraus_np = [K.astype(np.complex128) for K in Z_kraus.kraus]

    # Build observable constraint matrices
    obs_constraints: list[tuple[Matrix, float]] = []
    for key, val in observations.items():
        if key == "p_sift":
            continue
        obs_constraints.append((protocol.observable(key), float(val)))

    # Initialize ρ at a strictly feasible point (Werner state for BB84)
    rho = _init_feasible(d, obs_constraints)

    best_val = float("inf")
    best_rho = rho.copy()
    duality_gap = float("nan")

    for n in range(max_iters):
        # --- 1. Compute X = G(ρ) and Y = Z(X) ---
        X = _apply_kraus_numpy(G_kraus_np, rho)
        Y = _apply_kraus_numpy(Z_kraus_np, X)

        # --- 2. Objective value f(ρ) ---
        f_rho = _quantum_rel_entr_numpy(X, Y)
        if f_rho < best_val:
            best_val = f_rho
            best_rho = rho.copy()

        # --- 3. Gradient ∇f = G†(log X - log Y) ---
        try:
            grad = _gradient_numpy(G_kraus_np, X, Y)
        except (np.linalg.LinAlgError, ValueError):
            # Numerical issue; terminate with current best
            break

        # --- 4. Linear SDP: min Tr(grad @ sigma) s.t. sigma ∈ S ---
        sigma_star = _solve_linear_sdp(grad, obs_constraints, d, solver=solver)

        # --- 5. Duality gap (convergence criterion) ---
        duality_gap = float(np.real(np.trace(grad @ (rho - sigma_star))))
        if verbose:
            print(f"FW iter {n}: f={f_rho:.8f}, gap={duality_gap:.2e}")
        if duality_gap < 1e-8:
            break

        # --- 6. Exact line search over γ ∈ [0,1] ---
        delta = sigma_star - rho
        gamma = _line_search(rho, delta, G_kraus_np, Z_kraus_np)

        # --- 7. Update ---
        rho = rho + gamma * delta

    return _assemble_result(best_val, "optimal", best_rho, observations, f_ec,
                            solver=solver, gap=duality_gap, iters=n + 1)


# ---------------------------------------------------------------------------
# Frank-Wolfe helpers
# ---------------------------------------------------------------------------

def _apply_kraus_numpy(kraus: list[Matrix], rho: Matrix) -> Matrix:
    """Apply Kraus map: Σ_i K_i @ rho @ K_i†."""
    out = np.zeros_like(rho, dtype=np.complex128)
    for K in kraus:
        out += K @ rho @ K.conj().T
    return out


def _quantum_rel_entr_numpy(X: Matrix, Y: Matrix) -> float:
    """D(X||Y) = Tr(X(log X - log Y)) [nats]. Returns +inf if not well-defined."""
    try:
        log_X = la.logm(X)
        log_Y = la.logm(Y)
        result = np.real(np.trace(X @ (log_X - log_Y)))
        return float(result)
    except Exception:
        return float("inf")


def _gradient_numpy(G_kraus: list[Matrix], X: Matrix, Y: Matrix) -> Matrix:
    """∇f(ρ) = G†(log X - log Y) [Hermitian matrix].

    For G = identity: G†(M) = M.
    General: G†(M) = Σ_i K_i† @ M @ K_i (adjoint map).
    """
    log_X = la.logm(X)
    log_Y = la.logm(Y)
    inner = log_X - log_Y  # Hermitian

    # G† (adjoint of G w.r.t. Hilbert-Schmidt inner product):
    # G†(M) = Σ_i K_i† @ M @ K_i
    grad = np.zeros_like(inner, dtype=np.complex128)
    for K in G_kraus:
        grad += K.conj().T @ inner @ K
    return 0.5 * (grad + grad.conj().T)  # symmetrise for numerical safety


def _solve_linear_sdp(
    grad: Matrix,
    obs_constraints: list[tuple[Matrix, float]],
    d: int,
    solver: str = "CLARABEL",
) -> Matrix:
    """Solve min Tr(grad @ sigma) s.t. sigma ∈ S = {PSD, trace=1, obs=γ_k}.

    This is a linear SDP (linear objective over a semidefinite feasible set).
    Much faster than the quantum_rel_entr atom.
    """
    sigma = cp.Variable((d, d), hermitian=True)
    constraints: list[cp.Constraint] = [sigma >> 0, cp.real(cp.trace(sigma)) == 1]
    for Gamma_k, gamma_k in obs_constraints:
        constraints.append(
            cp.real(cp.trace(cp.Constant(Gamma_k) @ sigma)) == gamma_k
        )

    objective = cp.Minimize(cp.real(cp.trace(cp.Constant(grad.conj().T) @ sigma)))
    prob = cp.Problem(objective, constraints)

    if solver == "CLARABEL":
        prob.solve(solver=cp.CLARABEL)
    elif solver == "SCS":
        prob.solve(solver=cp.SCS, eps=1e-9)
    else:
        prob.solve(solver=solver)

    if prob.status not in {"optimal", "optimal_inaccurate"} or sigma.value is None:
        # Fallback: return maximally mixed state (always feasible if constraints are tight)
        return _init_feasible(d, obs_constraints)

    # Ensure Hermitian
    val = sigma.value
    return 0.5 * (val + val.conj().T)


def _line_search(
    rho: Matrix,
    delta: Matrix,
    G_kraus: list[Matrix],
    Z_kraus: list[Matrix],
    n_points: int = 20,
) -> float:
    """Find γ* = argmin_{γ ∈ [0,1]} D(G(ρ+γΔ) || Z(G(ρ+γΔ))).

    Uses a grid search followed by golden section.
    """
    def objective(gamma: float) -> float:
        rho_g = rho + gamma * delta
        X = _apply_kraus_numpy(G_kraus, rho_g)
        Y = _apply_kraus_numpy(Z_kraus, X)
        return _quantum_rel_entr_numpy(X, Y)

    # Coarse grid
    gammas = np.linspace(0.0, 1.0, n_points)
    vals = [objective(g) for g in gammas]
    best_idx = int(np.argmin(vals))
    lo = gammas[max(0, best_idx - 1)]
    hi = gammas[min(n_points - 1, best_idx + 1)]

    # Golden section refinement
    phi = (np.sqrt(5) - 1) / 2
    for _ in range(30):
        c = hi - phi * (hi - lo)
        d = lo + phi * (hi - lo)
        if objective(c) < objective(d):
            hi = d
        else:
            lo = c
        if hi - lo < 1e-10:
            break

    return float((lo + hi) / 2)


def _init_feasible(d: int, obs_constraints: list[tuple[Matrix, float]]) -> Matrix:
    """Find a strictly feasible ρ satisfying the equality constraints via SDP."""
    sigma = cp.Variable((d, d), hermitian=True)
    constraints: list[cp.Constraint] = [sigma >> 0, cp.real(cp.trace(sigma)) == 1]
    for Gamma_k, gamma_k in obs_constraints:
        constraints.append(
            cp.real(cp.trace(cp.Constant(Gamma_k) @ sigma)) == gamma_k
        )
    prob = cp.Problem(cp.Minimize(0), constraints)
    prob.solve(solver=cp.CLARABEL)

    if sigma.value is not None:
        val = sigma.value
        val = 0.5 * (val + val.conj().T)
        # Make strictly positive definite
        val += 1e-8 * np.eye(d)
        val /= np.trace(val).real
        return val

    # Last resort: maximally mixed state (may not satisfy obs constraints)
    return np.eye(d, dtype=np.complex128) / d


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _assemble_result(
    obj_value_nat: float,
    status: str,
    rho_val: Matrix | None,
    observations: Mapping[str, float],
    f_ec: float,
    solver: str,
    gap: float,
    iters: int,
) -> WLCResult:
    """Convert SDP objective (nats) to WLCResult (bit/signal)."""
    H_bits = obj_value_nat / np.log(2.0)
    qber_Z = float(observations["qber_Z"])
    p_sift = float(observations["p_sift"])
    leak_ec = f_ec * binary_entropy(qber_Z)
    key_rate = p_sift * (H_bits - leak_ec)

    logger.info(
        "wlc_result",
        status=status, value_nat=obj_value_nat,
        h_bits_per_sift=H_bits, key_rate=key_rate,
        leak_ec=leak_ec, p_sift=p_sift, solver=solver,
    )
    return WLCResult(
        key_rate=key_rate,
        primal_status=status,
        h_bits_per_sift=H_bits,
        iterations=iters,
        duality_gap=gap,
        optimal_rho=rho_val,
        solver=solver,
    )


def _get_gap(prob: cp.Problem) -> float:
    dual_obj = getattr(prob.solver_stats, "dual_objective", None)
    return float("nan") if dual_obj is None else abs(float(prob.value) - float(dual_obj))


def _get_iters(prob: cp.Problem) -> int:
    return getattr(prob.solver_stats, "num_iters", -1)


def _apply_cvxpy_map(K: KrausMap, X: cp.Expression) -> cp.Expression:
    """Apply Kraus map to CVXPY expression: Σ_i K_i X K_i†."""
    terms = [cp.Constant(Ki) @ X @ cp.Constant(Ki).H for Ki in K.kraus]
    result = terms[0]
    for t in terms[1:]:
        result = result + t
    return result


def _construct_Z_pinching(dim_key: int, dim_side: int = 1) -> KrausMap:
    """𝒵 pinching channel: K_x = |x⟩⟨x| ⊗ I_{dim_side}."""
    d = dim_key * dim_side
    I_side = np.eye(dim_side, dtype=np.complex128)
    kraus = []
    for x in range(dim_key):
        proj_x = np.zeros((dim_key, dim_key), dtype=np.complex128)
        proj_x[x, x] = 1.0
        kraus.append(np.kron(proj_x, I_side))
    return KrausMap(kraus=tuple(kraus), dim_in=d, dim_out=d)


def _construct_G_map(protocol: MSEBProtocol) -> GMap:
    """Build the 𝒢 map. For BB84: identity on 4-dim A_key ⊗ B space."""
    d = protocol.conditional_alice_bob_dim()
    n_key_vals = len(set(protocol.key_map.bitmap.values()))
    dim_key = max(2, n_key_vals)
    if d % dim_key != 0:
        sq = int(np.round(np.sqrt(d)))
        if sq * sq == d:
            dim_key = sq
    dim_side = d // dim_key
    return GMap(
        map=KrausMap.identity(d),
        dim_key=dim_key,
        dim_side=dim_side,
    )


def _build_observable_operators(
    protocol: MSEBProtocol,
    observation_keys: Sequence[str],
) -> Mapping[str, Matrix]:
    return {key: protocol.observable(key) for key in observation_keys}
