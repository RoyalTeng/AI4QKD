"""AD-specific combined plot: analytic log_neg + sparse E_R^PPT (existing data) + Pirandola.

Reuses pre-computed E_R^PPT SDP values from docs/research/data/beta_G3_log_neg_vs_pirandola.csv
to avoid re-running expensive MOSEK SDP. Adds dense analytic log_neg curve.

Output:
  docs/research/figures/AD_log_neg_vs_E_R_PPT.{png,pdf}

Reference:
  - β.G3 memo: docs/findings/beta_G3_golden_ratio_crossover_2026-04-23.md
  - log_neg(AD, η) = log₂(1+η) [SymPy verified, C1(c)+C2+C3 ✓]
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


def load_existing_er_ppt():
    """Load (eta, er_ppt_single) pairs from existing β.G3 CSV (skip blanks)."""
    csv_path = REPO / "docs" / "research" / "data" / "beta_G3_log_neg_vs_pirandola.csv"
    pts = []
    with open(csv_path) as f:
        r = csv.DictReader(f)
        for row in r:
            eta = float(row["eta_arm"])
            er = row.get("er_ppt_single_bits", "").strip()
            if er:
                pts.append((eta, float(er)))
    return sorted(pts, key=lambda x: x[0])


def main():
    # Dense analytic curves
    eta = np.linspace(1e-4, 1.0 - 1e-4, 1001)
    log_neg = np.log2(1.0 + eta)              # analytic [SYN, verified]
    pirandola = -np.log2(1.0 - eta)           # PLOB pure-loss bosonic

    # Sparse E_R^PPT (existing SDP results)
    er_pts = load_existing_er_ppt()
    er_eta = np.array([p[0] for p in er_pts])
    er_vals = np.array([p[1] for p in er_pts])

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.5))

    # Left: absolute bits
    ax = axes[0]
    ax.plot(eta, log_neg, label=r"log_neg = $\log_2(1+\eta)$ (analytic)", linewidth=2)
    ax.plot(eta, pirandola, label=r"Pirandola $-\log_2(1-\eta)$ (PLOB bosonic)", linewidth=1.5, linestyle="--", color="C3")
    ax.scatter(er_eta, er_vals, color="C2", s=40, label=r"$E_R^{PPT}$ single-arm (SDP, MOSEK)", zorder=5)

    # Mark golden ratio crossover
    phi = (1 + math.sqrt(5)) / 2
    eta_c = 1.0 / phi
    ax.axvline(eta_c, color="goldenrod", linewidth=0.8, alpha=0.6)
    ax.text(eta_c + 0.005, 3.5, r"$\eta_c = 1/\varphi$", fontsize=9, color="goldenrod")

    ax.set_xlabel("transmission η")
    ax.set_ylabel("bits")
    ax.set_title("AD channel: log_neg vs $E_R^{PPT}$ vs Pirandola (single arm)")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 4.8)
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)

    # Right: ratio plot
    ax = axes[1]
    ratio_log_neg_pir = log_neg / pirandola
    ax.plot(eta, ratio_log_neg_pir, label=r"log_neg / Pirandola", linewidth=2)
    # Sparse E_R / Pirandola
    er_pir = er_vals / (-np.log2(1 - er_eta))
    ax.scatter(er_eta, er_pir, color="C2", s=40, label=r"$E_R^{PPT}$ / Pirandola", zorder=5)

    ax.axvline(eta_c, color="goldenrod", linewidth=0.8, alpha=0.6)
    ax.axhline(1.0, color="gray", linewidth=0.5, alpha=0.5)
    ax.set_xlabel("transmission η")
    ax.set_ylabel("ratio")
    ax.set_title("Tightness ratio (vs Pirandola single-arm)")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.8)
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig_dir = REPO / "docs" / "research" / "figures"
    fig.savefig(fig_dir / "AD_log_neg_vs_E_R_PPT.png", dpi=160)
    fig.savefig(fig_dir / "AD_log_neg_vs_E_R_PPT.pdf")
    plt.close(fig)

    print("Done.")
    print(f"  PNG:  docs/research/figures/AD_log_neg_vs_E_R_PPT.png")
    print(f"  PDF:  docs/research/figures/AD_log_neg_vs_E_R_PPT.pdf")
    print()
    print(f"AD tightness summary (single-arm):")
    print(f"  E_R^PPT / Pirandola ∈ [{er_pir.min():.3f}, {er_pir.max():.3f}] over {len(er_pir)} SDP points")
    print(f"  log_neg / Pirandola at η=0.5: {log_neg[500]/pirandola[500]:.3f}")
    print(f"  log_neg / Pirandola at η=1/φ: {math.log2(1+eta_c)/(-math.log2(1-eta_c)):.3f} (=0.5 by golden-ratio identity)")


if __name__ == "__main__":
    main()
