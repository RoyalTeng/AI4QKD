"""log_neg of MS-EB protocols' equivalent channel vs achievable key rates.

Maps each protocol (BB84, six-state) to its symmetric depolarizing equivalent
channel with parameter p = 4·QBER/3 (per qkdx/protocols/bb84.py:bb84_channel).
Then compares:
  - log_neg of that channel (upper bound, our analytic formula)
  - Shor-Preskill SP rate: 1 - 2h(QBER) (achievable, BB84)
  - Six-state SP rate: 1 - h(QBER) - QBER·log₂(3) (Lo 2001 analytic)

Note: log_neg is an UPPER bound; SP rate is achievable LOWER bound. Comparing
both shows how much "room" the PPT bound leaves above the operational rate.

Output:
  docs/research/figures/log_neg_vs_msEB_rate.{png,pdf}
  docs/research/data/log_neg_vs_msEB_rate.csv
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

from qkdx.numerics.upper_bound import analytic_log_neg_depolarizing


def h2(p):
    """Binary entropy in bits."""
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def bb84_sp_rate(qber):
    """Shor-Preskill: r = max(0, 1 - 2 h(qber))."""
    return max(0.0, 1.0 - 2.0 * h2(qber))


def sixstate_sp_rate(qber):
    """Lo 2001: r = max(0, 1 - h(qber) - qber·log₂(3)).

    Six-state protocol exploits 3 mutually unbiased bases for tighter PA.
    """
    return max(0.0, 1.0 - h2(qber) - qber * math.log2(3.0))


def log_neg_at_qber(qber):
    """log_neg of equivalent depolarizing channel with p = 4·QBER/3.

    Per qkdx/protocols/bb84.py:bb84_channel — BB84 modeled as symmetric depol.
    """
    p = 4.0 * qber / 3.0
    if p > 1.0:
        return 0.0
    return analytic_log_neg_depolarizing(p)


def main():
    qbers = np.linspace(0.0, 0.20, 401)  # QBER 0 → 20%
    log_neg = np.array([log_neg_at_qber(q) for q in qbers])
    bb84_sp = np.array([bb84_sp_rate(q) for q in qbers])
    sixstate_sp = np.array([sixstate_sp_rate(q) for q in qbers])

    out_csv = REPO / "docs" / "research" / "data" / "log_neg_vs_msEB_rate.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "qber", "p_depol", "log_neg_bits", "bb84_SP_bits", "sixstate_SP_bits",
            "gap_bb84", "gap_sixstate",
        ])
        for q, ln, bb, ss in zip(qbers, log_neg, bb84_sp, sixstate_sp):
            w.writerow([f"{q:.5f}", f"{4*q/3:.5f}", f"{ln:.10f}", f"{bb:.10f}",
                        f"{ss:.10f}", f"{ln-bb:.10f}", f"{ln-ss:.10f}"])

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.5))

    # Left: absolute rates
    ax = axes[0]
    ax.plot(qbers * 100, log_neg, label="log_neg (PPT upper bound, analytic)", linewidth=2, color="C0")
    ax.plot(qbers * 100, bb84_sp, label="BB84 SP rate (achievable)", linewidth=2, color="C1", linestyle="--")
    ax.plot(qbers * 100, sixstate_sp, label="Six-state SP rate (achievable)", linewidth=2, color="C2", linestyle=":")
    ax.fill_between(qbers * 100, bb84_sp, log_neg, where=(log_neg > bb84_sp), alpha=0.10, color="C0", label="BB84 PPT excess")
    # BB84 threshold ~ 11%, six-state ~ 12.62%
    ax.axvline(11.0, color="C1", linewidth=0.5, alpha=0.5)
    ax.axvline(12.62, color="C2", linewidth=0.5, alpha=0.5)
    ax.set_xlabel("QBER (%)")
    ax.set_ylabel("bits / channel use")
    ax.set_title("MS-EB BB84/six-state: log_neg upper vs SP achievable")
    ax.set_xlim(0, 20)
    ax.set_ylim(-0.02, 1.02)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    # Right: ratio plot
    ax = axes[1]
    bb_safe = np.where(bb84_sp > 1e-6, bb84_sp, np.nan)
    ss_safe = np.where(sixstate_sp > 1e-6, sixstate_sp, np.nan)
    ax.plot(qbers * 100, log_neg / bb_safe, label="log_neg / SP_BB84", linewidth=2, color="C1")
    ax.plot(qbers * 100, log_neg / ss_safe, label="log_neg / SP_six-state", linewidth=2, color="C2", linestyle="--")
    ax.axhline(1.0, color="gray", linewidth=0.5, alpha=0.5)
    ax.set_xlabel("QBER (%)")
    ax.set_ylabel("ratio")
    ax.set_title("PPT-relaxed upper bound looseness vs achievable SP rate")
    ax.set_xlim(0, 11)  # restrict to where SP > 0
    ax.set_ylim(0.5, 8.0)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig_dir = REPO / "docs" / "research" / "figures"
    fig.savefig(fig_dir / "log_neg_vs_msEB_rate.png", dpi=160)
    fig.savefig(fig_dir / "log_neg_vs_msEB_rate.pdf")
    plt.close(fig)

    print("Done.")
    print(f"  CSV:  docs/research/data/log_neg_vs_msEB_rate.csv")
    print(f"  PNG:  docs/research/figures/log_neg_vs_msEB_rate.png")
    print()
    print("Key data points:")
    print(f"  {'QBER':>6} {'p_depol':>8} {'log_neg':>9} {'SP_BB84':>9} {'SP_6st':>9} {'ratio_BB84':>11} {'ratio_6st':>11}")
    for q in [0.00, 0.01, 0.03, 0.05, 0.08, 0.11, 0.1262, 0.15, 0.20]:
        ln = log_neg_at_qber(q)
        bb = bb84_sp_rate(q)
        ss = sixstate_sp_rate(q)
        ratio_bb = ln / bb if bb > 1e-6 else float('inf')
        ratio_ss = ln / ss if ss > 1e-6 else float('inf')
        print(f"  {q*100:5.2f}% {4*q/3:8.4f} {ln:9.4f} {bb:9.4f} {ss:9.4f} "
              f"{ratio_bb:11.3f} {ratio_ss:11.3f}")


if __name__ == "__main__":
    main()
