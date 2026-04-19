"""Reproduce Winick-Lütkenhaus-Coles 2018 Fig.3 — WLC key rate for BB84 with
symmetric depolarising channel, QBER ∈ [0, 11%].

Per WLC 2018 Fig.3 (left panel): the key rate is plotted as a function of
QBER with f_ec = 1.0 and f_ec = 1.16 for BB84 (Z and X bases equiprobable,
symmetric depolarising channel).

This script produces a Phase 0 integration figure combining:
  * BB84 WLC SDP(f_ec = 1.0, 1.16)
  * Shor-Preskill analytic comparison
  * six-state comparison (for the PROSPECTUS context)
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
import matplotlib.ticker as mticker

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from qkdx.analytic.shor_preskill import shor_preskill_rate
from qkdx.analytic.six_state import six_state_rate
from qkdx.analytic.gllp import mdi_ideal_symmetric_rate
from qkdx.numerics.wlc import wlc_key_rate
from qkdx.protocols.bb84 import build_bb84_protocol
from qkdx.protocols.sixstate import build_sixstate_protocol
from qkdx.protocols.mdi import build_mdi_protocol
from qkdx.utils.solvers import preferred_solver


def main() -> None:
    solver = preferred_solver()
    print(f"[p0_fig3] Preferred solver: {solver}")

    qbers = np.linspace(0.0, 0.12, 25)
    rows: list[dict] = []

    for q in qbers:
        q = float(q)
        row = {"qber": q}

        # BB84 at f_ec = 1.0 and 1.16
        for f_ec in [1.0, 1.16]:
            p = build_bb84_protocol(qber=q)
            obs = {"qber_Z": q, "qber_X": q, "p_sift": 0.5}
            res = wlc_key_rate(p, obs, f_ec=f_ec)
            row[f"bb84_wlc_fec{f_ec}"] = res.key_rate
            row[f"bb84_sp_fec{f_ec}"] = shor_preskill_rate(q, f_ec=f_ec)

        # Six-state at f_ec = 1.0
        p6 = build_sixstate_protocol(qber=q)
        obs6 = {"qber_Z": q, "qber_X": q, "qber_Y": q, "p_sift": 1.0 / 3.0}
        r6 = wlc_key_rate(p6, obs6, f_ec=1.0)
        row["six_wlc"] = r6.key_rate
        row["six_analytic"] = six_state_rate(q, f_ec=1.0)

        # MDI ideal at f_ec = 1.0
        pm = build_mdi_protocol(qber=q, p_sift=0.25)
        obsm = {"qber_Z": q, "qber_X": q, "p_sift": 0.25}
        rm = wlc_key_rate(pm, obsm, f_ec=1.0)
        row["mdi_wlc"] = rm.key_rate
        row["mdi_analytic"] = mdi_ideal_symmetric_rate(q, f_ec=1.0)

        rows.append(row)
        print(
            f"  QBER={q:.3f}  BB84(fec=1)={row['bb84_wlc_fec1.0']:+.4f}  "
            f"six={row['six_wlc']:+.4f}  MDI={row['mdi_wlc']:+.4f}"
        )

    # Save
    (REPO / "data").mkdir(exist_ok=True)
    with open(REPO / "data" / "phase0_winick_fig3.json", "w") as fh:
        json.dump({"solver": solver, "rows": rows}, fh, indent=2)
    print(f"[p0_fig3] Data → data/phase0_winick_fig3.json")

    # Plot
    (REPO / "docs" / "figures").mkdir(parents=True, exist_ok=True)
    q_pct = qbers * 100
    fig, ax = plt.subplots(figsize=(8, 5.5))
    bb84_wlc_1 = np.array([r["bb84_wlc_fec1.0"] for r in rows])
    bb84_wlc_116 = np.array([r["bb84_wlc_fec1.16"] for r in rows])
    six_wlc = np.array([r["six_wlc"] for r in rows])
    mdi_wlc = np.array([r["mdi_wlc"] for r in rows])

    ax.plot(q_pct, bb84_wlc_1, "b-o", markersize=4, label=f"BB84 WLC, f_ec=1.0 [{solver}]")
    ax.plot(q_pct, bb84_wlc_116, "b--s", markersize=4, label="BB84 WLC, f_ec=1.16")
    ax.plot(q_pct, six_wlc, "g-^", markersize=4, label="Six-state WLC, f_ec=1.0")
    ax.plot(q_pct, mdi_wlc, "r-d", markersize=4, label="MDI ideal WLC, f_ec=1.0")

    ax.axhline(0, color="gray", lw=0.8, ls=":")
    ax.axvline(11.0, color="red", lw=0.5, ls="--", alpha=0.5)
    ax.axvline(12.62, color="purple", lw=0.5, ls="--", alpha=0.5)
    ax.set_xlabel("QBER (%)")
    ax.set_ylabel("Key rate (bit/signal)")
    ax.set_title("Phase 0 Integration: BB84 / Six-state / MDI via WLC SDP\n"
                 "(Winick-Lütkenhaus-Coles 2018 Fig.3 reproduction)")
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=9)
    ax.set_xlim(0, 12.5)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(REPO / "docs" / "figures" / f"phase0_winick_fig3.{ext}", dpi=150)
    plt.close(fig)
    print("[p0_fig3] Figure → docs/figures/phase0_winick_fig3.{pdf,png}")
    print("[p0_fig3] DONE.")


if __name__ == "__main__":
    main()
