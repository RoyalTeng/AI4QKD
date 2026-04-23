"""Mixed channel composition E_A ∘ E_B: numerical log_neg.

Composes two qubit channels (potentially different families) by Kraus
multiplication: K_AB = {K_A · K_B for K_A, K_B in respective Kraus sets},
then builds Choi state and computes log_neg via PT eigenvalues.

Selected mixed pairs:
  - AD(γ) ∘ Dephasing(p):  hybrid loss + phase noise
  - AD(γ) ∘ Depolarizing(p):  loss + isotropic noise
  - Dephasing(p) ∘ Erasure(q):  phase noise + erasure (note: erasure changes dim_B!)

For erasure compositions: dim_B = 3 after erasure step. We keep dim_B = 2 by
restricting to channels that keep qubit dimension (so erasure mixed cases skipped).

Output:
  docs/research/figures/qubit_log_neg_mixed_composition.{png,pdf}
  docs/research/data/qubit_log_neg_mixed_composition.csv
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
    choi_state_from_kraus,
    kraus_amplitude_damping_qubit,
    kraus_dephasing_qubit,
    kraus_depolarizing_qubit,
)


def compose_kraus(K_A_list, K_B_list):
    """Composed channel E_A ∘ E_B has Kraus {K_A · K_B}."""
    return [K_A @ K_B for K_A in K_A_list for K_B in K_B_list]


def log_neg_choi_qubit(kraus_ops):
    """Compute log_neg of Choi state of qubit→qubit channel."""
    rho = choi_state_from_kraus(kraus_ops, dim_A=2)
    d = 2
    rho_TB = np.zeros((4, 4), dtype=complex)
    for i in range(d):
        for j in range(d):
            for k in range(d):
                for ll in range(d):
                    rho_TB[i*d+ll, k*d+j] = rho[i*d+j, k*d+ll]
    eigs = np.linalg.eigvalsh(rho_TB)
    tn = float(np.sum(np.abs(eigs)))
    return math.log2(tn) if tn > 1.0 else 0.0


def main():
    ts = np.linspace(0.001, 0.999, 200)

    # Pair 1: AD ∘ Dephasing — sweep both params on a few diagonals
    # Diagonals: equal noise, AD-heavy, dephasing-heavy

    diagonals = [
        ("equal", lambda t: (t, t)),                # γ = p
        ("AD-heavy", lambda t: (t, t * 0.3)),       # γ dominant
        ("dephase-heavy", lambda t: (t * 0.3, t)),  # p dominant
    ]

    results = {}  # (pair_name, diag) → list of (t, log_neg, gamma, p)
    for diag_name, diag_fn in diagonals:
        # AD ∘ Dephasing
        key = ("AD_x_DP", diag_name)
        results[key] = []
        for t in ts:
            g, p = diag_fn(t)
            if not (0 < g < 1 and 0 < p < 1):
                continue
            kraus = compose_kraus(kraus_amplitude_damping_qubit(g), kraus_dephasing_qubit(p))
            ln = log_neg_choi_qubit(kraus)
            results[key].append((t, ln, g, p))
        # AD ∘ Depolarizing
        key = ("AD_x_DE", diag_name)
        results[key] = []
        for t in ts:
            g, p = diag_fn(t)
            if not (0 < g < 1 and 0 < p < 1):
                continue
            kraus = compose_kraus(kraus_amplitude_damping_qubit(g), kraus_depolarizing_qubit(p))
            ln = log_neg_choi_qubit(kraus)
            results[key].append((t, ln, g, p))
        # Dephasing ∘ Depolarizing
        key = ("DP_x_DE", diag_name)
        results[key] = []
        for t in ts:
            g, p = diag_fn(t)
            if not (0 < g < 1 and 0 < p < 1):
                continue
            kraus = compose_kraus(kraus_dephasing_qubit(g), kraus_depolarizing_qubit(p))
            ln = log_neg_choi_qubit(kraus)
            results[key].append((t, ln, g, p))

    out_csv = REPO / "docs" / "research" / "data" / "qubit_log_neg_mixed_composition.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pair", "diagonal", "t", "param_A", "param_B", "log_neg_bits"])
        for (pair, diag), rows in results.items():
            for t, ln, a, b in rows:
                w.writerow([pair, diag, f"{t:.4f}", f"{a:.4f}", f"{b:.4f}", f"{ln:.10f}"])

    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.5))
    pair_titles = [
        ("AD_x_DP", "AD ∘ Dephasing"),
        ("AD_x_DE", "AD ∘ Depolarizing"),
        ("DP_x_DE", "Dephasing ∘ Depolarizing"),
    ]
    colors = {"equal": "C0", "AD-heavy": "C1", "dephase-heavy": "C2"}
    for ax, (pair, title) in zip(axes, pair_titles):
        for diag in ["equal", "AD-heavy", "dephase-heavy"]:
            key = (pair, diag)
            xs = [r[0] for r in results[key]]
            ys = [r[1] for r in results[key]]
            ax.plot(xs, ys, label=diag, color=colors[diag], linewidth=2)
        ax.set_xlabel("noise scale t")
        ax.set_ylabel("log_neg (bits)")
        ax.set_title(title)
        ax.set_xlim(0, 1)
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, alpha=0.3)
        ax.legend(loc="upper right", fontsize=8)
    fig.suptitle("Mixed channel composition: log-negativity (numerical PT)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig_dir = REPO / "docs" / "research" / "figures"
    fig.savefig(fig_dir / "qubit_log_neg_mixed_composition.png", dpi=160)
    fig.savefig(fig_dir / "qubit_log_neg_mixed_composition.pdf")
    plt.close(fig)

    print("Done.")
    print(f"  CSV:  docs/research/data/qubit_log_neg_mixed_composition.csv")
    print(f"  PNG:  docs/research/figures/qubit_log_neg_mixed_composition.png")
    print()
    print("Sample (equal diagonal, t=0.30):")
    for pair, title in pair_titles:
        rows = results[(pair, "equal")]
        # Find row with t closest to 0.30
        row = min(rows, key=lambda r: abs(r[0] - 0.30))
        print(f"  {title:30}: t={row[0]:.3f}, params=({row[2]:.3f}, {row[3]:.3f}), log_neg={row[1]:.4f}")


if __name__ == "__main__":
    main()
