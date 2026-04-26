"""Reproduce Cui 2019 Fig. 1 (TF-QKD without phase postselection,
infinite decoy state) and overlay path α scaling UB + PLOB UB.

Source paper: C. Cui, Z.-Q. Yin, R. Wang, W. Chen, S. Wang, G.-C. Guo,
Z.-F. Han, "Twin-Field Quantum Key Distribution without Phase
Postselection", Phys. Rev. Applied 11, 034053 (2019).

Formulas:
- Q_μ from Cui Eq. (B1)
- e_μ from Cui Eq. (B2)
- Y_{n,m} from Cui Eq. (B3) (infinite decoy)
- x_{ij} from Cui Eq. (A7)
- I^u_AE from Cui Eq. (2) optimization
- Key rate R from Cui Eq. (3)

Path α scaling UB:
- Pirandola 2019 N=1 chain: R_UB = -log2(1 - sqrt(η_AB))
- η_AB is end-to-end transmittance (Alice to Bob)

PLOB UB (point-to-point, for reference):
- R_PLOB = -log2(1 - η_AB)

Strict scope (per autonomous plan §0):
- This script is REFRAMING ONLY
- No closure of any path α sub-gap
- Numerical "consistency" check only — does NOT confirm path α scaling tight
- Path α v0.3 [USER-APPROVED PRIORITY but NOT C3-passed] status unchanged

Cui 2019 simulation parameters (page 3 §IV, infinite decoy case):
- p_d (dark count rate) = 1e-11
- η_d (detector efficiency) = 0.80
- f (error correction efficiency) = 1.1
- e_d = 0 (assumed for ideal infinite decoy)

Usage:
    PYTHONPATH=. python scripts/reproduce_cui_2019_fig1.py
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "docs" / "research" / "data"
FIG_DIR = REPO_ROOT / "docs" / "research" / "figures"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Cui 2019 Fig. 1 parameters (page 3 §IV, infinite decoy case)
P_D = 1e-11        # dark count rate per detector per pulse
ETA_D = 0.80       # detector efficiency
F_EC = 1.1         # error correction efficiency
E_D = 0.0          # misalignment error (assumed 0 for ideal Fig. 1)

# Truncation for photon number sums (n, m in Cui Eq. (A7))
N_TRUNC = 30


def poisson_prob(n: int, mu: float) -> float:
    """P_n^μ = e^(-μ) μ^n / n!"""
    return math.exp(-mu) * (mu ** n) / math.factorial(n)


def Y_nm_infinite_decoy(n: int, m: int, eta: float, p_d: float) -> float:
    """Cui Eq. (B3): Y_{n,m} = 1 - (1-p_d)^2 (1-η)^(n+m)

    η here is the EFFECTIVE per-side transmittance (channel × detector).
    """
    return 1.0 - (1.0 - p_d) ** 2 * (1.0 - eta) ** (n + m)


def Q_mu(mu: float, eta: float, p_d: float) -> float:
    """Cui Eq. (B1): Q_μ = (1-p_d)[1 - (1-p_d) exp(-2ημ)] + (1-p_d) exp(-2ημ) p_d

    Note: this is for the SINGLE detector counting a click in "code mode".
    """
    exp_term = math.exp(-2.0 * eta * mu)
    return (1.0 - p_d) * (1.0 - (1.0 - p_d) * exp_term) + (1.0 - p_d) * exp_term * p_d


def e_mu(mu: float, eta: float, p_d: float) -> float:
    """Cui Eq. (B2): e_μ = exp(-2ημ) p_d / [1 - (1-2p_d) exp(-2ημ)]"""
    exp_term = math.exp(-2.0 * eta * mu)
    denom = 1.0 - (1.0 - 2.0 * p_d) * exp_term
    if denom <= 0:
        return 0.5
    return exp_term * p_d / denom


def x_parity_sum(mu: float, eta: float, p_d: float, parity_n: int, parity_m: int) -> float:
    """Compute |Σ_{n,m} sqrt(P_{2n+pn} P_{2m+pm} Y_{2n+pn, 2m+pm})|^2 (Cui Eq. A7)

    parity_n, parity_m ∈ {0, 1}
    """
    s = 0.0
    for n in range(N_TRUNC):
        for m in range(N_TRUNC):
            nn = 2 * n + parity_n
            mm = 2 * m + parity_m
            P_nn = poisson_prob(nn, mu)
            P_mm = poisson_prob(mm, mu)
            Y_nm = Y_nm_infinite_decoy(nn, mm, eta, p_d)
            s += math.sqrt(P_nn * P_mm * Y_nm)
    return s ** 2


def h_two_arg(x: float, y: float) -> float:
    """Cui's h(x,y) = -x log2(x) - y log2(y) + (x+y) log2(x+y)

    NOTE: this is NOT the standard binary entropy. It's defined in Cui Eq. (2).
    """
    if x <= 0 or y <= 0:
        return 0.0
    if x + y <= 0:
        return 0.0
    return (-x * math.log2(x) - y * math.log2(y) + (x + y) * math.log2(x + y))


def h_binary(p: float) -> float:
    """Standard binary entropy h(p) = -p log p - (1-p) log(1-p)"""
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def cui_2019_rate(loss_dB: float, mu: float) -> float:
    """Compute Cui 2019 protocol asymptotic key rate per trial.

    Eq. (3): R = Q_μ [1 - f·h(e_μ, 1-e_μ) - I^u_AE]

    Where I^u_AE (info leakage upper bound) is computed from Eq. (2)
    with x_ij as the upper bounds from Cui Eq. (A7).

    For infinite decoy state, x_ij computed accurately via Y_{n,m} (Eq. B3).

    Path-α-relevant note: this rate is for CODE mode only. Decoy mode is
    used to extract Y_{n,m} but doesn't contribute to key rate directly.
    """
    eta_arm = 10.0 ** (-loss_dB / 20.0) * ETA_D
    # Note: each arm has loss_dB/2 of fiber loss, so eta per arm in
    # symmetric setup is sqrt(eta_total_fiber) * detector_efficiency.
    # But Cui Fig. 1 uses TOTAL Alice-to-Bob distance (loss_dB total).
    # The two arms (Alice-to-Charlie + Charlie-to-Bob) split loss equally.
    # The "effective single-side η" = sqrt(η_total) (since η_total = η_A·η_B = η_each^2)
    # For the protocol formulas (Q_μ, e_μ, Y_nm), Cui's "η" is per-side.

    # Compute upper bounds on x_ij (Cui Eq. A7 with infinite decoy)
    x00_ub = x_parity_sum(mu, eta_arm, P_D, 0, 0)
    x10_ub = x_parity_sum(mu, eta_arm, P_D, 1, 0)
    x01_ub = x_parity_sum(mu, eta_arm, P_D, 0, 1)
    x11_ub = x_parity_sum(mu, eta_arm, P_D, 1, 1)

    Q = Q_mu(mu, eta_arm, P_D)
    if Q <= 0:
        return 0.0

    # Constraint: x_00 + x_10 + x_11 + x_01 = Q_μ
    # When sum exceeds Q, normalize down (per Cui Eq. (2) constraint set)
    total = x00_ub + x10_ub + x11_ub + x01_ub
    if total > Q:
        scale = Q / total
        x00 = x00_ub * scale
        x10 = x10_ub * scale
        x11 = x11_ub * scale
        x01 = x01_ub * scale
    else:
        x00, x10, x11, x01 = x00_ub, x10_ub, x11_ub, x01_ub

    # Cui Eq. (2): I^u_AE = h(x00/Q, x10/Q) + h(x11/Q, x01/Q)
    I_u_AE = h_two_arg(x00 / Q, x10 / Q) + h_two_arg(x11 / Q, x01 / Q)

    # Cui Eq. (3): R = Q [1 - f·h(e_μ, 1-e_μ) - I^u_AE]
    eu = e_mu(mu, eta_arm, P_D)
    R = Q * (1.0 - F_EC * h_binary(eu) - I_u_AE)
    return max(R, 0.0)


def cui_2019_optimized_rate(loss_dB: float) -> tuple[float, float]:
    """Optimize μ to maximize Cui rate at given loss."""
    best_R = 0.0
    best_mu = 0.0
    # Sweep μ on log scale
    mu_grid = np.logspace(-4, 0.5, 50)
    for mu in mu_grid:
        R = cui_2019_rate(loss_dB, mu)
        if R > best_R:
            best_R = R
            best_mu = float(mu)
    return best_R, best_mu


def plob_ub(loss_dB: float) -> float:
    """PLOB Eq. (19): C_loss(η) = -log2(1-η)

    η is END-TO-END transmittance (Alice to Bob direct).
    """
    eta = 10.0 ** (-loss_dB / 10.0)
    if eta >= 1.0:
        return float("inf")
    return -math.log2(1.0 - eta)


def path_alpha_scaling_ub(loss_dB: float) -> float:
    """Path α scaling UB = Pirandola 2019 N=1 chain capacity.

    -log2(1 - sqrt(η_AB))

    where η_AB is END-TO-END Alice-Bob transmittance.
    """
    eta = 10.0 ** (-loss_dB / 10.0)
    eta_arm = math.sqrt(eta)
    if eta_arm >= 1.0:
        return float("inf")
    return -math.log2(1.0 - eta_arm)


def main() -> None:
    print("Reproduce Cui 2019 Fig. 1 (TF-QKD without phase postselection)")
    print("Parameters: p_d=1e-11, η_d=0.80, f=1.1, e_d=0.0")
    print("=" * 72)

    loss_grid = np.linspace(0, 90, 91)
    cui_rates = []
    cui_mu_opt = []
    plob_ubs = []
    path_alpha_ubs = []

    for loss in loss_grid:
        R_cui, mu_opt = cui_2019_optimized_rate(float(loss))
        cui_rates.append(R_cui)
        cui_mu_opt.append(mu_opt)
        plob_ubs.append(plob_ub(float(loss)))
        path_alpha_ubs.append(path_alpha_scaling_ub(float(loss)))

    # Save CSV
    csv_path = DATA_DIR / "cui_2019_fig1_reproduction.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "loss_dB", "cui_rate", "mu_opt",
            "plob_ub", "path_alpha_scaling_ub",
        ])
        for i, loss in enumerate(loss_grid):
            w.writerow([
                f"{loss:.2f}",
                f"{cui_rates[i]:.6e}",
                f"{cui_mu_opt[i]:.4e}",
                f"{plob_ubs[i]:.6e}" if not math.isinf(plob_ubs[i]) else "inf",
                f"{path_alpha_ubs[i]:.6e}" if not math.isinf(path_alpha_ubs[i]) else "inf",
            ])
    print(f"Wrote {csv_path}")

    # Print summary
    print()
    print(f"{'loss(dB)':>9} {'Cui rate':>12} {'μ_opt':>8} {'PLOB UB':>12} {'α-UB':>12}")
    for i, loss in enumerate(loss_grid):
        if loss % 10 == 0:
            cui_str = f"{cui_rates[i]:.3e}" if cui_rates[i] > 0 else "0"
            plob_str = f"{plob_ubs[i]:.3e}" if not math.isinf(plob_ubs[i]) else "inf"
            alpha_str = f"{path_alpha_ubs[i]:.3e}" if not math.isinf(path_alpha_ubs[i]) else "inf"
            print(f"{loss:>9.0f} {cui_str:>12} {cui_mu_opt[i]:.2e} {plob_str:>12} {alpha_str:>12}")

    # Plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib unavailable; skipping plot")
        return

    fig, ax = plt.subplots(figsize=(8, 6))

    cui_arr = np.array(cui_rates)
    pos = cui_arr > 0
    ax.semilogy(
        loss_grid[pos], cui_arr[pos],
        "-", color="C2", lw=2.0,
        label="Cui 2019 simplified TF-QKD (infinite decoy, reproduced)",
    )

    plob_arr = np.array(plob_ubs)
    valid = ~np.isinf(plob_arr)
    ax.semilogy(
        loss_grid[valid], plob_arr[valid],
        "-", color="C0", lw=1.5,
        label=r"PLOB UB: $-\log_2(1-\eta_{AB})$ (point-to-point) [SYN]",
    )

    alpha_arr = np.array(path_alpha_ubs)
    valid = ~np.isinf(alpha_arr)
    ax.semilogy(
        loss_grid[valid], alpha_arr[valid],
        "--", color="C3", lw=2.0,
        label=r"path α scaling UB: $-\log_2(1-\sqrt{\eta_{AB}})$ [SYN, conditional on 11 sub-gaps]",
    )

    # Reference √η scaling line
    eta_grid = 10.0 ** (-loss_grid / 10.0)
    sqrt_eta_ref = np.sqrt(eta_grid) * 0.5  # arbitrary prefactor for visual reference
    ax.semilogy(
        loss_grid, sqrt_eta_ref,
        ":", color="gray", alpha=0.5,
        label=r"$\sqrt{\eta_{AB}}$ scaling reference (visual)",
    )

    ax.set_xlabel("Total fiber loss Alice-to-Bob (dB)")
    ax.set_ylabel("Key rate / Capacity bound (bits per channel use)")
    ax.set_title(
        "Cui 2019 Fig. 1 reproduction + path α scaling UB\n"
        "[SYN] reframing only — no path α sub-gap closure asserted"
    )
    ax.set_xlim(0, 90)
    ax.set_ylim(1e-10, 5.0)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="lower left", fontsize=8)

    fig.tight_layout()
    out_png = FIG_DIR / "cui_2019_fig1_reproduction.png"
    out_pdf = FIG_DIR / "cui_2019_fig1_reproduction.pdf"
    fig.savefig(out_png, dpi=150)
    fig.savefig(out_pdf)
    print(f"Wrote {out_png}")
    print(f"Wrote {out_pdf}")


if __name__ == "__main__":
    main()
