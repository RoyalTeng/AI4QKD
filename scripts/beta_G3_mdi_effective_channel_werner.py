"""β.G3 analytical: MDI effective channel via Werner state reduction.

Uses the project's Werner-reduction result ([CONJ] per mdi_werner_reduction.md v0.3):
  - Ideal symmetric MDI with channel loss η_arm on each arm + depolarizing noise
  - Post-BSM + Table I flip → effective state is Werner W_F' on (A, B)
  - F' = F_1² + (1-F_1)²/3, where F_1 = 1 - 3λ/4 (λ = depolarizing strength)

For β.G3, the question is: what is E_R (or log-negativity) of the effective channel
that takes (Alice virtual qubit, Bob virtual qubit) → conditional Werner W_F'(AB) | Charlie BSM success?

For pure loss only (no depolarizing): F_1 relates to η_arm via loss model.
This is a simplified Werner-level analysis.

The effective channel output is a Werner state with fidelity F' depending on η_arm.
Log-negativity of Werner state is known analytically.
"""
from __future__ import annotations

import math
import numpy as np


def log_neg_werner(F: float) -> float:
    """Log-negativity of Werner state with fidelity F to |Phi+>.

    Werner state eigenvalues (in Bell basis):
        F (for Phi+), (1-F)/3 x 3 (for other Bell states).

    Partial transpose reorganizes into eigenvalues:
        (1/2) * (F + (1-F)/3) = (2F+1)/6 (doubly degenerate, non-negative)
        (1/2) * (F - (1-F)/3) = (4F-1)/6 (possibly negative if F < 1/4)
        ... specifically, partial transpose spectrum is:
          {(2F+1)/6 x 3, -(4F-1)/6 x 1}
    For F > 1/4: negative eigenvalue is -(4F-1)/6.
    Trace norm = 3*(2F+1)/6 + (4F-1)/6 = (6F+3+4F-1)/6 = (10F+2)/6

    Wait, let me redo. For Werner state W_F in Bell basis:
      diag = [F, (1-F)/3, (1-F)/3, (1-F)/3] in order {Phi+, Phi-, Psi+, Psi-}

    Partial transpose on B swaps:
      |Phi+><Phi+| ↔ I/2 (off-Bell)
      Actually PT of Bell states permutes among themselves and Bell+I/2 mixing.

    More concretely, for Werner:
      W_F^{T_B} eigenvalues known:
        {(1+F)/2 × 2 (for matrices acting like identity in partial transpose subspace),
         (1-F)/2 (possibly negative)}

    Actually I realize the cleanest way is to compute numerically.
    """
    # Work in Bell basis for simplicity
    Phi_p = np.array([1.0, 0, 0, 1.0]) / math.sqrt(2)
    Phi_m = np.array([1.0, 0, 0, -1.0]) / math.sqrt(2)
    Psi_p = np.array([0, 1.0, 1.0, 0]) / math.sqrt(2)
    Psi_m = np.array([0, 1.0, -1.0, 0]) / math.sqrt(2)
    W = (F * np.outer(Phi_p, Phi_p.conj())
         + (1.0 - F) / 3.0 * (
             np.outer(Phi_m, Phi_m.conj())
             + np.outer(Psi_p, Psi_p.conj())
             + np.outer(Psi_m, Psi_m.conj())
         ))
    # Partial transpose on qubit B (second qubit of 4-dim Hilbert space |ij>)
    W4 = W.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)
    eigs = np.linalg.eigvalsh(W4)
    trace_norm = np.abs(eigs).sum()
    if trace_norm < 1e-12:
        return -math.inf
    return math.log2(trace_norm)


def e_r_werner_known(F: float) -> float:
    """E_R of Werner state — closed-form from Vedral-Plenio 1998 / Rains 1999.

    For F > 1/2 Werner: E_R = 1 - H_2(F) — wait no.
    Actually: E_R of Werner state with fidelity F (to max entangled) is:
      E_R(W_F) = 1 - H(F)    for F > 1/2
      E_R(W_F) = 0            for F ≤ 1/2  (separable)
    where H(F) = -F log F - (1-F) log (1-F)

    Ref: Rains 1999 / Vedral-Plenio 1998.
    """
    if F <= 0.5:
        return 0.0
    return 1.0 - (-F * math.log2(F) - (1.0 - F) * math.log2(1.0 - F))


def mdi_effective_F_prime(eta_arm: float) -> float:
    """MDI effective post-BSM Werner fidelity under ideal symmetric setting.

    Using project's Werner reduction (docs/proofs/mdi_werner_reduction.md v0.3):
      F_1 = 1 - 3λ/4   (after single-arm depolarizing)
      F' = F_1² + (1-F_1)²/3   (after entanglement swap)

    For pure loss (amp-damp) converted to depolarizing-equivalent:
      Pure loss ≠ depolarizing, but here we use a heuristic: λ ≈ 1-η_arm as a
      crude approximation; this is for DIRECTIONAL signal only.

    Returns F' (Werner fidelity of post-BSM conditional state).
    """
    lam = 1.0 - eta_arm  # heuristic: "loss fraction" treated as depolarizing
    F_1 = 1.0 - 3.0 * lam / 4.0
    F_prime = F_1 ** 2 + (1.0 - F_1) ** 2 / 3.0
    return F_prime


def pirandola_trusted_relay(eta_arm: float) -> float:
    """Pirandola 2019 trusted relay at symmetric η_A = η_B = η_arm."""
    return -math.log2(1.0 - eta_arm)  # (= -log2(1-sqrt(eta^2)) for symmetric)


def plob_single_edge(eta: float) -> float:
    return -math.log2(1.0 - eta)


def main():
    print("β.G3 MDI-effective (Werner) analytical: Charlie BSM LOCC effect on β bound")
    print("Uses project Werner reduction [CONJ]: post-BSM ≈ Werner W_{F'} with")
    print("  F_1 = 1 - 3λ/4, F' = F_1² + (1-F_1)²/3, where λ = 1-η_arm heuristic.")
    print()
    print(f"{'eta_arm':>10} {'F_1':>8} {'F_prime':>8} "
          f"{'log_neg_W_F''':>14} {'E_R(W_F'')':>11} "
          f"{'Pirandola':>11} {'E_R/Pir':>9}")

    for eta_arm in [0.95, 0.9, 0.7, 0.5, 0.316, 0.1, 0.0316, 0.01, 0.001]:
        F_1 = 1.0 - 3.0 * (1.0 - eta_arm) / 4.0
        F_prime = F_1 ** 2 + (1.0 - F_1) ** 2 / 3.0
        ln_w = log_neg_werner(F_prime)
        er_w = e_r_werner_known(F_prime)
        pir = pirandola_trusted_relay(eta_arm)
        ratio = er_w / pir if pir > 0 else float("inf")
        print(f"{eta_arm:>10.4f} {F_1:>8.4f} {F_prime:>8.4f} "
              f"{ln_w:>14.6f} {er_w:>11.6f} "
              f"{pir:>11.4f} {ratio:>9.4f}")

    print()
    print("Interpretation:")
    print("  - E_R(W_F') = conditional state entanglement after Charlie BSM success")
    print("  - This is the ACTUAL β bound (含 Charlie BSM LOCC)")
    print("  - vs Pirandola min-cut trusted-relay = -log(1 - sqrt(eta^2)) = PLOB single-edge")
    print()
    print("Direction interpretation:")
    print("  - If E_R(W_F') / Pir < 1: β gives TIGHTER bound than Pirandola → 新定理 potential")
    print("  - If ratio ≥ 1: β no tighter than Pirandola in symmetric loss ideal model")
    print()
    print("Caveat (scope):")
    print("  - λ ≈ 1-η_arm heuristic treats loss as depolarizing (simplification)")
    print("  - Real bosonic pure-loss needs separate SDP")
    print("  - But directional signal useful for decision")


if __name__ == "__main__":
    main()
