"""PM-QKD (Ma-Zeng-Zhou 2018) analytic key-rate helpers — F6 §7.3 Round 2.

Reference:
    - Ma, X., Zeng, P., Zhou, H. (2018). Phase-Matching Quantum Key Distribution.
      PRX 8:031043. arXiv:1805.05538v3.
    - docs/literature/TF-QKD.md §4.3 (Level 3 memo)
    - docs/msen/pm_qkd_formulation.md (v0.1 Round 4)

Scope (Round 2, post-dev-reviewer fixes):
    * Ma Appendix B Eq. B13 / B14 / B19 / B22 honest-behavior simulation
      (faithful transcription — Round 1 impl used BB84-style mixture which was
       flagged as a major correctness issue)
    * Ma Eq. 4 asymptotic per-pulse rate
    * Ma Eq. 2 decoy-based phase-error UB (honest-behavior first pass; full
      decoy inversion is §7.5+)
    * log-log √η scaling validation (tfqkd_family.md §5.2 slope 0.5 ± 0.05)

Not in scope:
    - Multi-intensity decoy inversion for tight Y_k bounds (§7.5+)
    - Protocol builder `qkdx/protocols/pm_qkd.py` with phase register R_A
    - Asymmetric μ_a ≠ μ_b, finite-key analysis

Convention:
    * `eta_total` arg name means the effective per-click efficiency η
      (= per-arm transmittance × η_det); this matches Ma Appendix B convention
      where η absorbs both channel loss AND detector efficiency.
    * For `pm_asymptotic_rate`, the argument `eta_channel` is the total Alice-Bob
      transmittance; the per-click η is √eta_channel · η_det (each arm = L/2).
    * `e_delta` is Ma's phase-slice discretization error (Eq. B19) plus any
      physical misalignment; for honest simulation we use a user-supplied value
      (default 0.015 = Ma Fig. 3b).
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class PmQkdParams:
    """Physical setup parameters for PM-QKD (Ma-Zeng-Zhou 2018 Fig. 3b).

    Attributes:
        eta_det: detector quantum efficiency.
        p_d: dark-count probability per detector per pulse.
        e_delta: effective signal-error rate (phase-slice discretization Eq. B19
                 + physical misalignment).  Default 0.015 matches Ma Fig. 3b
                 "misalignment error e_d".  For M=16 alone the phase-slice
                 contribution is ~0.0035; higher values include physical detector
                 alignment imperfection.
        f_ec: error-correction efficiency (≥ 1).
        e_0: background event QBER (0.5 for uniform dark-count contribution).
        M: number of phase slices (sifting factor 2/M; M must be even, ≥ 4).
        alpha_db_per_km: fibre attenuation coefficient.
    """
    eta_det: float = 0.145
    p_d: float = 8e-8
    e_delta: float = 0.015
    f_ec: float = 1.15
    e_0: float = 0.5
    M: int = 16
    alpha_db_per_km: float = 0.2

    def __post_init__(self) -> None:
        if not (0.0 < self.eta_det <= 1.0):
            raise ValueError(f"eta_det must be in (0, 1], got {self.eta_det}")
        if not (0.0 <= self.p_d < 1.0):
            raise ValueError(f"p_d must be in [0, 1), got {self.p_d}")
        if not (0.0 <= self.e_delta <= 0.5):
            raise ValueError(f"e_delta must be in [0, 0.5], got {self.e_delta}")
        if self.f_ec < 1.0:
            raise ValueError(f"f_ec must be ≥ 1, got {self.f_ec}")
        if not (0.0 <= self.e_0 <= 1.0):
            raise ValueError(f"e_0 must be in [0, 1], got {self.e_0}")
        if self.M < 4 or self.M % 2 != 0:
            raise ValueError(f"M must be even and ≥ 4, got {self.M}")
        if self.alpha_db_per_km < 0.0:
            raise ValueError(f"alpha_db_per_km must be ≥ 0, got {self.alpha_db_per_km}")


def _binary_entropy(p: float) -> float:
    """Binary entropy h(p) in bits with 0·log 0 = 0; clamps p to [0, 1]."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


# ---------------------------------------------------------------------------
# Ma Appendix B — honest-behaviour simulation formulas
# ---------------------------------------------------------------------------

def pm_charlie_gain(mu: float, eta_total: float, p_d: float) -> float:
    """Charlie single-click gain Q_μ — Ma Appendix B Eq. B14 (exact form):

        Q_μ = (1 − p_d) · [1 − (1 − 2·p_d) · e^{−η·μ}]

    Limits:
        - η → 0:      Q_μ → 2·p_d·(1 − p_d) = Y_0 (dark-only)
        - η·μ → ∞:    Q_μ → (1 − p_d) (saturated, suppressed by p_d since
                       the "quiet" detector also has a chance to dark-fire)
        - Small η·μ:  Q_μ ≈ η·μ + 2·p_d  (leading-order linear)

    Args:
        mu: intensity (μ = μ_a + μ_b = 2·μ_i).
        eta_total: effective per-click efficiency η = η_arm · η_det.
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
    return (1.0 - p_d) * (1.0 - (1.0 - 2.0 * p_d) * math.exp(-eta_total * mu))


def pm_k_photon_yield(k: int, eta_total: float, p_d: float) -> float:
    """k-photon yield Y_k — Ma Appendix B Eq. B13:

        Y_k = 1 − (1 − 2·p_d) · (1 − η)^k

    Limits:
        - k = 0:  Y_0 = 2·p_d (dark-only)
        - k = 1:  Y_1 = η + 2·p_d·(1 − η)
        - η → 0:  Y_k → 2·p_d (any k)
        - η → 1:  Y_k → 1 (any k ≥ 1)

    Args:
        k: photon number (≥ 0).
        eta_total: effective per-click efficiency.
        p_d: dark-count probability per detector.

    Returns:
        Y_k ∈ [0, 1].
    """
    if k < 0:
        raise ValueError(f"k must be ≥ 0, got {k}")
    if not (0.0 <= eta_total <= 1.0):
        raise ValueError(f"eta_total must be in [0, 1], got {eta_total}")
    if not (0.0 <= p_d < 1.0):
        raise ValueError(f"p_d must be in [0, 1), got {p_d}")
    return 1.0 - (1.0 - 2.0 * p_d) * (1.0 - eta_total) ** k


def pm_single_photon_yield(eta_total: float, p_d: float) -> float:
    """Single-photon yield Y_1 = η + 2·p_d·(1 − η)  (Ma Eq. B13 at k=1)."""
    return pm_k_photon_yield(k=1, eta_total=eta_total, p_d=p_d)


def pm_vacuum_yield(p_d: float) -> float:
    """Vacuum yield Y_0 = 2·p_d·(1 − p_d)  (exact from click probabilities);
    Ma B13 k=0 approximates Y_0 ≈ 2·p_d (dropping O(p_d²))."""
    if not (0.0 <= p_d < 1.0):
        raise ValueError(f"p_d must be in [0, 1), got {p_d}")
    return 2.0 * p_d * (1.0 - p_d)


def pm_phase_slice_error_rate(M: int) -> float:
    """Phase-slice discretization error e_δ — Ma Appendix B Eq. B19:

        e_δ = π/M − (M²/π²) · sin³(π/M)

    This is the minimum intrinsic signal QBER from discrete phase slicing at
    M slices (no physical misalignment).  At M=16 this is ~0.0035; for the
    Ma Fig. 3b "e_d = 0.015" total, physical detector misalignment adds ~0.0115.

    Args:
        M: number of phase slices (even, ≥ 4).

    Returns:
        e_δ ≥ 0.
    """
    if M < 4 or M % 2 != 0:
        raise ValueError(f"M must be even and ≥ 4, got {M}")
    return math.pi / M - (M ** 2 / math.pi ** 2) * math.sin(math.pi / M) ** 3


def pm_bit_error_rate(
    mu: float,
    eta_total: float,
    p_d: float,
    e_delta: float,
) -> float:
    """Z-basis bit error rate E_μ^Z — Ma Appendix B Eq. B22:

        E_μ^Z ≈ (p_d + η·μ·e_δ) · e^{−η·μ} / Q_μ

    Derivation: dark-count contributes p_d·e^{−η·μ} (dark causes click while
    signal path is silent); signal misalignment contributes η·μ·e_δ·e^{−η·μ}
    (first-order signal click × e_δ fraction of error).  Ma B20 approximation.

    Clamped to [0, 0.5] so binary entropy stays valid.

    Args:
        mu: intensity.
        eta_total: effective per-click efficiency.
        p_d: dark-count probability.
        e_delta: effective signal QBER (phase slice + physical misalignment).

    Returns:
        E_μ^Z ∈ [0, 0.5].
    """
    if mu < 0.0:
        raise ValueError(f"mu must be ≥ 0, got {mu}")
    if not (0.0 <= eta_total <= 1.0):
        raise ValueError(f"eta_total must be in [0, 1], got {eta_total}")
    if not (0.0 <= p_d < 1.0):
        raise ValueError(f"p_d must be in [0, 1), got {p_d}")
    if not (0.0 <= e_delta <= 0.5):
        raise ValueError(f"e_delta must be in [0, 0.5], got {e_delta}")

    Q_mu = pm_charlie_gain(mu=mu, eta_total=eta_total, p_d=p_d)
    if Q_mu <= 0.0:
        return 0.5
    decay = math.exp(-eta_total * mu)
    raw = (p_d + eta_total * mu * e_delta) * decay / Q_mu
    return min(max(raw, 0.0), 0.5)


def pm_phase_error_upper(
    mu: float,
    Q_mu: float,
    Y_0: float,
    e_0: float = 0.5,
    e_delta: float = 0.0,
) -> float:
    """Ma Eq. 2 odd/even-photon phase-error upper bound (honest-behavior).

        E_μ^X ≤ e_0 · q_0 + Σ_{k≥0} e_{2k+1} · q_{2k+1}
                + (1 − q_0 − Σ_{k≥0} q_{2k+1})

    **First-pass honest-behavior simulation**:
        Retain q_0 (vacuum, contributes e_0) + q_1 (single-photon, contributes
        e_δ) and route higher-photon components into a conservative complement
        slack.  Uses the internal fallback Y_1 ≈ max(0, (Q_μ - Y_0)/μ), which
        is a **provably conservative under-estimate** of the honest Y_1 (since
        Q_μ includes Poisson-weighted contributions from k ≥ 2, so subtracting
        Y_0 and dividing by μ gives strictly less than the full Y_1).  This
        preserves the upper-bound property of E_μ^X without requiring the
        caller to supply decoy-derived values.

    **Public-API safety decision (Round 4, post-dev-reviewer)**:
        Earlier iterations exposed `Y_1_lower` and `Y_1_upper_check` parameters
        so callers could plug in decoy-state-inferred single-photon yields.
        The Codex reviewer correctly observed that no library-side check can
        prove a caller-supplied `Y_1_lower` is truly a lower bound — passing
        `Y_1_upper_check=1.0` (trivially true since Y_1 ≤ 1) lets any
        `Y_1_lower ∈ [0, 1]` through, silently breaking the UB property.
        Therefore those parameters are REMOVED from the public API.  Honest-
        behavior callers use the internal fallback.  Decoy-state-derived
        tighter bounds belong in a separate function (§7.5+ work,
        `qkdx/analytic/pm_qkd_decoy.py`) that will also implement the full
        multi-intensity decoy inversion.

    Args:
        mu: intensity.
        Q_mu: measured total gain.
        Y_0: measured vacuum yield.
        e_0: vacuum-event QBER (default 0.5 = uniform).  Clamped to [0, 0.5]
             on return so entropy is monotone.
        e_delta: single-photon signal QBER (phase slice + misalignment).

    Returns:
        E_μ^X ∈ [0, 0.5] upper bound.

    Raises:
        ValueError on invalid inputs.
    """
    if mu < 0.0:
        raise ValueError(f"mu must be ≥ 0, got {mu}")
    if not (0.0 <= Q_mu <= 1.0):
        raise ValueError(f"Q_mu must be in [0, 1], got {Q_mu}")
    if not (0.0 <= Y_0 <= 1.0):
        raise ValueError(f"Y_0 must be in [0, 1], got {Y_0}")
    if not (0.0 <= e_0 <= 1.0):
        raise ValueError(f"e_0 must be in [0, 1], got {e_0}")
    if not (0.0 <= e_delta <= 0.5):
        raise ValueError(f"e_delta must be in [0, 0.5], got {e_delta}")

    # Edge: μ ≤ 0 — all weight on vacuum (e_0) but clamped to entropy-safe range
    if mu <= 0.0:
        return min(max(e_0, 0.0), 0.5)
    # Edge: Q_μ ≤ 0 — no sift events, worst-case UB
    if Q_mu <= 0.0:
        return 0.5

    p0 = math.exp(-mu)
    p1 = mu * math.exp(-mu)
    q0 = p0 * Y_0 / Q_mu

    # Internal fallback: Y_1 ≈ max(0, (Q_μ - Y_0)/μ) — conservative under-estimate
    Y_1_lower = max(0.0, (Q_mu - Y_0) / mu)
    q1 = p1 * Y_1_lower / Q_mu

    if Y_1_lower > 0.0:
        e_1 = min(0.5, e_delta + 0.5 * Y_0 / Y_1_lower)
    else:
        e_1 = 0.5
    single_contrib = q1 * e_1

    complement = max(0.0, 1.0 - q0 - q1)
    raw = e_0 * q0 + single_contrib + complement
    return min(max(raw, 0.0), 0.5)


# ---------------------------------------------------------------------------
# Main asymptotic rate (Ma Eq. 4 / B23)
# ---------------------------------------------------------------------------

def pm_asymptotic_rate(
    mu: float,
    eta_channel: float,
    params: PmQkdParams = PmQkdParams(),
) -> float:
    """Ma Eq. 4 / B23 per-pulse asymptotic key rate.

        R_PM ≥ (2/M) · Q_μ · [1 − H(E_μ^X) − f_EC · H(E_μ^Z)]

    Honest-behavior simulation: Q_μ, E_μ^Z, E_μ^X computed from Ma B14 / B22 /
    heuristic Eq. 2 with per-click efficiency η = √η_channel · η_det.

    Args:
        mu: intensity μ = μ_a + μ_b.
        eta_channel: **total** Alice-Bob channel transmittance; per-arm
                     transmittance is √eta_channel (each arm = L/2).
        params: PmQkdParams.

    Returns:
        Per-pulse key rate (bits), may be negative below threshold.
    """
    if mu < 0.0:
        raise ValueError(f"mu must be ≥ 0, got {mu}")
    if not (0.0 <= eta_channel <= 1.0):
        raise ValueError(f"eta_channel must be in [0, 1], got {eta_channel}")

    eta_arm = math.sqrt(eta_channel)
    eta_effective = eta_arm * params.eta_det

    Q_mu = pm_charlie_gain(mu=mu, eta_total=eta_effective, p_d=params.p_d)
    Y_0 = pm_vacuum_yield(p_d=params.p_d)
    E_Z = pm_bit_error_rate(
        mu=mu, eta_total=eta_effective, p_d=params.p_d, e_delta=params.e_delta,
    )
    # Round-4 safety decision: pm_phase_error_upper no longer accepts caller-
    # supplied Y_1 (would enable UB violation).  Uses internal conservative
    # fallback Y_1 ≈ (Q_μ - Y_0)/μ.  For decoy-state-derived tighter bounds,
    # see §7.5+ separate module (not yet implemented).
    E_X = pm_phase_error_upper(
        mu=mu, Q_mu=Q_mu, Y_0=Y_0, e_0=params.e_0, e_delta=params.e_delta,
    )

    privacy = 1.0 - _binary_entropy(E_X)
    leak_ec = params.f_ec * _binary_entropy(E_Z)
    per_sift_net = privacy - leak_ec

    return (2.0 / params.M) * Q_mu * per_sift_net


def pm_qkd_sweep_vs_loss(
    mu: float,
    loss_db_values: list[float],
    params: PmQkdParams = PmQkdParams(),
) -> tuple[list[float], list[float]]:
    """Sweep PM-QKD rate over list of total loss values (dB).

    Returns (loss_db_values, rates); rates may be negative where protocol aborts.
    """
    rates: list[float] = []
    for loss in loss_db_values:
        eta = 10.0 ** (-loss / 10.0)
        rates.append(pm_asymptotic_rate(mu=mu, eta_channel=eta, params=params))
    return list(loss_db_values), rates
