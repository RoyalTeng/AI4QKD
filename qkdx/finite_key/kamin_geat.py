"""Kamin 2025 GEAT finite-key formulas for PM-QKD.

Phase 1 S2.5 Stage 1 (asymptotic anchor):
    Direct implementation of Kamin 2025 Theorem 3 (Eq. 16) for qubit BB84 with
    loss, using analytic rate functions (no SDP required).  This closes the
    "bridge" layer between the GEAT memo and the downstream decoy-state SDP.

References:
    - Kamin et al. 2025.  Finite-size analysis of prepare-and-measure and
      decoy-state QKD via entropy accumulation.  arXiv:2406.10198v3.
    - docs/literature/Kamin-2025.md (Level 3-4 memo)
    - Metger et al. 2024 GEAT (Thm 4.3, Cor 4.6) — parent theorem
    - docs/literature/GEAT-2024.md

Scope note (Stage 1):
    - Theorem 3 key length formula (Eq. 16) — yes
    - Optimal ε allocation (Eq. 57) — yes
    - Qubit BB84 asymptotic rate — yes
    - Choi-state SDP / Frank-Wolfe (Thm 4 dual) — NOT in this module
    - Decoy-state block-diagonal SDP (Thm 6) — NOT in this module
"""
from __future__ import annotations

import math


def _h(p: float) -> float:
    """Binary entropy (bits), 0·log 0 = 0 convention."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


# ---------------------------------------------------------------------------
# Kamin Eq. 57 — optimal ε_PA / ε_EV allocation
# ---------------------------------------------------------------------------

def optimal_eps_parameters(eps_secure: float, alpha: float) -> tuple[float, float]:
    """Kamin 2025 Eq. 57: optimal ε_PA, ε_EV split minimizing f_α.

        ε_PA = α / (2α - 1) · ε_secure
        ε_EV = (α - 1) / (2α - 1) · ε_secure

    Derived from calculus on Eq. 56: f_α(ε_secure, ε_PA) := α/(α-1)·log(1/ε_PA)
    + log(2/(ε_secure − ε_PA)).

    Args:
        eps_secure: total secrecy parameter (0 < ε ≤ 1).
        alpha: Rényi parameter, α ∈ (1, 3/2).

    Returns:
        (eps_PA, eps_EV) with eps_PA + eps_EV = eps_secure.

    Raises:
        ValueError on invalid inputs.
    """
    if not (0.0 < eps_secure <= 1.0):
        raise ValueError(f"eps_secure must be in (0, 1], got {eps_secure}")
    if not (1.0 < alpha < 1.5):
        raise ValueError(f"alpha must be in (1, 3/2), got {alpha}")
    eps_PA = alpha / (2.0 * alpha - 1.0) * eps_secure
    eps_EV = (alpha - 1.0) / (2.0 * alpha - 1.0) * eps_secure
    return eps_PA, eps_EV


# ---------------------------------------------------------------------------
# Kamin Eq. 11 — V² and K(α) second-order coefficients
# ---------------------------------------------------------------------------

def kamin_V_squared(d_A: int, var_f: float, kappa: int = 1) -> float:
    """Kamin Eq. 11: V(p, f) = (log(1 + 2 d_A^κ) + sqrt(2 + Var(p, f)))²

    κ = 1 for classical A_i, κ = 2 for quantum (Kamin §4, Eq. 11).

    Args:
        d_A: max alphabet dimension of A_i.
        var_f: Var_p(f) variance of f against distribution p.
        kappa: 1 (classical) or 2 (quantum).

    Returns:
        V².
    """
    if d_A < 1:
        raise ValueError(f"d_A must be ≥ 1, got {d_A}")
    if var_f < 0.0:
        raise ValueError(f"var_f must be ≥ 0, got {var_f}")
    if kappa not in (1, 2):
        raise ValueError(f"kappa must be 1 or 2, got {kappa}")
    inner = math.log2(1.0 + 2.0 * d_A ** kappa) + math.sqrt(2.0 + var_f)
    return inner * inner


def kamin_K_alpha(
    alpha: float,
    d_A: int,
    max_f: float,
    min_sigma_f: float,
    kappa: int = 1,
) -> float:
    """Kamin Eq. 11: K(α) second-order coefficient.

        K(α) = (2-α)³ / (6(3-2α)³ ln 2)
             · 2^{(α-1)/(2-α) · (κ·log d_A + max(f) − min_Σ(f))}
             · ln³(2^{κ·log d_A + max(f) − min_Σ(f)} + e²)

    Args:
        alpha: Rényi parameter ∈ (1, 3/2).
        d_A: max alphabet dim.
        max_f: max of min-tradeoff function f.
        min_sigma_f: min of f over valid distributions (Min_Σ(f) in Kamin notation).
        kappa: 1 or 2.

    Returns:
        K(α) > 0.
    """
    if not (1.0 < alpha < 1.5):
        raise ValueError(f"alpha must be in (1, 3/2), got {alpha}")
    if d_A < 1:
        raise ValueError(f"d_A must be ≥ 1, got {d_A}")
    if kappa not in (1, 2):
        raise ValueError(f"kappa must be 1 or 2, got {kappa}")

    log_dA = math.log2(d_A)
    span = kappa * log_dA + max_f - min_sigma_f

    prefactor = ((2.0 - alpha) ** 3) / (6.0 * ((3.0 - 2.0 * alpha) ** 3) * math.log(2.0))
    power_term = 2.0 ** ((alpha - 1.0) / (2.0 - alpha) * span)
    log_term = math.log(2.0 ** span + math.e ** 2) ** 3
    return prefactor * power_term * log_term


# ---------------------------------------------------------------------------
# Kamin Eq. 16 — Theorem 3 key length (unique-acceptance simplified form)
# ---------------------------------------------------------------------------

def kamin_theorem3_key_length(
    n: int,
    h: float,
    V_squared: float,
    K_alpha: float,
    alpha: float,
    lambda_EC: float,
    eps_EV: float,
    eps_PA: float,
) -> float:
    """Kamin 2025 Eq. 16, simplified for unique-acceptance (T_α = −((α-1)/(2-α))·(ln 2/2)·V²).

        ℓ ≤ n·h − n·((α-1)/(2-α))·(ln 2/2)·V²
          − n·((α-1)/(2-α))² · K(α)
          − λ_EC − ⌈log(1/ε_EV)⌉ − (α/(α-1))·log(1/ε_PA) + 2

    Valid for Protocol 1 with unique-acceptance (S_acc = {p^hon}) and affine f
    matching rate at p^hon (so Δ_com = 0 and T_α reduces to the variance term).

    Args:
        n: number of signal rounds.
        h: rate at honest distribution (per-round entropy, bits).
        V_squared: V²(p^hon, f) from Eq. 11.
        K_alpha: K(α) from Eq. 11.
        alpha: Rényi parameter ∈ (1, 3/2).
        lambda_EC: error-correction bits communicated (total, not per-round).
        eps_EV: error-verification failure probability ∈ (0, 1].
        eps_PA: privacy-amplification failure probability ∈ (0, 1].

    Returns:
        ℓ in bits (may be negative in infeasible regime).
    """
    if n < 1:
        raise ValueError(f"n must be ≥ 1, got {n}")
    if not (1.0 < alpha < 1.5):
        raise ValueError(f"alpha must be in (1, 3/2), got {alpha}")
    if not (0.0 < eps_EV <= 1.0):
        raise ValueError(f"eps_EV must be in (0, 1], got {eps_EV}")
    if not (0.0 < eps_PA <= 1.0):
        raise ValueError(f"eps_PA must be in (0, 1], got {eps_PA}")
    if V_squared < 0.0 or K_alpha < 0.0:
        raise ValueError(f"V² and K(α) must be ≥ 0")
    if lambda_EC < 0.0:
        raise ValueError(f"lambda_EC must be ≥ 0, got {lambda_EC}")

    beta = (alpha - 1.0) / (2.0 - alpha)
    variance_penalty = n * beta * (math.log(2.0) / 2.0) * V_squared
    K_penalty = n * (beta ** 2) * K_alpha
    log_EV = math.ceil(math.log2(1.0 / eps_EV))
    log_PA = (alpha / (alpha - 1.0)) * math.log2(1.0 / eps_PA)
    ell = n * h - variance_penalty - K_penalty - lambda_EC - log_EV - log_PA + 2.0
    return ell


# ---------------------------------------------------------------------------
# Qubit BB84 with loss (Kamin §6) — analytic asymptotic rate
# ---------------------------------------------------------------------------

def bb84_qubit_asymptotic_rate(
    p_depol: float,
    eta_det: float,
    gamma: float,
    f_EC: float = 1.16,
) -> float:
    """Kamin §6 qubit BB84 asymptotic (n → ∞) rate per transmitted signal.

        rate = (1 − γ)² · η_det · [1 − h(Q) − f_EC · h(Q)]    (Q = p_depol / 2)

    Derivation (Kamin Eq. 59 + §6.3):
        - Generation round chosen with prob (1 − γ)
        - Bob measures in Z-basis with prob (1 − γ)
        - Detection prob in Z (honest, loss-only): η_det
        - Single-photon privacy:  1 − h(Q_X), Q_X = p_depol/2 for depol channel
        - Leak EC per detected round: f_EC · h(Q_Z), Q_Z = p_depol/2

    Args:
        p_depol: depolarization parameter (honest behavior), ∈ [0, 1].
        eta_det: detection efficiency ∈ (0, 1], combined into honest loss.
        gamma: test-round probability ∈ (0, 1).
        f_EC: EC efficiency ≥ 1.

    Returns:
        Per-signal key rate (bits/signal), can be negative above threshold.
    """
    if not (0.0 <= p_depol <= 1.0):
        raise ValueError(f"p_depol must be in [0, 1], got {p_depol}")
    if not (0.0 < eta_det <= 1.0):
        raise ValueError(f"eta_det must be in (0, 1], got {eta_det}")
    if not (0.0 < gamma < 1.0):
        raise ValueError(f"gamma must be in (0, 1), got {gamma}")
    if f_EC < 1.0:
        raise ValueError(f"f_EC must be ≥ 1, got {f_EC}")

    Q = p_depol / 2.0
    hQ = _h(Q)
    return (1.0 - gamma) ** 2 * eta_det * (1.0 - hQ - f_EC * hQ)


# ---------------------------------------------------------------------------
# Qubit BB84 finite-key length via Kamin Theorem 3
# ---------------------------------------------------------------------------

def bb84_qubit_finite_key_length(
    n: int,
    p_depol: float,
    loss_dB: float,
    gamma: float,
    alpha: float,
    eps_secure: float = 1e-8,
    f_EC: float = 1.16,
) -> float:
    """Kamin qubit BB84 finite-key length via Theorem 3 (unique-acceptance).

    Asymptotic rate h = rate_asy(p_depol, eta_det, γ, f_EC).
    λ_EC = n · (1−γ)² · η_det · f_EC · h(Q)  (honest leak).
    V² uses Var(f) = Var(rate) ≤ Max(rate)² ≤ 1 (loose conservative bound).
    ε_PA, ε_EV optimally split per Eq. 57.

    Note (Stage 1 limitation): V² uses a conservative variance upper bound
    (Var(f) = 1) rather than the tight computation from the honest distribution;
    this underestimates the key length at small n.  Full optimization requires
    Theorem 4 SDP (Stage 2).

    Args:
        n: number of signal rounds.
        p_depol: depolarization parameter ∈ [0, 1].
        loss_dB: channel loss in dB, η_det = 10^(−loss_dB/10).
        gamma: test-round probability ∈ (0, 1).
        alpha: Rényi parameter ∈ (1, 3/2).
        eps_secure: total secrecy parameter (default 10^−8, Kamin §6).
        f_EC: EC efficiency (default 1.16, Kamin §4.2 Eq. 26).

    Returns:
        ℓ in bits (can be negative).
    """
    if loss_dB < 0.0:
        raise ValueError(f"loss_dB must be ≥ 0, got {loss_dB}")
    eta_det = 10.0 ** (-loss_dB / 10.0)

    # Honest rate h
    h = bb84_qubit_asymptotic_rate(p_depol, eta_det, gamma, f_EC)

    # Honest EC leakage (per-round): λ_EC / n = (1-γ)² · η_det · f_EC · h(Q)
    Q = p_depol / 2.0
    hQ = _h(Q)
    lambda_EC = n * (1.0 - gamma) ** 2 * eta_det * f_EC * hQ

    # Conservative V²: Var(f) bounded by (Max-Min)² ≤ 1 for rates in [0, 1]
    var_f = 1.0
    V_sq = kamin_V_squared(d_A=2, var_f=var_f, kappa=1)

    # K(α): max(f) = 1, min_Σ(f) = 0 (conservative)
    K_val = kamin_K_alpha(alpha=alpha, d_A=2, max_f=1.0, min_sigma_f=0.0, kappa=1)

    # ε split
    eps_PA, eps_EV = optimal_eps_parameters(eps_secure, alpha)

    return kamin_theorem3_key_length(
        n=n, h=h, V_squared=V_sq, K_alpha=K_val, alpha=alpha,
        lambda_EC=lambda_EC, eps_EV=eps_EV, eps_PA=eps_PA,
    )


def bb84_qubit_optimal_finite_key(
    n: int,
    p_depol: float,
    loss_dB: float,
    eps_secure: float = 1e-8,
    f_EC: float = 1.16,
    gamma_grid: tuple[float, ...] = (
        0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4,
    ),
    alpha_grid: tuple[float, ...] = (
        1.001, 1.005, 1.01, 1.02, 1.05, 1.1, 1.2, 1.3, 1.4,
    ),
) -> tuple[float, float, float]:
    """Grid search over (γ, α) to maximize Kamin qubit BB84 key length.

    Evaluates `bb84_qubit_finite_key_length` on the Cartesian product of
    gamma_grid × alpha_grid and returns the best (ℓ, γ*, α*).

    Args:
        n, p_depol, loss_dB, eps_secure, f_EC: as in bb84_qubit_finite_key_length.
        gamma_grid: γ values to try (default covers 0.5 % – 40 %).
        alpha_grid: α values to try (default covers near-1 to near-3/2).

    Returns:
        (ell_max, gamma_star, alpha_star).  ell_max may be negative if infeasible.
    """
    best = (-math.inf, gamma_grid[0], alpha_grid[0])
    for gamma in gamma_grid:
        for alpha in alpha_grid:
            ell = bb84_qubit_finite_key_length(
                n=n, p_depol=p_depol, loss_dB=loss_dB,
                gamma=gamma, alpha=alpha,
                eps_secure=eps_secure, f_EC=f_EC,
            )
            if ell > best[0]:
                best = (ell, gamma, alpha)
    return best
