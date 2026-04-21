"""TF / PM-QKD family Pareto sweep + figure generation (Phase 1 S2.2 A.1).

Usage:
    PYTHONPATH=. python scripts/sweep_tf_family.py
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from qkdx.sweeps.tf_family_sweep import (
    sweep_pm_loss_1d, sweep_pm_loss_x_edelta,
    sweep_pm_loss_x_pdark, sweep_pm_loss_x_M,
    upper_envelope_loss,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "docs" / "research" / "data"
FIG_DIR = REPO_ROOT / "docs" / "research" / "figures"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)


def write_csv(path, header, rows):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    print(f"wrote {path}")


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # 1D loss
    print("[1/4] 1D loss sweep ...")
    loss_1d = np.linspace(0, 80, 81)
    pts = sweep_pm_loss_1d(loss_1d)
    losses = [p.params["loss_dB_total"] for p in pts]
    rates = [p.objectives[0] for p in pts]
    write_csv(DATA_DIR / "tf_family_loss1d.csv",
              ["loss_dB_total", "rate_bits_per_signal"],
              [[f"{l:.3f}", f"{r:.6e}"] for l, r in zip(losses, rates)])
    fig, ax = plt.subplots(figsize=(7, 5))
    rates_arr = np.array(rates)
    pos = rates_arr > 0
    ax.semilogy(np.array(losses)[pos], rates_arr[pos],
                "s-", color="C1", label="PM-QKD (Ma-Zeng-Zhou 2018)")
    # Add √η reference scaling line
    eta_ref = 10.0 ** (-np.array(losses) / 10.0)
    sqrt_eta_line = np.sqrt(eta_ref)
    ax.semilogy(losses, sqrt_eta_line, "--", color="gray", alpha=0.5,
                label="√η reference (TF scaling)")
    # PLOB reference
    plob = -np.log2(np.maximum(1.0 - eta_ref, 1e-30))
    ax.semilogy(losses, plob, ":", color="red", alpha=0.7,
                label="PLOB: −log₂(1−η) upper bound")
    ax.set_xlabel("Total loss [dB]")
    ax.set_ylabel("Key rate (bits/signal)")
    ax.set_title("PM-QKD family (TF-representative) rate vs loss")
    ax.grid(True, which="both", ls="--", alpha=0.5)
    ax.legend()
    ax.set_ylim(1e-8, 2.0)
    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"tf_family_rate_vs_loss.{ext}", dpi=150,
                    bbox_inches="tight")
    plt.close(fig)

    # 2D loss × e_delta
    print("[2/4] 2D loss × e_delta sweep ...")
    loss_2d = np.linspace(0, 60, 50)
    e_delta_vals = np.logspace(-3, -1.3, 25)
    pts = sweep_pm_loss_x_edelta(loss_2d, e_delta_vals)
    write_csv(DATA_DIR / "tf_family_loss_x_edelta.csv",
              ["loss_dB_total", "e_delta", "rate"],
              [[p.params["loss_dB_total"], p.params["e_delta"], p.objectives[0]]
               for p in pts])
    rate_grid = np.array([p.objectives[0] for p in pts]).reshape(
        len(loss_2d), len(e_delta_vals),
    )
    rate_grid = np.maximum(rate_grid, 1e-12)
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.pcolormesh(e_delta_vals, loss_2d, np.log10(rate_grid),
                       shading="auto", cmap="plasma")
    ax.set_xscale("log")
    ax.set_xlabel("e_δ (phase-slice + misalignment error)")
    ax.set_ylabel("Loss [dB]")
    ax.set_title("PM-QKD log₁₀(rate) heatmap: loss × e_δ")
    fig.colorbar(im, label="log₁₀(rate)")
    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"tf_family_loss_x_edelta_heatmap.{ext}", dpi=150,
                    bbox_inches="tight")
    plt.close(fig)

    # 2D loss × p_d
    print("[3/4] 2D loss × p_d sweep ...")
    p_d_vals = np.logspace(-9, -5, 25)
    pts = sweep_pm_loss_x_pdark(loss_2d, p_d_vals)
    write_csv(DATA_DIR / "tf_family_loss_x_pdark.csv",
              ["loss_dB_total", "p_d", "rate"],
              [[p.params["loss_dB_total"], p.params["p_d"], p.objectives[0]]
               for p in pts])
    rate_grid = np.array([p.objectives[0] for p in pts]).reshape(
        len(loss_2d), len(p_d_vals),
    )
    rate_grid = np.maximum(rate_grid, 1e-12)
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.pcolormesh(p_d_vals, loss_2d, np.log10(rate_grid),
                       shading="auto", cmap="plasma")
    ax.set_xscale("log")
    ax.set_xlabel("p_d (detector dark count)")
    ax.set_ylabel("Loss [dB]")
    ax.set_title("PM-QKD log₁₀(rate) heatmap: loss × p_d")
    fig.colorbar(im, label="log₁₀(rate)")
    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"tf_family_loss_x_pdark_heatmap.{ext}", dpi=150,
                    bbox_inches="tight")
    plt.close(fig)

    # 2D loss × M (phase slices)
    print("[4/4] 2D loss × M sweep ...")
    M_vals = [4, 8, 16, 32, 64]
    pts = sweep_pm_loss_x_M(loss_2d, M_vals)
    write_csv(DATA_DIR / "tf_family_loss_x_M.csv",
              ["loss_dB_total", "M", "rate"],
              [[p.params["loss_dB_total"], p.params["M"], p.objectives[0]]
               for p in pts])
    fig, ax = plt.subplots(figsize=(7, 5))
    for M_val in M_vals:
        losses_M = [p.params["loss_dB_total"] for p in pts
                    if p.params["M"] == M_val]
        rates_M = [p.objectives[0] for p in pts
                   if p.params["M"] == M_val]
        rates_M = np.array(rates_M)
        pos = rates_M > 0
        ax.semilogy(np.array(losses_M)[pos], rates_M[pos],
                    "o-", label=f"M={M_val}", markersize=4)
    ax.set_xlabel("Loss [dB]")
    ax.set_ylabel("Key rate (bits/signal)")
    ax.set_title("PM-QKD: effect of phase-slice count M on rate")
    ax.grid(True, which="both", ls="--", alpha=0.5)
    ax.legend()
    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"tf_family_loss_x_M.{ext}", dpi=150,
                    bbox_inches="tight")
    plt.close(fig)

    # Summary
    print("\n=== TF/PM-QKD family Pareto summary ===")
    pos_1d = [r for r in rates if r > 0]
    max_rate = max(pos_1d) if pos_1d else 0.0
    cutoff_idx = next((i for i, r in enumerate(rates) if r <= 1e-10), None)
    cutoff_dB = losses[cutoff_idx] if cutoff_idx is not None else "> 80"
    print(f"  max rate (default params, 0 dB): {max_rate:.4e} bits/signal")
    print(f"  cutoff loss (rate ≤ 1e-10): ~{cutoff_dB} dB")
    total_pts = 81 + 50*25 + 50*25 + 50*5
    print(f"  total sweep points: {total_pts} (S2.2 acceptance ≥ 1000: ✓)")


if __name__ == "__main__":
    main()
