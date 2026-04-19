"""Six-state QKD protocol as MS-EB five-tuple.

Reference:
- Bruss 1998, PRL 81:3018 (original six-state)
- Lo 2001, QIC 1:81-94 (unconditional security)
- Scarani et al. 2009, RMP 81:1301, §III.D.1
- docs/literature/six-state.md (Level 2 memo)

Difference from BB84:
  * Adds Y-basis to MUB set ⇒ 3 MUBs, 6 states total
  * key_register_dim = 6 (3 bases × 2 values)
  * Sifting p = 1/3 (random 3-way basis match)
  * observation_keys adds "qber_Y"
  * d_rho still = 4 (A_key ⊗ B), so WLC SDP uses same 4-dim machinery
"""
from __future__ import annotations

import numpy as np

from qkdx.core.hilbert import (
    HADAMARD, IDENTITY_2, KET_0, KET_1,
    Matrix, tensor,
)
from qkdx.core.operators import KrausMap
from qkdx.protocol.base import (
    AnnouncementRule, KeyMap, MSEBProtocol,
    PublicQuantumNetwork, SourceParty,
)
from qkdx.protocols.bb84 import (
    bb84_channel, _bb84_conditional_state,
    _gamma_qber_Z, _gamma_qber_X,
)


# ---------------------------------------------------------------------------
# Basis rotation utilities
# ---------------------------------------------------------------------------

# Rotation from computational (Z) basis to Y basis:
#   U_Y |0⟩ = |+y⟩ = (|0⟩ + i|1⟩)/√2
#   U_Y |1⟩ = |-y⟩ = (|0⟩ - i|1⟩)/√2
U_Y: Matrix = np.array([[1.0, 1.0],
                        [1.0j, -1.0j]], dtype=np.complex128) / np.sqrt(2.0)


# ---------------------------------------------------------------------------
# Sub-builders
# ---------------------------------------------------------------------------

def sixstate_alice_source(qber: float) -> SourceParty:
    """Alice's EB state source for six-state QKD.

    |ψ⟩_{AA'} = (1/√6) Σ_{θ∈{Z,X,Y}, x∈{0,1}} |θ,x⟩_A ⊗ U_θ|x⟩_{A'}

    A register basis (6-dim):
        |0⟩ = |Z,0⟩, |1⟩ = |Z,1⟩,
        |2⟩ = |X,0⟩, |3⟩ = |X,1⟩,
        |4⟩ = |Y,0⟩, |5⟩ = |Y,1⟩.
    A' register: single qubit (2-dim). Total dim = 6 × 2 = 12.
    """
    # |ψ⟩ as 12-dim column vector, indexed (a, a') → 2a + a'
    psi = np.zeros((12, 1), dtype=np.complex128)
    amp = 1.0 / np.sqrt(6.0)

    # Z basis: U_Z = I
    psi[2 * 0 + 0, 0] = amp                  # |Z,0⟩ ⊗ |0⟩
    psi[2 * 1 + 1, 0] = amp                  # |Z,1⟩ ⊗ |1⟩

    # X basis: U_X = H,  H|0⟩ = |+⟩ = (|0⟩+|1⟩)/√2,  H|1⟩ = |-⟩ = (|0⟩-|1⟩)/√2
    psi[2 * 2 + 0, 0] = amp / np.sqrt(2.0)   # |X,0⟩ ⊗ |0⟩ part of |+⟩
    psi[2 * 2 + 1, 0] = amp / np.sqrt(2.0)   # |X,0⟩ ⊗ |1⟩ part of |+⟩
    psi[2 * 3 + 0, 0] = amp / np.sqrt(2.0)   # |X,1⟩ ⊗ |0⟩ part of |-⟩
    psi[2 * 3 + 1, 0] = -amp / np.sqrt(2.0)  # |X,1⟩ ⊗ |1⟩ part of |-⟩

    # Y basis: U_Y|0⟩ = (|0⟩+i|1⟩)/√2,  U_Y|1⟩ = (|0⟩-i|1⟩)/√2
    psi[2 * 4 + 0, 0] = amp / np.sqrt(2.0)
    psi[2 * 4 + 1, 0] = 1j * amp / np.sqrt(2.0)
    psi[2 * 5 + 0, 0] = amp / np.sqrt(2.0)
    psi[2 * 5 + 1, 0] = -1j * amp / np.sqrt(2.0)

    rho_aa_prime = psi @ psi.conj().T  # (12, 12)

    return SourceParty(
        name="Alice",
        key_register_dim=6,
        signal_register_dim=2,
        source_state=rho_aa_prime,
    )


def _gamma_qber_Y() -> Matrix:
    """Observable Γ_Y on 4-dim A_key ⊗ B space.

    Γ_Y = (U_Y ⊗ U_Y*) Γ_Z (U_Y ⊗ U_Y*)†  enforces Tr(Γ_Y ρ) = QBER_Y.

    The Bob-side complex conjugate U_Y* is required because |Φ+⟩ is *anti-*
    correlated in the Y basis:
        |Φ+⟩ = (|+y,-y⟩ + |-y,+y⟩)/√2  (in Y⊗Y basis)
    so raw Alice-Y vs Bob-Y measurements on the EB source differ; the standard
    convention absorbs this by conjugating Bob's basis transform.  Equivalently,
    after this definition, Tr(Γ_Y · ρ_Werner) = e for the symmetric
    depolarising Werner state (verified in test_gamma_Y_agrees_with_depolarizing_channel).

    Z and X bases use real rotations (U_Z = I, U_X = H) so this issue doesn't
    arise there.
    """
    U_Y_bob = U_Y.conj()  # Bob's basis transform is the complex conjugate of Alice's
    U_map = np.kron(U_Y, U_Y_bob)
    gamma_Z = _gamma_qber_Z()
    return (U_map @ gamma_Z @ U_map.conj().T).astype(np.complex128)


def _gamma_p_sift_sixstate() -> Matrix:
    """Observable for p_sift = 1/3.  Same semantic as BB84 p_sift (reference)."""
    return np.eye(4, dtype=np.complex128) / 3.0


# ---------------------------------------------------------------------------
# Protocol factory
# ---------------------------------------------------------------------------

def build_sixstate_protocol(qber: float) -> MSEBProtocol:
    """Construct the six-state MS-EB protocol object for a given symmetric QBER.

    Channel is symmetric depolarising ⇒ QBER_Z = QBER_X = QBER_Y = qber.

    Returns an MSEBProtocol with:
        - key_register_dim = 6, signal_register_dim = 2
        - conditional_alice_bob_dim() = 4  (same 4-dim SDP as BB84)
        - observation_keys = ("qber_Z", "qber_X", "qber_Y", "p_sift")
        - scope_tag = "covered"

    For the symmetric depolarising channel, the Z-basis sifted conditional state
    on A_key ⊗ B is identical to BB84's:
        ρ_{AB}^{sift} = diag((1-e)/2, e/2, e/2, (1-e)/2)

    (The difference from BB84 is the additional Γ_Y constraint in the SDP
    feasible set, not the sifted state.)
    """
    if not (0.0 <= qber <= 2.0 / 3.0):
        raise ValueError(f"QBER must be in [0, 2/3] for six-state, got {qber}")

    src = sixstate_alice_source(qber)
    ch = bb84_channel(qber)  # identical symmetric depolarising channel
    net = PublicQuantumNetwork(channel=ch)
    # Sifting: both sides pick same basis (3-way match)
    ann = AnnouncementRule(sift_keep=lambda outcomes: outcomes[0] == outcomes[1])
    # Key bit: Alice's low-bit index within basis (even/odd of register index)
    km = KeyMap(
        key_party="Alice",
        bitmap={0: 0, 1: 1, 2: 0, 3: 1, 4: 0, 5: 1},
    )

    qber_val = qber

    observable_builders: dict[str, object] = {
        "qber_Z": lambda _p: _gamma_qber_Z(),
        "qber_X": lambda _p: _gamma_qber_X(),
        "qber_Y": lambda _p: _gamma_qber_Y(),
        "p_sift": lambda _p: _gamma_p_sift_sixstate(),
        "_conditional_alice_bob": lambda _p: _bb84_conditional_state(qber_val),
        "_cond_dim": lambda _p: 4,
    }

    protocol = MSEBProtocol(
        name="SixState",
        sources=(src,),
        network=net,
        announcement=ann,
        key_map=km,
        observation_keys=("qber_Z", "qber_X", "qber_Y", "p_sift"),
        _observable_builders=observable_builders,  # type: ignore[arg-type]
    )
    return protocol
