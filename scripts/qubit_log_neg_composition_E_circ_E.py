"""log-negativity of composed qubit channels E∘E (one transmission through 2 sequential arms).

Composition rules (textbook, well-known):
  AD(γ) ∘ AD(γ):           single AD with γ_eff = 2γ - γ²
  Dephasing(p) ∘ Dephasing(p):  single dephasing with p_eff = 2p(1-p)
  Depolarizing(p) ∘ Depolarizing(p): single depolarizing with p_eff = 2p - p²
  Erasure(p) ∘ Erasure(p):  single erasure with p_eff = 2p - p²

Output:
  docs/research/figures/qubit_log_neg_E_circ_E.{png,pdf}
  docs/research/data/qubit_log_neg_E_circ_E.csv

Key structural finding (this script): AD∘AD and Erasure∘Erasure give the
SAME log_neg formula log₂(1 + (1-p)²), because both have effective parameter
p_eff = 2p − p² and same closed form 2 − p_eff = 1 + (1-p)².
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


def main():
    ts = np.linspace(0.0, 1.0, 1001)

    # Single arm
    ad_1 = np.array([ln_AD(p) for p in ts])
    dp_1 = np.array([ln_DP(p) for p in ts])
    de_1 = np.array([ln_DE(p) for p in ts])
    er_1 = np.array([ln_ER(p) for p in ts])

    # Composed E∘E
    ad_2 = np.array([ln_AD(2*p - p**2) for p in ts])
    dp_2 = np.array([ln_DP(2*p*(1-p)) for p in ts])
    de_2 = np.array([ln_DE(2*p - p**2) for p in ts])
    er_2 = np.array([ln_ER(2*p - p**2) for p in ts])

    out_csv = REPO / "docs" / "research" / "data" / "qubit_log_neg_E_circ_E.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "noise_param", "AD_1arm", "AD_composed", "DP_1arm", "DP_composed",
            "DE_1arm", "DE_composed", "ER_1arm", "ER_composed",
        ])
        for t, a1, a2, d1, d2, de1, de2, e1, e2 in zip(ts, ad_1, ad_2, dp_1, dp_2, de_1, de_2, er_1, er_2):
            w.writerow([f"{t:.4f}", f"{a1:.10f}", f"{a2:.10f}", f"{d1:.10f}", f"{d2:.10f}",
                        f"{de1:.10f}", f"{de2:.10f}", f"{e1:.10f}", f"{e2:.10f}"])

    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.0))

    pairs = [
        ("AD: $\\log_2(2-\\gamma)$", "AD∘AD: $\\log_2(1+(1-\\gamma)^2)$", ad_1, ad_2, axes[0, 0]),
        ("Dephasing", "Dephasing∘Dephasing", dp_1, dp_2, axes[0, 1]),
        ("Depolarizing", "Depolarizing∘Depolarizing", de_1, de_2, axes[1, 0]),
        ("Erasure: $\\log_2(2-p)$", "Erasure∘Erasure: $\\log_2(1+(1-p)^2)$", er_1, er_2, axes[1, 1]),
    ]
    for label1, label2, y1, y2, ax in pairs:
        ax.plot(ts, y1, label=label1, linewidth=2)
        ax.plot(ts, y2, label=label2, linewidth=2, linestyle="--")
        ax.fill_between(ts, y2, y1, alpha=0.15, label="composition gap")
        ax.set_xlabel("noise param")
        ax.set_ylabel("log_neg (bits)")
        ax.set_xlim(0, 1)
        ax.set_ylim(-0.05, 1.05)
        ax.legend(loc="upper right", fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_title(label2.split(":")[0])

    fig.suptitle(r"Single-arm vs composed $E \circ E$ log-negativity (qubit channels)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig_dir = REPO / "docs" / "research" / "figures"
    fig.savefig(fig_dir / "qubit_log_neg_E_circ_E.png", dpi=160)
    fig.savefig(fig_dir / "qubit_log_neg_E_circ_E.pdf")
    plt.close(fig)

    print("Done.")
    print(f"  PNG:  docs/research/figures/qubit_log_neg_E_circ_E.png")
    print(f"  PDF:  docs/research/figures/qubit_log_neg_E_circ_E.pdf")
    print(f"  CSV:  docs/research/data/qubit_log_neg_E_circ_E.csv")
    print()
    print("Structural finding: AD∘AD ≡ Erasure∘Erasure (same log_neg formula log₂(1+(1-p)²))")
    print("Verified at p=0.3: AD∘AD =", ln_AD(2*0.3 - 0.09), ", ER∘ER =", ln_ER(2*0.3 - 0.09))
    print()
    print("Depolarizing PPT zero crossing for composed:")
    # 2p - p² ≥ 2/3 → p² - 2p + 2/3 ≤ 0 → p = 1 - √(1/3) ≈ 0.4226
    print(f"  Single arm: p = 2/3 ≈ {2/3:.4f}")
    print(f"  Composed:   p = 1 - 1/√3 ≈ {1 - 1/math.sqrt(3):.4f}")


if __name__ == "__main__":
    main()
