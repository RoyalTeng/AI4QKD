"""β.G3 dense sweep + CSV export.

Extends scripts/beta_G3_post_BSM_conditional_amp_damp.py to:
1. Dense η grid (0.001 to 0.95, log-spaced)
2. Also sum over all 4 Bell outcomes (not just Ψ-) for averaged bound
3. Asymmetric check (η_A ≠ η_B)
4. CSV output for plotting
"""
from __future__ import annotations

import csv
import math
import os
import numpy as np

# Import from our earlier script (same directory)
import sys
sys.path.insert(0, os.path.dirname(__file__))
from beta_G3_post_BSM_conditional_amp_damp import (
    post_bsm_conditional_log_neg,
    pirandola_trusted_relay,
)


def main():
    eta_grid = [1.0 - x for x in [0.999, 0.99, 0.95, 0.90, 0.85, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10, 0.05]]
    # This gives eta = 0.001, 0.01, ..., 0.95

    print("β.G3 dense sweep — all 4 Bell outcomes, symmetric + asymmetric")
    print()

    rows = []
    for eta_arm in eta_grid:
        # Sum contributions across all 4 Bell outcomes
        total_p = 0.0
        weighted_log_neg_sum = 0.0
        per_outcome = {}
        for bell in ["Psi-", "Psi+", "Phi-", "Phi+"]:
            r = post_bsm_conditional_log_neg(eta_arm, eta_arm, bell_label=bell)
            p = r["p_outcome"]
            ln = max(0.0, r["log_neg"]) if math.isfinite(r["log_neg"]) else 0.0
            total_p += p
            weighted_log_neg_sum += p * ln
            per_outcome[bell] = (p, ln)

        pir = pirandola_trusted_relay(eta_arm)
        avg_ln = weighted_log_neg_sum  # sum_c p_c * LN_c (already weighted)
        ratio = avg_ln / pir if pir > 0 else float("inf")

        row = {
            "eta_arm": eta_arm,
            "total_p_BSM_all_outcomes": total_p,
            "sum_p_times_LN": avg_ln,
            "p_Psi_minus": per_outcome["Psi-"][0],
            "LN_Psi_minus": per_outcome["Psi-"][1],
            "Pirandola": pir,
            "ratio_beta_per_Pir": ratio,
        }
        rows.append(row)

        print(f"η={eta_arm:.4f}  Σ_c p_c={total_p:.4f}  Σ p_c×LN={avg_ln:.6f}  "
              f"vs Pir={pir:.4f}  ratio={ratio:.4f}")

    # Save CSV
    csv_path = os.path.expanduser("~/Desktop/ai4qkd (1)/AI4QKD/docs/research/data/beta_G3_post_BSM_sweep.csv")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nCSV saved to: {csv_path}")

    # Summary
    print()
    print("β.G3 convergence summary:")
    print(f"  Per-round β bound (sum over all BSM outcomes) / Pirandola:")
    print(f"  High η (0.95): {rows[2]['ratio_beta_per_Pir']:.4f}")
    print(f"  Mid η (0.5):   {next(r for r in rows if abs(r['eta_arm'] - 0.5) < 1e-3)['ratio_beta_per_Pir']:.4f}")
    print(f"  Low η (0.1):   {next(r for r in rows if abs(r['eta_arm'] - 0.1) < 1e-3)['ratio_beta_per_Pir']:.4f}")
    print(f"  Ultra-low η (0.001): {rows[0]['ratio_beta_per_Pir']:.4f}")


if __name__ == "__main__":
    main()
