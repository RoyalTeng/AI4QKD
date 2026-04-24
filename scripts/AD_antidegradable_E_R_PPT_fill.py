"""Fill in E_R^PPT SDP points for AD channel γ ∈ [0.5, 1.0] (anti-degradable region).

Extends existing sparse grid (0.5, 0.7, 0.9 already in qubit_E_R_PPT_SDP_all_4.csv)
with γ = 0.55, 0.60, 0.65, 0.75, 0.80, 0.85, 0.95 for finer anti-degradable coverage.

Data used in AD_anti_degradable_E_R_PPT_2026-04-24.md.

Output:
  docs/research/data/AD_antidegradable_E_R_PPT_fill.csv  (new points only)
"""
from __future__ import annotations

import csv
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from qkdx.numerics.upper_bound import (
    analytic_log_neg_amplitude_damping,
    e_r_channel_ppt,
    kraus_amplitude_damping_qubit,
    quantum_capacity_amplitude_damping_degradable,
)


def main():
    new_gammas = [0.55, 0.60, 0.65, 0.75, 0.80, 0.85, 0.95]
    rows = []

    print("E_R^PPT SDP sweep (AD anti-degradable fill-in)...")
    for gamma in new_gammas:
        t0 = time.time()
        kraus = kraus_amplitude_damping_qubit(gamma)
        result = e_r_channel_ppt(kraus, dim_A=2)
        er = float(result["E_R_channel_bits"])
        ln = analytic_log_neg_amplitude_damping(gamma)
        q = quantum_capacity_amplitude_damping_degradable(gamma)
        elapsed = time.time() - t0
        rows.append((gamma, er, ln, q, elapsed))
        status = "anti-degradable" if gamma > 0.5 else "degradable"
        print(f"  γ={gamma}: E_R^PPT={er:.4f}, log_neg={ln:.4f}, Q={q:.4f}  [{status}]  ({elapsed:.1f}s)")

    out_csv = REPO / "docs" / "research" / "data" / "AD_antidegradable_E_R_PPT_fill.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["gamma", "E_R_PPT_SDP", "log_neg_analytic", "Q_LB_on_K2way", "sdp_time_s"])
        for g, er, ln, q, t in rows:
            w.writerow([f"{g:.4f}", f"{er:.6f}", f"{ln:.6f}", f"{q:.6f}", f"{t:.2f}"])

    print()
    print(f"  CSV: docs/research/data/AD_antidegradable_E_R_PPT_fill.csv")
    print()
    print("Anti-degradable (γ > 0.5): Q=0 but E_R^PPT > 0 gives nontrivial UB on K^{↔}")


if __name__ == "__main__":
    main()
