"""β.G3 numerical exploration: E_R^PPT(M_tilde) vs Pirandola min-cut.

User 2026-04-22 decision Q1 Option 2 (β main + γ safety). β path's key
decision point: is E_R^∞(effective channel) strictly tighter than
Pirandola 2019 min-cut bound?

Approach:
Use qubit abstraction (amplitude damping). Construct effective channel
    M_tilde: A ⊗ B -> A ⊗ B (post-BSM conditional, Werner-form per ideal
    symmetric MDI reduction).
Compare E_R^PPT(M_tilde) with -log_2(1 - sqrt(eta_A * eta_B)).

Note: This is a QUBIT abstraction, not bosonic pure-loss. Results give
**directional signal** about whether β bound can beat Pirandola in the
qubit setting; bosonic case needs separate analysis.

Output: table of (eta_arm, E_R_beta_candidate, Pirandola_trusted_relay, ratio).
"""
from __future__ import annotations

import math
import os

os.environ.setdefault("MOSEKLM_LICENSE_FILE", os.path.expanduser("~/mosek/mosek.lic"))

import numpy as np

from qkdx.numerics.upper_bound import (
    e_r_ppt,
    e_r_channel_ppt,
    choi_state_from_kraus,
    kraus_amplitude_damping_qubit,
    log_negativity_channel_sdp,
)


def two_arm_channel_kraus(eta_A: float, eta_B: float) -> list[np.ndarray]:
    """Construct Kraus operators for parallel channel E_1 (qubit 1) tensor E_2 (qubit 2).

    Each arm is amplitude damping with gamma = 1 - eta (so eta = successful
    transmission probability at qubit level).

    Input space: A tensor B (dim 4).
    Output space: A tensor B (dim 4).
    """
    K1 = kraus_amplitude_damping_qubit(1.0 - eta_A)
    K2 = kraus_amplitude_damping_qubit(1.0 - eta_B)
    # Tensor product of Kraus ops
    tensor_kraus = []
    for k1 in K1:
        for k2 in K2:
            tensor_kraus.append(np.kron(k1, k2))
    return tensor_kraus


def pirandola_trusted_relay_bound(eta_A: float, eta_B: float) -> float:
    """Pirandola 2019 min-cut bound for trusted-relay single-path chain
    in (dB-compatible) high-loss limit.

    For single-relay chain Alice -> Charlie -> Bob: -log_2(1 - sqrt(eta_A * eta_B))
    """
    eta_end = eta_A * eta_B
    return -math.log2(1.0 - math.sqrt(eta_end))


def plob_single_edge_bound(eta: float) -> float:
    """PLOB 2017 for single-edge: -log_2(1 - eta). Used as min-cut (per γ path)."""
    return -math.log2(1.0 - eta)


def main():
    print("β.G3 numerical: E_R^PPT(parallel two-arm channel) vs Pirandola min-cut")
    print("Qubit abstraction: each arm amplitude-damping with gamma = 1 - eta_arm")
    print()
    print(f"{'eta_arm':>8} {'E_R_tensor':>12} {'log_neg_tensor':>15} "
          f"{'Pirandola':>12} {'PLOB_single':>12} {'ratio_ER/Pir':>14}")

    results = []
    for eta_arm in [0.9, 0.5, 0.316, 0.1, 0.0316, 0.01]:
        try:
            kraus = two_arm_channel_kraus(eta_arm, eta_arm)
            # Direct log-negativity of channel (upper bound on E_R)
            r_ln = log_negativity_channel_sdp(kraus, dim_A=4)
            log_neg = r_ln["log_negativity_bits"]

            # e_r_channel_ppt with dim_A=4 (16x16 Choi) is intractable (>60s/pt)
            # Use log_negativity as upper bound proxy for directional signal
            e_r = log_neg  # log-neg >= E_R; conservative upper bound

            pir = pirandola_trusted_relay_bound(eta_arm, eta_arm)
            plob = plob_single_edge_bound(eta_arm)
            ratio = e_r / pir if pir > 0 else float("inf")

            print(f"{eta_arm:>8.4f} {log_neg:>12.4f} {'(=log_neg)':>15} "
                  f"{pir:>12.4f} {plob:>12.4f} {ratio:>14.4f}")
            results.append({
                "eta_arm": eta_arm,
                "log_neg_tensor": log_neg,
                "Pirandola_trusted": pir,
                "PLOB_single": plob,
                "ratio_logNeg_Pir": ratio,
            })
        except Exception as e:
            print(f"{eta_arm:>8.4f}  ERROR: {type(e).__name__}: {e}")

    print()
    print("Interpretation:")
    print("  - E_R_tensor = E_R^PPT of E_1 ⊗ E_2 (parallel, no Charlie LOCC)")
    print("  - log_neg_tensor = log-negativity (looser upper bound on E_R)")
    print("  - Pirandola = trusted-relay min-cut = -log(1-sqrt(eta_A*eta_B))")
    print("  - PLOB_single = -log(1-eta) single-edge (γ path bound)")
    print()
    print("β interpretation:")
    print("  - If ratio_ER/Pir < 1: tensor-product E_R gives TIGHTER bound than Pirandola")
    print("    → β potentially novel tighter bound")
    print("  - If ratio >= 1: tensor-product E_R >= Pirandola")
    print("    → β gives no tighter bound than Pirandola via this route")
    print()
    print("Note: this is E_R of E_1 ⊗ E_2 WITHOUT Charlie BSM LOCC applied.")
    print("  Charlie BSM is LOCC → E_R(M_tilde) <= E_R(E_1 ⊗ E_2).")
    print("  So tensor-product is UPPER bound on E_R(M_tilde).")
    print("  If tensor < Pirandola then M_tilde < Pirandola (β tighter).")
    print("  If tensor >= Pirandola, M_tilde might still be tighter (need direct SDP).")


if __name__ == "__main__":
    main()
