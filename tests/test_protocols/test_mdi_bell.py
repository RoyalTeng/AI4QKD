"""Tests for build_mdi_bell_protocol — MDI with linear-optic Bell POVM channel.

Phase 1 Sub-Q2 Stage B:
    - 将 Charlie 的 Bell 测量从 `_conditional_alice_bob` override 提升到
      `PublicQuantumNetwork.channel`(linear_optic_bell_bsm)
    - executed_state() 现在返回 48×48 的 (K_A ⊗ K_B ⊗ C_announcement) 联合态
    - sift_keep 升级为 3-tuple: (θ_A, θ_B, c), 要求 basis match + Charlie 成功

Verification path:
    - 本 stage: channel 替换 + shape/invariant 检查; _conditional_alice_bob
      override 保留作为 fast path (WLC SDP 路径不变); scope 仍 partial
    - Next stage: 实现 _sift_projector,验证 default path 与 override 等价
      (那时才能升级到 covered)

Reference: qkdx/core/bell_povm.py linear_optic_bell_bsm; docs/PHASE1_LOG.md §3.6
"""
from __future__ import annotations

import numpy as np
import pytest

from qkdx.core.bell_povm import linear_optic_bell_bsm
from qkdx.protocol.base import MSEBProtocol
from qkdx.protocols.mdi import (
    build_mdi_bell_protocol, build_mdi_protocol, _mdi_bell_sift_keep,
)


# ---- Construction ------------------------------------------------------------

def test_build_mdi_bell_protocol_returns_MSEBProtocol() -> None:
    p = build_mdi_bell_protocol(qber=0.05)
    assert isinstance(p, MSEBProtocol)
    assert p.name == "MDI-QKD-Bell"
    assert len(p.sources) == 2


def test_mdi_bell_channel_is_linear_optic_bsm() -> None:
    p = build_mdi_bell_protocol(qber=0.05)
    ch = p.network.channel
    # linear_optic_bell_bsm: dim_in=4, dim_out=3
    assert ch.dim_in == 4
    assert ch.dim_out == 3
    assert len(ch.kraus) == 4  # Φ+, Ψ-, Φ-→fail, Ψ+→fail


def test_mdi_bell_scope_tag_still_partial() -> None:
    """Until default sift-projector path verified, scope remains partial."""
    p = build_mdi_bell_protocol(qber=0.05)
    assert p.scope_tag == "partial"
    assert "bell povm" in p.scope_reason.lower() or \
           "default path" in p.scope_reason.lower()


# ---- executed_state shape ----------------------------------------------------

def test_mdi_bell_executed_state_shape_48x48() -> None:
    """MDI + Bell POVM channel: executed_state on (K_A × K_B × C) = 4×4×3 = 48."""
    p = build_mdi_bell_protocol(qber=0.05)
    rho = p.executed_state()
    # d_keys = 4*4 = 16; d_B = 3 (Charlie announcement register); total 48×48
    assert rho.shape == (48, 48)


@pytest.mark.parametrize("qber", [0.0, 0.05, 0.10])
def test_mdi_bell_executed_state_is_density(qber: float) -> None:
    """Trace 1, Hermitian, PSD."""
    p = build_mdi_bell_protocol(qber=qber)
    rho = p.executed_state()
    assert np.isclose(np.trace(rho).real, 1.0, atol=1e-10), (
        f"qber={qber}: trace={np.trace(rho).real}"
    )
    assert np.allclose(rho, rho.conj().T, atol=1e-10)
    eigvals = np.linalg.eigvalsh(rho)
    assert np.all(eigvals > -1e-10), f"qber={qber}: min eig={eigvals.min()}"


# ---- Charlie announcement classical structure --------------------------------

def test_mdi_bell_executed_state_diagonal_in_C_register() -> None:
    """Classical announcement register C should appear diagonal.

    After Bell POVM measurement, the C register is a classical output.
    Tracing out K_A, K_B should give a diagonal 3×3 state (Charlie's
    marginal distribution over {Φ+, Ψ-, fail}).
    """
    p = build_mdi_bell_protocol(qber=0.05)
    rho = p.executed_state()
    # rho on (K_A ⊗ K_B ⊗ C) = 16 × 3 = 48
    # Trace out K_A, K_B (first 16 dims of tensor structure)
    # Reshape rho as (d_keys, d_C, d_keys, d_C) = (16, 3, 16, 3)
    rho_tensor = rho.reshape(16, 3, 16, 3)
    # Partial trace over K (axes 0, 2)
    rho_C = np.einsum('ikjk->ij', rho_tensor.transpose(0, 2, 1, 3)).reshape(3, 3) \
            if False else np.trace(rho_tensor, axis1=0, axis2=2)
    # Alternative correct partial trace over K_A⊗K_B (dim 16):
    rho_C_correct = np.zeros((3, 3), dtype=np.complex128)
    for k in range(16):
        rho_C_correct += rho[k * 3:(k + 1) * 3, k * 3:(k + 1) * 3]
    # Charlie marginal should be diagonal (classical outcome)
    off_diag = rho_C_correct - np.diag(np.diag(rho_C_correct))
    assert np.max(np.abs(off_diag)) < 1e-10, (
        f"Charlie marginal has non-diagonal entries: max={np.max(np.abs(off_diag))}"
    )


def test_mdi_bell_charlie_success_probability_half() -> None:
    """p(C ∈ {Φ+, Ψ-}) = 1/2 for linear-optic BSM on uniformly random input.

    For BB84 EB source + identity fibre (no loss), the A'⊗B' input to Charlie
    is maximally-mixed-like (each side weighted by Alice's source prior).
    Charlie's linear-optic BSM gives 1/2 success rate.
    """
    p = build_mdi_bell_protocol(qber=0.05)
    rho = p.executed_state()
    # Extract Charlie marginal
    rho_C = np.zeros((3, 3), dtype=np.complex128)
    for k in range(16):
        rho_C += rho[k * 3:(k + 1) * 3, k * 3:(k + 1) * 3]
    p_success = rho_C[0, 0].real + rho_C[1, 1].real  # Φ+ + Ψ-
    # Ideal BB84 EB source at qber=0.05 with fixed channel: expected ~ 0.5
    assert 0.45 < p_success < 0.55, (
        f"Charlie success probability {p_success:.4f} outside [0.45, 0.55]"
    )


# ---- sift_keep signature -----------------------------------------------------

def test_mdi_bell_sift_keep_basis_match_success() -> None:
    """sift_keep((θ_A, θ_B, c)) = True iff θ_A==θ_B AND c ∈ {0, 1}."""
    # Same basis (0==0), Charlie Φ+ (c=0)
    assert _mdi_bell_sift_keep((0, 0, 0)) is True
    # Same basis (1==1), Charlie Ψ- (c=1)
    assert _mdi_bell_sift_keep((1, 1, 1)) is True


def test_mdi_bell_sift_keep_basis_mismatch_rejected() -> None:
    assert _mdi_bell_sift_keep((0, 1, 0)) is False
    assert _mdi_bell_sift_keep((1, 0, 1)) is False


def test_mdi_bell_sift_keep_charlie_fail_rejected() -> None:
    assert _mdi_bell_sift_keep((0, 0, 2)) is False  # c=2 = fail
    assert _mdi_bell_sift_keep((1, 1, 2)) is False


def test_mdi_bell_sift_keep_too_short_returns_false() -> None:
    assert _mdi_bell_sift_keep((0, 0)) is False
    assert _mdi_bell_sift_keep((0,)) is False


# ---- Override still returns Werner for fast path -----------------------------

def test_mdi_bell_conditional_alice_bob_override_matches_werner() -> None:
    """Override still encodes the Werner state (identical to legacy MDI).

    The Bell POVM channel is now in the `channel`; the override remains as
    the fast path for WLC SDP (default path via sift_projector is next stage).
    """
    p_bell = build_mdi_bell_protocol(qber=0.05)
    p_legacy = build_mdi_protocol(qber=0.05)
    rho_bell = p_bell.conditional_alice_bob()
    rho_legacy = p_legacy.conditional_alice_bob()
    assert rho_bell.shape == (4, 4)
    assert rho_legacy.shape == (4, 4)
    assert np.allclose(rho_bell, rho_legacy, atol=1e-12), (
        "MDI-Bell conditional state must match legacy override"
    )


# ---- WLC SDP backward compat -------------------------------------------------

def test_mdi_bell_wlc_rate_matches_legacy() -> None:
    """WLC SDP on new builder gives same rate as legacy (via override fast path)."""
    from qkdx.numerics.wlc import wlc_key_rate
    qber = 0.05
    p_bell = build_mdi_bell_protocol(qber=qber)
    p_legacy = build_mdi_protocol(qber=qber)
    obs = {"qber_Z": qber, "qber_X": qber, "p_sift": 0.25}
    r_bell = wlc_key_rate(p_bell, obs, f_ec=1.0).key_rate
    r_legacy = wlc_key_rate(p_legacy, obs, f_ec=1.0).key_rate
    assert np.isclose(r_bell, r_legacy, rtol=1e-9, atol=1e-10), (
        f"MDI-Bell WLC rate {r_bell:.6f} != legacy {r_legacy:.6f}"
    )
