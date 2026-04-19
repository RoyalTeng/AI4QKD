"""Tests for qkdx/protocols/sarg04.py (F3 SARG04, simplified MS-EB model).

**Scope note**: This is a *partial* implementation of SARG04. The sifted
conditional state uses a simplified Werner form parametrized by
    q(e) = e / (1 + 2e)                   [effective sifted error]
    p_sift = 1/4 + e/2                    [effective sift rate]
derived from uniform pair-selection + depolarizing channel. This matches
the qualitative SARG04 behavior (1/4 sift, non-Shor-Preskill threshold)
but does not claim exact fidelity to Koashi 2005 (which gives ~9.68%
threshold; the simplified model yields ~14.1%).

References:
- Scarani-Acín-Ribordy-Gisin 2004, PRL 92:057901
- Koashi 2005, quant-ph/0507154
- Fung-Tamaki-Lo 2006, PRA 73:012337
"""
from __future__ import annotations

import numpy as np
import pytest

from qkdx.numerics.wlc import wlc_key_rate
from qkdx.protocol.base import MSEBProtocol
from qkdx.protocols.sarg04 import (
    build_sarg04_protocol, sarg04_alice_source,
    _sarg04_sifted_qber, _sarg04_p_sift,
)


# ---- Derived-quantity helpers -------------------------------------------------

@pytest.mark.parametrize("e,expected_q", [
    (0.0, 0.0),
    (0.05, 0.05 / 1.1),
    (0.1, 0.1 / 1.2),
    (0.2, 0.2 / 1.4),
])
def test_sarg04_sifted_qber_formula(e: float, expected_q: float) -> None:
    """q(e) = e / (1 + 2e)."""
    assert _sarg04_sifted_qber(e) == pytest.approx(expected_q, abs=1e-12)


@pytest.mark.parametrize("e,expected_p", [
    (0.0, 0.25),
    (0.05, 0.275),
    (0.1, 0.30),
    (0.2, 0.35),
])
def test_sarg04_p_sift_formula(e: float, expected_p: float) -> None:
    """p_sift(e) = 1/4 + e/2."""
    assert _sarg04_p_sift(e) == pytest.approx(expected_p, abs=1e-12)


# ---- Protocol construction ----------------------------------------------------

def test_protocol_metadata() -> None:
    p = build_sarg04_protocol(qber=0.05)
    assert isinstance(p, MSEBProtocol)
    assert p.name == "SARG04"
    assert p.scope_tag == "partial"
    assert p.scope_reason is not None
    assert "simplified" in p.scope_reason.lower() or "partial" in p.scope_reason.lower()
    assert len(p.sources) == 1
    assert p.sources[0].key_register_dim == 4
    assert p.sources[0].signal_register_dim == 2
    assert p.conditional_alice_bob_dim() == 4


def test_observation_keys() -> None:
    p = build_sarg04_protocol(qber=0.05)
    assert set(p.observation_keys) == {"qber_Z", "qber_X", "p_sift"}


def test_observables_are_hermitian_4x4() -> None:
    p = build_sarg04_protocol(qber=0.05)
    for key in ("qber_Z", "qber_X"):
        Gamma = p.observable(key)
        assert Gamma.shape == (4, 4)
        assert np.allclose(Gamma, Gamma.conj().T, atol=1e-10)


@pytest.mark.parametrize("qber", [0.0, 0.03, 0.05, 0.08, 0.10])
def test_source_state_is_pure_normalized(qber: float) -> None:
    """Source EB state: rank 1, trace 1 (same form as BB84 source)."""
    src = sarg04_alice_source(qber=qber)
    rho = src.source_state
    assert rho.shape == (8, 8)
    assert np.isclose(np.trace(rho).real, 1.0, atol=1e-10)
    eigvals = np.linalg.eigvalsh(rho)
    top = np.sort(eigvals)[-1]
    assert np.isclose(top, 1.0, atol=1e-10)


# ---- WLC SDP behavior ---------------------------------------------------------

@pytest.mark.parametrize("qber", [0.0, 0.02, 0.05, 0.08])
def test_wlc_sarg04_gives_positive_rate_below_threshold(qber: float) -> None:
    """Below ~14% simplified threshold: WLC rate > 0."""
    p = build_sarg04_protocol(qber=qber)
    q = _sarg04_sifted_qber(qber)
    p_s = _sarg04_p_sift(qber)
    obs = {"qber_Z": q, "qber_X": q, "p_sift": p_s}
    result = wlc_key_rate(p, obs, f_ec=1.0)
    assert result.key_rate > 0.0, f"qber={qber}: WLC rate={result.key_rate:.6f}"


def test_wlc_sarg04_above_simplified_threshold_gives_zero() -> None:
    """Simplified threshold ≈ 14.1%; qber=0.16 must give ≤ 0 rate."""
    qber = 0.16
    p = build_sarg04_protocol(qber=qber)
    q = _sarg04_sifted_qber(qber)
    p_s = _sarg04_p_sift(qber)
    obs = {"qber_Z": q, "qber_X": q, "p_sift": p_s}
    result = wlc_key_rate(p, obs, f_ec=1.0)
    assert result.key_rate <= 5e-4, (
        f"qber={qber}: WLC rate={result.key_rate:.6f} — above threshold should be 0"
    )


def test_wlc_sarg04_matches_werner_formula() -> None:
    """WLC rate should match p_sift · (1 - 2h(q)) in simplified model."""
    qber = 0.05
    q = _sarg04_sifted_qber(qber)
    p_s = _sarg04_p_sift(qber)
    p = build_sarg04_protocol(qber=qber)
    obs = {"qber_Z": q, "qber_X": q, "p_sift": p_s}
    result = wlc_key_rate(p, obs, f_ec=1.0)

    # Analytic Werner-model prediction: R = p_s · (1 - 2h(q))
    h_q = -q * np.log2(q) - (1 - q) * np.log2(1 - q) if q > 0 else 0.0
    expected = p_s * (1.0 - 2.0 * h_q)
    assert result.key_rate == pytest.approx(expected, rel=0.02, abs=1e-3)


# ---- Input validation ---------------------------------------------------------

def test_invalid_qber_negative() -> None:
    with pytest.raises(ValueError, match="QBER"):
        build_sarg04_protocol(qber=-0.01)


def test_invalid_qber_above_one() -> None:
    with pytest.raises(ValueError, match="QBER"):
        build_sarg04_protocol(qber=1.1)
