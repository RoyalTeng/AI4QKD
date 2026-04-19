"""MDI-QKD protocol as MS-EB five-tuple (ideal symmetric lossless case).

Reference:
- Lo-Curty-Qi 2012, PRL 108:130503 (arXiv:1109.1473)
- Ma-Razavi 2012, PRA 86:062319 (arXiv:1204.4856)
- docs/literature/MDI-QKD.md (Level 2-3 memo)
- docs/msen/mdi-formulation.md

Scope of this module (M2 baseline):
  * Ideal symmetric setting: η_A = η_B = 1 (no loss), single-photon source,
    symmetric depolarising effective channel on each leg so Alice-Bob
    effective QBER_Z = QBER_X = e.
  * Multi-source MS-EB:  two sources (Alice + Bob), each holding BB84-style
    EB pair; Charlie's untrusted Bell measurement is modelled via the
    conditional_alice_bob override (returns the post-announcement Werner-like
    4×4 state, identical in form to BB84's sifted state).
  * p_sift = 1/4  (basis match 1/2 × Charlie success rate 1/2 in ideal case).

Not in scope (deferred to M3):
  * decoy-state analysis (Ma-Razavi 2012 Fig.3 distance sweep)
  * coherent-state sources with Fock truncation
  * asymmetric channel losses η_A ≠ η_B
"""
from __future__ import annotations

import numpy as np

from qkdx.core.hilbert import Matrix
from qkdx.core.operators import KrausMap
from qkdx.protocol.base import (
    AnnouncementRule, KeyMap, MSEBProtocol,
    PublicQuantumNetwork, SourceParty,
)
from qkdx.protocols.bb84 import (
    bb84_alice_source, _bb84_conditional_state,
    _gamma_qber_Z, _gamma_qber_X,
)


# ---------------------------------------------------------------------------
# Sub-builders
# ---------------------------------------------------------------------------

def mdi_alice_source(qber: float) -> SourceParty:
    """Alice's source for MDI-QKD: same BB84 EB source (4-dim key, 2-dim signal)."""
    src = bb84_alice_source(qber)
    # Rename to disambiguate in multi-source context
    return SourceParty(
        name="Alice",
        key_register_dim=src.key_register_dim,
        signal_register_dim=src.signal_register_dim,
        source_state=src.source_state,
    )


def mdi_bob_source(qber: float) -> SourceParty:
    """Bob's source for MDI-QKD: mirror image of Alice's."""
    src = bb84_alice_source(qber)
    return SourceParty(
        name="Bob",
        key_register_dim=src.key_register_dim,
        signal_register_dim=src.signal_register_dim,
        source_state=src.source_state,
    )


def mdi_charlie_network(qber: float) -> PublicQuantumNetwork:
    """Charlie's combined (A' ⊗ B') → Bell outcome channel.

    In the ideal MDI baseline, we model the channel as identity on the
    combined 4-dim A'⊗B' Hilbert space; the *physical* Bell-measurement +
    announcement is absorbed into the `_conditional_alice_bob` override
    (equivalent in the virtual-EB picture per Lo-Curty-Qi 2012 §II).

    This approximation is faithful for WLC SDP key-rate computation because
    the SDP only uses `conditional_alice_bob_dim()` and the observable
    matrices Γ_Z, Γ_X — not the channel Kraus operators directly.
    """
    return PublicQuantumNetwork(channel=KrausMap.identity(4))


def _mdi_sift_keep(outcomes: tuple) -> bool:
    """Sift: Alice's basis = Bob's basis (ignore Charlie announcement detail)."""
    if len(outcomes) < 2:
        return False
    return outcomes[0] == outcomes[1]


# ---------------------------------------------------------------------------
# Protocol factory
# ---------------------------------------------------------------------------

def build_mdi_protocol(qber: float, p_sift: float = 0.25) -> MSEBProtocol:
    """Construct the ideal symmetric MDI-QKD MS-EB protocol.

    Args:
        qber: effective Alice-Bob QBER in Z and X bases (symmetric).
        p_sift: sifting probability. Default 0.25 = 1/2 basis match ×
                1/2 Charlie Bell success (ideal linear-optic BSM).

    Returns:
        MSEBProtocol with:
            - Two sources (Alice + Bob), each 4-dim key × 2-dim signal
            - Network: identity on 4-dim (channel absorbed into override)
            - conditional_alice_bob_dim() = 4  (A_key ⊗ B_effective-bit)
            - observation_keys = ("qber_Z", "qber_X", "p_sift")
            - **scope_tag = "partial"**: WLC SDP path works via the
              `_conditional_alice_bob` override, but the base-class
              `joint_state()` and `executed_state()` methods are not
              implemented for multi-source protocols.  Downgraded from
              "covered" per retrospective-review Agent 1 MAJOR #2 finding
              (2026-04-19).  Upgrade to "covered" requires implementing
              true multi-source state construction (Phase 1 Sub-Q2 MDI
              family sheet or earlier dedicated work).
    """
    if not (0.0 <= qber <= 1.0):
        raise ValueError(f"QBER must be in [0, 1], got {qber}")
    if not (0.0 < p_sift <= 1.0):
        raise ValueError(f"p_sift must be in (0, 1], got {p_sift}")

    src_A = mdi_alice_source(qber)
    src_B = mdi_bob_source(qber)
    net = mdi_charlie_network(qber)
    ann = AnnouncementRule(sift_keep=_mdi_sift_keep)
    # Key held by Alice; bitmap maps Alice's 4-dim key register → key bit
    km = KeyMap(key_party="Alice", bitmap={0: 0, 1: 1, 2: 0, 3: 1})

    qber_val = qber

    observable_builders: dict[str, object] = {
        "qber_Z": lambda _p: _gamma_qber_Z(),
        "qber_X": lambda _p: _gamma_qber_X(),
        "p_sift": lambda _p: np.eye(4, dtype=np.complex128) * p_sift,
        # Post-announcement conditional state (virtual EB picture):
        # identical in form to BB84's Z-basis sifted state.
        "_conditional_alice_bob": lambda _p: _bb84_conditional_state(qber_val),
        "_cond_dim": lambda _p: 4,
    }

    import warnings
    from qkdx.protocol.base import OutOfScopeWarning
    with warnings.catch_warnings():
        # Partial construction intentionally avoids out_of_scope warnings
        # (MDI WLC path works via override; base-class state queries raise).
        warnings.simplefilter("ignore", OutOfScopeWarning)
        protocol = MSEBProtocol(
            name="MDI-QKD",
            sources=(src_A, src_B),
            network=net,
            announcement=ann,
            key_map=km,
            observation_keys=("qber_Z", "qber_X", "p_sift"),
            scope_tag="partial",
            scope_reason=(
                "Multi-source MS-EB: base-class joint_state() and "
                "executed_state() are not implemented for len(sources) > 1. "
                "WLC SDP works via the _conditional_alice_bob override. "
                "Upgrade to scope_tag='covered' after implementing proper "
                "tensor + joint-channel semantics (deferred — Phase 1 "
                "Sub-Q2 MDI family sheet)."
            ),
            _observable_builders=observable_builders,  # type: ignore[arg-type]
        )
    return protocol
