"""Path α v0.2 numerical alignment — reframe existing TF/MDI Pareto LB
data against the path α scaling UB candidate (Pirandola 2019 N=1).

Status: [SYN] level. Reuses existing data; adds NO new LB claims.
The numerical UB column is identical to path δ v0.1 §3.2 (same formula);
this script merely produces a unified table for path α v0.2 §3.1.

Usage:
    PYTHONPATH=. python scripts/path_alpha_v0_2_alignment.py

Outputs:
    docs/research/data/path_alpha_v0_2_alignment.csv
    docs/research/figures/path_alpha_v0_2_alignment.png
    docs/research/figures/path_alpha_v0_2_alignment.pdf

Strict scope:
    - No protocol-class embedding lemma is asserted here.
    - No Eve-set compatibility is verified here.
    - Sub-gaps α.G1 / α.G2 / α.G2.E / α.G3 remain OPEN per
      docs/proofs/umr_path_alpha_three_lemma_v0_2.md §-1.
    - This script only renders numerical reframing for §3.1 of that doc.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "docs" / "research" / "data"
FIG_DIR = REPO_ROOT / "docs" / "research" / "figures"

TF_CSV = DATA_DIR / "tf_family_loss1d.csv"
MDI_CSV = DATA_DIR / "mdi_family_loss1d.csv"

OUT_CSV = DATA_DIR / "path_alpha_v0_2_alignment.csv"
OUT_PNG = FIG_DIR / "path_alpha_v0_2_alignment.png"
OUT_PDF = FIG_DIR / "path_alpha_v0_2_alignment.pdf"


def read_loss_rate_csv(path: Path) -> dict[float, float]:
    """Return {loss_dB: rate}. Skip header row."""
    out: dict[float, float] = {}
    with path.open() as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            loss = float(row[0])
            rate = float(row[1])
            out[round(loss, 3)] = rate
    return out


def path_alpha_scaling_ub(loss_dB: float) -> float:
    """Pirandola 2019 N=1 trusted-chain UB applied via path α framework.

    eta_total = 10^(-loss/10)
    eta_arm = sqrt(eta_total)  (symmetric two-segment loss)
    UB = -log2(1 - eta_arm) = -log2(1 - sqrt(eta_total))

    [SYN] under path α v0.2 (sub-gaps α.G1/G2/G2.E/G3 OPEN).
    """
    eta_total = 10.0 ** (-loss_dB / 10.0)
    eta_arm = math.sqrt(eta_total)
    if eta_arm >= 1.0:
        return float("inf")
    return -math.log2(1.0 - eta_arm)


def main() -> None:
    if not TF_CSV.exists():
        raise SystemExit(f"missing {TF_CSV}; run sweep_tf_family.py first")
    if not MDI_CSV.exists():
        raise SystemExit(f"missing {MDI_CSV}; run sweep_mdi_family.py first")

    tf = read_loss_rate_csv(TF_CSV)
    mdi = read_loss_rate_csv(MDI_CSV)

    target_grid = [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0]

    rows: list[list[str]] = []
    for loss in target_grid:
        ub = path_alpha_scaling_ub(loss)
        tf_lb = tf.get(round(loss, 3))
        mdi_lb = mdi.get(round(loss, 3))

        ub_str = "inf" if math.isinf(ub) else f"{ub:.6e}"

        def ratio(lb: float | None) -> str:
            if lb is None or lb <= 0 or math.isinf(ub):
                return "—"
            return f"{ub / lb:.2f}"

        rows.append([
            f"{loss:.1f}",
            f"{10.0 ** (-loss/10.0):.6e}",
            ub_str,
            f"{tf_lb:.6e}" if tf_lb is not None else "—",
            f"{mdi_lb:.6e}" if mdi_lb is not None else "—",
            ratio(tf_lb),
            ratio(mdi_lb),
        ])

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "loss_dB", "eta_total",
            "path_alpha_scaling_UB",
            "TF_pareto_LB", "MDI_pareto_LB",
            "UB_over_TF_ratio", "UB_over_MDI_ratio",
        ])
        writer.writerows(rows)
    print(f"wrote {OUT_CSV}")

    print()
    print("Path α v0.2 §3.1 alignment table (numerical reframing only):")
    print(f"{'loss(dB)':>9} {'η_total':>12} {'α-UB':>14} "
          f"{'TF-LB':>14} {'MDI-LB':>14} {'UB/TF':>8} {'UB/MDI':>8}")
    for r in rows:
        print(f"{r[0]:>9} {r[1]:>12} {r[2]:>14} {r[3]:>14} "
              f"{r[4]:>14} {r[5]:>8} {r[6]:>8}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("matplotlib unavailable; skipping figure")
        return

    dense_loss = np.linspace(0.5, 80.0, 320)
    dense_eta = 10.0 ** (-dense_loss / 10.0)
    dense_ub = -np.log2(1.0 - np.sqrt(dense_eta))

    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    ax.semilogy(dense_loss, dense_ub, "-", color="C3", lw=2.0,
                label=r"path α scaling UB = $-\log_2(1-\sqrt{\eta_{AB}})$ [SYN]")

    tf_loss = np.array(sorted(tf.keys()))
    tf_rate = np.array([tf[k] for k in tf_loss])
    pos = tf_rate > 0
    ax.semilogy(tf_loss[pos], tf_rate[pos], "s-", color="C1",
                label="TF-QKD Pareto LB (PM-QKD, Ma-Zeng-Zhou 2018)")

    mdi_loss = np.array(sorted(mdi.keys()))
    mdi_rate = np.array([mdi[k] for k in mdi_loss])
    pos_m = mdi_rate > 0
    ax.semilogy(mdi_loss[pos_m], mdi_rate[pos_m], "o-", color="C0",
                label="MDI-QKD Pareto LB (Ma-Razavi 2012)")

    sqrt_ref = np.sqrt(dense_eta)
    ax.semilogy(dense_loss, sqrt_ref, "--", color="gray", alpha=0.4,
                label=r"$\sqrt{\eta_{AB}}$ scaling reference")

    ax.set_xlabel("Total loss (dB)")
    ax.set_ylabel("Rate (bits / signal)")
    ax.set_title("Path α v0.2 §3.1 — scaling UB vs Pareto LB (numerical reframing only)\n"
                 "[SYN] sub-gaps α.G1/G2/G2.E/G3 OPEN; no Lemma A/B/C closure asserted")
    ax.set_xlim(0, 80)
    ax.set_ylim(1e-11, 5.0)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="lower left", fontsize=9)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    fig.savefig(OUT_PDF)
    print(f"wrote {OUT_PNG}")
    print(f"wrote {OUT_PDF}")


if __name__ == "__main__":
    main()
