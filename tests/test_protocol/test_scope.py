"""Tests for R1.4: framework coverage and OutOfScopeWarning mechanism."""
from __future__ import annotations

import warnings

import numpy as np
import pytest

from qkdx.protocol.base import (
    AnnouncementRule, KeyMap, MSEBProtocol, OutOfScopeWarning,
    PublicQuantumNetwork, SourceParty,
)
from qkdx.core.operators import KrausMap
from qkdx.protocols.bb84 import build_bb84_protocol


def _dummy_protocol(scope_tag: str, scope_reason: str | None = None) -> MSEBProtocol:
    """Minimal valid protocol for scope testing."""
    src = SourceParty(
        name="Alice", key_register_dim=4, signal_register_dim=2,
        source_state=np.eye(8, dtype=np.complex128) / 8,
    )
    net = PublicQuantumNetwork(channel=KrausMap.identity(2))
    ann = AnnouncementRule(sift_keep=lambda outcomes: True)
    km = KeyMap(key_party="Alice", bitmap={0: 0, 1: 1, 2: 0, 3: 1})
    return MSEBProtocol(
        name="DummyProtocol",
        sources=(src,),
        network=net,
        announcement=ann,
        key_map=km,
        observation_keys=("qber_Z",),
        scope_tag=scope_tag,  # type: ignore[arg-type]
        scope_reason=scope_reason,
    )


# ---- BB84 is covered --------------------------------------------------------

def test_bb84_scope_tag_is_covered() -> None:
    protocol = build_bb84_protocol(qber=0.05)
    assert protocol.scope_tag == "covered"


def test_bb84_no_warning_on_construction() -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error", OutOfScopeWarning)
        build_bb84_protocol(qber=0.05)  # must not raise


# ---- out_of_scope warning ---------------------------------------------------

def test_out_of_scope_raises_warning() -> None:
    with pytest.warns(OutOfScopeWarning, match="out_of_scope"):
        _dummy_protocol("out_of_scope", scope_reason="requires cross-round adaptive E")


def test_out_of_scope_warning_contains_reason() -> None:
    reason = "requires cross-round adaptive E, violates single-E MS-EB assumption"
    with pytest.warns(OutOfScopeWarning, match=reason):
        _dummy_protocol("out_of_scope", scope_reason=reason)


# ---- out_of_scope requires reason -------------------------------------------

def test_out_of_scope_without_reason_raises() -> None:
    with pytest.raises(ValueError, match="scope_reason"):
        _dummy_protocol("out_of_scope", scope_reason=None)


def test_partial_without_reason_raises() -> None:
    with pytest.raises(ValueError, match="scope_reason"):
        _dummy_protocol("partial", scope_reason=None)


# ---- invalid scope_tag ------------------------------------------------------

def test_invalid_scope_tag_raises() -> None:
    with pytest.raises(ValueError, match="scope_tag"):
        _dummy_protocol("unknown_tag")  # type: ignore[arg-type]


# ---- toy cross-round protocol is rejected -----------------------------------

def test_cross_round_adaptive_protocol_out_of_scope() -> None:
    """A toy 'cross-round adaptive E' protocol must trigger OutOfScopeWarning."""
    with pytest.warns(OutOfScopeWarning):
        p = _dummy_protocol(
            "out_of_scope",
            scope_reason=(
                "channel E depends on measurement history across rounds "
                "(cross-round adaptive), violating single-E MS-EB assumption"
            ),
        )
    assert p.scope_tag == "out_of_scope"
    assert p.scope_reason is not None
    assert "cross-round" in p.scope_reason


# ---- partial tag ------------------------------------------------------------

def test_partial_protocol_no_error() -> None:
    """A 'partial' protocol (e.g. TF-QKD before M4B) should not warn."""
    with warnings.catch_warnings():
        warnings.simplefilter("error", OutOfScopeWarning)
        p = _dummy_protocol("partial", scope_reason="TF-QKD support pending M4B implementation")
    assert p.scope_tag == "partial"
