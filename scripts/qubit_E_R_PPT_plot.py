"""Render 4-channel E_R^PPT comparison plot from saved CSV.

Separate from compute script to allow re-rendering without re-running SDP.
Erasure row intentionally absent (OOM in current env; dim_B=3 too large).
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


def main():
    csv_path = REPO / "docs" / "research" / "data" / "qubit_E_R_PPT_SDP_all_4.csv"
    rows = {"AD": [], "Dephasing": [], "Depolarizing": [], "Erasure": []}
    with open(csv_path) as f:
        for r in csv.DictReader(f):
            fam = r["family"]
            p = float(r["param"])
            er = float(r["E_R_PPT_SDP"])
            ln = float(r["log_neg_analytic"])
            kd_str = r["K_D_or_E_R_analytic"]
            kd = float(kd_str) if kd_str.strip() else None
            rows[fam].append((p, er, ln, kd))

    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.5))

    panels = [
        ("AD", "Amplitude Damping", "γ", axes[0]),
        ("Dephasing", "Dephasing", "p", axes[1]),
        ("Depolarizing", "Depolarizing", "p", axes[2]),
    ]
    for fam, title, xlab, ax in panels:
        data = sorted(rows[fam], key=lambda r: r[0])
        if not data:
            continue
        xs = [r[0] for r in data]
        ax.plot(xs, [r[2] for r in data], "o-", label="log_neg (analytic)", markersize=7, linewidth=2)
        ax.plot(xs, [r[1] for r in data], "s--", label=r"$E_R^{PPT}$ (MOSEK SDP)", markersize=6, linewidth=2)
        if fam == "Dephasing":
            ax.plot(xs, [r[3] for r in data], "^:", label=r"$K_D$ (PLOB Eq.39)", markersize=6, linewidth=2)
        elif fam == "Depolarizing":
            ax.plot(xs, [r[3] for r in data], "^:", label=r"$E_R$ (Horodecki 99)", markersize=6, linewidth=2)
        ax.set_xlabel(f"{xlab} (noise)")
        ax.set_ylabel("bits")
        ax.set_title(title)
        ax.legend(fontsize=9, loc="upper right")
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.05, 1.05)

    fig.suptitle(r"Upper-bound hierarchy (MOSEK SDP): log_neg ≥ $E_R^{PPT}$ ≥ $K_D / E_R$ (analytic)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig_dir = REPO / "docs" / "research" / "figures"
    fig.savefig(fig_dir / "qubit_E_R_PPT_all_4.png", dpi=160)
    fig.savefig(fig_dir / "qubit_E_R_PPT_all_4.pdf")
    plt.close(fig)

    print("Done.")
    print(f"  PNG:  docs/research/figures/qubit_E_R_PPT_all_4.png")
    print(f"  PDF:  docs/research/figures/qubit_E_R_PPT_all_4.pdf")

    # Print ratio summary
    print()
    print("E_R^PPT / log_neg ratio by channel (tightness of PPT-SDP vs PPT-relaxed analytic):")
    for fam in ["AD", "Dephasing", "Depolarizing"]:
        data = sorted(rows[fam], key=lambda r: r[0])
        ratios = [r[1] / r[2] if r[2] > 0 else 0 for r in data]
        print(f"  {fam:14}: ratios = {[f'{x:.3f}' for x in ratios]}")


if __name__ == "__main__":
    main()
