"""AD complete upper-bound hierarchy: K_D (degradable analytic) vs E_R^PPT (SDP, sparse) vs log_neg.

For γ ≤ 1/2: K_D = Q = max_p[h((1-γ)p) - h(γp)] (Caruso-Giovannetti-Holevo 2014).
For γ > 1/2: anti-degradable, Q = 0; K_D might still be > 0 via two-way LOCC (open).

Output:
  docs/research/figures/AD_complete_hierarchy.{png,pdf}
  docs/research/data/AD_complete_hierarchy.csv
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from qkdx.numerics.upper_bound import (
    K_D_amplitude_damping_degradable, analytic_log_neg_amplitude_damping,
)


def load_E_R_PPT_AD():
    """Load AD E_R^PPT SDP values from existing CSV."""
    csv_path = REPO / "docs" / "research" / "data" / "qubit_E_R_PPT_SDP_all_4.csv"
    pts = []
    with open(csv_path) as f:
        for r in csv.DictReader(f):
            if r["family"] == "AD":
                pts.append((float(r["param"]), float(r["E_R_PPT_SDP"])))
    return sorted(pts, key=lambda x: x[0])


def main():
    gammas = np.linspace(0.001, 0.999, 1001)
    log_neg = np.array([analytic_log_neg_amplitude_damping(g) for g in gammas])
    K_D = np.array([K_D_amplitude_damping_degradable(g) for g in gammas])

    er_pts = load_E_R_PPT_AD()
    er_g = np.array([p[0] for p in er_pts])
    er_v = np.array([p[1] for p in er_pts])

    out_csv = REPO / "docs" / "research" / "data" / "AD_complete_hierarchy.csv"
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["gamma", "log_neg_analytic", "K_D_degradable_analytic"])
        for g, ln, kd in zip(gammas, log_neg, K_D):
            w.writerow([f"{g:.4f}", f"{ln:.10f}", f"{kd:.10f}"])

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.5))

    # Left: absolute
    ax = axes[0]
    ax.plot(gammas, log_neg, label="log_neg (loosest UB, analytic)", linewidth=2, color="C0", alpha=0.8)
    ax.scatter(er_g, er_v, color="C1", marker="s", s=60,
               label=r"$E_R^{PPT}$ (MOSEK SDP, 7 pts)", zorder=5)
    # K_D solid for γ ≤ 1/2 (degradable), dashed/zero after
    K_D_deg = np.where(gammas <= 0.5, K_D, 0)
    ax.plot(gammas, K_D_deg, label=r"$K_D = Q$ (degradable γ ≤ 1/2)", linewidth=2.5, color="C2", linestyle="--")
    # Shaded "K_D unknown" region for γ > 1/2
    ax.axvspan(0.5, 1.0, alpha=0.08, color="gray")
    ax.text(0.65, 0.85, r"K_D unknown" + "\n" + r"(γ > 1/2,"+ "\n" + r"anti-degradable)",
            fontsize=8, color="gray", ha="center")
    ax.axvline(0.5, color="gray", linewidth=0.8, alpha=0.5, linestyle=":")
    ax.set_xlabel("γ (damping prob)")
    ax.set_ylabel("bits")
    ax.set_title("AD complete hierarchy: K_D ≤ $E_R^{PPT}$ ≤ log_neg")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.02, 1.05)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    # Right: ratios in degradable regime
    ax = axes[1]
    K_D_safe = np.where(K_D > 1e-6, K_D, np.nan)
    ax.plot(gammas, log_neg / K_D_safe, label="log_neg / K_D", linewidth=2, color="C0")
    # Sparse E_R/K_D
    K_D_at_er = np.array([K_D_amplitude_damping_degradable(g) for g in er_g])
    ratios_er_kd = np.where(K_D_at_er > 1e-6, er_v / K_D_at_er, np.nan)
    ax.scatter(er_g, ratios_er_kd, color="C1", marker="s", s=60, label=r"$E_R^{PPT}$ / K_D", zorder=5)
    ax.axvline(0.5, color="gray", linewidth=0.8, alpha=0.5, linestyle=":")
    ax.axhline(1.0, color="gray", linewidth=0.5, alpha=0.5)
    ax.set_xlabel("γ")
    ax.set_ylabel("UB / K_D ratio")
    ax.set_title(r"AD: tightness of UB candidates vs true K_D")
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0.5, 5.0)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig_dir = REPO / "docs" / "research" / "figures"
    fig.savefig(fig_dir / "AD_complete_hierarchy.png", dpi=160)
    fig.savefig(fig_dir / "AD_complete_hierarchy.pdf")
    plt.close(fig)

    print("Done.")
    print(f"  CSV:  docs/research/data/AD_complete_hierarchy.csv")
    print(f"  PNG:  docs/research/figures/AD_complete_hierarchy.png")
    print()
    print(f"AD complete hierarchy (γ ≤ 1/2 degradable):")
    print(f"  {'γ':>6} {'K_D':>9} {'E_R^PPT':>9} {'log_neg':>9} {'E_R/K_D':>9} {'log_neg/K_D':>11}")
    for g, ev in er_pts:
        if g >= 0.5: break
        kd = K_D_amplitude_damping_degradable(g)
        ln = analytic_log_neg_amplitude_damping(g)
        print(f"  {g:6.4f} {kd:9.4f} {ev:9.4f} {ln:9.4f} {ev/kd:9.3f} {ln/kd:11.3f}")


if __name__ == "__main__":
    main()
