"""Plot AD channel hierarchy across γ ∈ [0,1] with anti-degradable emphasis.

Combines:
- log_neg analytic (dense, 1001 pts)
- Q analytic (dense, only for γ ≤ 0.5)
- E_R^PPT SDP (sparse, merged from qubit_E_R_PPT_SDP_all_4.csv + AD_antidegradable_E_R_PPT_fill.csv)

Highlights anti-degradable region (γ > 1/2) where Q=0 but E_R^PPT > 0.

Output:
  docs/research/figures/AD_anti_degradable_hierarchy.{png,pdf}
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from qkdx.numerics.upper_bound import (
    analytic_log_neg_amplitude_damping,
    quantum_capacity_amplitude_damping_degradable,
)


def load_E_R_PPT_AD():
    """Merge AD rows from both SDP CSVs."""
    pts = {}
    csv_main = REPO / "docs" / "research" / "data" / "qubit_E_R_PPT_SDP_all_4.csv"
    with open(csv_main) as f:
        for r in csv.DictReader(f):
            if r["family"] == "AD":
                pts[float(r["param"])] = float(r["E_R_PPT_SDP"])
    csv_fill = REPO / "docs" / "research" / "data" / "AD_antidegradable_E_R_PPT_fill.csv"
    if csv_fill.exists():
        with open(csv_fill) as f:
            for r in csv.DictReader(f):
                pts[float(r["gamma"])] = float(r["E_R_PPT_SDP"])
    return sorted(pts.items())


def main():
    gammas = np.linspace(0.001, 0.999, 1001)
    log_neg = np.array([analytic_log_neg_amplitude_damping(g) for g in gammas])
    Q = np.array([quantum_capacity_amplitude_damping_degradable(g) for g in gammas])

    er_pts = load_E_R_PPT_AD()
    er_g = np.array([g for g, _ in er_pts])
    er_v = np.array([v for _, v in er_pts])

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8))

    # Left: absolute scale
    ax = axes[0]
    ax.axvspan(0.5, 1.0, alpha=0.10, color="gray")
    ax.text(0.72, 0.82, r"$Q = 0$" + "\n" + r"(anti-degradable)",
            fontsize=9, color="gray", ha="center")
    ax.plot(gammas, log_neg, label="log_neg (analytic, UB)", linewidth=2, color="C0")
    ax.scatter(er_g, er_v, color="C3", marker="s", s=55,
               label=r"$E_R^{PPT}$ (MOSEK SDP)", zorder=5)
    Q_deg = np.where(gammas <= 0.5, Q, 0)
    ax.plot(gammas, Q_deg, label=r"$Q$ (LB on $K^{\leftrightarrow}$, γ ≤ 1/2)",
            linewidth=2, color="C2", linestyle="--")
    ax.axvline(0.5, color="gray", linewidth=0.8, linestyle=":")
    ax.set_xlabel("γ (damping probability)")
    ax.set_ylabel("bits per channel use")
    ax.set_title(r"AD hierarchy: $Q \leq K^{\leftrightarrow} \leq E_R^{PPT} \leq \log\|\cdot\|_{\mathrm{PT}}$")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    # Right: log_neg / E_R^PPT ratio (tightness tracking)
    ax = axes[1]
    ratios = np.array([analytic_log_neg_amplitude_damping(g) / v if v > 1e-10 else np.nan
                       for g, v in er_pts])
    ax.plot(er_g, ratios, "o-", color="C3", markersize=7, linewidth=2,
            label=r"log_neg / $E_R^{PPT}$")
    ax.axvspan(0.5, 1.0, alpha=0.10, color="gray")
    ax.axhline(2.0, color="gray", linewidth=0.5, linestyle=":")
    ax.axvline(0.5, color="gray", linewidth=0.8, linestyle=":")
    ax.text(0.72, 1.18, "anti-degradable", fontsize=9, color="gray", ha="center")
    ax.text(0.22, 1.18, "degradable", fontsize=9, color="gray", ha="center")
    ax.set_xlabel("γ")
    ax.set_ylabel(r"log_neg / $E_R^{PPT}$")
    ax.set_title("log_neg looseness vs tighter SDP UB")
    ax.set_xlim(0, 1)
    ax.set_ylim(1.0, 2.4)
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig_dir = REPO / "docs" / "research" / "figures"
    fig.savefig(fig_dir / "AD_anti_degradable_hierarchy.png", dpi=160)
    fig.savefig(fig_dir / "AD_anti_degradable_hierarchy.pdf")
    plt.close(fig)

    print("Done.")
    print(f"  PNG: docs/research/figures/AD_anti_degradable_hierarchy.png")
    print(f"  E_R^PPT points: {len(er_pts)}")


if __name__ == "__main__":
    main()
