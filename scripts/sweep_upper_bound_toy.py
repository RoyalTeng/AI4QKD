"""Numerical E_R^PPT sweep over qubit toy channels (Phase 2 U3.7).

Generates:
    docs/research/data/er_ppt_depol_sweep.csv
    docs/research/data/er_ppt_amp_damping_sweep.csv
    docs/research/data/er_ppt_dephasing_sweep.csv
    docs/research/figures/upper_bound_toy_channels.{png,pdf}

Compares numerical E_R^PPT against reference upper/lower bounds.
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from qkdx.numerics.upper_bound import (
    e_r_channel_ppt,
    kraus_depolarizing_qubit,
    kraus_dephasing_qubit,
    kraus_amplitude_damping_qubit,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "docs" / "research" / "data"
FIG_DIR = REPO_ROOT / "docs" / "research" / "figures"


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    p_values = np.linspace(0.0, 1.0, 21)

    # Depolarizing channel
    print("[1/3] E_R^PPT for qubit depolarizing ...")
    depol_rates = []
    for p in p_values:
        r = e_r_channel_ppt(kraus_depolarizing_qubit(float(p)), dim_A=2)
        depol_rates.append(r["E_R_channel_bits"])
        print(f"  p={p:.3f}: E_R^PPT = {r['E_R_channel_bits']:.4f}")
    with (DATA_DIR / "er_ppt_depol_sweep.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["p_depolarizing", "E_R_ppt_bits"])
        for p, r in zip(p_values, depol_rates):
            w.writerow([f"{p:.4f}", f"{r:.6e}"])

    # Dephasing
    print("[2/3] E_R^PPT for qubit dephasing ...")
    deph_rates = []
    for p in p_values:
        r = e_r_channel_ppt(kraus_dephasing_qubit(float(p)), dim_A=2)
        deph_rates.append(r["E_R_channel_bits"])
    with (DATA_DIR / "er_ppt_dephasing_sweep.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["p_dephasing", "E_R_ppt_bits"])
        for p, r in zip(p_values, deph_rates):
            w.writerow([f"{p:.4f}", f"{r:.6e}"])

    # Amplitude damping
    print("[3/3] E_R^PPT for qubit amplitude damping ...")
    amp_rates = []
    for gamma in p_values:
        r = e_r_channel_ppt(kraus_amplitude_damping_qubit(float(gamma)), dim_A=2)
        amp_rates.append(r["E_R_channel_bits"])
    with (DATA_DIR / "er_ppt_amp_damping_sweep.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["gamma_damping", "E_R_ppt_bits"])
        for p, r in zip(p_values, amp_rates):
            w.writerow([f"{p:.4f}", f"{r:.6e}"])

    # Combined figure
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(p_values, depol_rates, "o-", label="Depolarizing: ρ→(1-p)ρ + pI/2")
    ax.plot(p_values, deph_rates, "s-", label="Dephasing: ρ→(1-p)ρ + pZρZ")
    ax.plot(p_values, amp_rates, "^-", label="Amplitude damping: γ = damping prob")

    # Reference: PLOB for pure-loss-analog (amp damping at γ = 1-η)
    # For amp damping: E_R = -log_2(1-γ) is the PLOB-analog (Wilde-Tomamichel-Berta 2017 §7)
    plob_amp = [-np.log2(1.0 - g) if g < 1 else np.nan for g in p_values]
    ax.plot(p_values, plob_amp, "--", color="gray", alpha=0.6,
            label="−log₂(1−γ) (amp-damp PLOB analog)")

    ax.set_xlabel("Channel noise parameter (p or γ)")
    ax.set_ylabel("E_R^PPT (bits/channel use)")
    ax.set_title("Numerical E_R^PPT upper bounds for qubit toy channels")
    ax.grid(True, ls="--", alpha=0.5)
    ax.legend(loc="upper right", fontsize=9)
    ax.set_ylim(-0.05, 2.5)

    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"upper_bound_toy_channels.{ext}", dpi=150,
                    bbox_inches="tight")
    plt.close(fig)

    print(f"\nwrote {FIG_DIR}/upper_bound_toy_channels.{{png,pdf}}")
    print("\n=== U3.7 Layer 5.3 SDP summary ===")
    print(f"  Depolarizing: E_R @ p=0 = {depol_rates[0]:.4f} (expect 1)")
    print(f"  Depolarizing: E_R @ p=1 = {depol_rates[-1]:.4f} (expect 0)")
    print(f"  Dephasing: E_R @ p=0.5 = {deph_rates[10]:.4f}")
    print(f"  Amp damping: E_R @ γ=0.5 = {amp_rates[10]:.4f}")


if __name__ == "__main__":
    main()
