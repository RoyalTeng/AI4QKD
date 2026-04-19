"""M2 MDI-QKD ideal-case QBER sweep: WLC SDP vs GLLP/MDI analytic."""
from __future__ import annotations

import json
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

from qkdx.analytic.gllp import mdi_ideal_symmetric_rate
from qkdx.analytic.shor_preskill import shor_preskill_rate
from qkdx.numerics.wlc import wlc_key_rate
from qkdx.protocols.bb84 import build_bb84_protocol
from qkdx.protocols.mdi import build_mdi_protocol
from qkdx.utils.solvers import preferred_solver, has_mosek


def main() -> None:
    solver = preferred_solver()
    mosek = has_mosek()
    print(f"[m2_mdi] Preferred solver: {solver}  MOSEK available: {mosek}")

    qbers = np.linspace(0.0, 0.11, 23)
    f_ec = 1.0

    rows: list[dict] = []
    for q in qbers:
        q = float(q)
        p_mdi = build_mdi_protocol(qber=q, p_sift=0.25)
        obs_mdi = {"qber_Z": q, "qber_X": q, "p_sift": 0.25}
        t0 = time.perf_counter()
        r_mdi = wlc_key_rate(p_mdi, obs_mdi, f_ec=f_ec)
        dt_mdi = time.perf_counter() - t0
        a_mdi = mdi_ideal_symmetric_rate(q, f_ec=f_ec)

        p_bb = build_bb84_protocol(qber=q)
        obs_bb = {"qber_Z": q, "qber_X": q, "p_sift": 0.5}
        t0 = time.perf_counter()
        r_bb = wlc_key_rate(p_bb, obs_bb, f_ec=f_ec)
        dt_bb = time.perf_counter() - t0
        a_bb = shor_preskill_rate(q, f_ec=f_ec)

        rows.append({
            "qber": q,
            "mdi_wlc": r_mdi.key_rate,
            "mdi_analytic": a_mdi,
            "mdi_abs_dev": abs(r_mdi.key_rate - a_mdi),
            "bb84_wlc": r_bb.key_rate,
            "bb84_analytic": a_bb,
            "bb84_abs_dev": abs(r_bb.key_rate - a_bb),
            "mdi_time": dt_mdi,
            "bb84_time": dt_bb,
            "mdi_gap": r_mdi.duality_gap,
            "bb84_gap": r_bb.duality_gap,
        })
        print(
            f"  QBER={q:.3f}  mdi(WLC={r_mdi.key_rate:+.6f} "
            f"a={a_mdi:+.6f} |d|={abs(r_mdi.key_rate-a_mdi):.2e})  "
            f"ratio_mdi/bb84={r_mdi.key_rate/r_bb.key_rate if abs(r_bb.key_rate)>1e-12 else float('nan'):.4f}"
        )

    mdi_max_dev = max(r["mdi_abs_dev"] for r in rows)
    bb84_max_dev = max(r["bb84_abs_dev"] for r in rows)
    print(f"\n[m2_mdi] Max |WLC - analytic|  MDI:  {mdi_max_dev:.3e}")
    print(f"[m2_mdi] Max |WLC - analytic|  BB84: {bb84_max_dev:.3e}")

    # Persist
    (REPO / "data").mkdir(exist_ok=True)
    out_json = {
        "preferred_solver": solver,
        "mosek_available": mosek,
        "f_ec": f_ec,
        "rows": rows,
        "mdi_max_abs_dev": mdi_max_dev,
        "bb84_max_abs_dev": bb84_max_dev,
    }
    with open(REPO / "data" / "m2_mdi_sweep.json", "w") as fh:
        json.dump(out_json, fh, indent=2)
    print(f"[m2_mdi] Data saved → data/m2_mdi_sweep.json")

    # ---- Figure ----
    (REPO / "docs" / "figures").mkdir(parents=True, exist_ok=True)
    qber_pct = qbers * 100
    mdi_wlc = np.array([r["mdi_wlc"] for r in rows])
    mdi_ana = np.array([r["mdi_analytic"] for r in rows])
    bb_wlc = np.array([r["bb84_wlc"] for r in rows])
    bb_ana = np.array([r["bb84_analytic"] for r in rows])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(qber_pct, bb_ana, "k-", label="BB84 Shor-Preskill")
    ax.plot(qber_pct, bb_wlc, "ko", markersize=4, label=f"BB84 WLC [{solver}]")
    ax.plot(qber_pct, mdi_ana, "g-", label="MDI ideal (BB84/2)")
    ax.plot(qber_pct, mdi_wlc, "g^", markersize=5, label=f"MDI WLC [{solver}]")
    ax.axhline(0, color="gray", lw=0.8, ls=":")
    ax.axvline(11.0, color="red", lw=0.8, ls="--", alpha=0.5, label="Threshold ≈ 11%")
    ax.set_xlabel("QBER (%)")
    ax.set_ylabel("Key rate (bit/signal)")
    ax.set_title(f"BB84 vs ideal MDI-QKD (f_ec={f_ec})")
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9, loc="upper right")
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(REPO / "docs" / "figures" / f"m2_mdi_vs_bb84.{ext}", dpi=150)
    plt.close(fig)
    print("[m2_mdi] Figure saved → docs/figures/m2_mdi_vs_bb84.{pdf,png}")
    print("[m2_mdi] DONE.")


if __name__ == "__main__":
    main()
