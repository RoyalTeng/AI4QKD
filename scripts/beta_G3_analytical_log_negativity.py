"""β.G3 analytical exploration: log-negativity of parallel two-arm amp-damping channel.

No MOSEK SDP — direct eigenvalue computation of partial-transpose Choi state.

Output: compares log-negativity of E_1 ⊗ E_2 with Pirandola 2019 min-cut bound.
Gives directional signal for whether β could give tighter bound than Pirandola.
"""
from __future__ import annotations

import math
import numpy as np


def kraus_amplitude_damping(gamma: float) -> list[np.ndarray]:
    """Qubit amp-damping channel: K0 = |0⟩⟨0| + √(1-γ)|1⟩⟨1|, K1 = √γ |0⟩⟨1|."""
    K0 = np.array([[1.0, 0.0], [0.0, math.sqrt(1.0 - gamma)]], dtype=np.complex128)
    K1 = np.array([[0.0, math.sqrt(gamma)], [0.0, 0.0]], dtype=np.complex128)
    return [K0, K1]


def choi_state_from_kraus(kraus: list[np.ndarray], dim_in: int) -> np.ndarray:
    """Choi state via (I ⊗ N)(|Φ+⟩⟨Φ+|) on dim_in ⊗ dim_in."""
    phi_plus = np.zeros(dim_in * dim_in, dtype=np.complex128)
    for i in range(dim_in):
        phi_plus[i * dim_in + i] = 1.0 / math.sqrt(dim_in)
    rho_AB = np.outer(phi_plus, phi_plus.conj())

    dim_out = kraus[0].shape[0]
    # Apply kraus on B subsystem: sum_k (I_A ⊗ K_k) rho (I_A ⊗ K_k^†)
    result = np.zeros((dim_in * dim_out, dim_in * dim_out), dtype=np.complex128)
    for K in kraus:
        op = np.kron(np.eye(dim_in, dtype=np.complex128), K)
        result += op @ rho_AB @ op.conj().T
    return result


def partial_transpose_B(rho: np.ndarray, dim_A: int, dim_B: int) -> np.ndarray:
    """Partial transpose on subsystem B."""
    T = rho.reshape(dim_A, dim_B, dim_A, dim_B)
    T = T.transpose(0, 3, 2, 1)  # swap B ket/bra
    return T.reshape(dim_A * dim_B, dim_A * dim_B)


def log_negativity(rho: np.ndarray, dim_A: int, dim_B: int) -> float:
    """Log-negativity: log_2(||rho^T_B||_1)."""
    rho_pt = partial_transpose_B(rho, dim_A, dim_B)
    eigs = np.linalg.eigvalsh(rho_pt)
    trace_norm = np.abs(eigs).sum()
    return math.log2(trace_norm)


def log_neg_amp_damp_single_qubit(gamma: float) -> float:
    """Single qubit amp-damp channel log-negativity (direct computation)."""
    kraus = kraus_amplitude_damping(gamma)
    rho = choi_state_from_kraus(kraus, dim_in=2)
    return log_negativity(rho, dim_A=2, dim_B=2)


def log_neg_tensor_two_arm(eta_A: float, eta_B: float) -> float:
    """Log-negativity of two-arm parallel channel E_1 ⊗ E_2 (4→4)."""
    gamma_A = 1.0 - eta_A
    gamma_B = 1.0 - eta_B
    K1 = kraus_amplitude_damping(gamma_A)
    K2 = kraus_amplitude_damping(gamma_B)
    # Tensor Kraus
    tensor_kraus = []
    for k1 in K1:
        for k2 in K2:
            tensor_kraus.append(np.kron(k1, k2))

    # Choi state on (A ⊗ A')_{in=4} ⊗ (A ⊗ A')_{out=4}
    rho = choi_state_from_kraus(tensor_kraus, dim_in=4)
    return log_negativity(rho, dim_A=4, dim_B=4)


def pirandola_trusted_relay(eta_A: float, eta_B: float) -> float:
    """Pirandola 2019 trusted-relay single-chain: -log(1 - sqrt(eta_A * eta_B))."""
    return -math.log2(1.0 - math.sqrt(eta_A * eta_B))


def plob_single_edge(eta: float) -> float:
    """PLOB 2017 single-edge: -log(1 - eta)."""
    return -math.log2(1.0 - eta)


def plob_full_bosonic_eta(eta: float) -> float:
    """PLOB pure-loss bosonic two-way private capacity = -log_2(1-eta)."""
    return -math.log2(1.0 - eta)


def main():
    print("β.G3 analytical: log-negativity of two-arm amp-damping channel vs bounds")
    print("Qubit abstraction (amp-damp on each arm); for qualitative signal only.")
    print()
    print(f"{'eta_arm':>8} {'LN_single':>10} {'LN_tensor':>10} "
          f"{'LN_addit_chk':>13} {'Pir_trust':>10} {'PLOB_single':>12} "
          f"{'LN/Pir':>8}")

    for eta_arm in [0.9, 0.7, 0.5, 0.316, 0.1, 0.0316, 0.01]:
        ln_single = log_neg_amp_damp_single_qubit(1.0 - eta_arm)
        ln_tensor = log_neg_tensor_two_arm(eta_arm, eta_arm)
        ln_additivity_check = 2 * ln_single  # expected if additive

        pir = pirandola_trusted_relay(eta_arm, eta_arm)
        plob = plob_single_edge(eta_arm)

        ratio = ln_tensor / pir if pir > 0 else float("inf")

        print(f"{eta_arm:>8.4f} {ln_single:>10.4f} {ln_tensor:>10.4f} "
              f"{ln_additivity_check:>13.4f} {pir:>10.4f} {plob:>12.4f} "
              f"{ratio:>8.4f}")

    print()
    print("Interpretation for β.G3:")
    print("  LN_single = log-neg of amp-damp (single-arm qubit channel)")
    print("  LN_tensor = log-neg of parallel tensor product E_1 ⊗ E_2 (β's upstream M_tilde bound)")
    print("  LN_addit_chk = 2*LN_single (additivity check)")
    print("  Pir_trust = -log(1 - sqrt(eta^2)) = -log(1 - eta) = PLOB single-edge at eta_arm")
    print("  Note: trusted-relay Pirandola bound at symmetric eta collapses to PLOB single-edge!")
    print()
    print("Key observation:")
    print("  - LN_tensor 代表 parallel two-arm channel 的 log-negativity (β upstream bound)")
    print("  - Charlie BSM is LOCC → E_R(M_tilde) ≤ E_R(E_1⊗E_2) ≤ LN_tensor")
    print("  - 如果 LN_tensor < Pirandola_trusted → β 潜在更紧")
    print("  - 如果 LN_tensor ≥ Pirandola → β 通过 tensor-product route 不 tighter")


if __name__ == "__main__":
    main()
