"""Generate β.G3 visualization from sweep CSV."""
from __future__ import annotations

import csv
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    csv_path = os.path.expanduser("~/Desktop/ai4qkd (1)/AI4QKD/docs/research/data/beta_G3_post_BSM_sweep.csv")
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    eta = [float(r["eta_arm"]) for r in rows]
    beta_bound = [float(r["sum_p_times_LN"]) for r in rows]
    pirandola = [float(r["Pirandola"]) for r in rows]
    ratio = [float(r["ratio_beta_per_Pir"]) for r in rows]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: log-log bounds vs eta
    axes[0].loglog(eta, beta_bound, "o-", label=r"$\beta$ per-round bound = $\sum_c p_c \cdot LN(\rho_{AB|c})$", linewidth=2)
    axes[0].loglog(eta, pirandola, "s--", label=r"Pirandola 2019 trusted-relay: $-\log_2(1-\eta)$", linewidth=2)
    axes[0].set_xlabel(r"$\eta_{\rm arm}$ (per-arm transmittance)", fontsize=11)
    axes[0].set_ylabel(r"upper bound (bits/round)", fontsize=11)
    axes[0].set_title(r"$\beta$ path vs Pirandola (qubit amp-damp post-BSM)", fontsize=12)
    axes[0].legend(loc="lower right", fontsize=10)
    axes[0].grid(True, which="both", alpha=0.3)

    # Right: ratio plot
    axes[1].semilogx(eta, ratio, "o-", linewidth=2, color="darkred")
    axes[1].axhline(y=1.0, color="black", linestyle=":", alpha=0.5, label="ratio = 1 (same as Pirandola)")
    axes[1].axhline(y=0.19, color="blue", linestyle="--", alpha=0.5, label=r"plateau $\approx 0.19\times$")
    axes[1].set_xlabel(r"$\eta_{\rm arm}$", fontsize=11)
    axes[1].set_ylabel(r"$\beta$ bound / Pirandola bound", fontsize=11)
    axes[1].set_title(r"Tightness ratio (lower = tighter $\beta$)", fontsize=12)
    axes[1].legend(loc="best", fontsize=10)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim(0, 0.5)

    plt.tight_layout()

    fig_dir = os.path.expanduser("~/Desktop/ai4qkd (1)/AI4QKD/docs/research/figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig_path_png = os.path.join(fig_dir, "beta_G3_post_BSM_vs_pirandola.png")
    fig_path_pdf = os.path.join(fig_dir, "beta_G3_post_BSM_vs_pirandola.pdf")
    plt.savefig(fig_path_png, dpi=150, bbox_inches="tight")
    plt.savefig(fig_path_pdf, bbox_inches="tight")
    print(f"Saved: {fig_path_png}")
    print(f"Saved: {fig_path_pdf}")


if __name__ == "__main__":
    main()
