"""Efficient BB84 (F4, Lo-Chau-Ardehali 2005) as MS-EB five-tuple.

Reference:
- Lo-Chau-Ardehali 2005, J. Cryptology 18:133 (biased-basis BB84)
- docs/families/bb84_family.md §1.4, §3.4

Difference from BB84 (F1):
    - Alice picks Z basis with probability p_Z > 1/2 (X with 1-p_Z)
    - Assuming Bob mirror-biases, p_sift = p_Z^2 + (1-p_Z)^2 > 0.5
    - Source state amplitudes rescaled accordingly
    - Observables Γ_Z, Γ_X unchanged (Z-sifted conditional state same Werner form)
    - Key rate R = p_sift · (1 - 2h(e))  (vs BB84's 0.5 · (1-2h(e)))
"""
from __future__ import annotations

import numpy as np

from qkdx.core.hilbert import HADAMARD, Matrix
from qkdx.protocol.base import (
    AnnouncementRule, KeyMap, MSEBProtocol,
    PublicQuantumNetwork, SourceParty,
)
from qkdx.protocols.bb84 import (
    bb84_channel, _bb84_conditional_state, _gamma_qber_Z, _gamma_qber_X,
)


def efficient_bb84_alice_source(qber: float, p_Z: float) -> SourceParty:
    """Biased EB state source.

    |ψ⟩_{AA'} = √(p_Z/2)·(|Z,0⟩|0⟩+|Z,1⟩|1⟩) + √((1-p_Z)/2)·(|X,0⟩|+⟩+|X,1⟩|-⟩)

    A register basis (4-dim): |0⟩=|Z,0⟩, |1⟩=|Z,1⟩, |2⟩=|X,0⟩, |3⟩=|X,1⟩.
    A' register: single qubit (2-dim).

    Amplitude weights:
        - |Z,x⟩|x⟩:   √(p_Z/2)
        - |X,x⟩|+/-⟩ (2 components each): √((1-p_Z)/4)

    Marginal basis probabilities: P(Z)=p_Z, P(X)=1-p_Z.
    """
    psi = np.zeros((8, 1), dtype=np.complex128)
    z_amp = np.sqrt(p_Z / 2.0)
    x_amp = np.sqrt((1.0 - p_Z) / 4.0)
    # |Z,0⟩ ⊗ |0⟩  → index 0
    psi[0, 0] = z_amp
    # |Z,1⟩ ⊗ |1⟩  → index 3
    psi[3, 0] = z_amp
    # |X,0⟩ ⊗ |+⟩  → indices 4, 5 (equal)
    psi[4, 0] = x_amp
    psi[5, 0] = x_amp
    # |X,1⟩ ⊗ |-⟩  → indices 6, 7 (opposite)
    psi[6, 0] = x_amp
    psi[7, 0] = -x_amp

    rho_aa_prime = psi @ psi.conj().T

    return SourceParty(
        name="Alice",
        key_register_dim=4,
        signal_register_dim=2,
        source_state=rho_aa_prime,
    )


def _gamma_p_sift_efficient(p_Z: float) -> Matrix:
    """p_sift observable normalised to p_Z^2 + (1-p_Z)^2.

    Γ_psift = p_sift · I/4  (reference — wlc_key_rate treats p_sift as scalar constraint).
    """
    p_sift = p_Z ** 2 + (1 - p_Z) ** 2
    return np.eye(4, dtype=np.complex128) * (p_sift / 4.0)


def build_efficient_bb84_protocol(qber: float, p_Z: float = 0.9) -> MSEBProtocol:
    """Construct the Efficient BB84 (F4) MS-EB protocol.

    Args:
        qber: Symmetric depolarising QBER (Z = X basis), in [0, 1].
        p_Z: Z-basis selection probability, must be in (0.5, 1.0) strictly.
             Default 0.9 (typical efficient BB84 bias).

    Returns:
        MSEBProtocol with:
            - scope_tag = "covered"
            - sources = (Alice,) with key_register_dim=4, signal_register_dim=2
            - conditional_alice_bob_dim() = 4
            - observation_keys = ("qber_Z", "qber_X", "p_sift")
            - p_sift = p_Z^2 + (1-p_Z)^2  (assuming Bob mirror-biases)

    Raises:
        ValueError: qber not in [0, 1], or p_Z not in (0.5, 1.0).

    References:
        Lo-Chau-Ardehali 2005, J. Cryptology 18:133.
    """
    if not (0.0 <= qber <= 1.0):
        raise ValueError(f"QBER must be in [0, 1], got {qber}")
    if not (0.5 < p_Z < 1.0):
        raise ValueError(f"p_Z must be in (0.5, 1.0) strictly, got {p_Z}")

    src = efficient_bb84_alice_source(qber, p_Z)
    ch = bb84_channel(qber)
    net = PublicQuantumNetwork(channel=ch)
    ann = AnnouncementRule(sift_keep=lambda outcomes: outcomes[0] == outcomes[1])
    km = KeyMap(key_party="Alice", bitmap={0: 0, 1: 1, 2: 0, 3: 1})

    qber_val = qber
    p_Z_val = p_Z

    observable_builders: dict[str, object] = {
        "qber_Z": lambda _p: _gamma_qber_Z(),
        "qber_X": lambda _p: _gamma_qber_X(),
        "p_sift": lambda _p: _gamma_p_sift_efficient(p_Z_val),
        # Conditional state is Z-sifted Werner form — bias cancels in conditioning.
        "_conditional_alice_bob": lambda _p: _bb84_conditional_state(qber_val),
        "_cond_dim": lambda _p: 4,
    }

    return MSEBProtocol(
        name="EfficientBB84",
        sources=(src,),
        network=net,
        announcement=ann,
        key_map=km,
        observation_keys=("qber_Z", "qber_X", "p_sift"),
        _observable_builders=observable_builders,  # type: ignore[arg-type]
    )
