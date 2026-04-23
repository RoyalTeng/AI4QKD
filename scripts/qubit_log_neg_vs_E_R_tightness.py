"""Tightness comparison: log_neg (PPT-relaxed) vs E_R / K_D (true 2-way capacity).

For qubit dephasing and depolarizing channels both have analytic closed forms
for K_D (PLOB Eq.39 / Horodecki 1999), so we can quantify the PPT-relaxation gap.

Inequality chain (Plenio 2005): log_neg ≥ E_R ≥ K_D.

Output:
  docs/research/figures/qubit_log_neg_vs_K_D_tightness.{png,pdf}
  docs/research/data/qubit_log_neg_vs_K_D_tightness.csv

Reference:
  - PLOB 2017 Nat. Commun. 8:15043 (dephasing K_D = 1 - h(p))
  - Horodecki et al. 1999 (isotropic E_R)
  - docs/findings/qubit_channel_log_neg_comparison_2026-04-23.md
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
    analytic_log_neg_dephasing,
    analytic_log_neg_depolarizing,
    analytic_log_neg_erasure,
    e_r_depolarizing_analytic,
)
from qkdx.numerics.e_r_upper import e_r_dephasing, e_r_erasure


def main():
    ts = np.linspace(0.0, 1.0, 1001)
    log_neg_dp = np.array([analytic_log_neg_dephasing(p) for p in ts])
    K_D_dp = np.array([e_r_dephasing(p) for p in ts])  # PLOB Eq.39: 1 - h(p)
    log_neg_de = np.array([analytic_log_neg_depolarizing(p) for p in ts])
    E_R_de = np.array([e_r_depolarizing_analytic(p) for p in ts])  # Horodecki 99
    log_neg_er = np.array([analytic_log_neg_erasure(p) for p in ts])
    K_D_er = np.array([e_r_erasure(p) for p in ts])  # PLOB Eq.43: 1 - p

    out_csv = REPO / "docs" / "research" / "data" / "qubit_log_neg_vs_K_D_tightness.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "noise_param", "dephase_log_neg", "dephase_K_D_PLOB",
            "dephase_gap_bits", "depol_log_neg", "depol_E_R", "depol_gap_bits",
            "erasure_log_neg", "erasure_K_D_PLOB", "erasure_gap_bits",
        ])
        for t, ln_dp, kd_dp, ln_de, er_de, ln_er, kd_er in zip(
            ts, log_neg_dp, K_D_dp, log_neg_de, E_R_de, log_neg_er, K_D_er
        ):
            w.writerow([
                f"{t:.4f}", f"{ln_dp:.10f}", f"{kd_dp:.10f}", f"{ln_dp - kd_dp:.10f}",
                f"{ln_de:.10f}", f"{er_de:.10f}", f"{ln_de - er_de:.10f}",
                f"{ln_er:.10f}", f"{kd_er:.10f}", f"{ln_er - kd_er:.10f}",
            ])

    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.5))

    # Dephasing
    ax = axes[0]
    ax.plot(ts, log_neg_dp, label=r"log_neg = $\log_2(1+|1-2p|)$", linewidth=2)
    ax.plot(ts, K_D_dp, label=r"$K_D$ (PLOB Eq.39) = $1 - h(p)$", linewidth=2, linestyle="--")
    gap_dp = log_neg_dp - K_D_dp
    ax.fill_between(ts, K_D_dp, log_neg_dp, alpha=0.15, label="PPT relaxation gap")
    ax.set_xlabel("dephasing prob p")
    ax.set_ylabel("bits / channel use")
    ax.set_title("Qubit Dephasing: log_neg vs $K_D$ (PLOB exact)")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc="upper center", fontsize=8)
    ax.grid(True, alpha=0.3)

    # Depolarizing
    ax = axes[1]
    ax.plot(ts, log_neg_de, label=r"log_neg = $\log_2(2-3p/2)$", linewidth=2)
    ax.plot(ts, E_R_de, label=r"$E_R$ (Horodecki 99) for isotropic", linewidth=2, linestyle="--")
    ax.fill_between(ts, E_R_de, log_neg_de, alpha=0.15, label="PPT relaxation gap")
    ax.axvline(2.0/3.0, color="gray", linewidth=0.8, alpha=0.5)
    ax.set_xlabel("depolarizing param p")
    ax.set_ylabel("bits / channel use")
    ax.set_title("Qubit Depolarizing: log_neg vs $E_R$ (analytic)")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    # Erasure
    ax = axes[2]
    ax.plot(ts, log_neg_er, label=r"log_neg = $\log_2(2-p)$", linewidth=2)
    ax.plot(ts, K_D_er, label=r"$K_D$ (PLOB Eq.43) = $1 - p$", linewidth=2, linestyle="--")
    ax.fill_between(ts, K_D_er, log_neg_er, alpha=0.15, label="PPT relaxation gap")
    ax.set_xlabel("erasure prob p")
    ax.set_ylabel("bits / channel use")
    ax.set_title("Qubit Erasure: log_neg vs $K_D$ (PLOB exact)")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig_dir = REPO / "docs" / "research" / "figures"
    fig.savefig(fig_dir / "qubit_log_neg_vs_K_D_tightness.png", dpi=160)
    fig.savefig(fig_dir / "qubit_log_neg_vs_K_D_tightness.pdf")
    plt.close(fig)

    print("Done.")
    print(f"  CSV:  {out_csv.relative_to(REPO)}")
    print(f"  PNG:  docs/research/figures/qubit_log_neg_vs_K_D_tightness.png")
    print(f"  PDF:  docs/research/figures/qubit_log_neg_vs_K_D_tightness.pdf")
    print()
    print("Tightness gap samples (log_neg − K_D / E_R):")
    print(f"  {'p':>6} {'dp_ln':>10} {'dp_KD':>10} {'gap':>8} {'de_ln':>10} {'de_ER':>10} {'gap':>8} {'er_ln':>10} {'er_KD':>10} {'gap':>8}")
    for p in [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 2/3, 0.80]:
        ln_dp = analytic_log_neg_dephasing(p)
        kd_dp = e_r_dephasing(p)
        ln_de = analytic_log_neg_depolarizing(p)
        er_de = e_r_depolarizing_analytic(p)
        ln_er = analytic_log_neg_erasure(p)
        kd_er = e_r_erasure(p)
        print(f"  {p:6.4f} {ln_dp:10.4f} {kd_dp:10.4f} {ln_dp-kd_dp:8.4f} {ln_de:10.4f} {er_de:10.4f} {ln_de-er_de:8.4f} {ln_er:10.4f} {kd_er:10.4f} {ln_er-kd_er:8.4f}")


if __name__ == "__main__":
    main()
