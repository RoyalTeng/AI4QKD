"""BB84 protocol as MS-EB five-tuple.

Reference: Winick-Lütkenhaus-Coles 2018 §5, Coles-Metodiev-Lütkenhaus 2016 §3.
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


# ---------------------------------------------------------------------------
# Sub-builders (exported for testing)
# ---------------------------------------------------------------------------

def bb84_alice_source(qber: float) -> SourceParty:
    """Alice's EB state source.

    |ψ⟩_{AA'} = (1/2) Σ_{θ∈{Z,X}, x∈{0,1}} |θ,x⟩_A ⊗ U_θ|x⟩_{A'}

    A register basis (4-dim): |0⟩=|Z,0⟩, |1⟩=|Z,1⟩, |2⟩=|X,0⟩, |3⟩=|X,1⟩.
    A' register is a single qubit (2-dim).
    """
    # Build |ψ⟩ as 8-dim column vector
    psi = np.zeros((8, 1), dtype=np.complex128)
    # |Z,0⟩_A ⊗ I|0⟩ = |0⟩_A ⊗ |0⟩  → index 2*0+0 = 0
    psi[0, 0] = 0.5
    # |Z,1⟩_A ⊗ I|1⟩ = |1⟩_A ⊗ |1⟩  → index 2*1+1 = 3
    psi[3, 0] = 0.5
    # |X,0⟩_A ⊗ H|0⟩ = |2⟩_A ⊗ |+⟩  → index 2*2+0=4 and 2*2+1=5
    psi[4, 0] = 0.5 / np.sqrt(2)
    psi[5, 0] = 0.5 / np.sqrt(2)
    # |X,1⟩_A ⊗ H|1⟩ = |3⟩_A ⊗ |-⟩  → index 2*3+0=6 and 2*3+1=7
    psi[6, 0] = 0.5 / np.sqrt(2)
    psi[7, 0] = -0.5 / np.sqrt(2)

    rho_aa_prime = psi @ psi.conj().T  # shape (8,8)

    return SourceParty(
        name="Alice",
        key_register_dim=4,
        signal_register_dim=2,
        source_state=rho_aa_prime,
    )


def bb84_channel(qber: float) -> KrausMap:
    """Symmetric depolarising channel with QBER = qber.

    Kraus operators:
        K_0 = sqrt(1 - 3p/4) · I        (no error)
        K_1 = sqrt(p/4) · σ_x           (bit flip)
        K_2 = sqrt(p/4) · σ_y           (bit+phase flip)
        K_3 = sqrt(p/4) · σ_z           (phase flip)

    where p = 4*qber/3 (depolarising parameter, so QBER = 3p/4 * 1/3 for σ_x portion
    — in the symmetric model QBER = p/2 + p/2 counting bit-flip and combined errors).

    For consistency with WLC 2018 §5: QBER = e relates to depolarising via
        ρ_B = (1-e)|b⟩⟨b| + e|b̄⟩⟨b̄|
    This is reproduced by the asymmetric X-dominant channel: K_0=sqrt(1-e)I, K_1=sqrt(e)σ_x.
    We use the full symmetric model so qber_Z = qber_X = qber.
    """
    p = 4.0 * qber / 3.0  # depolarising parameter
    k0 = np.sqrt(max(1.0 - 3.0 * p / 4.0, 0.0)) * IDENTITY_2
    k1 = np.sqrt(p / 4.0) * np.array([[0, 1], [1, 0]], dtype=np.complex128)
    k2 = np.sqrt(p / 4.0) * np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    k3 = np.sqrt(p / 4.0) * np.array([[1, 0], [0, -1]], dtype=np.complex128)
    return KrausMap(kraus=(k0, k1, k2, k3), dim_in=2, dim_out=2)


def _bb84_conditional_state(qber: float) -> Matrix:
    """Sifted state ρ_{AB} on C^2 ⊗ C^2 (Alice key bit ⊗ Bob's Z outcome).

    For symmetric depolarising with QBER e, the Z-basis sifted state is:
        ρ = (1-e)/2 |00⟩⟨00| + e/2 |01⟩⟨01| + e/2 |10⟩⟨10| + (1-e)/2 |11⟩⟨11|

    where |xy⟩ denotes Alice bit x ⊗ Bob outcome y (in {|00⟩,|01⟩,|10⟩,|11⟩}).
    """
    e = qber
    return np.diag([(1 - e) / 2, e / 2, e / 2, (1 - e) / 2]).astype(np.complex128)


def _gamma_qber_Z() -> Matrix:
    """Observable Γ_Z = |01⟩⟨01| + |10⟩⟨10| on 4-dim A_key ⊗ B space.

    Enforces Tr(Γ_Z ρ) = QBER_Z.  (CML 2016 Eq. 25)
    """
    return np.diag([0.0, 1.0, 1.0, 0.0]).astype(np.complex128)


def _gamma_qber_X() -> Matrix:
    """Observable Γ_X = (H⊗H) Γ_Z (H⊗H) on 4-dim A_key ⊗ B space.

    Enforces Tr(Γ_X ρ) = QBER_X.  (CML 2016 Eq. 26)
    """
    HH = np.kron(HADAMARD, HADAMARD)
    gamma_Z = _gamma_qber_Z()
    return (HH @ gamma_Z @ HH.conj().T).astype(np.complex128)


def _gamma_p_sift() -> Matrix:
    """Observable for p_sift = 0.5 (Z-basis sifting probability).

    For symmetric BB84: p_sift = P(sift_keep) = 0.5.
    We encode the trace-level constraint: Tr(I/2 · ρ) = 0.5, i.e., Γ_psift = I/2.
    But since p_sift is typically fed as a scalar (not SDP constraint), we provide
    this as a reference.  wlc_key_rate skips "p_sift" in the matrix constraints.
    """
    return np.eye(4, dtype=np.complex128) / 2.0


# ---------------------------------------------------------------------------
# Protocol factory
# ---------------------------------------------------------------------------

def build_bb84_protocol(qber: float) -> MSEBProtocol:
    """Construct the BB84 MS-EB protocol object for a given QBER.

    Returns an MSEBProtocol with:
        - d = conditional_alice_bob_dim() = 4
        - observation_keys = ("qber_Z", "qber_X", "p_sift")
        - observable("qber_Z") → 4×4 Hermitian Γ_Z
        - observable("qber_X") → 4×4 Hermitian Γ_X

    The SDP variable ρ lives in the d=4 space (Alice key bit ⊗ Bob outcome).
    G map = identity on this 4-dim space; dim_key=2, dim_side=2.
    """
    if not (0.0 <= qber <= 1.0):
        raise ValueError(f"QBER must be in [0, 1], got {qber}")

    src = bb84_alice_source(qber)
    ch = bb84_channel(qber)
    net = PublicQuantumNetwork(channel=ch)
    ann = AnnouncementRule(sift_keep=lambda outcomes: outcomes[0] == outcomes[1])
    km = KeyMap(key_party="Alice", bitmap={0: 0, 1: 1, 2: 0, 3: 1})

    qber_val = qber  # capture for closures

    observable_builders: dict[str, object] = {
        "qber_Z": lambda _p: _gamma_qber_Z(),
        "qber_X": lambda _p: _gamma_qber_X(),
        "p_sift": lambda _p: _gamma_p_sift(),
        # Override: directly return analytic 4x4 sifted state (faster + exact)
        "_conditional_alice_bob": lambda _p: _bb84_conditional_state(qber_val),
        # Internal dim hint (returns scalar int, cast by caller)
        "_cond_dim": lambda _p: 4,
    }

    protocol = MSEBProtocol(
        name="BB84",
        sources=(src,),
        network=net,
        announcement=ann,
        key_map=km,
        observation_keys=("qber_Z", "qber_X", "p_sift"),
        _observable_builders=observable_builders,  # type: ignore[arg-type]
    )
    return protocol


def _make_sift_projector(protocol: MSEBProtocol) -> Matrix:
    """8-dim projector onto Z-basis rounds in the full A ⊗ B space.

    Returns P = P_{θ=Z} ⊗ I_B, where P_{θ=Z} projects onto the first 2
    basis states of the 4-dim A register (corresponding to θ=Z).
    """
    P_theta_Z = np.zeros((4, 4), dtype=np.complex128)
    P_theta_Z[0, 0] = 1.0
    P_theta_Z[1, 1] = 1.0
    return np.kron(P_theta_Z, np.eye(2, dtype=np.complex128))
