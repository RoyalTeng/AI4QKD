"""Tests for qkdx/protocols/mdi.py + WLC SDP on MDI-QKD (ideal case)."""
from __future__ import annotations

import numpy as np
import pytest

from qkdx.analytic.gllp import mdi_ideal_symmetric_rate
from qkdx.analytic.shor_preskill import shor_preskill_rate
from qkdx.numerics.wlc import wlc_key_rate
from qkdx.protocol.base import MSEBProtocol
from qkdx.protocols.bb84 import build_bb84_protocol
from qkdx.protocols.mdi import build_mdi_protocol
from qkdx.utils.solvers import has_mosek


# ---- Protocol construction ----------------------------------------------------

def test_mdi_has_two_sources() -> None:
    p = build_mdi_protocol(qber=0.05)
    assert isinstance(p, MSEBProtocol)
    assert p.name == "MDI-QKD"
    assert p.scope_tag == "covered"
    assert len(p.sources) == 2
    assert p.sources[0].name == "Alice"
    assert p.sources[1].name == "Bob"


def test_mdi_has_bb84_conditional_dim() -> None:
    p = build_mdi_protocol(qber=0.05)
    assert p.conditional_alice_bob_dim() == 4


def test_mdi_observation_keys() -> None:
    p = build_mdi_protocol(qber=0.05)
    assert set(p.observation_keys) == {"qber_Z", "qber_X", "p_sift"}


def test_mdi_observables_hermitian() -> None:
    p = build_mdi_protocol(qber=0.05)
    for key in ("qber_Z", "qber_X"):
        Gamma = p.observable(key)
        assert Gamma.shape == (4, 4)
        assert np.allclose(Gamma, Gamma.conj().T, atol=1e-12)


# ---- WLC SDP vs analytic ------------------------------------------------------

_FALLBACK_TOL = dict(rel=0.02, abs=1e-3)
_MOSEK_TOL = dict(rel=0.01, abs=5e-4)


@pytest.mark.parametrize("qber", [0.01, 0.02, 0.05, 0.08, 0.10])
def test_wlc_mdi_matches_analytic(qber: float) -> None:
    """WLC SDP MDI key rate matches ideal GLLP/MDI analytic within acceptance.

    Fallback (CLARABEL Frank-Wolfe): rel=0.02, abs=1e-3.
    Primary (MOSEK): rel=0.01, abs=5e-4.
    """
    p = build_mdi_protocol(qber=qber, p_sift=0.25)
    obs = {"qber_Z": qber, "qber_X": qber, "p_sift": 0.25}
    result = wlc_key_rate(p, obs, f_ec=1.0)

    analytic = mdi_ideal_symmetric_rate(qber, f_ec=1.0)
    tol = _MOSEK_TOL if has_mosek() else _FALLBACK_TOL
    assert result.key_rate == pytest.approx(analytic, **tol), (
        f"QBER={qber}: WLC={result.key_rate:.6f}, analytic={analytic:.6f}, "
        f"|diff|={abs(result.key_rate - analytic):.2e}, solver={result.solver}"
    )


def test_wlc_mdi_is_bb84_halved() -> None:
    """Ideal symmetric MDI WLC rate = BB84 WLC rate × 0.5 (p_sift ratio 0.25/0.5)."""
    qber = 0.05
    p_mdi = build_mdi_protocol(qber=qber, p_sift=0.25)
    obs_mdi = {"qber_Z": qber, "qber_X": qber, "p_sift": 0.25}
    r_mdi = wlc_key_rate(p_mdi, obs_mdi, f_ec=1.0)

    p_bb = build_bb84_protocol(qber=qber)
    obs_bb = {"qber_Z": qber, "qber_X": qber, "p_sift": 0.5}
    r_bb = wlc_key_rate(p_bb, obs_bb, f_ec=1.0)

    tol = _MOSEK_TOL if has_mosek() else _FALLBACK_TOL
    assert r_mdi.key_rate == pytest.approx(r_bb.key_rate / 2.0, **tol)


def test_mdi_zero_qber() -> None:
    p = build_mdi_protocol(qber=0.0, p_sift=0.25)
    obs = {"qber_Z": 0.0, "qber_X": 0.0, "p_sift": 0.25}
    result = wlc_key_rate(p, obs, f_ec=1.0)
    tol = _MOSEK_TOL if has_mosek() else _FALLBACK_TOL
    assert result.key_rate == pytest.approx(0.25, **tol)


# ---- Input validation ---------------------------------------------------------

def test_invalid_qber() -> None:
    with pytest.raises(ValueError, match="QBER"):
        build_mdi_protocol(qber=-0.01)
    with pytest.raises(ValueError, match="QBER"):
        build_mdi_protocol(qber=1.1)


def test_invalid_p_sift() -> None:
    with pytest.raises(ValueError, match="p_sift"):
        build_mdi_protocol(qber=0.05, p_sift=0.0)
    with pytest.raises(ValueError, match="p_sift"):
        build_mdi_protocol(qber=0.05, p_sift=1.5)
