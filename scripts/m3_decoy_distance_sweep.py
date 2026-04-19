"""M3 distance sweep: reproduce Lo-Ma-Chen 2005 Fig.3 shape.

For each distance L in [0, 200] km:
    * Compute optimal μ via simple grid search over [0.05, 1.0]
    * Evaluate 1-decoy WLC key rate
    * Record R, μ_opt, estimates

Produces:
    data/m3_distance_sweep.json
    docs/figures/m3_decoy_distance.{pdf,png}
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from qkdx.analytic.channel import FibreChannel
from qkdx.numerics.decoy import decoy_wlc_rate_one
from qkdx.utils.solvers import preferred_solver


def best_mu(channel: FibreChannel, nu_fraction: float = 0.2) -> tuple[float, float]:
    """Grid-search μ ∈ [0.05, 1.0] to maximise rate.  Returns (μ_opt, R_opt)."""
    mus = np.linspace(0.05, 1.0, 20)
    best_R, best_mu_val = -float("inf"), 0.5
    for mu in mus:
        nu = mu * nu_fraction
        try:
            res = decoy_wlc_rate_one(channel, mu=float(mu), nu=float(nu))
            if res.key_rate > best_R:
                best_R = res.key_rate
                best_mu_val = float(mu)
        except Exception:
            continue
    return best_mu_val, best_R


def main() -> None:
    solver = preferred_solver()
    print(f"[m3_sweep] Preferred solver: {solver}")

    # Lo-Ma-Chen 2005 Fig.3 parameters
    params = dict(
        eta_detector=0.145,
        p_dark=8.5e-7,
        e_misalignment=0.033,
        alpha_db_per_km=0.21,
        f_ec=1.22,
    )

    lengths = list(np.linspace(0.0, 200.0, 41))
    rows: list[dict] = []
    t_start = time.perf_counter()

    for L in lengths:
        ch = FibreChannel(length_km=float(L), **params)
        t0 = time.perf_counter()
        mu_opt, R_opt = best_mu(ch)
        dt = time.perf_counter() - t0

        nu_opt = mu_opt * 0.2
        res = decoy_wlc_rate_one(ch, mu=mu_opt, nu=nu_opt)
        rows.append({
            "length_km": float(L),
            "mu_opt": mu_opt,
            "nu": nu_opt,
            "key_rate": res.key_rate,
            "Q_1_lower": res.estimates.Q_1_lower,
            "e_1_upper": res.estimates.e_1_upper,
            "Q_mu": res.Q_mu,
            "E_mu": res.E_mu,
            "h_bits_per_sift": res.h_bits_per_sift,
            "time_seconds": dt,
        })
        print(
            f"  L={L:5.1f} km  μ_opt={mu_opt:.3f}  "
            f"R={res.key_rate:+.3e}  "
            f"Y_1^L={res.estimates.Y_1_lower:.3e}  "
            f"e_1^U={res.estimates.e_1_upper:.4f}  t={dt:.2f}s"
        )

    total_time = time.perf_counter() - t_start
    print(f"\n[m3_sweep] Total time: {total_time:.1f}s")

    # ---- Persist ----
    (REPO / "data").mkdir(exist_ok=True)
    out = {
        "params": params,
        "solver": solver,
        "rows": rows,
    }
    with open(REPO / "data" / "m3_distance_sweep.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"[m3_sweep] Data → data/m3_distance_sweep.json")

    # ---- Figure ----
    (REPO / "docs" / "figures").mkdir(parents=True, exist_ok=True)
    L_arr = np.array([r["length_km"] for r in rows])
    R_arr = np.array([r["key_rate"] for r in rows])
    mu_arr = np.array([r["mu_opt"] for r in rows])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Left: R vs L (log y)
    R_pos = np.where(R_arr > 1e-12, R_arr, np.nan)
    ax1.semilogy(L_arr, R_pos, "b.-", markersize=6, label=f"1-decoy WLC [{solver}]")
    ax1.set_xlabel("Distance (km)")
    ax1.set_ylabel("Key rate (bit/signal)")
    ax1.set_title("Decoy-state BB84 — Lo-Ma-Chen 2005 parameters")
    ax1.grid(True, alpha=0.3, which="both")
    ax1.legend()
    ax1.set_xlim(0, 210)

    # Right: μ_opt vs L
    ax2.plot(L_arr, mu_arr, "g.-", markersize=6)
    ax2.set_xlabel("Distance (km)")
    ax2.set_ylabel("μ_opt (signal intensity)")
    ax2.set_title("Optimal signal intensity vs distance")
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 210)

    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(REPO / "docs" / "figures" / f"m3_decoy_distance.{ext}", dpi=150)
    plt.close(fig)
    print("[m3_sweep] Figures → docs/figures/m3_decoy_distance.{pdf,png}")
    print("[m3_sweep] DONE.")


if __name__ == "__main__":
    main()
