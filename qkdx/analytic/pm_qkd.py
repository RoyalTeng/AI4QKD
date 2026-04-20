"""PM-QKD (Ma-Zeng-Zhou 2018) analytic key-rate helpers — F6 §7.3 first pass.

Reference:
    - Ma, X., Zeng, P., Zhou, H. (2018). Phase-Matching Quantum Key Distribution.
      PRX 8:031043. arXiv:1805.05538v3.
    - docs/literature/TF-QKD.md §4.3 (Level 3 memo)
    - docs/msen/pm_qkd_formulation.md (v0.1 Round 4)

Scope (first pass, tfqkd_family.md §7.3):
    * Ma Eq. 4 asymptotic per-pulse rate R_PM = (2/M) Q_μ [1 − H(E_μ^X) − f H(E_μ^Z)]
    * Ma Eq. 2 decoy-state upper bound on phase-error rate E_μ^X
    * Honest-behaviour simulation: dark counts + detector efficiency + misalignment
    * log-log √η scaling validation (tfqkd_family.md §5.2 acceptance)

Not in scope (§7.5+):
    - Rigorous decoy-state yield inversion from multi-intensity measurements
    - Discrete-phase randomization + slice choice optimization
    - Protocol builder with MS-EB source_state (`qkdx/protocols/pm_qkd.py`)

Physical model:
    - Per-arm transmittance: η_arm = √η_total (since Alice→Charlie distance = L/2)
    - Total arm-to-detection efficiency: η = η_arm · η_det
    - Charlie gain: Q_μ = 2 · (1 − (1 − p_d) · e^{-η·μ/2})² · e^{-η·μ/2}   (small-μ ≈ η·μ)
    - Phase error: E_μ^X ≤ decoy UB (Ma Eq. 2)
    - Bit error: E_μ^Z ≈ e_d + p_d/Q_μ (misalignment + dark-count background)
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class PmQkdParams:
    """Physical setup parameters for PM-QKD (Ma-Zeng-Zhou 2018 Fig. 3b).

    Attributes:
        eta_det: detector quantum efficiency (per detector)
        p_d: dark-count probability per detector per pulse
        e_d: optical misalignment error
        f_ec: error-correction efficiency (≥ 1)
        e_0: QBER contribution of vacuum/background (0.5 for uniform)
        M: number of phase slices (sifting factor 2/M; M must be even, ≥ 4)
        alpha_db_per_km: fibre attenuation coefficient
    """
    eta_det: float = 0.145
    p_d: float = 8e-8
    e_d: float = 0.015
    f_ec: float = 1.15
    e_0: float = 0.5
    M: int = 16
    alpha_db_per_km: float = 0.2

    def __post_init__(self) -> None:
        if not (0.0 < self.eta_det <= 1.0):
            raise ValueError(f"eta_det must be in (0, 1], got {self.eta_det}")
        if not (0.0 <= self.p_d < 1.0):
            raise ValueError(f"p_d must be in [0, 1), got {self.p_d}")
        if not (0.0 <= self.e_d <= 0.5):
            raise ValueError(f"e_d must be in [0, 0.5], got {self.e_d}")
        if self.f_ec < 1.0:
            raise ValueError(f"f_ec must be ≥ 1, got {self.f_ec}")
        if not (0.0 <= self.e_0 <= 1.0):
            raise ValueError(f"e_0 must be in [0, 1], got {self.e_0}")
        if self.M < 4 or self.M % 2 != 0:
            raise ValueError(f"M must be even and ≥ 4, got {self.M}")
        if self.alpha_db_per_km < 0.0:
            raise ValueError(f"alpha_db_per_km must be ≥ 0, got {self.alpha_db_per_km}")


def _binary_entropy(p: float) -> float:
    """Binary entropy h(p) in bits, with 0·log 0 = 0."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


# ---------------------------------------------------------------------------
# Ma Appendix B / §V simulation formulas
# ---------------------------------------------------------------------------

def pm_charlie_gain(mu: float, eta_total: float, p_d: float) -> float:
    """Charlie single-click gain Q_μ (Ma §V simulation, Appendix B).

        Q_μ = 2 · [1 − (1 − p_d) · e^{−η·μ/2}] · (1 − p_d) · e^{−η·μ/2}

    Derivation: each detector sees independent Poisson mean η·μ/2 (half the
    total intensity after 50:50 BS with phase-averaged input).  Detector-i
    fires with probability 1 − (1 − p_d)·e^{−η·μ/2}.  Exactly-one-click =
    (L fires ∧ R silent) ∨ (R fires ∧ L silent), each with probability
    [1 − (1 − p_d)·e^{−η·μ/2}] · (1 − p_d)·e^{−η·μ/2}, times 2 by symmetry.

    Limits:
        - η → 0:    Q_μ → 2·p_d·(1 − p_d) = Y_0   (dark-only limit, matches `pm_vacuum_yield`)
        - η·μ small: Q_μ ≈ η·μ + 2·p_d·(1 − 2·p_d − η·μ)
        - Per-arm transmittance √η_total ⇒ Q_μ ∝ √η_total (the √η scaling)

    Args:
        mu: total Alice-Bob intensity (μ = μ_a + μ_b); often μ ≈ 0.3-0.9.
        eta_total: combined per-click efficiency η = η_arm · η_det
                   (for total Alice-Bob transmittance η_AB, η = √η_AB · η_det).
        p_d: dark-count probability per detector per pulse.

    Returns:
        Q_μ ∈ [0, 1].

    Raises:
        ValueError on invalid inputs.
    """
    if mu < 0.0:
        raise ValueError(f"mu must be ≥ 0, got {mu}")
    if not (0.0 <= eta_total <= 1.0):
        raise ValueError(f"eta_total must be in [0, 1], got {eta_total}")
    if not (0.0 <= p_d < 1.0):
        raise ValueError(f"p_d must be in [0, 1), got {p_d}")

    decay = math.exp(-eta_total * mu / 2.0)
    fire_prob = 1.0 - (1.0 - p_d) * decay
    silent_prob = (1.0 - p_d) * decay
    return 2.0 * fire_prob * silent_prob


def pm_single_photon_yield(eta_total: float, p_d: float) -> float:
    """Single-photon yield Y_1 (Ma §V / Appendix B).

        Y_1 = η + 2·p_d · (1 − η)   (small p_d, leading order)
            ≈ η + 2·p_d            when η ≪ 1

    Single photon from one arm goes to BS, routed to either detector with
    probability η/2 each → Y_1 ≈ η (plus dark-count contribution).

    Args:
        eta_total: per-click efficiency.
        p_d: dark-count probability per detector per pulse.

    Returns:
        Y_1 ∈ [0, 1].
    """
    if not (0.0 <= eta_total <= 1.0):
        raise ValueError(f"eta_total must be in [0, 1], got {eta_total}")
    if not (0.0 <= p_d < 1.0):
        raise ValueError(f"p_d must be in [0, 1), got {p_d}")
    # Single photon → exactly-one-click probability: η + 2·p_d·(1-η)·(1-p_d)
    # At small p_d: Y_1 ≈ η + 2·p_d - 2·η·p_d
    return eta_total + 2.0 * p_d * (1.0 - eta_total) * (1.0 - p_d)


def pm_vacuum_yield(p_d: float) -> float:
    """Vacuum yield Y_0 = 2 · p_d · (1 − p_d).

    Probability of exactly-one-click at Charlie when both arms have no photon:
    one of the two dark-count detectors fires, the other does not.
    """
    if not (0.0 <= p_d < 1.0):
        raise ValueError(f"p_d must be in [0, 1), got {p_d}")
    return 2.0 * p_d * (1.0 - p_d)


def pm_bit_error_rate(
    mu: float,
    eta_total: float,
    p_d: float,
    e_d: float,
    Q_mu: float | None = None,
) -> float:
    """Z-basis bit error rate E_μ^Z (Ma §V honest-behaviour simulation).

        E_μ^Z = [e_d · (Q_μ − Y_0) + (1/2) · Y_0] / Q_μ

    Misaligned signals contribute e_d fraction of errors; dark counts
    contribute 1/2 (random).  At small p_d: E_μ^Z ≈ e_d.

    Args:
        mu, eta_total, p_d, e_d: physical parameters.
        Q_mu: optional pre-computed gain; recomputes if None.

    Returns:
        E_μ^Z ∈ [0, 0.5].
    """
    if Q_mu is None:
        Q_mu = pm_charlie_gain(mu, eta_total, p_d)
    if Q_mu <= 0.0:
        return 0.5  # no signal detected, worst-case
    Y_0 = pm_vacuum_yield(p_d)
    signal_contribution = e_d * (Q_mu - Y_0)
    dark_contribution = 0.5 * Y_0
    return min(max((signal_contribution + dark_contribution) / Q_mu, 0.0), 0.5)


def pm_phase_error_upper(
    mu: float,
    Q_mu: float,
    Y_0: float,
    e_0: float = 0.5,
    e_d: float = 0.0,
    Y_1: float | None = None,
) -> float:
    """Ma Eq. 2 odd/even-photon phase-error upper bound (honest simulation).

        E_μ^X ≤ e_0 · q_0 + Σ_{k=0}^∞ e_{2k+1} · q_{2k+1}
                + (1 − q_0 − Σ_{k=0}^∞ q_{2k+1})

    **First-pass simplification** (F6 §7.3 initial, honest behaviour):
        Only the vacuum (q_0 contributes e_0) and single-photon (q_1 contributes
        e_d) terms are retained with **estimated** Y_k rather than worst-case
        Y_k ≤ 1.  Higher odd-photon components and the even-complement are
        absorbed into a residual slack proportional to the observed background
        (Y_0 / Q_μ).  Full multi-photon decomposition with per-k decoy yield
        inversion is deferred to §7.5+.

    Args:
        mu: intensity.
        Q_mu: measured total gain.
        Y_0: measured vacuum yield (dark-count related).
        e_0: vacuum-event QBER (default 0.5 = uniform).
        e_d: misalignment QBER contribution to single-photon phase error.
        Y_1: single-photon yield estimate; if None, uses Y_1 ≈ eta_effective
             leading-order approximation derived from (Q_μ, Y_0, μ) via the
             small-μ decoy limit.

    Returns:
        E_μ^X ∈ [0, 1] upper bound.
    """
    if mu <= 0.0:
        return e_0
    if Q_mu <= 0.0:
        return 1.0

    # Poisson weights
    p0 = math.exp(-mu)
    p1 = mu * math.exp(-mu)

    # q_0 (vacuum fraction of Charlie clicks)
    q0 = p0 * Y_0 / Q_mu

    # Leading-order Y_1 estimate (honest simulation; per-arm single-photon yield
    # ≈ effective per-click efficiency).  Extract from (Q_μ, Y_0, μ) via the
    # small-μ limit Q_μ ≈ μ·Y_1 + Y_0.
    if Y_1 is None:
        Y_1 = max(0.0, (Q_mu - Y_0) / mu) if mu > 0.0 else 0.0
    q1 = p1 * Y_1 / Q_mu

    # Single-photon phase-error contribution: dominated by misalignment e_d,
    # plus background fraction (dark counts corrupting single-photon events).
    # For honest behaviour: e_1 ≈ e_d + (Y_0/2) / Y_1 (dark contributes 1/2
    # random error per BG event).
    if Y_1 > 0.0:
        e_1 = min(0.5, e_d + 0.5 * Y_0 / Y_1)
    else:
        e_1 = 0.5
    single_contrib = q1 * e_1

    # Complement slack: 1 − q_0 − q_1 covers multi-photon components;
    # conservatively contributes at most this fraction to E_X.
    complement = max(0.0, 1.0 - q0 - q1)

    raw = e_0 * q0 + single_contrib + complement
    return min(max(raw, 0.0), 1.0)


# ---------------------------------------------------------------------------
# Main asymptotic rate (Ma Eq. 4)
# ---------------------------------------------------------------------------

def pm_asymptotic_rate(
    mu: float,
    eta_channel: float,
    params: PmQkdParams = PmQkdParams(),
) -> float:
    """Ma Eq. 4 per-pulse asymptotic key rate.

        R_PM ≥ (2/M) · Q_μ · [1 − H(E_μ^X) − f_EC · H(E_μ^Z)]

    where Q_μ, E_μ^X, E_μ^Z are computed from the honest-behaviour simulation
    with per-click efficiency η = √η_channel · η_det.

    Args:
        mu: intensity μ = μ_a + μ_b.
        eta_channel: **total** Alice-Bob channel transmittance (e.g., 10^{-L/50}
                     for fibre loss L dB at 0.2 dB/km); per-arm transmittance
                     is √eta_channel.
        params: PmQkdParams with detector + misalignment + M settings.

    Returns:
        Per-pulse key rate (bits), may be negative below threshold.
    """
    if mu < 0.0:
        raise ValueError(f"mu must be ≥ 0, got {mu}")
    if not (0.0 <= eta_channel <= 1.0):
        raise ValueError(f"eta_channel must be in [0, 1], got {eta_channel}")

    # Per-arm efficiency: each arm sees √η_channel (half-distance each)
    eta_arm = math.sqrt(eta_channel)
    eta_effective = eta_arm * params.eta_det

    Q_mu = pm_charlie_gain(mu, eta_effective, params.p_d)
    Y_0 = pm_vacuum_yield(params.p_d)
    E_Z = pm_bit_error_rate(mu, eta_effective, params.p_d, params.e_d, Q_mu=Q_mu)
    E_X = pm_phase_error_upper(mu, Q_mu, Y_0, e_0=params.e_0, e_d=params.e_d)

    privacy = 1.0 - _binary_entropy(E_X)
    leak_ec = params.f_ec * _binary_entropy(E_Z)
    per_sift_net = privacy - leak_ec

    return (2.0 / params.M) * Q_mu * per_sift_net


def pm_qkd_sweep_vs_loss(
    mu: float,
    loss_db_values: list[float],
    params: PmQkdParams = PmQkdParams(),
) -> tuple[list[float], list[float]]:
    """Sweep PM-QKD rate over a list of total loss values (in dB).

    Args:
        mu: intensity.
        loss_db_values: list of total Alice-Bob loss in dB.
        params: physical parameters.

    Returns:
        (loss_db_values, rates) — rates is list of per-pulse R_PM (may be
        negative where the protocol aborts).
    """
    rates: list[float] = []
    for loss in loss_db_values:
        eta = 10.0 ** (-loss / 10.0)
        rates.append(pm_asymptotic_rate(mu=mu, eta_channel=eta, params=params))
    return list(loss_db_values), rates
