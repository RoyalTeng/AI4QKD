"""Decoy-state analytic formulas.

Reference: Ma, Qi, Zhao, Lo (2005). Practical decoy state for quantum key
distribution. PRA 72:012326.  arXiv:quant-ph/0503005.

Key formulas (Ma 2005):
    * 1-decoy (signal μ + vacuum 0):           Eq. 34-35
    * 2-decoy (signal μ + two decoys ν₁ > ν₂): Eq. 36-37
    * Infinite-decoy limit:                     Lo-Ma-Chen 2005 PRL 94:230504

All bounds are LOWER bounds on Y_1 and UPPER bounds on e_1.  They are
chosen so that GLLP rate computed from (Y_1^L, e_1^U) gives a valid
asymptotic lower bound on the secret key rate.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class DecoyEstimates:
    """Estimated single-photon parameters from decoy measurements."""
    Y_1_lower: float  # Y_1^L
    e_1_upper: float  # e_1^U
    Q_1_lower: float  # Q_1^L = μ·e^(-μ)·Y_1^L (signal-pulse single-photon gain)
    mu: float         # signal intensity


def y1_one_decoy_vacuum(
    mu: float,
    nu: float,
    Q_mu: float,
    Q_nu: float,
    Y_0: float,
) -> float:
    """Y_1^L for 1-decoy (weak + vacuum) — Ma 2005 Eq. 34.

    Args:
        mu: signal intensity (larger)
        nu: weak decoy intensity (0 < ν < μ;  ν = 0 is the vacuum-only
            degenerate case — use y1_vacuum_only in that limit)
        Q_mu, Q_nu: measured gains at intensities μ and ν
        Y_0: measured vacuum yield (from separate vacuum pulses)

    Returns:
        Lower bound Y_1^L.  May be clamped to 0.0 when the raw formula
        goes negative (below-threshold parameter choice).

    Formula (Ma 2005 Eq. 34):
        Y_1^L = μ / (μν - ν²) · [Q_ν·e^ν − (ν/μ)²·Q_μ·e^μ − ((μ²-ν²)/μ²)·Y_0]
    """
    if not (0.0 < nu < mu):
        raise ValueError(f"require 0 < ν < μ, got ν={nu}, μ={mu}")

    numerator = (
        Q_nu * math.exp(nu)
        - (nu / mu) ** 2 * Q_mu * math.exp(mu)
        - ((mu ** 2 - nu ** 2) / mu ** 2) * Y_0
    )
    denominator = mu * nu - nu ** 2
    if abs(denominator) < 1e-15:
        raise ValueError("1-decoy denominator (μν-ν²) too small; check intensities")
    Y_1_raw = (mu / denominator) * numerator
    return max(0.0, Y_1_raw)


def e1_one_decoy_vacuum(
    nu: float,
    E_nu: float,
    Q_nu: float,
    Y_0: float,
    Y_1_lower: float,
    e_0: float = 0.5,
) -> float:
    """e_1^U for 1-decoy (weak + vacuum) — Ma 2005 Eq. 35.

    Formula:
        e_1^U = (E_ν·Q_ν·e^ν − e_0·Y_0) / (Y_1^L · ν)

    Clamped to [0, 1] (bound always physically meaningful).
    """
    if Y_1_lower < 1e-15 or nu < 1e-15:
        return 0.5  # no information on single-photon QBER; worst case
    numerator = E_nu * Q_nu * math.exp(nu) - e_0 * Y_0
    e_1_raw = numerator / (Y_1_lower * nu)
    return min(max(e_1_raw, 0.0), 0.5)


def y1_two_decoy(
    mu: float,
    nu_1: float,
    nu_2: float,
    Q_mu: float,
    Q_nu_1: float,
    Q_nu_2: float,
    Y_0: float,
) -> float:
    """Y_1^L for 2-decoy (signal + two decoys) — Ma 2005 Eq. 36.

    Args:
        mu: signal intensity
        nu_1, nu_2: decoy intensities with 0 ≤ ν₂ < ν₁ < μ and ν₁+ν₂ < μ
        Q_mu, Q_nu_1, Q_nu_2: measured gains
        Y_0: vacuum yield

    Formula:
        Y_1^L = μ / (μ·ν₁ − μ·ν₂ − ν₁² + ν₂²)
              · [Q_{ν₁}·e^{ν₁} − Q_{ν₂}·e^{ν₂}
                 − ((ν₁² − ν₂²)/μ²)·(Q_μ·e^μ − Y_0)]
    """
    if not (0.0 <= nu_2 < nu_1 < mu):
        raise ValueError(f"require 0 ≤ ν₂ < ν₁ < μ, got ν₁={nu_1}, ν₂={nu_2}, μ={mu}")
    if nu_1 + nu_2 >= mu:
        raise ValueError(f"require ν₁+ν₂ < μ for Ma-Qi-Zhao-Lo 2005 Eq. 36 validity; "
                         f"got ν₁+ν₂={nu_1+nu_2}, μ={mu}")

    denom = mu * nu_1 - mu * nu_2 - nu_1 ** 2 + nu_2 ** 2
    if abs(denom) < 1e-15:
        raise ValueError("2-decoy denominator too small; check intensities")

    numerator = (
        Q_nu_1 * math.exp(nu_1) - Q_nu_2 * math.exp(nu_2)
        - ((nu_1 ** 2 - nu_2 ** 2) / mu ** 2) * (Q_mu * math.exp(mu) - Y_0)
    )
    Y_1_raw = (mu / denom) * numerator
    return max(0.0, Y_1_raw)


def e1_two_decoy(
    nu_1: float,
    nu_2: float,
    E_nu_1: float,
    E_nu_2: float,
    Q_nu_1: float,
    Q_nu_2: float,
    Y_1_lower: float,
) -> float:
    """e_1^U for 2-decoy — Ma 2005 Eq. 37.

    Formula:
        e_1^U = (E_{ν₁}·Q_{ν₁}·e^{ν₁} − E_{ν₂}·Q_{ν₂}·e^{ν₂})
              / ((ν₁ − ν₂) · Y_1^L)
    """
    if Y_1_lower < 1e-15:
        return 0.5
    num = E_nu_1 * Q_nu_1 * math.exp(nu_1) - E_nu_2 * Q_nu_2 * math.exp(nu_2)
    denom = (nu_1 - nu_2) * Y_1_lower
    if abs(denom) < 1e-15:
        return 0.5
    e_1_raw = num / denom
    return min(max(e_1_raw, 0.0), 0.5)


# ---------------------------------------------------------------------------
# Convenience: turn a channel + intensities into DecoyEstimates
# ---------------------------------------------------------------------------

def estimate_decoy_vacuum(
    channel,  # qkdx.analytic.channel.FibreChannel
    mu: float,
    nu: float,
) -> DecoyEstimates:
    """1-decoy estimation using a FibreChannel to generate ground-truth gains.

    Alice sends signal μ and decoy ν (+ separately measures Y_0 from vacuum).
    Eve is assumed absent (normal-operation channel) — this gives the
    *observed* gains; the decoy bounds then produce Y_1^L, e_1^U that Alice
    would infer.

    Returns DecoyEstimates with Y_1^L, e_1^U, Q_1^L = μ·e^-μ·Y_1^L.
    """
    Q_mu = channel.Q_mu(mu)
    Q_nu = channel.Q_mu(nu)
    E_nu = channel.E_mu(nu)
    Y_0 = channel.Y_0()

    Y_1_L = y1_one_decoy_vacuum(mu, nu, Q_mu, Q_nu, Y_0)
    e_1_U = e1_one_decoy_vacuum(nu, E_nu, Q_nu, Y_0, Y_1_L)
    Q_1_L = mu * math.exp(-mu) * Y_1_L

    return DecoyEstimates(
        Y_1_lower=Y_1_L, e_1_upper=e_1_U, Q_1_lower=Q_1_L, mu=mu,
    )


def estimate_decoy_two(
    channel,
    mu: float,
    nu_1: float,
    nu_2: float,
) -> DecoyEstimates:
    """2-decoy estimation using a FibreChannel."""
    Q_mu = channel.Q_mu(mu)
    Q_nu_1 = channel.Q_mu(nu_1)
    Q_nu_2 = channel.Q_mu(nu_2)
    E_nu_1 = channel.E_mu(nu_1)
    E_nu_2 = channel.E_mu(nu_2)
    Y_0 = channel.Y_0()

    Y_1_L = y1_two_decoy(mu, nu_1, nu_2, Q_mu, Q_nu_1, Q_nu_2, Y_0)
    e_1_U = e1_two_decoy(nu_1, nu_2, E_nu_1, E_nu_2, Q_nu_1, Q_nu_2, Y_1_L)
    Q_1_L = mu * math.exp(-mu) * Y_1_L

    return DecoyEstimates(
        Y_1_lower=Y_1_L, e_1_upper=e_1_U, Q_1_lower=Q_1_L, mu=mu,
    )


# ---------------------------------------------------------------------------
# Asymptotic key rate (GLLP with decoy estimates)
# ---------------------------------------------------------------------------

def decoy_rate_gllp(
    estimates: DecoyEstimates,
    Q_mu: float,
    E_mu: float,
    f_ec: float = 1.22,
    q_sift: float = 0.5,
) -> float:
    """GLLP asymptotic rate R = q·{-Q_μ·f·h(E_μ) + Q_1^L·(1-h(e_1^U))}.

    Args:
        estimates: DecoyEstimates from estimate_decoy_* above
        Q_mu: observed gain at signal intensity (for EC leakage estimate)
        E_mu: observed QBER at signal intensity (for EC leakage)
        f_ec: error-correction efficiency
        q_sift: basis sifting factor (0.5 for BB84)

    Returns:
        R in bit/signal (NOT clipped at 0).
    """
    from qkdx.core.entropy import binary_entropy
    h_e_mu = binary_entropy(E_mu)
    h_e_1 = binary_entropy(estimates.e_1_upper)
    leak_ec = Q_mu * f_ec * h_e_mu
    privacy = estimates.Q_1_lower * (1.0 - h_e_1)
    return q_sift * (privacy - leak_ec)
