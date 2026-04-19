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
    build_mdi_bell_protocol, build_mdi_physical_protocol, build_mdi_protocol,
    _mdi_bell_sift_keep,
    mdi_full_physical_channel, _mdi_bell_conditional_from_executed,
    mdi_alice_source, mdi_bob_source,
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


# ---- Stage B.2: default-path (physical channel + sift + post-processing) -----

def test_full_physical_channel_trace_preserving() -> None:
    """64 composed Kraus (depol × depol × BSM) sum to identity."""
    net = mdi_full_physical_channel(arm_depol_p=0.05)
    ch = net.channel
    assert len(ch.kraus) == 64  # 4 (depol_A) × 4 (depol_B) × 4 (BSM)
    total = np.zeros((4, 4), dtype=np.complex128)
    for K in ch.kraus:
        total += K.conj().T @ K
    assert np.allclose(total, np.eye(4), atol=1e-12)


def _build_mdi_bell_physical(qber: float) -> MSEBProtocol:
    """Helper: MDI protocol with full physical channel (depol ⊗ depol → BSM).

    (Pre-dating public `build_mdi_physical_protocol`; retained for
    test_default_path_* tests that verify the extractor internals.)
    """
    from qkdx.protocol.base import AnnouncementRule, KeyMap
    src_A = mdi_alice_source(qber)
    src_B = mdi_bob_source(qber)
    net = mdi_full_physical_channel(arm_depol_p=qber)
    ann = AnnouncementRule(sift_keep=_mdi_bell_sift_keep)
    km = KeyMap(key_party="Alice", bitmap={0: 0, 1: 1, 2: 0, 3: 1})
    import warnings
    from qkdx.protocol.base import OutOfScopeWarning
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", OutOfScopeWarning)
        return MSEBProtocol(
            name="MDI-Bell-physical",
            sources=(src_A, src_B), network=net, announcement=ann, key_map=km,
            observation_keys=("p_sift",),
            scope_tag="partial", scope_reason="prototype full physical channel",
            _observable_builders={"p_sift": lambda _p: np.eye(4, dtype=np.complex128)},
        )


def test_default_path_equals_override_at_qber_zero() -> None:
    """At qber=0: default-path conditional = |Φ+⟩ pure state = override Werner."""
    p = _build_mdi_bell_physical(qber=0.0)
    rho_default = _mdi_bell_conditional_from_executed(p)
    expected = np.diag([0.5, 0.0, 0.0, 0.5]).astype(np.complex128)
    assert np.allclose(rho_default, expected, atol=1e-12), (
        f"default path at qber=0: got diag={np.diag(rho_default).real}"
    )


@pytest.mark.parametrize("q", [0.0, 0.02, 0.05, 0.08, 0.10, 0.15])
def test_default_path_effective_qber_matches_quadratic_formula(q: float) -> None:
    """[ADR] Effective QBER formula: e_eff = 4q/3 − 8q²/9.

    Derivation (for composition bb84_channel(q)⊗bb84_channel(q) then
    linear-optic BSM + classical bit-flip correction):
        - Per-arm single-qubit error rate in Z basis: 2q/3 (bb84_channel
          convention p=4q/3, so Z-QBER = p/2 = 2q/3)
        - Single-arm success probability: 1 − 2q/3
        - Joint agreement prob after BSM post-correction:
            P(both same OR both flipped) = (1-2q/3)² + (2q/3)²
            = 1 − 4q/3 + 8q²/9
        - Effective QBER = 1 − P(agreement) = 4q/3 − 8q²/9

    This test PINs the formula at 6 q values within `1e-4` absolute
    (Round 2 dev-reviewer response to loose `5e-3` tolerance).
    """
    p = build_mdi_physical_protocol(arm_depol_p=q)
    rho = _mdi_bell_conditional_from_executed(p)
    eff_qber = rho[1, 1].real * 2  # Werner diag[1] = e/2
    expected = 4 * q / 3 - 8 * q ** 2 / 9
    assert abs(eff_qber - expected) < 1e-4, (
        f"arm_depol_p={q}: eff QBER={eff_qber:.6f}, "
        f"expected 4q/3-8q²/9 = {expected:.6f} (diff={eff_qber-expected:.2e})"
    )


def test_build_mdi_physical_protocol_invalid_inputs() -> None:
    """Input validation for the new physical builder (all 4 boundary cases)."""
    with pytest.raises(ValueError, match="arm_depol_p"):
        build_mdi_physical_protocol(arm_depol_p=-0.01)
    with pytest.raises(ValueError, match="arm_depol_p"):
        build_mdi_physical_protocol(arm_depol_p=1.1)
    with pytest.raises(ValueError, match="p_sift"):
        build_mdi_physical_protocol(arm_depol_p=0.05, p_sift=0.0)
    with pytest.raises(ValueError, match="p_sift"):
        build_mdi_physical_protocol(arm_depol_p=0.05, p_sift=1.5)


def test_mdi_full_physical_channel_invalid_input() -> None:
    with pytest.raises(ValueError, match="arm_depol_p"):
        mdi_full_physical_channel(arm_depol_p=-0.01)
    with pytest.raises(ValueError, match="arm_depol_p"):
        mdi_full_physical_channel(arm_depol_p=1.5)


def test_build_mdi_physical_protocol_default_path_matches_override_at_q_zero() -> None:
    """At arm_depol_p=0: default path = |Φ+⟩ = override Werner."""
    p = build_mdi_physical_protocol(arm_depol_p=0.0)
    rho = p.conditional_alice_bob()
    expected = np.diag([0.5, 0, 0, 0.5]).astype(np.complex128)
    assert np.allclose(rho, expected, atol=1e-12)


def test_default_path_preserves_werner_form() -> None:
    """Default-path result is always in Werner form: diag(a, b, b, a) with 2a+2b=1."""
    for qber in [0.0, 0.02, 0.05, 0.08, 0.10]:
        p = _build_mdi_bell_physical(qber=qber)
        rho = _mdi_bell_conditional_from_executed(p)
        d = np.diag(rho).real
        # Check symmetry pattern
        assert abs(d[0] - d[3]) < 1e-10, f"qber={qber}: d[0]={d[0]}, d[3]={d[3]}"
        assert abs(d[1] - d[2]) < 1e-10, f"qber={qber}: d[1]={d[1]}, d[2]={d[2]}"
        # Trace = 1
        assert abs(sum(d) - 1.0) < 1e-10
        # Off-diagonal elements should be ~0 (Werner form is diagonal)
        off_diag = rho - np.diag(d)
        assert np.max(np.abs(off_diag)) < 1e-10


def test_default_path_reproduces_override_at_qber_zero_via_physical_channel() -> None:
    """At qber=0: physical channel + default path gives exact override Werner.

    Confirms that at zero noise, the MS-EB framework with full physical
    channel + default sift-projector route is equivalent to the override.
    (At qber > 0 they differ due to convention; see above tests.)
    """
    p_phys = _build_mdi_bell_physical(qber=0.0)
    rho_default = _mdi_bell_conditional_from_executed(p_phys)
    p_legacy = build_mdi_protocol(qber=0.0)
    rho_override = p_legacy.conditional_alice_bob()
    assert np.allclose(rho_default, rho_override, atol=1e-12), (
        f"qber=0: default diag={np.diag(rho_default).real}, "
        f"override diag={np.diag(rho_override).real}"
    )
