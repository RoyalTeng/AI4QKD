"""SARG04 (F3, Scarani-Acín-Ribordy-Gisin 2004) as MS-EB five-tuple.

**Scope**: `partial` — simplified Werner-form conditional state.

Reference:
- Scarani-Acín-Ribordy-Gisin 2004, PRL 92:057901
- Koashi 2005, quant-ph/0507154 (security bound)
- Fung-Tamaki-Lo 2006, PRA 73:012337 (refined security analysis)
- docs/families/bb84_family.md §3.3 (MS-EB formulation)

Difference from BB84 (F1):
    - Alice's announcement is a pair of non-orthogonal states (not basis choice)
    - Sifting rule: Bob's outcome must conclusively exclude one of the pair
    - Sift rate p_sift ≈ 1/4 (vs BB84's 1/2)
    - Sifted error rate q(e) = e / (1 + 2e)
    - Threshold (simplified): e ≤ 14.1% (vs Koashi 2005 exact ~9.68%)

**Simplifying assumptions in this implementation** (→ scope_tag='partial'):
    - Pair-selection probabilities uniform (Alice picks 1 of 2 valid pairs for each sent state)
    - Announcement semantics collapsed into p_sift scalar + Werner conditional state
    - Does not separately track Alice's 4 announcement choices as a classical register
    - Threshold differs from Koashi 2005 exact; for full fidelity, reformulate
      announcement as an explicit classical register in MS-EB A (Phase 1 deferred work)

Derivation of q(e) and p_sift(e) for symmetric depolarizing channel:
    Enumerate sent ∈ {|0⟩,|1⟩,|+⟩,|-⟩}, announced pair ∈ {valid 2 options},
    Bob basis ∈ {Z, X}, Bob outcome. Applying SARG04 sift rule:
        p_sift(e) = 1/4 + e/2       [NO error → sift from X, Error → sift from Z]
        q(e)      = (e/4) / (1/4 + e/2)  =  e / (1 + 2e)

At e=0: q=0, p_sift=1/4 (exact ideal SARG04 rate).
At e=0.11: q=0.11/1.22=0.090, 1-2h(0.09)=0.12 > 0.
At e=0.14: q=0.14/1.28=0.109, 1-2h(0.109)=0.02 (near threshold).
"""
from __future__ import annotations

import numpy as np

from qkdx.core.hilbert import Matrix
from qkdx.protocol.base import (
    AnnouncementRule, KeyMap, MSEBProtocol,
    PublicQuantumNetwork, SourceParty, OutOfScopeWarning,
)
from qkdx.protocols.bb84 import (
    bb84_alice_source, bb84_channel, _gamma_qber_Z, _gamma_qber_X,
)


def _sarg04_sifted_qber(e: float) -> float:
    """Sifted error rate for simplified SARG04 model: q(e) = e / (1 + 2e)."""
    return e / (1.0 + 2.0 * e)


def _sarg04_p_sift(e: float) -> float:
    """Effective sift probability: p_sift(e) = 1/4 + e/2."""
    return 0.25 + 0.5 * e


def _sarg04_conditional_state(qber: float) -> Matrix:
    """Sifted 4×4 Werner state parametrized by q(e) = e/(1+2e)."""
    q = _sarg04_sifted_qber(qber)
    return np.diag([(1 - q) / 2, q / 2, q / 2, (1 - q) / 2]).astype(np.complex128)


def _gamma_p_sift_sarg04(qber: float) -> Matrix:
    """p_sift observable scaled to p_sift(e) = 1/4 + e/2."""
    p_s = _sarg04_p_sift(qber)
    return np.eye(4, dtype=np.complex128) * (p_s / 4.0)


def sarg04_alice_source(qber: float) -> SourceParty:
    """Alice's 4-state EB source (same as BB84: 4-dim key × 2-dim signal).

    Note: in full SARG04 MS-EB formulation, the 4-dim register would encode
    Alice's CLASSICAL announcement choice (pair ∈ {4 pairs}), not just the
    sent state. Here we reuse BB84's source — the announcement semantics are
    absorbed into the sifted conditional state + p_sift scalar.
    """
    return bb84_alice_source(qber)


def build_sarg04_protocol(qber: float) -> MSEBProtocol:
    """Construct the SARG04 (F3) MS-EB protocol (simplified, partial scope).

    Args:
        qber: Symmetric depolarising channel QBER (Z = X), in [0, 1].

    Returns:
        MSEBProtocol with:
            - scope_tag = "partial" (see module docstring for assumptions)
            - conditional_alice_bob_dim() = 4
            - observation_keys = ("qber_Z", "qber_X", "p_sift")
            - Conditional state Werner(q) with q = e/(1+2e)
            - p_sift = 1/4 + e/2 (from enumeration of sift cases)

    Raises:
        ValueError: if qber not in [0, 1].

    References:
        Scarani-Acín-Ribordy-Gisin 2004, PRL 92:057901;
        Koashi 2005, quant-ph/0507154.
    """
    if not (0.0 <= qber <= 1.0):
        raise ValueError(f"QBER must be in [0, 1], got {qber}")

    src = sarg04_alice_source(qber)
    ch = bb84_channel(qber)
    net = PublicQuantumNetwork(channel=ch)
    # Simplified sift rule — in full SARG04 this would be a 3-tuple
    # (Alice announce pair, Bob basis, Bob outcome) with USD condition.
    ann = AnnouncementRule(sift_keep=lambda outcomes: outcomes[0] == outcomes[1])
    # Key bit: SARG04 assigns |0⟩/|+⟩→0, |1⟩/|-⟩→1 (bit by "sign").
    # Encoding: register index 0=|0⟩ (bit 0), 1=|1⟩ (bit 1), 2=|+⟩ (bit 0), 3=|-⟩ (bit 1)
    km = KeyMap(key_party="Alice", bitmap={0: 0, 1: 1, 2: 0, 3: 1})

    qber_val = qber
    observable_builders: dict[str, object] = {
        "qber_Z": lambda _p: _gamma_qber_Z(),
        "qber_X": lambda _p: _gamma_qber_X(),
        "p_sift": lambda _p: _gamma_p_sift_sarg04(qber_val),
        "_conditional_alice_bob": lambda _p: _sarg04_conditional_state(qber_val),
        "_cond_dim": lambda _p: 4,
    }

    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", OutOfScopeWarning)
        return MSEBProtocol(
            name="SARG04",
            sources=(src,),
            network=net,
            announcement=ann,
            key_map=km,
            observation_keys=("qber_Z", "qber_X", "p_sift"),
            scope_tag="partial",
            scope_reason=(
                "SARG04 announcement is simplified: Alice's 4-pair "
                "announcement is collapsed into the sifted conditional state "
                "(Werner form with q=e/(1+2e)) + p_sift=1/4+e/2 scalar. "
                "Full MS-EB would encode Alice's announcement pair as a "
                "classical register in A, making Bob's USD sift condition "
                "explicit. Simplified threshold ~14.1% vs Koashi 2005 ~9.68%. "
                "Upgrade to 'covered' requires explicit announcement register "
                "(Phase 1 Sub-Q2 deferred work)."
            ),
            _observable_builders=observable_builders,  # type: ignore[arg-type]
        )
