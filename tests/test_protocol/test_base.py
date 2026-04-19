"""Tests for MSEBProtocol dataclass and invariants (§4.4)."""
from __future__ import annotations

import numpy as np
import pytest

from qkdx.protocols.bb84 import build_bb84_protocol


# ---- state quality -----------------------------------------------------------

def test_mseb_joint_state_norm_preserved() -> None:
    protocol = build_bb84_protocol(qber=0.05)
    psi = protocol.joint_state()
    assert np.isclose(np.linalg.norm(psi), 1.0, atol=1e-10)


def test_mseb_executed_state_is_density() -> None:
    from qkdx.core.hilbert import is_density
    protocol = build_bb84_protocol(qber=0.05)
    rho = protocol.executed_state()
    assert is_density(rho, atol=1e-7)


def test_mseb_conditional_alice_bob_is_density() -> None:
    from qkdx.core.hilbert import is_density
    protocol = build_bb84_protocol(qber=0.05)
    rho = protocol.conditional_alice_bob()
    assert is_density(rho, atol=1e-7)


def test_mseb_conditional_alice_bob_dim_matches_matrix() -> None:
    protocol = build_bb84_protocol(qber=0.05)
    d = protocol.conditional_alice_bob_dim()
    rho = protocol.conditional_alice_bob()
    assert rho.shape == (d, d)


# ---- immutability ------------------------------------------------------------

def test_mseb_sources_tuple_immutable() -> None:
    protocol = build_bb84_protocol(qber=0.05)
    with pytest.raises((AttributeError, TypeError)):
        protocol.sources[0].name = "Eve"  # type: ignore[misc]


# ---- constructor validation --------------------------------------------------

def test_mseb_empty_observation_keys_raises() -> None:
    from qkdx.protocol.base import (
        AnnouncementRule, KeyMap, MSEBProtocol, PublicQuantumNetwork, SourceParty
    )
    from qkdx.core.operators import KrausMap
    src = SourceParty(name="Alice", key_register_dim=4, signal_register_dim=2,
                      source_state=np.eye(8, dtype=np.complex128) / 8)
    net = PublicQuantumNetwork(channel=KrausMap.identity(2))
    ann = AnnouncementRule(sift_keep=lambda outcomes: True)
    km = KeyMap(key_party="Alice", bitmap={0: 0, 1: 1, 2: 0, 3: 1})
    with pytest.raises(ValueError, match="observation_keys"):
        MSEBProtocol(
            name="Dummy", sources=(src,), network=net,
            announcement=ann, key_map=km, observation_keys=()
        )


# ---- observable lookup -------------------------------------------------------

def test_mseb_unknown_observation_key_raises() -> None:
    protocol = build_bb84_protocol(qber=0.05)
    with pytest.raises(ValueError):
        protocol.observable("nonexistent_key_xyz")


def test_mseb_observable_qber_Z_shape() -> None:
    protocol = build_bb84_protocol(qber=0.05)
    Gamma = protocol.observable("qber_Z")
    d = protocol.conditional_alice_bob_dim()
    assert Gamma.shape == (d, d)


def test_mseb_observable_qber_Z_is_hermitian() -> None:
    from qkdx.core.hilbert import is_hermitian
    protocol = build_bb84_protocol(qber=0.05)
    Gamma = protocol.observable("qber_Z")
    assert is_hermitian(Gamma)
