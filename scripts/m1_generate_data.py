"""Generate M1 benchmark data for docs/findings/m1_wlc_bb84.md.

Runs a QBER sweep with the currently available solver (CLARABEL fallback
if MOSEK is absent), saves results as JSON + matplotlib figures.

Output files:
  docs/figures/m1_wlc_bb84_keyrate.{pdf,png}
  docs/figures/m1_wlc_bb84_deviation.{pdf,png}
  data/m1_bb84_sweep.json
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from qkdx.protocols.bb84 import build_bb84_protocol
from qkdx.numerics.wlc import wlc_key_rate
from qkdx.analytic.shor_preskill import shor_preskill_rate
from qkdx.utils.solvers import preferred_solver, has_mosek


def main() -> None:
    solver = preferred_solver()
    mosek = has_mosek()
    print(f"[m1_sweep] Preferred solver: {solver}  MOSEK available: {mosek}")

    qber_values = np.linspace(0.0, 0.11, 23)
    f_ec = 1.0

    wlc_rates: list[float] = []
    sp_rates: list[float] = []
    solvers: list[str] = []
    times: list[float] = []
    gaps: list[float] = []
    statuses: list[str] = []

    for q in qber_values:
        proto = build_bb84_protocol(qber=float(q))
        obs = {"qber_Z": float(q), "qber_X": float(q), "p_sift": 0.5}
        t0 = time.perf_counter()
        res = wlc_key_rate(proto, obs, f_ec=f_ec)
        dt = time.perf_counter() - t0

        wlc_rates.append(res.key_rate)
        sp_rates.append(shor_preskill_rate(float(q), f_ec=f_ec))
        solvers.append(res.solver)
        times.append(dt)
        gaps.append(res.duality_gap)
        statuses.append(res.primal_status)
        print(
            f"  QBER={q:.3f}  WLC={res.key_rate:+.6f}  SP={sp_rates[-1]:+.6f}"
            f"  |diff|={abs(res.key_rate - sp_rates[-1]):.2e}"
            f"  gap={res.duality_gap:.1e}  t={dt:.2f}s  [{res.solver}]"
        )

    wlc_rates_np = np.array(wlc_rates)
    sp_rates_np = np.array(sp_rates)
    max_dev = float(np.max(np.abs(wlc_rates_np - sp_rates_np)))
    mean_dev = float(np.mean(np.abs(wlc_rates_np - sp_rates_np)))

    print(f"\n[m1_sweep] Max |WLC - SP|  : {max_dev:.3e}")
    print(f"[m1_sweep] Mean |WLC - SP| : {mean_dev:.3e}")
    print(f"[m1_sweep] Total time     : {sum(times):.1f}s ({np.mean(times):.2f}s/pt)")

    # ---- Save data ----
    data = {
        "qber_values": qber_values.tolist(),
        "wlc_rates": wlc_rates,
        "sp_rates": sp_rates,
        "solvers": solvers,
        "times_seconds": times,
        "duality_gaps": gaps,
        "primal_statuses": statuses,
        "f_ec": f_ec,
        "preferred_solver": solver,
        "mosek_available": mosek,
        "max_abs_deviation": max_dev,
        "mean_abs_deviation": mean_dev,
        "total_time_seconds": float(sum(times)),
    }
    (REPO / "data").mkdir(exist_ok=True)
    data_path = REPO / "data" / "m1_bb84_sweep.json"
    with open(data_path, "w") as fh:
        json.dump(data, fh, indent=2)
    print(f"[m1_sweep] Data saved → {data_path}")

    # ---- Plots ----
    (REPO / "docs" / "figures").mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 5))
    qber_pct = qber_values * 100
    ax.plot(qber_pct, sp_rates_np, "k-", linewidth=2, label="Shor-Preskill (analytic)")
    ax.plot(qber_pct, wlc_rates_np, "bo--", markersize=5,
            label=f"WLC SDP ({solver})")
    ax.axhline(0, color="gray", linewidth=0.8, linestyle=":")
    ax.axvline(11.0, color="red", linewidth=0.8, linestyle="--", alpha=0.6,
               label="Threshold ≈ 11%")
    ax.set_xlabel("QBER (%)")
    ax.set_ylabel("Key rate (bit/signal)")
    ax.set_title(f"BB84 Asymptotic Key Rate (f_ec = {f_ec})")
    ax.legend()
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 11.5)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(REPO / "docs" / "figures" / f"m1_wlc_bb84_keyrate.{ext}", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    deviation = np.abs(wlc_rates_np - sp_rates_np)
    ax.semilogy(qber_pct, np.maximum(deviation, 1e-12), "b.-", markersize=8)
    ax.axhline(1e-3, color="orange", linestyle="--", linewidth=1, label="1e-3")
    ax.axhline(1e-5, color="green", linestyle="--", linewidth=1, label="1e-5")
    ax.set_xlabel("QBER (%)")
    ax.set_ylabel("|WLC − SP| (bit/signal)")
    ax.set_title("WLC vs Shor-Preskill — absolute deviation")
    ax.legend()
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
    ax.grid(True, alpha=0.3, which="both")
    ax.set_xlim(0, 11.5)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(REPO / "docs" / "figures" / f"m1_wlc_bb84_deviation.{ext}", dpi=150)
    plt.close(fig)

    print("[m1_sweep] Figures saved → docs/figures/m1_wlc_bb84_*.{pdf,png}")
    print("[m1_sweep] DONE.")


if __name__ == "__main__":
    main()
