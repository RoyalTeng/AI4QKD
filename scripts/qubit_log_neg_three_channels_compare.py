"""Comparison plot: log-negativity of Choi state for three qubit channels.

AD / dephasing / depolarizing — analytic formulas verified by SymPy + numerical SDP.

Output:
  docs/research/figures/qubit_log_neg_three_channels.png
  docs/research/figures/qubit_log_neg_three_channels.pdf
  docs/research/data/qubit_log_neg_three_channels.csv

References:
  - docs/findings/qubit_channel_log_neg_comparison_2026-04-23.md
  - qkdx/numerics/upper_bound.py:analytic_log_neg_*
"""
from __future__ import annotations

import csv
import math
import os
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
    analytic_log_neg_dephasing,
    analytic_log_neg_depolarizing,
    analytic_log_neg_erasure,
)


def main():
    ts = np.linspace(0.0, 1.0, 1001)
    ad = np.array([analytic_log_neg_amplitude_damping(g) for g in ts])
    dp = np.array([analytic_log_neg_dephasing(p) for p in ts])
    de = np.array([analytic_log_neg_depolarizing(p) for p in ts])
    er = np.array([analytic_log_neg_erasure(p) for p in ts])

    out_data = REPO / "docs" / "research" / "data" / "qubit_log_neg_three_channels.csv"
    out_data.parent.mkdir(parents=True, exist_ok=True)
    with open(out_data, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["noise_param", "AD_log_neg_bits", "dephase_log_neg_bits",
                    "depol_log_neg_bits", "erasure_log_neg_bits"])
        for t, a, d, de_v, er_v in zip(ts, ad, dp, de, er):
            w.writerow([f"{t:.4f}", f"{a:.10f}", f"{d:.10f}", f"{de_v:.10f}", f"{er_v:.10f}"])

    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.plot(ts, ad, label=r"AD: $\log_2(2-\gamma)$", linewidth=2.0)
    ax.plot(ts, dp, label=r"Dephase: $\log_2(1+|1-2p|)$", linewidth=2.0, linestyle="--")
    ax.plot(ts, de, label=r"Depol: $\log_2(2-3p/2)$", linewidth=2.0, linestyle=":")
    ax.plot(ts, er, label=r"Erasure: $\log_2(2-p)$", linewidth=2.0, linestyle="-.")

    # PPT thresholds
    ax.axvline(2.0/3.0, color="gray", linewidth=0.8, alpha=0.5)
    ax.text(2.0/3.0 + 0.005, 0.05, r"depol PPT $p=2/3$", fontsize=8, color="gray")
    ax.axvline(0.5, color="gray", linewidth=0.8, alpha=0.5)
    ax.text(0.5 + 0.005, 0.95, r"dephase $p=1/2$", fontsize=8, color="gray")

    ax.set_xlabel("Noise parameter (γ for AD, p for dephase/depol)")
    ax.set_ylabel(r"$\log_2 \|\rho_{\rm Choi}^{T_B}\|_1$  (bits)")
    ax.set_title("Log-negativity of qubit Choi states (analytic formulas, [SYN])")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower left", fontsize=9)
    fig.tight_layout()

    fig_dir = REPO / "docs" / "research" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(fig_dir / "qubit_log_neg_three_channels.png", dpi=160)
    fig.savefig(fig_dir / "qubit_log_neg_three_channels.pdf")
    plt.close(fig)

    print("Done.")
    print(f"  CSV:  {out_data.relative_to(REPO)}")
    print(f"  PNG:  {(fig_dir / 'qubit_log_neg_three_channels.png').relative_to(REPO)}")
    print(f"  PDF:  {(fig_dir / 'qubit_log_neg_three_channels.pdf').relative_to(REPO)}")
    print()
    print("Sample values:")
    for t in [0.0, 0.1, 0.3, 0.5, 2/3, 0.9, 1.0]:
        print(f"  noise={t:.4f}: AD={analytic_log_neg_amplitude_damping(t):.4f}, "
              f"dephase={analytic_log_neg_dephasing(t):.4f}, "
              f"depol={analytic_log_neg_depolarizing(t):.4f}, "
              f"erasure={analytic_log_neg_erasure(t):.4f}")


if __name__ == "__main__":
    main()
