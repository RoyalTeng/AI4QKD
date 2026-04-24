"""Gap 定量形状 (G4.1 Sub-Q4 §5.1 初步).

Plots gap(η) between Sub-Q3 upper bound candidates and Sub-Q2 Pareto
lower bounds across loss range.

Candidates for upper bound:
  A: PLOB on worst edge (symmetric: -log_2(1 - √η_end2end))
  B: Pirandola 2019 N=1 chain (same as A for symmetric)
  C: E_R^PPT SDP for qubit amp-damping channel (effective qubit analog)

Lower bound:
  TF/PM-QKD asymptotic from tf_family_loss1d.csv

Reference (NOT an upper bound):
  Q_AD: qubit AD channel quantum capacity Q = unassisted private capacity P
        for γ ≤ 1/2 (Caruso-Giovannetti-Holevo 2014). Plotted for reference.
        IMPORTANT: Q ≤ K^{↔} for any channel, so Q is a LOWER BOUND on the
        two-way key capacity, not an upper bound. NOT a gap UB candidate.

Caveat: All upper-bound candidates A/B/C are [CONJ] for umr topology per
docs/proofs/upper_bound_msen.md. The qubit AD quantum capacity Q is [THM]
for the qubit AD channel but NOT a UB on the umr K^{↔} topology.

This script gives gap SHAPE under candidate assumption; does NOT give
[THM]-level gap for umr topology.
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "docs" / "research" / "data"
FIG_DIR = REPO_ROOT / "docs" / "research" / "figures"


def load_tf_1d():
    path = DATA_DIR / "tf_family_loss1d.csv"
    rows = []
    with path.open() as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((float(row["loss_dB_total"]),
                         float(row["rate_bits_per_signal"])))
    return zip(*rows)


def plob_worst_edge(loss_dB_total):
    """Candidate A/B: symmetric 2-arm loss, worst-edge PLOB.

    loss_dB_total = -10·log_10(η_end2end), symmetric η_arm = √η_end2end.
    Worst edge has transmission η_arm, PLOB bound = -log_2(1 - η_arm).
    """
    eta_end = 10.0 ** (-loss_dB_total / 10.0)
    eta_arm = np.sqrt(eta_end)
    return -np.log2(np.maximum(1.0 - eta_arm, 1e-30))


def pirandola_n1(loss_dB_total):
    """Pirandola 2019 N=1 chain: -log_2(1 - √η_total) [same as worst-edge for symmetric]."""
    eta = 10.0 ** (-loss_dB_total / 10.0)
    return -np.log2(np.maximum(1.0 - np.sqrt(eta), 1e-30))


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    loss_tf, rate_tf = load_tf_1d()
    loss_arr = np.array(loss_tf)
    rate_arr = np.array(rate_tf)

    # Upper bound candidates
    ub_plob_end = -np.log2(
        np.maximum(1.0 - 10.0 ** (-loss_arr / 10.0), 1e-30)
    )  # PLOB with end-to-end η (not used for umr, shown for comparison)
    ub_worst = plob_worst_edge(loss_arr)  # Candidate A/B (symmetric)

    # Candidate C: E_R^PPT qubit amp damping with γ = 1 - η_arm
    # Run this only at a subset of loss values to save time
    print("Computing E_R^PPT for qubit amp damping (subset) ...")
    from qkdx.numerics.upper_bound import (
        quantum_capacity_amplitude_damping_degradable,
        e_r_channel_ppt, kraus_amplitude_damping_qubit,
    )
    sub_losses = loss_arr[::10]  # every 10 dB
    sub_ub = []
    sub_q_ref = []  # Reference: AD quantum capacity Q (NOT an upper bound on K^{↔})
    for L in sub_losses:
        eta_arm = 10.0 ** (-L / 20.0)
        gamma = 1.0 - eta_arm
        try:
            r = e_r_channel_ppt(kraus_amplitude_damping_qubit(float(gamma)), dim_A=2)
            sub_ub.append(r["E_R_channel_bits"])
        except Exception as e:
            print(f"  loss={L}: SDP fail {e}")
            sub_ub.append(np.nan)
        # Q reference (lower bound on K^{↔}, not an upper bound)
        q = quantum_capacity_amplitude_damping_degradable(float(gamma)) if gamma < 0.5 else np.nan
        sub_q_ref.append(q)
        q_str = f"{q:.4f}" if not np.isnan(q) else "anti-deg(NaN)"
        print(f"  loss={L:.0f} dB (γ={gamma:.4f}): E_R^PPT={sub_ub[-1]:.4f}, Q={q_str}")

    # Gap calculations
    gap_plob_end = ub_plob_end - rate_arr  # direct PLOB (end-to-end, single-edge original)
    gap_worst = ub_worst - rate_arr        # candidate A/B

    # Save data
    with (DATA_DIR / "gap_shape.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "loss_dB_total", "tf_rate",
            "ub_candA_worst", "gap_candA",
            "ub_plob_end2end_direct", "gap_plob_direct",
        ])
        for i in range(len(loss_arr)):
            w.writerow([
                f"{loss_arr[i]:.3f}", f"{rate_arr[i]:.6e}",
                f"{ub_worst[i]:.6e}", f"{gap_worst[i]:.6e}",
                f"{ub_plob_end[i]:.6e}", f"{gap_plob_end[i]:.6e}",
            ])
    print(f"wrote {DATA_DIR}/gap_shape.csv")

    # === Figure 1: upper bound vs lower bound vs gap (log-log) ===
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    pos_r = rate_arr > 0
    ax1.semilogy(loss_arr[pos_r], rate_arr[pos_r], "s-", color="C1",
                 label="TF/PM-QKD lower bound (asymp)")
    ax1.semilogy(loss_arr, ub_worst, "--", color="red",
                 label="Upper bound candidate A/B (symmetric umr)")
    ax1.semilogy(loss_arr, ub_plob_end, ":", color="gray", alpha=0.5,
                 label="PLOB direct-link (reference, NOT umr)")
    if sub_ub:
        ax1.semilogy(sub_losses, sub_ub, "o", color="purple",
                     label="Candidate C: E_R^PPT amp-damp SDP")
    if sub_q_ref:
        sub_q_arr = np.array(sub_q_ref)
        valid = ~np.isnan(sub_q_arr) & (sub_q_arr > 1e-15)
        if valid.any():
            ax1.semilogy(np.array(sub_losses)[valid], sub_q_arr[valid], "D",
                         color="green", markersize=8, linestyle="none",
                         label=r"AD $Q$ analytic (ref, γ<1/2) — LB on K$^{↔}$, not UB")
    ax1.set_xlabel("Loss [dB]")
    ax1.set_ylabel("Rate (bits/signal)")
    ax1.set_title("Upper vs Lower bounds")
    ax1.grid(True, which="both", ls="--", alpha=0.4)
    ax1.legend(loc="lower left", fontsize=9)

    # Ratio plot (gap/lower)
    ratio = np.divide(ub_worst, rate_arr,
                      out=np.full_like(ub_worst, np.inf),
                      where=rate_arr > 1e-15)
    ax2.semilogy(loss_arr[rate_arr > 0], ratio[rate_arr > 0], "-", color="darkred",
                 label="candidate A/B ratio: UB / TF_LB")
    ax2.set_xlabel("Loss [dB]")
    ax2.set_ylabel("Gap ratio (UB / LB)")
    ax2.set_title("Gap ratio (log scale)")
    ax2.grid(True, which="both", ls="--", alpha=0.4)
    ax2.legend()
    ax2.axhline(y=1, color="black", alpha=0.3)

    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"gap_shape.{ext}", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {FIG_DIR}/gap_shape.{{png,pdf}}")

    # Summary
    print("\n=== Gap shape summary ===")
    print(f"Loss=0 dB:    UB(A/B)={ub_worst[0]:.4f}, LB_TF={rate_arr[0]:.4e}, ratio={ratio[0]:.2e}")
    print(f"Loss=20 dB:   UB(A/B)={ub_worst[20]:.4f}, LB_TF={rate_arr[20]:.4e}, ratio={ratio[20]:.2e}")
    print(f"Loss=40 dB:   UB(A/B)={ub_worst[40]:.4f}, LB_TF={rate_arr[40]:.4e}, ratio={ratio[40]:.2e}")
    print(f"Loss=60 dB:   UB(A/B)={ub_worst[60]:.4f}, LB_TF={rate_arr[60]:.4e}, ratio={ratio[60]:.2e}")


if __name__ == "__main__":
    main()
