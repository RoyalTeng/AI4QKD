"""E_R^PPT (SDP) for 4 qubit channel families — completes upper-bound matrix.

Compared to analytic log_neg (always a valid UB ≥ E_R^PPT):
- Sparse grid 5-7 param points per channel (MOSEK SDP ~seconds each)
- For erasure: dim_B = 3 (handled by e_r_channel_ppt dim_out logic)

Output:
  docs/research/data/qubit_E_R_PPT_SDP_all_4.csv
  docs/research/figures/qubit_E_R_PPT_all_4.{png,pdf}
"""
from __future__ import annotations

import csv
import math
import sys
import time
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
    e_r_channel_ppt,
    e_r_depolarizing_analytic,
    kraus_amplitude_damping_qubit,
    kraus_dephasing_qubit,
    kraus_depolarizing_qubit,
)
from qkdx.numerics.e_r_upper import e_r_dephasing, e_r_erasure


def kraus_erasure_qubit(p: float) -> list[np.ndarray]:
    """Qubit erasure: K0 = √(1-p)·[[1,0],[0,1],[0,0]] (3x2), Ke_i = √p·|e⟩⟨i|."""
    K0 = math.sqrt(1.0 - p) * np.array([[1, 0], [0, 1], [0, 0]], dtype=np.complex128)
    Ke0 = math.sqrt(p) * np.array([[0, 0], [0, 0], [1, 0]], dtype=np.complex128)
    Ke1 = math.sqrt(p) * np.array([[0, 0], [0, 0], [0, 1]], dtype=np.complex128)
    return [K0, Ke0, Ke1]


def main():
    grid_ad = [0.05, 0.10, 0.20, 0.30, 0.50, 0.70, 0.90]
    grid_dp = [0.05, 0.10, 0.15, 0.20, 0.30, 0.40]  # dephase: stop before 1/2
    grid_de = [0.02, 0.05, 0.10, 0.20, 0.30, 0.50]  # depol: stop before 2/3
    grid_er = [0.05, 0.10, 0.20, 0.30, 0.50, 0.70, 0.90]

    rows = []

    print("Computing E_R^PPT via MOSEK SDP for 4 channel families...")
    for gamma in grid_ad:
        t0 = time.time()
        kraus = kraus_amplitude_damping_qubit(gamma)
        result = e_r_channel_ppt(kraus, dim_A=2)
        er = float(result["E_R_channel_bits"])
        ln = analytic_log_neg_amplitude_damping(gamma)
        elapsed = time.time() - t0
        rows.append(("AD", gamma, er, ln, None, elapsed))
        print(f"  AD γ={gamma}: E_R={er:.4f}, log_neg={ln:.4f}, ratio={er/ln if ln>0 else 0:.3f}  ({elapsed:.1f}s)")

    for p in grid_dp:
        t0 = time.time()
        kraus = kraus_dephasing_qubit(p)
        result = e_r_channel_ppt(kraus, dim_A=2)
        er = float(result["E_R_channel_bits"])
        ln = analytic_log_neg_dephasing(p)
        kd = e_r_dephasing(p)
        elapsed = time.time() - t0
        rows.append(("Dephasing", p, er, ln, kd, elapsed))
        print(f"  Dephase p={p}: E_R={er:.4f}, log_neg={ln:.4f}, K_D={kd:.4f}  ({elapsed:.1f}s)")

    for p in grid_de:
        t0 = time.time()
        kraus = kraus_depolarizing_qubit(p)
        result = e_r_channel_ppt(kraus, dim_A=2)
        er = float(result["E_R_channel_bits"])
        ln = analytic_log_neg_depolarizing(p)
        kd = e_r_depolarizing_analytic(p)
        elapsed = time.time() - t0
        rows.append(("Depolarizing", p, er, ln, kd, elapsed))
        print(f"  Depol p={p}: E_R={er:.4f}, log_neg={ln:.4f}, E_R_analytic={kd:.4f}  ({elapsed:.1f}s)")

    for p in grid_er:
        t0 = time.time()
        kraus = kraus_erasure_qubit(p)
        result = e_r_channel_ppt(kraus, dim_A=2)
        er = float(result["E_R_channel_bits"])
        ln = analytic_log_neg_erasure(p)
        kd = e_r_erasure(p)
        elapsed = time.time() - t0
        rows.append(("Erasure", p, er, ln, kd, elapsed))
        print(f"  Erase p={p}: E_R={er:.4f}, log_neg={ln:.4f}, K_D={kd:.4f}  ({elapsed:.1f}s)")

    out_csv = REPO / "docs" / "research" / "data" / "qubit_E_R_PPT_SDP_all_4.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["family", "param", "E_R_PPT_SDP", "log_neg_analytic", "K_D_or_E_R_analytic", "sdp_time_s"])
        for family, p, er, ln, kd, t in rows:
            w.writerow([family, f"{p:.4f}", f"{er:.6f}", f"{ln:.6f}",
                        f"{kd:.6f}" if kd is not None else "", f"{t:.2f}"])

    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.5))
    # AD
    ax = axes[0, 0]
    ad_data = [r for r in rows if r[0] == "AD"]
    xs = [r[1] for r in ad_data]
    ax.plot(xs, [r[3] for r in ad_data], "o-", label="log_neg (analytic)", markersize=7, linewidth=2)
    ax.plot(xs, [r[2] for r in ad_data], "s--", label=r"$E_R^{PPT}$ (SDP)", markersize=6, linewidth=2)
    ax.set_xlabel("γ (damping prob)")
    ax.set_ylabel("bits")
    ax.set_title("Amplitude Damping")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # Dephasing
    ax = axes[0, 1]
    dp_data = [r for r in rows if r[0] == "Dephasing"]
    xs = [r[1] for r in dp_data]
    ax.plot(xs, [r[3] for r in dp_data], "o-", label="log_neg (analytic)", markersize=7, linewidth=2)
    ax.plot(xs, [r[2] for r in dp_data], "s--", label=r"$E_R^{PPT}$ (SDP)", markersize=6, linewidth=2)
    ax.plot(xs, [r[4] for r in dp_data], "^:", label=r"$K_D$ (PLOB)", markersize=6, linewidth=2)
    ax.set_xlabel("p (dephase prob)")
    ax.set_ylabel("bits")
    ax.set_title("Dephasing")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # Depolarizing
    ax = axes[1, 0]
    de_data = [r for r in rows if r[0] == "Depolarizing"]
    xs = [r[1] for r in de_data]
    ax.plot(xs, [r[3] for r in de_data], "o-", label="log_neg (analytic)", markersize=7, linewidth=2)
    ax.plot(xs, [r[2] for r in de_data], "s--", label=r"$E_R^{PPT}$ (SDP)", markersize=6, linewidth=2)
    ax.plot(xs, [r[4] for r in de_data], "^:", label=r"$E_R$ (Horodecki 99)", markersize=6, linewidth=2)
    ax.set_xlabel("p (depol param)")
    ax.set_ylabel("bits")
    ax.set_title("Depolarizing")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # Erasure
    ax = axes[1, 1]
    er_data = [r for r in rows if r[0] == "Erasure"]
    xs = [r[1] for r in er_data]
    ax.plot(xs, [r[3] for r in er_data], "o-", label="log_neg (analytic)", markersize=7, linewidth=2)
    ax.plot(xs, [r[2] for r in er_data], "s--", label=r"$E_R^{PPT}$ (SDP)", markersize=6, linewidth=2)
    ax.plot(xs, [r[4] for r in er_data], "^:", label=r"$K_D$ (PLOB)", markersize=6, linewidth=2)
    ax.set_xlabel("p (erase prob)")
    ax.set_ylabel("bits")
    ax.set_title("Erasure")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    fig.suptitle(r"Upper bound hierarchy: log_neg ≥ $E_R^{PPT}$ ≥ K_D / $E_R$ (analytic)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig_dir = REPO / "docs" / "research" / "figures"
    fig.savefig(fig_dir / "qubit_E_R_PPT_all_4.png", dpi=160)
    fig.savefig(fig_dir / "qubit_E_R_PPT_all_4.pdf")
    plt.close(fig)

    print()
    print(f"  CSV:  docs/research/data/qubit_E_R_PPT_SDP_all_4.csv")
    print(f"  PNG:  docs/research/figures/qubit_E_R_PPT_all_4.png")


if __name__ == "__main__":
    main()
