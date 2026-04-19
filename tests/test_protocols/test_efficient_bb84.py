"""Tests for qkdx/protocols/efficient_bb84.py (F4 Efficient BB84, Lo-Chau-Ardehali 2005).

Efficient BB84 biases basis choice toward Z (prob p_Z > 1/2):
    - Same 4-dim key register + 2-dim signal as BB84
    - Same depolarising channel
    - Same observables Γ_Z, Γ_X
    - DIFFERENT p_sift = p_Z^2 + (1-p_Z)^2 (> 0.5 when biased)
    - Same Z-sifted conditional state (Werner form — bias cancels in conditioning)
    - Key rate R = p_sift · (1 - 2h(e))  — higher than BB84's 0.5 · (1-2h(e))

Reference: Lo-Chau-Ardehali 2005, J. Cryptology 18:133.
"""
from __future__ import annotations

import numpy as np
import pytest

from qkdx.analytic.shor_preskill import shor_preskill_rate
from qkdx.numerics.wlc import wlc_key_rate
from qkdx.protocol.base import MSEBProtocol
from qkdx.protocols.efficient_bb84 import (
    build_efficient_bb84_protocol, efficient_bb84_alice_source,
)
from qkdx.utils.solvers import has_mosek


# ---- Protocol construction ----------------------------------------------------

def test_protocol_metadata() -> None:
    p = build_efficient_bb84_protocol(qber=0.05, p_Z=0.9)
    assert isinstance(p, MSEBProtocol)
    assert p.name == "EfficientBB84"
    assert p.scope_tag == "covered"
    assert len(p.sources) == 1
    assert p.sources[0].key_register_dim == 4
    assert p.sources[0].signal_register_dim == 2
    assert p.conditional_alice_bob_dim() == 4


def test_observation_keys() -> None:
    p = build_efficient_bb84_protocol(qber=0.05, p_Z=0.9)
    assert set(p.observation_keys) == {"qber_Z", "qber_X", "p_sift"}


def test_observables_are_hermitian_4x4() -> None:
    p = build_efficient_bb84_protocol(qber=0.05, p_Z=0.9)
    for key in ("qber_Z", "qber_X"):
        Gamma = p.observable(key)
        assert Gamma.shape == (4, 4)
        assert np.allclose(Gamma, Gamma.conj().T, atol=1e-10)


@pytest.mark.parametrize("p_Z", [0.51, 0.7, 0.9, 0.99])
def test_source_state_is_pure_normalized(p_Z: float) -> None:
    """Source is a pure EB state: PSD, trace 1, rank 1."""
    src = efficient_bb84_alice_source(qber=0.05, p_Z=p_Z)
    rho = src.source_state
    assert rho.shape == (8, 8)
    assert np.isclose(np.trace(rho).real, 1.0, atol=1e-10), (
        f"p_Z={p_Z}: trace={np.trace(rho).real}"
    )
    eigvals = np.linalg.eigvalsh(rho)
    assert np.all(eigvals > -1e-10)
    top2 = np.sort(eigvals)[-2:]
    assert np.isclose(top2[-1], 1.0, atol=1e-10), f"p_Z={p_Z}: top={top2[-1]}"
    assert np.isclose(top2[-2], 0.0, atol=1e-10), f"p_Z={p_Z}: second={top2[-2]}"


@pytest.mark.parametrize("p_Z", [0.51, 0.7, 0.9, 0.99])
def test_source_state_basis_weights(p_Z: float) -> None:
    """Tr over signal register gives classical bias: P(Z basis)=p_Z, P(X)=1-p_Z."""
    src = efficient_bb84_alice_source(qber=0.05, p_Z=p_Z)
    rho = src.source_state  # 8x8
    # Trace out signal register (dim 2) → 4x4 marginal on key register
    rho_key = np.zeros((4, 4), dtype=np.complex128)
    for a in range(4):
        for b in range(4):
            rho_key[a, b] = rho[2 * a, 2 * b] + rho[2 * a + 1, 2 * b + 1]
    # Diagonal: P(Z,0), P(Z,1), P(X,0), P(X,1)
    diag = np.diag(rho_key).real
    assert np.isclose(diag[0] + diag[1], p_Z, atol=1e-10), f"P(Z)={diag[0]+diag[1]}"
    assert np.isclose(diag[2] + diag[3], 1 - p_Z, atol=1e-10), (
        f"P(X)={diag[2]+diag[3]}"
    )


# ---- p_sift derivation --------------------------------------------------------

@pytest.mark.parametrize("p_Z", [0.51, 0.7, 0.9, 0.99])
def test_p_sift_formula(p_Z: float) -> None:
    """p_sift = p_Z^2 + (1-p_Z)^2 (both pick same basis, assuming Bob mirror-bias)."""
    p = build_efficient_bb84_protocol(qber=0.05, p_Z=p_Z)
    Gamma_psift = p.observable("p_sift")
    # Trace(Γ_psift · ρ_sifted) normalisation — here Γ_psift = (p_Z^2+(1-p_Z)^2)·I/4
    expected = p_Z ** 2 + (1 - p_Z) ** 2
    # Trace should equal expected (Γ_psift = expected · I/4 on 4-dim)
    assert np.isclose(np.trace(Gamma_psift).real, expected, atol=1e-12)


# ---- WLC SDP vs analytic ------------------------------------------------------

@pytest.mark.parametrize("qber,p_Z", [
    (0.01, 0.9),
    (0.05, 0.9),
    (0.05, 0.7),
    (0.05, 0.99),
    (0.08, 0.9),
])
def test_wlc_efficient_bb84_matches_analytic(qber: float, p_Z: float) -> None:
    """Efficient BB84 key rate = p_sift · (1 - 2h(e)).

    Equivalent to shor_preskill_rate(qber) · 2 · p_sift (since shor_preskill
    includes a 0.5 p_sift factor for symmetric BB84).
    """
    p = build_efficient_bb84_protocol(qber=qber, p_Z=p_Z)
    p_sift = p_Z ** 2 + (1 - p_Z) ** 2
    obs = {"qber_Z": qber, "qber_X": qber, "p_sift": p_sift}
    result = wlc_key_rate(p, obs, f_ec=1.0)

    R_bb84 = shor_preskill_rate(qber, f_ec=1.0)  # includes p_sift=0.5 factor
    R_expected = R_bb84 * (p_sift / 0.5)

    tol = dict(rel=0.01, abs=5e-4) if has_mosek() else dict(rel=0.02, abs=1e-3)
    assert result.key_rate == pytest.approx(R_expected, **tol), (
        f"qber={qber}, p_Z={p_Z}: WLC={result.key_rate:.6f}, "
        f"expected={R_expected:.6f}, p_sift={p_sift}"
    )


def test_efficient_bb84_beats_bb84_at_p_Z_09() -> None:
    """At p_Z=0.9 and qber=0.05: R_efficient / R_bb84 ≈ 0.82/0.5 = 1.64 (f_ec consistent)."""
    qber = 0.05
    p_Z = 0.9
    f_ec = 1.0
    p = build_efficient_bb84_protocol(qber=qber, p_Z=p_Z)
    p_sift = p_Z ** 2 + (1 - p_Z) ** 2  # 0.82
    obs = {"qber_Z": qber, "qber_X": qber, "p_sift": p_sift}
    r_eff = wlc_key_rate(p, obs, f_ec=f_ec).key_rate
    r_bb84 = shor_preskill_rate(qber, f_ec=f_ec)  # 0.5 * (1 - (1+f_ec)h)
    ratio = r_eff / r_bb84
    assert ratio == pytest.approx(p_sift / 0.5, rel=0.02), (
        f"ratio={ratio}, expected={p_sift/0.5}"
    )


# ---- Input validation ---------------------------------------------------------

def test_invalid_qber() -> None:
    with pytest.raises(ValueError, match="QBER"):
        build_efficient_bb84_protocol(qber=-0.01, p_Z=0.9)
    with pytest.raises(ValueError, match="QBER"):
        build_efficient_bb84_protocol(qber=1.1, p_Z=0.9)


@pytest.mark.parametrize("p_Z", [0.0, 0.3, 0.5, 1.0, 1.5])
def test_invalid_p_Z(p_Z: float) -> None:
    """p_Z must be in (0.5, 1.0) strictly for efficient BB84 (biased toward Z)."""
    with pytest.raises(ValueError, match="p_Z"):
        build_efficient_bb84_protocol(qber=0.05, p_Z=p_Z)
