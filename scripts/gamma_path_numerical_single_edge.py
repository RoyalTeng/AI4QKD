"""γ path toy Choi-state diagnostic: single amp-damp channel log-negativity.

**Scope**: toy Choi-state numerical diagnostic ONLY, 非 γ path derivation.

γ path (Log 07 §4.5) 的 formal target 是:
  R ≤ E_R^∞(E_1) via single-edge PLOB + data-processing inequality (DPI)

**重要 caveat**: γ path 的 DPI transfer step 仍是 [CONJ] target lemma (见
[docs/proofs/umr_path_gamma_v0_4_derivation.md](../docs/proofs/umr_path_gamma_v0_4_derivation.md)
v0.5 §6.1 γ.B.G1)，**未 formal established**。本 script 不 establish γ derivation。

本 script 仅 compute: single amp-damp channel Choi state 的 log-negativity，
作为 qubit toy diagnostic 对比 Pirandola single-edge -log(1-η)。

**未**声称:
- LN(E_1) = γ bound (需 channel-to-state reduction lemma，本 script 未含)
- γ path 的 rigorous 性 (DPI lemma 仍 open)
- formal β vs γ 序列

Output: log_neg(E_1 Choi state) vs -log(1-η) — toy diagnostic only.
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
    print("Interpretation (toy diagnostic only):")
    print("  LN_Choi(E_1) = log-negativity of single amp-damp channel Choi state (toy)")
    print("  Pir_single   = -log(1-η) (bosonic single-edge PLOB baseline, ref)")
    print("  ratio        = LN_Choi / Pir_single (informational)")
    print()
    print("Caveats:")
    print("  - LN_Choi is NOT the γ bound.  γ formal target E_R^∞(E_1) requires")
    print("    channel-to-state reduction lemma (NOT provided by this script).")
    print("  - amp-damp qubit ≠ bosonic pure-loss; different abstract models.")
    print("  - Direct numeric comparison serves as descriptive companion to β.G3 toy only,")
    print("    and does NOT predict the formal β-vs-γ ordering.")


if __name__ == "__main__":
    main()
