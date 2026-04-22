"""β.G3: post-BSM Alice-Bob conditional state under amp-damp (pure-loss) model.

Closer to actual pure-loss bosonic scenario than the depolarizing Werner heuristic.

Procedure:
1. Initial state: |Φ+⟩_{A,A'} ⊗ |Φ+⟩_{B,B'}   (Alice + Bob each prepares EB pair)
2. Apply amp-damp_γ on A' and B' (each arm, γ = 1 - η_arm)
3. Project (A', B') onto |Ψ-⟩_{A'B'}  (Bell projection, BSM success)
4. Trace out (A', B') → conditional state ρ_{AB}
5. Compute log-negativity of ρ_{AB} (via partial transpose eigenvalues)

This gives the actual conditional entanglement shared by Alice-Bob after
successful BSM outcome in a qubit-abstracted pure-loss model.
"""
from __future__ import annotations

import math
import numpy as np


def kraus_amp_damp(gamma: float) -> list[np.ndarray]:
    """Qubit amp-damping Kraus (pure-loss analog)."""
    K0 = np.array([[1.0, 0.0], [0.0, math.sqrt(1.0 - gamma)]], dtype=np.complex128)
    K1 = np.array([[0.0, math.sqrt(gamma)], [0.0, 0.0]], dtype=np.complex128)
    return [K0, K1]


def apply_channel_on_qubit(rho: np.ndarray, kraus: list[np.ndarray], qubit_idx: int, n_qubits: int) -> np.ndarray:
    """Apply qubit channel `kraus` on qubit at `qubit_idx` in an n-qubit rho."""
    d = 2 ** n_qubits
    output = np.zeros((d, d), dtype=np.complex128)
    for K in kraus:
        # Build full operator: I ⊗ ... ⊗ K ⊗ ... ⊗ I with K at qubit_idx position
        ops = [np.eye(2, dtype=np.complex128) for _ in range(n_qubits)]
        ops[qubit_idx] = K
        full_K = ops[0]
        for op in ops[1:]:
            full_K = np.kron(full_K, op)
        output += full_K @ rho @ full_K.conj().T
    return output


def project_qubits_onto_bell(rho: np.ndarray, qubit_i: int, qubit_j: int, n_qubits: int, bell_label: str = "Psi-") -> np.ndarray:
    """Project qubits i, j onto specified Bell state; return unnormalized result + P(outcome)."""
    d = 2 ** n_qubits
    # Bell states
    bell_vecs = {
        "Phi+": np.array([1, 0, 0, 1]) / math.sqrt(2),
        "Phi-": np.array([1, 0, 0, -1]) / math.sqrt(2),
        "Psi+": np.array([0, 1, 1, 0]) / math.sqrt(2),
        "Psi-": np.array([0, 1, -1, 0]) / math.sqrt(2),
    }
    b = bell_vecs[bell_label]
    # Construct projector on qubits (i, j)
    bell_proj = np.outer(b, b.conj())
    # Place projector at qubits (i, j), identity elsewhere
    # For simplicity, assume i=n_qubits-2, j=n_qubits-1 (last two qubits)
    # For general indices, need qubit reordering — skip and assume last two
    assert qubit_i == n_qubits - 2 and qubit_j == n_qubits - 1
    rest_dim = 2 ** (n_qubits - 2)
    full_proj = np.kron(np.eye(rest_dim, dtype=np.complex128), bell_proj)
    rho_projected = full_proj @ rho @ full_proj
    p_outcome = float(np.trace(rho_projected).real)
    return rho_projected, p_outcome


def trace_out_last_two_qubits(rho: np.ndarray, n_qubits: int) -> np.ndarray:
    """Trace out last 2 qubits → leave (n-2)-qubit state."""
    d_keep = 2 ** (n_qubits - 2)
    d_trace = 4  # last 2 qubits = 4 dims
    # Reshape
    rho4 = rho.reshape(d_keep, d_trace, d_keep, d_trace)
    # Trace over traced dims (index 1 = 3)
    result = np.einsum("ijkj->ik", rho4)
    return result


def log_negativity(rho: np.ndarray, dim_A: int, dim_B: int) -> float:
    """Log-negativity of bipartite rho."""
    # Partial transpose on B
    T = rho.reshape(dim_A, dim_B, dim_A, dim_B).transpose(0, 3, 2, 1).reshape(dim_A * dim_B, dim_A * dim_B)
    eigs = np.linalg.eigvalsh(T)
    trace_norm = np.abs(eigs).sum()
    if trace_norm < 1e-12:
        return -math.inf
    return math.log2(trace_norm)


def post_bsm_conditional_log_neg(eta_A: float, eta_B: float, bell_label: str = "Psi-") -> dict:
    """Compute log-negativity of Alice-Bob conditional state after successful BSM."""
    # Qubit order: A, A', B, B'
    # Initial: |Phi+⟩_{A,A'} ⊗ |Phi+⟩_{B,B'}
    # But our projection assumes last 2 qubits. So order: A, B, A', B' (A'B' = qubits 2,3)
    # Build |Phi+⟩_{A,A'} ⊗ |Phi+⟩_{B,B'} in order (A, A', B, B'), then reorder to (A, B, A', B')
    Phi_p = np.array([1.0, 0, 0, 1.0]) / math.sqrt(2)
    psi_init = np.kron(Phi_p, Phi_p)  # dim 16, order (A, A', B, B')
    rho_init = np.outer(psi_init, psi_init.conj())  # 16x16 pure state

    # Reorder qubits: (A, A', B, B') → (A, B, A', B')
    # Positions 0,1,2,3 → 0,2,1,3
    t = rho_init.reshape(2, 2, 2, 2, 2, 2, 2, 2)
    t = t.transpose(0, 2, 1, 3, 4, 6, 5, 7)
    rho = t.reshape(16, 16)

    # Apply amp-damp on A' (qubit 2) and B' (qubit 3)
    K_A = kraus_amp_damp(1.0 - eta_A)
    K_B = kraus_amp_damp(1.0 - eta_B)
    rho = apply_channel_on_qubit(rho, K_A, qubit_idx=2, n_qubits=4)
    rho = apply_channel_on_qubit(rho, K_B, qubit_idx=3, n_qubits=4)

    # Project A'B' onto Bell
    rho_proj, p = project_qubits_onto_bell(rho, qubit_i=2, qubit_j=3, n_qubits=4, bell_label=bell_label)
    if p < 1e-15:
        return {"eta_A": eta_A, "eta_B": eta_B, "bell": bell_label, "p_outcome": 0.0,
                "log_neg": float("nan"), "fidelity_phi_plus": float("nan")}
    rho_cond = rho_proj / p  # normalized

    # Trace out A'B' → (A, B) state
    rho_AB = trace_out_last_two_qubits(rho_cond, n_qubits=4)
    # Compute log-negativity
    ln = log_negativity(rho_AB, dim_A=2, dim_B=2)

    # Also compute fidelity to |Phi+⟩ (for Werner comparison)
    Phi_p_AB = np.array([1.0, 0, 0, 1.0]) / math.sqrt(2)
    F_phi = float((Phi_p_AB.conj() @ rho_AB @ Phi_p_AB).real)

    return {"eta_A": eta_A, "eta_B": eta_B, "bell": bell_label,
            "p_outcome": p, "log_neg": ln, "fidelity_phi_plus": F_phi}


def pirandola_trusted_relay(eta_arm: float) -> float:
    return -math.log2(1.0 - eta_arm)


def main():
    print("β.G3 Alice-Bob post-BSM conditional state under amp-damp (pure-loss qubit analog)")
    print("Per-round β bound candidate: p_BSM × E_R(conditional) ≤ p_BSM × log_neg(cond)")
    print()
    print(f"{'eta_arm':>10} {'p_BSM':>8} {'log_neg(cond)':>15} "
          f"{'fid_to_Phi+':>13} {'Pirandola':>11} "
          f"{'p_BSM × LN':>12} {'ratio':>8}")

    for eta_arm in [0.95, 0.9, 0.7, 0.5, 0.316, 0.1, 0.0316, 0.01, 0.001]:
        r = post_bsm_conditional_log_neg(eta_arm, eta_arm, bell_label="Psi-")
        pir = pirandola_trusted_relay(eta_arm)
        per_round_bound = r["p_outcome"] * max(0.0, r["log_neg"]) if math.isfinite(r["log_neg"]) else 0.0
        ratio = per_round_bound / pir if pir > 0 else float("inf")
        print(f"{eta_arm:>10.4f} {r['p_outcome']:>8.4f} {r['log_neg']:>15.6f} "
              f"{r['fidelity_phi_plus']:>13.4f} {pir:>11.4f} "
              f"{per_round_bound:>12.6f} {ratio:>8.4f}")

    print()
    print("Interpretation:")
    print("  - p_BSM = probability of successful |Ψ-⟩ outcome on (A',B')")
    print("  - log_neg(cond) = log-negativity of conditional state on (A,B)")
    print("  - fid_to_Phi+ = ⟨Φ+|ρ_{AB}|Φ+⟩ — shows if state is Phi+-centered")
    print("  - p_BSM × LN = per-round β bound candidate")
    print("  - Pirandola per-round = -log(1 - η) used as baseline comparison")
    print()
    print("If p_BSM × LN < Pirandola: β gives TIGHTER bound in pure-loss qubit model")
    print("If ≥: β no advantage over Pirandola in this model")


if __name__ == "__main__":
    main()
