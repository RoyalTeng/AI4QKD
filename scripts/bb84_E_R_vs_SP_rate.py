"""BB84/six-state: E_R (corrected analytic) vs SP achievable rate vs log_neg.

After bug fix in e_r_depolarizing_analytic, E_R = 1 - h(F) for d=2 isotropic
is the **true** E_R (= E_R^PPT for 2⊗2 by Horodecki 96).

Maps QBER → depolarizing with p_depol = 4·QBER/3 (qkdx/protocols/bb84.py).
Three curves on one plot:
  - log_neg (analytic, loosest UB)
  - E_R (corrected, tight UB = E_R^PPT)
  - SP_BB84 / SP_six-state (achievable LB)

Output:
  docs/research/figures/bb84_E_R_vs_SP_rate.{png,pdf}
  docs/research/data/bb84_E_R_vs_SP_rate.csv
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
    analytic_log_neg_depolarizing, e_r_depolarizing_analytic,
)


def h2(p):
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def bb84_sp(qber):
    return max(0.0, 1.0 - 2.0 * h2(qber))


def sixstate_sp(qber):
    return max(0.0, 1.0 - h2(qber) - qber * math.log2(3.0))


def main():
    qbers = np.linspace(0.0, 0.20, 401)
    log_neg = np.array([analytic_log_neg_depolarizing(4*q/3) if 4*q/3 <= 1 else 0
                       for q in qbers])
    e_r = np.array([e_r_depolarizing_analytic(min(4*q/3, 1.0)) for q in qbers])
    bb_sp = np.array([bb84_sp(q) for q in qbers])
    ss_sp = np.array([sixstate_sp(q) for q in qbers])

    out_csv = REPO / "docs" / "research" / "data" / "bb84_E_R_vs_SP_rate.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["qber", "p_depol", "log_neg", "E_R_corrected", "SP_BB84", "SP_6state",
                    "ratio_ER_BB", "ratio_ER_6st"])
        for q, ln, er, bb, ss in zip(qbers, log_neg, e_r, bb_sp, ss_sp):
            r_bb = er / bb if bb > 1e-6 else float('inf')
            r_ss = er / ss if ss > 1e-6 else float('inf')
            w.writerow([f"{q:.5f}", f"{4*q/3:.5f}", f"{ln:.10f}", f"{er:.10f}",
                        f"{bb:.10f}", f"{ss:.10f}",
                        f"{r_bb:.4f}" if not math.isinf(r_bb) else "inf",
                        f"{r_ss:.4f}" if not math.isinf(r_ss) else "inf"])

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.5))

    ax = axes[0]
    ax.plot(qbers * 100, log_neg, label="log_neg (analytic, loosest UB)", linewidth=2, color="C0", alpha=0.7)
    ax.plot(qbers * 100, e_r, label=r"$E_R$ (corrected = $E_R^{PPT}$, tight UB)", linewidth=2.5, color="C3")
    ax.plot(qbers * 100, bb_sp, label="BB84 SP (achievable LB)", linewidth=2, color="C1", linestyle="--")
    ax.plot(qbers * 100, ss_sp, label="six-state SP (achievable LB)", linewidth=2, color="C2", linestyle=":")
    ax.fill_between(qbers * 100, bb_sp, e_r, where=(e_r > bb_sp), alpha=0.15, color="C3", label="BB84 UB-LB gap")
    ax.axvline(11.0, color="C1", linewidth=0.5, alpha=0.5)
    ax.axvline(12.62, color="C2", linewidth=0.5, alpha=0.5)
    ax.set_xlabel("QBER (%)")
    ax.set_ylabel("bits / channel use")
    ax.set_title("MS-EB BB84/six-state: $E_R$ tightens log_neg → SP")
    ax.set_xlim(0, 20)
    ax.set_ylim(-0.02, 1.02)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    bb_safe = np.where(bb_sp > 1e-6, bb_sp, np.nan)
    ss_safe = np.where(ss_sp > 1e-6, ss_sp, np.nan)
    ax.plot(qbers * 100, log_neg / bb_safe, label="log_neg / SP_BB84", linewidth=1.5, alpha=0.6, color="C0")
    ax.plot(qbers * 100, e_r / bb_safe, label=r"$E_R$ / SP_BB84 (tightest UB/LB)", linewidth=2, color="C3")
    ax.plot(qbers * 100, e_r / ss_safe, label=r"$E_R$ / SP_six-state", linewidth=2, color="C2", linestyle="--")
    ax.axhline(1.0, color="gray", linewidth=0.5, alpha=0.5)
    ax.set_xlabel("QBER (%)")
    ax.set_ylabel("UB / LB ratio")
    ax.set_title("Tightest known UB / SP achievable LB")
    ax.set_xlim(0, 11)
    ax.set_ylim(0.5, 5.0)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig_dir = REPO / "docs" / "research" / "figures"
    fig.savefig(fig_dir / "bb84_E_R_vs_SP_rate.png", dpi=160)
    fig.savefig(fig_dir / "bb84_E_R_vs_SP_rate.pdf")
    plt.close(fig)

    print("Done.")
    print(f"  CSV:  docs/research/data/bb84_E_R_vs_SP_rate.csv")
    print(f"  PNG:  docs/research/figures/bb84_E_R_vs_SP_rate.png")
    print()
    print("E_R (corrected, true UB) vs SP rates:")
    print(f"  {'QBER':>5} {'p':>6} {'log_neg':>9} {'E_R':>9} {'SP_BB':>9} {'SP_6st':>9} {'E_R/BB':>8} {'E_R/6st':>8}")
    for q in [0.00, 0.01, 0.03, 0.05, 0.08, 0.11, 0.1262, 0.15, 0.20]:
        p = 4*q/3
        if p > 1: p = 1
        ln = analytic_log_neg_depolarizing(p)
        er = e_r_depolarizing_analytic(p)
        bb = bb84_sp(q)
        ss = sixstate_sp(q)
        r_bb = er/bb if bb > 1e-6 else float('inf')
        r_ss = er/ss if ss > 1e-6 else float('inf')
        print(f"  {q*100:5.2f}% {p:6.4f} {ln:9.4f} {er:9.4f} {bb:9.4f} {ss:9.4f} "
              f"{r_bb:8.3f} {r_ss:8.3f}")


if __name__ == "__main__":
    main()
