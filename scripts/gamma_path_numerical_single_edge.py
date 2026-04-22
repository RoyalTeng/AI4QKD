"""γ path numerical toy analog: single-edge PLOB on E_1 under amp-damp.

γ path (Log 07 §4.5 minimal baseline):
  R_A-B ≤ K_A-C_single-edge(E_1) + data-processing transfer

Target for γ: $R \leq E_R^\infty(\mathcal{E}_1)$ for single amp-damp channel.

For amp-damp channel with γ = 1 - η:
- Choi state = (I ⊗ N)(|Φ+⟩⟨Φ+|)
- Compute log-negativity (upper bound on E_R)

Compare with Pirandola 2019 trusted-relay at symmetric η_A = η_B = η_arm:
  Pirandola_sym = -log(1 - sqrt(η^2)) = -log(1 - η) = PLOB single-edge at η

So γ bound via single-edge PLOB on E_1 = Pirandola single-edge (trivially
same formula). The γ path doesn't claim numerical tightening vs Pirandola
(per Log 07 §4.5 "最小可信 baseline"), only provides rigorous derivation
via data-processing monotonicity.

Output: log_neg(E_1) vs -log(1-η) for qubit amp-damp.
"""
from __future__ import annotations

import math
import numpy as np


def kraus_amp_damp(gamma: float) -> list[np.ndarray]:
    K0 = np.array([[1.0, 0.0], [0.0, math.sqrt(1.0 - gamma)]], dtype=np.complex128)
    K1 = np.array([[0.0, math.sqrt(gamma)], [0.0, 0.0]], dtype=np.complex128)
    return [K0, K1]


def choi_state(kraus: list[np.ndarray], dim_in: int) -> np.ndarray:
    phi_p = np.zeros(dim_in * dim_in, dtype=np.complex128)
    for i in range(dim_in):
        phi_p[i * dim_in + i] = 1.0 / math.sqrt(dim_in)
    rho = np.outer(phi_p, phi_p.conj())
    dim_out = kraus[0].shape[0]
    result = np.zeros((dim_in * dim_out, dim_in * dim_out), dtype=np.complex128)
    for K in kraus:
        op = np.kron(np.eye(dim_in, dtype=np.complex128), K)
        result += op @ rho @ op.conj().T
    return result


def log_neg(rho: np.ndarray, dim_A: int, dim_B: int) -> float:
    T = rho.reshape(dim_A, dim_B, dim_A, dim_B).transpose(0, 3, 2, 1).reshape(dim_A * dim_B, dim_A * dim_B)
    eigs = np.linalg.eigvalsh(T)
    tn = np.abs(eigs).sum()
    if tn < 1e-12:
        return -math.inf
    return math.log2(tn)


def pirandola_single_edge(eta: float) -> float:
    return -math.log2(1.0 - eta)


def main():
    print("γ path toy numerical: single-edge amp-damp log-negativity vs Pirandola single-edge")
    print()
    print(f"{'η_arm':>8} {'LN(E_1)':>10} {'Pir_single':>11} {'ratio':>8}")

    import csv, os
    rows = []
    for eta_arm in [0.99, 0.9, 0.7, 0.5, 0.316, 0.1, 0.0316, 0.01, 0.001]:
        K = kraus_amp_damp(1.0 - eta_arm)
        rho = choi_state(K, dim_in=2)
        ln = log_neg(rho, 2, 2)
        pir = pirandola_single_edge(eta_arm)
        ratio = ln / pir if pir > 0 else float("inf")
        print(f"{eta_arm:>8.4f} {ln:>10.6f} {pir:>11.4f} {ratio:>8.4f}")
        rows.append({"eta_arm": eta_arm, "LN_amp_damp": ln, "Pirandola_single": pir, "ratio": ratio})

    csv_path = os.path.expanduser("~/Desktop/ai4qkd (1)/AI4QKD/docs/research/data/gamma_path_single_edge_toy.csv")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nCSV saved to: {csv_path}")

    print()
    print("Interpretation:")
    print("  LN(E_1) = log-negativity of single amp-damp channel Choi state")
    print("  Pir_single = -log(1-η) (PLOB single-edge bound)")
    print("  ratio = LN / Pir")
    print()
    print("Note: γ path claims R ≤ E_R^∞(E_1), and E_R ≤ LN generally.")
    print("So γ bound ≤ LN(E_1). Pirandola single-edge is -log(1-η) (ref).")
    print()
    print("If ratio < 1: γ's single-channel LN IS already tighter than classical PLOB formula")
    print("             (because amp-damp qubit ≠ bosonic pure-loss exactly).")
    print("Both quantities refer to different abstract models; direct comparison is informational.")


if __name__ == "__main__":
    main()
