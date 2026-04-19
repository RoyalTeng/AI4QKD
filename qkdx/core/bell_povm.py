"""Bell-state measurement (BSM) channels for MDI-QKD and related protocols.

Two variants provided:

1. **Ideal 4-outcome BSM** (`ideal_bell_bsm`): full Bell-basis projective
   measurement distinguishing all 4 outcomes {Φ+, Φ-, Ψ+, Ψ-}. Not physically
   realisable with linear optics + photon-number measurement alone, but serves
   as a mathematical upper reference.

2. **Linear-optic BSM** (`linear_optic_bell_bsm`): realistic BSM distinguishing
   only {Φ+, Ψ-} outcomes as "success", with the other 2 outcomes merged into
   a single "fail" classical label.  This is the physically meaningful
   channel in MDI-QKD (Lo-Curty-Qi 2012).

Both factories return a `KrausMap` with:
    - `dim_in = 4` (A' ⊗ B' = 2 ⊗ 2, combined signal register)
    - `dim_out = 4` for ideal, `dim_out = 3` for linear-optic
    - Kraus operators `K_k = |k⟩_C ⟨ψ_k|`, where |k⟩_C is the classical
      announcement register and |ψ_k⟩ is the k-th Bell state (or fail subspace)

References:
- Lo-Curty-Qi 2012, PRL 108:130503
- docs/literature/MDI-QKD.md (Level 2-3 memo, Phase 0)
- docs/msen/mdi-formulation.md §1.2 (Bell POVM channel layer)
"""
from __future__ import annotations

import numpy as np

from qkdx.core.hilbert import Matrix
from qkdx.core.operators import KrausMap


def _bell_ket(label: str) -> Matrix:
    """Return the 4-dim ket for a Bell state.

    Convention: |Φ+⟩ = (|00⟩+|11⟩)/√2, |Φ-⟩ = (|00⟩-|11⟩)/√2,
                |Ψ+⟩ = (|01⟩+|10⟩)/√2, |Ψ-⟩ = (|01⟩-|10⟩)/√2.
    """
    root2 = np.sqrt(2.0)
    psi = np.zeros((4, 1), dtype=np.complex128)
    if label == "Phi+":
        psi[0, 0] = 1 / root2
        psi[3, 0] = 1 / root2
    elif label == "Phi-":
        psi[0, 0] = 1 / root2
        psi[3, 0] = -1 / root2
    elif label == "Psi+":
        psi[1, 0] = 1 / root2
        psi[2, 0] = 1 / root2
    elif label == "Psi-":
        psi[1, 0] = 1 / root2
        psi[2, 0] = -1 / root2
    else:
        raise ValueError(f"unknown Bell label {label!r}; use Phi+, Phi-, Psi+, Psi-")
    return psi


def ideal_bell_bsm() -> KrausMap:
    """Ideal 4-outcome projective Bell measurement on 2-qubit input.

    Kraus operators:
        K_0 = |0⟩_C ⟨Φ+|,  K_1 = |1⟩_C ⟨Φ-|,
        K_2 = |2⟩_C ⟨Ψ+|,  K_3 = |3⟩_C ⟨Ψ-|.

    Applied to any 2-qubit ρ, yields a 4-dim classical output density
    (diagonal) with probabilities p_k = ⟨ψ_k| ρ |ψ_k⟩.

    Trace-preserving: Σ_k K_k† K_k = Σ_k |ψ_k⟩⟨ψ_k| = I_4 (Bell states
    form an orthonormal basis of C^4).
    """
    labels = ["Phi+", "Phi-", "Psi+", "Psi-"]
    kraus_ops = []
    for k, lbl in enumerate(labels):
        bra = _bell_ket(lbl).conj().T  # shape (1, 4)
        ket_c = np.zeros((4, 1), dtype=np.complex128)
        ket_c[k, 0] = 1.0
        K = ket_c @ bra  # shape (4, 4)
        kraus_ops.append(K)
    return KrausMap(kraus=tuple(kraus_ops), dim_in=4, dim_out=4)


def linear_optic_bell_bsm() -> KrausMap:
    """Linear-optic BSM distinguishing only {Φ+, Ψ-}; rest merged into 'fail'.

    Kraus operators (3 outcomes):
        K_0 = |0⟩_C ⟨Φ+|           (success, classical label 0)
        K_1 = |1⟩_C ⟨Ψ-|           (success, classical label 1)
        K_2 = |2⟩_C · P_fail       (fail, classical label 2)

    where P_fail = |Φ-⟩⟨Φ-| + |Ψ+⟩⟨Ψ+| is the projector onto the
    indistinguishable subspace.

    To stay trace-preserving with a single 'fail' output label, the fail
    Kraus is a single operator with rank-2 projector pre-composition.
    Concretely: we use TWO Kraus operators for fail (one per indistinguishable
    Bell state), both mapping to the same classical label |2⟩_C.  That's
    equivalent to a partial trace over Φ-/Ψ+ and preserves total probability.

    Trace-preserving check:
        Σ K_i† K_i = |Φ+⟩⟨Φ+| + |Ψ-⟩⟨Ψ-| + |Φ-⟩⟨Φ-| + |Ψ+⟩⟨Ψ+| = I_4 ✓

    Output dim: 3 (0=Φ+, 1=Ψ-, 2=fail).  Applied to a 2-qubit ρ, yields a
    3-dim classical diagonal density:
        p_0 = ⟨Φ+|ρ|Φ+⟩,  p_1 = ⟨Ψ-|ρ|Ψ-⟩,
        p_2 = ⟨Φ-|ρ|Φ-⟩ + ⟨Ψ+|ρ|Ψ+⟩.
    """
    ket0_c = np.array([[1], [0], [0]], dtype=np.complex128)  # shape (3, 1)
    ket1_c = np.array([[0], [1], [0]], dtype=np.complex128)
    ket2_c = np.array([[0], [0], [1]], dtype=np.complex128)
    K_phi_plus = ket0_c @ _bell_ket("Phi+").conj().T
    K_psi_minus = ket1_c @ _bell_ket("Psi-").conj().T
    K_fail_a = ket2_c @ _bell_ket("Phi-").conj().T
    K_fail_b = ket2_c @ _bell_ket("Psi+").conj().T
    return KrausMap(
        kraus=(K_phi_plus, K_psi_minus, K_fail_a, K_fail_b),
        dim_in=4, dim_out=3,
    )
