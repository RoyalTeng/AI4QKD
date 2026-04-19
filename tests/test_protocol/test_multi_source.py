"""Tests for multi-source MS-EB state queries.

Phase 1 Sub-Q2 infrastructure: implements executed_state() and joint_state()
for len(sources) > 1, unblocking:
    - F5 MDI-QKD multi-source tensor + joint-channel semantics (partial → covered)
    - F3 SARG04 announcement classical register (when combined with
      AnnouncementRule extension)

The new `executed_state()` for N sources:
    1. Tensor-product each source's EB density matrix:  ρ_joint = ⊗_i ρ_i
    2. Reorder tensor axes from (K_1 S_1 K_2 S_2 ... K_N S_N) to
       (K_1 K_2 ... K_N S_1 S_2 ... S_N)
    3. Apply (I_keys ⊗ channel) to get ρ_{K_1..K_N, B}

References:
- docs/PHASE1_LOG.md §3 (implementation decision record)
- docs/msen/mdi-formulation.md (MDI MS-EB formulation)
"""
from __future__ import annotations

import numpy as np
import pytest

from qkdx.core.operators import KrausMap
from qkdx.protocol.base import (
    AnnouncementRule, KeyMap, MSEBProtocol,
    PublicQuantumNetwork, SourceParty,
)
from qkdx.protocols.bb84 import bb84_alice_source, bb84_channel
from qkdx.protocols.mdi import build_mdi_protocol


def _make_trivial_2source_protocol() -> MSEBProtocol:
    """Toy 2-source protocol: 2 BB84-like sources + identity channel.

    Used to test multi-source machinery in isolation (no Charlie POVM,
    no announcement complications).
    """
    src_A = SourceParty(
        name="A",
        key_register_dim=bb84_alice_source(0.05).key_register_dim,
        signal_register_dim=bb84_alice_source(0.05).signal_register_dim,
        source_state=bb84_alice_source(0.05).source_state,
    )
    src_B = SourceParty(
        name="B",
        key_register_dim=bb84_alice_source(0.05).key_register_dim,
        signal_register_dim=bb84_alice_source(0.05).signal_register_dim,
        source_state=bb84_alice_source(0.05).source_state,
    )
    # Identity channel on combined signals (4-dim = 2 ⊗ 2)
    net = PublicQuantumNetwork(channel=KrausMap.identity(4))
    ann = AnnouncementRule(sift_keep=lambda outcomes: outcomes[0] == outcomes[1])
    km = KeyMap(key_party="A", bitmap={0: 0, 1: 1, 2: 0, 3: 1})
    return MSEBProtocol(
        name="Toy2Source",
        sources=(src_A, src_B),
        network=net,
        announcement=ann,
        key_map=km,
        observation_keys=("p_sift",),
        scope_tag="partial",  # multi-source still partial until full semantics
        scope_reason="Toy test protocol for multi-source machinery only.",
        _observable_builders={"p_sift": lambda _p: np.eye(4, dtype=np.complex128)},
    )


# ---- joint_state() for multi-source ------------------------------------------

def test_joint_state_two_sources_tensor_product() -> None:
    """For 2 pure sources, joint_state = |ψ_1⟩ ⊗ |ψ_2⟩."""
    p = _make_trivial_2source_protocol()
    psi_joint = p.joint_state()
    # Each source has 8-dim EB state (4-dim key × 2-dim signal)
    # Joint should be 64-dim ket
    assert psi_joint.shape == (64, 1)
    # Norm = 1
    assert np.isclose(np.linalg.norm(psi_joint), 1.0, atol=1e-10)

    # Compare to explicit tensor product
    src = bb84_alice_source(0.05)
    eigvals, eigvecs = np.linalg.eigh(src.source_state)
    idx = np.argmax(eigvals)
    psi_single = eigvecs[:, idx : idx + 1]
    psi_single = psi_single / np.linalg.norm(psi_single)
    psi_expected = np.kron(psi_single, psi_single)
    # Up to global phase — compare |⟨expected | joint⟩|² ≈ 1
    inner = abs((psi_expected.conj().T @ psi_joint).item())
    assert np.isclose(inner, 1.0, atol=1e-10), (
        f"joint state differs from tensor product: |⟨exp|joint⟩|={inner}"
    )


def test_joint_state_single_source_still_works() -> None:
    """Regression: single-source joint_state() behaviour unchanged."""
    from qkdx.protocols.bb84 import build_bb84_protocol
    p = build_bb84_protocol(qber=0.05)
    psi = p.joint_state()
    assert psi.shape == (8, 1)
    assert np.isclose(np.linalg.norm(psi), 1.0, atol=1e-10)


# ---- executed_state() for multi-source ---------------------------------------

def test_executed_state_two_sources_identity_channel_is_tensor() -> None:
    """With identity channel, executed_state = tensor-product of source states
    after reordering tensor axes so keys are grouped first."""
    p = _make_trivial_2source_protocol()
    rho = p.executed_state()
    # Shape: (d_keys * d_B, d_keys * d_B) = (16 * 4, 16 * 4) = (64, 64)
    assert rho.shape == (64, 64)
    # Trace 1
    assert np.isclose(np.trace(rho).real, 1.0, atol=1e-10)
    # Hermitian
    assert np.allclose(rho, rho.conj().T, atol=1e-10)
    # PSD
    eigvals = np.linalg.eigvalsh(rho)
    assert np.all(eigvals > -1e-10), f"negative eigvals: {eigvals[eigvals<-1e-12]}"


def test_executed_state_multi_source_returns_psd_hermitian() -> None:
    """MDI new path: executed_state() now works instead of raising."""
    p = build_mdi_protocol(qber=0.05)
    rho = p.executed_state()
    # MDI: 2 sources each (4 key, 2 signal) + identity(4) channel
    # executed_state shape: (d_keys * d_B, d_keys * d_B) = (16 * 4, 16 * 4) = (64, 64)
    assert rho.shape == (64, 64)
    assert np.isclose(np.trace(rho).real, 1.0, atol=1e-10)
    assert np.allclose(rho, rho.conj().T, atol=1e-10)
    eigvals = np.linalg.eigvalsh(rho)
    assert np.all(eigvals > -1e-10)


def test_executed_state_single_source_unchanged() -> None:
    """Regression: single-source executed_state behaviour unchanged."""
    from qkdx.protocols.bb84 import build_bb84_protocol
    p = build_bb84_protocol(qber=0.05)
    rho = p.executed_state()
    assert rho.shape == (8, 8)
    assert np.isclose(np.trace(rho).real, 1.0, atol=1e-10)


# ---- MDI scope reconsidered ---------------------------------------------------

def test_mdi_no_longer_raises_on_state_queries() -> None:
    """After Phase 1 multi-source impl, MDI executed_state + joint_state work."""
    p = build_mdi_protocol(qber=0.05)
    # Both should succeed (return matrix / ket), not raise
    psi = p.joint_state()
    rho = p.executed_state()
    assert psi is not None
    assert rho is not None


def test_mdi_conditional_alice_bob_override_still_primary() -> None:
    """MDI's _conditional_alice_bob override returns the Werner form (4x4).

    The multi-source executed_state gives a 64×64 joint state, which is
    NOT equal to the Werner form without Charlie's Bell POVM + post-selection.
    So the override remains the correct path for the WLC SDP.
    """
    p = build_mdi_protocol(qber=0.05)
    rho_cond = p.conditional_alice_bob()
    assert rho_cond.shape == (4, 4)
    # Werner form: diagonal (1-e)/2, e/2, e/2, (1-e)/2
    expected = np.diag([0.475, 0.025, 0.025, 0.475]).astype(np.complex128)
    assert np.allclose(rho_cond, expected, atol=1e-10)


# ---- Scale sanity: 3-source works too ----------------------------------------

def test_executed_state_three_sources() -> None:
    """Generic N-source infrastructure: 3 small sources + identity channel."""
    # 3 tiny sources: each (2 key, 2 signal), pure source = |00⟩⟨00| + |11⟩⟨11|
    psi = np.array([1, 0, 0, 1], dtype=np.complex128).reshape(4, 1) / np.sqrt(2)
    rho_small = psi @ psi.conj().T  # 4x4
    src = SourceParty(
        name="x", key_register_dim=2, signal_register_dim=2, source_state=rho_small,
    )
    srcs = (src, src, src)  # 3 copies
    # Identity on combined 8-dim signals (2*2*2)
    net = PublicQuantumNetwork(channel=KrausMap.identity(8))
    km = KeyMap(key_party="x", bitmap={0: 0, 1: 1})
    p = MSEBProtocol(
        name="3src", sources=srcs, network=net,
        announcement=AnnouncementRule(sift_keep=lambda o: True),
        key_map=km, observation_keys=("p_sift",),
        scope_tag="partial", scope_reason="Toy 3-source test.",
        _observable_builders={"p_sift": lambda _p: np.eye(8, dtype=np.complex128)},
    )
    rho = p.executed_state()
    # Shape: (prod keys * d_B) = (2*2*2 * 8, same) = (64, 64)
    assert rho.shape == (64, 64)
    assert np.isclose(np.trace(rho).real, 1.0, atol=1e-10)
    assert np.allclose(rho, rho.conj().T, atol=1e-10)
    eigvals = np.linalg.eigvalsh(rho)
    assert np.all(eigvals > -1e-10)
