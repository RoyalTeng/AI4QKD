"""MDI-QKD family Pareto sweep + figure generation (Phase 1 S2.2 A.1).

Generates:
    docs/research/data/mdi_family_loss1d.csv       — 1D loss sweep
    docs/research/data/mdi_family_loss_x_edev.csv  — 2D loss × e_d
    docs/research/data/mdi_family_loss_x_pdark.csv — 2D loss × p_d
    docs/research/figures/mdi_family_rate_vs_loss.{png,pdf}
    docs/research/figures/mdi_family_loss_x_edev_heatmap.{png,pdf}
    docs/research/figures/mdi_family_loss_x_pdark_heatmap.{png,pdf}

Usage:
    PYTHONPATH=. python scripts/sweep_mdi_family.py
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from qkdx.sweeps.mdi_family_sweep import (
    sweep_mdi_loss_1d,
    sweep_mdi_loss_x_edeviation,
    sweep_mdi_loss_x_pdark,
    upper_envelope_loss,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "docs" / "research" / "data"
FIG_DIR = REPO_ROOT / "docs" / "research" / "figures"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, header: list[str], rows: list[list]) -> None:
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    print(f"wrote {path}")


def make_figures():
    """Lazy-import matplotlib so unit tests don't need it."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # 1D loss sweep
    print("[1/3] 1D loss sweep ...")
    loss_1d = np.linspace(0, 80, 81)
    pts = sweep_mdi_loss_1d(loss_1d)
    losses = [p.params["loss_dB_total"] for p in pts]
    rates = [p.objectives[0] for p in pts]
    write_csv(
        DATA_DIR / "mdi_family_loss1d.csv",
        ["loss_dB_total", "rate_bits_per_signal"],
        [[f"{l:.3f}", f"{r:.6e}"] for l, r in zip(losses, rates)],
    )
    fig, ax = plt.subplots(figsize=(7, 5))
    # Only plot positive rates on log scale
    rates_arr = np.array(rates)
    pos = rates_arr > 0
    ax.semilogy(np.array(losses)[pos], rates_arr[pos],
                "o-", label="Ma-Razavi decoy MDI (Fig.4 original)")
    ax.set_xlabel("Total two-arm loss [dB]")
    ax.set_ylabel("Key rate (bits/signal)")
    ax.set_title("MDI-QKD: rate vs loss (Ma-Razavi 2012 Table I defaults)")
    ax.grid(True, which="both", ls="--", alpha=0.5)
    ax.legend()
    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"mdi_family_rate_vs_loss.{ext}", dpi=150,
                    bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {FIG_DIR / 'mdi_family_rate_vs_loss.{png,pdf}'}")

    # 2D loss × e_d
    print("[2/3] 2D loss × e_d sweep ...")
    loss_2d = np.linspace(0, 60, 50)
    e_d_vals = np.logspace(-3, -1, 25)  # 0.001 to 0.1 (1250 points)
    pts = sweep_mdi_loss_x_edeviation(loss_2d, e_d_vals)
    write_csv(
        DATA_DIR / "mdi_family_loss_x_edev.csv",
        ["loss_dB_total", "e_d", "rate"],
        [[p.params["loss_dB_total"], p.params["e_d"], p.objectives[0]]
         for p in pts],
    )
    # Heatmap: rows = loss, cols = e_d
    rate_grid = np.array([p.objectives[0] for p in pts]).reshape(
        len(loss_2d), len(e_d_vals),
    )
    rate_grid = np.maximum(rate_grid, 1e-12)  # clip for log scale
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.pcolormesh(e_d_vals, loss_2d, np.log10(rate_grid),
                       shading="auto", cmap="viridis")
    ax.set_xscale("log")
    ax.set_xlabel("e_d (optical misalignment)")
    ax.set_ylabel("Loss [dB]")
    ax.set_title("MDI-QKD log₁₀(rate) heatmap: loss × e_d")
    fig.colorbar(im, label="log₁₀(rate)")
    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"mdi_family_loss_x_edev_heatmap.{ext}", dpi=150,
                    bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {FIG_DIR}/mdi_family_loss_x_edev_heatmap.{{png,pdf}}")

    # 2D loss × p_dark
    print("[3/3] 2D loss × p_d sweep ...")
    p_d_vals = np.logspace(-8, -4, 25)  # 1e-8 to 1e-4 (1250 points)
    pts = sweep_mdi_loss_x_pdark(loss_2d, p_d_vals)
    write_csv(
        DATA_DIR / "mdi_family_loss_x_pdark.csv",
        ["loss_dB_total", "p_d", "rate"],
        [[p.params["loss_dB_total"], p.params["p_d"], p.objectives[0]]
         for p in pts],
    )
    rate_grid = np.array([p.objectives[0] for p in pts]).reshape(
        len(loss_2d), len(p_d_vals),
    )
    rate_grid = np.maximum(rate_grid, 1e-12)
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.pcolormesh(p_d_vals, loss_2d, np.log10(rate_grid),
                       shading="auto", cmap="viridis")
    ax.set_xscale("log")
    ax.set_xlabel("p_d (detector dark-count probability)")
    ax.set_ylabel("Loss [dB]")
    ax.set_title("MDI-QKD log₁₀(rate) heatmap: loss × p_d")
    fig.colorbar(im, label="log₁₀(rate)")
    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"mdi_family_loss_x_pdark_heatmap.{ext}", dpi=150,
                    bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {FIG_DIR}/mdi_family_loss_x_pdark_heatmap.{{png,pdf}}")

    # Summary stats
    print("\n=== MDI family Pareto summary ===")
    pos_1d = [r for r in rates if r > 0]
    max_rate = max(pos_1d) if pos_1d else 0.0
    cutoff_idx = next(
        (i for i, r in enumerate(rates) if r <= 1e-10),
        None,
    )
    cutoff_dB = losses[cutoff_idx] if cutoff_idx is not None else "> 80"
    print(f"  max rate (1D, optimized μ, default e_d/p_d): {max_rate:.4e} bits/signal")
    print(f"  cutoff loss (rate ≤ 1e-10): ~{cutoff_dB} dB")
    print(f"  total 2D grid points (loss × e_d): {len(loss_2d) * len(e_d_vals)}")
    print(f"  total 2D grid points (loss × p_d): {len(loss_2d) * len(p_d_vals)}")


if __name__ == "__main__":
    make_figures()
