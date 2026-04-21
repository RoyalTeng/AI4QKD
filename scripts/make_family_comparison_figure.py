"""Generate DV-QKD protocol family comparison figure (A.2 PHASE1_REPORT).

Combines BB84 / MDI / TF-QKD family Pareto data into a single (loss_dB, rate)
log-log plot on a common loss axis.

BB84: WLC SDP rate at qber=0 (as limit, uses p_sift=0.5 × 1 bit).
MDI: Ma-Razavi 2012 decoy, Table I defaults.
TF/PM-QKD: Ma-Zeng-Zhou 2018, default params.

Usage:
    PYTHONPATH=. python scripts/make_family_comparison_figure.py
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "docs" / "research" / "data"
FIG_DIR = REPO_ROOT / "docs" / "research" / "figures"


def load_csv_1d(path, loss_key="loss_dB_total", rate_key="rate_bits_per_signal"):
    rows = []
    with path.open() as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append((float(r[loss_key]), float(r[rate_key])))
    return zip(*rows)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Load family 1D loss sweeps
    mdi_loss, mdi_rates = load_csv_1d(DATA_DIR / "mdi_family_loss1d.csv")
    tf_loss, tf_rates = load_csv_1d(DATA_DIR / "tf_family_loss1d.csv")

    # BB84 analytic: at qber=0 after depol channel with η, effective qber is 0
    # (assuming perfect misalignment); rate = p_sift · (1-2h(qber))·(1 - f_ec·h(qber))
    # Here we do qber=0 as limit → rate = 1/2 = 0.5 bits/signal (independent of η).
    # To include loss, multiply by η (photon-count detection probability).
    # For fair comparison on PLOB plot, use: BB84 rate = η · 0.5 (bits/signal).
    # This is a SIMPLIFICATION — full BB84 with loss uses decoy-state, which
    # reduces the rate further.  But as a family "Pareto envelope" it's still
    # meaningful for the comparison.
    bb84_loss = np.linspace(0, 80, 81)
    eta = 10.0 ** (-bb84_loss / 10.0)
    bb84_rates = 0.5 * eta  # Werner 1-photon rate at qber=0

    # PLOB upper bound reference
    plob_rates = -np.log2(np.maximum(1.0 - eta, 1e-30))

    # √η and η reference lines
    sqrt_eta = np.sqrt(eta)
    eta_line = eta

    fig, ax = plt.subplots(figsize=(9, 6))

    # Family curves (positive values only on log scale)
    mdi_loss_arr = np.array(mdi_loss)
    mdi_rates_arr = np.array(mdi_rates)
    pos_m = mdi_rates_arr > 0
    ax.semilogy(mdi_loss_arr[pos_m], mdi_rates_arr[pos_m],
                "o-", color="C0", markersize=4,
                label="MDI-QKD (Ma-Razavi 2012, decoy)")

    tf_loss_arr = np.array(tf_loss)
    tf_rates_arr = np.array(tf_rates)
    pos_t = tf_rates_arr > 0
    ax.semilogy(tf_loss_arr[pos_t], tf_rates_arr[pos_t],
                "s-", color="C1", markersize=4,
                label="PM-QKD / TF family (Ma-Zeng-Zhou 2018)")

    pos_b = bb84_rates > 1e-15
    ax.semilogy(bb84_loss[pos_b], bb84_rates[pos_b],
                "^-", color="C2", markersize=4,
                label="BB84 single-photon limit (η · 1/2)")

    # Reference scaling lines
    ax.semilogy(bb84_loss, plob_rates, ":", color="red", alpha=0.6,
                label="PLOB upper bound: −log₂(1−η)")
    ax.semilogy(bb84_loss, sqrt_eta, "--", color="gray", alpha=0.4,
                label="√η reference (TF scaling)")
    ax.semilogy(bb84_loss, eta_line, "--", color="lightgray", alpha=0.4,
                label="η reference (direct-link scaling)")

    ax.set_xlabel("Loss [dB]", fontsize=12)
    ax.set_ylabel("Key rate (bits/signal)", fontsize=12)
    ax.set_title(
        "DV-QKD Family Pareto Map: BB84 / MDI-QKD / PM-QKD vs PLOB",
        fontsize=13,
    )
    ax.grid(True, which="both", ls="--", alpha=0.4)
    ax.legend(loc="lower left", fontsize=9)
    ax.set_ylim(1e-8, 3.0)
    ax.set_xlim(0, 80)

    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"family_comparison.{ext}", dpi=200,
                    bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {FIG_DIR}/family_comparison.{{png,pdf}}")

    # Cross-over analysis: find loss at which TF overtakes MDI
    common_loss = sorted(set(mdi_loss_arr.tolist()) & set(tf_loss_arr.tolist()))
    mdi_dict = dict(zip(mdi_loss_arr.tolist(), mdi_rates_arr.tolist()))
    tf_dict = dict(zip(tf_loss_arr.tolist(), tf_rates_arr.tolist()))
    for L in common_loss:
        if L > 0 and tf_dict[L] > mdi_dict[L]:
            print(f"TF overtakes MDI at loss = {L} dB "
                  f"(TF={tf_dict[L]:.2e} vs MDI={mdi_dict[L]:.2e})")
            break


if __name__ == "__main__":
    main()
