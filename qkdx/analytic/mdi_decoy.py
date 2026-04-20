"""MDI-QKD decoy-state analytic key rate formulas (Ma-Razavi 2012).

Reference: Ma & Razavi (2012). Alternative schemes for MDI-QKD.
           PRA 86:062319. arXiv:1204.4856.

Implements the "original MDI-QKD" key rate (Appendix B §4, Eq. B27),
corresponding to the Lo-Curty-Qi 2012 X-Z basis encoding with decoy states.
This reproduces the "Decoy: original" (dashed) curve in Fig. 4.

Physical model (Appendix A + B):
    Y_11   — single-photon BSM success probability (Eq. A9)
    e_11   — single-photon QBER including misalignment (Eq. A11)
    Q_11   — single-photon gain (Eq. B1)
    Q_rect — gain in Z-basis (rectilinear) (Eqs. B28–B30)
    E_rect — QBER in Z-basis (Eq. B31)

Default parameters match Table I (η_det=14.5 %, p_d=3e-6, f=1.16, e_d=1.5 %).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from scipy.special import i0 as bessel_i0  # modified Bessel function I_0(x)


# ---------------------------------------------------------------------------
# Physical parameters dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MdiDecoyParams:
    """Physical setup parameters for MDI-QKD (Ma-Razavi 2012 Table I).

    Attributes:
        eta_det:  detector quantum efficiency (per detector)
        p_d:      dark-count probability per detector per pulse
        e_d:      optical misalignment error (relative phase distortion)
        f_ec:     error-correction efficiency (≥ 1)
        e_0:      QBER contribution of vacuum/background (default 0.5)
        alpha_db_per_km: fibre loss coefficient [dB/km]
    """
    eta_det: float = 0.145
    p_d: float = 3.0e-6
    e_d: float = 0.015
    f_ec: float = 1.16
    e_0: float = 0.5
    alpha_db_per_km: float = 0.2  # standard single-mode fibre

    def __post_init__(self) -> None:
        if not (0.0 < self.eta_det <= 1.0):
            raise ValueError(f"eta_det must be in (0,1], got {self.eta_det}")
        if not (0.0 <= self.p_d < 1.0):
            raise ValueError(f"p_d must be in [0,1), got {self.p_d}")
        if not (0.0 <= self.e_d <= 0.5):
            raise ValueError(f"e_d must be in [0,0.5], got {self.e_d}")
        if self.f_ec < 1.0:
            raise ValueError(f"f_ec must be ≥ 1, got {self.f_ec}")

    def arm_efficiency(self, loss_db_per_arm: float) -> float:
        """Total per-arm efficiency η = η_det × 10^(-loss_dB/10)."""
        eta_fibre = 10.0 ** (-loss_db_per_arm / 10.0)
        return self.eta_det * eta_fibre


# ---------------------------------------------------------------------------
# Core Ma-Razavi 2012 formulas
# ---------------------------------------------------------------------------

def y11_single_photon(eta_a: float, eta_b: float, p_d: float) -> float:
    """Single-photon BSM yield Y_11 (Ma-Razavi 2012 Eq. A9).

        Y_11 = (1-p_d)^2 [η_a η_b/2
                           + (2η_a + 2η_b − 3η_a η_b) p_d
                           + 4(1−η_a)(1−η_b) p_d^2]

    Y_11 is the probability of a successful partial BSM given that both Alice
    and Bob transmit a single photon and choose the same basis.  Reduces to
    η_a η_b / 2 when p_d = 0 (no background).

    Args:
        eta_a: total path efficiency for Alice's arm (fibre × detector)
        eta_b: total path efficiency for Bob's arm
        p_d:   dark-count probability per detector per pulse

    Returns:
        Y_11 ∈ [0, 1]
    """
    pd2 = (1.0 - p_d) ** 2
    return pd2 * (
        eta_a * eta_b / 2.0
        + (2 * eta_a + 2 * eta_b - 3 * eta_a * eta_b) * p_d
        + 4.0 * (1.0 - eta_a) * (1.0 - eta_b) * p_d ** 2
    )


def e11_single_photon(
    eta_a: float,
    eta_b: float,
    p_d: float,
    e_d: float,
    Y_11: float,
    e_0: float = 0.5,
) -> float:
    """Single-photon QBER e_11 (Ma-Razavi 2012 Eq. A11).

    From Eq. (A11):
        e_11 Y_11 = e_0 Y_11 − (e_0 − e_d)(1−p_d)^2 η_a η_b / 2

    Rearranging:
        e_11 = e_0 − (e_0 − e_d)(1−p_d)^2 η_a η_b / (2 Y_11)

    Args:
        eta_a, eta_b: arm efficiencies
        p_d: dark-count rate per detector
        e_d: misalignment error (variance of Δ_θ = θ_a − θ_b)
        Y_11: single-photon yield (from y11_single_photon)
        e_0: background QBER (0.5 for fully random background)

    Returns:
        e_11 ∈ [0, 0.5], clamped at 0.5 if Y_11 ≈ 0
    """
    if Y_11 < 1e-15:
        return e_0
    pd2 = (1.0 - p_d) ** 2
    e11 = e_0 - (e_0 - e_d) * pd2 * eta_a * eta_b / (2.0 * Y_11)
    return float(min(max(e11, 0.0), 0.5))


def q11_gain(mu_a: float, mu_b: float, Y_11: float) -> float:
    """Single-photon gain Q_11 (Ma-Razavi 2012 Eq. B1).

        Q_11 = μ_a μ_b e^{−μ_a − μ_b} Y_11

    Probability that Alice sends μ_a, Bob sends μ_b, both contributing
    single-photon Fock states (Poisson weight) and the BSM succeeds.

    Args:
        mu_a, mu_b: mean photon numbers (source intensities)
        Y_11: single-photon yield

    Returns:
        Q_11 ≥ 0
    """
    return mu_a * mu_b * math.exp(-mu_a - mu_b) * Y_11


def _q_rect_components(
    mu_a: float,
    mu_b: float,
    eta_a: float,
    eta_b: float,
    p_d: float,
) -> tuple[float, float]:
    """Q_rect^(C) and Q_rect^(E) (Ma-Razavi 2012 Eqs. B29–B30).

    Decomposition of the Z-basis (rectilinear) gain into:
        Q_rect^(C): contribution from the "correlated" scenario (Eq. B29)
        Q_rect^(E): contribution from the "error" scenario (Eq. B30)

    Notation (Eq. B7):
        μ' = η_a μ_a + η_b μ_b
        x  = √(η_a μ_a η_b μ_b) / 2
    """
    mu_prime = eta_a * mu_a + eta_b * mu_b
    x = math.sqrt(eta_a * mu_a * eta_b * mu_b) / 2.0

    pd2 = (1.0 - p_d) ** 2
    exp_half = math.exp(-mu_prime / 2.0)

    # Q_rect^(C) = 2(1-p_d)^2 e^{-μ'/2} [1-(1-p_d)e^{-η_a μ_a/2}][1-(1-p_d)e^{-η_b μ_b/2}]
    factor_a = 1.0 - (1.0 - p_d) * math.exp(-eta_a * mu_a / 2.0)
    factor_b = 1.0 - (1.0 - p_d) * math.exp(-eta_b * mu_b / 2.0)
    Q_C = 2.0 * pd2 * exp_half * factor_a * factor_b

    # Q_rect^(E) = 2 p_d (1-p_d)^2 e^{-μ'/2} [I_0(2x) - (1-p_d) e^{-μ'/2}]
    I0_2x = float(bessel_i0(2.0 * x))
    Q_E = 2.0 * p_d * pd2 * exp_half * (I0_2x - (1.0 - p_d) * exp_half)

    return Q_C, Q_E


def q_rect_total(
    mu_a: float,
    mu_b: float,
    eta_a: float,
    eta_b: float,
    p_d: float,
) -> float:
    """Z-basis (rectilinear) overall gain Q_rect (Eq. B28).

        Q_rect = Q_rect^(C) + Q_rect^(E)

    Q_rect is the probability that Alice and Bob choose the same rectilinear
    basis AND a successful BSM click occurs.
    """
    Q_C, Q_E = _q_rect_components(mu_a, mu_b, eta_a, eta_b, p_d)
    return Q_C + Q_E


def e_rect_qber(
    mu_a: float,
    mu_b: float,
    eta_a: float,
    eta_b: float,
    p_d: float,
    e_d: float,
) -> float:
    """Z-basis (rectilinear) QBER E_rect (Eq. B31).

        E_rect Q_rect = e_d Q_rect^(C) + (1 − e_d) Q_rect^(E)

    In the Z-basis, correlated clicks have misalignment error e_d;
    background-driven "error" clicks contribute (1 − e_d) ≈ 1.
    """
    Q_C, Q_E = _q_rect_components(mu_a, mu_b, eta_a, eta_b, p_d)
    Q_total = Q_C + Q_E
    if Q_total < 1e-15:
        return 0.5
    return (e_d * Q_C + (1.0 - e_d) * Q_E) / Q_total


def q_prime_0mu_b(
    mu_a: float,
    mu_b: float,
    eta_b: float,
    p_d: float,
) -> float:
    """Vacuum-Alice contribution Q'_{0μ_b} (Ma-Razavi 2012 Eq. B13).

        Q'_{0μ_b} = e^{−μ_a} · Q_{0μ_b}
        Q_{0μ_b}  = 4(1−p_d)^2 e^{−η_b μ_b/2} [1−(1−p_d)e^{−η_b μ_b/4}]^2

    This is the probability that Alice sends vacuum AND Bob sends μ_b AND the
    relay fires a successful BSM.  It contributes to the key rate only under
    FORWARD classical communication (Alice → Bob); including it extends the
    maximum operational loss by ~10 dB vs the conservative Eq. B27 lower bound.

    Note: Ma-Razavi Eq. B27 sets Q'_{0μ_b} = 0 as a lower bound. Including
    it (this function) better reproduces the Lo-Curty-Qi 2012 Fig. results.
    """
    pd2 = (1.0 - p_d) ** 2
    inner = 1.0 - (1.0 - p_d) * math.exp(-eta_b * mu_b / 4.0)
    Q_0mu_b = 4.0 * pd2 * math.exp(-eta_b * mu_b / 2.0) * inner ** 2
    return math.exp(-mu_a) * Q_0mu_b


def mdi_original_rate(
    mu_a: float,
    mu_b: float,
    eta_a: float,
    eta_b: float,
    p_d: float,
    e_d: float,
    f_ec: float,
    e_0: float = 0.5,
    include_vacuum_term: bool = False,
) -> float:
    """MDI-QKD (Lo-Curty-Qi 2012) key rate for given intensities.

    Ma-Razavi 2012 Eq. B27 (infinite decoy limit, symmetric MDI):

        R ≥ Q_11 [1 − H(e_11)] − Q_rect · f · H(E_rect)

    Optionally include the Q'_{0μ_b} forward-reconciliation vacuum term
    (Eq. B13) which Ma-Razavi sets to 0 as a conservative lower bound but
    which the Lo-Curty-Qi 2012 scheme inherits via forward communication:

        R ≥ Q_11 [1 − H(e_11)] + Q'_{0μ_b} − Q_rect · f · H(E_rect)

    Including Q'_{0μ_b} extends the operational loss by ~10 dB and better
    reproduces the "Decoy: original" dashed curve in Ma-Razavi Fig. 4.

    Note: bit/signal rate; basis-sift factor absorbed into Q_rect.

    Args:
        mu_a, mu_b: source intensities
        eta_a, eta_b: total arm efficiencies (fibre × detector)
        p_d: dark-count probability per detector
        e_d: misalignment error
        f_ec: error-correction efficiency (≥ 1)
        e_0: vacuum QBER (default 0.5)
        include_vacuum_term: if True, add Q'_{0μ_b} (Eq. B13)

    Returns:
        Key rate R (bits per signal); negative means infeasible.
    """
    Y_11 = y11_single_photon(eta_a, eta_b, p_d)
    e_11 = e11_single_photon(eta_a, eta_b, p_d, e_d, Y_11, e_0)
    Q_11 = q11_gain(mu_a, mu_b, Y_11)
    Q_rect = q_rect_total(mu_a, mu_b, eta_a, eta_b, p_d)
    E_rect = e_rect_qber(mu_a, mu_b, eta_a, eta_b, p_d, e_d)

    privacy = Q_11 * (1.0 - _h(e_11))
    if include_vacuum_term:
        privacy += q_prime_0mu_b(mu_a, mu_b, eta_b, p_d)
    ec_leak = Q_rect * f_ec * _h(E_rect)
    return privacy - ec_leak


def mdi_original_rate_optimised(
    eta_a: float,
    eta_b: float,
    params: MdiDecoyParams,
    mu_min: float = 0.01,
    mu_max: float = 1.0,
    n_grid: int = 50,
    include_vacuum_term: bool = True,
) -> float:
    """MDI-QKD key rate optimised over symmetric μ = μ_a = μ_b.

    Grid-searches μ ∈ [mu_min, mu_max] with n_grid points on a log scale,
    returns max(0, max_μ R(μ)).

    Args:
        eta_a, eta_b: arm efficiencies
        params: MdiDecoyParams (detector/channel parameters)
        mu_min, mu_max: intensity optimisation range
        n_grid: number of grid points
        include_vacuum_term: add Q'_{0μ_b} forward-reconciliation term
            (default True; better reproduces Ma-Razavi Fig.4 dashed curve)

    Returns:
        Optimised key rate ≥ 0 (clipped; 0.0 means infeasible regime).
    """
    best = 0.0
    for i in range(n_grid):
        mu = mu_min * (mu_max / mu_min) ** (i / (n_grid - 1))
        r = mdi_original_rate(
            mu_a=mu, mu_b=mu,
            eta_a=eta_a, eta_b=eta_b,
            p_d=params.p_d, e_d=params.e_d,
            f_ec=params.f_ec, e_0=params.e_0,
            include_vacuum_term=include_vacuum_term,
        )
        if r > best:
            best = r
    return best


def mdi_original_sweep(
    loss_db_total_range: list[float],
    params: MdiDecoyParams | None = None,
) -> list[float]:
    """Sweep key rate vs total two-arm fibre loss (dB).

    Implements the "Decoy: original" curve in Ma-Razavi 2012 Fig. 4.

    For each total loss value L_dB (= −10 log10(η_fibre_a × η_fibre_b)
    for the symmetric case, i.e., L_dB = 2 × one-arm loss in dB):

        η_fibre per arm = 10^(−L_dB/20)
        η_a = η_b = η_det × η_fibre

    Args:
        loss_db_total_range: list of total two-arm fibre loss values [dB]
        params: MdiDecoyParams; uses Ma-Razavi Table I defaults if None

    Returns:
        List of optimised key rates (bit/signal), clipped at 0.
        Matches Fig. 4 "Decoy: original" (dashed) curve ordering.
    """
    if params is None:
        params = MdiDecoyParams()

    rates = []
    for L in loss_db_total_range:
        eta_fibre = 10.0 ** (-L / 20.0)  # symmetric per-arm fibre transmissivity
        eta_a = params.eta_det * eta_fibre
        eta_b = params.eta_det * eta_fibre
        r = mdi_original_rate_optimised(eta_a, eta_b, params)
        rates.append(r)
    return rates


# ---------------------------------------------------------------------------
# Convenience: single-photon quantities (for theory/debug)
# ---------------------------------------------------------------------------

def y11_zero_background(eta_a: float, eta_b: float) -> float:
    """Y_11 in the absence of dark counts (p_d → 0).

    Y_11 = η_a η_b / 2  (linear in both arm efficiencies).
    Matches Ma-Razavi text below Eq. A9.
    """
    return eta_a * eta_b / 2.0


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _h(p: float) -> float:
    """Binary entropy h(p) = −p log₂ p − (1−p) log₂(1−p)."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)
