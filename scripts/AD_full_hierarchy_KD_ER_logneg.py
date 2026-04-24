"""AD Choi-state quantities: Q (channel, LB on K^{↔}) vs E_R^PPT (Choi-state SDP) vs log_neg (Choi-state).

NOTE (2026-04-24 post-Codex-REJECTED): AD is NOT teleportation-covariant
(WTB 2017), so Choi-state E_R^PPT does NOT automatically upper-bound
the channel two-way key capacity K^{↔}(N_AD). Earlier version of this
docstring claimed 'Q ≤ K^{↔} ≤ E_R^PPT ≤ log_neg' at channel level —
that claim is withdrawn. See:
  docs/findings/AD_anti_degradable_E_R_PPT_2026-04-24.md §-1
  docs/research/RETRACTION.md §8

Objects plotted/recorded:
- Q(N_AD) (channel, analytic, LB on K^{↔} for γ ≤ 1/2): max_p[h((1-γ)p) - h(γp)]
- E_R^PPT(J_{N_AD}) (Choi-state, SDP)
- log_neg(J_{N_AD}) (Choi-state, analytic)

For γ > 1/2 (anti-degradable): Q=0; channel K^{↔} OPEN; Choi-state
E_R^PPT and log_neg remain numerically meaningful but are not channel UBs.

Output:
  docs/research/figures/AD_complete_hierarchy.{png,pdf}
  docs/research/data/AD_complete_hierarchy.csv
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
    quantum_capacity_amplitude_damping_degradable, analytic_log_neg_amplitude_damping,
)
K_D_amplitude_damping_degradable = quantum_capacity_amplitude_damping_degradable  # backward compat


def load_E_R_PPT_AD():
    """Load AD E_R^PPT SDP values from existing CSV."""
    csv_path = REPO / "docs" / "research" / "data" / "qubit_E_R_PPT_SDP_all_4.csv"
    pts = []
    with open(csv_path) as f:
        for r in csv.DictReader(f):
            if r["family"] == "AD":
                pts.append((float(r["param"]), float(r["E_R_PPT_SDP"])))
    return sorted(pts, key=lambda x: x[0])


def main():
    gammas = np.linspace(0.001, 0.999, 1001)
    log_neg = np.array([analytic_log_neg_amplitude_damping(g) for g in gammas])
    Q = np.array([quantum_capacity_amplitude_damping_degradable(g) for g in gammas])
    K_D = Q  # kept for plotting compatibility below

    er_pts = load_E_R_PPT_AD()
    er_g = np.array([p[0] for p in er_pts])
    er_v = np.array([p[1] for p in er_pts])

    out_csv = REPO / "docs" / "research" / "data" / "AD_complete_hierarchy.csv"
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["gamma", "log_neg_analytic", "Q_degradable_analytic_LB_on_K2way"])
        for g, ln, q in zip(gammas, log_neg, Q):
            w.writerow([f"{g:.4f}", f"{ln:.10f}", f"{q:.10f}"])

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.5))

    # Left: absolute
    ax = axes[0]
    ax.plot(gammas, log_neg, label="log_neg (loosest UB, analytic)", linewidth=2, color="C0", alpha=0.8)
    ax.scatter(er_g, er_v, color="C1", marker="s", s=60,
               label=r"$E_R^{PPT}$ (MOSEK SDP, 7 pts)", zorder=5)
    # K_D solid for γ ≤ 1/2 (degradable), dashed/zero after
    Q_deg = np.where(gammas <= 0.5, Q, 0)
    ax.plot(gammas, Q_deg, label=r"$Q$ = quantum capacity (LB on $K^{\leftrightarrow}$, γ ≤ 1/2)", linewidth=2.5, color="C2", linestyle="--")
    # Shaded "K^{↔} unknown" region for γ > 1/2
    ax.axvspan(0.5, 1.0, alpha=0.08, color="gray")
    ax.text(0.65, 0.85, r"$K^{\leftrightarrow}$ OPEN" + "\n" + r"(γ > 1/2,"+ "\n" + r"anti-degradable)",
            fontsize=8, color="gray", ha="center")
    ax.axvline(0.5, color="gray", linewidth=0.8, alpha=0.5, linestyle=":")
    ax.set_xlabel("γ (damping prob)")
    ax.set_ylabel("bits")
    ax.set_title("AD: channel $Q$ (LB on $K^{\\leftrightarrow}$) + Choi-state $E_R^{PPT}$ / log_neg\n"
                 + r"(AD not tele-covariant; Choi-state values NOT automatic channel UB)")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.02, 1.05)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    # Right: ratios in degradable regime
    ax = axes[1]
    Q_safe = np.where(Q > 1e-6, Q, np.nan)
    ax.plot(gammas, log_neg / Q_safe, label="log_neg / Q", linewidth=2, color="C0")
    # Sparse E_R^PPT / Q
    Q_at_er = np.array([quantum_capacity_amplitude_damping_degradable(g) for g in er_g])
    ratios_er_q = np.where(Q_at_er > 1e-6, er_v / Q_at_er, np.nan)
    ax.scatter(er_g, ratios_er_q, color="C1", marker="s", s=60,
               label=r"$E_R^{PPT}(J_N)$ / $Q(N)$ (Choi-vs-channel, not a UB/LB ratio)", zorder=5)
    ax.axvline(0.5, color="gray", linewidth=0.8, alpha=0.5, linestyle=":")
    ax.axhline(1.0, color="gray", linewidth=0.5, alpha=0.5)
    ax.set_xlabel("γ")
    ax.set_ylabel(r"ratio (Choi-state values / channel $Q$)")
    ax.set_title("AD: Choi-state log_neg and $E_R^{PPT}$ compared to channel $Q$\n"
                 + "(ratio informational only; not channel UB vs LB)")
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0.5, 5.0)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig_dir = REPO / "docs" / "research" / "figures"
    fig.savefig(fig_dir / "AD_complete_hierarchy.png", dpi=160)
    fig.savefig(fig_dir / "AD_complete_hierarchy.pdf")
    plt.close(fig)

    print("Done.")
    print(f"  CSV:  docs/research/data/AD_complete_hierarchy.csv")
    print(f"  PNG:  docs/research/figures/AD_complete_hierarchy.png")
    print()
    print(f"AD (γ ≤ 1/2): channel Q (LB on K^{{↔}}) vs Choi-state E_R^PPT and log_neg")
    print(f"  (AD not tele-covariant per WTB 2017; Choi-state E_R^PPT is NOT a channel")
    print(f"   K^{{↔}} UB for AD. Channel K^{{↔}}(AD) OPEN. Ratios below are Choi-vs-channel")
    print(f"   informational comparisons, not UB/LB hierarchy statements.)")
    print(f"  {'γ':>6} {'Q (ch LB)':>10} {'E_R^PPT (Choi)':>16} {'log_neg (Choi)':>16} {'ratio ER/Q':>11} {'ratio ln/Q':>11}")
    for g, ev in er_pts:
        if g >= 0.5: break
        q = quantum_capacity_amplitude_damping_degradable(g)
        ln = analytic_log_neg_amplitude_damping(g)
        print(f"  {g:6.4f} {q:10.4f} {ev:16.4f} {ln:16.4f} {ev/q:11.3f} {ln/q:11.3f}")


if __name__ == "__main__":
    main()
