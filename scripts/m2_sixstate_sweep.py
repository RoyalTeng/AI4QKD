"""Generate M2 six-state QBER sweep: WLC SDP vs analytic."""
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

from qkdx.analytic.six_state import six_state_rate
from qkdx.analytic.shor_preskill import shor_preskill_rate
from qkdx.numerics.wlc import wlc_key_rate
from qkdx.protocols.bb84 import build_bb84_protocol
from qkdx.protocols.sixstate import build_sixstate_protocol
from qkdx.utils.solvers import preferred_solver, has_mosek


def main() -> None:
    solver = preferred_solver()
    mosek = has_mosek()
    print(f"[m2_six] Preferred solver: {solver}  MOSEK available: {mosek}")

    # Six-state: threshold ~12.62%, sweep up to 13%
    qbers = np.linspace(0.0, 0.13, 27)
    f_ec = 1.0

    rows: list[dict] = []
    for q in qbers:
        q = float(q)
        # six-state
        p6 = build_sixstate_protocol(qber=q)
        obs6 = {"qber_Z": q, "qber_X": q, "qber_Y": q, "p_sift": 1.0 / 3.0}
        t0 = time.perf_counter()
        r6 = wlc_key_rate(p6, obs6, f_ec=f_ec)
        dt6 = time.perf_counter() - t0
        a6 = six_state_rate(q, f_ec=f_ec)
        # BB84 comparison (sifted per-signal)
        pb = build_bb84_protocol(qber=q)
        obsb = {"qber_Z": q, "qber_X": q, "p_sift": 0.5}
        t0 = time.perf_counter()
        rb = wlc_key_rate(pb, obsb, f_ec=f_ec)
        dtb = time.perf_counter() - t0
        ab = shor_preskill_rate(q, f_ec=f_ec)

        rows.append({
            "qber": q,
            "six_wlc": r6.key_rate,
            "six_analytic": a6,
            "bb84_wlc": rb.key_rate,
            "bb84_analytic": ab,
            "six_abs_dev": abs(r6.key_rate - a6),
            "bb84_abs_dev": abs(rb.key_rate - ab),
            "six_time": dt6,
            "bb84_time": dtb,
            "six_gap": r6.duality_gap,
            "bb84_gap": rb.duality_gap,
        })
        print(
            f"  QBER={q:.3f}  six(WLC={r6.key_rate:+.6f} SP={a6:+.6f} |d|={abs(r6.key_rate-a6):.2e})  "
            f"bb84(WLC={rb.key_rate:+.6f} SP={ab:+.6f} |d|={abs(rb.key_rate-ab):.2e})"
        )

    six_max_dev = max(r["six_abs_dev"] for r in rows)
    bb84_max_dev = max(r["bb84_abs_dev"] for r in rows)
    print(f"\n[m2_six] Max |WLC - analytic|  six-state: {six_max_dev:.3e}")
    print(f"[m2_six] Max |WLC - analytic|  bb84:      {bb84_max_dev:.3e}")

    # Persist
    (REPO / "data").mkdir(exist_ok=True)
    out_json = {
        "preferred_solver": solver,
        "mosek_available": mosek,
        "f_ec": f_ec,
        "rows": rows,
        "six_max_abs_dev": six_max_dev,
        "bb84_max_abs_dev": bb84_max_dev,
    }
    with open(REPO / "data" / "m2_sixstate_sweep.json", "w") as fh:
        json.dump(out_json, fh, indent=2)
    print(f"[m2_six] Data saved → data/m2_sixstate_sweep.json")

    # ---- Figure: rate curves ----
    (REPO / "docs" / "figures").mkdir(parents=True, exist_ok=True)
    qber_pct = qbers * 100
    six_wlc = np.array([r["six_wlc"] for r in rows])
    six_ana = np.array([r["six_analytic"] for r in rows])
    bb84_wlc = np.array([r["bb84_wlc"] for r in rows])
    bb84_ana = np.array([r["bb84_analytic"] for r in rows])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(qber_pct, bb84_ana, "k-", label="BB84 Shor-Preskill")
    ax.plot(qber_pct, bb84_wlc, "ko", markersize=4, label=f"BB84 WLC [{solver}]")
    ax.plot(qber_pct, six_ana, "b-", label="Six-state analytic")
    ax.plot(qber_pct, six_wlc, "bs", markersize=4, label=f"Six-state WLC [{solver}]")
    ax.axhline(0, color="gray", lw=0.8, ls=":")
    ax.axvline(11.0, color="red", lw=0.8, ls="--", alpha=0.5, label="BB84 thresh ≈ 11%")
    ax.axvline(12.62, color="purple", lw=0.8, ls="--", alpha=0.5, label="Six-state thresh ≈ 12.62%")
    ax.set_xlabel("QBER (%)")
    ax.set_ylabel("Key rate (bit/signal)")
    ax.set_title(f"BB84 vs Six-State (f_ec={f_ec})")
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9, loc="upper right")
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(REPO / "docs" / "figures" / f"m2_sixstate_vs_bb84.{ext}", dpi=150)
    plt.close(fig)
    print("[m2_six] Figure saved → docs/figures/m2_sixstate_vs_bb84.{pdf,png}")
    print("[m2_six] DONE.")


if __name__ == "__main__":
    main()
