"""Kamin 2025 finite-key for MDI-QKD (D.4 migration).

Scope:
    Ideal symmetric MDI-QKD with WLC-level Kamin Choi-state SDP:
    - Two-source (Alice + Bob) protocol
    - Charlie's Bell measurement absorbed into the conditional state
      (virtual-EB picture, per qkdx/protocols/mdi.py)
    - Effective Alice-Bob state is Werner-like with effective QBER
    - p_sift = 1/4 (basis match 1/2 × Charlie success 1/2)

Per-round sift probability for ideal symmetric MDI at η_A = η_B = η_arm:
    p_sift_effective = (1-γ)² · p_sift_base · η_A · η_B
                     = (1-γ)² · (1/4) · η_arm²
                     = (1-γ)² · η_A_effective  (where η_A_effective = η_arm²/4)

Reference:
    - Lo-Curty-Qi 2012, PRL 108:130503
    - Ma-Razavi 2012, PRA 86:062319
    - Kamin 2025 §5-6 (qubit BB84 SDP, this module reuses)
    - qkdx/protocols/mdi.py (existing MDI MS-EB shell)
    - qkdx/numerics/kamin_sdp.py (Kamin Choi SDP, reused)

Reduction to qubit BB84 Kamin SDP:
    In the virtual-EB picture (Lo-Curty-Qi §II), after Charlie's successful
    Bell projection the conditional Alice-Bob state has the Werner form
    Tr[|Φ⁺⟩⟨Φ⁺|·ρ_AB] = 1 - 3·qber/2 (for the basis-matched-correct BSM).
    This is structurally identical to qubit BB84's Werner state at effective
    QBER, allowing DIRECT reuse of `kamin_choi_sdp_qubit_bb84`.

Divergence from real MDI:
    This implementation assumes the ideal virtual-EB reduction; full-rigor
    MDI finite-key would treat Charlie's Bell POVM explicitly, with a 2-source
    Kamin SDP on the combined A'⊗B' space (scope_tag="partial", future work).
"""
from __future__ import annotations

import math
import os
from typing import Any

import cvxpy as cp
import numpy as np

from qkdx.numerics.kamin_sdp import (
    kamin_choi_sdp_qubit_bb84,
    kamin_choi_sdp_qubit_bb84_with_dual,
    _kamin_V2_bb84_tight,
    _kamin_ell_from_sdp_result,
)

_DEFAULT_MOSEK_LIC = os.path.expanduser("~/mosek/mosek.lic")
if os.path.exists(_DEFAULT_MOSEK_LIC) and "MOSEKLM_LICENSE_FILE" not in os.environ:
    os.environ["MOSEKLM_LICENSE_FILE"] = _DEFAULT_MOSEK_LIC


def kamin_mdi_h_per_sift(
    qber: float,
    gamma: float = 0.01,
    solver: str = "MOSEK",
    epsilon_regularization: float = 1e-9,
    verbose: bool = False,
) -> dict[str, Any]:
    """Kamin Choi SDP h_per_sift for ideal symmetric MDI-QKD.

    By the virtual-EB reduction (Lo-Curty-Qi 2012), the conditional
    Alice-Bob state after Charlie's successful Bell measurement is
    structurally identical to qubit BB84 Werner state at the effective
    MDI QBER.  Therefore we DELEGATE to the existing qubit BB84 Kamin SDP.

    Args:
        qber: symmetric Alice-Bob effective QBER.
        gamma, solver, epsilon_regularization, verbose: as for
            kamin_choi_sdp_qubit_bb84.

    Returns:
        dict as returned by kamin_choi_sdp_qubit_bb84_with_dual,
        plus "protocol" = "mdi" tag.
    """
    r = kamin_choi_sdp_qubit_bb84_with_dual(
        qber=qber, gamma=gamma, solver=solver,
        epsilon_regularization=epsilon_regularization, verbose=verbose,
    )
    r["protocol"] = "mdi"
    r["p_sift_base"] = 0.25  # MDI p_sift = 1/4 (BB84 p_sift = 1/2)
    return r


def kamin_mdi_key_length(
    qber: float,
    n: int,
    loss_dB_total: float,
    gamma: float,
    alpha: float,
    eps_secure: float = 1e-8,
    f_EC: float = 1.16,
    solver: str = "MOSEK",
    epsilon_regularization: float = 1e-9,
    verbose: bool = False,
) -> dict[str, Any]:
    """Kamin Eq. 16 finite-key length for ideal symmetric MDI-QKD.

    Loss model: symmetric two-arm MDI with total loss loss_dB_total over
    both Alice-Charlie and Charlie-Bob arms combined.
        η_end2end = 10^(−loss_dB_total/10)
        η_A = η_B = √η_end2end (symmetric)
        p_detect_effective = η_A · η_B = η_end2end (for coincidence clicks)

    Per-round rate scales by:
        (1-γ)² · p_sift_base · η_end2end = (1-γ)² · (1/4) · η_end2end

    This is the MDI analog of `kamin_full_key_length_bb84_loss`.

    Args:
        qber: effective Alice-Bob QBER.
        n: signal rounds.
        loss_dB_total: total two-arm loss.
        gamma, alpha, eps_secure, f_EC: finite-key params.

    Returns:
        dict with ell, rate_per_round, h_per_sift, g_star, status, etc.
    """
    if loss_dB_total < 0.0:
        raise ValueError(f"loss_dB_total must be ≥ 0, got {loss_dB_total}")
    if n < 1:
        raise ValueError(f"n must be ≥ 1, got {n}")

    eta_end2end = 10.0 ** (-loss_dB_total / 10.0)
    # MDI effective per-round sift probability:
    # p_sift_effective = (1-γ)² · (1/4) · η_end2end
    # In the qubit BB84 Kamin framework, (1-γ)² · η_det is the sift factor.
    # For MDI we use eta_det_effective = (1/4) · η_end2end.
    eta_det_eff = 0.25 * eta_end2end

    # Solve Kamin SDP for conditional h_per_sift
    sdp = kamin_mdi_h_per_sift(
        qber=qber, gamma=gamma, solver=solver,
        epsilon_regularization=epsilon_regularization, verbose=verbose,
    )
    h_per_sift = sdp["h_per_sift"]
    g_Z = sdp["g_star"]["g_star_Z"]
    g_X = sdp["g_star"]["g_star_X"]

    # Use the shared helper (same formula as qubit BB84 loss, with
    # eta_det_eff absorbing MDI's p_sift_base = 1/4)
    ell = _kamin_ell_from_sdp_result(
        h_per_sift=h_per_sift, g_Z=g_Z, g_X=g_X,
        qber=qber, n=n, gamma=gamma, alpha=alpha,
        eps_secure=eps_secure, f_EC=f_EC, eta_det=eta_det_eff,
    )

    # Per-round rate for return dict
    R_per_round = eta_det_eff * (1.0 - gamma) ** 2 * h_per_sift

    return {
        "ell": ell,
        "rate_per_round": ell / n,
        "R_per_round_asymp": R_per_round,
        "h_per_sift": h_per_sift,
        "eta_end2end": eta_end2end,
        "eta_det_eff": eta_det_eff,
        "protocol": "mdi",
        "g_star": sdp["g_star"],
        "sdp_status": sdp["status"],
    }


def kamin_mdi_key_length_optimized(
    qber: float,
    n: int,
    loss_dB_total: float,
    eps_secure: float = 1e-8,
    f_EC: float = 1.16,
    gamma_grid: tuple[float, ...] = (
        0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5,
    ),
    alpha_grid: tuple[float, ...] | None = None,
    solver: str = "MOSEK",
    epsilon_regularization: float = 1e-9,
    verbose: bool = False,
) -> dict[str, Any]:
    """Grid-optimize (γ, α) for Kamin MDI finite-key.

    Like kamin_full_key_length_bb84_loss_optimized but with p_sift=1/4.
    SDP solved ONCE at (qber, gamma_grid[0]); (γ, α) sweep is cached
    (γ, α enter only via the key-length formula, not the SDP).
    """
    if alpha_grid is None:
        inv_sqrt_n = 1.0 / math.sqrt(n)
        alpha_grid = tuple(
            1.0 + scale * inv_sqrt_n
            for scale in (0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0)
            if 1.0 + scale * inv_sqrt_n < 1.5
        )

    # Solve SDP once
    sdp = kamin_mdi_h_per_sift(
        qber=qber, gamma=gamma_grid[0], solver=solver,
        epsilon_regularization=epsilon_regularization, verbose=verbose,
    )
    h_per_sift = sdp["h_per_sift"]
    g_Z = sdp["g_star"]["g_star_Z"]
    g_X = sdp["g_star"]["g_star_X"]

    eta_end2end = 10.0 ** (-loss_dB_total / 10.0)
    eta_det_eff = 0.25 * eta_end2end

    best_ell = -math.inf
    best_gamma = gamma_grid[0]
    best_alpha = alpha_grid[0]
    for gamma in gamma_grid:
        for alpha in alpha_grid:
            try:
                ell = _kamin_ell_from_sdp_result(
                    h_per_sift=h_per_sift, g_Z=g_Z, g_X=g_X,
                    qber=qber, n=n, gamma=gamma, alpha=alpha,
                    eps_secure=eps_secure, f_EC=f_EC, eta_det=eta_det_eff,
                )
            except (ValueError, OverflowError):
                continue
            if ell > best_ell:
                best_ell = ell
                best_gamma = gamma
                best_alpha = alpha

    return {
        "ell_star": best_ell,
        "rate_star": best_ell / n,
        "gamma_star": best_gamma,
        "alpha_star": best_alpha,
        "h_per_sift": h_per_sift,
        "eta_end2end": eta_end2end,
        "eta_det_eff": eta_det_eff,
        "protocol": "mdi",
        "g_star": sdp["g_star"],
        "sdp_status": sdp["status"],
    }
