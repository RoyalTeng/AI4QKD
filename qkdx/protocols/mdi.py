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

from qkdx.core.bell_povm import linear_optic_bell_bsm
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


def mdi_bell_charlie_network() -> PublicQuantumNetwork:
    """Charlie's linear-optic Bell-state measurement as quantum channel.

    Uses `linear_optic_bell_bsm()`: 4→3 KrausMap with 3 outcomes:
        - 0 = Φ+ success
        - 1 = Ψ- success
        - 2 = fail (Φ- + Ψ+ merged, not distinguishable linear-optic-ly)

    Replaces `mdi_charlie_network`'s `KrausMap.identity(4)` in the Phase 1
    Sub-Q2 Stage B upgrade — Bell POVM now lives in the `channel` rather
    than being absorbed in `_conditional_alice_bob` override.

    Reference:
        - Lo-Curty-Qi 2012, PRL 108:130503 §II (virtual-EB equivalence)
        - qkdx/core/bell_povm.py (channel implementation)
    """
    return PublicQuantumNetwork(channel=linear_optic_bell_bsm())


def _mdi_bell_sift_keep(outcomes: tuple) -> bool:
    """Sift for Bell-POVM MDI: basis match AND Charlie success announcement.

    Args:
        outcomes: 3-tuple (θ_A, θ_B, c) where:
            - θ_A, θ_B: Alice / Bob basis choice indices
            - c: Charlie's announcement (0=Φ+, 1=Ψ-, 2=fail)

    Returns:
        True iff θ_A == θ_B AND c ∈ {0, 1}.
    """
    if len(outcomes) < 3:
        return False
    return outcomes[0] == outcomes[1] and outcomes[2] in (0, 1)


def _mdi_sift_keep(outcomes: tuple) -> bool:
    """Sift helper: Alice-Bob basis match (virtual-EB reduction).

    **Semantic note (Agent 2 retrospective review, Round 2, 2026-04-19):**
    In the full Lo-Curty-Qi 2012 MDI protocol, sifting requires both
    (i) Alice-Bob basis match AND (ii) Charlie announces a successful
    Bell-state measurement (not 'fail').  This helper only encodes (i);
    Charlie's success probability is **absorbed into the external
    `p_sift=0.25`** (= 1/2 basis match × 1/2 ideal BSM success) and into
    the post-announcement state returned by the `_conditional_alice_bob`
    override (virtual-EB picture, Lo-Curty-Qi 2012 §II).

    This is faithful for the WLC SDP computation in the ideal symmetric
    case because the SDP consumes only `p_sift` and the conditional 4×4
    state, not the raw outcome tuple.  A full multi-source MS-EB
    formulation (deferred to Phase 1 Sub-Q2) would encode Charlie's
    announcement as a third outcome component.
    """
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
                "Charlie's Bell POVM + announcement is absorbed into the "
                "`_conditional_alice_bob` override (virtual-EB picture, "
                "Lo-Curty-Qi 2012 §II) rather than modelled as the network "
                "channel.  Base-class `executed_state()` and `joint_state()` "
                "ARE implemented (Phase 1 Sub-Q2, 2026-04-19) and return the "
                "pre-POVM joint 64×64 state; but `conditional_alice_bob()` "
                "without the override would fall back to this state (wrong "
                "for MDI).  Upgrade to scope_tag='covered' requires modelling "
                "Charlie's Bell measurement as the `PublicQuantumNetwork.channel` "
                "with classical announcement output + extending `sift_keep` "
                "to consume Charlie's outcome (deferred — shared infrastructure "
                "with F3 SARG04 announcement register, Phase 1 Sub-Q2)."
            ),
            _observable_builders=observable_builders,  # type: ignore[arg-type]
        )
    return protocol


def build_mdi_bell_protocol(qber: float, p_sift: float = 0.25) -> MSEBProtocol:
    """MDI-QKD with Charlie's Bell POVM modelled as `PublicQuantumNetwork.channel`.

    Phase 1 Sub-Q2 Stage B implementation (2026-04-19):
        Replace `build_mdi_protocol`'s `KrausMap.identity(4)` with
        `linear_optic_bell_bsm()` so Charlie's Bell measurement + classical
        announcement sits *in* the channel rather than being absorbed into
        the `_conditional_alice_bob` override.

    Changes vs `build_mdi_protocol`:
        - `network.channel`:  `identity(4)` → `linear_optic_bell_bsm()`
          (dim_in=4, dim_out=3 classical announcement {Φ+, Ψ-, fail})
        - `announcement.sift_keep`:  2-tuple (θ_A, θ_B) →
          3-tuple (θ_A, θ_B, c);  success iff basis match AND c ∈ {0, 1}
        - `executed_state()`:  now 48×48 on (K_A ⊗ K_B ⊗ C)
          (vs legacy 64×64 on (K_A ⊗ K_B ⊗ A'⊗B'))

    Unchanged (for WLC SDP backward compat):
        - `_conditional_alice_bob` override returns 4×4 Werner
          (fast path; default path via sift_projector = follow-up stage)
        - `_cond_dim = 4`, observables Γ_Z, Γ_X on 4-dim bit_A ⊗ bit_B
        - `p_sift` observable (same semantics)

    Current scope status (`partial`):
        Channel now encodes Charlie Bell POVM — the v0.2 PHASE1_LOG §3.5.2
        / framework_coverage §3.1 F5 partial-cause is resolved.  But the
        `conditional_alice_bob()` default path (sift_projector on 48×48)
        must be implemented and verified to equal the override Werner
        before upgrading to `covered`.  Deferred to Stage B.2.

    References:
        - Lo-Curty-Qi 2012, PRL 108:130503
        - qkdx/core/bell_povm.py
        - docs/PHASE1_LOG.md §3.6 (Stage B decision log)
    """
    if not (0.0 <= qber <= 1.0):
        raise ValueError(f"QBER must be in [0, 1], got {qber}")
    if not (0.0 < p_sift <= 1.0):
        raise ValueError(f"p_sift must be in (0, 1], got {p_sift}")

    src_A = mdi_alice_source(qber)
    src_B = mdi_bob_source(qber)
    net = mdi_bell_charlie_network()  # Bell POVM, not identity
    ann = AnnouncementRule(sift_keep=_mdi_bell_sift_keep)  # 3-tuple
    km = KeyMap(key_party="Alice", bitmap={0: 0, 1: 1, 2: 0, 3: 1})

    qber_val = qber
    p_sift_val = p_sift
    observable_builders: dict[str, object] = {
        "qber_Z": lambda _p: _gamma_qber_Z(),
        "qber_X": lambda _p: _gamma_qber_X(),
        "p_sift": lambda _p: np.eye(4, dtype=np.complex128) * p_sift_val,
        # Override still primary (fast path); default-path sift_projector TBD.
        "_conditional_alice_bob": lambda _p: _bb84_conditional_state(qber_val),
        "_cond_dim": lambda _p: 4,
    }

    import warnings
    from qkdx.protocol.base import OutOfScopeWarning
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", OutOfScopeWarning)
        return MSEBProtocol(
            name="MDI-QKD-Bell",
            sources=(src_A, src_B),
            network=net,
            announcement=ann,
            key_map=km,
            observation_keys=("qber_Z", "qber_X", "p_sift"),
            scope_tag="partial",
            scope_reason=(
                "Phase 1 Sub-Q2 Stage B: Charlie's Bell POVM now lives in "
                "the `channel` (linear_optic_bell_bsm, dim_in=4, dim_out=3). "
                "Remaining partial cause: the `conditional_alice_bob()` "
                "default path (via `_sift_projector` on 48×48 executed_state) "
                "has not been implemented; the `_conditional_alice_bob` "
                "override is still the fast path for WLC SDP.  Upgrade to "
                "`covered` requires implementing + numerically verifying "
                "that the default path produces the same 4×4 Werner state "
                "as the override (Stage B.2, follow-up)."
            ),
            _observable_builders=observable_builders,  # type: ignore[arg-type]
        )
