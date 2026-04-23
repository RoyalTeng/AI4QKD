"""n-fold composition E^n: log-negativity scaling with chain length.

Composition recursion rules (textbook):
  AD:           γ_n = 1 - (1-γ)^n
  Dephasing:    p_n = (1 - (1-2p)^n) / 2          (Z parity argument)
  Depolarizing: p_n = 1 - (1-p)^n
  Erasure:      p_n = 1 - (1-p)^n

Key structural observation:
- AD, Depolarizing, Erasure share the SAME parameter recursion p_n = 1-(1-p)^n.
- Dephasing has DIFFERENT recursion (Chebyshev-like Z parity decay).

For PPT zero-crossing as function of n:
- Depolarizing: log_neg=0 when p_n ≥ 2/3 → n ≥ log(1/3)/log(1-p)
- Dephasing:    log_neg=0 only when p_n = 1/2 (one specific n at most)
- AD/Erasure:   log_neg > 0 for all finite n if p < 1

Output:
  docs/research/figures/qubit_log_neg_n_fold.{png,pdf}
  docs/research/data/qubit_log_neg_n_fold.csv
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
    analytic_log_neg_amplitude_damping as ln_AD,
    analytic_log_neg_dephasing as ln_DP,
    analytic_log_neg_depolarizing as ln_DE,
    analytic_log_neg_erasure as ln_ER,
)


def n_fold_param(family: str, p: float, n: int) -> float:
    """Effective parameter after n-fold self-composition."""
    if family in ("AD", "depolar", "erasure"):
        return 1.0 - (1.0 - p) ** n
    if family == "dephase":
        return (1.0 - (1.0 - 2 * p) ** n) / 2.0
    raise ValueError(family)


def log_neg_n_fold(family: str, p: float, n: int) -> float:
    """log_neg of n-fold composed channel."""
    p_n = n_fold_param(family, p, n)
    if family == "AD":
        return ln_AD(p_n)
    if family == "dephase":
        return ln_DP(p_n)
    if family == "depolar":
        return ln_DE(p_n)
    if family == "erasure":
        return ln_ER(p_n)
    raise ValueError(family)


def main():
    n_values = list(range(1, 21))  # n=1..20
    p_values = [0.05, 0.10, 0.20, 0.30, 0.50]

    # CSV: (family, p, n, log_neg)
    out_csv = REPO / "docs" / "research" / "data" / "qubit_log_neg_n_fold.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["family", "param", "n", "log_neg_bits", "effective_param"])
        for family in ("AD", "dephase", "depolar", "erasure"):
            for p in p_values:
                for n in n_values:
                    p_n = n_fold_param(family, p, n)
                    ln = log_neg_n_fold(family, p, n)
                    w.writerow([family, f"{p:.2f}", n, f"{ln:.10f}", f"{p_n:.10f}"])

    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.0))
    families = [
        ("AD", "AD: $\\gamma_n = 1-(1-\\gamma)^n$", axes[0, 0]),
        ("dephase", "Dephase: $p_n = (1-(1-2p)^n)/2$", axes[0, 1]),
        ("depolar", "Depolar: $p_n = 1-(1-p)^n$ (PPT cliff)", axes[1, 0]),
        ("erasure", "Erasure: $p_n = 1-(1-p)^n$", axes[1, 1]),
    ]
    for family, title, ax in families:
        for p in p_values:
            ys = [log_neg_n_fold(family, p, n) for n in n_values]
            ax.plot(n_values, ys, marker="o", markersize=4, label=f"p={p}")
        ax.set_xlabel("chain length n")
        ax.set_ylabel("log_neg (bits)")
        ax.set_title(title)
        ax.set_xlim(0.5, 20.5)
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, alpha=0.3)
        ax.legend(loc="upper right", fontsize=8)
    fig.suptitle("Log-negativity of n-fold composed qubit channels", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig_dir = REPO / "docs" / "research" / "figures"
    fig.savefig(fig_dir / "qubit_log_neg_n_fold.png", dpi=160)
    fig.savefig(fig_dir / "qubit_log_neg_n_fold.pdf")
    plt.close(fig)

    print("Done.")
    print(f"  CSV:  docs/research/data/qubit_log_neg_n_fold.csv")
    print(f"  PNG:  docs/research/figures/qubit_log_neg_n_fold.png")
    print()
    print("Sample table (n vs log_neg, p=0.10):")
    print(f"  {'n':>3} | {'AD':>8} {'dephase':>8} {'depolar':>8} {'erasure':>8}")
    for n in [1, 2, 5, 10, 20]:
        print(f"  {n:>3} | {log_neg_n_fold('AD', 0.10, n):>8.4f} "
              f"{log_neg_n_fold('dephase', 0.10, n):>8.4f} "
              f"{log_neg_n_fold('depolar', 0.10, n):>8.4f} "
              f"{log_neg_n_fold('erasure', 0.10, n):>8.4f}")
    print()
    print("Depolarizing PPT zero crossing as function of p (smallest n with log_neg=0):")
    for p in [0.05, 0.10, 0.20, 0.30, 0.50]:
        # log_neg = 0 when p_n >= 2/3 ↔ (1-p)^n <= 1/3
        n_crit = math.ceil(math.log(1/3) / math.log(1-p))
        print(f"  p={p}: n_crit = {n_crit} (closed form: ⌈log(1/3)/log(1-p)⌉)")


if __name__ == "__main__":
    main()
